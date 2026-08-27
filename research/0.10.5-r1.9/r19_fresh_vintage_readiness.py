#!/usr/bin/env python3
import hashlib,json,os,re,unicodedata
from collections import Counter,defaultdict
from pathlib import Path
import duckdb,requests
from bs4 import BeautifulSoup

DB=Path(os.environ['R19_PARENT_DB']); OUT=Path(os.environ.get('R19_FRESH_ROOT','/tmp/r19fresh'));OUT.mkdir(parents=True,exist_ok=True)
R17=Path('research/0.10.5-r1.7/evidence-full-route/FULL_ROUTE_SAMPLE_MANIFEST.json')
R18=Path('research/0.10.5-r1.8/evidence-holdout-a/HOLDOUT_A_ROUTE_MANIFEST.json')
R3=Path('research/0.10.5-r1.9/evidence-nested-gate-repair/ATTEMPT_FAMILYWISE_NULL_PREREG_SEAL_R3.json')
NAP=Path('research/0.10.5-r1.9/NAPKIN_INTENT_AND_PREREGISTRATION.json')
UA='CUBE-REV/0.10.5-R1.9 post-seal fresh-vintage readiness audit'

def norm(s):
 s=unicodedata.normalize('NFKD',str(s or ''));s=''.join(c for c in s if not unicodedata.combining(c)).casefold();return ' '.join(re.sub(r'[^a-z0-9]+',' ',s).split())
def cs(s):
 s=str(s or '').strip().replace('+','').strip()
 if not s or s.upper() in {'DNF','DNS'}:return None
 try:
  if ':' in s:
   m,x=s.split(':',1);return int(round((int(m)*60+float(x))*100))
  return int(round(float(s)*100))
 except:return None
def speed(v):return '<5' if v<500 else ('5-7' if v<700 else '7-10')
def era(y):return '<=2012' if y<=2012 else ('2013-16' if y<=2016 else ('2017-19' if y<=2019 else ('2020-22' if y<=2022 else '2023-26')))
def extract(html):
 soup=BeautifulSoup(html,'lxml');table=soup.find('table')
 if not table:raise RuntimeError('R19_RECO_TABLE_NOT_FOUND')
 out=[]
 for tr in table.find_all('tr'):
  td=tr.find_all('td')
  if len(td)<11:continue
  v=[' '.join(x.stripped_strings) for x in td]
  try:rid=int(v[0])
  except:continue
  if v[1].strip()!='3x3':continue
  href=None
  for a in tr.find_all('a',href=True):
   if re.search(r'/solve/\d+',a['href']):href=a['href'];break
  out.append({'reco_id':rid,'result_text':v[2].strip(),'solver':v[3].strip(),'method':v[4].strip(),'date':v[5].strip(),'competition':v[6].strip(),'tags':v[7].strip(),'movecount':v[8].strip(),'tps':v[9].strip(),'reconstructor':v[10].strip(),'url':('https://reco.nz'+href if href and href.startswith('/') else href or f'https://reco.nz/solve/{rid}')})
 return out

def stable_rank(r):return hashlib.sha256(f"R19FRESH:{r['result_id']}:{r['attempt_number']}:{r['reco_id']}".encode()).hexdigest()

r3=json.loads(R3.read_text());nap=json.loads(NAP.read_text())
assert r3['status']=='SEALED_FOR_FUTURE_FRESH_VINTAGE_R3_NESTED_EXACT_PREREG_GATE'
assert r3['future_fresh_outcomes_seen'] is False
assert nap['fresh_vintage_readiness']['frozen_historical_reco_rows']==10596
assert nap['fresh_vintage_readiness']['frozen_historical_max_reco_id']==14051
r17=json.loads(R17.read_text())['records'];r18=json.loads(R18.read_text())['records']
hist_keys={(int(r['result_id']),int(r['attempt_number'])) for r in r17}|{(int(r['result_id']),int(r['attempt_number'])) for r in r18}
assert len(hist_keys)==1800
con=duckdb.connect(str(DB),read_only=True)
frozen_ids={int(x[0]) for x in con.execute('select reco_id from reco_index').fetchall()}
assert len(frozen_ids)==10596 and max(frozen_ids)==14051

# FIRST current-vintage network read in R1.9 occurs only after the assertions above.
s=requests.Session();s.headers['User-Agent']=UA
resp=s.get('https://reco.nz/solve/',timeout=60);resp.raise_for_status();live=extract(resp.text)
live_ids={r['reco_id'] for r in live};new=[r for r in live if r['reco_id'] not in frozen_ids]
removed=sorted(frozen_ids-live_ids)
index_full=(len(live)>=len(frozen_ids) and max(live_ids,default=-1)>=max(frozen_ids) and not removed)

