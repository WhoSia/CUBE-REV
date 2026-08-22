#!/usr/bin/env python3
import hashlib,json,os
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path
import requests
from bs4 import BeautifulSoup

OUT=Path(os.environ.get('R114_ROOT','/tmp/r114'));OUT.mkdir(parents=True,exist_ok=True)
NAPKIN=Path('research/0.10.5-r1.14/NAPKIN_G4_PREREGISTRATION.json')
LEDGER=Path('research/0.10.5-r1.14/GENERATION_INHERITANCE_LEDGER.json')
n=json.loads(NAPKIN.read_text(encoding='utf-8'));g=json.loads(LEDGER.read_text(encoding='utf-8'))
assert n['status']=='FROZEN_BEFORE_G4_ROUTE_RECLASSIFICATION_AND_BEFORE_G4_NETWORK_SNAPSHOT'
assert g['generation']=='ROUX-MEASUREMENT-G4'
assert n['freshness_design']['ordering'][0].startswith('Commit this NAPKIN')

def parse_index(text):
    soup=BeautifulSoup(text,'lxml');table=soup.find('table')
    if table is None: raise RuntimeError('R114_RECO_TABLE_NOT_FOUND')
    rows=[]
    for tr in table.find_all('tr'):
        td=tr.find_all('td')
        if not td: continue
        vals=[' '.join(x.stripped_strings) for x in td]
        try: rid=int(vals[0])
        except Exception: continue
        # Event is diagnostic metadata only. Membership in the baseline ID set uses rid alone.
        event=vals[1].strip() if len(vals)>1 else None
        rows.append({'reco_id':rid,'event':event})
    return rows

s=requests.Session();s.headers['User-Agent']='CUBE-REV/0.10.5-R1.14 G4 baseline-vintage freeze; research-only single index read'
r=s.get('https://reco.nz/solve/',timeout=90);r.raise_for_status()
rows=parse_index(r.text)
ids=[x['reco_id'] for x in rows];unique=sorted(set(ids))
canon='\n'.join(str(x) for x in unique).encode('utf-8')
events=Counter(x.get('event') or 'UNKNOWN' for x in rows)
out={
  'schema_version':'CR0105R114-G4-BASELINE-VINTAGE-1',
  'generation':'ROUX-MEASUREMENT-G4',
  'status':'PASS_G4_BASELINE_VINTAGE_FROZEN' if unique and len(unique)==len(ids) else 'HOLD_G4_BASELINE_INDEX_INTEGRITY',
  'ordering_proof':{
    'napkin_committed_before_network_read':True,
    'generation_ledger_committed_before_network_read':True,
    'g4_route_reclassification_before_this_read':False,
    'g4_feature_or_null_scoring_before_this_read':False,
    'fresh_authority_scoring_before_this_read':False
  },
  'retrieval':{
    'url':'https://reco.nz/solve/','retrieved_at_utc':datetime.now(timezone.utc).isoformat(),
    'http_status':r.status_code,'html_bytes':len(r.content),'html_sha256':hashlib.sha256(r.content).hexdigest()
  },
  'baseline_definition':{
    'membership':'every integer reco_id parsed from the live index table, regardless of event/method/reconstruction/linkage/geometry/score',
    'uses_method':False,'uses_route_detail':False,'uses_linkage':False,'uses_geometry':False,'uses_features':False,'uses_null_score':False
  },
  'live':{
    'row_n':len(ids),'unique_reco_id_n':len(unique),'duplicate_id_rows':len(ids)-len(unique),
    'min_reco_id':min(unique) if unique else None,'max_reco_id':max(unique) if unique else None,
    'id_set_sha256':hashlib.sha256(canon).hexdigest(),'event_counts_diagnostic_only':dict(sorted(events.items()))
  },
  'baseline_reco_ids':unique,
  'authority':{
    'baseline_only':True,'route_detail_fetch_performed':False,'method_filter_performed_for_membership':False,
    'linkage_performed':False,'geometry_scoring_performed':False,'null_scoring_performed':False,
    'roux_future_scoring_authority':False
  },
  'human_observations':0
}
(OUT/'G4_BASELINE_VINTAGE.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in out.items() if k!='baseline_reco_ids'},indent=2,ensure_ascii=False))
if out['status']!='PASS_G4_BASELINE_VINTAGE_FROZEN': raise SystemExit(20)
