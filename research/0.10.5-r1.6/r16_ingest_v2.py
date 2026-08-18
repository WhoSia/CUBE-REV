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
# Exact schema repairs from sealed WCA v2.0.2 TSV headers (2026-08-18 vintage).
code=code.replace(', a.regional_single_record\n FROM {A}', '\n FROM {A}')
code=code.replace('c.country_iso2,', 'c.country_id,')
code=code.replace('p.country_iso2 FROM {P}', 'p.country_id FROM {P}')
# Reserved date aliases in DuckDB.
code=code.replace('cast(c.year as INTEGER) year,cast(c.month as INTEGER) month,cast(c.day as INTEGER) day',
                  'cast(c.year as INTEGER) comp_year,cast(c.month as INTEGER) comp_month,cast(c.day as INTEGER) comp_day')
code=code.replace('c.year,c.month,c.day,', 'c.comp_year,c.comp_month,c.comp_day,')
code=code.replace('select year,count(*)', 'select comp_year,count(*)')
code=code.replace('group by year order by year', 'group by comp_year order by comp_year')
code=code.replace('select year,count(*) filter(where shock_slow)', 'select comp_year,count(*) filter(where shock_slow)')
code=code.replace('SELECT year,attempt_status,count(*) n', 'SELECT comp_year,attempt_status,count(*) n')
code=code.replace('GROUP BY year,attempt_status ORDER BY year,attempt_status', 'GROUP BY comp_year,attempt_status ORDER BY comp_year,attempt_status')
# VALUE is reserved. Protect only the raw WCA result_attempts read; all later references target attempts_333.attempt_value.
code=code.replace('cast(a.value as INTEGER)', 'cast(a.__R16_SOURCE_VALUE__ as INTEGER)')
code=re.sub(r'\bvalue\b','attempt_value',code)
code=code.replace('a.__R16_SOURCE_VALUE__','a.value')
# Repair original two-CTE syntax.
code=code.replace('FROM attempt_spine s), z AS SELECT *,', 'FROM attempt_spine s), z AS (SELECT *,')
code=code.replace(' FROM b SELECT * FROM z', ' FROM b) SELECT * FROM z')
compile(code,str(Path(__file__).with_name('r16_ingest.py')),'exec')
exec(compile(code,str(Path(__file__).with_name('r16_ingest.py')),'exec'),{'__name__':'__main__','__file__':str(Path(__file__).with_name('r16_ingest.py'))})
