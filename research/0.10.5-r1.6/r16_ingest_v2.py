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
# DuckDB 1.3 treats VALUE as a reserved keyword. Preserve the WCA source field a.value,
# but rename the analytical alias/references to attempt_value throughout generated SQL.
code=code.replace('a.value','a.__R16_SOURCE_VALUE__')
code=re.sub(r'\bvalue\b','attempt_value',code)
code=code.replace('a.__R16_SOURCE_VALUE__','a.value')
compile(code,str(Path(__file__).with_name('r16_ingest.py')),'exec')
exec(compile(code,str(Path(__file__).with_name('r16_ingest.py')),'exec'),{'__name__':'__main__','__file__':str(Path(__file__).with_name('r16_ingest.py'))})
