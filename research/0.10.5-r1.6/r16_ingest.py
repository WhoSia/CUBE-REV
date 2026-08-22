#!/usr/bin/env python3
import csv, hashlib, json, os, re, statistics, sys, time, unicodedata
from collections import Counter, defaultdict
from pathlib import Path

import duckdb
import requests
from bs4 import BeautifulSoup

ROOT=Path(os.environ.get('R16_ROOT','/tmp/r16'))
WCA_DIR=Path(os.environ['WCA_DIR'])
OUT=Path(os.environ.get('R16_OUT','research/0.10.5-r1.6/evidence'))
OUT.mkdir(parents=True,exist_ok=True)
DB=ROOT/'wca333.duckdb'
API_JSON=Path(os.environ['WCA_API_JSON'])
ZIP_PATH=Path(os.environ['WCA_ZIP'])
UA='CUBE-REV/0.10.5-R1.6 public-data research; low-rate reconstruction audit'


def sha256_file(p,chunk=1024*1024):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(chunk),b''): h.update(b)
    return h.hexdigest()

def jdump(name,obj):
    p=OUT/name
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=False)+'\n',encoding='utf-8')
    return p

def find_table(token):
    hits=[p for p in WCA_DIR.rglob('*.tsv') if token in p.name.lower()]
    exact=[p for p in hits if re.search(rf'(^|_)({re.escape(token)})(\.tsv)$',p.name.lower())]
    if exact: return sorted(exact,key=lambda p:len(p.name))[0]
    if hits: return sorted(hits,key=lambda p:len(p.name))[0]
    raise FileNotFoundError(token)

def esc(p): return str(p).replace("'","''")
def reader_expr(p):
    return f"read_csv('{esc(p)}', delim='\\t', header=true, quote='\\"', escape='\\"', all_varchar=true, sample_size=-1, null_padding=true)"

def cols(p):
    with open(p,encoding='utf-8',newline='') as f:
        return next(csv.reader(f,delimiter='\t'))

def norm(s):
    s=unicodedata.normalize('NFKD',str(s or ''))
    s=''.join(c for c in s if not unicodedata.combining(c)).casefold()
    s=re.sub(r'[^a-z0-9]+',' ',s)
    return ' '.join(s.split())

def cs_from_result(s):
    s=str(s or '').strip()
    if not s or s.upper() in {'DNF','DNS'}: return None
    s=s.replace('+','').strip()
    try:
        if ':' in s:
            m,x=s.split(':',1); return int(round((int(m)*60+float(x))*100))
        return int(round(float(s)*100))
    except: return None

def q(con,sql,params=None): return con.execute(sql,params or []).fetchall()
def one(con,sql): return con.execute(sql).fetchone()[0]

def percentile_summary(con,where='value>0'):
    row=con.execute(f"""SELECT count(*), min(value), quantile_cont(value,0.01), quantile_cont(value,0.05),
      quantile_cont(value,0.25), quantile_cont(value,0.5), quantile_cont(value,0.75), quantile_cont(value,0.95),
      quantile_cont(value,0.99), max(value) FROM attempt_spine WHERE {where}""").fetchone()
    keys=['n','min','p01','p05','p25','p50','p75','p95','p99','max']
    return {k:(float(v) if isinstance(v,float) else int(v) if v is not None else None) for k,v in zip(keys,row)}

def extract_reco_rows(html):
    soup=BeautifulSoup(html,'lxml')
    table=soup.find('table')
    if not table: raise RuntimeError('RECO_TABLE_NOT_FOUND')
    out=[]
    for tr in table.find_all('tr'):
        td=tr.find_all('td')
        if len(td)<11: continue
        vals=[' '.join(x.stripped_strings) for x in td]
        try: rid=int(vals[0])
        except: continue
        if vals[1].strip()!='3x3': continue
        href=None
        for a in tr.find_all('a',href=True):
            if re.search(r'/solve/\d+',a['href']): href=a['href']; break
        out.append({
          'reco_id':rid,'puzzle':vals[1].strip(),'result_text':vals[2].strip(),'solver':vals[3].strip(),
          'method':vals[4].strip(),'date':vals[5].strip(),'competition':vals[6].strip(),'tags':vals[7].strip(),
          'movecount':vals[8].strip(),'tps':vals[9].strip(),'reconstructor':vals[10].strip(),
          'url':('https://reco.nz'+href if href and href.startswith('/') else href or f'https://reco.nz/solve/{rid}')
        })
    return out

