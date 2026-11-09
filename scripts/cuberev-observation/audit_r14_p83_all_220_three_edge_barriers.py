#!/usr/bin/env python3
"""Exact conditional 3 residual edge cubies, both permutation parity strata, all 220 sets.
Sound application: after fully reading 9 edge positions with 18 reads, 2 final reads cannot recover the remaining triple for hard triples even with common parity revealed for free.
"""
from collections import Counter
from functools import lru_cache
from itertools import combinations, permutations, product
from pathlib import Path
import json
# Use independent physical color words from integer normals.
F={'U':(0,1,0),'D':(0,-1,0),'R':(1,0,0),'L':(-1,0,0),'F':(0,0,1),'B':(0,0,-1)}
S=tuple((p,F[f]) for p in product((-1,0,1),repeat=3) if sum(x!=0 for x in p) in (2,3) for f in 'URFDLB' if sum(x*y for x,y in zip(p,F[f]))==1)
ids={z:i for i,z in enumerate(S)};pieces={}
for p in sorted({p for p,n in S}):
 z=[ids[(p,n)] for n in F.values() if sum(x*y for x,y in zip(p,n))==1]
 if len(z)==2:z.sort(key=lambda i:0 if abs(S[i][1][1]) else 1 if abs(S[i][1][2]) else 2)
 else:continue
 pieces[p]=tuple(z)
words=tuple(''.join(next(f for f,n in F.items() if n==S[j][1]) for j in pieces[p]) for p in sorted(pieces))
assert len(words)==12

def sign(seq):return sum(seq[i]>seq[j] for i in range(len(seq)) for j in range(i+1,len(seq)))%2

def states(triple,par):
 ret=[]
 for p in permutations(range(3)):
  if sign(p)!=par:continue
  for a,b in product(range(2),repeat=2):
   o=(a,b,(a+b)%2)
   ret.append(''.join(triple[p[i]][(j+o[i])%2] for i in range(3) for j in range(2)))
 assert len(ret)==12 and len(set(ret))==12
 return tuple(ret)

def depth(X):
 n=len(X);outcome=[]
 for q in range(6):
  bins={}
  for i,state in enumerate(X):bins[state[q]]=bins.get(state[q],0)|(1<<i)
  outcome.append(tuple(bins.values()))
 whole=(1<<n)-1
 @lru_cache(None)
 def win(mask,budget):
  if mask.bit_count()<=1:return True
  if not budget or mask.bit_count()>6**budget:return False
  for p in outcome:
   c=[mask&z for z in p if mask&z]
   if len(c)>1 and all(win(z,budget-1) for z in c):return True
  return False
 return next(d for d in range(1,7) if win(whole,d)),win(whole,2)
rows=[]
for ids in combinations(range(12),3):
 triple=tuple(words[i] for i in ids)
 outcomes=[depth(states(triple,p)) for p in (0,1)]
 rows.append({'types':triple,'ids':ids,'exact_parity_depths':[v[0] for v in outcomes]})
print('counts parity0',Counter(r['exact_parity_depths'][0] for r in rows), 'parity1',Counter(r['exact_parity_depths'][1] for r in rows),flush=True)
print('joint',Counter(tuple(r['exact_parity_depths']) for r in rows),flush=True)
receipt={'result':'R14_P83_ALL_220_THREE_EDGE_KNOWN_PARITY_EXACT_PASS','all_source_triples':220,'states_per_known_parity':12,'parity0_depth_histogram':dict(Counter(str(r['exact_parity_depths'][0]) for r in rows)),'parity1_depth_histogram':dict(Counter(str(r['exact_parity_depths'][1]) for r in rows)),'triples_that_require_at_least_three_in_both_parities':sum(min(r['exact_parity_depths'])>=3 for r in rows),'triples_with_two_read_solution_in_any_parity':sum(min(r['exact_parity_depths'])<=2 for r in rows),'rows':rows,'implication':'A fixed 18-frame schedule completing 9 edge positions without visiting the other 3 cannot guarantee all states with only 2 further paired reads when remaining triple is one of the depth>=3 cases, even granting full common parity information and arbitrary corner readings. Not a no20 global theorem: other schedules interleave partial edges.'}
Path(__file__).with_name('R14_P83_ALL_220_THREE_EDGE_BARRIER_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print('PASS',receipt['result'])
