#!/usr/bin/env python3
"""Exact D-1 AND-OR impossibility on 30 six-edge graph orbit representatives.
A TRUE result means the proposed one-step depth is exactly optimal in the
conditional parity-fixed game. No inference for other orbit members without
query-coordinate-isomorphism proof.
"""
from itertools import permutations,product
from collections import Counter
from functools import lru_cache
from pathlib import Path
import json,time,sys
HERE=Path(__file__).resolve().parent
prior=json.loads((HERE/'R14_P74_SIX_EDGE_ORBIT_POLICY_RECEIPT.json').read_text())
rows=[];start=time.monotonic()
limit=int(sys.argv[1]) if len(sys.argv)>1 else len(prior['rows'])
for j,entry in enumerate(prior['rows'][:limit]):
 L=entry['representative']; n=len(L); words=[]
 for p in permutations(range(n)):
  if sum(p[i]>p[k] for i in range(n) for k in range(i+1,n))%2:continue
  for z in product((0,1),repeat=n-1):
   f=z+(sum(z)%2,)
   words.append(''.join(L[p[i]][(t+f[i])%2] for i in range(n) for t in range(2)))
 assert len(set(words))==11520
 masks=[{} for _ in range(2*n)]
 for ix,w in enumerate(words):
  for q,c in enumerate(w): masks[q][c]=masks[q].get(c,0)|(1<<ix)
 def kids(B,q):return [v for m in masks[q].values() if (v:=B&m)]
 @lru_cache(None)
 def win(B,k):
  if B.bit_count()==1:return True
  if k<=0 or B.bit_count()>6**k:return False
  opts=[]
  for q in range(2*n):
   cs=kids(B,q)
   if len(cs)<2:continue
   maxsz=max(x.bit_count() for x in cs)
   if maxsz>6**(k-1):continue
   size=[x.bit_count() for x in cs]
   opts.append(((maxsz,len(cs),sum(x*x for x in size),q),cs))
  for _,cs in sorted(opts,key=lambda x:x[0]):
   if all(win(child,k-1) for child in sorted(cs,key=int.bit_count,reverse=True)):return True
  return False
 bound=entry['one_step_worst_depth']; t=time.monotonic();possible=win((1<<len(words))-1,bound-1)
 rows.append({'representative':L,'orbit_size':entry['orbit_size'],'policy_upper':bound,'cannot_finish_one_fewer':not possible,'recursion_states':win.cache_info().currsize,'seconds':round(time.monotonic()-t,3)})
 output={'result':'R14_P74_SIX_EDGE_EXACT_REPRESENTATIVES','graph_orbit_count':prior['orbit_count'],'representatives_checked':len(rows),'all_checked_lower_infeasible':all(x['cannot_finish_one_fewer'] for x in rows),'rows':rows,'scope':'Complete AND-OR lower for listed representative priors ONLY; uniform transfer to other color graph orbit members requires a proved state/query isomorphism. Not full P48.'}
 (HERE/'R14_P74_SIX_EDGE_EXACT_REPRESENTATIVES_RECEIPT.json').write_text(json.dumps(output,indent=2,sort_keys=True)+'\n')
 print('EXACT',j+1,'/',limit,'D',bound,'negative',not possible,'states',win.cache_info().currsize,'s',round(time.monotonic()-t,2),flush=True)
 output={'result':'R14_P74_SIX_EDGE_EXACT_REPRESENTATIVES','graph_orbit_count':prior['orbit_count'],'representatives_checked':len(rows),'all_checked_lower_infeasible':all(x['cannot_finish_one_fewer'] for x in rows),'rows':rows,'scope':'Complete AND-OR lower for listed representative priors ONLY; uniform transfer to other color graph orbit members requires a proved state/query isomorphism. Not full P48.'}
 (HERE/'R14_P74_SIX_EDGE_EXACT_REPRESENTATIVES_RECEIPT.json').write_text(json.dumps(output,indent=2,sort_keys=True)+'\n')
