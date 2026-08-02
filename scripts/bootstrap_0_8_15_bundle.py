#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
import io
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTS = [ROOT / f"scripts/.cr0815_payload_{i:02d}.txt" for i in range(1, 5)]
ARCHIVE_SHA256 = "031d8a80e0c09086db22e74b948080f6f98f5282bf2d61f6ca5412c67f60d41e"
EXPECTED = {
    "analysis/cognitive_mechanism_lattice_0_8_15.py": "cfd279acae0badbdeee4898d6f29e2c66593d5b66de01ebfa1f7cf15d83fff7d",
    "tests/mechanism_lattice_0.8.15.test.py": "9455fa60bfb8441c8ae59baed4ae0a0cb768c85f15caa54d83a222eb04107637",
    "research/CUBE_REV_0.8.15_MECHANISM_AXIS_REGISTRY.json": "e2d84b11cedc5c1acc99f32856482945ebecb0fab2665897d6e646027c5ee780",
    "research/CUBE_REV_0.8.15_LITERATURE_ANCHORS.md": "51ad652e963fa370516c733417c450512d725ddba89eb653bdb7be12454cb9d6",
    "research/CUBE_REV_0.8.15_VALIDATION_REPORT.md": "fdb61ec87644960b8d975122f9bd65dd4914825365a906c109194479a70f6040",
    "research/CUBE_REV_0.8.15_DECISION_PACKET.json": "bf602b232ec098cc1f28d8250aefbe542ceacbae2e7d3d95c45733b5452b08ca",
    "research/CUBE_REV_0.8.15_RUNBOOK.md": "ee96573ced1abb1300fed439e93fe4cd735cb154112f5de909edd309cba43c92",
    ".github/workflows/build-0.8.15-cognitive-mechanism-lattice.yml": "170fef956cc4b361fbd1ef848d3dcd8fe420d22987d40e9bbe7621401e3df063",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    for part in PARTS:
        if not part.is_file():
            raise SystemExit(f"CR0815_BOOTSTRAP_PART_MISSING:{part.name}")
    encoded = "".join(part.read_text(encoding="ascii").strip() for part in PARTS)
    raw = base64.b64decode(encoded, validate=True)
    if sha(raw) != ARCHIVE_SHA256:
        raise SystemExit(f"CR0815_BOOTSTRAP_ARCHIVE_SHA_MISMATCH:{sha(raw)}")

    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as archive:
        members = archive.getmembers()
        names = [member.name for member in members]
        if set(names) != set(EXPECTED) or len(names) != len(EXPECTED):
            raise SystemExit(f"CR0815_BOOTSTRAP_MEMBER_SET_MISMATCH:{names}")
        for member in members:
            if not member.isfile() or member.name.startswith("/") or ".." in Path(member.name).parts:
                raise SystemExit(f"CR0815_BOOTSTRAP_UNSAFE_MEMBER:{member.name}")
            handle = archive.extractfile(member)
            if handle is None:
                raise SystemExit(f"CR0815_BOOTSTRAP_MEMBER_UNREADABLE:{member.name}")
            data = handle.read()
            actual = sha(data)
            if actual != EXPECTED[member.name]:
                raise SystemExit(f"CR0815_BOOTSTRAP_FILE_SHA_MISMATCH:{member.name}:{actual}")
            target = ROOT / member.name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)

    for name, expected in EXPECTED.items():
        actual = sha((ROOT / name).read_bytes())
        if actual != expected:
            raise SystemExit(f"CR0815_BOOTSTRAP_POSTWRITE_SHA_MISMATCH:{name}:{actual}")
    print(f"CR0815_BOOTSTRAP_PASS archive={ARCHIVE_SHA256} files={len(EXPECTED)}")


if __name__ == "__main__":
    main()
