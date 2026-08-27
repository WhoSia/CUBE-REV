#!/usr/bin/env python3
import hashlib,json,os,time,urllib.parse
from collections import defaultdict,Counter
from pathlib import Path
import duckdb,requests
from bs4 import BeautifulSoup

ROOT=Path('.').resolve()
DB=Path(os.environ['R112_PARENT_DB'])
OUT=Path(os.environ.get('R112_ROOT','/tmp/r112')); OUT.mkdir(parents=True,exist_ok=True)
FREEZE=Path('research/0.10.5-r1.12/ACQUISITION_FREEZE.json')
CENSUS=Path('research/0.10.5-r1.12/evidence-census/SEALED_ROUTE_CENSUS.json')
UA='CUBE-REV/0.10.5-R1.12 one-shot Roux G2 route acquisition; public reconstruction research audit'

def stable_hash(s): return hashlib.sha256(str(s).encode('utf-8')).hexdigest()
def alg_unescape(s):
    if s is None:return ''
    s=s.replace('-',"'").replace('&#45;','-')
    s=s.replace('&#2b;','+').replace('&#95;','_')
    return s.replace('_',' ')
def extract_route_link(html,base_url):
    soup=BeautifulSoup(html,'lxml'); cand=[]
    for a in soup.find_all('a',href=True):
        href=urllib.parse.urljoin(base_url,a['href'])
        if 'alg.cubing.net' not in href: continue
        q=urllib.parse.parse_qs(urllib.parse.urlparse(href).query,keep_blank_values=True)
        if 'alg' not in q or 'setup' not in q: continue
        typ=q.get('type',[''])[0]
        cand.append({'alg_href':href,'raw_alg':alg_unescape(q['alg'][0]),'raw_setup':alg_unescape(q['setup'][0]),'alg_type':typ})
    if not cand:return None
    cand.sort(key=lambda x:(0 if x['alg_type']=='reconstruction' else 1,-len(x['raw_alg']),x['alg_href']))
    return cand[0]

freeze=json.loads(FREEZE.read_text(encoding='utf-8'))
census=json.loads(CENSUS.read_text(encoding='utf-8'))
assert freeze['status']=='FROZEN_BEFORE_G2_GEOMETRY_AND_BEFORE_ROUTE_FETCH'
assert freeze['membership']['one_shot_cap']==800
assert freeze['membership']['route_geometry_variables_allowed_for_selection'] is False
assert census['status']=='PASS' and census['candidate_bank_ge_100'] is False
used={r['attempt_key'] for r in census['all_clean_attempts']}
assert len(used)==98

con=duckdb.connect(str(DB),read_only=True)
rows=con.execute("""
select r.reco_id,r.method,r.url,c.result_id,c.attempt_number,c.attempt_value,
       s.comp_year,s.competition_id,s.round_type_id,s.person_id,s.person_name,l.tier
from reco_index r
join linkage_class l using(reco_id)
join linkage_candidates c using(reco_id)
join attempt_spine s on s.result_id=c.result_id and s.attempt_number=c.attempt_number
where r.method='Roux' and l.tier in ('A_EXACT_UNIQUE','B_NORMALIZED_UNIQUE')
order by c.result_id,c.attempt_number,r.reco_id
""").fetchall()
cols=['reco_id','method','url','result_id','attempt_number','attempt_value','comp_year','competition_id','round_type_id','person_id','person_name','tier']
by=defaultdict(list)
for z in rows:
    r=dict(zip(cols,z)); key=f"{int(r['result_id'])}:{int(r['attempt_number'])}"
    if key in used: continue
    by[key].append(r)
canonical=[]
for key,rs in by.items():
    rs.sort(key=lambda r:stable_hash(f"R112ACQ:{r['result_id']}:{r['attempt_number']}:{r['reco_id']}"))
    r=rs[0].copy(); r['attempt_key']=key; r['duplicate_reconstruction_count']=len(rs)
    r['membership_hash']=stable_hash(f"R112ORDER:{r['result_id']}:{r['attempt_number']}")
    canonical.append(r)
canonical.sort(key=lambda r:(r['membership_hash'],r['attempt_key']))
cap=int(freeze['membership']['one_shot_cap']); selected=canonical[:cap]
membership={
  'schema_version':'CR0105R112-ONE-SHOT-ROUX-EXPANSION-MEMBERSHIP-1',
  'status':'PASS_MEMBERSHIP_FROZEN',
  'parent_db_sha256':os.environ.get('R112_PARENT_DB_SHA256',''),
  'existing_attempts_excluded_n':len(used),
  'eligible_unique_official_attempts_n':len(canonical),
  'one_shot_cap':cap,
  'selected_n':len(selected),
  'selection_exhausted_pool':len(canonical)<=cap,
  'selection_uses_geometry':False,
  'selection_uses_annotation_text':False,
  'selection_uses_null_score':False,
  'records':selected,
  'human_observations':0
}
(OUT/'ROUX_EXPANSION_MEMBERSHIP.json').write_text(json.dumps(membership,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

sess=requests.Session(); sess.headers['User-Agent']=UA
records=[]; failures=Counter()
for i,base in enumerate(selected):
    rec=base.copy()
    try:
        rr=sess.get(base['url'],timeout=30); rr.raise_for_status()
        rec['detail_http']=rr.status_code; rec['detail_bytes']=len(rr.content); rec['detail_sha256']=hashlib.sha256(rr.content).hexdigest()
        link=extract_route_link(rr.text,base['url'])
        if link:
            rec.update(link); rec['route_source_status']='RAW_ALG_CUBING_LINK'
        else:
            rec['route_source_status']='NO_ALG_LINK'; failures['NO_ALG_LINK']+=1
    except Exception as e:
        rec['route_source_status']='FETCH_ERROR'; rec['error']=str(e)[:300]; failures['FETCH_ERROR']+=1
    records.append(rec)
    if (i+1)%100==0 or i+1==len(selected): print(f'R112_ACQ_PROGRESS {i+1}/{len(selected)}',flush=True)
    if i+1<len(selected): time.sleep(float(freeze['fetch']['inter_request_delay_seconds']))
raw=sum(r.get('route_source_status')=='RAW_ALG_CUBING_LINK' for r in records)
out={
  'schema_version':'CR0105R112-ONE-SHOT-ROUX-EXPANSION-ROUTES-1',
  'status':'PASS_ACQUIRED' if len(records)==len(selected) else 'HOLD_ACQUISITION_INCOMPLETE',
  'membership_sha256':hashlib.sha256((OUT/'ROUX_EXPANSION_MEMBERSHIP.json').read_bytes()).hexdigest(),
  'selected_n':len(selected),'raw_route_source_n':raw,
  'raw_route_source_rate':raw/max(1,len(selected)),
  'route_source_failures':dict(failures),
  'records':records,
  'fresh_network_read':True,
  'fresh_index_scan':False,
  'new_linkage_performed':False,
  'epistemic_role':'DEVELOPMENT_AND_CALIBRATION_ONLY',
  'human_observations':0,
  'claim_boundary':'One-shot provenance-frozen route acquisition only. No G2 geometry or null score was computed in membership selection or this fetch process.'
}
(OUT/'ROUX_EXPANSION_ROUTE_MANIFEST.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:out[k] for k in ['status','selected_n','raw_route_source_n','raw_route_source_rate','route_source_failures']},indent=2))
print(json.dumps({k:membership[k] for k in ['eligible_unique_official_attempts_n','selected_n','selection_exhausted_pool']},indent=2))
