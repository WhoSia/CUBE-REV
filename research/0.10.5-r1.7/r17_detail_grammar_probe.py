#!/usr/bin/env python3
import hashlib,json,os,re,time
from collections import Counter,defaultdict
from pathlib import Path
import duckdb,requests
from bs4 import BeautifulSoup

DB=Path(os.environ['R17_PARENT_DB'])
OUT=Path(os.environ.get('R17_OUT','research/0.10.5-r1.7/evidence-grammar'))
OUT.mkdir(parents=True,exist_ok=True)
UA='CUBE-REV/0.10.5-R1.7 reconstruction grammar probe; low-rate public research audit'
MOVE_RE=re.compile(r"^(?:[URFDLBMESxyz]|[urfdlb])(?:w)?(?:2'?|')?$",re.I)
SCRAMBLE_RE=re.compile(r"^(?:(?:[URFDLB](?:w)?|[urfdlb])(?:2'?|')?\s+){8,}(?:[URFDLB](?:w)?|[urfdlb])(?:2'?|')?$",re.I)

def speed_bin(v):
    if v<500:return '<5s'
    if v<700:return '5-7s'
    if v<1000:return '7-10s'
    if v<1500:return '10-15s'
    if v<3000:return '15-30s'
    return '30s+'

def clean_comment(s):
    s=' '.join(str(s).split()).strip().lower()
    s=re.sub(r'https?://\S+','URL',s)
    return s[:160]

def parse_detail(html):
    soup=BeautifulSoup(html,'lxml')
    strings=[' '.join(x.split()) for x in soup.stripped_strings]
    scramble=next((x for x in strings if SCRAMBLE_RE.match(x)),None)
    lines=[]
    all_moves=[]
    for raw in strings:
        if '//' not in raw: continue
        left,comment=raw.split('//',1)
        toks=[]; rejected=[]
        for tok in left.strip().split():
            if MOVE_RE.match(tok): toks.append(tok)
            elif re.search(r'[A-Za-z]',tok): rejected.append(tok)
        if toks:
            lines.append({'moves':toks,'comment':clean_comment(comment),'rejected_tokens':rejected[:8]})
            all_moves.extend(toks)
    return {'scramble':scramble,'lines':lines,'moves':all_moves}

con=duckdb.connect(str(DB),read_only=True)
linked=con.execute("""
select r.reco_id,r.method,r.url,c.attempt_value,c.result_id,c.attempt_number,c.competition_id,
       s.comp_year,s.person_id,s.person_name
from reco_index r join linkage_class l using(reco_id)
join linkage_candidates c using(reco_id)
join attempt_spine s on s.result_id=c.result_id and s.attempt_number=c.attempt_number
where l.tier in ('A_EXACT_UNIQUE','B_NORMALIZED_UNIQUE')
qualify count(*) over(partition by r.reco_id)=1
order by r.reco_id desc
""").fetchall()
cols=['reco_id','method','url','attempt_value','result_id','attempt_number','competition_id','comp_year','person_id','person_name']
rows=[dict(zip(cols,x)) for x in linked]
method_counts=Counter((r['method'] or 'UNKNOWN') for r in rows)
speed_counts=Counter(speed_bin(r['attempt_value']) for r in rows)
# Deterministic stratified probe: at most 12 per method x speed cell, newest-first, max 144.
selected=[]; cell=Counter()
for r in rows:
    key=(r['method'] or 'UNKNOWN',speed_bin(r['attempt_value']))
    if cell[key]>=12: continue
    selected.append(r); cell[key]+=1
    if len(selected)>=144: break

sess=requests.Session(); sess.headers['User-Agent']=UA
comment_counter=Counter(); phase_terms=Counter(); method_probe=Counter(); token_class=Counter(); records=[]
phase_patterns={
 'CROSS':re.compile(r'\b(?:x?cross)\b',re.I),
 'F2L':re.compile(r'\b(?:f2l|[1-4](?:st|nd|rd|th)?\s*pair|first\s*pair|second\s*pair|third\s*pair|fourth\s*pair)\b',re.I),
 'OLL':re.compile(r'\b(?:oll|eoll|coll)\b',re.I),
 'PLL':re.compile(r'\b(?:pll|zbll|auf)\b',re.I),
 'ROUX':re.compile(r'\b(?:first\s*block|second\s*block|cmll|lse)\b',re.I),
 'ZZ':re.compile(r'\b(?:eo(?:line|cross)?|zz)\b',re.I),
}
for i,r in enumerate(selected):
    rec={k:r[k] for k in cols}; rec['speed_bin']=speed_bin(r['attempt_value'])
    try:
        resp=sess.get(r['url'],timeout=30); resp.raise_for_status(); p=parse_detail(resp.text)
        rec.update({'http':resp.status_code,'html_sha256':hashlib.sha256(resp.content).hexdigest(),
                    'scramble_found':bool(p['scramble']),'line_count':len(p['lines']),'move_count':len(p['moves']),
                    'rotation_tokens':sum(t[0].lower() in 'xyz' for t in p['moves']),
                    'slice_tokens':sum(t[0].upper() in 'MES' for t in p['moves']),
                    'wide_tokens':sum(('w' in t.lower()) or (t and t[0].islower() and t[0].lower() in 'urfdlb') for t in p['moves']),
                    'comments':[x['comment'] for x in p['lines'] if x['comment']][:24]})
        for t in p['moves']:
            if t[0].lower() in 'xyz': token_class['rotation']+=1
            elif t[0].upper() in 'MES': token_class['slice']+=1
            elif 'w' in t.lower() or t[0].islower(): token_class['wide']+=1
            else: token_class['face']+=1
        for ln in p['lines']:
            c=ln['comment']
            if c:
                comment_counter[c]+=1
                for name,pat in phase_patterns.items():
                    if pat.search(c): phase_terms[name]+=1
        method_probe[r['method'] or 'UNKNOWN']+=1
    except Exception as e:
        rec['error']=str(e)[:220]
    records.append(rec)
    time.sleep(0.05)

ok=[r for r in records if 'error' not in r]
out={
 'schema_version':'CR0105R17-DETAIL-GRAMMAR-PROBE-1','status':'PASS' if len(ok)>=80 else 'HOLD',
 'parent_db_sha256':'a04f1d2fd351e34ec7406e63524b7b8ceb166bf8a53d4630f94c9d6a792848f1',
 'linked_unique_frame_rows':len(rows),'method_distribution':dict(method_counts),'speed_distribution':dict(speed_counts),
 'probe_selected':len(selected),'probe_ok':len(ok),'probe_failed':len(records)-len(ok),
 'probe_method_distribution':dict(method_probe),'move_token_classes':dict(token_class),
 'records_with_scramble':sum(bool(r.get('scramble_found')) for r in ok),
 'records_with_rotation':sum(r.get('rotation_tokens',0)>0 for r in ok),
 'records_with_slice':sum(r.get('slice_tokens',0)>0 for r in ok),
 'records_with_wide':sum(r.get('wide_tokens',0)>0 for r in ok),
 'phase_comment_hits':dict(phase_terms),'top_comments':comment_counter.most_common(80),
 'records':records,
 'interpretation_boundary':'Comments are reconstruction annotations, not independently validated cognitive phase labels. State replay must independently verify any promoted phase phenotype.',
 'human_observations':0
}
(OUT/'DETAIL_GRAMMAR_PROBE.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
if out['status']!='PASS': raise SystemExit(2)
print(json.dumps({k:out[k] for k in ['status','linked_unique_frame_rows','probe_ok','records_with_rotation','records_with_slice','records_with_wide','phase_comment_hits']},indent=2))
