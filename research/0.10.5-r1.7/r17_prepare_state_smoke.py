#!/usr/bin/env python3
import hashlib,json,os,re,time
from collections import Counter
from pathlib import Path
import duckdb,requests
from bs4 import BeautifulSoup

DB=Path(os.environ['R17_PARENT_DB'])
OUT=Path(os.environ.get('R17_SMOKE_ROOT','/tmp/r17smoke'))
OUT.mkdir(parents=True,exist_ok=True)
UA='CUBE-REV/0.10.5-R1.7 state-replay smoke; low-rate public reconstruction audit'
MOVE_RE=re.compile(r"^(?:[URFDLBMESxyz]|[urfdlb])(?:w)?(?:2['’]?|['’])?$",re.I)
SCRAMBLE_RE=re.compile(r"^(?:(?:[URFDLB](?:w)?|[urfdlb])(?:2['’]?|['’])?\s+){8,}(?:[URFDLB](?:w)?|[urfdlb])(?:2['’]?|['’])?$",re.I)

def normtok(t):
    t=t.replace('’',"'").strip()
    if t.endswith("2'"): t=t[:-1]
    if t and t[0] in 'urfdlb' and 'w' not in t.lower():
        t=t[0].upper()+'w'+t[1:]
    return t

def parse_detail(html):
    soup=BeautifulSoup(html,'lxml')
    strings=[' '.join(x.split()) for x in soup.stripped_strings]
    scramble=next((x.replace('’',"'") for x in strings if SCRAMBLE_RE.match(x)),None)
    lines=[]; moves=[]
    for raw in strings:
        if '//' not in raw: continue
        left,comment=raw.split('//',1)
        toks=[]
        for tok in left.strip().split():
            if MOVE_RE.match(tok): toks.append(normtok(tok))
        if toks:
            lines.append({'start_index':len(moves),'moves':toks,'comment':' '.join(comment.split())[:180]})
            moves.extend(toks)
    return scramble,lines,moves

def speed_bin(v):
    if v<500:return '<5s'
    if v<700:return '5-7s'
    if v<1000:return '7-10s'
    if v<1500:return '10-15s'
    return '15s+'

con=duckdb.connect(str(DB),read_only=True)
rows=con.execute("""
select r.reco_id,r.method,r.url,c.attempt_value,c.result_id,c.attempt_number,c.competition_id,
       s.comp_year,s.person_id,s.person_name,s.round_type_id
from reco_index r join linkage_class l using(reco_id)
join linkage_candidates c using(reco_id)
join attempt_spine s on s.result_id=c.result_id and s.attempt_number=c.attempt_number
where l.tier in ('A_EXACT_UNIQUE','B_NORMALIZED_UNIQUE')
qualify count(*) over(partition by r.reco_id)=1
order by r.reco_id desc
""").fetchall()
cols=['reco_id','method','url','attempt_value','result_id','attempt_number','competition_id','comp_year','person_id','person_name','round_type_id']
frame=[dict(zip(cols,x)) for x in rows]
# deterministic diversity: rotate across method x speed cells while retaining newest-first within cell
cells={}
for r in frame:
    k=(r['method'] or 'UNKNOWN',speed_bin(r['attempt_value']))
    cells.setdefault(k,[]).append(r)
order=sorted(cells,key=lambda k:(k[0],k[1]))
queue=[]
for depth in range(30):
    for k in order:
        if depth<len(cells[k]): queue.append(cells[k][depth])

sess=requests.Session(); sess.headers['User-Agent']=UA
accepted=[]; audit=[]; reject=Counter()
for r in queue[:240]:
    rec={k:r[k] for k in cols}; rec['speed_bin']=speed_bin(r['attempt_value'])
    try:
        resp=sess.get(r['url'],timeout=30); resp.raise_for_status()
        scramble,lines,moves=parse_detail(resp.text)
        rec['html_sha256']=hashlib.sha256(resp.content).hexdigest(); rec['http']=resp.status_code
        rec['scramble']=scramble; rec['lines']=lines; rec['moves']=moves
        rec['rotation_tokens']=sum(t[0].lower() in 'xyz' for t in moves)
        rec['slice_tokens']=sum(t[0].upper() in 'MES' for t in moves)
        rec['wide_tokens']=sum('w' in t for t in moves)
        if not scramble or len(moves)<10:
            reject['missing_parse']+=1; rec['admission']='REJECT_PARSE'; audit.append(rec); continue
        sm=con.execute("""select round_type_id,group_id,is_extra,scramble_num from scrambles_333
                          where competition_id=? and scramble=?""",[r['competition_id'],scramble]).fetchall()
        rec['wca_scramble_matches']=[list(x) for x in sm]
        if len(sm)!=1:
            reject['scramble_not_unique']+=1; rec['admission']='REJECT_SCRAMBLE_NOT_UNIQUE'; audit.append(rec); continue
        # Keep exact round-type agreement as an additional provenance condition.
        if sm[0][0] != r['round_type_id']:
            reject['round_mismatch']+=1; rec['admission']='REJECT_ROUND_MISMATCH'; audit.append(rec); continue
        rec['admission']='ADMIT_EXACT_WCA_SCRAMBLE'; accepted.append(rec); audit.append(rec)
        if len(accepted)>=72: break
    except Exception as e:
        rec['error']=str(e)[:240]; rec['admission']='REJECT_FETCH'; reject['fetch_error']+=1; audit.append(rec)
    time.sleep(0.04)

out={'schema_version':'CR0105R17-STATE-SMOKE-INPUT-1','status':'PASS' if len(accepted)>=36 else 'HOLD',
     'parent_db_sha256':'a04f1d2fd351e34ec7406e63524b7b8ceb166bf8a53d4630f94c9d6a792848f1',
     'frozen_linked_frame_rows':len(frame),'attempted_detail_pages':len(audit),'accepted':len(accepted),
     'reject_counts':dict(reject),'accepted_records':accepted,'audit_records':audit,
     'admission_rule':'Unique A/B attempt linkage + exact unique WCA scramble text + WCA round-type agreement + parseable move stream.',
     'human_observations':0}
(OUT/'STATE_SMOKE_INPUT.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
if out['status']!='PASS': raise SystemExit(2)
print(json.dumps({'status':out['status'],'frame':len(frame),'attempted':len(audit),'accepted':len(accepted),'rejects':dict(reject)},indent=2))
