#!/usr/bin/env python3
"""Anytime counterexample search to overly broad one-step tie-break optimality on 5 edges.
A two-step policy beating one-step is a SOUND upper-bound counterexample even
without full AND-OR minimax. Does not claim two-step itself is optimal.
"""
from itertools import combinations,permutations,product
from functools import lru_cache
from pathlib import Path
from collections import Counter
import json,sys
TYPES=('UR','UF','UL','UB','DR','DF','DL','DB','FR','FL','BL','BR')
old=json.loads(Path(__file__).with_name('R14_P7_ALL_495_LOOKAHEAD_RESULTS.json').read_text())
T={frozenset(x['types']) for x in old['rows'] if x['greedy']>x['exact']}
sets=list(combinations(TYPES,5))
# Concentrate where the 4-edge old greedy obstruction occurs in a subset;
# no claim this is necessarily predictive of 5-edge obstructions.
sets.sort(key=lambda L:(-sum(frozenset(q) in T for q in combinations(L,4)),L))
cap=int(sys.argv[1]) if len(sys.argv)>1 else 60
rows=[]
for j,L in enumerate(sets[:cap]):
 n=5; words=[]
 for p in permutations(range(n)):
  if sum(p[i]>p[k] for i in range(n) for k in range(i+1,n))%2:continue
  for flips in product((0,1),repeat=n-1):
   o=flips+(sum(flips)%2,)
   words.append(''.join(L[p[i]][(k+o[i])%2] for i in range(n) for k in range(2)))
 assert len(words)==960
 masks=[{} for _ in range(2*n)]
 for ix,w in enumerate(words):
  for q,c in enumerate(w):masks[q][c]=masks[q].get(c,0)|(1<<ix)
 def kids(B,q):return [x for m in masks[q].values() if (x:=B&m)]
 @lru_cache(None)
 def V(B):
  if B.bit_count()==1:return 1
  return min(max(z.bit_count() for z in cs) for q in range(10) if len(cs:=kids(B,q))>1)
 @lru_cache(None)
 def depth(B,kind):
  if B.bit_count()==1:return 0
  arr=[]
  for q in range(10):
   cs=kids(B,q)
   if len(cs)<2:continue
   s=[c.bit_count() for c in cs]
   base=(max(s),len(cs),sum(x*x for x in s),q)
   key=(max(V(c) for c in cs),*base) if kind==1 else base
   arr.append((key,cs))
  chosen=min(arr,key=lambda a:a[0])[1]
  return 1+max(depth(c,kind) for c in chosen)
 full=(1<<960)-1
 few=depth(full,0); two=depth(full,1)
 rows.append({'types':L,'fewest_outcomes_one_step':few,'two_step_maxleaf':two,'difference':few-two,
              'contains_t_four_edge_subsets':sum(frozenset(q) in T for q in combinations(L,4))})
 if few>two:
  print('COUNTEREXAMPLE',L,'few',few,'two',two,'at',j+1,'/',cap,flush=True)
  break
 if (j+1)%10==0:print('checked',j+1,'of',cap,'depth',few,two,flush=True)
res={'result':'R14_P73_ANYTIME_FIVE_EDGE_TIEBREAK_SEARCH','attempted':len(rows),'requested_cap':cap,
     'found_one_step_beaten_by_two_step':any(r['difference']>0 for r in rows),
     'rows':rows,'scope':'Anytime deterministic 5-edge search. A found counterexample is sound; absence in subset is NOT a theorem over all 792 types.'}
Path(__file__).with_name('R14_P73_ANYTIME_FIVE_EDGE_SEARCH.json').write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')
print('RESULT',res['found_one_step_beaten_by_two_step'],'cases',len(rows),flush=True)
