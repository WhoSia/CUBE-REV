#!/usr/bin/env python3
from pathlib import Path
import json
src=Path('research/0.10.5-r1.8/r18_distance_null_calibration.mjs').read_text(encoding='utf-8')
repls={
    "sha(fs.readFileSync(MANIFEST_PATH))":"sha(fs.readFileSync(MANIFEST_PATH,'utf8'))",
    "sha(fs.readFileSync(NULL_FREEZE_PATH))":"sha(fs.readFileSync(NULL_FREEZE_PATH,'utf8'))",
}
for old,new in repls.items():
    if src.count(old)!=1:
        raise RuntimeError(f'R18_NULL_PATCH_ANCHOR_COUNT {old} {src.count(old)}')
    src=src.replace(old,new)
out=Path('/tmp/r18null/r18_distance_null_calibration_runtime.mjs')
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(src,encoding='utf-8')
record={
  'schema_version':'CR0105R18-NULL-RUNTIME-PATCH-1',
  'status':'PASS_SOURCE_BOUND_RUNTIME_PATCH',
  'changes':[
    'R1.7 manifest provenance hash uses UTF-8 file text bytes, not stable serialization of a Node Buffer object.',
    'NAPKIN null-freeze provenance hash uses UTF-8 file text bytes, not stable serialization of a Node Buffer object.'
  ],
  'scientific_definition_changed':False,
  'holdout_outcomes_seen':False,
  'human_observations':0
}
Path('/tmp/r18null/NULL_RUNTIME_PATCH.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(json.dumps(record,indent=2))
