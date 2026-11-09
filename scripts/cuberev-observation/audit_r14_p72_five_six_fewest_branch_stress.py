#!/usr/bin/env python3
"""Direct exact replay of one-step fewest-branch tie-break on TWO fixed hard residual examples.
Not a proof over all C(12,5) or C(12,6) source-label families.
"""
from itertools import permutations,product
from collections import Counter
from functools import lru_cache
from pathlib import Path
import json
rows=[]
for L in [('UR','UF','UL','UB','FR'),('UR','UF','UL','UB','FR','FL')]:
 n=len(L);W=[]
 for p in permutations(range(n)):
  if sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))%2:continue
  for fs in product((0,1),repeat=n-1):
   o=fs+(sum(fs)%2,)
   W.append(''.join(L[p[i]][(j+o[i])%2] for i in range(n) for j in range(2)))
 mask=[{} for _ in range(2*n)]
 for ix,w in enumerate(W):
  for q,color in enumerate(w):mask[q][color]=mask[q].get(color,0)|(1<<ix)
 def children(B,q):return [c for m in mask[q].values() if (c:=B&m)]
 selected={}
 @lru_cache(None)
 def depth(B):
  if B.bit_count()==1:return 0
  options=[]
  for q in range(2*n):
   cs=children(B,q)
   if len(cs)<2:continue
   s=[v.bit_count() for v in cs]
   options.append(((max(s),len(cs),sum(v*v for v in s),q),cs))
  best=min(options,key=lambda x:x[0]);selected[B]=best[0][-1]
  return 1+max(depth(ch) for ch in best[1])
 full=(1<<len(W))-1;d=depth(full);replay=Counter()
 for ix,w in enumerate(W):
  B=full;count=0
  while B.bit_count()>1:
   q=selected[B]
   B &= mask[q][w[q]]
   count+=1
  assert B==1<<ix
  replay[count]+=1
 expected=7 if n==5 else 9
 rows.append({'types':L,'legal_states':len(W),'one_step_fewest_branches_worst_depth':d,'prior_exact_minimax_depth':expected,
              'regret':d-expected,'all_states_decoded':sum(replay.values()),'depth_hist':dict(replay)})
 print('R14-P7.2 stress',n,'depth',d,'oracle',expected,'beliefs',depth.cache_info().currsize,flush=True)
res={'result':'R14_P72_5_6_FEWEST_OUTCOME_ONE_STEP_STRESS_PASS','rows':rows,
     'scope':'Two hard examples only; prior exact minima imported from earlier R14 courts.'}
Path(__file__).with_name('R14_P72_5_6_FEWEST_BRANCH_STRESS.json').write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')