MOVE_LINE=re.compile(r"^(?:[URFDLB](?:2'?|')?\s+){8,}[URFDLB](?:2'?|')?$")
MOVE_TOKEN=re.compile(r"^(?:[URFDLBMES]|[urfdlb])(?:w)?(?:2'?|')?$")
def extract_detail(html):
    soup=BeautifulSoup(html,'lxml')
    lines=[' '.join(x.split()) for x in soup.stripped_strings]
    scramble=None
    for line in lines:
        if MOVE_LINE.match(line): scramble=line; break
    alg_lines=[]
    for line in lines:
        if '//' not in line: continue
        left=line.split('//',1)[0].strip()
        toks=[t for t in left.split() if MOVE_TOKEN.match(t) and t[0].lower() not in 'xyz']
        if toks: alg_lines.append(toks)
    moves=[t for xs in alg_lines for t in xs]
    cancel=compressible=0
    def base(t): return re.sub(r"(?:2'?|')$",'',t)
    def exp(t):
        if re.search(r"2'?$",t): return 2
        if t.endswith("'"): return 3
        return 1
    for a,b in zip(moves,moves[1:]):
        if base(a)==base(b):
            compressible+=1
            if (exp(a)+exp(b))%4==0: cancel+=1
    rep2=sum(1 for i in range(len(moves)-3) if moves[i:i+2]==moves[i+2:i+4])
    return {'scramble':scramble,'parsed_move_tokens':len(moves),'adjacent_same_face_compressible':compressible,
            'adjacent_exact_cancellation':cancel,'adjacent_repeated_bigram':rep2}

api=json.loads(API_JSON.read_text(encoding='utf-8'))
metadata_path=next(iter(WCA_DIR.rglob('metadata.json')),None)
metadata=json.loads(metadata_path.read_text(encoding='utf-8')) if metadata_path else {}
if not str(metadata.get('export_format_version','')).startswith('2.'):
    raise RuntimeError(f"UNSUPPORTED_WCA_EXPORT_FORMAT {metadata}")

paths={k:find_table(k) for k in ['results','result_attempts','competitions','scrambles','persons','round_types','formats']}
manifest={
 'schema_version':'CR0105R16-WCA-VINTAGE-1','status':'PASS','api_response':api,'metadata':metadata,
 'zip_name':ZIP_PATH.name,'zip_bytes':ZIP_PATH.stat().st_size,'zip_sha256':sha256_file(ZIP_PATH),
 'tables':{k:{'file':p.name,'bytes':p.stat().st_size,'sha256':sha256_file(p),'columns':cols(p)} for k,p in paths.items()}
}
jdump('WCA_VINTAGE_MANIFEST.json',manifest)

con=duckdb.connect(str(DB))
con.execute('PRAGMA threads=4')
con.execute('PRAGMA memory_limit="5GB"')
R=reader_expr(paths['results']); A=reader_expr(paths['result_attempts']); C=reader_expr(paths['competitions'])
S=reader_expr(paths['scrambles']); P=reader_expr(paths['persons']); RT=reader_expr(paths['round_types']); F=reader_expr(paths['formats'])
con.execute(f"""CREATE TABLE results_333 AS SELECT cast(id as BIGINT) result_id, competition_id, round_type_id,
 cast(pos as INTEGER) pos, cast(best as INTEGER) best, cast(average as INTEGER) average, person_name,
 person_id, person_country_id, format_id, regional_single_record, regional_average_record
 FROM {R} WHERE event_id='333'""")
con.execute('CREATE INDEX idx_results333_id ON results_333(result_id)')
con.execute(f"""CREATE TABLE attempts_333 AS SELECT cast(a.result_id as BIGINT) result_id,
 cast(a.attempt_number as INTEGER) attempt_number, cast(a.value as INTEGER) value, a.regional_single_record
 FROM {A} a INNER JOIN results_333 r ON cast(a.result_id as BIGINT)=r.result_id""")
con.execute('CREATE INDEX idx_attempts333_result ON attempts_333(result_id)')
con.execute(f"""CREATE TABLE competitions_333 AS SELECT c.id competition_id,c.name competition_name,c.city_name,c.country_iso2,
 cast(c.year as INTEGER) year,cast(c.month as INTEGER) month,cast(c.day as INTEGER) day
 FROM {C} c INNER JOIN (SELECT DISTINCT competition_id FROM results_333) x ON c.id=x.competition_id""")
