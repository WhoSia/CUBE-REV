#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FILES=[
 ROOT/'research/CUBE_REV_0.8.14_VALIDATION_REPORT.md',
 ROOT/'research/CUBE_REV_0.8.14_DECISION_PACKET.json',
 ROOT/'research/CUBE_REV_0.8.14_RUNBOOK.md',
]
REPLACEMENTS={
 '254b6d327c3d4713d0b2b923fc2bcdaebe4a0c5b1ffbb7407de9cabecb4e2c59':'0b8ae0679a6033b8cd4862ef6de81fe2f1ee8fde8b7bfd1ff3dee7616722fc32',
 '0dba4a7f5b36a93084e327fc4b462cbfb760b14fed64d65b5093e7c6d42980bc':'80db6740754297b51b87c6542a4ef6d5f3958f5da2c0e4ce65989a1768c78520',
 '| candidate files | 21 |':'| candidate files | 22 |',
 '"file_count": 21':'"file_count": 22',
 'file count        21':'file count        22',
 '| staging ZIP bytes | 66,618 |':'| staging ZIP bytes | 68,054 |',
 '"zip_bytes": 66618':'"zip_bytes": 68054',
 'ZIP bytes         66618':'ZIP bytes         68054',
 '- the archival Factory bridge;\n- the 0.8.13 erratum and archival evidence record;\n- staging provenance and rollback plan.':'- the archival Factory bridge;\n- the 0.8.13 erratum and archival evidence record;\n- the governing 0.8.14 Chromium-only browser support policy;\n- staging provenance and rollback plan.',
}
EXPECTED_COUNTS={
 '254b6d327c3d4713d0b2b923fc2bcdaebe4a0c5b1ffbb7407de9cabecb4e2c59':3,
 '0dba4a7f5b36a93084e327fc4b462cbfb760b14fed64d65b5093e7c6d42980bc':3,
 '| candidate files | 21 |':1,
 '"file_count": 21':1,
 'file count        21':1,
 '| staging ZIP bytes | 66,618 |':1,
 '"zip_bytes": 66618':1,
 'ZIP bytes         66618':1,
 '- the archival Factory bridge;\n- the 0.8.13 erratum and archival evidence record;\n- staging provenance and rollback plan.':1,
}
combined='\n'.join(p.read_text(encoding='utf-8') for p in FILES)
for old,count in EXPECTED_COUNTS.items():
    observed=combined.count(old)
    if observed!=count:
        raise SystemExit(f'PATCH_PRECONDITION_FAILED token={old!r} expected={count} observed={observed}')
for p in FILES:
    text=p.read_text(encoding='utf-8')
    for old,new in REPLACEMENTS.items():
        text=text.replace(old,new)
    p.write_text(text,encoding='utf-8')
combined_after='\n'.join(p.read_text(encoding='utf-8') for p in FILES)
for old in REPLACEMENTS:
    if old in combined_after:
        raise SystemExit(f'PATCH_OLD_TOKEN_REMAINS token={old!r}')
for new in REPLACEMENTS.values():
    if new not in combined_after:
        raise SystemExit(f'PATCH_NEW_TOKEN_MISSING token={new!r}')
print('CR0814_FINAL_STAGING_IDENTITY_DOC_PATCH_PASS files=3 candidate_files=22')
