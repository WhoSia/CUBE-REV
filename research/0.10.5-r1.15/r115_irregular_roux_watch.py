#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, os, time, urllib.parse
from datetime import datetime, timezone
from pathlib import Path
import requests
from bs4 import BeautifulSoup

OUT=Path(os.environ.get('R115_ROOT','/tmp/r115'));OUT.mkdir(parents=True,exist_ok=True)
BASE=json.load(open('research/0.10.5-r1.14/evidence-baseline/G4_BASELINE_VINTAGE.json'))
SEAL=json.load(open('research/0.10.5-r1.15/MANUSCRIPT_BRIDGE_SEAL.json'))
assert SEAL['status']=='PASS_MANUSCRIPT_BRIDGE_WITH_COHERENT_METHOD_CLAIM_HOLD_PREPRINT_FREEZE'
assert SEAL['measurement_generation']=='ROUX-MEASUREMENT-G4'
assert SEAL['roux_freshness_before_watch']['baseline_id_set_sha256']==BASE['live']['id_set_sha256']
assert SEAL['roux_freshness_before_watch']['authority_threshold']==20
BASE_IDS=set(map(int,BASE['baseline_reco_ids']))

def parse_index(text):
    soup=BeautifulSoup(text,'lxml'); table=soup.find('table')
    if table is None: raise RuntimeError('R115_RECO_TABLE_NOT_FOUND')
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
def has_raw_route(html,base_url):
    soup=BeautifulSoup(html,'lxml')
    for a in soup.find_all('a',href=True):
        href=urllib.parse.urljoin(base_url,a['href'])
        if 'alg.cubing.net' not in href: continue
        q=urllib.parse.parse_qs(urllib.parse.urlparse(href).query,keep_blank_values=True)
        if 'alg' in q and 'setup' in q and alg_unescape(q['alg'][0]).strip(): return True
    return False

sess=requests.Session();sess.headers['User-Agent']='CUBE-REV/0.10.5-R1.15 irregular Roux freshness watch; research-only'
r=sess.get('https://reco.nz/solve/',timeout=90);r.raise_for_status();rows=parse_index(r.text)
ids={x['reco_id'] for x in rows};missing=sorted(BASE_IDS-ids);new_ids=sorted(ids-BASE_IDS)
new_roux=sorted([x for x in rows if x['reco_id'] not in BASE_IDS and x['is_3x3'] and x['is_roux']],key=lambda x:x['reco_id'])
route_rows=[]
for i,x in enumerate(new_roux):
    rid=x['reco_id']; url=f'https://reco.nz/solve/{rid}'
    status='FETCH_ERROR'; raw=False; err=None
    try:
        q=sess.get(url,timeout=30);q.raise_for_status();raw=has_raw_route(q.text,url);status='RAW_ALG_CUBING_LINK' if raw else 'NO_ALG_LINK'
    except Exception as e: err=str(e)[:300]
    route_rows.append({'reco_id':rid,'route_status':status,'raw_route':raw,'error':err})
    if i+1<len(new_roux): time.sleep(.05)
raw_n=sum(x['raw_route'] for x in route_rows)
threshold=20
status='HOLD_BASELINE_INTEGRITY' if missing else ('TRIGGER_FROZEN_G4_AUTHORITY_COURT' if raw_n>=threshold else 'NO_CHANGE' if raw_n==0 else 'ACCUMULATING_DATA_WAIT')
out={
  'schema_version':'CR0105R115-IRREGULAR-ROUX-WATCH-1',
  'status':status,
  'watch_mode':'IRREGULAR_RESEARCH_TURN_NOT_AUTOMATION',
  'ordering':{'manuscript_bridge_seal_preceded_watch':True,'g4_baseline_unchanged':True,'g4_reference_definitions_mutated':False,'authority_scoring_performed':False},
  'retrieval':{'retrieved_at_utc':datetime.now(timezone.utc).isoformat(),'http_status':r.status_code,'html_bytes':len(r.content),'html_sha256':hashlib.sha256(r.content).hexdigest()},
  'baseline':{'id_n':len(BASE_IDS),'max_id':max(BASE_IDS),'id_set_sha256':BASE['live']['id_set_sha256']},
  'live':{'id_n':len(ids),'max_id':max(ids) if ids else None},
  'delta':{'missing_baseline_id_n':len(missing),'new_id_n_all_events':len(new_ids),'new_ids_all_events':new_ids,'new_3x3_roux_index_n':len(new_roux),'new_3x3_roux_ids':[x['reco_id'] for x in new_roux]},
  'roux_accumulation':{'new_roux_index_n':len(new_roux),'new_raw_roux_n':raw_n,'authority_threshold':threshold,'progress':f'{raw_n}/{threshold}','route_rows':route_rows},
  'authority':{'roux_future_scoring_authority':False,'authority_court_may_reopen':raw_n>=threshold and not missing,'reason':'Frozen G4 authority court may reopen only at >=20 post-freeze raw Roux routes; this watch never scores outcomes.'},
  'human_observations':0
}
(OUT/'IRREGULAR_ROUX_WATCH.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({k:out[k] for k in ['status','baseline','live','delta','roux_accumulation','authority']},indent=2,ensure_ascii=False))
if missing: raise SystemExit(20)
