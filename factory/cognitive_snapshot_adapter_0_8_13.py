#!/usr/bin/env python3
"""CUBE-REV 0.8.13 cognitive-snapshot Factory compatibility adapter.

The adapter never mutates the supplied JSON. It supports either the inner
CR0813 scientific snapshot or the exact 0.7.12 Collector compatibility
envelope that contains it. Raw bytes, canonical identities, projection QC,
analysis tables, and a provenance manifest are emitted separately.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import zipfile
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

VERSION = "CUBE-REV 0.8.13"
SCHEMA = "CR0813-COLLECTOR-PAYLOAD-1"
ADAPTER = "CR0813_COGNITIVE_SNAPSHOT_FACTORY_ADAPTER_V1"
COLLECTOR_PROJECT = "CUBE-REV"
COLLECTOR_VERSION = "0.7.12"
COMPAT_SCHEMA = "CR0813-COLLECTOR-COMPATIBILITY-ENVELOPE-1"
TRIAL_POLICY = "LOSSLESS_OPAQUE_RESPONSE_PROJECTION_V1"
IDENTITY_POLICY = "IDENTITY_SESSION_V1"
BRIDGE_POLICY = "DETERMINISTIC_LEGACY_SESSION_BRIDGE_V1"
HEX64 = re.compile(r"^[0-9a-f]{64}$")
CHOICE = re.compile(r"^CR9C-[0-9a-f]{16}$")
MOVE = re.compile(r"^[URFDLB](?:2|')?$")
SESSION = re.compile(r"^CR-[0-9]{14}-[0-9a-f]{12}$")
SCIENTIFIC_SESSION = re.compile(r"^CR[A-Za-z0-9-]{5,127}$")
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


def fnv1a32(text: str) -> int:
    value = 0x811C9DC5
    for char in text:
        value ^= ord(char)
        value = (value * 0x01000193) & 0xFFFFFFFF
    return value


def checksum_text(text: str) -> str:
    return f"{fnv1a32(text):08x}"


def utc_stamp14(value: Any) -> str:
    if not isinstance(value, str) or not value:
        raise FactoryError("TRANSPORT_TIMESTAMP_INVALID")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    except Exception as exc:
        raise FactoryError("TRANSPORT_TIMESTAMP_INVALID") from exc
    return parsed.strftime("%Y%m%d%H%M%S")


def transport_identity(snapshot: dict[str, Any]) -> dict[str, str]:
    scientific = snapshot.get("session_id")
    if not isinstance(scientific, str) or not scientific:
        raise FactoryError("SCIENTIFIC_SESSION_IDENTITY")
    if SESSION.fullmatch(scientific):
        return {
            "session_id": scientific,
            "original_scientific_session_id": scientific,
            "transport_session_policy": IDENTITY_POLICY,
        }
    stamp = utc_stamp14(snapshot.get("started_at") or snapshot.get("scientific_completed_at"))
    seed = f"{scientific}|{snapshot.get('participant_token') or ''}|{snapshot.get('sequence_id') or ''}"
    suffix = (checksum_text(f"{seed}|A") + checksum_text(f"{seed}|B"))[:12]
    return {
        "session_id": f"CR-{stamp}-{suffix}",
        "original_scientific_session_id": scientific,
        "transport_session_policy": BRIDGE_POLICY,
    }


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


def check_projection(trials: Any, snapshot: dict[str, Any]) -> list[QC]:
    qc: list[QC] = []
    responses = snapshot.get("responses") if isinstance(snapshot.get("responses"), list) else []
    qc.append(QC("COMPAT_TRIAL_ARRAY", "ERROR", isinstance(trials, list), type(trials).__name__))
    if not isinstance(trials, list):
        return qc
    qc.append(QC("COMPAT_TRIAL_COUNT", "ERROR", len(trials) == 28, str(len(trials))))
    exact = len(trials) == len(responses) == 28
    for i, (trial, response) in enumerate(zip(trials, responses), 1):
        if not isinstance(trial, dict) or not isinstance(response, dict):
            exact = False
            continue
        projected = trial.get("response") if isinstance(trial.get("response"), dict) else {}
        exact = exact and trial.get("trial_index") == i
        exact = exact and trial.get("stimulus_id") == response.get("stimulus_id")
        exact = exact and projected.get("choice_display") == response.get("choice_display")
        exact = exact and projected.get("choice_code") == response.get("choice_code")
        exact = exact and projected.get("latency_ms") == response.get("latency_ms")
        exact = exact and projected.get("recorded_at") == response.get("recorded_at")
        exact = exact and trial.get("source_schema") == snapshot.get("schema_version")
        exact = exact and trial.get("scientific_revision") == snapshot.get("scientific_revision")
    qc.append(QC("COMPAT_TRIAL_EXACT_PROJECTION", "ERROR", exact, "28 opaque responses projected without semantic change"))
    return qc


def unwrap_root(root: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any] | None, list[QC]]:
    if root.get("schema_version") == SCHEMA and root.get("version") == VERSION:
        return root, None, [QC("ROOT_KIND", "INFO", True, "inner_scientific_snapshot")]

    snapshot = root.get("cognitive_snapshot")
    data_submission = root.get("data_submission")
    qc = [
        QC("ROOT_KIND", "INFO", True, "collector_compatibility_envelope"),
        QC("COLLECTOR_PROJECT", "ERROR", root.get("project") == COLLECTOR_PROJECT, str(root.get("project"))),
        QC("COLLECTOR_VERSION", "ERROR", root.get("version") == COLLECTOR_VERSION, str(root.get("version"))),
        QC("COLLECTOR_SESSION_ID", "ERROR", isinstance(root.get("session_id"), str) and bool(SESSION.fullmatch(root.get("session_id", ""))), str(root.get("session_id"))),
        QC("COLLECTOR_DATA_SUBMISSION", "ERROR", isinstance(data_submission, dict), type(data_submission).__name__),
        QC("COLLECTOR_INNER_SNAPSHOT", "ERROR", isinstance(snapshot, dict), type(snapshot).__name__),
    ]
    if not isinstance(snapshot, dict):
        raise FactoryError("COLLECTOR_ENVELOPE_WITHOUT_COGNITIVE_SNAPSHOT")
    expected_identity = transport_identity(snapshot)
    root_original = root.get("original_scientific_session_id")
    root_policy = root.get("transport_session_policy")
    qc.extend([
        QC("TRANSPORT_SESSION_DETERMINISM", "ERROR", root.get("session_id") == expected_identity["session_id"], f"expected={expected_identity['session_id']} actual={root.get('session_id')}"),
        QC("ORIGINAL_SCIENTIFIC_SESSION", "ERROR", root_original == snapshot.get("session_id") == expected_identity["original_scientific_session_id"], f"outer_original={root_original} inner={snapshot.get('session_id')}"),
        QC("TRANSPORT_SESSION_POLICY", "ERROR", root_policy == expected_identity["transport_session_policy"], f"expected={expected_identity['transport_session_policy']} actual={root_policy}"),
    ])
    if isinstance(data_submission, dict):
        qc.extend([
            QC("COMPATIBILITY_SCHEMA", "ERROR", data_submission.get("collector_compatibility_schema") == COMPAT_SCHEMA, str(data_submission.get("collector_compatibility_schema"))),
            QC("COMPATIBILITY_TRIAL_POLICY", "ERROR", data_submission.get("compatibility_trial_policy") == TRIAL_POLICY, str(data_submission.get("compatibility_trial_policy"))),
            QC("APP_PAYLOAD_VERSION", "ERROR", data_submission.get("app_payload_version") == snapshot.get("version"), str(data_submission.get("app_payload_version"))),
            QC("APP_PAYLOAD_SCHEMA", "ERROR", data_submission.get("app_payload_schema") == snapshot.get("schema_version"), str(data_submission.get("app_payload_schema"))),
            QC("DATA_SUBMISSION_ORIGINAL_SESSION", "ERROR", data_submission.get("original_scientific_session_id") == expected_identity["original_scientific_session_id"], str(data_submission.get("original_scientific_session_id"))),
            QC("DATA_SUBMISSION_TRANSPORT_SESSION", "ERROR", data_submission.get("transport_session_id") == expected_identity["session_id"], str(data_submission.get("transport_session_id"))),
            QC("DATA_SUBMISSION_TRANSPORT_POLICY", "ERROR", data_submission.get("transport_session_policy") == expected_identity["transport_session_policy"], str(data_submission.get("transport_session_policy"))),
        ])
        expected_sha = data_submission.get("immutable_snapshot_sha256")
        if expected_sha is not None:
            actual_sha = sha256_bytes(canonical_bytes(snapshot))
            qc.append(QC("IMMUTABLE_SNAPSHOT_SHA256", "ERROR", expected_sha == actual_sha, f"expected={expected_sha} actual={actual_sha}"))
    qc.extend(check_projection(root.get("trials"), snapshot))
    envelope_info = {
        "project": root.get("project"),
        "version": root.get("version"),
        "session_id": root.get("session_id"),
        "scientific_session_id": snapshot.get("session_id"),
        "transport_session_policy": root_policy,
        "generated_at": root.get("generated_at"),
        "trial_count": len(root.get("trials", [])) if isinstance(root.get("trials"), list) else None,
        "compatibility_schema": data_submission.get("collector_compatibility_schema") if isinstance(data_submission, dict) else None,
        "synthetic_live_cert": data_submission.get("synthetic_live_cert") if isinstance(data_submission, dict) else None,
        "exclude_from_human_cohort": data_submission.get("exclude_from_human_cohort") if isinstance(data_submission, dict) else None,
    }
    return snapshot, envelope_info, qc


def validate_snapshot(snapshot: dict[str, Any]) -> list[QC]:
    qc: list[QC] = []

    def check(code: str, condition: bool, detail: str, severity: str = "ERROR") -> None:
        qc.append(QC(code, severity, bool(condition), detail))

    check("SCHEMA_IDENTITY", snapshot.get("schema_version") == SCHEMA, str(snapshot.get("schema_version")))
    check("VERSION_IDENTITY", snapshot.get("version") == VERSION, str(snapshot.get("version")))
    check("RESPONSE_ENCODING", snapshot.get("response_encoding") == "OPAQUE_CHOICE_CODE_V1", str(snapshot.get("response_encoding")))
    check("SCIENTIFIC_SESSION_ID", isinstance(snapshot.get("session_id"), str) and bool(SCIENTIFIC_SESSION.fullmatch(snapshot.get("session_id", ""))), str(snapshot.get("session_id")))
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
    row_valid = True
    for i, response in enumerate(responses, 1):
        if not isinstance(response, dict):
            row_valid = False
            continue
        positions.append(response.get("position"))
        stimuli.append(response.get("stimulus_id"))
        row_valid = row_valid and response.get("position") == i
        row_valid = row_valid and isinstance(response.get("stimulus_id"), str) and bool(response.get("stimulus_id"))
        row_valid = row_valid and isinstance(response.get("choice_display"), str) and bool(MOVE.fullmatch(response.get("choice_display", "")))
        row_valid = row_valid and isinstance(response.get("choice_code"), str) and bool(CHOICE.fullmatch(response.get("choice_code", "")))
        row_valid = row_valid and isinstance(response.get("latency_ms"), (int, float)) and response.get("latency_ms", -1) >= 0
        row_valid = row_valid and isinstance(response.get("recorded_at"), str) and bool(response.get("recorded_at"))
    check("RESPONSE_ROWS", row_valid, "all rows structurally valid")
    check("POSITION_ORDER", positions == list(range(1, 29)), json.dumps(positions))
    check("STIMULUS_UNIQUENESS", len(stimuli) == 28 and len(set(stimuli)) == 28, f"unique={len(set(stimuli))}")

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
        root = json.loads(raw.decode("utf-8-sig"))
    except Exception as exc:
        raise FactoryError(f"INVALID_JSON:{exc}") from exc
    if not isinstance(root, dict):
        raise FactoryError("ROOT_NOT_OBJECT")

    snapshot, envelope_info, envelope_qc = unwrap_root(root)
    qc = envelope_qc + validate_snapshot(snapshot)
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
        "scientific_session_id": session_id,
        "transport_session_id": envelope_info.get("session_id") if envelope_info else session_id,
        "transport_session_policy": envelope_info.get("transport_session_policy") if envelope_info else IDENTITY_POLICY,
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
        "root_kind": "collector_compatibility_envelope" if envelope_info else "inner_scientific_snapshot",
        "collector_project": envelope_info.get("project") if envelope_info else None,
        "collector_version": envelope_info.get("version") if envelope_info else None,
        "collector_trial_count": envelope_info.get("trial_count") if envelope_info else None,
        "exclude_from_human_cohort": envelope_info.get("exclude_from_human_cohort") if envelope_info else None,
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
    (outdir / "interpreted_sessions.jsonl").write_text(json.dumps({"session": session_row, "responses": trial_rows, "telemetry": telemetry_rows, "envelope": envelope_info, "qc": [asdict(q) for q in qc]}, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")

    created = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_names = ["session_table.csv", "trial_table.csv", "telemetry_table.csv", "qc_report.csv", "interpreted_sessions.jsonl"]
    manifest: dict[str, Any] = {
        "schema_version": "CR0813-FACTORY-MANIFEST-1",
        "factory_adapter": ADAPTER,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source": {
            "path": input_path.name,
            "root_kind": "collector_compatibility_envelope" if envelope_info else "inner_scientific_snapshot",
            "raw_sha256": sha256_bytes(raw),
            "canonical_root_sha256": sha256_bytes(canonical_bytes(root)),
            "canonical_snapshot_sha256": sha256_bytes(canonical_bytes(snapshot)),
            "raw_copy_path": str(raw_copy.relative_to(outdir)),
            "collector_envelope": envelope_info,
        },
        "blocking_qc_count": len(blocking),
        "analysis_eligible": len(blocking) == 0,
        "outputs": {},
    }
    for name in output_names:
        p = outdir / name
        manifest["outputs"][name] = {"sha256": sha256_file(p), "bytes": p.stat().st_size}
    manifest_path = outdir / "analysis_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    zip_path = outdir / f"CUBE-REV_0.8.13_COGNITIVE_ANALYSIS_READY_{created}.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in [raw_copy, *(outdir / name for name in output_names), manifest_path]:
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
    print(f"CR0813_FACTORY_RECONSTRUCTION_PASS responses=28 root={manifest['source']['root_kind']} outputs={len(manifest['outputs'])} bundle={manifest['bundle']['path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
