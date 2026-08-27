#!/usr/bin/env python3
from pathlib import Path
import re

src=Path(__file__).with_name('r16_ingest.py').read_text(encoding='utf-8').splitlines()
reader_patched=False
version_patched=False
for i,line in enumerate(src):
    if line.strip().startswith('return f"read_csv('):
        src[i]="    return \"read_csv('\" + esc(p) + \"', delim='\\t', header=true, all_varchar=true, sample_size=-1, null_padding=true)\""
        reader_patched=True
    if "startswith('2.')" in line and "export_format_version" in line:
        src[i]=line.replace("str(metadata.get('export_format_version','')).startswith('2.')","str(metadata.get('export_format_version','')).lstrip('v').startswith('2.')")
        version_patched=True
if not reader_patched: raise RuntimeError('R16_READER_PATCH_ANCHOR_NOT_FOUND')
if not version_patched: raise RuntimeError('R16_VERSION_PATCH_ANCHOR_NOT_FOUND')
code='\n'.join(src)+'\n'

# Source-bound WCA v2.0.2 schema repairs from the sealed 2026-08-18 vintage.
code=code.replace(', a.regional_single_record\n FROM {A}', '\n FROM {A}')
code=code.replace('c.country_iso2,', 'c.country_id,')
code=code.replace('p.country_iso2 FROM {P}', 'p.country_id FROM {P}')
code=code.replace('cast(c.year as INTEGER) year,cast(c.month as INTEGER) month,cast(c.day as INTEGER) day',
                  'cast(c.year as INTEGER) comp_year,cast(c.month as INTEGER) comp_month,cast(c.day as INTEGER) comp_day')
code=code.replace('c.year,c.month,c.day,', 'c.comp_year,c.comp_month,c.comp_day,')
code=code.replace('select year,count(*)', 'select comp_year,count(*)')
code=code.replace('group by year order by year', 'group by comp_year order by comp_year')
code=code.replace('select year,count(*) filter(where shock_slow)', 'select comp_year,count(*) filter(where shock_slow)')
code=code.replace('SELECT year,attempt_status,count(*) n', 'SELECT comp_year,attempt_status,count(*) n')
code=code.replace('GROUP BY year,attempt_status ORDER BY year,attempt_status', 'GROUP BY comp_year,attempt_status ORDER BY comp_year,attempt_status')

# Normalize only distinct WCA names, then use native DuckDB equality joins across the 9M-attempt spine.
old_link="""con.create_function('r16_norm',norm,[str],str)
con.execute(\"\"\"CREATE TABLE linkage_candidates AS SELECT r.reco_id,r.result_text,r.method,r.movecount,r.tps,r.url,
 s.result_id,s.competition_id,s.person_id,s.attempt_number,s.value,
 (r.solver=s.person_name AND r.competition=s.competition_name) exact_text
 FROM reco_index r JOIN attempt_spine s ON cast(r.result_cs as INTEGER)=s.value
 AND r16_norm(r.solver)=r16_norm(s.person_name) AND r16_norm(r.competition)=r16_norm(s.competition_name)\"\"\")"""
