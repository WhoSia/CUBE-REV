#!/usr/bin/env python3
import asyncio, json, os, re, secrets, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path
from playwright.async_api import async_playwright

PUBLIC_URL = "https://whosia.github.io/CUBE-REV/"
EXPECTED_MAIN = "19f7b83aceba3a3d0cec94a3c10b1b80af85fafd"
EXPECTED_PUBLIC_SHA256 = "98e6431c72c7b32fd9461b261c981b470bdda04c617bdb0595b7ce059a250180"
EXPECTED_VERSION = "0.7.12"
EXPECTED_COLLECTOR = "CUBE-REV-0712-MAIN"
EXPECTED_PROTOCOL = "receipt-v2"
ART = Path(os.environ.get("CR0105R14_ARTIFACT_DIR", "cr0105r14-artifact"))
ART.mkdir(parents=True, exist_ok=True)

def parse_jsonp(text, callback):
    m = re.fullmatch(re.escape(callback) + r"\((.*)\);?\s*", text.strip(), flags=re.S)
    if not m:
        raise RuntimeError("invalid JSONP response")
    return json.loads(m.group(1))

def jsonp_get(endpoint, params):
    callback = "CR0105R14CB" + secrets.token_hex(5)
    q = dict(params)
    q["callback"] = callback
    q["_"] = str(int(datetime.now(timezone.utc).timestamp() * 1000))
    url = endpoint + ("&" if "?" in endpoint else "?") + urllib.parse.urlencode(q)
    req = urllib.request.Request(url, headers={"User-Agent":"CUBE-REV-R1.4-engineering-canary/1"})
    with urllib.request.urlopen(req, timeout=30) as r:
        text = r.read().decode("utf-8")
        status = r.status
    return {"http_status":status,"url":url,"payload":parse_jsonp(text, callback)}

def new_session_id():
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"CR-{stamp}-{secrets.token_hex(6)}"

CLIENT_JS = r"""
async ({sessionId, variant, expectedSha, expectedMain, staleVersion}) => {
  const Client = window.CubeRevCollectorClient;
  if (typeof Client !== 'function') throw new Error('CubeRevCollectorClient missing on public host');
  const baseCfg = window.CUBE_REV_COLLECTOR_CONFIG;
  if (!baseCfg) throw new Error('collector config missing on public host');
  const hashString = (text) => {
    let hash = 0x811c9dc5;
    for (const ch of text) { hash ^= ch.charCodeAt(0); hash = Math.imul(hash,0x01000193) >>> 0; }
    return hash >>> 0;
  };
  const randomHex = (n) => {
    const b = new Uint8Array(n); crypto.getRandomValues(b);
    return Array.from(b, x => x.toString(16).padStart(2,'0')).join('');
  };
  const mk = (version, session, events, statuses) => new Client({
    config: Client.normalizeConfig({...baseCfg, gzipWhenAvailable:false}, version),
    version,
    getSession: () => session,
    exportSession: () => session,
    logEvent: (type, extra) => events.push({type,...(extra||{})}),
    persist: () => {},
    setStatus: (message, kind, options) => statuses.push({message,kind,options}),
    randomHex, hashString,
    translate: (key, vars={}) => String(key).replace(/\{(\w+)\}/g,(_,k)=>vars[k]??'')
  });

  if (staleVersion) {
    const staleEvents=[], staleStatuses=[];
    const staleSession={project:'CUBE-REV',version:staleVersion,session_id:sessionId,participant_code:'SYNTHETIC-NONHUMAN',mode:'SYNTHETIC_CANARY_R14',trials:[],data_submission:{}};
    const staleClient=mk(staleVersion,staleSession,staleEvents,staleStatuses);
    try { await staleClient.checkHealth(); return {stale_health_rejected:false}; }
    catch(e) { return {stale_health_rejected:true,stale_error:String(e?.message||e)}; }
  }

  const events=[], statuses=[];
  const session={
    project:'CUBE-REV', version:'0.7.12', session_id:sessionId,
    participant_code:'SYNTHETIC-NONHUMAN-R14', mode:'SYNTHETIC_CANARY_R14',
    source_class:'ENGINEERING_LIVE_CANARY', human_observation:false, synthetic_canary:true,
    research_stage:'CUBE-REV 0.10.5-R1.4', public_release_sha256:expectedSha,
    deployment_commit:expectedMain, canary_variant:variant,
    created_at:new Date().toISOString(), trials:[], data_submission:{}
  };
  const client=mk('0.7.12',session,events,statuses);
  const health=await client.checkHealth();
  let receipts;
  if (variant === 'A_STORED_BASE') {
    const p1=client.submit();
    const p2=client.submit();
    receipts=await Promise.all([p1,p2]);
  } else {
    receipts=[await client.submit()];
  }
  return {
    href:location.href,
    config:{enabled:baseCfg.enabled,endpoint:baseCfg.endpoint,studyId:baseCfg.studyId,collectorId:baseCfg.collectorId,protocolVersion:baseCfg.protocolVersion},
    health, session, events, statuses, receipts,
    submission_attempt_event_count:events.filter(x=>x.type==='submission_attempted').length,
    receipt_event_count:events.filter(x=>x.type==='submission_receipt_confirmed').length
  };
}
"""

