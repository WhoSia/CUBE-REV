#!/usr/bin/env python3
"""Independent direct-frozenset exact AND-OR for ALL 24 color-graph orbits
of the 792 five-edge known parity residual games. Verifies the original 792
finite receipt by a structurally separate representation without importing code.
"""
from itertools import permutations,product,combinations
from functools import lru_cache
from collections import Counter,defaultdict
from pathlib import Path
import json,time
here=Path(__file__).resolve().parent
source=json.loads((here/'R14_P73_ALL_792_EXACT_MINIMAX_RECEIPT.json').read_text())
assert source['all_five_edge_sets']==792
T=('UR','UF','UL','UB','DR','DF','DL','DB','FR','FL','BL','BR')
PAIRS=(('U','D'),('R','L'),('F','B'))
edge={frozenset(e):e for e in T}
automorphisms=[]
for p in permutations(range(3)):
 for f in product((0,1),repeat=3):
  move={}
  for i,(a,b) in enumerate(PAIRS):
   tgt=PAIRS[p[i]]
   move[a]=tgt[f[i]]
   move[b]=tgt[1-f[i]]
  automorphisms.append({e:edge[frozenset(move[c] for c in e)] for e in T})
assert len(automorphisms)==48

def rep(L):return min(tuple(sorted(m[e] for e in L)) for m in automorphisms)
classes=defaultdict(list)
for row in source['rows']:
 classes[rep(row['types'])].append(row)
assert len(classes)==24 and sum(map(len,classes.values()))==792
rows=[];t0=time.monotonic()
for nr,(L,group) in enumerate(sorted(classes.items()),1):
 depths={row['exact_minimax'] for row in group}
 assert len(depths)==1,(L,depths)
 expected=next(iter(depths))
 assert all(row['one_step_fewest_outcomes']==expected and row['two_step_maxleaf']==expected for row in group)
 # Independent enumeration of the 960 parity-even/flip-even state words
 words=[]
 for p in permutations(range(5)):
  if sum(p[i]>p[j] for i in range(5) for j in range(i+1,5))%2:continue
  for z in product((0,1),repeat=4):
   f=z+(sum(z)%2,)
   words.append(''.join(L[p[i]][(s+f[i])%2] for i in range(5) for s in range(2)))
 assert len(words)==960 and len(set(words))==960
 @lru_cache(None)
 def split(B,q):
  d={}
  for ix in B:d.setdefault(words[ix][q],[]).append(ix)
  return tuple(frozenset(indices) for indices in d.values())
 @lru_cache(None)
 def can(B,k):
  if len(B)==1:return True
  if k==0 or len(B)>6**k:return False
  options=[]
  for q in range(10):
   cs=split(B,q)
   if len(cs)<2 or max(map(len,cs))>6**(k-1):continue
   nums=[len(ch) for ch in cs]
   options.append(((max(nums),len(cs),sum(s*s for s in nums),q),cs))
  for _,cs in sorted(options,key=lambda p:p[0]):
   if all(can(ch,k-1) for ch in sorted(cs,key=len,reverse=True)):return True
  return False
 full=frozenset(range(960))
 assert not can(full,expected-1),('shorter than producer',L)
 selected={}
 @lru_cache(None)
 def policy_depth(B):
  if len(B)==1:return 0
  opts=[]
  for q in range(10):
   cs=split(B,q)
   if len(cs)<2:continue
   sizes=[len(c) for c in cs]
   opts.append(((max(sizes),len(cs),sum(x*x for x in sizes),q),q,cs))
  _,query,cs=min(opts,key=lambda z:z[0]);selected[B]=query
  return 1+max(policy_depth(c) for c in cs)
 assert policy_depth(full)==expected
 for ix in range(960):
  B=full;steps=0
  while len(B)>1:
   q=selected[B]
   B=next(child for child in split(B,q) if ix in child)
   steps+=1
  assert B==frozenset([ix]) and steps<=expected
 rows.append({'representative':L,'graph_orbit_size':len(group),'exact_minimax':expected,
              'independent_lower_unsatisfiable':True,'independent_960_state_policy_replays':960,
              'AND_OR_cache_size':can.cache_info().currsize,'policy_cache_size':policy_depth.cache_info().currsize})
 if nr%4==0:print('independently verified',nr,'of 24 orbit representatives','seconds',round(time.monotonic()-t0,1),flush=True)
assert sum(r['graph_orbit_size'] for r in rows)==792
assert Counter({d:sum(r['graph_orbit_size'] for r in rows if r['exact_minimax']==d) for d in (5,6,7)})==Counter({5:12,6:672,7:108})
receipt={'result':'R14_P73_INDEPENDENT_ALL_24_COLOR_GRAPH_ORBITS_EXACT_FROZENSET_PASS',
 'color_graph_automorphisms':48,'graph_orbit_representatives_checked':24,
 'all_five_edge_sets_covered_by_orbits':792,'independent_exact_histogram':{'5':12,'6':672,'7':108},
 'explicit_representative_state_replays':24*960,'rows':rows,
 'limit':'Uses exact graph orbit isomorphisms for the other 768 sets; original producer separately checks all 792 exact lower bounds & 760320 policy replays. Not a full physical 12E8C result.'}
(here/'R14_P73_INDEPENDENT_24_ORBIT_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(receipt['result'],'seconds',round(time.monotonic()-t0,1))
