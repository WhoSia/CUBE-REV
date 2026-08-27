#!/usr/bin/env python3
import hashlib,json,os,time,urllib.parse
from pathlib import Path
import requests
from bs4 import BeautifulSoup

OUT=Path(os.environ.get('R18_HOLDOUT_ROOT','/tmp/r18holdout'));OUT.mkdir(parents=True,exist_ok=True)
MEM=Path('research/0.10.5-r1.8/evidence-support-preflight/HOLDOUT_A_MEMBERSHIP.json')
R17=Path('research/0.10.5-r1.7/evidence-full-route/FULL_ROUTE_SAMPLE_MANIFEST.json')
NULL=Path('research/0.10.5-r1.8/evidence-null-calibration-r2/NULL_THRESHOLD_SEAL.json')
UA='CUBE-REV/0.10.5-R1.8 threshold-sealed attempt-disjoint holdout route acquisition'

def alg_unescape(s):
    if s is None:return ''
    s=s.replace('-',"'").replace('&#45;','-')
    s=s.replace('&#2b;','+').replace('&#95;','_')
    return s.replace('_',' ')

def extract_route_link(html,base_url):
    soup=BeautifulSoup(html,'lxml');c=[]
    for a in soup.find_all('a',href=True):
        href=urllib.parse.urljoin(base_url,a['href'])
        if 'alg.cubing.net' not in href:continue
        q=urllib.parse.parse_qs(urllib.parse.urlparse(href).query,keep_blank_values=True)
        if 'alg' not in q or 'setup' not in q:continue
        typ=q.get('type',[''])[0]
        c.append({'alg_href':href,'raw_alg':alg_unescape(q['alg'][0]),'raw_setup':alg_unescape(q['setup'][0]),'alg_type':typ})
    if not c:return None
    c.sort(key=lambda x:(0 if x['alg_type']=='reconstruction' else 1,-len(x['raw_alg']),x['alg_href']))
    return c[0]

m=json.loads(MEM.read_text(encoding='utf-8'));n=json.loads(NULL.read_text(encoding='utf-8'));r17=json.loads(R17.read_text(encoding='utf-8'))
assert m['status']=='PASS_MEMBERSHIP_FROZEN' and m['selected_n']==900 and m['overlap_with_r17_n']==0
assert n['status']=='SEALED_BEFORE_HOLDOUT_SCORE' and n['holdout_outcomes_seen'] is False
assert n['seal_sha256']=='1343a667600a4a859ae081b3b3042cbe365e447b7b082dd7ebf77b9edc8494ea'
assert hashlib.sha256(R17.read_bytes()).hexdigest()=='ce7de5db2c2448d13af922930997fedf6196c6a5f2d573425d4d22fdc3d14bbe'
used={(int(x['result_id']),int(x['attempt_number'])) for x in r17['records']}
selected={(int(x['result_id']),int(x['attempt_number'])) for x in m['records']}
assert len(selected)==900 and not (used&selected)

sess=requests.Session();sess.headers['User-Agent']=UA
records=[];fail={}
for i,base in enumerate(m['records']):
    rec={**base}
    try:
        rr=sess.get(base['url'],timeout=30);rr.raise_for_status();link=extract_route_link(rr.text,base['url'])
        rec['detail_http']=rr.status_code;rec['detail_bytes']=len(rr.content);rec['detail_sha256']=hashlib.sha256(rr.content).hexdigest()
        if link:
            rec.update(link);rec['route_source_status']='RAW_ALG_CUBING_LINK'
        else:
            rec['route_source_status']='NO_ALG_LINK';fail['NO_ALG_LINK']=fail.get('NO_ALG_LINK',0)+1
    except Exception as e:
        rec['route_source_status']='FETCH_ERROR';rec['error']=str(e)[:300];fail['FETCH_ERROR']=fail.get('FETCH_ERROR',0)+1
    records.append(rec)
    if (i+1)%100==0:print(f'R18_HOLDOUT_FETCH_PROGRESS {i+1}/900',flush=True)
    if i+1<len(m['records']):time.sleep(0.08)
raw=sum(x.get('route_source_status')=='RAW_ALG_CUBING_LINK' for x in records)
out={
 'schema_version':'CR0105R18-HOLDOUT-A-ROUTE-MANIFEST-1',
 'status':'PASS' if len(records)==900 and raw>=855 else 'HOLD_ROUTE_SOURCE',
 'threshold_seal_semantic_sha256':n['seal_sha256'],
 'threshold_seal_file_sha256':hashlib.sha256(NULL.read_bytes()).hexdigest(),
 'holdout_membership_file_sha256':hashlib.sha256(MEM.read_bytes()).hexdigest(),
 'r17_manifest_sha256':hashlib.sha256(R17.read_bytes()).hexdigest(),
 'holdout_n':len(records),'raw_route_source_n':raw,'raw_route_source_rate':raw/900,
 'route_source_failures':fail,'r17_attempt_overlap_n':len(used&selected),
 'records':records,'human_observations':0,
 'authority':'RESEARCH_ONLY',
 'ordering_proof':'NULL_THRESHOLD_SEAL was present and verified before the first holdout detail-page request in this process.'
}
(OUT/'HOLDOUT_A_ROUTE_MANIFEST.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:out[k] for k in ['status','holdout_n','raw_route_source_n','raw_route_source_rate','route_source_failures','r17_attempt_overlap_n','threshold_seal_semantic_sha256']},indent=2))
if out['status']!='PASS':raise SystemExit(20)
