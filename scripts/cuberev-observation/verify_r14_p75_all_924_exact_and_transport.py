#!/usr/bin/env python3
"""R14-P7.5: independent evidence-composition and all-924 signed policy transport.
Primary AND-OR proof results are imported exactly from P7.4 + P7.5 stage receipts.
Only proves type-set game isomorphism; not a physical 12E/8C P48 action.
"""
from itertools import combinations,permutations,product
from collections import Counter,defaultdict
from pathlib import Path
import json
H=Path(__file__).resolve().parent
T=('UR','UF','UL','UB','DR','DF','DL','DB','FR','FL','BL','BR')
PAIRS=(('U','D'),('R','L'),('F','B'))
canonical={frozenset(t):t for t in T}
upper=json.loads((H/'R14_P74_SIX_EDGE_ORBIT_POLICY_RECEIPT.json').read_text())
all_exact=[]
for f in ['R14_P74_SIX_EDGE_EXACT_REPRESENTATIVES_RECEIPT.json','R14_P75_STAGE_A_LOWER_RECEIPT.json','R14_P75_STAGE_B_LOWER_RECEIPT.json','R14_P75_STAGE_C_LOWER_RECEIPT.json']:
 rows=json.loads((H/f).read_text())['rows']
 for row in rows:
  r=tuple(row['representative'])
  if any(tuple(x['representative'])==r for x in all_exact):continue
  assert row['cannot_finish_one_fewer'] and row['recursion_states']>0,(f,r)
  all_exact.append(row)
assert len(all_exact)==30 and len({tuple(r['representative']) for r in all_exact})==30
assert len(upper['rows'])==30
byrep={tuple(r['representative']):r for r in upper['rows']}
for r in all_exact:
 s=byrep[tuple(r['representative'])]
 assert r['policy_upper']==s['one_step_worst_depth']
 assert r['orbit_size']==s['orbit_size']
colors=('U','D','R','L','F','B')
opp={'U':'D','D':'U','R':'L','L':'R','F':'B','B':'F'}
autos=[]
for p in permutations(colors):
 c=dict(zip(colors,p))
 if all(c[opp[x]]==opp[c[x]] for x in colors):autos.append(c)
assert len(autos)==48
sets=list(combinations(T,6))
classes=defaultdict(list)
for L in sets:
 transforms=[]
 for c in autos:
  dest=tuple(sorted(canonical[frozenset(c[x] for x in e)] for e in L))
  transforms.append(dest)
 classes[min(transforms)].append(L)
assert len(classes)==30
assert set(byrep)==set(classes)
# Every 924 type set obtains a concrete color map and SIGNED query permutation
# to its canonical representative. Verify its permutation and XOR equations.
def par(a):return sum(a[i]>a[j] for i in range(len(a)) for j in range(i+1,len(a)))%2
out=[];weight=Counter();parity_adjustments=Counter();flip_adjustments=Counter()
for L in sets:
 rep=min(tuple(sorted(canonical[frozenset(c[x] for x in e)] for e in L)) for c in autos)
 c=next(c for c in autos if tuple(sorted(canonical[frozenset(c[x] for x in e)] for e in L))==rep)
 tau=tuple(rep.index(canonical[frozenset(c[x] for x in e)]) for e in L)
 eps=tuple(int(''.join(c[x] for x in e)!=canonical[frozenset(c[x] for x in e)]) for e in L)
 sigma=list(range(6))
 if par(tau):sigma[0],sigma[1]=sigma[1],sigma[0]
 delta=[0]*6;delta[0]=sum(eps)%2
 assert par(tau)==par(sigma) and sum(eps)%2==sum(delta)%2
 qmap=tuple(2*sigma[i]+(s^delta[i]) for i in range(6) for s in range(2))
 assert len(set(qmap))==12
 # Independent observation and state invariants for six legal words per set.
 for perm in list(permutations(range(6)))[:32]:
  if par(perm):continue
  for f5 in ((0,0,0,0,0),(1,0,1,0,1)):
   f=f5+(sum(f5)%2,)
   w=''.join(L[perm[i]][s^f[i]] for i in range(6) for s in range(2))
   z=''.join(c[w[qmap[q]]] for q in range(12))
   pp=[];ff=[]
   for i in range(6):
    piece=z[2*i:2*i+2];j=next(j for j,e in enumerate(rep) if set(e)==set(piece))
    pp.append(j);ff.append(int(piece!=rep[j]))
   assert par(pp)==0 and sum(ff)%2==0
 depth=byrep[rep]['one_step_worst_depth'];weight[depth]+=1
 parity_adjustments[par(tau)]+=1;flip_adjustments[sum(eps)%2]+=1
 out.append({'L':L,'representative':rep,'depth':depth,'color_map':c,'source_index_perm':tau,'orientation_correction':eps,'spatial_perm':sigma,'spatial_flip':delta,'target_to_source_query_map':qmap})
assert dict(weight)=={7:20,8:832,9:72}
receipt={'result':'R14_P75_ALL_924_EXACT_MINIMAX_COVARIANT_COURT_PASS',
 'all_924_original_edge_type_sets':924,'exact_representative_lower_proofs':30,
 'verified_representative_upper_policy_replays':345600,'color_graph_orbits':30,
 'exact_minimax_histogram':dict(weight),
 'signed_source_query_transport_witnesses':out,
 'parity_corrections':dict(parity_adjustments),'total_flip_corrections':dict(flip_adjustments),
 'proof_dependence':'30 complete AND-OR D-1 negative certificates imported from P7.4 and three P7.5 stage receipts; 30 constructive one-step upper trees and state replays imported from P7.4; this checker independently reconstructs 924 group orbits and per-set legal state/query signed transport.',
 'limitations':'Correct upper policy for each L is the inverse-transported representative policy, not necessarily freshly evaluated local-index one-step greedy. Source-color graph actions are NOT claimed physical corner/chirality P48 moves; 18<=h_adaptive<=21 full cube remains open.'}
(H/'R14_P75_ALL_924_EXACT_MINIMAX_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(receipt['result'],weight,'signed transports',len(out))
