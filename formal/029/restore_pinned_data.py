#!/usr/bin/env python3
"""Restore exact, public proof certificates before a clean Lean build.

Only local, committed data is read. Both the compressed blobs and their
uncompressed payloads have fixed SHA-256 digests. Never fetch certificates
from mutable remote URLs during a proof build.
"""
import base64
import binascii
import gzip
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CERTS = {
    'EIGHTEEN_QUERY_DAG': (
        '92c131615f7ca8a070f108053c7473752c8b9964b6abcf7552ab61dcad05278d',
        'dc9841db1f84819e140a02e9d468a7bbaf062e974beff440fed5db3bcf1bd8ce',
    ),
    'upper-policy-certificate': (
        'd9dd5f9c283b9d79a86bcf00cefc51e013bc8d20a1c8c34077316a1c81e3f1d3',
        '80f334520d288b09d0ad2398b596e8910515d312b342cf07ceeb5e4107922227',
    ),
}


def verify_hash(raw: bytes, expected: str, stage: str) -> None:
    actual = hashlib.sha256(raw).hexdigest()
    if actual != expected:
        raise ValueError(f'{stage}: expected SHA-256 {expected}, found {actual}')


def restore_one(name: str, packed_hash: str, plain_hash: str) -> dict:
    source = ROOT / 'certificate_blobs' / f'{name}.json.gz.b64'
    target = ROOT / f'{name}.json'
    encoded = source.read_bytes().strip()
    try:
        packed = base64.b64decode(encoded, validate=True)
    except binascii.Error as exc:
        raise ValueError(f'{source}: invalid base64 certificate') from exc
    verify_hash(packed, packed_hash, f'{name}: compressed')
    plain = gzip.decompress(packed)
    verify_hash(plain, plain_hash, f'{name}: raw JSON')
    # Do not silently overwrite a different pre-existing proof input.
    if target.exists() and target.read_bytes() != plain:
        raise ValueError(f'{target}: existing proof input conflicts with the pinned bytes')
    target.write_bytes(plain)
    return {'name': name, 'bytes': len(plain), 'raw_sha256': plain_hash,
            'compressed_sha256': packed_hash, 'target': str(target)}


def main() -> None:
    import json
    print(json.dumps([restore_one(name, *checks) for name, checks in CERTS.items()],
                     indent=2), flush=True)


if __name__ == '__main__':
    main()
