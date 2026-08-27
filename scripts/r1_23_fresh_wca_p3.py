#!/usr/bin/env python3
from __future__ import annotations
import concurrent.futures as cf
import csv, datetime as dt, gzip, hashlib, json, time, urllib.request
from collections import Counter, defaultdict
from decimal import Decimal, ROUND_FLOOR
from pathlib import Path

VERSION='CUBE-REV 0.10.5-R1.23-P3'
PIN='e5a6bb14961b5b26c882f9fb3bf13d61d9eba890'
REPO='2017YANR02/cuberoot.me'
RECONS_URL=f'https://raw.githubusercontent.com/{REPO}/{PIN}/data/recon_backup/recons_backup.json'
RECONS_BLOB='681adbeba019ef1fc657d6927287fd00dbca6c87'
OUT=Path('r1_23_output_p3'); RAW=OUT/'wca_api_raw_gz'; OUT.mkdir(exist_ok=True); RAW.mkdir(exist_ok=True)
API='https://www.worldcubeassociation.org/api/v0/competitions/{}/results'
EVENT={'3x3':'333','2x2':'222','4x4':'444','5x5':'555','6x6':'666','7x7':'777','3bld':'333bf','4bld':'444bf','5bld':'555bf','mbld':'333mbf','oh':'333oh','fmc':'333fm','feet':'333ft','pyra':'pyram','pyraminx':'pyram','mega':'minx','megaminx':'minx','square1':'sq1','square-1':'sq1','sq1':'sq1','clock':'clock','skewb':'skewb'}

def norm_event(x):
 s=str(x or '').strip().lower(); return EVENT.get(s)

def round_candidates(x):
 if x is None: return []
 s=str(x).strip()
 if s in ('1','d'): return ['1','d']
 if s in ('h','0'): return [s]
 if s in ('2','e','g'): return ['2','e','g']
 if s=='3': return ['3']
 if s in ('f','c','b'): return ['f','c','b']
 if s=='R1': return ['1','d']
 if s=='R2': return ['2','e','g']
 if s=='R3': return ['3']
 if s=='Fi': return ['f','c','b']
 return []

def raw_cs(x):
 try:
  d=Decimal(str(x))
  if not d.is_finite() or d<0: return None
  return int((d*100).to_integral_value(rounding=ROUND_FLOOR))
 except Exception: return None

def blob_sha1(b): return hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()

def get(url, timeout=120, retries=3):
 err=None
 for i in range(retries):
  try:
   req=urllib.request.Request(url,headers={'User-Agent':'CUBE-REV-R1.23-P3/1.0 research'})
   with urllib.request.urlopen(req,timeout=timeout) as r: return r.read(),r.status
  except Exception as e:
   err=e; time.sleep(1.5*(i+1))
 raise err

def fetch_comp(comp):
 url=API.format(comp); t0=time.time()
 try:
  b,status=get(url,120,3); parsed=json.loads(b)
  if not isinstance(parsed,list): raise ValueError('WCA result payload not list')
  (RAW/f'{comp}.json.gz').write_bytes(gzip.compress(b,compresslevel=9))
  return comp,parsed,{'competition_id':comp,'http_status':status,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'result_rows':len(parsed),'elapsed_s':round(time.time()-t0,3),'error':''}
 except Exception as e:
  return comp,None,{'competition_id':comp,'http_status':'','bytes':0,'sha256':'','result_rows':0,'elapsed_s':round(time.time()-t0,3),'error':repr(e)}

def write_csv(path,rows,fields=None):
 rows=list(rows); fields=fields or (list(rows[0]) if rows else [])
 with path.open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore'); w.writeheader(); w.writerows(rows)

