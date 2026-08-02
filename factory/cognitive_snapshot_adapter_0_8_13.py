#!/usr/bin/env python3
"""CUBE-REV 0.8.13 cognitive-snapshot compatibility adapter.

This adapter does not mutate the source JSON. It validates the opaque 28-response
scientific snapshot, writes analysis-ready tables plus a QC trail, and records
SHA-256 identities for every output in the same provenance-first spirit as the
CUBE-REV 0.7 Factory.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import sys
import zipfile
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

VERSION = "CUBE-REV 0.8.13"
SCHEMA = "CR0813-COLLECTOR-PAYLOAD-1"
ADAPTER = "CR0813_COGNITIVE_SNAPSHOT_FACTORY_ADAPTER_V1"
HEX64 = re.compile(r"^[0-9a-f]{64}$")
CHOICE = re.compile(r"^CR9C-[0-9a-f]{16}$")
MOVE = re.compile(r"^[URFDLB](?:2|')?$")
FORBIDDEN = {"state_id", "rotation_id", "face_map", "choice_canonical", "canonical_move"}


class FactoryError(ValueError):
    pass


@dataclass(frozen=True)
class QC:
    code: str
    severity: str
    passed: bool
    detail: str


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def walk_forbidden(value: Any, trail: str = "$") -> list[str]:
    found: list[str] = []
    if isinstance(value, list):
        for i, item in enumerate(value):
            found.extend(walk_forbidden(item, f"{trail}[{i}]"))
    elif isinstance(value, dict):
        for key, item in value.items():
            if key in FORBIDDEN:
                found.append(f"{trail}.{key}")
            found.extend(walk_forbidden(item, f"{trail}.{key}"))
    return found


def validate(snapshot: dict[str, Any]) -> list[QC]:
    qc: list[QC] = []

    def check(code: str, condition: bool, detail: str, severity: str = "ERROR") -> None:
        qc.append(QC(code=code, severity=severity, passed=bool(condition), detail=detail))

    check("SCHEMA_IDENTITY", snapshot.get("schema_version") == SCHEMA, str(snapshot.get("schema_version")))
    check("VERSION_IDENTITY", snapshot.get("version") == VERSION, str(snapshot.get("version")))
    check("RESPONSE_ENCODING", snapshot.get("response_encoding") == "OPAQUE_CHOICE_CODE_V1", str(snapshot.get("response_encoding")))
    check("SESSION_ID", isinstance(snapshot.get("session_id"), str) and bool(snapshot.get("session_id")), str(snapshot.get("session_id")))
    check("PARTICIPANT_TOKEN", isinstance(snapshot.get("participant_token"), str) and bool(snapshot.get("participant_token")), "present" if snapshot.get("participant_token") else "missing")
    check("SEQUENCE_ID", str(snapshot.get("sequence_id", "")) in {str(i) for i in range(1, 25)}, str(snapshot.get("sequence_id")))
    check("SCIENTIFIC_REVISION", isinstance(snapshot.get("scientific_revision"), int) and snapshot.get("scientific_revision", 0) >= 1, str(snapshot.get("scientific_revision")))

    responses = snapshot.get("responses")
    check("RESPONSE_ARRAY", isinstance(responses, list), type(responses).__name__)
    if not isinstance(responses, list):
        responses = []
    check("RESPONSE_COUNT", len(responses) == 28, str(len(responses)))

    positions: list[int] = []
    stimuli: list[str] = []
    codes: list[str] = []
    row_valid = True
    for i, response in enumerate(responses, 1):
        if not isinstance(response, dict):
            row_valid = False
            continue
        positions.append(response.get("position"))
        stimuli.append(response.get("stimulus_id"))
        codes.append(response.get("choice_code"))
        row_valid = row_valid and response.get("position") == i
        row_valid = row_valid and isinstance(response.get("stimulus_id"), str) and bool(response.get("stimulus_id"))
        row_valid = row_valid and isinstance(response.get("choice_display"), str) and bool(MOVE.fullmatch(response["choice_display"]))
        row_valid = row_valid and isinstance(response.get("choice_code"), str) and bool(CHOICE.fullmatch(response["choice_code"]))
        row_valid = row_valid and isinstance(response.get("latency_ms"), (int, float)) and response["latency_ms"] >= 0
        row_valid = row_valid and isinstance(response.get("recorded_at"), str) and bool(response.get("recorded_at"))
    check("RESPONSE_ROWS", row_valid, "all rows structurally valid")
    check("POSITION_ORDER", positions == list(range(1, 29)), json.dumps(positions))
    check("STIMULUS_UNIQUENESS", len(stimuli) == 28 and len(set(stimuli)) == 28, f"unique={len(set(stimuli))}")
    check("CHOICE_CODE_UNIQUENESS_WITHIN_SESSION", len(codes) == 28 and len(set(codes)) == 28, f"unique={len(set(codes))}", severity="WARN")

    telemetry = snapshot.get("telemetry")
    check("TELEMETRY_ARRAY", isinstance(telemetry, list), type(telemetry).__name__)
    if isinstance(telemetry, list):
        event_ids = [x.get("event_id") for x in telemetry if isinstance(x, dict) and x.get("event_id")]
        check("TELEMETRY_EVENT_ID_UNIQUENESS", len(event_ids) == len(set(event_ids)), f"events={len(event_ids)}")

    post = snapshot.get("post_task")
    check("POST_TASK", isinstance(post, dict), type(post).__name__)
    binding = snapshot.get("asset_binding")
    binding_ok = isinstance(binding, dict) and all(bool(HEX64.fullmatch(str(binding.get(k, "")))) for k in ("manifest_sha256", "public_bank_sha256", "public_config_sha256", "private_crosswalk_sha256"))
    check("ASSET_BINDING", binding_ok, "four SHA-256 identities")
    factory = snapshot.get("factory_contract")
    check("FACTORY_CONTRACT", isinstance(factory, dict) and factory.get("adapter") == ADAPTER and factory.get("raw_snapshot_immutable") is True, json.dumps(factory, ensure_ascii=False))
    forbidden = walk_forbidden(snapshot)
    check("PUBLIC_MINIMIZATION", not forbidden, ",".join(forbidden) if forbidden else "none")
    return qc


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def adapt(input_path: Path, outdir: Path) -> dict[str, Any]:
    raw = input_path.read_bytes()
    try:
        snapshot = json.loads(raw.decode("utf-8-sig"))
    except Exception as exc:
        raise FactoryError(f"INVALID_JSON:{exc}") from exc
    if not isinstance(snapshot, dict):
        raise FactoryError("ROOT_NOT_OBJECT")

    qc = validate(snapshot)
    blocking = [q for q in qc if q.severity == "ERROR" and not q.passed]
    outdir.mkdir(parents=True, exist_ok=True)
    rawdir = outdir / "raw"
    rawdir.mkdir(exist_ok=True)
    raw_copy = rawdir / input_path.name
    raw_copy.write_bytes(raw)
    if raw_copy.read_bytes() != raw:
        raise FactoryError("RAW_COPY_MISMATCH")

    session_id = str(snapshot.get("session_id") or "UNKNOWN")
    responses = snapshot.get("responses") if isinstance(snapshot.get("responses"), list) else []
    telemetry = snapshot.get("telemetry") if isinstance(snapshot.get("telemetry"), list) else []
    post = snapshot.get("post_task") if isinstance(snapshot.get("post_task"), dict) else {}

    session_row = {
        "session_id": session_id,
        "version": snapshot.get("version"),
        "schema_version": snapshot.get("schema_version"),
        "mode_id": snapshot.get("mode_id"),
        "participant_token": snapshot.get("participant_token"),
        "sequence_id": snapshot.get("sequence_id"),
        "response_count": len(responses),
        "telemetry_count": len(telemetry),
        "scientific_revision": snapshot.get("scientific_revision"),
        "started_at": snapshot.get("started_at"),
        "scientific_completed_at": snapshot.get("scientific_completed_at"),
        "upgrade_epoch": snapshot.get("upgrade_epoch"),
        "hypothesis_guess": post.get("hypothesis_guess"),
        "confidence": post.get("confidence"),
        "deliberate_strategy_change": post.get("deliberate_strategy_change"),
        "technical_notes": post.get("technical_notes"),
        "snapshot_sha256": sha256_bytes(canonical_bytes(snapshot)),
        "raw_file_sha256": sha256_bytes(raw),
        "factory_adapter": ADAPTER,
        "qc_blocking_count": len(blocking),
        "analysis_eligible": len(blocking) == 0,
    }
    write_csv(outdir / "session_table.csv", list(session_row), [session_row])

    trial_rows: list[dict[str, Any]] = []
    for response in responses:
        if not isinstance(response, dict):
            continue
        trial_rows.append({
            "session_id": session_id,
            "sequence_id": snapshot.get("sequence_id"),
            "position": response.get("position"),
            "stimulus_id": response.get("stimulus_id"),
            "choice_display": response.get("choice_display"),
            "choice_code": response.get("choice_code"),
            "latency_ms": response.get("latency_ms"),
            "recorded_at": response.get("recorded_at"),
            "response_encoding": snapshot.get("response_encoding"),
        })
    write_csv(outdir / "trial_table.csv", ["session_id", "sequence_id", "position", "stimulus_id", "choice_display", "choice_code", "latency_ms", "recorded_at", "response_encoding"], trial_rows)

    telemetry_rows: list[dict[str, Any]] = []
    for i, event in enumerate(telemetry, 1):
        if not isinstance(event, dict):
            continue
        telemetry_rows.append({
            "session_id": session_id,
            "event_index": i,
            "event_id": event.get("event_id"),
            "event_type": event.get("type"),
            "event_at": event.get("at"),
            "event_data_json": json.dumps(event.get("data"), ensure_ascii=False, separators=(",", ":")),
        })
    write_csv(outdir / "telemetry_table.csv", ["session_id", "event_index", "event_id", "event_type", "event_at", "event_data_json"], telemetry_rows)

    write_csv(outdir / "qc_report.csv", ["code", "severity", "passed", "detail"], [asdict(q) for q in qc])
    (outdir / "interpreted_sessions.jsonl").write_text(json.dumps({"session": session_row, "responses": trial_rows, "telemetry": telemetry_rows, "qc": [asdict(q) for q in qc]}, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")

    created = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    manifest = {
        "schema_version": "CR0813-FACTORY-MANIFEST-1",
        "factory_adapter": ADAPTER,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source": {"path": input_path.name, "raw_sha256": sha256_bytes(raw), "canonical_snapshot_sha256": sha256_bytes(canonical_bytes(snapshot)), "raw_copy_path": str(raw_copy.relative_to(outdir))},
        "blocking_qc_count": len(blocking),
        "analysis_eligible": len(blocking) == 0,
        "outputs": {},
    }
    output_names = ["session_table.csv", "trial_table.csv", "telemetry_table.csv", "qc_report.csv", "interpreted_sessions.jsonl"]
    for name in output_names:
        p = outdir / name
        manifest["outputs"][name] = {"sha256": sha256_file(p), "bytes": p.stat().st_size}
    manifest_path = outdir / "analysis_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    zip_path = outdir / f"CUBE-REV_0.8.13_COGNITIVE_ANALYSIS_READY_{created}.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in [raw_copy, *(outdir / n for n in output_names), manifest_path]:
            zf.write(p, p.relative_to(outdir))
    manifest["bundle"] = {"path": zip_path.name, "sha256": sha256_file(zip_path), "bytes": zip_path.stat().st_size}
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    if blocking:
        raise FactoryError("BLOCKING_QC:" + ",".join(q.code for q in blocking))
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--outdir", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        manifest = adapt(args.input, args.outdir)
    except FactoryError as exc:
        print(f"CR0813_FACTORY_RECONSTRUCTION_FAIL {exc}", file=sys.stderr)
        return 2
    print(f"CR0813_FACTORY_RECONSTRUCTION_PASS responses=28 outputs={len(manifest['outputs'])} bundle={manifest['bundle']['path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
