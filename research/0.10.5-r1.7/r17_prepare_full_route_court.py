#!/usr/bin/env python3
import hashlib,json,math,os,time,urllib.parse
from collections import defaultdict,Counter
from pathlib import Path
import duckdb,requests
from bs4 import BeautifulSoup

DB=Path(os.environ['R17_PARENT_DB'])
OUT=Path(os.environ.get('R17_FULL_ROOT','/tmp/r17full'))
OUT.mkdir(parents=True,exist_ok=True)
SAMPLE_N=900
UA='CUBE-REV/0.10.5-R1.7 full-route court; low-rate public reconstruction audit'

def speed(v):
    if v<500:return '<5'
    if v<700:return '5-7'
    return '7-10'
def era(y):
    if y<=2012:return '<=2012'
    if y<=2016:return '2013-16'
    if y<=2019:return '2017-19'
    if y<=2022:return '2020-22'
    return '2023-26'
def stable_hash(s):return hashlib.sha256(s.encode()).hexdigest()
def alg_unescape(s):
    if s is None:return ''
    # Match alg.cubing.net's historical unescape_alg after standard URL decoding.
    s=s.replace('-',"'").replace('&#45;','-')
    s=s.replace('&#2b;','+').replace('&#95;','_')
    s=s.replace('_',' ')
    return s

def extract_route_link(html,base_url):
    soup=BeautifulSoup(html,'lxml'); candidates=[]
    for a in soup.find_all('a',href=True):
        href=urllib.parse.urljoin(base_url,a['href'])
        if 'alg.cubing.net' not in href: continue
        q=urllib.parse.parse_qs(urllib.parse.urlparse(href).query,keep_blank_values=True)
        if 'alg' not in q or 'setup' not in q: continue
        typ=q.get('type',[''])[0]
        candidates.append({'href':href,'raw_alg':alg_unescape(q['alg'][0]),'raw_setup':alg_unescape(q['setup'][0]),'type':typ})
    if not candidates:return None
    candidates.sort(key=lambda x:(0 if x['type']=='reconstruction' else 1, -len(x['raw_alg']), x['href']))
    return candidates[0]

con=duckdb.connect(str(DB),read_only=True)
# Canonical reconstruction per distinct official attempt: deterministic SHA rank, not recency/quality.
raw=con.execute("""
select r.reco_id,r.method,r.url,c.result_id,c.attempt_number,c.attempt_value,
       s.comp_year,s.competition_id,s.round_type_id,s.person_id,s.person_name,l.tier
from reco_index r join linkage_class l using(reco_id)
join linkage_candidates c using(reco_id)
join attempt_spine s on s.result_id=c.result_id and s.attempt_number=c.attempt_number
where l.tier in ('A_EXACT_UNIQUE','B_NORMALIZED_UNIQUE') and c.attempt_value>0 and c.attempt_value<1000
order by c.result_id,c.attempt_number,r.reco_id
""").fetchall()
cols=['reco_id','method','url','result_id','attempt_number','attempt_value','comp_year','competition_id','round_type_id','person_id','person_name','tier']
by_attempt=defaultdict(list)
for z in raw:
    r=dict(zip(cols,z)); key=(r['result_id'],r['attempt_number']); by_attempt[key].append(r)
canonical=[]
for key,rs in by_attempt.items():
    rs.sort(key=lambda r:stable_hash(f"{r['result_id']}:{r['attempt_number']}:{r['reco_id']}"))
    r=rs[0]; r['duplicate_reconstruction_count']=len(rs); r['speed']=speed(r['attempt_value']); r['era']=era(r['comp_year']); canonical.append(r)

# Target population cells are all valid WCA <10s attempts.
target_rows=con.execute("""
select case when attempt_value<500 then '<5' when attempt_value<700 then '5-7' else '7-10' end speed,
       case when comp_year<=2012 then '<=2012' when comp_year<=2016 then '2013-16' when comp_year<=2019 then '2017-19' when comp_year<=2022 then '2020-22' else '2023-26' end era,
       count(*) n
from phenotype_attempts where attempt_value>0 and attempt_value<1000
group by 1,2 order by 1,2
""").fetchall()
target={(s,e):int(n) for s,e,n in target_rows}; target_total=sum(target.values())
pools=defaultdict(list)
for r in canonical:pools[(r['speed'],r['era'])].append(r)
for k in pools:pools[k].sort(key=lambda r:stable_hash(f"R17FULL:{r['result_id']}:{r['attempt_number']}"))
linked={k:len(v) for k,v in pools.items()}

