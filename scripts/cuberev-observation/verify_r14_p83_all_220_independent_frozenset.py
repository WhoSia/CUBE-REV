#!/usr/bin/env python3
"""No import of source/geometry: independent literal frozenset AND-OR three-edge classification."""
from itertools import combinations,permutations,product
from collections import Counter
from functools import lru_cache
from pathlib import Path
import json
EDGES=('UR','UF','UL','UB','DR','DF','DL','DB','FR','FL','BL','BR')

def sign(p):return sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))%2

def make(triple,par):
 return frozenset(''.join(triple[perm[i]][j^flip[i]] for i in range(3) for j in range(2)) for perm in permutations(range(3)) if sign(perm)==par for flip in ((0,0,0),(0,1,1),(1,0,1),(1,1,0)))

def exact_depth(X):
 @lru_cache(None)
 def rec(B):
  if len(B)<=1:return 0
  options=[]
  for q in range(6):
   children=[frozenset(s for s in B if s[q]==v) for v in set(s[q] for s in B)]
   if len(children)>1:options.append(1+max(rec(x) for x in children))
  return min(options)
 return rec(X)
rows=[]
for combo in combinations(EDGES,3):
 deg=Counter(''.join(combo))
 degrees=tuple(sorted(deg.values(),reverse=True))
 depths=tuple(exact_depth(make(combo,p)) for p in (0,1))
 rows.append((combo,degrees,depths))
hard=[combo for combo,deg,ds in rows if ds==(3,3)]
assert len(rows)==220 and len(hard)==32
assert all((ds==(3,3))==(deg in ((3,1,1,1),(2,2,2))) for combo,deg,ds in rows)
assert Counter(deg for _,deg,_ in rows)=={(3,1,1,1):24,(2,2,2):8,(2,2,1,1):84,(2,1,1,1,1):96,(1,1,1,1,1,1):8}
assert all(ds in ((2,2),(3,3)) for _,_,ds in rows)
output={'result':'R14_P83_INDEPENDENT_ALL_220_FROZENSET_STAR_TRIANGLE_IFF_PASS','triples':220,'known_even_parity_depths':dict(Counter(str(ds[0]) for _,_,ds in rows)),'known_odd_parity_depths':dict(Counter(str(ds[1]) for _,_,ds in rows)),'hard_triples':len(hard),'graph_criterion':'D=3 in both known-parity strata iff degree sequence (3,1,1,1) star or (2,2,2) triangle; otherwise D=2','structural_counts':{str(k):v for k,v in Counter(deg for _,deg,_ in rows).items()},'limitations':'Exact finite edge-only trios, not full 12E8C global 20-frame minimax.'}
Path(__file__).with_name('R14_P83_INDEPENDENT_ALL_220_RECEIPT.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(output,indent=2))
