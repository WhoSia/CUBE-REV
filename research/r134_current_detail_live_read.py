import hashlib
import json
import time
import urllib.request
from pathlib import Path

DETAIL_IDS = [2412, 2413, 2467]
API_ORIGIN = "https://api.cuberoot.me"
WEB_ORIGIN = "https://cuberoot.me"
SOURCE_COMMIT = "bbf6132b9654fbc0774b4c1aa88b834e8cc37bdc"
RECON_ROUTE_BLOB_SHA = "fcd17ca1c5c607a28a94cdd94207d9a3ec5719f5"
API_BASE_BLOB_SHA = "a6d9a64b07ed7de253771bb602d11abc5d320bf9"
OUT = Path("r134-output")
OUT.mkdir(parents=True, exist_ok=True)


def fetch(url: str, tries: int = 4):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "CUBE-REV-R1.34-current-detail/1.0"})
            with urllib.request.urlopen(req, timeout=30) as response:
                body = response.read()
                return body, {
                    "status": getattr(response, "status", None),
                    "content_type": response.headers.get("content-type"),
                    "final_url": response.geturl(),
                }
        except Exception as exc:
            last = exc
            time.sleep(1.2 * (i + 1))
    raise RuntimeError(f"GET failed {url}: {last}")


rows = []
failures = []
for recon_id in DETAIL_IDS:
    api_url = f"{API_ORIGIN}/v1/recon/{recon_id}"
    api_body, api_meta = fetch(api_url)
    api_sha = hashlib.sha256(api_body).hexdigest()
    try:
        doc = json.loads(api_body)
    except Exception as exc:
        failures.append({"recon_id": recon_id, "reason": "api_json_parse", "error": repr(exc)})
        continue
    solution = doc.get("solution") if isinstance(doc, dict) else None
    stm = doc.get("stm") if isinstance(doc, dict) else None
    observed_id = doc.get("id") if isinstance(doc, dict) else None
    solution_ok = isinstance(solution, str) and bool(solution.strip())
    stm_ok = isinstance(stm, (int, float)) and not isinstance(stm, bool) and stm > 0
    id_ok = int(observed_id) == recon_id if isinstance(observed_id, (int, float, str)) and str(observed_id).isdigit() else False
    if not solution_ok:
        failures.append({"recon_id": recon_id, "reason": "solution_missing"})
    if not stm_ok:
        failures.append({"recon_id": recon_id, "reason": "stm_missing_or_nonpositive", "stm": stm})
    if not id_ok:
        failures.append({"recon_id": recon_id, "reason": "id_mismatch", "observed_id": observed_id})

    html_body, html_meta = fetch(f"{WEB_ORIGIN}/recon/{recon_id}")
    html_sha = hashlib.sha256(html_body).hexdigest()
    html_text = html_body.decode("utf-8", "replace")
    html_surface_ok = str(recon_id) in html_meta["final_url"] and "STM" in html_text
    if not html_surface_ok:
        failures.append({"recon_id": recon_id, "reason": "html_detail_surface_not_confirmed", "final_url": html_meta["final_url"]})

    rows.append({
        "recon_id": recon_id,
        "api_url": api_url,
        "api_http": api_meta,
        "api_body_bytes": len(api_body),
        "api_body_sha256": api_sha,
        "solution_present": solution_ok,
        "solution_chars": len(solution) if isinstance(solution, str) else None,
        "solution_sha256": hashlib.sha256(solution.encode("utf-8")).hexdigest() if isinstance(solution, str) else None,
        "stm": stm,
        "raw_time": doc.get("rawTime") if isinstance(doc, dict) else None,
        "html_http": html_meta,
        "html_body_bytes": len(html_body),
        "html_body_sha256": html_sha,
        "html_surface_ok": html_surface_ok,
    })

receipt = {
    "schema": "cube-rev/r134-current-detail-live-read-v1",
    "source_repo": "2017YANR02/cuberoot.me",
    "source_commit_observed_at_court": SOURCE_COMMIT,
    "recon_route_blob_sha1": RECON_ROUTE_BLOB_SHA,
    "api_base_blob_sha1": API_BASE_BLOB_SHA,
    "route_contract": "GET /v1/recon/:id reads SELECT * FROM recons and maps the full row to JSON; list surface is intentionally slimmer",
    "sample_policy": "three public 3x3 detail rows already visible on the current web surface; live-read proves existence/preservation, not exhaustive archive coverage",
    "rows": rows,
    "failures": failures,
    "pass": len(rows) == len(DETAIL_IDS) and not failures and all(r["solution_present"] and r["html_surface_ok"] for r in rows),
    "archive_completeness_claim": False,
    "human_rows": 0,
    "live_collector_calls": 0,
    "production_writes": 0,
    "request_method": "GET only",
}
(OUT / "R134_CURRENT_DETAIL_LIVE_READ.json").write_text(json.dumps(receipt, indent=2, sort_keys=True), encoding="utf-8")
print(json.dumps(receipt, indent=2, sort_keys=True))
if not receipt["pass"]:
    raise SystemExit(2)
