#!/usr/bin/env python3
import os,re,hashlib,json
from pathlib import Path
src=Path('research/0.10.5-r1.14/r114_g4_ontology_geometry.mjs').read_text(encoding='utf-8')
receipt=json.loads(Path('research/0.10.5-r1.14/evidence-ontology/PREEXEC_IMPLEMENTATION_REPAIR_RECEIPT.json').read_text(encoding='utf-8'))
assert receipt['status']=='PASS_SINGLE_LITERAL_REPAIR_BEFORE_ANY_G4_ROUTE_OUTCOME'
old=receipt['old_literal']; new=receipt['new_literal']
if src.count(old)!=1: raise SystemExit(f'R114_RECORDED_REPAIR_LITERAL_COUNT={src.count(old)}')
src=src.replace(old,new,1)
manifest=os.environ['R114_EXTERNAL_MANIFEST'].replace('\\','\\\\').replace("'","\\'")
replacement=f"function loadRecords(){{const m=JSON.parse(fs.readFileSync('{manifest}','utf8'));const rows=(m.records||[]).filter(r=>r.route_source_status==='RAW_ALG_CUBING_LINK');return rows.map(r=>({{...r,source:m.role||r.source||'EXTERNAL'}})).sort((a,b)=>attemptKey(a).localeCompare(attemptKey(b)));}}\n\nconst records=loadRecords()"
pat=r"function loadRecords\(\)\{.*?\}\n\nconst records=loadRecords\(\)"
out,n=re.subn(pat,replacement,src,count=1,flags=re.S)
if n!=1: raise SystemExit(f'R114_EXTERNAL_LOADER_REWRITE_COUNT={n}')
path=Path(os.environ.get('R114_EXTERNAL_CLASSIFIER_OUT','/tmp/r114_external_classifier.mjs'));path.write_text(out,encoding='utf-8')
print('R114_EXTERNAL_CLASSIFIER_MATERIALIZED',len(out),'RECORDED_HELPER_REPAIR_COUNT=1','SHA256='+hashlib.sha256(out.encode()).hexdigest())