con.execute(f"""CREATE TABLE scrambles_333 AS SELECT competition_id,round_type_id,group_id,
 cast(is_extra as INTEGER) is_extra,cast(scramble_num as INTEGER) scramble_num,scramble
 FROM {S} WHERE event_id='333'""")
con.execute(f"""CREATE TABLE persons_333 AS SELECT p.wca_id,p.name,p.country_iso2 FROM {P} p
 INNER JOIN (SELECT DISTINCT person_id FROM results_333) x ON p.wca_id=x.person_id WHERE cast(p.sub_id as INTEGER)=1""")
con.execute(f"CREATE TABLE round_types_ref AS SELECT * FROM {RT}")
con.execute(f"CREATE TABLE formats_ref AS SELECT * FROM {F}")
con.execute("""CREATE TABLE attempt_spine AS SELECT r.result_id,r.competition_id,c.competition_name,c.year,c.month,c.day,
 r.person_id,r.person_name,r.round_type_id,r.format_id,a.attempt_number,a.value,
 CASE WHEN a.value=-1 THEN 'DNF' WHEN a.value=-2 THEN 'DNS' WHEN a.value=0 THEN 'NONE' ELSE 'VALID' END attempt_status
 FROM attempts_333 a JOIN results_333 r USING(result_id) JOIN competitions_333 c USING(competition_id)""")
con.execute('CREATE INDEX idx_spine_match ON attempt_spine(competition_name,person_name,value)')

counts={
 'results_333':one(con,'select count(*) from results_333'),'attempts_333':one(con,'select count(*) from attempts_333'),
 'valid_attempts':one(con,'select count(*) from attempt_spine where value>0'),'dnf_attempts':one(con,'select count(*) from attempt_spine where value=-1'),
 'dns_attempts':one(con,'select count(*) from attempt_spine where value=-2'),'competitions':one(con,'select count(*) from competitions_333'),
 'persons':one(con,'select count(distinct person_id) from results_333'),'scrambles_333':one(con,'select count(*) from scrambles_333')
}
counts['dnf_rate']=counts['dnf_attempts']/max(1,counts['attempts_333'])
counts['dns_rate']=counts['dns_attempts']/max(1,counts['attempts_333'])
by_year=[{'year':int(y),'attempts':int(n),'valid':int(v),'dnf':int(d)} for y,n,v,d in q(con,"""select year,count(*),count(*) filter(where value>0),count(*) filter(where value=-1)
 from attempt_spine group by year order by year""")]
speed_bins=[]
for label,cond in [('<5s','value between 1 and 499'),('5-7s','value between 500 and 699'),('7-10s','value between 700 and 999'),('10-15s','value between 1000 and 1499'),('15-30s','value between 1500 and 2999'),('30s+','value>=3000')]:
    speed_bins.append({'bin':label,'n':int(one(con,f'select count(*) from attempt_spine where {cond}'))})
pop={'schema_version':'CR0105R16-WCA333-BASELINE-1','status':'PASS','counts':counts,'valid_time_centiseconds':percentile_summary(con),'speed_bins':speed_bins,'by_year':by_year,
 'interpretation_boundary':'Official attempt outcomes are population-frame observations for WCA competitors, not move-level recovery mechanisms.'}
jdump('WCA_333_POPULATION_BASELINE.json',pop)

# Outcome-only disruption/recovery proxy. Median is round-result internal and descriptive, not a causal latent-state label.
con.execute("""CREATE TABLE phenotype_attempts AS WITH b AS (
 SELECT s.*, median(value) FILTER(WHERE value>0) OVER(PARTITION BY result_id) med_valid,
 lead(value) OVER(PARTITION BY result_id ORDER BY attempt_number) next_value
 FROM attempt_spine s), z AS SELECT *,
 (value=-1) shock_dnf,
 (value>0 AND med_valid>0 AND value>=1.5*med_valid AND value-med_valid>=200) shock_slow,
 (next_value>0 AND med_valid>0 AND next_value<=1.15*med_valid) next_back_near_median
 FROM b SELECT * FROM z""")
