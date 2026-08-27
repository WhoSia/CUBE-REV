#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, json, urllib.request
from collections import Counter, defaultdict
from pathlib import Path

PIN='e5a6bb14961b5b26c882f9fb3bf13d61d9eba890'
URL=f'https://raw.githubusercontent.com/2017YANR02/cuberoot.me/{PIN}/data/recon_backup/recons_backup.json'
EXP_BYTES=2089782; EXP_BLOB='681adbeba019ef1fc657d6927287fd00dbca6c87'
SRC=Path('r1_23_output_p1/CUBE_REV_0.10.5-R1.23_P1_REGENERATED_CROSSWALK.csv')
OUT=Path('r1_23_output_p2');OUT.mkdir(exist_ok=True)

def blobsha(b):return hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()
def fetch():
 req=urllib.request.Request(URL,headers={'User-Agent':'CUBE-REV-R1.23-P2/1.0'})
 with urllib.request.urlopen(req,timeout=120) as r:return r.read()
def I(x):
 try:return int(float(x))
 except:return None

def main():
 b=fetch(); sha=blobsha(b)
 if len(b)!=EXP_BYTES or sha!=EXP_BLOB:raise SystemExit('recons byte identity failed')
 rs=json.loads(b); by={int(x['id']):x for x in rs if x.get('id') is not None}
 with SRC.open(encoding='utf-8',newline='') as f: base=[x for x in csv.DictReader(f) if x['status']=='EXACT_REPAIRED_VALUE_VERIFIED']
 sizes=Counter(x['attempt_key'] for x in base)
 rows=[]
 for x in base:
  rid=I(x['recon_id']); r=by[rid]
  rows.append({
   'attempt_key':x['attempt_key'],'revision_cluster_size':sizes[x['attempt_key']],
   'recon_id':rid,'official':r.get('official'),'event':r.get('event'),'compWcaId':r.get('compWcaId'),'personId':r.get('personId'),'round':r.get('round'),'solveNum':r.get('solveNum'),
   'wca_attempt_value_cs':I(x['chosen_wca_value']),'rawTime':r.get('rawTime'),'method':r.get('method'),'stm':r.get('stm'),'tps':r.get('tps'),'completionStatus':r.get('completionStatus'),
   'reconer':r.get('reconer'),'reconerId':r.get('reconerId'),'personCountry':r.get('personCountry'),'recon_visibility':r.get('visibility'),
   'optimalScramble_present':bool(r.get('optimalScramble')),'videoUrl_present':bool(r.get('videoUrl'))})
 fields=list(rows[0])
 with (OUT/'CUBE_REV_0.10.5-R1.23_P2_EXACT_MESO_PANEL.csv').open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
 # Attempt-cluster counting: each linked attempt counted once. For concentration label, use set of attempt keys per actor.
 by_solver=defaultdict(set); by_reconer=defaultdict(set); by_method=defaultdict(set); by_event=defaultdict(set)
 for r in rows:
  k=r['attempt_key'];by_solver[r.get('personId') or 'MISSING'].add(k);by_reconer[r.get('reconerId') or r.get('reconer') or 'MISSING'].add(k);by_method[r.get('method') or 'MISSING'].add(k);by_event[r.get('event') or 'MISSING'].add(k)
 def top(d,n=15):return [{'id':k,'unique_attempts':len(v)} for k,v in sorted(d.items(),key=lambda kv:(-len(kv[1]),str(kv[0])))[:n]]
 uniq=len(set(r['attempt_key'] for r in rows))
 summ={
  'schema_version':'CUBE-REV-R1.23-P2-EXACT-MESO-1','pinned_commit':PIN,
  'byte_audit':{'bytes':len(b),'git_blob_sha1':sha,'sha256':hashlib.sha256(b).hexdigest(),'pass':True},
  'panel':{'reconstruction_version_rows':len(rows),'unique_attempts':uniq,'revision_collision_attempts':sum(v>1 for v in sizes.values()),'stm_present':sum(r.get('stm') not in (None,'') for r in rows),'tps_present':sum(r.get('tps') not in (None,'') for r in rows),'reconer_id_present':sum(r.get('reconerId') not in (None,'') for r in rows)},
  'unique_attempt_concentration':{'top_solvers':top(by_solver),'top_reconstructors':top(by_reconer),'methods':top(by_method,30),'events':top(by_event,30)},
  'authority':{'unit_for_selection':'unique WCA attempt','reconstruction_versions_are_not_independent':True,'meso_metrics_descriptive_only_before_selection_weighting':True}}
 (OUT/'CUBE_REV_0.10.5-R1.23_P2_EXACT_MESO_SUMMARY.json').write_text(json.dumps(summ,indent=2,ensure_ascii=False),encoding='utf-8')
 print(json.dumps(summ,ensure_ascii=False))
if __name__=='__main__':main()
