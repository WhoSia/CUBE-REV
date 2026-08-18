#!/usr/bin/env python3
from pathlib import Path
import re
p=Path(__file__).with_name('r16_ingest_ravel_final.py')
text=p.read_text(encoding='utf-8')
pattern=r'\nnew_counter=""".*?"""\n# The last line above intentionally needs syntactic restoration below; use a safer direct replacement instead\.\n'
clean,n=re.subn(pattern,'\n',text,flags=re.S)
if n!=1:
    raise RuntimeError(f'R16_FINAL_WRAPPER_CLEAN_ANCHOR_COUNT={n}')
compile(clean,str(p),'exec')
exec(compile(clean,str(p),'exec'),{'__name__':'__main__','__file__':str(p)})
