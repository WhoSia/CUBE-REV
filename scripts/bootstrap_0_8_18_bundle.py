#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
import io
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTS = [ROOT / f"scripts/.cr0818_payload_{i:02d}.txt" for i in range(1, 8)]
ARCHIVE_SHA256 = "1e47b31e90f26bd3b0b090ec8d6eb1f2e90d0f87ac789e7c41b3d28eac436d06"
EXPECTED = {
    "analysis/temporal_route_calibration_0_8_18.py": "0ef49c077c3f4df57945f95594fee0b6f8735e0c8543cbca6206c525ce66cd6a",
    "tests/temporal_route_calibration_0.8.18.test.py": "40573c9bc8fbaefce5505286e3390fd91aa3319c88d4e5b5452d538608368f41",
    "research/CUBE_REV_0.8.18_CERTIFICATION_RESULT.json": "56890ad85dea6054de90735891275c33fa84a3480a01ed4f9daf41593045be2e",
    "research/CUBE_REV_0.8.18_CONSENT_AND_CUSTODY_CONTRACT.json": "bca68ac4e82a06c17ae51e9871027e2ffd35ec21e02bf58a3022d2b1ccb3fb09",
    "research/CUBE_REV_0.8.18_DECISION_PACKET.json": "7cb36f31bd124e975703e173b1b4501c64a5a8469a9f36bcf2e970bfaad88951",
    "research/CUBE_REV_0.8.18_EXTERNAL_TIMESTAMP_SOURCE_REGISTRY.json": "4713ae55c8a0acc63bf41ea9116bc45031fbafe732a61d068b2f7c2670f852a3",
    "research/CUBE_REV_0.8.18_PUBLIC_TIMESTAMP_FIXTURE_PACK.json": "0a92cbe3c13d81e86146dac9d188b40fd3f895fa6d38b31b97931d74e8f4632c",
    "research/CUBE_REV_0.8.18_REWEIGHTING_RESULT.json": "d6a65af98e8304ca48ddaf5fad09ed736851a8bcadd428eb7b6151752a0e7f50",
    "research/CUBE_REV_0.8.18_RUNBOOK.md": "ba0d4236584329bf81d66547f408c218a8e98edf324927498e3ff5126c65234e",
    "research/CUBE_REV_0.8.18_SCOPE_CHECKPOINT.md": "e4afd84f63bada7f15b7274c96f15c3d142ce1336432676e41cba367c9cc8efc",
    "research/CUBE_REV_0.8.18_SNAPSHOT_MANIFEST.json": "05d4a69e71e9aff48d542aaa434b22898f763986e3197333b30b1ed2dde1083a",
    "research/CUBE_REV_0.8.18_TEMPORAL_DOMAIN_GAP_RESULT.json": "a9706f53d03900ee9edf302135e59d2a978e21270bc5015e26f834f394dec1ab",
    "research/CUBE_REV_0.8.18_THIRD_PARTY_NOTICE.md": "7eb94a85257cf724dda2df1577aa9e6a828e313a16580cb3f6211d35bef5b308",
    "research/CUBE_REV_0.8.18_TIMESTAMP_QC_RESULT.json": "70e0bf177410fbbd1258e5b1263f8dacf94899dc3fa1517709efd56d171a9d48",
    "research/CUBE_REV_0.8.18_VALIDATION_REPORT.md": "3b850de0d36b57116cfb7cd6d45e8c3e46455d946ec99aceef6995c12196c49f",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    for part in PARTS:
        if not part.is_file():
            raise SystemExit(f"CR0818_BOOTSTRAP_PART_MISSING:{part.name}")
    encoded = "".join(part.read_text(encoding="ascii").strip() for part in PARTS)
    raw = base64.b64decode(encoded, validate=True)
    if sha(raw) != ARCHIVE_SHA256:
        raise SystemExit(f"CR0818_ARCHIVE_SHA_MISMATCH:{sha(raw)}")

    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as archive:
        members = archive.getmembers()
        names = [member.name for member in members]
        if set(names) != set(EXPECTED) or len(names) != len(EXPECTED):
            raise SystemExit(f"CR0818_ARCHIVE_MEMBER_SET_MISMATCH:{names}")
        for member in members:
            if not member.isfile() or member.name.startswith("/") or ".." in Path(member.name).parts:
                raise SystemExit(f"CR0818_UNSAFE_MEMBER:{member.name}")
            handle = archive.extractfile(member)
            if handle is None:
                raise SystemExit(f"CR0818_UNREADABLE_MEMBER:{member.name}")
            data = handle.read()
            actual = sha(data)
            if actual != EXPECTED[member.name]:
                raise SystemExit(f"CR0818_FILE_SHA_MISMATCH:{member.name}:{actual}")
            target = ROOT / member.name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)

    for name, expected in EXPECTED.items():
        actual = sha((ROOT / name).read_bytes())
        if actual != expected:
            raise SystemExit(f"CR0818_POSTWRITE_SHA_MISMATCH:{name}:{actual}")
    print(f"CR0818_BOOTSTRAP_PASS archive={ARCHIVE_SHA256} files={len(EXPECTED)}")


if __name__ == "__main__":
    main()
