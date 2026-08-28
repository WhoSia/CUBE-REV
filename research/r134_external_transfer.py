import csv
import hashlib
import json
import re
import statistics
import time
import urllib.request
from pathlib import Path

DATASET = "cubed-core/cubed-data-v1"
PINNED_REVISION = "8389a6784342fdb4437cd12556dc0e92a51b33f2"
API = f"https://huggingface.co/api/datasets/{DATASET}"
BASE = f"https://huggingface.co/datasets/{DATASET}/resolve/{PINNED_REVISION}"
OUT = Path("r134-output")
RAW = OUT / "raw"
OUT.mkdir(parents=True, exist_ok=True)
RAW.mkdir(parents=True, exist_ok=True)


def fetch(url: str, dest: Path | None = None, tries: int = 4):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "CUBE-REV-R1.34/3.0"})
            with urllib.request.urlopen(req, timeout=45) as response:
                body = response.read()
                meta = {
                    "status": getattr(response, "status", None),
                    "content_type": response.headers.get("content-type"),
                    "final_url": response.geturl(),
                }
            if dest is not None:
                dest.write_bytes(body)
            return body, meta
        except Exception as exc:
            last = exc
            time.sleep(1.5 * (i + 1))
    raise RuntimeError(f"fetch failed {url}: {last}")


# The moving head is read only as a drift witness. Every court byte below uses PINNED_REVISION.
api_bytes, api_meta = fetch(API, OUT / "HF_DATASET_API.json")
api_doc = json.loads(api_bytes)
observed_head = api_doc.get("sha")

sums_bytes, sums_meta = fetch(f"{BASE}/SHA256SUMS?download=true", OUT / "SHA256SUMS")
sums_sha = hashlib.sha256(sums_bytes).hexdigest()
expected = {}
for line in sums_bytes.decode("utf-8").splitlines():
    match = re.match(r"^([0-9a-f]{64})\s+\*?(.+)$", line.strip())
    if match:
        expected[match.group(2)] = match.group(1)
session_paths = sorted(path for path in expected if re.fullmatch(r"captures/[^/]+/cube_session\.json", path))
manifest_bytes, manifest_meta = fetch(f"{BASE}/dataset/manifest.json?download=true", OUT / "DATASET_MANIFEST.json")

rows = []
probes = []
failures = []
total_moves = 0
total_intervals = 0
total_boundaries = 0
total_zero_imi = 0
total_negative_imi = 0
if len(session_paths) != 35:
    failures.append({"reason": "session_path_count", "observed": len(session_paths), "expected": 35})

