#!/usr/bin/env python3
"""Research question: With fixed 9E/5C fully observed suffix, can additional corner-only observations fit inside 18-frame 9E scan, leaving 2 paired reads?"""
from pathlib import Path
import importlib.util,contextlib,io,sys,json
from functools import lru_cache
from collections import Counter
src=Path(__file__).with_name('audit_r14_p83_physical_648_exact_andor.py')
with contextlib.redirect_stdout(io.StringIO()):
 spec=importlib.util.spec_from_file_location('p83_suffix_solver',src)
 mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
S=mod.states;whole=mod.whole
corner_queries=range(15,24)
cells={q:{} for q in corner_queries}
for q in corner_queries:
 for i,(e,c) in enumerate(S):
  y=c[q];cells[q][y]=cells[q].get(y,0)|(1<<i)
@lru_cache(None)
def can(mask,free_c,paired):
 if mask.bit_count()==1:return True
 if not free_c:return mod.win(mask,paired)
 for q in corner_queries:
  children=[mask&bits for bits in cells[q].values() if mask&bits]
  if len(children)>1 and all(can(z,free_c-1,paired) for z in children):return True
 return False
results={}
for n in range(5):
 v=can(whole,n,2);results[str(n)]=v
 print('corner_free',n,'pair_final2',v,'cache',can.cache_info().currsize,flush=True)
 if v:break
receipt={'result':'R14_P83_CORNER_ONLY_TO_PAIRED_HORIZON_COURT','conditional_full_prefix':'9E5C full observations first, 648 physically valid parity-matched states','remaining_edge_single_facelet_queries':6,'remaining_corner_single_facelet_queries':9,'goal_pair_reads':2,'extra_corner_only_query_budget_results':results,'cache_entries':can.cache_info().currsize,'limitations':'Conditional 9E5C prefix and free corner-only queries, not a full cube 20-frame strategy. If 3 queries necessary/sufficient, full 18-frame prefix scheduling and all source label cases still need proof.'}
Path(__file__).with_name('R14_P83_CORNER_ONLY_TIME_TRADEOFF_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(receipt)