new_link="""person_map_path=ROOT/'wca_person_norm.csv'
with open(person_map_path,'w',encoding='utf-8',newline='') as f:
    w=csv.writer(f); w.writerow(['person_name','solver_norm'])
    for (name,) in con.execute('select distinct person_name from attempt_spine').fetchall(): w.writerow([name,norm(name)])
competition_map_path=ROOT/'wca_competition_norm.csv'
with open(competition_map_path,'w',encoding='utf-8',newline='') as f:
    w=csv.writer(f); w.writerow(['competition_name','competition_norm'])
    for (name,) in con.execute('select distinct competition_name from attempt_spine').fetchall(): w.writerow([name,norm(name)])
con.execute(\"CREATE TABLE person_norm_map AS SELECT * FROM read_csv_auto(?,header=true,all_varchar=true)\",[str(person_map_path)])
con.execute(\"CREATE TABLE competition_norm_map AS SELECT * FROM read_csv_auto(?,header=true,all_varchar=true)\",[str(competition_map_path)])
con.execute('CREATE INDEX idx_person_norm ON person_norm_map(solver_norm)')
con.execute('CREATE INDEX idx_comp_norm ON competition_norm_map(competition_norm)')
con.execute(\"\"\"CREATE TABLE linkage_candidates AS SELECT r.reco_id,r.result_text,r.method,r.movecount,r.tps,r.url,
 s.result_id,s.competition_id,s.person_id,s.attempt_number,s.value,
 (r.solver=s.person_name AND r.competition=s.competition_name) exact_text
 FROM reco_index r
 JOIN person_norm_map pn ON r.solver_norm=pn.solver_norm
 JOIN competition_norm_map cn ON r.competition_norm=cn.competition_norm
 JOIN attempt_spine s ON s.person_name=pn.person_name AND s.competition_name=cn.competition_name
 AND cast(r.result_cs as INTEGER)=s.value\"\"\")"""
if old_link not in code: raise RuntimeError('R16_FINAL_LINKAGE_PATCH_ANCHOR_NOT_FOUND')
code=code.replace(old_link,new_link)

# reco.nz reports execution time in Result and carries +2 separately in Tags. Convert to the official WCA time.
old_result="'result_cs':cs_from_result(r['result_text']),'solver_norm':norm(r['solver']),'competition_norm':norm(r['competition'])"
new_result="'result_cs':(None if cs_from_result(r['result_text']) is None else cs_from_result(r['result_text']) + (200 if '[+2]' in str(r.get('tags','')) else 0)),'solver_norm':norm(r['solver']),'competition_norm':norm(r['competition'])"
if old_result not in code: raise RuntimeError('R16_PLUS2_PATCH_ANCHOR_NOT_FOUND')
code=code.replace(old_result,new_result)

# VALUE is reserved. Preserve only the raw WCA field name; analytical namespace is attempt_value.
code=code.replace('cast(a.value as INTEGER)', 'cast(a.__R16_SOURCE_VALUE__ as INTEGER)')
code=re.sub(r'\bvalue\b','attempt_value',code)
code=code.replace('a.__R16_SOURCE_VALUE__','a.value')

# Repair original phenotype two-CTE syntax.
code=code.replace('FROM attempt_spine s), z AS SELECT *,', 'FROM attempt_spine s), z AS (SELECT *,')
code=code.replace(' FROM b SELECT * FROM z', ' FROM b) SELECT * FROM z')

# Full public reco.nz index.
code=code.replace("sess.get('https://reco.nz/',timeout=45)","sess.get('https://reco.nz/solve/',timeout=45)")
code=code.replace("'retrieved_url':'https://reco.nz/'","'retrieved_url':'https://reco.nz/solve/'")

