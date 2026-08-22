#!/usr/bin/env python3
import hashlib,json,os,time,urllib.parse
from pathlib import Path
from datetime import datetime,timezone
import requests
from bs4 import BeautifulSoup

OUT=Path(os.environ.get('R114_ROOT','/tmp/r114'));OUT.mkdir(parents=True,exist_ok=True)
BASE=json.load(open('research/0.10.5-r1.14/evidence-baseline/G4_BASELINE_VINTAGE.json'))
REF=json.load(open('research/0.10.5-r1.14/evidence-reference/G4_REFERENCE_BANK_SEAL.json'))
FREEZE=json.load(open('research/0.10.5-r1.14/G4_EXTERNAL_COURT_FREEZE.json'))
assert BASE['live']['id_set_sha256']==FREEZE['baseline_id_set_sha256']
assert REF['seal_sha256']==FREEZE['reference_seal_sha256']
assert REF['second_live_index_read_seen'] is False and REF['fresh_outcomes_seen'] is False
baseline=set(map(int,BASE['baseline_reco_ids']))

def dev_ids():
    c=json.load(open('research/0.10.5-r1.12/evidence-census/SEALED_ROUTE_CENSUS.json'))
    a=json.load(open('research/0.10.5-r1.12/evidence-acquisition/ROUX_EXPANSION_ROUTE_MANIFEST.json'))
    out=set()
    for r in c['all_clean_attempts']:
        if r.get('reco_id') is not None: out.add(int(r['reco_id']))
    for r in a['records']:
        if r.get('route_source_status')=='RAW_ALG_CUBING_LINK' and r.get('reco_id') is not None: out.add(int(r['reco_id']))
    return out
DEV=dev_ids()

def parse_index(text):
    soup=BeautifulSoup(text,'lxml'); table=soup.find('table')
    if table is None: raise RuntimeError('R114_LIVE_TABLE_NOT_FOUND')
    rows=[]
    for tr in table.find_all('tr'):
        td=tr.find_all('td')
        if not td: continue
        vals=[' '.join(x.stripped_strings) for x in td]
        try: rid=int(vals[0])
        except Exception: continue
        rows.append({'reco_id':rid,'cells':vals,'is_3x3':any(v.strip()=='3x3' for v in vals),'is_roux':any(v.strip()=='Roux' for v in vals)})
    return rows

def alg_unescape(s):
    if s is None:return ''
    s=s.replace('-',"'").replace('&#45;','-').replace('&#2b;','+').replace('&#95;','_')
    return s.replace('_',' ')
def extract_route(html,base_url):
    soup=BeautifulSoup(html,'lxml');cand=[]
    for a in soup.find_all('a',href=True):
        href=urllib.parse.urljoin(base_url,a['href'])
        if 'alg.cubing.net' not in href: continue
        q=urllib.parse.parse_qs(urllib.parse.urlparse(href).query,keep_blank_values=True)
        if 'alg' not in q or 'setup' not in q: continue
        cand.append({'alg_href':href,'raw_alg':alg_unescape(q['alg'][0]),'raw_setup':alg_unescape(q['setup'][0]),'alg_type':q.get('type',[''])[0]})
    if not cand:return None
    cand.sort(key=lambda x:(0 if x['alg_type']=='reconstruction' else 1,-len(x['raw_alg']),x['alg_href']))
    return cand[0]

def h(s): return hashlib.sha256(str(s).encode()).hexdigest()
def fetch_routes(rows,role):
    sess=requests.Session();sess.headers['User-Agent']='CUBE-REV/0.10.5-R1.14 G4 external ontology court; research-only low-rate acquisition'
    out=[]
    for i,x in enumerate(rows):
        rid=int(x['reco_id']); url=f'https://reco.nz/solve/{rid}'
        rec={'reco_id':rid,'result_id':f'RECO_{rid}','attempt_number':0,'route_key':f'reco:{rid}','method':'Roux','source':role,'url':url,'index_cells':x.get('cells',[]),'baseline_member':rid in baseline,'development_reco_overlap':rid in DEV}
        try:
            r=sess.get(url,timeout=int(FREEZE['detail_fetch']['timeout_seconds']));r.raise_for_status(); rec['detail_http']=r.status_code;rec['detail_sha256']=hashlib.sha256(r.content).hexdigest();rec['detail_bytes']=len(r.content)
            z=extract_route(r.text,url)
            if z: rec.update(z);rec['route_source_status']='RAW_ALG_CUBING_LINK'
            else: rec['route_source_status']='NO_ALG_LINK'
        except Exception as e: rec['route_source_status']='FETCH_ERROR';rec['error']=str(e)[:300]
        out.append(rec)
        if i+1<len(rows): time.sleep(float(FREEZE['detail_fetch']['request_delay_seconds']))
    return out

