/**
 * CUBE-REV 0.6.11 result collector.
 *
 * Automatic submission uses a token-free public deployment handshake and a two-stage confirmation protocol:
 * 1. The page and collector verify a stable collector ID, protocol, and experiment version.
 * 2. doPost stores or deduplicates the JSON file.
 * 3. The collector returns an acknowledgement and exposes a short-lived
 *    receipt endpoint so the experiment can verify that storage completed.
 */
const EXPECTED_PROJECT = 'CUBE-REV';
const EXPECTED_VERSION = '0.6.11';
const MAX_JSON_BYTES = 20 * 1024 * 1024;
const PROP_FOLDER_ID = 'CUBE_REV_FOLDER_ID';
const PROP_SHEET_ID = 'CUBE_REV_SHEET_ID';
const COLLECTOR_ID = 'CUBE-REV-0611-MAIN';
const PROTOCOL_VERSION = 'receipt-v2';
const RECEIPT_CACHE_PREFIX = 'CUBE_REV_RECEIPT_';
const RECEIPT_CACHE_SECONDS = 10 * 60;
const SUBMISSION_HEADERS = [
  'received_at',
  'session_id',
  'participant_code',
  'version',
  'mode',
  'trial_count',
  'json_bytes',
  'drive_file_id',
  'status',
  'submission_method'
];

function setupCollector() {
  const resources = ensureCollectorResources_();
  const result = {
    folderId: resources.folder.getId(),
    sheetId: resources.book.getId(),
    collectorId: COLLECTOR_ID,
    protocolVersion: PROTOCOL_VERSION,
    expectedVersion: EXPECTED_VERSION,
    manualUploadUrl: ScriptApp.getService().getUrl() || 'Deploy the script as a web app first.',
    receiptProtocol: 'post_then_jsonp_receipt_v2'
  };
  console.log(JSON.stringify(result, null, 2));
  return result;
}

