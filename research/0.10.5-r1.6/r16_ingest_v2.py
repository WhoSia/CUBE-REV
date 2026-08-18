#!/usr/bin/env python3
from pathlib import Path
src=Path(__file__).with_name('r16_ingest.py').read_text(encoding='utf-8').splitlines()
patched=False
for i,line in enumerate(src):
    if line.strip().startswith('return f"read_csv('):
        src[i]="    return \"read_csv('\" + esc(p) + \"', delim='\\t', header=true, all_varchar=true, sample_size=-1, null_padding=true)\""
        patched=True
        break
if not patched:
    raise RuntimeError('R16_READER_PATCH_ANCHOR_NOT_FOUND')
code='\n'.join(src)+'\n'
compile(code,str(Path(__file__).with_name('r16_ingest.py')),'exec')
exec(compile(code,str(Path(__file__).with_name('r16_ingest.py')),'exec'),{'__name__':'__main__','__file__':str(Path(__file__).with_name('r16_ingest.py'))})