sess=requests.Session();sess.headers['User-Agent']='CUBE-REV/0.10.5-R1.14 G4 second live-index read; research-only'
r=sess.get(FREEZE['second_live_read']['index_url'],timeout=90);r.raise_for_status();rows=parse_index(r.text)
live_ids={x['reco_id'] for x in rows};missing=sorted(baseline-live_ids);new=sorted(live_ids-baseline)
roux3=[x for x in rows if x['is_3x3'] and x['is_roux']]
pre=[x for x in roux3 if x['reco_id'] in baseline and x['reco_id'] not in DEV]
pre.sort(key=lambda x:(h(f"R114PRE:{x['reco_id']}"),x['reco_id']))
pre=pre[:int(FREEZE['preexisting_unseen']['one_shot_cap'])]
fresh=[x for x in roux3 if x['reco_id'] not in baseline]
fresh.sort(key=lambda x:x['reco_id'])
overflow=len(fresh)>int(FREEZE['post_freeze_fresh']['hard_safety_cap'])
if overflow: fresh_to_fetch=[]
else: fresh_to_fetch=fresh
pre_routes=fetch_routes(pre,'PREEXISTING_UNSEEN_HOLDOUT')
fresh_routes=fetch_routes(fresh_to_fetch,'POST_FREEZE_FRESH_VINTAGE')
raw_pre=sum(x['route_source_status']=='RAW_ALG_CUBING_LINK' for x in pre_routes);raw_fresh=sum(x['route_source_status']=='RAW_ALG_CUBING_LINK' for x in fresh_routes)
audit={'schema_version':'CR0105R114-G4-SECOND-LIVE-READ-1','generation':'ROUX-MEASUREMENT-G4','status':'HOLD_LIVE_INDEX_INTEGRITY' if missing else ('HOLD_FRESH_BATCH_OVERFLOW' if overflow else 'PASS_SECOND_LIVE_READ_AND_MEMBERSHIP_FREEZE'),'retrieval':{'url':FREEZE['second_live_read']['index_url'],'retrieved_at_utc':datetime.now(timezone.utc).isoformat(),'http_status':r.status_code,'html_bytes':len(r.content),'html_sha256':hashlib.sha256(r.content).hexdigest()},'baseline':{'id_n':len(baseline),'id_set_sha256':BASE['live']['id_set_sha256'],'max_id':max(baseline)},'live':{'id_n':len(live_ids),'max_id':max(live_ids) if live_ids else None,'roux3_index_rows':len(roux3)},'delta':{'missing_baseline_id_n':len(missing),'missing_baseline_ids_first50':missing[:50],'new_id_n_all_events':len(new),'new_ids_all_events':new,'new_3x3_roux_index_n':len(fresh),'new_3x3_roux_ids':[x['reco_id'] for x in fresh]},'preexisting_unseen':{'eligible_index_n':len([x for x in roux3 if x['reco_id'] in baseline and x['reco_id'] not in DEV]),'selected_n':len(pre),'raw_route_n':raw_pre,'selection_cap':FREEZE['preexisting_unseen']['one_shot_cap'],'selection_used_geometry':False,'selection_used_score':False},'post_freeze_fresh':{'eligible_index_n':len(fresh),'fetched_n':len(fresh_routes),'raw_route_n':raw_fresh,'overflow':overflow,'minimum_raw_for_authority':FREEZE['post_freeze_fresh']['minimum_raw_roux_routes_for_authority']},'authority':{'second_live_index_read_seen':True,'reference_seal_predated_read':True,'fresh_authority_released':False},'human_observations':0}
(OUT/'G4_SECOND_LIVE_READ_AUDIT.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False)+'\n')
(OUT/'G4_PREEXISTING_UNSEEN_ROUTE_MANIFEST.json').write_text(json.dumps({'schema_version':'CR0105R114-PREEXISTING-UNSEEN-ROUTES-1','role':'PROSPECTIVE_ONTOLOGY_TRANSPORT_DIAGNOSTIC_ONLY','selected_index_n':len(pre),'raw_route_n':raw_pre,'records':pre_routes,'human_observations':0},indent=2,ensure_ascii=False)+'\n')
(OUT/'G4_POST_FREEZE_FRESH_ROUTE_MANIFEST.json').write_text(json.dumps({'schema_version':'CR0105R114-POST-FREEZE-FRESH-ROUTES-1','role':'FRESH_AUTHORITY_ELIGIBLE_ONLY_IF_GATES_PASS','selected_index_n':len(fresh),'raw_route_n':raw_fresh,'records':fresh_routes,'human_observations':0},indent=2,ensure_ascii=False)+'\n')
print(json.dumps(audit,indent=2,ensure_ascii=False))
if missing or overflow: raise SystemExit(20)
