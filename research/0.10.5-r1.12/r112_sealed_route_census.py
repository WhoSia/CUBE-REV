#!/usr/bin/env python3
import json, os, hashlib
from pathlib import Path
from collections import defaultdict, Counter

ROOT=Path(os.environ.get('R112_REPO_ROOT','.')).resolve()
OUT=Path(os.environ.get('R112_ROOT','/tmp/r112')); OUT.mkdir(parents=True,exist_ok=True)
REQ=('result_id','attempt_number','raw_alg','raw_setup','route_source_status','method')

def sha(s): return hashlib.sha256(str(s).encode('utf-8')).hexdigest()
def attempt_key(r): return f"{r['result_id']}:{r['attempt_number']}"
def record_ok(r):
    return isinstance(r,dict) and all(k in r for k in REQ) and r.get('method')=='Roux' and r.get('route_source_status')=='RAW_ALG_CUBING_LINK' and bool(r.get('raw_alg')) and r.get('raw_setup') is not None

def walk(x, source, out):
    if isinstance(x,dict):
        if record_ok(x): out.append((source,x))
        for v in x.values(): walk(v,source,out)
    elif isinstance(x,list):
        for v in x: walk(v,source,out)

def load_used():
    paths=[
      ROOT/'research/0.10.5-r1.7/evidence-full-route/FULL_ROUTE_SAMPLE_MANIFEST.json',
      ROOT/'research/0.10.5-r1.8/evidence-holdout-a/HOLDOUT_A_ROUTE_MANIFEST.json'
    ]
    used=set(); missing=[]
    for p in paths:
        if not p.exists(): missing.append(str(p.relative_to(ROOT))); continue
        j=json.loads(p.read_text(encoding='utf-8'))
        for r in j.get('records',[]):
            if record_ok(r): used.add(attempt_key(r))
    return used,missing

hits=[]; files_scanned=0; parse_errors=[]
for p in sorted((ROOT/'research').rglob('*.json')):
    rel=str(p.relative_to(ROOT))
    if rel.startswith('research/0.10.5-r1.12/'):
        continue
    try:
        # Prevent accidental pathological reads while keeping all existing research manifests in scope.
        if p.stat().st_size>50_000_000: continue
        j=json.loads(p.read_text(encoding='utf-8')); files_scanned+=1
        walk(j,rel,hits)
    except Exception as e:
        parse_errors.append({'path':rel,'error':str(e)[:200]})

by=defaultdict(list)
for source,r in hits:
    by[attempt_key(r)].append((source,r))
used,used_missing=load_used()
rows=[]; conflicts=[]
for k,vals in sorted(by.items()):
    variants=defaultdict(list)
    for source,r in vals:
        sig=sha(json.dumps({'raw_alg':r.get('raw_alg'),'raw_setup':r.get('raw_setup'),'reco_id':r.get('reco_id')},sort_keys=True,ensure_ascii=False))
        variants[sig].append(source)
    algsetup={(r.get('raw_alg'),r.get('raw_setup')) for _,r in vals}
    conflict=len(algsetup)>1
    if conflict:
        conflicts.append({'attempt_key':k,'variant_count':len(algsetup),'sources':sorted({s for s,_ in vals})})
    source,r=sorted(vals,key=lambda z:(str(z[1].get('reco_id','')),z[0]))[0]
    rows.append({
      'attempt_key':k,'result_id':r.get('result_id'),'attempt_number':r.get('attempt_number'),'reco_id':r.get('reco_id'),
      'raw_alg':r.get('raw_alg'),'raw_setup':r.get('raw_setup'),'method':'Roux','route_source_status':'RAW_ALG_CUBING_LINK',
      'source_count':len({s for s,_ in vals}),'sources':sorted({s for s,_ in vals}),
      'route_conflict':conflict,'used_by_r111':k in used
    })
clean=[r for r in rows if not r['route_conflict']]
novel=[r for r in clean if not r['used_by_r111']]
summary={
  'schema_version':'CR0105R112-SEALED-ROUTE-CENSUS-1',
  'status':'PASS',
  'files_scanned':files_scanned,
  'raw_record_hits':len(hits),
  'unique_official_attempts':len(rows),
  'clean_unique_official_attempts':len(clean),
  'r111_used_attempts_found':sum(r['used_by_r111'] for r in clean),
  'novel_sealed_attempts':len(novel),
  'combined_candidate_bank_if_all_clean_used':len(clean),
  'candidate_bank_ge_100':len(clean)>=100,
  'route_conflict_attempts':len(conflicts),
  'parse_error_files':len(parse_errors),
  'r111_source_manifest_missing':used_missing,
  'source_file_top20':Counter(s for s,_ in hits).most_common(20),
  'conflicts':conflicts[:100],
  'novel_attempts':novel,
  'all_clean_attempts':clean,
  'human_observations':0,
  'fresh_network_read':False,
  'claim_boundary':'Availability/provenance census only. This does not establish G2 geometry admissibility or scientific authority.'
}
(OUT/'SEALED_ROUTE_CENSUS.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({k:summary[k] for k in ['status','files_scanned','raw_record_hits','unique_official_attempts','clean_unique_official_attempts','r111_used_attempts_found','novel_sealed_attempts','combined_candidate_bank_if_all_clean_used','candidate_bank_ge_100','route_conflict_attempts','parse_error_files']},indent=2))
