#!/usr/bin/env python3
import json,urllib.parse,requests,hashlib
from bs4 import BeautifulSoup
from pathlib import Path

def alg_unescape(s):
    if s is None:return ''
    s=s.replace('-',"'").replace('&#45;','-')
    s=s.replace('&#2b;','+').replace('&#95;','_')
    s=s.replace('_',' ')
    return s

def extract(url):
    rr=requests.get(url,headers={'User-Agent':'CUBE-REV/0.10.5-R1.7 raw-route decoder preflight'},timeout=30);rr.raise_for_status()
    soup=BeautifulSoup(rr.text,'lxml');cs=[]
    for a in soup.find_all('a',href=True):
        href=urllib.parse.urljoin(url,a['href'])
        if 'alg.cubing.net' not in href:continue
        q=urllib.parse.parse_qs(urllib.parse.urlparse(href).query,keep_blank_values=True)
        if 'alg' not in q or 'setup' not in q:continue
        cs.append({'href':href,'alg':alg_unescape(q['alg'][0]),'setup':alg_unescape(q['setup'][0]),'type':q.get('type',[''])[0]})
    cs.sort(key=lambda x:(0 if x['type']=='reconstruction' else 1,-len(x['alg'])))
    return {'url':url,'http':rr.status_code,'html_sha256':hashlib.sha256(rr.content).hexdigest(),'candidates':cs,'chosen':cs[0] if cs else None}
rows=[extract('https://reco.nz/solve/12564'),extract('https://reco.nz/solve/11919')]
out={'schema_version':'CR0105R17-RAW-ROUTE-PREFLIGHT-1','status':'PASS' if all(x['chosen'] for x in rows) else 'HOLD','records':rows,'human_observations':0}
Path('research/0.10.5-r1.7/evidence-raw-route-preflight').mkdir(parents=True,exist_ok=True)
Path('research/0.10.5-r1.7/evidence-raw-route-preflight/RAW_ROUTE_EXTRACT.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'status':out['status'],'counts':[len(x['candidates']) for x in rows]},indent=2))
if out['status']!='PASS':raise SystemExit(2)