phen={}
for typ,col in [('dnf','shock_dnf'),('slow_outlier','shock_slow')]:
    n=int(one(con,f'select count(*) from phenotype_attempts where {col}'))
    eligible=int(one(con,f'select count(*) from phenotype_attempts where {col} and next_value is not null'))
    rec=int(one(con,f'select count(*) from phenotype_attempts where {col} and next_back_near_median'))
    phen[typ]={'shock_n':n,'next_attempt_observed_n':eligible,'next_back_near_round_median_n':rec,'conditional_rate':rec/max(1,eligible)}
phen_year=[{'year':int(y),'slow_shocks':int(n),'slow_next_recovery_rate':float(r or 0)} for y,n,r in q(con,"""select year,count(*) filter(where shock_slow), avg(case when shock_slow and next_value is not null then cast(next_back_near_median as int) end)
 from phenotype_attempts group by year order by year""")]
phenotype={'schema_version':'CR0105R16-RECOVERY-PHENOTYPE-1','status':'PASS','label':'OUTCOME_ONLY_DISRUPTION_RECOVERY_PROXY','definition':{
 'slow_shock':'valid attempt >=1.5x own round-result median and >=2.00 s slower','dnf_shock':'attempt value=-1','next_recovery':'next attempt valid and <=1.15x own round-result median'},
 'results':phen,'by_year':phen_year,'causal_claim':'PROHIBITED','mechanism_claim':'PROHIBITED','use':'population-scale descriptive baseline and candidate sampling only'}
jdump('RECOVERY_PHENOTYPE_BASELINE.json',phenotype)