for path in session_paths:
    capture_id = path.split("/")[1]
    body, http = fetch(f"{BASE}/{path}?download=true", RAW / f"{capture_id}_cube_session.json")
    observed_sha = hashlib.sha256(body).hexdigest()
    expected_sha = expected[path]
    doc = json.loads(body)
    moves = doc.get("moves") if isinstance(doc, dict) else None
    scrub = doc.get("scrub") if isinstance(doc, dict) else None
    relativized = scrub.get("relativized") if isinstance(scrub, dict) else None
    probe = {
        "capture_id": capture_id,
        "path": path,
        "bytes": len(body),
        "sha256": observed_sha,
        "expected_sha256": expected_sha,
        "hash_match": observed_sha == expected_sha,
        "schema_version": doc.get("schema_version") if isinstance(doc, dict) else None,
        "has_scrub": isinstance(scrub, dict),
        "relativized_done": isinstance(relativized, dict) and relativized.get("done") is True,
        "moves_len": len(moves) if isinstance(moves, list) else None,
        **http,
    }
    probes.append(probe)
    if observed_sha != expected_sha:
        failures.append({"capture_id": capture_id, "reason": "sha256_mismatch", "expected": expected_sha, "observed": observed_sha})
    if not isinstance(moves, list) or len(moves) < 2:
        failures.append({"capture_id": capture_id, "reason": "moves_missing_or_short", "moves_type": type(moves).__name__})
        continue

    timestamps = []
    missing_t = 0
    nonint_t = 0
    for move in moves:
        t_ms = move.get("t_ms") if isinstance(move, dict) else None
        if t_ms is None:
            missing_t += 1
        elif not isinstance(t_ms, int) or isinstance(t_ms, bool):
            nonint_t += 1
        else:
            timestamps.append(t_ms)
    if missing_t or nonint_t or len(timestamps) != len(moves):
        failures.append({
            "capture_id": capture_id,
            "reason": "timestamp_schema",
            "missing_t": missing_t,
            "nonint_t": nonint_t,
            "moves": len(moves),
            "valid_t": len(timestamps),
        })
        continue

    intervals = [later - earlier for earlier, later in zip(timestamps, timestamps[1:])]
    zero_count = sum(delta == 0 for delta in intervals)
    negative_count = sum(delta < 0 for delta in intervals)
    if negative_count:
        failures.append({"capture_id": capture_id, "reason": "negative_imi", "count": negative_count})
    median_imi = statistics.median(intervals)
    mad_imi = statistics.median(abs(delta - median_imi) for delta in intervals)
    threshold = median_imi + 3 * mad_imi
    boundary_count = sum(delta > threshold for delta in intervals)
    row = {
        "capture_id": capture_id,
        "path": path,
        "bytes": len(body),
        "sha256": observed_sha,
        "expected_sha256": expected_sha,
        "hash_match": observed_sha == expected_sha,
        "schema_version": doc.get("schema_version"),
        "has_scrub": isinstance(scrub, dict),
        "relativized_done": isinstance(relativized, dict) and relativized.get("done") is True,
        "move_count": len(moves),
        "interval_count": len(intervals),
        "first_t_ms": timestamps[0],
        "last_t_ms": timestamps[-1],
        "duration_ms": timestamps[-1] - timestamps[0],
        "nondecreasing": negative_count == 0,
        "strictly_increasing": zero_count == 0 and negative_count == 0,
        "zero_imi_count": zero_count,
        "negative_imi_count": negative_count,
        "median_imi_ms": median_imi,
        "mad_imi_ms": mad_imi,
        "threshold_ms": threshold,
        "boundary_count": boundary_count,
        "boundary_rate": boundary_count / len(intervals),
        "max_imi_ms": max(intervals),
    }
    rows.append(row)
    total_moves += len(moves)
    total_intervals += len(intervals)
    total_boundaries += boundary_count
    total_zero_imi += zero_count
    total_negative_imi += negative_count

if len(rows) != 35:
    failures.append({"reason": "analyzable_row_count", "rows": len(rows), "expected": 35})

leave_one_capture_out = []
for held in rows:
    remaining_intervals = sum(r["interval_count"] for r in rows if r["capture_id"] != held["capture_id"])
    remaining_boundaries = sum(r["boundary_count"] for r in rows if r["capture_id"] != held["capture_id"])
    leave_one_capture_out.append({
        "held_out": held["capture_id"],
        "remaining_intervals": remaining_intervals,
        "remaining_boundaries": remaining_boundaries,
        "boundary_rate": remaining_boundaries / remaining_intervals if remaining_intervals else None,
    })

