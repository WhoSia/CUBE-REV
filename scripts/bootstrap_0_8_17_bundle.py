#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
import io
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTS = [ROOT / f"scripts/.cr0817_payload_{i:02d}.txt" for i in range(1, 5)]
ARCHIVE_SHA256 = "32ecb7256496bc8d07ae04171148fb2341a0151707d9f86c734ebcb024f79abf"
EXPECTED = {
    "analysis/external_trajectory_snapshot_0_8_17.py": "488f0ca6802dc9ec2f402f02fe6f140d133aae779e6d05fc256569d76e699cb6",
    "tests/external_trajectory_snapshot_0.8.17.test.py": "15fcbcc7012cecc352ca559c9421d6b262fc7953f0946cadd3cabd81f9f909ea",
    "research/CUBE_REV_0.8.17_EXTERNAL_TRAJECTORY_FIXTURE_PACK.json": "c7f28d1fcd1354f42171e60e38253fe8fefe7d20ae1eeb684da92d6e05f1d3f4",
    "research/CUBE_REV_0.8.17_EXTERNAL_SOURCE_REGISTRY.json": "ef8fe30bb772ba9a32ef47bc9bb9803683f300edee7c7b8cbf35c0f43ff9774d",
    "research/CUBE_REV_0.8.17_ROUTE_GRAMMAR_CONTRACT.json": "bac29e03442fe9319fe63e6896ea0e2c2be9ebcb73d2278669d88942921b236a",
    "research/CUBE_REV_0.8.17_ECOLOGICAL_PROBE_TRANSFER_RESULT.json": "bd6fa7f8f25a9ab24d0364fc1c9289f74ec1494435cc6a5990477b6c18d60a00",
    "research/CUBE_REV_0.8.17_ROUTE_GRAMMAR_ROWS.jsonl": "1a42378183617d24e639497313fbf3e74edc58c8d6e00e3350fc488f713ac249",
    "research/CUBE_REV_0.8.17_EXTERNAL_SNAPSHOT_MANIFEST.json": "b90896da5eaebfe2e48e5ccc3f13f2881b6326f95c4e6fa84ae22fe5d09e158e",
    "research/CUBE_REV_0.8.17_VALIDATION_REPORT.md": "6c8e0a376244bc2b652f7c635fe3d87c2d3ba3061c9d79025209f675e4652ac6",
    "research/CUBE_REV_0.8.17_DECISION_PACKET.json": "1eb40f91730cb76f7ddc83ef7832837ebd2677910d03d5abcfe2b2763c7d778a",
    "research/CUBE_REV_0.8.17_RUNBOOK.md": "eb80e247e004849c0672fcf1e3599bba12f9f92725914f2a50c7015c81ebe5e0",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    encoded = "".join(part.read_text(encoding="ascii").strip() for part in PARTS)
    raw = base64.b64decode(encoded, validate=True)
    if sha(raw) != ARCHIVE_SHA256:
        raise SystemExit(f"CR0817_ARCHIVE_SHA_MISMATCH:{sha(raw)}")
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as archive:
        members = archive.getmembers()
        if {m.name for m in members} != set(EXPECTED) or len(members) != len(EXPECTED):
            raise SystemExit("CR0817_ARCHIVE_MEMBER_SET_MISMATCH")
        for member in members:
            if not member.isfile() or member.name.startswith("/") or ".." in Path(member.name).parts:
                raise SystemExit(f"CR0817_UNSAFE_MEMBER:{member.name}")
            handle = archive.extractfile(member)
            if handle is None:
                raise SystemExit(f"CR0817_UNREADABLE_MEMBER:{member.name}")
            data = handle.read()
            if sha(data) != EXPECTED[member.name]:
                raise SystemExit(f"CR0817_FILE_SHA_MISMATCH:{member.name}:{sha(data)}")
            target = ROOT / member.name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    for name, expected in EXPECTED.items():
        if sha((ROOT / name).read_bytes()) != expected:
            raise SystemExit(f"CR0817_POSTWRITE_SHA_MISMATCH:{name}")
    print(f"CR0817_BOOTSTRAP_PASS archive={ARCHIVE_SHA256} files={len(EXPECTED)}")


if __name__ == "__main__":
    main()
