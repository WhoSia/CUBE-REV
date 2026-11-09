#!/usr/bin/env python3
"""R14-P7.4: classify all 6-edge type sets into abstract K222 graph orbits;
calculate exact upper-policy depths on representatives, not exact minimax.
"""
from itertools import permutations,product,combinations
from collections import defaultdict,Counter
from functools import lru_cache
from pathlib import Path
import json,sys,time
T=('UR','UF','UL','UB','DR','DF','DL','DB','FR','FL','BL','BR')
PAIRS=(('U','D'),('R','L'),('F','B'))
EDGES={frozenset(e):e for e in T}
autos=[]
for p in permutations(range(3)):
 for f in product((0,1),repeat=3):
  m={}
  for i,(a,b) in enumerate(PAIRS):m[a]=PAIRS[p[i]][f[i]];m[b]=PAIRS[p[i]][1-f[i]]
  autos.append({e:EDGES[frozenset(m[z] for z in e)] for e in T})
assert len(autos)==48
orbits=defaultdict(list)
for L in combinations(T,6):
 rep=min(tuple(sorted(a[e] for e in L)) for a in autos)
 orbits[rep].append(L)
assert len(orbits)>0 and sum(map(len,orbits.values()))==924
ordered=sorted(orbits.items(),key=lambda z:(-len(z[1]),z[0]))
print('SIX_EDGE_ORBITS',len(orbits),Counter(map(len,orbits.values())),flush=True)
limit=int(sys.argv[1]) if len(sys.argv)>1 else len(ordered)
rows=[];start=time.monotonic()
for k,(L,grp) in enumerate(ordered[:limit],1):
 n=6; W=[]
 for p in permutations(range(n)):
  if sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))%2:continue
  for z in product((0,1),repeat=n-1):
   f=z+(sum(z)%2,)
   W.append(''.join(L[p[i]][(t+f[i])%2] for i in range(n) for t in range(2)))
 assert len(W)==11520 and len(set(W))==11520
 masks=[{} for _ in range(12)]
 for i,w in enumerate(W):
  for q,c in enumerate(w):masks[q][c]=masks[q].get(c,0)|(1<<i)
 def children(B,q):return [x for m in masks[q].values() if (x:=B&m)]
 choices={}
 @lru_cache(None)
 def solve(B):
  if B.bit_count()==1:return 0
  o=[]
  for q in range(12):
   kids=children(B,q)
   if len(kids)<2:continue
   ns=[x.bit_count() for x in kids]
   o.append(((max(ns),len(kids),sum(x*x for x in ns),q),kids))
  win=min(o,key=lambda x:x[0]);choices[B]=win[0][3]
  return 1+max(solve(c) for c in win[1])
 whole=(1<<len(W))-1;d=solve(whole)
 hist=Counter()
 for ix,w in enumerate(W):
  b=whole;steps=0
  while b.bit_count()>1:
   q=choices[b];b &= masks[q][w[q]];steps+=1
  assert b==1<<ix and steps<=d
  hist[steps]+=1
 assert sum(hist.values())==11520 and max(hist)==d
 rows.append({'representative':L,'orbit_size':len(grp),'one_step_worst_depth':d,'replayed_states':11520,'history_depth_hist':dict(sorted(hist.items())),'policy_beliefs':solve.cache_info().currsize})
 print('SIX_REP',k,'/',len(ordered),'orbit',len(grp),'depth',d,'cached',solve.cache_info().currsize,'total_s',round(time.monotonic()-start,1),flush=True)
 result={'result':'R14_P74_SIX_EDGE_GRAPH_ORBIT_AND_UPPER_POLICY_CENSUS','all_924_six_edge_types':924,'graph_automorphisms':48,'orbit_count':len(orbits),'orbit_size_histogram':dict(Counter(map(len,orbits.values()))),'representatives_computed':len(rows),'representative_count':len(ordered),'complete_representative_upper':len(rows)==len(ordered),'rows':rows,'claim_limit':'Exact constructive single-step policy UPPER DEPTH only. Does not certify optimal minimax or prove graph relabeling preserves coordinate-index tie-break for all orbit members; no P48 full cube theorem.'}
 out=Path(__file__).with_name('R14_P74_SIX_EDGE_ORBIT_POLICY_RECEIPT.json');out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(result['result'],len(rows),flush=True)
