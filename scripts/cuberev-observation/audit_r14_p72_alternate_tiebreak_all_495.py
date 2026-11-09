#!/usr/bin/env python3
"""Full all-495 falsification of 'two-step is necessary': two different one-step tie-breaks.
Exact optimum is read from independently verified P7.1 full 495-row receipt.
"""
from itertools import permutations,product
from functools import lru_cache
from collections import Counter
from pathlib import Path
import json
here=Path(__file__).resolve().parent
prior=json.loads((here/'R14_P7_ALL_495_LOOKAHEAD_RESULTS.json').read_text())
rows=[]
for ix,row in enumerate(prior['rows']):
 L=row['types'];words=[]
 for p in permutations(range(4)):
  if sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))%2:continue
  for fs in product((0,1),repeat=3):
   o=fs+(sum(fs)%2,)
   words.append(''.join(L[p[i]][(j+o[i])%2] for i in range(4) for j in range(2)))
 masks=[{} for _ in range(8)]
 for i,w in enumerate(words):
  for q,c in enumerate(w):masks[q][c]=masks[q].get(c,0)|(1<<i)
 def children(B,q):return [z for mask in masks[q].values() if (z:=B&mask)]
 @lru_cache(None)
 def policy(B,variant):
  if B.bit_count()==1:return 0
  actions=[]
  for q in range(8):
   kids=children(B,q)
   if len(kids)<2:continue
   counts=[v.bit_count() for v in kids]
   if variant==0: key=(max(counts),len(kids),sum(v*v for v in counts),q) # few first
   else:key=(max(counts),-len(kids),sum(v*v for v in counts),q) # many first
   actions.append((key,kids))
  return 1+max(policy(c,variant) for c in min(actions,key=lambda a:a[0])[1])
 whole=(1<<96)-1
 few,many=policy(whole,0),policy(whole,1)
 rows.append({'types':L,'exact':row['exact'],'original_greedy':row['greedy'],'few':few,'many':many})
 if (ix+1)%100==0:print('checked',ix+1,flush=True)
countfew=Counter(x['few']-x['exact'] for x in rows)
countmany=Counter(x['many']-x['exact'] for x in rows)
result={'result':'R14_P72_ALL_495_ONE_STEP_TIEBREAK_FALSIFICATION_PASS',
 'all_sets':len(rows),'min_worst_then_fewest_color_outcomes_regret':dict(countfew),
 'min_worst_then_most_color_outcomes_regret':dict(countmany),
 'few_policy_minimax_hist':dict(Counter(x['few'] for x in rows)),
 'many_policy_minimax_hist':dict(Counter(x['many'] for x in rows)),
 'few_policy_counterexample':next((x for x in rows if x['few']>x['exact']),None),
 'many_policy_counterexample':next((x for x in rows if x['many']>x['exact']),None),
 'rows':rows,
 'scope':'Fixed known-parity four-edge family, exact root optimum from P7.1. One-step maximum child minimization followed by number of distinct output colors tie-break. Not a global theoretical guarantee.'}
(here/'R14_P72_ALL_495_TIEBREAK_RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))