def main():
 rb,_=get(RECONS_URL); got=blob_sha1(rb)
 if got!=RECONS_BLOB: raise SystemExit(f'recons blob mismatch {got}')
 recons=json.loads(rb); wca=[r for r in recons if r.get('official')=='wca']
 comps=sorted({r.get('compWcaId') for r in wca if r.get('compWcaId')})
 fetched={}; manifest=[]
 with cf.ThreadPoolExecutor(max_workers=8) as ex:
  futs=[ex.submit(fetch_comp,c) for c in comps]
  for fut in cf.as_completed(futs):
   c,data,meta=fut.result(); manifest.append(meta)
   if data is not None: fetched[c]=data
 manifest.sort(key=lambda x:x['competition_id'])
 write_csv(OUT/'CUBE_REV_0.10.5-R1.23_P3_WCA_API_RESPONSE_MANIFEST.csv',manifest)
 idx=defaultdict(lambda:defaultdict(lambda:defaultdict(dict)))
 for comp,rows in fetched.items():
  for e in rows:
   person=str(e.get('wca_id') or ''); ev=str(e.get('event_id') or ''); rt=str(e.get('round_type_id') or ''); a=e.get('attempts') or []
   if person and ev and rt and isinstance(a,list): idx[comp][person][ev][rt]=a
 out=[]; exact=defaultdict(list)
 for r in recons:
  rid=r.get('id'); official=r.get('official'); comp=r.get('compWcaId') or ''; person=r.get('personId') or ''; ev=norm_event(r.get('event')); rc=round_candidates(r.get('round'))
  try: sn=int(r.get('solveNum')) if r.get('solveNum') not in (None,'') else None
  except Exception: sn=None
  rcs=raw_cs(r.get('rawTime')); candidates=[]
  if not rid: status='KEY_INCOMPLETE_ID'
  elif not comp or not person or not sn: status='KEY_INCOMPLETE_COMP_PERSON_SOLVENUM'
  elif not ev: status='EVENT_UNSUPPORTED'
  elif not rc: status='ROUND_TOKEN_UNMAPPED'
  elif comp not in fetched: status='WCA_API_COMP_FETCH_FAILED'
  elif person not in idx[comp]: status='WCA_API_PERSON_MISSING'
  elif ev not in idx[comp][person]: status='WCA_API_EVENT_MISSING'
  else:
   for rt in rc:
    arr=idx[comp][person][ev].get(rt)
    if arr is None: continue
    if sn<1 or sn>len(arr): candidates.append((rt,None,'OUT_OF_RANGE')); continue
    v=arr[sn-1]
    if v==0: state='ZERO_PLACEHOLDER'
    elif isinstance(v,(int,float)) and v<0: state='NEGATIVE_RESULT'
    elif rcs is None: state='POSITION_ONLY'
    elif v==rcs: state='VALUE_MATCH'
    elif v-rcs==200: state='PLUS2_COMPATIBLE'
    else: state='VALUE_MISMATCH'
    candidates.append((rt,v,state))
   vm=[c for c in candidates if c[2]=='VALUE_MATCH']; pos=[c for c in candidates if c[1] not in (None,0)]
   if len(vm)==1: status='EXACT_FRESH_WCA_VALUE_VERIFIED'
   elif len(vm)>1: status='ROUND_CANDIDATE_COLLISION_VALUE_MATCH'
   elif len([c for c in candidates if c[2]=='PLUS2_COMPATIBLE'])==1 and len(pos)==1: status='PLUS2_COMPATIBLE_REMAND'
   elif len([c for c in candidates if c[2]=='NEGATIVE_RESULT'])==1 and len(pos)==1: status='NEGATIVE_RESULT_REMAND'
   elif len(pos)==1 and pos[0][2]=='POSITION_ONLY': status='POSITION_LINK_VALUE_NOT_TESTABLE'
   elif len(pos)==1: status='POSITION_LINK_VALUE_MISMATCH'
   elif len(pos)>1: status='ROUND_CANDIDATE_AMBIGUOUS'
   else: status='WCA_API_EVENT_ROUND_ATTEMPT_MISSING'
  vm=[c for c in candidates if c[2]=='VALUE_MATCH']; chosen=vm[0] if len(vm)==1 else None
  er=f'{ev}_{chosen[0]}' if chosen else ''; key=f'{comp}|{person}|{er}|{sn}' if chosen else ''
  row={'recon_id':rid,'official':official,'event_raw':r.get('event'),'event_wca':ev,'competition_id':comp,'person_id':person,'round_raw':r.get('round'),'solve_num':sn,'rawTime':r.get('rawTime'),'raw_time_cs_floor':rcs,'status':status,'candidate_count':len(candidates),'candidate_rounds':';'.join(c[0] for c in candidates),'candidate_values':';'.join(str(c[1]) for c in candidates),'candidate_states':';'.join(c[2] for c in candidates),'chosen_event_round':er,'chosen_wca_value':chosen[1] if chosen else None,'attempt_key':key,'method':r.get('method'),'stm':r.get('stm'),'tps':r.get('tps'),'reconstructor':r.get('reconer'),'reconstructor_id':r.get('reconerId')}
  out.append(row)
  if chosen: exact[key].append(row)
 write_csv(OUT/'CUBE_REV_0.10.5-R1.23_P3_FRESH_WCA_CROSSWALK.csv',out)
 exact_rows=[v for xs in exact.values() for v in xs]; write_csv(OUT/'CUBE_REV_0.10.5-R1.23_P3_FRESH_WCA_EXACT_RECON_VERSIONS.csv',exact_rows)
 collisions=[{'attempt_key':k,'n_versions':len(v),'recon_ids':';'.join(str(x['recon_id']) for x in v)} for k,v in exact.items() if len(v)>1]
 write_csv(OUT/'CUBE_REV_0.10.5-R1.23_P3_REVISION_COLLISIONS.csv',collisions,['attempt_key','n_versions','recon_ids'])
 status_wca=Counter(x['status'] for x in out if x['official']=='wca')
 summary={'schema_version':'CUBE-REV-R1.23-P3-FRESH-WCA-1','version':VERSION,'pinned_recon':{'commit':PIN,'records':len(recons),'wca_classified':len(wca),'bytes':len(rb),'git_blob_sha1':got,'sha256':hashlib.sha256(rb).hexdigest()},'fresh_wca_api':{'competitions_requested':len(comps),'competitions_ok':len(fetched),'competitions_failed':len(comps)-len(fetched),'fetched_at_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'response_manifest':'CUBE_REV_0.10.5-R1.23_P3_WCA_API_RESPONSE_MANIFEST.csv'},'operator':{'event_alias_normalization':EVENT,'round_policy':'raw round bucket candidates; missing/R1-prime/R1 Extra not inferred','strict_primary':'unique exact centisecond value match within comp+person+event+round-bucket+solveNum','plus2_negative_mismatch':'remand, not primary exact'},'result':{'status_counts_wca':dict(status_wca),'exact_recon_versions':len(exact_rows),'exact_unique_attempts':len(exact),'revision_collision_attempts':len(collisions)},'authority':{'cross_vintage_warning':'pinned CubeRoot reconstruction snapshot vs WCA API fetched at execution time','causal':False,'population_generalization':False}}
 (OUT/'CUBE_REV_0.10.5-R1.23_P3_FRESH_WCA_SUMMARY.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
 files=[]
 for p in sorted(OUT.rglob('*')):
  if p.is_file(): files.append({'path':str(p.relative_to(OUT)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 (OUT/'CUBE_REV_0.10.5-R1.23_P3_MANIFEST.json').write_text(json.dumps(files,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
