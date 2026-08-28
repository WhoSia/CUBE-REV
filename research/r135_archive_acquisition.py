from __future__ import annotations

import concurrent.futures
import hashlib
import json
import time
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

OUT = Path("r135-output")
OUT.mkdir(parents=True, exist_ok=True)

SOURCE_REPO = "2017YANR02/cuberoot.me"
HIST_COMMIT = "9c784f97ba7b9879dd0d352e99c02c0f3a387b19"
HIST_BLOB_SHA1 = "98d40926eba8be7708909383ea7273ced8a6ec7c"
FRAME_COMMIT = "e5a6bb14961b5b26c882f9fb3bf13d61d9eba890"
FRAME_BLOB_SHA1 = "681adbeba019ef1fc657d6927287fd00dbca6c87"
PATH = "data/recon_backup/recons_backup.json"
CURRENT_SOURCE_COMMIT = "bbf6132b9654fbc0774b4c1aa88b834e8cc37bdc"
RECON_ROUTE_BLOB_SHA1 = "fcd17ca1c5c607a28a94cdd94207d9a3ec5719f5"
API_ORIGIN = "https://api.cuberoot.me"
EXPECTED_FRAME_N = 1890
MAX_WORKERS = 8


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def git_blob_sha1(b: bytes) -> str:
    return hashlib.sha1(f"blob {len(b)}\0".encode() + b).hexdigest()


def fetch_bytes(url: str, *, tries: int = 5, timeout: int = 40) -> tuple[bytes, dict]:
    last = None
    for attempt in range(tries):
        req = urllib.request.Request(url, headers={
            "User-Agent": "CUBE-REV-R1.35-archive-census/1.0",
            "Accept": "application/json,text/plain,*/*",
        })
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                body = r.read()
                return body, {
                    "status": getattr(r, "status", None),
                    "final_url": r.geturl(),
                    "content_type": r.headers.get("content-type"),
                }
        except urllib.error.HTTPError as exc:
            body = exc.read()
            status = exc.code
            if status in (401, 403, 404):
                return body, {
                    "status": status,
                    "final_url": exc.geturl(),
                    "content_type": exc.headers.get("content-type") if exc.headers else None,
                }
            last = f"HTTP {status}: {body[:200]!r}"
        except Exception as exc:
            last = repr(exc)
        time.sleep(min(8.0, 0.7 * (2 ** attempt)))
    raise RuntimeError(f"GET failed after {tries} tries: {url}: {last}")


def raw_url(commit: str) -> str:
    return f"https://raw.githubusercontent.com/{SOURCE_REPO}/{commit}/{PATH}"


# Lane A: exact historical full-solution byte transfer.
hist_bytes, hist_http = fetch_bytes(raw_url(HIST_COMMIT))
frame_bytes, frame_http = fetch_bytes(raw_url(FRAME_COMMIT))
(OUT / "R135_HISTORICAL_RECONS_BACKUP_2026-04-05.json").write_bytes(hist_bytes)
(OUT / "R135_R123_FRAME_RECONS_BACKUP_2026-08-16.json").write_bytes(frame_bytes)

hist_git = git_blob_sha1(hist_bytes)
frame_git = git_blob_sha1(frame_bytes)
if hist_git != HIST_BLOB_SHA1:
    raise SystemExit(f"historical Git blob mismatch: {hist_git} != {HIST_BLOB_SHA1}")
if frame_git != FRAME_BLOB_SHA1:
    raise SystemExit(f"frame Git blob mismatch: {frame_git} != {FRAME_BLOB_SHA1}")

hist_rows = json.loads(hist_bytes)
frame_rows_all = json.loads(frame_bytes)
if not isinstance(hist_rows, list) or not isinstance(frame_rows_all, list):
    raise SystemExit("backup payload is not a list")

frame_rows = [
    r for r in frame_rows_all
    if r.get("event") == "3x3" and r.get("completionStatus") == "solved"
]
if len(frame_rows) != EXPECTED_FRAME_N:
    raise SystemExit(f"R1.23 solved-3x3 frame mismatch: {len(frame_rows)}")
frame_by_id = {int(r["id"]): r for r in frame_rows}
if len(frame_by_id) != EXPECTED_FRAME_N:
    raise SystemExit("duplicate ids in solved-3x3 frame")
frame_ids = sorted(frame_by_id)
hist_by_id = {int(r["id"]): r for r in hist_rows if isinstance(r, dict) and str(r.get("id", "")).isdigit()}


