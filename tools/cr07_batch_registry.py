#!/usr/bin/env python3
"""Deduplicate CR07-BATCH ZIPs without retaining raw participant payloads."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

MAX_MEMBER_BYTES = 50 * 1024 * 1024


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_member(name: str) -> bool:
    value = PurePosixPath(name.replace("\\", "/"))
    return not value.is_absolute() and ".." not in value.parts


def canonical_json(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def inspect_batch(zip_path: Path, registry: dict) -> tuple[dict, dict | None]:
    payload = zip_path.read_bytes()
    batch_hash = sha256(payload)
    existing_batches = {item["zip_sha256"] for item in registry.get("batches", [])}
    if batch_hash in existing_batches:
        return {
            "status": "duplicate_batch",
            "zip_sha256": batch_hash,
            "accepted_sessions": [],
            "duplicate_sessions": [],
            "conflicts": [],
            "clock_state": registry["clock"]["state"],
        }, None

    accepted, duplicates, conflicts, invalid = [], [], [], []
    session_updates = {}
    with zipfile.ZipFile(zip_path) as archive:
        for info in archive.infolist():
            if not safe_member(info.filename):
                raise ValueError(f"unsafe ZIP member: {info.filename}")
            if info.is_dir() or not info.filename.lower().endswith(".json"):
                continue
            if info.file_size > MAX_MEMBER_BYTES:
                invalid.append({"member": info.filename, "reason": "member_too_large"})
                continue
            try:
                value = json.loads(archive.read(info).decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                invalid.append({"member": info.filename, "reason": "invalid_json"})
                continue
            if not isinstance(value, dict) or value.get("project") != "CUBE-REV":
                continue
            session_id = str(value.get("session_id") or "").strip()
            if not session_id:
                invalid.append({"member": info.filename, "reason": "missing_session_id"})
                continue
            content_hash = sha256(canonical_json(value))
            prior = registry.get("sessions", {}).get(session_id)
            if prior:
                if prior["content_sha256"] == content_hash:
                    duplicates.append(session_id)
                else:
                    conflicts.append({
                        "session_id": session_id,
                        "existing_sha256": prior["content_sha256"],
                        "incoming_sha256": content_hash,
                    })
                continue
            if session_id in session_updates:
                if session_updates[session_id]["content_sha256"] == content_hash:
                    duplicates.append(session_id)
                else:
                    conflicts.append({"session_id": session_id, "reason": "conflicting_duplicates_in_batch"})
                continue
            session_updates[session_id] = {
                "content_sha256": content_hash,
                "first_batch_sha256": batch_hash,
                "protocol_version": value.get("calibration_0711", {}).get("protocol_version") or value.get("version"),
                "data_classification": value.get("calibration_0711", {}).get(
                    "data_classification", "LEGACY_OR_UNCLASSIFIED_RUN_IN"
                ),
                "clock_eligible": False,
            }
            accepted.append(session_id)

    report = {
        "status": "conflict" if conflicts else "accepted",
        "zip_sha256": batch_hash,
        "zip_name": zip_path.name,
        "accepted_sessions": sorted(accepted),
        "duplicate_sessions": sorted(set(duplicates)),
        "conflicts": conflicts,
        "invalid_members": invalid,
        "clock_state": registry["clock"]["state"],
        "raw_payloads_retained": False,
    }
    if conflicts:
        return report, None

    updated = json.loads(json.dumps(registry))
    updated.setdefault("sessions", {}).update(session_updates)
    updated.setdefault("batches", []).append({
        "zip_sha256": batch_hash,
        "zip_name": zip_path.name,
        "registered_at": datetime.now(timezone.utc).isoformat(),
        "accepted_session_count": len(accepted),
        "duplicate_session_count": len(set(duplicates)),
        "invalid_member_count": len(invalid),
    })
    return report, updated


def atomic_json_write(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("batch_zip", type=Path)
    parser.add_argument(
        "--registry",
        type=Path,
        default=Path("research/registry/cumulative_registry.json"),
    )
    parser.add_argument("--report", type=Path)
    parser.add_argument("--commit", action="store_true", help="Atomically update the cumulative registry.")
    args = parser.parse_args()
    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    report, updated = inspect_batch(args.batch_zip, registry)
    if args.report:
        atomic_json_write(args.report, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report["status"] == "conflict":
        return 2
    if args.commit and updated is not None:
        atomic_json_write(args.registry, updated)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
