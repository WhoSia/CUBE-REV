#!/usr/bin/env python3
from __future__ import annotations
import base64, hashlib, io, json, tarfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PARTS=[ROOT / p for p in ['scripts/.cr0816_payload_00.txt', 'scripts/.cr0816_payload_01.txt', 'scripts/.cr0816_payload_02.txt', 'scripts/.cr0816_payload_03.txt', 'scripts/.cr0816_payload_04.txt', 'scripts/.cr0816_payload_05.txt', 'scripts/.cr0816_payload_06.txt']]
ARCHIVE_SHA256='195aa92219048ab342a10cb737c7fb9297bf5890608db5fdcd22518174b3b351'
EXPECTED={
  "analysis/minimal_trajectory_probes_0_8_16.py": "7753a86491adee1eb1fc98622b60a074070b8832b15d684bdb466153075aea48",
  "analysis/external_trajectory_linkage_0_8_16.py": "a9cee055bff0a80791bf84d86d394adfb25f331775f4295ffc9743583040a886",
  "tests/minimal_trajectory_probes_0.8.16.test.py": "f181c74dc061bd06fb85943453bb4a85e1d748fa271eaadb97d723be7b1fd56e",
  "research/CUBE_REV_0.8.16_CERTIFICATION_RESULT.json": "57124d2132288b9a34347c7da3b9ce46cd3fe273dea26c5f4feff581894d667d",
  "research/CUBE_REV_0.8.16_DECISION_PACKET.json": "ec2a73b0d5427a9907a3787720caeb1bc44533044353d793e7ae2024acd40814",
  "research/CUBE_REV_0.8.16_EXTERNAL_DATA_NOTE.md": "740011ba0f2dcc67dbbf058c9f133a73e6d815d6cfde0e387dde48431b7580e3",
  "research/CUBE_REV_0.8.16_EXTERNAL_LINKAGE_DRYRUN.json": "546ec44554b6bc7f9fde3ec8cb01f0b73b299959210dcdf08c0c387afb33f88b",
  "research/CUBE_REV_0.8.16_EXTERNAL_RECONSTRUCTION_FIXTURE_AUDIT.json": "1488005d656f6b8d56e334d923593f5889883b62d9c43a292d06ff7562d9bb03",
  "research/CUBE_REV_0.8.16_EXTERNAL_RECONSTRUCTION_FIXTURE_PACK.json": "bb8468273816a9990c1825c1d482a6c2540b6d03701c1bcf4bd78ca6fa4dfded",
  "research/CUBE_REV_0.8.16_EXTERNAL_TRAJECTORY_LINKAGE_CONTRACT.json": "5229a1bc0e097942954bde90f7939ecd76ae8939a1dcf568c07c74ae7b198a7a",
  "research/CUBE_REV_0.8.16_EXTERNAL_TRAJECTORY_SOURCE_REGISTRY.json": "fcd424beeaea6e076e960f5d531c75defbe5f5ddfd5fef7882fa5f553eda18b5",
  "research/CUBE_REV_0.8.16_NONREACTIVE_TRAJECTORY_DESIGN.json": "795a8cb43281efd37f678ca7f57d63f723bd97888740202e676f6d0b86726b35",
  "research/CUBE_REV_0.8.16_RUNBOOK.md": "8aecc19a6a8ea9eb6108b243cbb43feb4a5224773e66c95769a26b9f3026b9e8",
  "research/CUBE_REV_0.8.16_TRAJECTORY_IDENTIFIABILITY_RESULT.json": "08287de7498958219aa265bfe9787ef45895e4f19be35fc702511316b20efa47",
  "research/CUBE_REV_0.8.16_TRAJECTORY_PROBE_REGISTRY.json": "11aa4f2b4a6bfa8a24ca21f5f6b6e853e69ba3978f43549502457f8cb3871571",
  "research/CUBE_REV_0.8.16_TRAJECTORY_SCHEDULES.json": "18656cbf883c64834e4122f47446bebe85742c18b9c8d63018d91bf45a873844",
  "research/CUBE_REV_0.8.16_VALIDATION_REPORT.md": "ff52ad9c973a584db02be6a2696d15d4623bfdbfe5218a914d32b404cfbc72bc"
}

def sha(data:bytes)->str:return hashlib.sha256(data).hexdigest()

def main():
    for p in PARTS:
        if not p.is_file(): raise SystemExit(f"CR0816_BOOTSTRAP_PART_MISSING:{p.name}")
    encoded=''.join(p.read_text(encoding='ascii').strip() for p in PARTS)
    raw=base64.b64decode(encoded, validate=True)
    if sha(raw)!=ARCHIVE_SHA256: raise SystemExit(f"CR0816_BOOTSTRAP_ARCHIVE_SHA_MISMATCH:{sha(raw)}")
    with tarfile.open(fileobj=io.BytesIO(raw), mode='r:gz') as tf:
        members=tf.getmembers(); names=[m.name for m in members]
        if set(names)!=set(EXPECTED) or len(names)!=len(EXPECTED): raise SystemExit(f"CR0816_BOOTSTRAP_MEMBER_SET_MISMATCH:{names}")
        for member in members:
            if not member.isfile() or member.name.startswith('/') or '..' in Path(member.name).parts: raise SystemExit(f"CR0816_BOOTSTRAP_UNSAFE_MEMBER:{member.name}")
            h=tf.extractfile(member)
            if h is None: raise SystemExit(f"CR0816_BOOTSTRAP_MEMBER_UNREADABLE:{member.name}")
            data=h.read(); actual=sha(data)
            if actual!=EXPECTED[member.name]: raise SystemExit(f"CR0816_BOOTSTRAP_FILE_SHA_MISMATCH:{member.name}:{actual}")
            target=ROOT/member.name; target.parent.mkdir(parents=True,exist_ok=True); target.write_bytes(data)
    for name,expected in EXPECTED.items():
        actual=sha((ROOT/name).read_bytes())
        if actual!=expected: raise SystemExit(f"CR0816_BOOTSTRAP_POSTWRITE_SHA_MISMATCH:{name}:{actual}")
    print(f"CR0816_BOOTSTRAP_PASS archive={ARCHIVE_SHA256} files={len(EXPECTED)}")
if __name__=='__main__': main()
