#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, json, urllib.request
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation, ROUND_FLOOR
from pathlib import Path

PIN='e5a6bb14961b5b26c882f9fb3bf13d61d9eba890'
REPO='2017YANR02/cuberoot.me'
BASE=f'https://raw.githubusercontent.com/{REPO}/{PIN}/data/recon_backup'
EXP={
 'recons_backup.json':(2089782,'681adbeba019ef1fc657d6927287fd00dbca6c87'),
 'wca_attempts.json':(110301,'78949e0be591c8d99dfa5e5e5754b76eb4013df9')}
OUT=Path('r1_23_output_p1'); OUT.mkdir(exist_ok=True)
EVENT={'3x3':'333','2x2':'222','OH':'333oh','3BLD':'333bf','4BLD':'444bf','5BLD':'555bf','4x4':'444','5x5':'555','6x6':'666','7x7':'777','Pyraminx':'pyram','Skewb':'skewb','SQ1':'sq1','Megaminx':'minx','Clock':'clock'}
SOURCE_EVENT={k:v for k,v in EVENT.items() if k!='4x4'}
SOURCE_ROUND={'R1':['1','d'],'R2':['2','e'],'R3':['3','g'],'Fi':['f','c','b']}

def get(name):
 req=urllib.request.Request(f'{BASE}/{name}',headers={'User-Agent':'CUBE-REV-R1.23-P1/1.0'})
 with urllib.request.urlopen(req,timeout=120) as r:return r.read()
def blobsha(b):return hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()
def I(x):
 try:return int(x) if x not in (None,'') else None
 except:return None
def cs(x):
 try:
  d=Decimal(str(x));
  if not d.is_finite() or d<0:return None
  return int((d*100).to_integral_value(rounding=ROUND_FLOOR))
 except (InvalidOperation,ValueError,TypeError):return None

def current_round_candidates(x):
 if x is None:return []
 s=str(x).strip()
 # Explicit compiler boundary based on current shared wca_round.ts, while
 # keeping qualification h/0 exact rather than treating them as ordinary R1.
 groups={
  'R1':['1','d'],'1':['1','d'],'d':['d','1'],
  'R2':['2','e','g'],'2':['2','e','g'],'e':['e','2','g'],'g':['g','2','e'],
  'R3':['3'],'3':['3'],
  'Fi':['f','c','b'],'f':['f','c','b'],'c':['c','f','b'],'b':['b','f','c'],
  'h':['h'],'0':['0']}
 return groups.get(s,[])

def legacy(side):
 out=[]
 for comp,pers in side.items():
  for pid,pd in (pers or {}).items():
   for er,e in (pd or {}).items():
    for sn,rid in ((e or {}).get('r') or {}).items():
     n=I(sn); a=(e or {}).get('a') or []
     out.append({'competition_id':comp,'person_id':pid,'event_round':er,'attempt_index':n,'recon_id':I(rid),'wca_attempt_value':a[n-1] if n and n<=len(a) else None})
 return out

def faithful(recons,side):
 idx=defaultdict(lambda:defaultdict(lambda:defaultdict(dict)))
 for r in recons:
  comp=r.get('compWcaId') or ''; pid=r.get('personId') or ''; ev=SOURCE_EVENT.get(str(r.get('event') or '')); rr=SOURCE_ROUND.get(str(r.get('round') or ''),[]); sn=r.get('solveNum'); rid=r.get('id')
  if comp and pid and ev and rr and sn and rid:
   for rt in rr:idx[comp][pid][f'{ev}_{rt}'][str(sn)]=rid
 out=[]
 for comp,pers in side.items():
  for pid,pd in (pers or {}).items():
   for er,e in (pd or {}).items():
    for sn,rid in idx.get(comp,{}).get(pid,{}).get(er,{}).items():
     n=I(sn); a=(e or {}).get('a') or []
     if n and n<=len(a):out.append((comp,pid,er,n,I(rid),a[n-1]))
 return out

