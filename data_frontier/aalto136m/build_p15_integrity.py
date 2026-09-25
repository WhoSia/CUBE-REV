#!/usr/bin/env python3
"""Streaming P15 source-integrity pass; writes aggregates only, never raw rows."""
from __future__ import annotations

import argparse, csv, hashlib, io, json, re, unicodedata, zipfile
from collections import Counter
from pathlib import Path

from p15_compiler import KeyEvent, compile_stream, CORRECTION_KEYS
from p15_r1_adapter import classify

csv.field_size_limit(10_000_000)

MODIFIERS = {"SHIFT", "CONTROL", "CTRL", "ALT", "META", "CAPSLOCK", "TAB", "ENTER", "ESC", "ARROWLEFT", "ARROWRIGHT", "ARROWUP", "ARROWDOWN"}


def output_char(letter: str, keycode: str):
    s = (letter or "").strip("\ufeff")
    if len(s) == 1:
        return s
    if s.upper() in CORRECTION_KEYS | MODIFIERS:
        return None
    try:
        code = int(keycode)
        return chr(code) if 32 <= code <= 126 else None
    except (ValueError, TypeError):
        return None


def optional_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def event_order_key(row):
    """Recover browser keydown order without inventing missing timestamps."""
    press = optional_float(row.get("PRESS_TIME"))
    try:
        event_id = int(row.get("KEYSTROKE_ID"))
    except (TypeError, ValueError):
        event_id = 2**63 - 1
    return (press is None, press if press is not None else 0.0, event_id)


def iter_streams(za, names):
    for name in names:
        source_id = re.search(r"/(\d+)_keystrokes\.txt$", name).group(1)
        with za.open(name) as fh:
            # Raw files contain at least one embedded/newline-sensitive field.
            # TextIOWrapper with newline='' delegates the record boundary to csv
            # rather than silently splitting a transcription row.
            rd = csv.DictReader(io.TextIOWrapper(fh, encoding="utf-8-sig", errors="replace", newline=""), delimiter="\t")
            sid, rows = None, []
            for r in rd:
                nxt = r["TEST_SECTION_ID"]
                if sid is not None and nxt != sid:
                    yield source_id, sid, rows
                    rows = []
                sid = nxt
                rows.append(r)
            if rows:
                yield source_id, sid, rows


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--shards", type=int, default=1)
    ap.add_argument("--policy", choices=["r0", "r1"], default="r1")
    args = ap.parse_args()
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    zpath = Path(args.zip)
    census = Counter(); stream_disagree = 0; stream_total = 0
    participant_streams = Counter(); participant_text = Counter(); participant_errors = Counter()
    sample_header_mismatch = 0
    with zipfile.ZipFile(zpath) as za:
        all_names = sorted(n for n in za.namelist() if n.endswith("_keystrokes.txt"))
        if not (0 <= args.shard < args.shards):
            raise ValueError("shard must satisfy 0 <= shard < shards")
        shard_names = all_names[args.shard::args.shards]
        for source_id, section, rows in iter_streams(za, shard_names):
            stream_total += 1; participant_streams[source_id] += 1
            target = rows[0].get("SENTENCE")
            logged = rows[0].get("USER_INPUT")
            if target is None:
                # Preserve this source anomaly in the census; no target-based
                # compiler or hazard observation is authorized for this stream.
                census["invalid_missing_target_stream"] += 1
                continue
            # The collector appends a completed record on keyup, while the
            # text-producing operation occurred at keydown/keypress.  Layer T
            # therefore follows recorded press time, with source event id only
            # as a deterministic tie-breaker.
            rows = sorted(rows, key=event_order_key)
            if args.policy == "r1":
                adapted = [classify(r["LETTER"], r["KEYCODE"]) for r in rows]
                events = [KeyEvent(op, optional_float(r["PRESS_TIME"]), optional_float(r["RELEASE_TIME"]), lit)
                          for r, (op, lit) in zip(rows, adapted)]
                census.update(op for op, _ in adapted)
                conservative_ok = all(op not in {"UNKNOWN", "AMBIGUOUS_OUTPUT", "DELETE"} for op, _ in adapted)
            else:
                events = [KeyEvent(r["LETTER"], optional_float(r["PRESS_TIME"]), optional_float(r["RELEASE_TIME"]), output_char(r["LETTER"], r["KEYCODE"])) for r in rows]
                conservative_ok = False
            result = compile_stream(target, events, logged, include_alignment=False)
            if not result["stream_matches_logged_final"]:
                stream_disagree += 1
            census["raw_key_rows"] += len(rows)
            census["missing_press_time"] += sum(e.press_ms is None for e in events)
            census["missing_release_time"] += sum(e.release_ms is None for e in events)
            census["text_key_rows"] += sum(1 for e in events if e.output is not None)
            census["stream_target_match"] += int(result["stream_matches_target"])
            census["stream_target_mismatch"] += int(not result["stream_matches_target"])
            census["stream_final_disagreement"] += int(not result["stream_matches_logged_final"])
            if conservative_ok:
                census["r2_eligible_stream"] += 1
                census["r2_exact_match"] += int(result["stream_matches_logged_final"])
                norm_match = (logged is not None and unicodedata.normalize("NFC", logged.replace("\r\n", "\n")) ==
                              unicodedata.normalize("NFC", result["reconstructed"].replace("\r\n", "\n")))
                census["r2_normalization_match"] += int(norm_match)
            census["corrected_error_episodes"] += result["corrected_episode_count"]
            census["uncorrected_errors"] += result["uncorrected_error_count"]
            census["ambiguous_edits"] += result["ambiguous_edit_count"]
            participant_text[source_id] += sum(1 for e in events if e.output is not None)
            participant_errors[source_id] += result["corrected_episode_count"] + result["uncorrected_error_count"]
            if stream_total % 10000 == 0:
                print(json.dumps({"streams": stream_total, "final_disagreement": stream_disagree}), flush=True)
    people = [{"participant_source_id": p, "streams": participant_streams[p], "text_keys": participant_text[p], "error_episodes": participant_errors[p]} for p in sorted(participant_streams)]
    (out / "p15_integrity_typist_aggregates.json").write_text(json.dumps(people), encoding="utf-8")
    receipt = {
        "stage": "G3-P15 integrity pass",
        "shard": args.shard,
        "shards": args.shards,
        "policy": args.policy,
        "raw_files_in_shard": len(shard_names),
        "archive_sha256": sha256_file(zpath),
        "streams": stream_total,
        "participants": len(participant_streams),
        "final_input_stream_disagreement_n": stream_disagree,
        "final_input_stream_disagreement_rate": stream_disagree / stream_total if stream_total else None,
        "census": dict(census),
        "warning": "compiler is intentionally end-edit conservative; this integrity pass is not the P15 hazard analysis",
    }
    (out / "p15_integrity_receipt.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