# Add explicit +2 and index-date diagnostic audits without using date as a hard linkage condition.
old_counter="link_counter=Counter(t for _,t in class_rows)\nlinked_attempts=int(one(con,\"\"\""
new_counter="""link_counter=Counter(t for _,t in class_rows)
reco_by_id={r['reco_id']:r for r in reco_rows}
plus2_rows=sum(1 for r in reco_rows if '[+2]' in str(r.get('tags','')))
date_year_audit={'unique_with_parseable_index_year':0,'index_year_matches_wca_competition_start_year':0,'index_year_mismatches_wca_competition_start_year':0}
for rid,tier in class_rows:
    if tier not in ('A_EXACT_UNIQUE','B_NORMALIZED_UNIQUE'): continue
    raw_date=str(reco_by_id.get(rid,{}).get('date',''))
    if not re.match(r'^\\d{4}-',raw_date): continue
    row=con.execute(\"\"\"select s.comp_year from linkage_candidates c join attempt_spine s on c.result_id=s.result_id and c.attempt_number=s.attempt_number where c.reco_id=? limit 1\"\"\",[rid]).fetchone()
    if not row: continue
    date_year_audit['unique_with_parseable_index_year']+=1
    if int(raw_date[:4])==int(row[0]): date_year_audit['index_year_matches_wca_competition_start_year']+=1
    else: date_year_audit['index_year_mismatches_wca_competition_start_year']+=1
linked_attempts=int(one(con(\"\"\""""
# The last line above intentionally needs syntactic restoration below; use a safer direct replacement instead.
if old_counter not in code: raise RuntimeError('R16_DATE_AUDIT_PATCH_ANCHOR_NOT_FOUND')
# Avoid constructing malformed function syntax in the replacement text.
replacement="link_counter=Counter(t for _,t in class_rows)\nreco_by_id={r['reco_id']:r for r in reco_rows}\nplus2_rows=sum(1 for r in reco_rows if '[+2]' in str(r.get('tags','')))\ndate_year_audit={'unique_with_parseable_index_year':0,'index_year_matches_wca_competition_start_year':0,'index_year_mismatches_wca_competition_start_year':0}\nfor rid,tier in class_rows:\n    if tier not in ('A_EXACT_UNIQUE','B_NORMALIZED_UNIQUE'): continue\n    raw_date=str(reco_by_id.get(rid,{}).get('date',''))\n    if not re.match(r'^\\d{4}-',raw_date): continue\n    row=con.execute(\"select s.comp_year from linkage_candidates c join attempt_spine s on c.result_id=s.result_id and c.attempt_number=s.attempt_number where c.reco_id=? limit 1\",[rid]).fetchone()\n    if not row: continue\n    date_year_audit['unique_with_parseable_index_year']+=1\n    if int(raw_date[:4])==int(row[0]): date_year_audit['index_year_matches_wca_competition_start_year']+=1\n    else: date_year_audit['index_year_mismatches_wca_competition_start_year']+=1\nlinked_attempts=int(one(con,\"\"\""
code=code.replace(old_counter,replacement)

old_linkage="'reco_3x3_rows':len(reco_rows),'tiers':dict(link_counter),'linked_distinct_wca_attempts':linked_attempts,'selection_by_time_bin':sel_bins,"
new_linkage="'reco_3x3_rows':len(reco_rows),'reco_plus2_rows':plus2_rows,'tiers':dict(link_counter),'linked_distinct_wca_attempts':linked_attempts,'selection_by_time_bin':sel_bins,'index_date_year_diagnostic':date_year_audit,"
if old_linkage not in code: raise RuntimeError('R16_AUDIT_OUTPUT_PATCH_ANCHOR_NOT_FOUND')
code=code.replace(old_linkage,new_linkage)

# Controlled local CSV output path.
old_copy="con.execute(\"COPY (SELECT comp_year,attempt_status,count(*) n FROM attempt_spine GROUP BY comp_year,attempt_status ORDER BY comp_year,attempt_status) TO ? (HEADER,DELIMITER ',')\",[str(OUT/'WCA_333_YEAR_STATUS_COUNTS.csv')])"
new_copy="csv_out=str(OUT/'WCA_333_YEAR_STATUS_COUNTS.csv').replace(\"'\",\"''\")\ncon.execute(\"COPY (SELECT comp_year,attempt_status,count(*) n FROM attempt_spine GROUP BY comp_year,attempt_status ORDER BY comp_year,attempt_status) TO '\"+csv_out+\"' (HEADER,DELIMITER ',')\")"
if old_copy not in code: raise RuntimeError('R16_FINAL_COPY_PATCH_ANCHOR_NOT_FOUND')
code=code.replace(old_copy,new_copy)

compile(code,str(Path(__file__).with_name('r16_ingest.py')),'exec')
exec(compile(code,str(Path(__file__).with_name('r16_ingest.py')),'exec'),{'__name__':'__main__','__file__':str(Path(__file__).with_name('r16_ingest.py'))})
