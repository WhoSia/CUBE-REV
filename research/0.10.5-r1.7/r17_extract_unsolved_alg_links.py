#!/usr/bin/env python3
import json,urllib.parse,time,hashlib
from pathlib import Path
import requests
from bs4 import BeautifulSoup

inp=json.load(open('research/0.10.5-r1.7/evidence-state-smoke2/STATE_SMOKE_INPUT.json'))
st=json.load(open('research/0.10.5-r1.7/evidence-state-smoke-kpattern/STATE_ENGINE_SMOKE_KPATTERN.json'))
uns={r['reco_id'] for r in st['results'] if not r.get('final_kpattern_solved',False)}
base={r['reco_id']:r for r in inp['accepted_records']}
s=requests.Session();s.headers['User-Agent']='CUBE-REV/0.10.5-R1.7 unsolved provenance audit; low-rate public research check'
out=[]
for rid in sorted(uns,reverse=True):
    r=base[rid]; rec={'reco_id':rid,'url':r['url'],'method':r['method'],'attempt_value':r['attempt_value'],'parsed_moves':r['moves'],'page_scramble':r['scramble'],'lines':r['lines']}
    try:
        rr=s.get(r['url'],timeout=30);rr.raise_for_status(); soup=BeautifulSoup(rr.text,'lxml')
        links=[]
        for a in soup.find_all('a',href=True):
            href=urllib.parse.urljoin(r['url'],a['href'])
            if 'alg.cubing.net' not in href: continue
            q=urllib.parse.parse_qs(urllib.parse.urlparse(href).query,keep_blank_values=True)
            if 'alg' in q:
                links.append({'href':href,'alg':q.get('alg',[''])[0],'setup':q.get('setup',[''])[0],'type':q.get('type',[''])[0],'view':q.get('view',[''])[0]})
        rec['http']=rr.status_code; rec['html_sha256']=hashlib.sha256(rr.content).hexdigest(); rec['alg_links']=links
    except Exception as e: rec['error']=str(e)[:300]
    out.append(rec);time.sleep(.08)
res={'schema_version':'CR0105R17-UNSOLVED-ALG-LINK-EXTRACT-1','status':'PASS' if len(out)==len(uns) and all(r.get('alg_links') for r in out) else 'HOLD','unsolved_count':len(uns),'records':out,'human_observations':0}
Path('research/0.10.5-r1.7/evidence-unsolved-audit').mkdir(parents=True,exist_ok=True)
Path('research/0.10.5-r1.7/evidence-unsolved-audit/UNSOLVED_ALG_LINK_EXTRACT.json').write_text(json.dumps(res,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'status':res['status'],'unsolved_count':len(uns),'alg_link_counts':{str(r['reco_id']):len(r.get('alg_links',[])) for r in out}},indent=2))