rates = [r["boundary_rate"] for r in rows]
medians = [r["median_imi_ms"] for r in rows]
thresholds = [r["threshold_ms"] for r in rows]
summary = {
    "court": "CUBE-REV 0.10.5-R1.34 — External Raw-Byte Transfer, 35-Capture Timestamp Replication & Current-Detail Live-Read Court",
    "dataset": DATASET,
    "pinned_revision": PINNED_REVISION,
    "observed_head_revision": observed_head,
    "head_equals_pin_at_run": observed_head == PINNED_REVISION,
    "hf_api_http": api_meta,
    "sha256sums_http": sums_meta,
    "manifest_http": manifest_meta,
    "sha256sums_sha256": sums_sha,
    "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
    "session_path_count": len(session_paths),
    "download_count": len(probes),
    "download_hash_match_count": sum(p["hash_match"] for p in probes),
    "timestamp_session_count": len(rows),
    "scrub_declared_count": sum(r["has_scrub"] for r in rows),
    "relativized_done_count": sum(r["relativized_done"] for r in rows),
    "nondecreasing_count": sum(r["nondecreasing"] for r in rows),
    "strictly_increasing_count": sum(r["strictly_increasing"] for r in rows),
    "captures_with_zero_imi": sum(r["zero_imi_count"] > 0 for r in rows),
    "total_zero_imi": total_zero_imi,
    "total_negative_imi": total_negative_imi,
    "total_moves": total_moves,
    "total_intervals": total_intervals,
    "total_boundaries": total_boundaries,
    "aggregate_boundary_rate": total_boundaries / total_intervals if total_intervals else None,
    "capture_boundary_rate_min": min(rates) if rates else None,
    "capture_boundary_rate_median": statistics.median(rates) if rates else None,
    "capture_boundary_rate_max": max(rates) if rates else None,
    "capture_median_imi_ms_median": statistics.median(medians) if medians else None,
    "capture_threshold_ms_median": statistics.median(thresholds) if thresholds else None,
    "lco_boundary_rate_min": min((x["boundary_rate"] for x in leave_one_capture_out), default=None),
    "lco_boundary_rate_max": max((x["boundary_rate"] for x in leave_one_capture_out), default=None),
    "rule": "within-capture IMI boundary iff IMI > median(IMI_capture) + 3*MAD(IMI_capture); integer-ms ties remain zero IMIs; no pooled threshold; LCO only recomputes aggregate rate",
    "timestamp_order_contract": "negative IMI is invalid; zero IMI is retained and reported because raw-cube-session-v3 specifies integer t_ms but no strict-increase constraint",
    "failures": failures,
    "pass": (
        len(rows) == 35
        and len(session_paths) == 35
        and not failures
        and all(r["hash_match"] and r["nondecreasing"] and r["has_scrub"] and r["relativized_done"] for r in rows)
    ),
    "human_rows": 0,
    "live_collector_calls": 0,
    "production_writes": 0,
}

(OUT / "R134_TIMESTAMP_REPLICATION.json").write_text(json.dumps({"summary": summary, "captures": rows, "leave_one_capture_out": leave_one_capture_out}, indent=2, sort_keys=True), encoding="utf-8")
(OUT / "R134_DOWNLOAD_PROBES.json").write_text(json.dumps(probes, indent=2, sort_keys=True), encoding="utf-8")
with (OUT / "R134_CAPTURE_TABLE.csv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)
(OUT / "R134_TRANSFER_RECEIPT.json").write_text(json.dumps({
    "schema": "cube-rev/r134-external-byte-transfer-v3",
    "dataset": DATASET,
    "pinned_revision": PINNED_REVISION,
    "observed_head_revision": observed_head,
    "source_base": BASE,
    "sha256sums_sha256": sums_sha,
    "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
    "selected_files": [{"path": p["path"], "bytes": p["bytes"], "sha256": p["sha256"], "hash_match": p["hash_match"]} for p in probes],
    "selected_file_count": len(probes),
    "all_expected_hashes_match": len(probes) == 35 and all(p["hash_match"] for p in probes),
    "raw_bytes_retained_in_artifact": True,
    "network_executor": "GitHub-hosted ubuntu-latest runner on isolated research branch; every scientific byte uses exact pinned HF revision",
    "human_rows": 0,
    "live_collector_calls": 0,
    "production_writes": 0,
}, indent=2, sort_keys=True), encoding="utf-8")
print(json.dumps(summary, indent=2, sort_keys=True))