def nonempty_solution(row: dict | None) -> str | None:
    if not isinstance(row, dict):
        return None
    s = row.get("solution")
    return s if isinstance(s, str) and s.strip() else None


def current_get(recon_id: int) -> dict:
    url = f"{API_ORIGIN}/v1/recon/{recon_id}"
    try:
        body, meta = fetch_bytes(url, tries=4, timeout=35)
    except Exception as exc:
        return {
            "recon_id": recon_id,
            "class": "remanded_network",
            "error": repr(exc),
            "status": None,
            "body_sha256": None,
            "body_bytes": None,
            "body_text": None,
        }

    status = meta.get("status")
    body_text = body.decode("utf-8", "replace")
    base = {
        "recon_id": recon_id,
        "status": status,
        "http": meta,
        "body_sha256": sha256(body),
        "body_bytes": len(body),
        "body_text": body_text,
    }
    if status == 403:
        base["class"] = "private"
        return base
    if status == 404:
        # Every queried ID is proven to exist in the frozen R1.23 frame.
        base["class"] = "deleted_since_r123_or_source_inconsistency"
        return base
    if status != 200:
        base["class"] = "remanded_http"
        return base
    try:
        doc = json.loads(body)
    except Exception as exc:
        base["class"] = "remanded_json"
        base["error"] = repr(exc)
        return base
    if not isinstance(doc, dict):
        base["class"] = "remanded_shape"
        return base
    try:
        observed_id = int(doc.get("id"))
    except Exception:
        observed_id = None
    if observed_id != recon_id:
        base["class"] = "remanded_id_mismatch"
        base["observed_id"] = doc.get("id")
        return base
    base["class"] = "reachable"
    base["doc"] = doc
    base["visibility"] = doc.get("visibility")
    s = nonempty_solution(doc)
    base["solution_present"] = s is not None
    base["solution_chars"] = len(s) if s is not None else None
    base["solution_sha256"] = hashlib.sha256(s.encode()).hexdigest() if s is not None else None
    return base


# Lane B: exhaustive bounded GET-only detail reconstruction over all 1,890 IDs.
current_results: list[dict] = []
with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
    futs = {ex.submit(current_get, rid): rid for rid in frame_ids}
    for idx, fut in enumerate(concurrent.futures.as_completed(futs), 1):
        current_results.append(fut.result())
        if idx % 100 == 0:
            print(f"R1.35 current-detail progress {idx}/{EXPECTED_FRAME_N}", flush=True)
current_results.sort(key=lambda x: x["recon_id"])

# Archive exact bodies as JSONL so every current observation is byte-auditable.
with (OUT / "R135_CURRENT_DETAIL_ARCHIVE.jsonl").open("w", encoding="utf-8") as f:
    for row in current_results:
        f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")

current_by_id = {r["recon_id"]: r for r in current_results}
class_counts = Counter(r["class"] for r in current_results)
visibility_counts = Counter(r.get("visibility") for r in current_results if r["class"] == "reachable")