function doGet(e) {
  const params = (e && e.parameter) || {};
  const action = String(params.action || '').toLowerCase();

  if (action === 'health') {
    return handleHealthRequest_(params);
  }

  if (action === 'receipt') {
    return handleReceiptRequest_(params);
  }

  if (String(params.format || '').toLowerCase() === 'json') {
    return ContentService.createTextOutput(JSON.stringify({
      ok: true,
      service: 'CUBE-REV collector',
      expected_version: EXPECTED_VERSION,
      collector_id: COLLECTOR_ID,
      protocol_version: PROTOCOL_VERSION,
      manual_upload_available: true,
      receipt_confirmation_available: true,
      server_time: new Date().toISOString()
    })).setMimeType(ContentService.MimeType.JSON);
  }

  return HtmlService.createHtmlOutput(buildManualUploadPage_(String(params.expected_file || '')))
    .setTitle('CUBE-REV 결과 제출')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

function doPost(e) {
  const params = (e && e.parameter) || {};
  const nonce = String(params.submission_nonce || '');
  const claimedSessionId = String(params.session_id || '');

  try {
    validateAutomaticRequestIdentity_(nonce, claimedSessionId);

    validateProtocolRequest_(params, true);

    const encoding = String(params.encoding || 'json');
    const transmittedPayload = String(params.payload || '');
    if (!transmittedPayload) throw new Error('Empty payload.');

    const jsonText = decodePayload_(transmittedPayload, encoding);
    const claimedChecksum = String(params.checksum_fnv1a32 || '').toLowerCase();
    if (!/^[0-9a-f]{8}$/.test(claimedChecksum)) throw new Error('Invalid payload checksum.');
    const actualChecksum = fnv1a32Hex_(jsonText);
    if (actualChecksum !== claimedChecksum) throw new Error('Payload checksum mismatch.');
    const stored = storeJson_(jsonText, 'automatic_form_post', claimedSessionId);
    const receipt = makePublicReceipt_({
      ok: true,
      nonce: nonce,
      sessionId: stored.session_id,
      status: stored.status,
      fileName: stored.file_name,
      receivedAt: stored.received_at,
      confirmationSource: 'doPost_store_complete',
      checksum: actualChecksum
    });
    saveReceipt_(receipt);
    return ackHtml_(receipt);
  } catch (error) {
    console.error(error && error.stack ? error.stack : error);
    const receipt = makePublicReceipt_({
      ok: false,
      nonce: nonce,
      sessionId: claimedSessionId,
      status: 'error',
      error: String(error && error.message ? error.message : error),
      confirmationSource: 'doPost_error'
    });
    if (isValidNonce_(nonce) && isValidSessionId_(claimedSessionId)) {
      saveReceipt_(receipt);
    }
    return ackHtml_(receipt);
  }
}

/** Called from the manual upload page through google.script.run. */
function submitManualJson(jsonText) {
  try {
    return { ok: true, ...storeJson_(String(jsonText || ''), 'manual_upload_portal', '') };
  } catch (error) {
    console.error(error && error.stack ? error.stack : error);
    throw new Error(String(error && error.message ? error.message : error));
  }
}

function validateAutomaticRequestIdentity_(nonce, sessionId) {
  if (!isValidNonce_(nonce)) throw new Error('Invalid submission nonce.');
  if (!isValidSessionId_(sessionId)) throw new Error('Invalid CUBE-REV session ID.');
}

function validateProtocolRequest_(params, requireVersion) {
  if (String(params.collector_id || '') !== COLLECTOR_ID) {
    throw new Error('Collector ID mismatch.');
  }
  if (String(params.protocol_version || '') !== PROTOCOL_VERSION) {
    throw new Error('Collector protocol mismatch.');
  }
  if (requireVersion && String(params.version || '') !== EXPECTED_VERSION) {
    throw new Error('Experiment version mismatch.');
  }
}

function isValidNonce_(nonce) {
  return /^[0-9a-f]{24}$/i.test(String(nonce || ''));
}

function isValidSessionId_(sessionId) {
  return /^CR-\d{14}-[0-9a-f]{12}$/i.test(String(sessionId || ''));
}

function makePublicReceipt_(options) {
  const receivedAt = options.receivedAt || new Date().toISOString();
  return {
    type: 'CUBE_REV_COLLECTOR_ACK',
    ok: options.ok === true,
    status: String(options.status || (options.ok ? 'stored' : 'error')),
    submission_nonce: String(options.nonce || ''),
    session_id: String(options.sessionId || ''),
    file_name: options.fileName ? String(options.fileName) : null,
    received_at: receivedAt,
    receipt_code: options.ok ? makeReceiptCode_(String(options.sessionId || ''), receivedAt) : null,
    confirmation_source: String(options.confirmationSource || ''),
    checksum_fnv1a32: options.checksum ? String(options.checksum).toLowerCase() : null,
    error: options.error ? String(options.error) : null
  };
}

function makeReceiptCode_(sessionId, receivedAt) {
  const bytes = Utilities.computeDigest(
    Utilities.DigestAlgorithm.SHA_256,
    sessionId + '|' + receivedAt,
    Utilities.Charset.UTF_8
  );
  return Utilities.base64EncodeWebSafe(bytes).replace(/=+$/g, '').slice(0, 12).toUpperCase();
}

function receiptCacheKey_(nonce) {
  return RECEIPT_CACHE_PREFIX + nonce;
}

function saveReceipt_(receipt) {
  CacheService.getScriptCache().put(
    receiptCacheKey_(receipt.submission_nonce),
    JSON.stringify(receipt),
    RECEIPT_CACHE_SECONDS
  );
}

function readReceipt_(nonce) {
  const raw = CacheService.getScriptCache().get(receiptCacheKey_(nonce));
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch (_) {
    return null;
  }
}

function handleHealthRequest_(params) {
  const callback = validateJsonpCallback_(String(params.callback || ''));
  const requestedVersion = String(params.version || '');
  const serviceUrl = ScriptApp.getService().getUrl() || '';
  const deploymentMatch = serviceUrl.match(/\/s\/([^/]+)\/exec$/);
  const payload = {
    type: 'CUBE_REV_COLLECTOR_HEALTH',
    ok: true,
    service: 'CUBE-REV collector',
    expected_version: EXPECTED_VERSION,
    requested_version: requestedVersion || null,
    version_match: requestedVersion ? requestedVersion === EXPECTED_VERSION : null,
    collector_id: COLLECTOR_ID,
    protocol_version: PROTOCOL_VERSION,
    collector_match: String(params.collector_id || '') === COLLECTOR_ID,
    protocol_match: String(params.protocol_version || '') === PROTOCOL_VERSION,
    receipt_confirmation_available: true,
    manual_upload_available: true,
    deployment_id: deploymentMatch ? deploymentMatch[1].slice(0, 16) : null,
    server_time: new Date().toISOString()
  };
  return jsonpOutput_(callback, payload);
}

function handleReceiptRequest_(params) {
  const callback = validateJsonpCallback_(String(params.callback || ''));
  const nonce = String(params.submission_nonce || '');
  const sessionId = String(params.session_id || '');

  let payload;
  try {
    validateAutomaticRequestIdentity_(nonce, sessionId);
    validateProtocolRequest_(params, true);

    const cached = readReceipt_(nonce);
    if (cached && cached.session_id === sessionId) {
      payload = cached;
    } else {
      const stored = findStoredSession_(sessionId);
      payload = stored
        ? makePublicReceipt_({
            ok: true,
            nonce: nonce,
            sessionId: sessionId,
            status: 'stored',
            fileName: stored.file_name,
            receivedAt: stored.received_at,
            confirmationSource: 'drive_lookup',
            checksum: stored.checksum_fnv1a32
          })
        : {
            type: 'CUBE_REV_COLLECTOR_ACK',
            ok: true,
            status: 'pending',
            submission_nonce: nonce,
            session_id: sessionId,
            file_name: null,
            received_at: null,
            receipt_code: null,
            confirmation_source: 'receipt_poll',
            checksum_fnv1a32: null,
            error: null
          };
    }
  } catch (error) {
    payload = {
      type: 'CUBE_REV_COLLECTOR_ACK',
      ok: false,
      status: 'error',
      submission_nonce: nonce,
      session_id: sessionId,
      file_name: null,
      received_at: new Date().toISOString(),
      receipt_code: null,
      confirmation_source: 'receipt_request_error',
      checksum_fnv1a32: null,
      error: String(error && error.message ? error.message : error)
    };
  }

  return jsonpOutput_(callback, payload);
}

function validateJsonpCallback_(callback) {
  if (!/^[A-Za-z_$][0-9A-Za-z_$]{0,120}$/.test(callback)) {
    throw new Error('Invalid JSONP callback.');
  }
  return callback;
}

function jsonpOutput_(callback, payload) {
  const safeJson = JSON.stringify(payload).replace(/</g, '\\u003c');
  return ContentService
    .createTextOutput(callback + '(' + safeJson + ');')
    .setMimeType(ContentService.MimeType.JAVASCRIPT);
}

function findStoredSession_(sessionId) {
  if (!isValidSessionId_(sessionId)) return null;
  const resources = ensureCollectorResources_();
  const fileName = safeFileName_(sessionId + '.json');
  const files = resources.folder.getFilesByName(fileName);
  if (!files.hasNext()) return null;
  const file = files.next();
  return {
    file_name: fileName,
    received_at: file.getDateCreated().toISOString(),
    checksum_fnv1a32: fnv1a32Hex_(file.getBlob().getDataAsString('UTF-8'))
  };
}

function ensureCollectorResources_() {
  const props = PropertiesService.getScriptProperties();
  let folderId = props.getProperty(PROP_FOLDER_ID);
  let sheetId = props.getProperty(PROP_SHEET_ID);
  let folder;
  let book;

  if (folderId) {
    try { folder = DriveApp.getFolderById(folderId); } catch (_) { folder = null; }
  }
  if (!folder) {
    folder = DriveApp.createFolder('CUBE-REV 0.6.11 submissions');
    props.setProperty(PROP_FOLDER_ID, folder.getId());
  } else {
    folder.setName('CUBE-REV submissions');
  }

  if (sheetId) {
    try { book = SpreadsheetApp.openById(sheetId); } catch (_) { book = null; }
  }
  if (!book) {
    book = SpreadsheetApp.create('CUBE-REV submission index');
    props.setProperty(PROP_SHEET_ID, book.getId());
  } else {
    DriveApp.getFileById(book.getId()).setName('CUBE-REV submission index');
  }

  const sheet = book.getSheets()[0];
  sheet.setName('submissions');
  sheet.getRange(1, 1, 1, SUBMISSION_HEADERS.length).setValues([SUBMISSION_HEADERS]);
  sheet.setFrozenRows(1);

  return { props: props, folder: folder, book: book, sheet: sheet };
}

function storeJson_(jsonText, submissionMethod, claimedSessionId) {
  if (!jsonText) throw new Error('JSON file is empty.');
  const jsonBytes = Utilities.newBlob(jsonText).getBytes().length;
  if (jsonBytes > MAX_JSON_BYTES) throw new Error('The JSON file exceeds the 20 MB collector limit.');

  let record;
  try {
    record = JSON.parse(jsonText);
  } catch (_) {
    throw new Error('The selected file is not valid JSON.');
  }
  validateRecord_(record, claimedSessionId);

  const resources = ensureCollectorResources_();
  const fileName = safeFileName_(record.session_id + '.json');
  const lock = LockService.getScriptLock();
  lock.waitLock(15000);
  try {
    const existing = resources.folder.getFilesByName(fileName);
    if (existing.hasNext()) {
      const file = existing.next();
      return {
        status: 'duplicate',
        session_id: record.session_id,
        drive_file_id: file.getId(),
        file_name: fileName,
        received_at: file.getDateCreated().toISOString(),
        submission_method: submissionMethod
      };
    }

    const file = resources.folder.createFile(
      Utilities.newBlob(jsonText, 'application/json', fileName)
    );
    const receivedAt = new Date().toISOString();
    resources.sheet.appendRow([
      receivedAt,
      record.session_id,
      record.participant_code || '',
      record.version,
      record.mode || '',
      Array.isArray(record.trials) ? record.trials.length : '',
      jsonBytes,
      file.getId(),
      'stored',
      submissionMethod
    ]);
    SpreadsheetApp.flush();

    return {
      status: 'stored',
      session_id: record.session_id,
      drive_file_id: file.getId(),
      file_name: fileName,
      received_at: receivedAt,
      submission_method: submissionMethod
    };
  } finally {
    lock.releaseLock();
  }
}

function validateRecord_(record, claimedSessionId) {
  if (!record || typeof record !== 'object') throw new Error('JSON root must be an object.');
  if (record.project !== EXPECTED_PROJECT) throw new Error('This is not a CUBE-REV result file.');
  if (record.version !== EXPECTED_VERSION) {
    throw new Error('Expected version ' + EXPECTED_VERSION + ', but received ' + record.version + '.');
  }
  if (!isValidSessionId_(record.session_id)) throw new Error('Invalid CUBE-REV session ID.');
  if (claimedSessionId && claimedSessionId !== record.session_id) throw new Error('Session ID mismatch.');
  if (!Array.isArray(record.trials)) throw new Error('The result file does not contain a trials array.');
}

function decodePayload_(payload, encoding) {
  if (encoding === 'json') return payload;
  if (encoding === 'gzip-base64') {
    const compressed = Utilities.newBlob(
      Utilities.base64Decode(payload),
      'application/gzip'
    );
    return Utilities.ungzip(compressed).getDataAsString('UTF-8');
  }
  throw new Error('Unsupported payload encoding: ' + encoding);
}

function fnv1a32Hex_(text) {
  let hash = 2166136261 >>> 0;
  const value = String(text || '');
  for (let i = 0; i < value.length; i += 1) {
    hash ^= value.charCodeAt(i);
    hash = Math.imul(hash, 16777619) >>> 0;
  }
  return ('00000000' + hash.toString(16)).slice(-8);
}

function safeFileName_(name) {
  return String(name).replace(/[^A-Za-z0-9._-]/g, '_').slice(0, 180);
}

function ackHtml_(payload) {
  const safeJson = JSON.stringify(payload).replace(/</g, '\u003c');
  const successText = payload.ok ? '수신 완료' : '수신 실패';
  const escapeText_ = function(value) {
    return String(value || '').replace(/[<>&]/g, '');
  };
  const detail = payload.ok
    ? '<p>파일: <strong>' + escapeText_(payload.file_name) + '</strong></p><p>확인 코드: <strong>' + escapeText_(payload.receipt_code) + '</strong></p><p>무결성 확인: <strong>' + escapeText_(payload.checksum_fnv1a32) + '</strong></p>'
    : '<p>' + escapeText_(payload.error) + '</p>';
  const html = '<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + successText + '</title></head>' +
    '<body><main><h1>' + successText + '</h1>' + detail + '</main><script>' +
    'const receipt=' + safeJson + ';' +
    'try{window.parent.postMessage(receipt,"*");}catch(_){ }' +
    '<\/script></body></html>';
  return HtmlService.createHtmlOutput(html)
    .setTitle(successText)
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

function buildManualUploadPage_(expectedFile) {
  const expectedLiteral = JSON.stringify(expectedFile || '');
  return `<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>CUBE-REV 결과 제출</title>
<style>
:root{color-scheme:dark;--bg:#0d1117;--panel:#161d27;--line:#2d394b;--text:#edf3fb;--muted:#9cacc0;--accent:#79a8ff;--good:#54d397;--bad:#ff7d7d}
*{box-sizing:border-box}body{margin:0;min-height:100vh;display:grid;place-items:center;padding:24px;background:radial-gradient(circle at 50% 10%,#1c2a3c,#0d1117 54%);color:var(--text);font-family:Inter,"Noto Sans KR",system-ui,sans-serif}.card{width:min(680px,96vw);padding:28px;border:1px solid var(--line);border-radius:22px;background:rgba(22,29,39,.97);box-shadow:0 20px 55px rgba(0,0,0,.35)}h1{margin:.2rem 0 .7rem;font-size:clamp(1.65rem,5vw,2.35rem)}p{line-height:1.65}.muted{color:var(--muted)}.drop{display:grid;place-items:center;min-height:190px;margin:20px 0;padding:22px;border:2px dashed #42536b;border-radius:18px;background:#101721;text-align:center;cursor:pointer}.drop.drag{border-color:var(--accent);background:#14213a}.file{font-family:ui-monospace,Consolas,monospace;word-break:break-all;color:#dce9fb}.actions{display:flex;gap:10px;flex-wrap:wrap}button{flex:1;min-width:170px;padding:.85rem 1rem;border-radius:12px;border:1px solid #3d4c63;background:#26344a;color:var(--text);font:inherit;cursor:pointer}button.primary{background:#2868d7;border-color:#4a88ec;font-weight:800}button:disabled{opacity:.5;cursor:not-allowed}.status{display:none;margin-top:16px;padding:13px 15px;border-left:3px solid var(--accent);border-radius:8px;background:#101721;line-height:1.55}.status.good{display:block;border-color:var(--good)}.status.bad{display:block;border-color:var(--bad)}.status.info{display:block}
</style>
</head>
<body>
<main class="card">
  <div class="muted">CUBE-REV ${EXPECTED_VERSION}</div>
  <h1>결과 JSON 제출</h1>
  <p>실험이 끝난 뒤 내려받은 <code>CR-....json</code> 파일을 선택해 제출합니다. 같은 세션을 다시 올려도 중복 파일은 생기지 않습니다.</p>
  <div id="drop" class="drop" role="button" tabindex="0">
    <input id="file" type="file" accept="application/json,.json" hidden>
    <span><strong>JSON 파일을 선택하거나 여기에 끌어 놓으세요.</strong><br><span id="expected" class="muted"></span></span>
  </div>
  <p id="fileName" class="file muted">선택된 파일 없음</p>
  <div class="actions"><button id="choose">파일 선택</button><button id="submit" class="primary" disabled>제출</button></div>
  <div id="status" class="status"></div>
</main>
<script>
const expectedFile=${expectedLiteral};
const input=document.getElementById('file'),drop=document.getElementById('drop'),fileName=document.getElementById('fileName'),submit=document.getElementById('submit'),status=document.getElementById('status');let selectedFile=null;
document.getElementById('expected').textContent=expectedFile?'예상 파일: '+expectedFile:'파일 이름과 내용을 수정하지 않은 원본 JSON을 사용하세요.';
document.getElementById('choose').onclick=()=>input.click();drop.onclick=()=>input.click();drop.onkeydown=e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();input.click();}};
for(const type of ['dragenter','dragover'])drop.addEventListener(type,e=>{e.preventDefault();drop.classList.add('drag');});
for(const type of ['dragleave','drop'])drop.addEventListener(type,e=>{e.preventDefault();drop.classList.remove('drag');});
drop.addEventListener('drop',e=>{if(e.dataTransfer.files.length){selectedFile=e.dataTransfer.files[0];updateFile();}});
input.addEventListener('change',()=>{selectedFile=input.files[0]||null;updateFile();});
function updateFile(){const f=selectedFile;fileName.textContent=f?f.name+' · '+Math.ceil(f.size/1024).toLocaleString()+' KB':'선택된 파일 없음';submit.disabled=!f;status.className='status';status.textContent='';}
function show(message,kind){status.textContent=message;status.className='status '+kind;}
submit.onclick=async()=>{const file=selectedFile;if(!file)return;submit.disabled=true;show('파일을 확인하고 제출하고 있습니다.','info');try{const text=await file.text();const parsed=JSON.parse(text);if(parsed.project!=='CUBE-REV')throw new Error('CUBE-REV 결과 파일이 아닙니다.');if(parsed.version!=='${EXPECTED_VERSION}')throw new Error('이 수집기는 ${EXPECTED_VERSION} 파일만 받습니다. 현재 파일: '+parsed.version);google.script.run.withSuccessHandler(result=>{submit.disabled=false;show(result.status==='duplicate'?'수신 완료. 이미 저장된 세션입니다. 추가 작업은 필요하지 않습니다.':'수신 완료. 결과 파일이 저장되었습니다. 이 창을 닫아도 됩니다.','good');}).withFailureHandler(error=>{submit.disabled=false;show('제출하지 못했습니다: '+(error.message||error),'bad');}).submitManualJson(text);}catch(error){submit.disabled=false;show(error.message||String(error),'bad');}};
<\/script>
</body>
</html>`;
}
