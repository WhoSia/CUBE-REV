#!/usr/bin/env python3
import hashlib,json,os,re
from pathlib import Path
import duckdb,requests
from bs4 import BeautifulSoup

OUT=Path(os.environ.get('R110_WATCH_ROOT','/tmp/r110watch'));OUT.mkdir(parents=True,exist_ok=True)
DB=Path(os.environ['R110_PARENT_DB'])
SEAL=Path('research/0.10.5-r1.10/LOCAL_AUTHORITY_SEAL.json')
local=json.loads(SEAL.read_text())
assert local['fresh_network_read_before_this_seal'] is False
assert local['fresh_watch_permitted_after_this_commit'] is True
assert local['fresh_confirmatory_scoring_authorized'] is False

def ids_from_html(text):
    soup=BeautifulSoup(text,'lxml');table=soup.find('table')
    if table is None: raise RuntimeError('R110_RECO_TABLE_NOT_FOUND')
    ids=[]
    for tr in table.find_all('tr'):
        td=tr.find_all('td')
        if len(td)<2: continue
        vals=[' '.join(x.stripped_strings) for x in td]
        try: rid=int(vals[0])
        except Exception: continue
        if vals[1].strip()=='3x3': ids.append(rid)
    return ids

con=duckdb.connect(str(DB),read_only=True)
frozen={int(x[0]) for x in con.execute('select reco_id from reco_index').fetchall()}
con.close()
s=requests.Session();s.headers['User-Agent']='CUBE-REV/0.10.5-R1.10 fresh-vintage watch; research-only low-rate audit'
r=s.get('https://reco.nz/solve/',timeout=90);r.raise_for_status()
live_list=ids_from_html(r.text);live=set(live_list)
missing=sorted(frozen-live);new=sorted(live-frozen)
canon='\n'.join(str(x) for x in sorted(live)).encode()
status='HOLD_LIVE_INDEX_INTEGRITY' if missing else ('WATCH_NEW_VINTAGE_DETECTED_ONLY' if new else 'WATCH_PASS_DATA_WAIT')
out={
 'schema_version':'CR0105R110-FRESH-VINTAGE-WATCH-1','status':status,
 'ordering_proof':{'local_authority_seal_sha256':local['seal_sha256'],'local_seal_committed_before_network_read':True,'fresh_confirmatory_scoring_authorized':False},
 'retrieval':{'url':'https://reco.nz/solve/','http_status':r.status_code,'html_bytes':len(r.content),'html_sha256':hashlib.sha256(r.content).hexdigest()},
 'frozen':{'db_sha256':os.environ.get('R110_PARENT_DB_SHA256',''),'reco_rows':len(frozen),'max_reco_id':max(frozen) if frozen else None},
 'live':{'reco_rows':len(live),'max_reco_id':max(live) if live else None,'id_set_sha256':hashlib.sha256(canon).hexdigest(),'duplicate_id_rows':len(live_list)-len(live)},
 'delta':{'missing_frozen_id_n':len(missing),'missing_frozen_ids_first50':missing[:50],'new_reco_id_n':len(new),'new_reco_ids':new,'new_ids_above_frozen_max':[x for x in new if frozen and x>max(frozen)]},
 'authority':{'watch_only':True,'route_fetch_performed':False,'linkage_performed':False,'phenotype_scoring_performed':False,'future_layered_scorer_used':False,'roux_scorer_used':False},
 'human_observations':0
}
(OUT/'FRESH_VINTAGE_WATCH.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
if missing: raise SystemExit(20)