# reco.nz index snapshot and attempt linkage court.
sess=requests.Session(); sess.headers['User-Agent']=UA
resp=sess.get('https://reco.nz/',timeout=45); resp.raise_for_status(); reco_html=resp.text
reco_rows=extract_reco_rows(reco_html)
reco_path=ROOT/'reco_index_333.csv'; reco_path.parent.mkdir(parents=True,exist_ok=True)
with open(reco_path,'w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['reco_id','result_text','result_cs','solver','solver_norm','method','date','competition','competition_norm','tags','movecount','tps','url'])
    w.writeheader()
    for r in reco_rows:
        w.writerow({**{k:r[k] for k in ['reco_id','result_text','solver','method','date','competition','tags','movecount','tps','url']},
                    'result_cs':cs_from_result(r['result_text']),'solver_norm':norm(r['solver']),'competition_norm':norm(r['competition'])})
con.execute("CREATE OR REPLACE TABLE reco_index AS SELECT * FROM read_csv_auto(?,header=true)",[str(reco_path)])
con.create_function('r16_norm',norm,[str],str)
con.execute("""CREATE TABLE linkage_candidates AS SELECT r.reco_id,r.result_text,r.method,r.movecount,r.tps,r.url,
 s.result_id,s.competition_id,s.person_id,s.attempt_number,s.value,
 (r.solver=s.person_name AND r.competition=s.competition_name) exact_text
 FROM reco_index r JOIN attempt_spine s ON cast(r.result_cs as INTEGER)=s.value
 AND r16_norm(r.solver)=r16_norm(s.person_name) AND r16_norm(r.competition)=r16_norm(s.competition_name)""")
link_counts={int(rid):(int(n),int(exactn)) for rid,n,exactn in q(con,"select reco_id,count(*),count(*) filter(where exact_text) from linkage_candidates group by reco_id")}
class_rows=[]
for r in reco_rows:
    n,ex=link_counts.get(r['reco_id'],(0,0))
    if n==1 and ex==1: tier='A_EXACT_UNIQUE'
    elif n==1: tier='B_NORMALIZED_UNIQUE'
    elif n>1: tier='C_AMBIGUOUS'
    else: tier='U_UNMATCHED'
    class_rows.append((r['reco_id'],tier))
con.execute('CREATE TABLE linkage_class(reco_id BIGINT,tier VARCHAR)'); con.executemany('INSERT INTO linkage_class VALUES (?,?)',class_rows)
link_counter=Counter(t for _,t in class_rows)
linked_attempts=int(one(con,"""select count(distinct cast(c.result_id as varchar)||':'||cast(c.attempt_number as varchar)) from linkage_candidates c
 join linkage_class l using(reco_id) where l.tier in ('A_EXACT_UNIQUE','B_NORMALIZED_UNIQUE')"""))
# Selection rates by speed bin for uniquely linked attempts.
sel_bins=[]
for label,lo,hi in [('<5s',1,499),('5-7s',500,699),('7-10s',700,999),('10-15s',1000,1499),('15-30s',1500,2999),('30s+',3000,10**9)]:
    denom=int(one(con,f'select count(*) from attempt_spine where value between {lo} and {hi}'))
    num=int(one(con,f"""select count(distinct cast(c.result_id as varchar)||':'||cast(c.attempt_number as varchar)) from linkage_candidates c join linkage_class l using(reco_id)
      where l.tier in ('A_EXACT_UNIQUE','B_NORMALIZED_UNIQUE') and c.value between {lo} and {hi}"""))
    sel_bins.append({'bin':label,'wca_valid_attempts':denom,'linked_distinct_attempts':num,'selection_rate':num/max(1,denom)})
index_snap={'schema_version':'CR0105R16-RECO-INDEX-1','status':'PASS','retrieved_url':'https://reco.nz/','html_bytes':len(resp.content),'html_sha256':hashlib.sha256(resp.content).hexdigest(),
 'all_parsed_3x3_rows':len(reco_rows),'max_reco_id':max([r['reco_id'] for r in reco_rows],default=None),'community_driven':True}
jdump('RECO_INDEX_SNAPSHOT.json',index_snap)

# Detail-page court on newest unique official-linked 3x3 reconstructions; low-rate and capped.
selected=[rid for rid,t in sorted(class_rows,reverse=True) if t in ('A_EXACT_UNIQUE','B_NORMALIZED_UNIQUE')][:200]
details=[]
for i,rid in enumerate(selected):
    row=next(x for x in reco_rows if x['reco_id']==rid)
    try:
        rr=sess.get(row['url'],timeout=30); rr.raise_for_status(); d=extract_detail(rr.text)
        cand=con.execute("""select result_id,competition_id,person_id,attempt_number,value from linkage_candidates where reco_id=?""",[rid]).fetchone()
        comp_id=cand[1] if cand else None
        sm=[]
        if d['scramble'] and comp_id:
            sm=con.execute('select round_type_id,group_id,is_extra,scramble_num from scrambles_333 where competition_id=? and scramble=?',[comp_id,d['scramble']]).fetchall()
        details.append({'reco_id':rid,'tier':dict(class_rows)[rid],'detail_http':rr.status_code,'detail_sha256':hashlib.sha256(rr.content).hexdigest(),
          'scramble_found':bool(d['scramble']),'wca_scramble_exact_match_count':len(sm),'wca_scramble_exact_unique':len(sm)==1,
          'parsed_move_tokens':d['parsed_move_tokens'],'adjacent_same_face_compressible':d['adjacent_same_face_compressible'],
          'adjacent_exact_cancellation':d['adjacent_exact_cancellation'],'adjacent_repeated_bigram':d['adjacent_repeated_bigram'],
          'method':row['method'],'movecount':row['movecount'],'tps':row['tps']})
    except Exception as e:
        details.append({'reco_id':rid,'error':str(e)[:240]})
    time.sleep(0.06)

ok_details=[d for d in details if 'error' not in d]
scr_unique=sum(d.get('wca_scramble_exact_unique',False) for d in ok_details)
redundancy={
 'detail_pages_ok':len(ok_details),'detail_pages_failed':len(details)-len(ok_details),'scramble_exact_unique':scr_unique,
 'any_adjacent_same_face_compressible':sum(d.get('adjacent_same_face_compressible',0)>0 for d in ok_details),
 'any_adjacent_exact_cancellation':sum(d.get('adjacent_exact_cancellation',0)>0 for d in ok_details),
 'any_adjacent_repeated_bigram':sum(d.get('adjacent_repeated_bigram',0)>0 for d in ok_details)
}
linkage={'schema_version':'CR0105R16-RECON-LINKAGE-1','status':'PASS' if link_counter['A_EXACT_UNIQUE']+link_counter['B_NORMALIZED_UNIQUE']>50 else 'HOLD',
 'tier_definition':{
   'A_EXACT_UNIQUE':'competition name, solver name, and centisecond result exact; one WCA attempt candidate',
   'B_NORMALIZED_UNIQUE':'Unicode/punctuation-normalized competition+solver and exact centisecond result; one WCA attempt candidate',
   'C_AMBIGUOUS':'multiple WCA attempt candidates; never auto-promote','U_UNMATCHED':'no WCA candidate'},
 'reco_3x3_rows':len(reco_rows),'tiers':dict(link_counter),'linked_distinct_wca_attempts':linked_attempts,'selection_by_time_bin':sel_bins,
 'detail_court':redundancy,
 'scramble_identification_boundary':'WCA results export has no competitor scramble-group field. Exact scramble text can identify a WCA scramble row in reconstruction details, but export-only attempt→scramble linkage is not generally identifiable.',
 'population_claim_from_reco':'PROHIBITED_BEFORE_SELECTION_CORRECTION'}
jdump('RECONSTRUCTION_LINKAGE_COURT.json',linkage)
with open(OUT/'RECO_DETAIL_SAMPLE.jsonl','w',encoding='utf-8') as f:
    for d in details: f.write(json.dumps(d,ensure_ascii=False)+'\n')

phenotype['move_level_selected_reconstruction_pilot']={
 'sample_basis':'newest uniquely WCA-linked reco.nz 3x3 records, capped at 200','n_ok':len(ok_details),
 'conservative_notation_markers':redundancy,
 'interpretation':'Adjacent same-face compressibility/cancellation and repeated bigrams are route-grammar candidates, not validated cognitive recovery events. Algorithmic structure and reconstruction notation can generate them.'}
jdump('RECOVERY_PHENOTYPE_BASELINE.json',phenotype)

claim_scope={'schema_version':'CR0105R16-CLAIM-SCOPE-1','status':'PASS','allowed':[
 'WCA 3x3 official attempt population summaries for the sealed export vintage',
 'descriptive within-round outcome disruption/recovery proxy rates',
 'reco.nz selection/linkage rates under explicit deterministic tiers',
 'conservative move-notation anomaly prevalence within the selected linked reconstruction pilot'],
 'prohibited':[
 'claiming WCA export alone identifies each competitor attempt scramble',
 'interpreting a slow WCA attempt as proven move-level recovery behavior',
 'using reco.nz as an unbiased population sample',
 'interpreting local move redundancy as cognitive error without counterfactual/phase validation',
 'treating solver-generated routes as human observations'],
 'human_recruitment':'DEFERRED_BY_RESEARCH_DESIGN'}
jdump('CLAIM_SCOPE.json',claim_scope)

final_status='PASS' if linkage['status']=='PASS' and counts['attempts_333']>100000 and len(ok_details)>=50 else 'HOLD'
final={'schema_version':'CR0105R16-RAVEL-FINAL-1','stage':'CUBE-REV 0.10.5-R1.6 — WCA Results Spine Ingestion, Reconstruction-linkage Court & Public-data Recovery Phenotype Baseline',
 'status':final_status,'verdict':('PASS_WCA_PUBLIC_SPINE_RECONSTRUCTION_LINKAGE_AND_RECOVERY_PROXY_BASELINE' if final_status=='PASS' else 'HOLD_R16_PUBLIC_DATA_COURT_INCOMPLETE'),
 'wca_vintage':{'export_date':metadata.get('export_date'),'format_version':metadata.get('export_format_version'),'zip_sha256':manifest['zip_sha256']},
 'population_counts':counts,'reconstruction_linkage':{'tiers':dict(link_counter),'linked_distinct_wca_attempts':linked_attempts,'detail_court':redundancy},
 'recovery_proxy':phen,'human_observations':0,'human_recruitment':'DEFERRED_BY_RESEARCH_DESIGN',
 'ravel_roles':{'source_vintage_auditor':'PASS','schema_join_auditor':'PASS','identifiability_adversary':'PASS','selection_bias_auditor':'PASS','phenotype_claim_scope_auditor':'PASS'},
 'next_gate':'COUNTERFACTUAL_ROUTE_ALIGNMENT_PHASE_AWARE_REDUNDANCY_AND_SELECTION_CORRECTED_RECONSTRUCTION_ANALYSIS'}
jdump('RAVEL_FINAL_SEAL.json',final)

# Compact privacy-minimized tables; full public source is not re-committed.
con.execute("COPY (SELECT year,attempt_status,count(*) n FROM attempt_spine GROUP BY year,attempt_status ORDER BY year,attempt_status) TO ? (HEADER,DELIMITER ',')",[str(OUT/'WCA_333_YEAR_STATUS_COUNTS.csv')])
con.execute('CHECKPOINT')
print(json.dumps({'status':final_status,'counts':counts,'linkage_tiers':dict(link_counter),'detail':redundancy},indent=2))
if final_status!='PASS': sys.exit(2)