# Prospective support set: same criterion as prior target court; cells with >=5 linked and >=100 WCA population.
supported=[k for k,n in target.items() if n>=100 and linked.get(k,0)>=5]
supported_pop=sum(target[k] for k in supported)
# Allocate SAMPLE_N proportional to supported WCA target mass, then cap by linked availability and redistribute deficits.
alloc={k:0 for k in supported}; exact={k:SAMPLE_N*target[k]/supported_pop for k in supported}
for k in supported:alloc[k]=min(linked[k],int(math.floor(exact[k])))
remaining=SAMPLE_N-sum(alloc.values())
while remaining>0:
    eligible=[k for k in supported if alloc[k]<linked[k]]
    if not eligible:break
    # Largest target-share shortfall, deterministic tie break.
    k=max(eligible,key=lambda z:(exact[z]-alloc[z],target[z],z))
    alloc[k]+=1; remaining-=1
if sum(alloc.values())<SAMPLE_N: raise RuntimeError(f'R17_SAMPLE_ALLOCATION_SHORTFALL_{sum(alloc.values())}')
selected=[]
for k,n in alloc.items():selected.extend(pools[k][:n])
selected.sort(key=lambda r:stable_hash(f"R17ORDER:{r['result_id']}:{r['attempt_number']}"))
assert len(selected)==SAMPLE_N

sess=requests.Session();sess.headers['User-Agent']=UA
records=[];fail=Counter()
for i,r in enumerate(selected):
    rec={**r,'cell':f"{r['speed']}|{r['era']}"}
    try:
        rr=sess.get(r['url'],timeout=30);rr.raise_for_status(); link=extract_route_link(rr.text,r['url'])
        rec['detail_http']=rr.status_code;rec['detail_sha256']=hashlib.sha256(rr.content).hexdigest()
        if not link:
            rec['route_source_status']='NO_ALG_LINK';fail['no_alg_link']+=1
        else:
            rec.update(link);rec['route_source_status']='RAW_ALG_CUBING_LINK'
    except Exception as ex:
        rec['route_source_status']='FETCH_ERROR';rec['error']=str(ex)[:300];fail['fetch_error']+=1
    records.append(rec)
    if i+1<len(selected):time.sleep(0.10)

manifest={
 'schema_version':'CR0105R17-FULL-ROUTE-SAMPLE-1','status':'PASS' if len(records)==SAMPLE_N else 'HOLD',
 'parent_db_sha256':'a04f1d2fd351e34ec7406e63524b7b8ceb166bf8a53d4630f94c9d6a792848f1',
 'target_definition':'WCA official valid 3x3 attempts with result <10.00 s in frozen 2026-08-18 export; speed x era post-stratified descriptive target.',
 'sample_design':'Canonical one reconstruction per distinct linked WCA attempt by SHA rank; 900 attempts allocated proportional to supported WCA speed x era population, availability-capped; within-cell SHA rank selection.',
 'sample_n':SAMPLE_N,'canonical_linked_attempts_under10':len(canonical),'target_population_under10':target_total,
 'supported_target_population':supported_pop,'supported_target_fraction':supported_pop/target_total,
 'target_cells':[{'speed':k[0],'era':k[1],'population_n':target[k],'linked_n':linked.get(k,0),'supported':k in supported,'sample_n':alloc.get(k,0)} for k in sorted(target)],
 'route_source_failures':dict(fail),'raw_alg_link_records':sum(r.get('route_source_status')=='RAW_ALG_CUBING_LINK' for r in records),
 'records':records,'human_observations':0,
 'provenance_boundary':'Reco setup+alg is the route-state source. WCA linkage supplies official result/solver/competition/era. WCA export does not identify competitor scramble-group, so WCA scramble text is not an attempt-level admission key.'
}
(OUT/'FULL_ROUTE_SAMPLE_MANIFEST.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({k:manifest[k] for k in ['status','sample_n','canonical_linked_attempts_under10','target_population_under10','supported_target_fraction','route_source_failures','raw_alg_link_records']},indent=2))
if manifest['status']!='PASS':raise SystemExit(2)