# Lane C: source reconciliation and denominator freeze.
ledger = []
overlap_solution_equal = 0
overlap_solution_unequal = 0
chosen_solution_count = 0
chosen_source_counts = Counter()
for rid in frame_ids:
    frame = frame_by_id[rid]
    hist = hist_by_id.get(rid)
    cur = current_by_id[rid]
    hsol = nonempty_solution(hist)
    cdoc = cur.get("doc") if cur.get("class") == "reachable" else None
    csol = nonempty_solution(cdoc)

    if hsol is not None and csol is not None:
        if hsol == csol:
            overlap_solution_equal += 1
        else:
            overlap_solution_unequal += 1

    # Primary census truth is the exhaustively reconstructed current detail when available.
    # Historical bytes are a fail-closed fallback only for frame IDs no longer readable now.
    if csol is not None:
        chosen = csol
        chosen_source = "current_detail"
        chosen_doc = cdoc
    elif hsol is not None:
        chosen = hsol
        chosen_source = "historical_2026-04-05_fallback"
        chosen_doc = hist
    else:
        chosen = None
        chosen_source = "none_remand"
        chosen_doc = None

    if chosen is not None:
        chosen_solution_count += 1
    chosen_source_counts[chosen_source] += 1

    scramble = None
    scramble_source = None
    if isinstance(chosen_doc, dict):
        for key in ("optimalScramble", "wcaScramble", "scramble"):
            val = chosen_doc.get(key)
            if isinstance(val, str) and val.strip():
                scramble = val
                scramble_source = f"chosen_doc:{key}"
                break
    if scramble is None:
        for key in ("optimalScramble", "wcaScramble", "scramble"):
            val = frame.get(key)
            if isinstance(val, str) and val.strip():
                scramble = val
                scramble_source = f"r123_frame:{key}"
                break

    ledger.append({
        "recon_id": rid,
        "r123_frame_row_sha256": sha256(json.dumps(frame, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()),
        "current_class": cur["class"],
        "current_http_status": cur.get("status"),
        "current_visibility": cur.get("visibility"),
        "historical_row_present": hist is not None,
        "historical_solution_present": hsol is not None,
        "historical_solution_sha256": hashlib.sha256(hsol.encode()).hexdigest() if hsol is not None else None,
        "current_solution_present": csol is not None,
        "current_solution_sha256": hashlib.sha256(csol.encode()).hexdigest() if csol is not None else None,
        "cross_vintage_solution_exact_equal": (hsol == csol) if hsol is not None and csol is not None else None,
        "chosen_source": chosen_source,
        "solution": chosen,
        "solution_sha256": hashlib.sha256(chosen.encode()).hexdigest() if chosen is not None else None,
        "scramble": scramble,
        "scramble_source": scramble_source,
        "scramble_sha256": hashlib.sha256(scramble.encode()).hexdigest() if scramble is not None else None,
        "frame_stm": frame.get("stm"),
        "frame_reconer": frame.get("reconer"),
        "frame_person": frame.get("person"),
        "frame_official": frame.get("official"),
        "frame_method": frame.get("method"),
    })

(OUT / "R135_ORDERED_SOLUTION_DENOMINATOR.json").write_text(
    json.dumps(ledger, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
)

hist_frame_ids = [rid for rid in frame_ids if rid in hist_by_id]
hist_frame_solutions = [rid for rid in frame_ids if nonempty_solution(hist_by_id.get(rid)) is not None]
summary = {
    "schema": "cube-rev/r135-archive-acquisition-v1",
    "source_repo": SOURCE_REPO,
    "historical": {
        "commit": HIST_COMMIT,
        "expected_git_blob_sha1": HIST_BLOB_SHA1,
        "observed_git_blob_sha1": hist_git,
        "sha256": sha256(hist_bytes),
        "bytes": len(hist_bytes),
        "http": hist_http,
        "rows": len(hist_rows),
        "r123_frame_ids_present": len(hist_frame_ids),
        "r123_frame_ids_with_solution": len(hist_frame_solutions),
    },
    "r123_frame": {
        "commit": FRAME_COMMIT,
        "expected_git_blob_sha1": FRAME_BLOB_SHA1,
        "observed_git_blob_sha1": frame_git,
        "sha256": sha256(frame_bytes),
        "bytes": len(frame_bytes),
        "all_rows": len(frame_rows_all),
        "solved_3x3_rows": len(frame_rows),
        "http": frame_http,
    },
    "current_detail": {
        "api_origin": API_ORIGIN,
        "source_commit_observed_at_r134": CURRENT_SOURCE_COMMIT,
        "recon_route_blob_sha1": RECON_ROUTE_BLOB_SHA1,
        "request_method": "GET only",
        "max_workers": MAX_WORKERS,
        "enumerated": len(current_results),
        "class_counts": dict(sorted(class_counts.items())),
        "visibility_counts": {str(k): v for k, v in sorted(visibility_counts.items(), key=lambda kv: str(kv[0]))},
        "solution_present_reachable": sum(1 for r in current_results if r.get("solution_present")),
    },
    "reconciliation": {
        "denominator": EXPECTED_FRAME_N,
        "chosen_solution_count": chosen_solution_count,
        "chosen_source_counts": dict(chosen_source_counts),
        "overlap_solution_exact_equal": overlap_solution_equal,
        "overlap_solution_unequal": overlap_solution_unequal,
        "ordered_solution_denominator_complete": chosen_solution_count == EXPECTED_FRAME_N,
    },
    "authority": {
        "production_writes": 0,
        "main_branch_mutations": 0,
        "human_rows": 0,
        "live_collector_calls": 0,
        "population_generalization": False,
        "causal_cognition_claim": False,
    },
}
(OUT / "R135_ACQUISITION_SUMMARY.json").write_text(
    json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
)
print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))

# Acquisition execution itself only requires exhaustive classification and pinned byte identity.
execution_ok = (
    hist_git == HIST_BLOB_SHA1
    and frame_git == FRAME_BLOB_SHA1
    and len(current_results) == EXPECTED_FRAME_N
    and len(current_by_id) == EXPECTED_FRAME_N
)
if not execution_ok:
    raise SystemExit(2)