async def main():
    session_id = new_session_id()
    out = {"schema_version":"CR0105R14-LIVE-COLLECTOR-CANARY-1","session_id":session_id,"human_observations":0}
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True, args=["--no-sandbox"])
        ctx = await browser.new_context()
        page = await ctx.new_page()
        page_errors=[]
        page.on("pageerror", lambda e: page_errors.append(str(e)))
        await page.goto(PUBLIC_URL + "?cr0105r14=canary-" + secrets.token_hex(6), wait_until="networkidle", timeout=60000)
        a = await page.evaluate(CLIENT_JS, {"sessionId":session_id,"variant":"A_STORED_BASE","expectedSha":EXPECTED_PUBLIC_SHA256,"expectedMain":EXPECTED_MAIN,"staleVersion":None})

        page2 = await ctx.new_page()
        page2_errors=[]
        page2.on("pageerror", lambda e: page2_errors.append(str(e)))
        await page2.goto(PUBLIC_URL + "?cr0105r14=duplicate-" + secrets.token_hex(6), wait_until="networkidle", timeout=60000)
        b = await page2.evaluate(CLIENT_JS, {"sessionId":session_id,"variant":"B_MUTATED_DUPLICATE","expectedSha":EXPECTED_PUBLIC_SHA256,"expectedMain":EXPECTED_MAIN,"staleVersion":None})

        stale = await page2.evaluate(CLIENT_JS, {"sessionId":session_id,"variant":"STALE_VERSION_READONLY","expectedSha":EXPECTED_PUBLIC_SHA256,"expectedMain":EXPECTED_MAIN,"staleVersion":"0.7.11"})
        await browser.close()

    endpoint = a["config"]["endpoint"]
    fresh_nonce = secrets.token_hex(12)
    lookup = jsonp_get(endpoint, {
        "action":"receipt","submission_nonce":fresh_nonce,"session_id":session_id,
        "collector_id":EXPECTED_COLLECTOR,"protocol_version":EXPECTED_PROTOCOL,"version":EXPECTED_VERSION
    })
    health_independent = jsonp_get(endpoint, {
        "action":"health","collector_id":EXPECTED_COLLECTOR,"protocol_version":EXPECTED_PROTOCOL,"version":EXPECTED_VERSION
    })

    a_checksum = a["session"]["data_submission"].get("checksum_fnv1a32")
    b_checksum = b["session"]["data_submission"].get("checksum_fnv1a32")
    a_receipt = a["receipts"][0]
    b_receipt = b["receipts"][0]
    stored_checksum = lookup["payload"].get("checksum_fnv1a32")
    checks = {
        "public_client_present": bool(a.get("config")),
        "health_exact": a["health"].get("expected_version")==EXPECTED_VERSION and a["health"].get("collector_id")==EXPECTED_COLLECTOR and a["health"].get("protocol_version")==EXPECTED_PROTOCOL and a["health"].get("receipt_confirmation_available") is True,
        "first_submit_stored": a_receipt.get("ok") is True and a_receipt.get("status") in ("stored","duplicate"),
        "first_receipt_checksum_verified": a_receipt.get("checksum_verified") is True,
        "concurrent_submit_collapsed": a.get("submission_attempt_event_count")==1 and len(a.get("receipts",[]))==2 and a["receipts"][0].get("submission_nonce")==a["receipts"][1].get("submission_nonce"),
        "second_tab_duplicate": b_receipt.get("ok") is True and b_receipt.get("status")=="duplicate",
        "second_tab_checksum_verified_by_client": b_receipt.get("checksum_verified") is True,
        "payloads_intentionally_different": bool(a_checksum and b_checksum and a_checksum != b_checksum),
        "fresh_lookup_stored": lookup["payload"].get("ok") is True and lookup["payload"].get("status")=="stored",
        "fresh_lookup_binds_original_stored_checksum": bool(stored_checksum and stored_checksum==a_checksum),
        "duplicate_receipt_binds_actual_stored_checksum": bool(stored_checksum and b_receipt.get("checksum_fnv1a32")==stored_checksum),
        "stale_version_health_fail_closed": stale.get("stale_health_rejected") is True,
        "independent_health_exact": health_independent["payload"].get("expected_version")==EXPECTED_VERSION and health_independent["payload"].get("collector_id")==EXPECTED_COLLECTOR and health_independent["payload"].get("protocol_version")==EXPECTED_PROTOCOL,
        "no_page_errors": not page_errors and not page2_errors,
        "synthetic_markers_present": a["session"].get("source_class")=="ENGINEERING_LIVE_CANARY" and a["session"].get("human_observation") is False and a["session"].get("mode")=="SYNTHETIC_CANARY_R14"
    }
    integrity_hold = checks["second_tab_duplicate"] and checks["second_tab_checksum_verified_by_client"] and checks["payloads_intentionally_different"] and checks["fresh_lookup_binds_original_stored_checksum"] and not checks["duplicate_receipt_binds_actual_stored_checksum"]
    infrastructure_ok = all(checks[k] for k in [
        "public_client_present","health_exact","first_submit_stored","first_receipt_checksum_verified",
        "concurrent_submit_collapsed","second_tab_duplicate","second_tab_checksum_verified_by_client",
        "payloads_intentionally_different","fresh_lookup_stored","fresh_lookup_binds_original_stored_checksum",
        "stale_version_health_fail_closed","independent_health_exact","no_page_errors","synthetic_markers_present"
    ])
    out.update({
        "status":"HOLD" if integrity_hold else ("PASS" if infrastructure_ok and checks["duplicate_receipt_binds_actual_stored_checksum"] else "FAIL"),
        "verdict":"HOLD_DUPLICATE_RECEIPT_NOT_BOUND_TO_STORED_BYTES" if integrity_hold else ("PASS_LIVE_COLLECTOR_END_TO_END_PROVENANCE" if infrastructure_ok else "FAIL_CANARY_COURT"),
        "public_url":PUBLIC_URL,"expected_main":EXPECTED_MAIN,"expected_public_sha256":EXPECTED_PUBLIC_SHA256,
        "first_tab":a,"second_tab":b,"stale_version_probe":stale,"fresh_drive_lookup":lookup,"independent_health":health_independent,
        "page_errors":page_errors,"page2_errors":page2_errors,"checks":checks,
        "integrity_hold":integrity_hold,
        "human_launch_gate":"HOLD" if integrity_hold or not infrastructure_ok else "ELIGIBLE",
        "human_launch_reason":"duplicate receipt verifies retry payload checksum rather than immutable stored-file checksum" if integrity_hold else None
    })
    (ART/"LIVE_COLLECTOR_CANARY.json").write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding="utf-8")
    print(json.dumps(out,indent=2,ensure_ascii=False))
    if not infrastructure_ok:
        raise SystemExit(2)

if __name__ == "__main__":
    asyncio.run(main())