tiers=Counter();linked=[]
for r in new:
 v=cs(r['result_text'])
 if v is not None and '[+2]' in r.get('tags',''):v+=200
 if v is None:tiers['U_UNMATCHED']+=1;continue
 sn,cn=norm(r['solver']),norm(r['competition'])
 cands=con.execute("""select s.result_id,s.attempt_number,s.attempt_value,s.comp_year,s.person_name,s.competition_name
 from attempt_spine s join person_norm_map pn on s.person_name=pn.person_name join competition_norm_map cnm on s.competition_name=cnm.competition_name
 where pn.solver_norm=? and cnm.competition_norm=? and s.attempt_value=?""",[sn,cn,int(v)]).fetchall()
 exact=[x for x in cands if x[4]==r['solver'] and x[5]==r['competition']]
 tier='A_EXACT_UNIQUE' if len(cands)==1 and len(exact)==1 else ('B_NORMALIZED_UNIQUE' if len(cands)==1 else ('C_AMBIGUOUS' if len(cands)>1 else 'U_UNMATCHED'))
 tiers[tier]+=1
 if tier in {'A_EXACT_UNIQUE','B_NORMALIZED_UNIQUE'}:
  x=cands[0];z={**r,'tier':tier,'result_id':int(x[0]),'attempt_number':int(x[1]),'attempt_value':int(x[2]),'comp_year':int(x[3])};z['speed']=speed(z['attempt_value']);z['era']=era(z['comp_year']);z['cell']=f"{z['speed']}|{z['era']}";z['historical_attempt_overlap']=(z['result_id'],z['attempt_number']) in hist_keys;linked.append(z)
by=defaultdict(list)
for r in linked:by[(r['result_id'],r['attempt_number'])].append(r)
canonical=[]
for k,rs in by.items():rs.sort(key=stable_rank);canonical.append(rs[0])
fresh=[r for r in canonical if not r['historical_attempt_overlap']]
modern=[r for r in fresh if r['speed']=='7-10' and r['era']=='2023-26']
cells=Counter(r['cell'] for r in fresh)

fresh_any_pre_route = len(fresh)>=200 and len(cells)>=3
modern_pre_route = len(modern)>=80
if not index_full: status='HOLD_LIVE_INDEX_NOT_SUPERSET_OF_FROZEN'
elif len(new)==0: status='READINESS_PASS_DATA_WAIT'
elif not fresh_any_pre_route: status='READINESS_PASS_NEW_RECORDS_BELOW_CONFIRMATORY_GATE'
else: status='ROUTE_VALIDATION_REQUIRED_BEFORE_CONFIRMATORY_GATE'

out={'schema_version':'CR0105R19-FRESH-VINTAGE-READINESS-1','status':status,'ordering_proof':{'r3_seal_sha256':r3['seal_sha256'],'r3_status':r3['status'],'fresh_outcomes_seen_in_seal':r3['future_fresh_outcomes_seen'],'network_read_after_local_seal_assertions':True},'retrieval':{'url':'https://reco.nz/solve/','http_status':resp.status_code,'html_bytes':len(resp.content),'html_sha256':hashlib.sha256(resp.content).hexdigest()},'frozen':{'db_sha256':os.environ.get('R19_PARENT_DB_SHA256'),'reco_rows':len(frozen_ids),'max_reco_id':max(frozen_ids),'historical_attempt_keys':len(hist_keys)},'live':{'reco_rows':len(live),'max_reco_id':max(live_ids,default=None),'removed_frozen_id_n':len(removed),'removed_frozen_ids_first20':removed[:20],'index_superset_gate':index_full},'fresh':{'new_reco_id_rows':len(new),'new_reco_ids':sorted(r['reco_id'] for r in new),'linkage_tiers':dict(tiers),'unique_linked_attempts':len(canonical),'historical_attempt_overlap_n':sum(r['historical_attempt_overlap'] for r in canonical),'novel_unique_linked_attempts':len(fresh),'novel_cells':dict(cells),'fresh_any_pre_route_gate':fresh_any_pre_route,'fresh_modern_2023_26_7_10_n':len(modern),'fresh_modern_pre_route_gate':modern_pre_route,'records':fresh},'confirmatory_authority':{'score_recovery_rate':False,'reason':'R1.9 is readiness only; route/state validation and all preregistered fresh gates must pass in a later confirmatory court before any estimate.','fresh_any_required':'>=200 novel unique-linked state-certified attempts, >=3 cells, ESS>=100','fresh_modern_required':'>=80 novel unique-linked state-certified attempts in 2023-26 × 7-10 s'},'human_observations':0,'authority':'RESEARCH_ONLY'}
(OUT/'FRESH_VINTAGE_READINESS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','ordering_proof','retrieval','frozen','live','fresh','confirmatory_authority'] if k!='fresh'}|{'fresh':{x:out['fresh'][x] for x in ['new_reco_id_rows','linkage_tiers','unique_linked_attempts','historical_attempt_overlap_n','novel_unique_linked_attempts','novel_cells','fresh_any_pre_route_gate','fresh_modern_2023_26_7_10_n','fresh_modern_pre_route_gate']}},indent=2))
if not index_full:raise SystemExit(20)
