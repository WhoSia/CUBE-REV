/**
 * CUBE-REV 0.6.10 automatic submission collector.
 * Deploy as a Google Apps Script web app: execute as yourself; access for anyone with the link.
 */
const EXPECTED_PROJECT = 'CUBE-REV';
const EXPECTED_VERSION = '0.6.10';
const MAX_JSON_BYTES = 20 * 1024 * 1024;
const PROP_FOLDER_ID = 'CUBE_REV_FOLDER_ID';
const PROP_SHEET_ID = 'CUBE_REV_SHEET_ID';
const PROP_STUDY_TOKEN = 'CUBE_REV_STUDY_TOKEN';

function setupCollector() {
  const props = PropertiesService.getScriptProperties();
  let folderId = props.getProperty(PROP_FOLDER_ID);
  let sheetId = props.getProperty(PROP_SHEET_ID);
  let token = props.getProperty(PROP_STUDY_TOKEN);

  if (!folderId) {
    const folder = DriveApp.createFolder('CUBE-REV 0.6.10 submissions');
    folderId = folder.getId();
    props.setProperty(PROP_FOLDER_ID, folderId);
  }
  if (!sheetId) {
    const book = SpreadsheetApp.create('CUBE-REV 0.6.10 submission index');
    const sheet = book.getSheets()[0];
    sheet.setName('submissions');
    sheet.appendRow(['received_at', 'session_id', 'participant_code', 'version', 'mode', 'trial_count', 'json_bytes', 'drive_file_id', 'status']);
    sheet.setFrozenRows(1);
    sheetId = book.getId();
    props.setProperty(PROP_SHEET_ID, sheetId);
  }
  if (!token) {
    token = Utilities.getUuid().replace(/-/g, '');
    props.setProperty(PROP_STUDY_TOKEN, token);
  }

  const result = { folderId, sheetId, studyToken: token, expectedVersion: EXPECTED_VERSION };
  console.log(JSON.stringify(result, null, 2));
  return result;
}

function doGet() {
  return ContentService.createTextOutput(JSON.stringify({
    ok: true,
    service: 'CUBE-REV collector',
    expected_version: EXPECTED_VERSION,
    server_time: new Date().toISOString()
  })).setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
  const nonce = String((e && e.parameter && e.parameter.submission_nonce) || '');
  try {
    const props = PropertiesService.getScriptProperties();
    const configuredToken = props.getProperty(PROP_STUDY_TOKEN);
    if (!configuredToken) throw new Error('Collector has not been initialized. Run setupCollector() first.');
    if (String(e.parameter.study_token || '') !== configuredToken) throw new Error('Study token mismatch.');

    const encoding = String(e.parameter.encoding || 'json');
    const transmittedPayload = String(e.parameter.payload || '');
    if (!transmittedPayload) throw new Error('Empty payload.');
    const jsonText = decodePayload_(transmittedPayload, encoding);
    const jsonBytes = Utilities.newBlob(jsonText).getBytes().length;
    if (jsonBytes > MAX_JSON_BYTES) throw new Error('Payload exceeds collector limit.');

    const record = JSON.parse(jsonText);
    if (record.project !== EXPECTED_PROJECT) throw new Error('Unexpected project.');
    if (record.version !== EXPECTED_VERSION) throw new Error('Unexpected version: ' + record.version);
    if (!/^CR-\d{14}-[0-9a-f]{12}$/i.test(String(record.session_id || ''))) throw new Error('Invalid session ID.');
    if (String(e.parameter.session_id || '') !== record.session_id) throw new Error('Session ID mismatch.');

    const folder = DriveApp.getFolderById(props.getProperty(PROP_FOLDER_ID));
    const sheet = SpreadsheetApp.openById(props.getProperty(PROP_SHEET_ID)).getSheets()[0];
    const fileName = safeFileName_(record.session_id + '.json');
    const lock = LockService.getScriptLock();
    lock.waitLock(15000);
    try {
      const existing = folder.getFilesByName(fileName);
      if (existing.hasNext()) {
        const file = existing.next();
        return ackHtml_({ ok: true, status: 'duplicate', nonce, receipt_id: file.getId(), file_name: fileName, received_at: new Date().toISOString() });
      }
      const file = folder.createFile(Utilities.newBlob(jsonText, 'application/json', fileName));
      const receivedAt = new Date().toISOString();
      sheet.appendRow([receivedAt, record.session_id, record.participant_code || '', record.version, record.mode || '', Array.isArray(record.trials) ? record.trials.length : '', jsonBytes, file.getId(), 'stored']);
      return ackHtml_({ ok: true, status: 'stored', nonce, receipt_id: file.getId(), file_name: fileName, received_at: receivedAt });
    } finally {
      lock.releaseLock();
    }
  } catch (error) {
    console.error(error && error.stack ? error.stack : error);
    return ackHtml_({ ok: false, status: 'error', nonce, error: String(error && error.message ? error.message : error) });
  }
}

function decodePayload_(payload, encoding) {
  if (encoding === 'json') return payload;
  if (encoding === 'gzip-base64') {
    const compressed = Utilities.newBlob(Utilities.base64Decode(payload), 'application/gzip');
    return Utilities.ungzip(compressed).getDataAsString('UTF-8');
  }
  throw new Error('Unsupported payload encoding: ' + encoding);
}

function safeFileName_(name) {
  return String(name).replace(/[^A-Za-z0-9._-]/g, '_').slice(0, 180);
}

function ackHtml_(payload) {
  const safeJson = JSON.stringify({ type: 'CUBE_REV_COLLECTOR_ACK', ...payload }).replace(/</g, '\\u003c');
  return HtmlService.createHtmlOutput('<!doctype html><meta charset="utf-8"><script>window.parent.postMessage(' + safeJson + ', "*");</script>');
}