def wcsv(path,rows):
 if not rows:return
 with open(path,'w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def main():
 rb=get('recons_backup.json'); ab=get('wca_attempts.json')
 audit={}
 for n,b in [('recons_backup.json',rb),('wca_attempts.json',ab)]:
  eb,es=EXP[n]; audit[n]={'bytes':len(b),'expected_bytes':eb,'git_blob_sha1':blobsha(b),'expected_git_blob_sha1':es,'byte_count_pass':len(b)==eb,'blob_sha1_pass':blobsha(b)==es,'sha256':hashlib.sha256(b).hexdigest()}
 if not all(v['byte_count_pass'] and v['blob_sha1_pass'] for v in audit.values()):raise SystemExit('byte audit failed')
 recons=json.loads(rb); side=json.loads(ab); byid={I(r.get('id')):r for r in recons if I(r.get('id'))}
 old=legacy(side); oldids={x['recon_id'] for x in old}; oldby=defaultdict(list)
 for x in old:oldby[(x['competition_id'],x['person_id'],x['event_round'],x['attempt_index'])].append(x['recon_id'])
 frows=faithful(recons,side); fids={x[4] for x in frows}
 rows=[]; amap=defaultdict(list); sc=Counter(); wsc=Counter(); evc=Counter(); roundall=Counter(); roundwca=Counter()
 for r in recons:
  rid=I(r.get('id')); off=r.get('official') or ''; ev0=str(r.get('event') or ''); comp=r.get('compWcaId') or ''; pid=r.get('personId') or ''; rr=r.get('round'); sn=I(r.get('solveNum')); rawcs=cs(r.get('rawTime')); wev=EVENT.get(ev0); rts=current_round_candidates(rr)
  if rr not in (None,''):roundall[str(rr)]+=1
  if off=='wca' and rr not in (None,''):roundwca[str(rr)]+=1
  cand=[]
  if not rid:st='KEY_INCOMPLETE_ID'
  elif not comp or not pid or not sn:st='KEY_INCOMPLETE_COMP_PERSON_SOLVENUM'
  elif not wev:st='EVENT_UNSUPPORTED'
  elif not rts:st='ROUND_TOKEN_UNMAPPED'
  elif comp not in side:st='SIDECAR_COMP_MISSING'
  elif pid not in (side.get(comp) or {}):st='SIDECAR_PERSON_MISSING'
  else:
   pd=side[comp][pid]
   for rt in rts:
    er=f'{wev}_{rt}'; e=pd.get(er)
    if not e:continue
    a=e.get('a') or []
    if sn<1 or sn>len(a):cand.append((er,None,'OUT_OF_RANGE'));continue
    wv=a[sn-1]
    if wv==0:cand.append((er,wv,'ZERO_PLACEHOLDER'));continue
    if rawcs is None or wv<0:cand.append((er,wv,'POSITION_ONLY'));continue
    cand.append((er,wv,'VALUE_MATCH' if wv==rawcs else 'VALUE_MISMATCH'))
   vm=[c for c in cand if c[2]=='VALUE_MATCH']; pos=[c for c in cand if c[1] not in (None,0)]
   if len(vm)==1:st='EXACT_REPAIRED_VALUE_VERIFIED'
   elif len(vm)>1:st='ROUND_CANDIDATE_COLLISION_VALUE_MATCH'
   elif len(pos)==1 and pos[0][2]=='POSITION_ONLY':st='POSITION_LINK_VALUE_NOT_TESTABLE'
   elif len(pos)==1:st='POSITION_LINK_VALUE_MISMATCH'
   elif len(pos)>1:st='ROUND_CANDIDATE_AMBIGUOUS'
   else:st='SIDECAR_EVENT_ROUND_ATTEMPT_MISSING'
  sc[st]+=1
  if off=='wca':wsc[st]+=1
  vm=[c for c in cand if c[2]=='VALUE_MATCH']; chosen=vm[0] if len(vm)==1 else None; key=None
  if chosen:
   key=(comp,pid,chosen[0],sn); amap[key].append(rid);evc[ev0]+=1
  lshadow='LEGACY_SAME_ATTEMPT_SAME_RECON' if key and rid in oldby.get(key,[]) else ('LEGACY_RECON_PRESENT_OTHER_OR_UNRESOLVED_ATTEMPT' if rid in oldids else 'NO_LEGACY_R')
  rows.append({'recon_id':rid,'official':off,'event':ev0,'compWcaId':comp,'personId':pid,'round':rr,'solveNum':sn,'method':r.get('method') or '', 'rawTime':r.get('rawTime'),'raw_time_cs_floor':rawcs,'source_faithful_regenerated':rid in fids,'status':st,'candidate_count':len(cand),'candidate_event_rounds':'|'.join(str(c[0]) for c in cand),'candidate_wca_values':'|'.join(str(c[1]) for c in cand),'candidate_value_states':'|'.join(c[2] for c in cand),'chosen_event_round':chosen[0] if chosen else '','chosen_wca_value':chosen[1] if chosen else '','attempt_key':'|'.join(map(str,key)) if key else '','legacy_shadow':lshadow})
 exactkeys=set(amap); den=[]
 for comp,pers in side.items():
  for pid,pd in (pers or {}).items():
   for er,e in (pd or {}).items():
    event_id,_,rt=er.rpartition('_')
    for n,val in enumerate((e or {}).get('a') or [],1):
     if val==0:continue
     k=(comp,pid,er,n);den.append({'competition_id':comp,'person_id':pid,'event_round':er,'event_id':event_id,'round_type_id':rt,'attempt_index':n,'wca_attempt_value':val,'valid_positive_time':int(isinstance(val,(int,float)) and val>0),'repaired_exact_link':int(k in exactkeys),'n_recon_versions':len(amap.get(k,[]))})
 la=[]
 for x in old:
  k=(x['competition_id'],x['person_id'],x['event_round'],x['attempt_index']); rr=byid.get(x['recon_id'])
  state='LEGACY_ORPHAN_RECON_MISSING' if rr is None else ('LEGACY_RECOVERED_BY_REPAIRED_COMPILER' if x['recon_id'] in amap.get(k,[]) else ('LEGACY_REGENERATED_SOURCE_FAITHFUL_OTHER_CHECK_NEEDED' if x['recon_id'] in fids else 'LEGACY_STALE_OR_SCHEMA_DRIFT'))
  la.append({**x,'recon_present':rr is not None,'audit_state':state,'current_round':rr.get('round') if rr else None,'current_event':rr.get('event') if rr else None,'current_official':rr.get('official') if rr else None})
 strata=defaultdict(lambda:[0,0]); sol=defaultdict(lambda:[0,0])
 for d in den:
  k=(d['event_id'],d['round_type_id'],d['attempt_index']);strata[k][0]+=1;strata[k][1]+=d['repaired_exact_link'];sol[d['person_id']][0]+=1;sol[d['person_id']][1]+=d['repaired_exact_link']
 sr=[{'event_id':k[0],'round_type_id':k[1],'attempt_index':k[2],'denominator_n':v[0],'linked_n':v[1],'link_rate':v[1]/v[0]} for k,v in sorted(strata.items())]
 sor=[{'person_id':k,'denominator_n':v[0],'linked_n':v[1],'link_rate':v[1]/v[0]} for k,v in sorted(sol.items())]
 coll={'|'.join(map(str,k)):v for k,v in amap.items() if len(v)>1}
 wcsv(OUT/'CUBE_REV_0.10.5-R1.23_P1_REGENERATED_CROSSWALK.csv',rows);wcsv(OUT/'CUBE_REV_0.10.5-R1.23_P1_SOURCE_LOCAL_ATTEMPT_DENOMINATOR.csv',den);wcsv(OUT/'CUBE_REV_0.10.5-R1.23_P1_LEGACY_R_AUDIT.csv',la);wcsv(OUT/'CUBE_REV_0.10.5-R1.23_P1_POSITIVITY_STRATA.csv',sr);wcsv(OUT/'CUBE_REV_0.10.5-R1.23_P1_SOLVER_LINKAGE_STRATA.csv',sor)
 pos=[x for x in sr if x['linked_n']>0];zero=[x for x in sr if x['linked_n']==0];mixed=[x for x in sr if 0<x['linked_n']<x['denominator_n']];full=[x for x in sr if x['linked_n']==x['denominator_n']]
 exact=[x for x in rows if x['status']=='EXACT_REPAIRED_VALUE_VERIFIED']; wexact=[x for x in exact if x['official']=='wca']
 summary={'schema_version':'CUBE-REV-R1.23-P1-ROUND-BUCKET-REGENERATION-1','pinned_commit':PIN,'byte_audit':audit,'snapshot':{'recon_records':len(recons),'official_counts':dict(Counter(r.get('official') for r in recons)),'legacy_r_mappings':len(old)},'source_faithful_fresh_regeneration':{'mapping_rows':len(frows),'distinct_recon_ids':len(fids)},'round_repair_contract':{'first':['1','d'],'qualification_exact_only':['h','0'],'second':['2','e','g'],'third':['3'],'final':['f','c','b'],'legacy_labels':['R1','R2','R3','Fi'],'ordinary_4x4_added':'444'},'repaired_regeneration':{'all_exact_recon_rows':len(exact),'wca_exact_recon_rows':len(wexact),'exact_unique_attempts':len(amap),'attempts_with_multiple_recon_versions':len(coll),'status_counts_all':dict(sc),'status_counts_wca':dict(wsc),'event_counts_exact':dict(evc)},'round_vocabulary':{'all':dict(roundall),'wca':dict(roundwca)},'legacy_audit_counts':dict(Counter(x['audit_state'] for x in la)),'source_local_denominator':{'nonzero_attempt_slots':len(den),'linked_attempt_slots':sum(d['repaired_exact_link'] for d in den),'attempt_link_rate':sum(d['repaired_exact_link'] for d in den)/len(den),'strata_total':len(sr),'strata_with_any_link':len(pos),'strata_zero_link':len(zero),'strata_mixed':len(mixed),'strata_all_linked':len(full)},'authority':{'selection_probability_target':'P(exact repaired reconstruction link | source-local sidecar attempt slot covariates)','causal':False,'population_wca_generalization':False,'model_gate':'POSITIVITY_DIAGNOSTICS_REQUIRED_POST_ARTIFACT'}}
 (OUT/'CUBE_REV_0.10.5-R1.23_P1_REGENERATION_SUMMARY.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf-8');(OUT/'CUBE_REV_0.10.5-R1.23_P1_COLLISION_CLUSTERS.json').write_text(json.dumps(coll,indent=2,ensure_ascii=False),encoding='utf-8');(OUT/'CUBE_REV_0.10.5-R1.23_P1_BYTE_AUDIT.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False),encoding='utf-8')
 print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()
