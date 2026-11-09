#!/usr/bin/env python3
"""Independent color-graph orbit derivation, 30 representative policy upper receipt
and the currently completed exact AND-OR lower proof rows. No full 924 claim."""
from itertools import permutations,combinations
from collections import Counter,defaultdict
from pathlib import Path
import json
H=Path(__file__).resolve().parent
upper=json.loads((H/'R14_P74_SIX_EDGE_ORBIT_POLICY_RECEIPT.json').read_text())
lower=json.loads((H/'R14_P74_SIX_EDGE_EXACT_REPRESENTATIVES_RECEIPT.json').read_text())
colors=('U','D','R','L','F','B'); opp={'U':'D','D':'U','R':'L','L':'R','F':'B','B':'F'}
edge_types=tuple(sorted(tuple(sorted(e)) for e in combinations(colors,2) if e[1]!=opp[e[0]]))
assert len(edge_types)==12
# Infer 48 automorphisms independently as ALL permutations preserving opposing pairs.
autos=[]
for perm in permutations(colors):
 m=dict(zip(colors,perm))
 if all(m[opp[x]]==opp[m[x]] for x in colors):autos.append(m)
assert len(autos)==48
orbits={}
for L in combinations(edge_types,6):
 rep=min(tuple(sorted(tuple(sorted((m[a],m[b]))) for a,b in L)) for m in autos)
 orbits.setdefault(rep,[]).append(L)
assert len(orbits)==30 and sum(map(len,orbits.values()))==924
assert Counter(map(len,orbits.values()))==Counter({48:14,24:6,16:1,12:7,4:2})
assert len(upper['rows'])==30 and upper['complete_representative_upper']
membership={L:rep for rep,group in orbits.items() for L in group}
seen=set(); d_count=Counter();policy_replays=0
for r in upper['rows']:
 label=tuple(sorted(tuple(sorted(e)) for e in r['representative']))
 rep=membership[label]
 assert rep not in seen and len(orbits[rep])==r['orbit_size']
 seen.add(rep)
 assert r['replayed_states']==11520 and sum(map(int,r['history_depth_hist'].values()))==11520
 assert max(map(int,r['history_depth_hist'].keys()))==r['one_step_worst_depth']
 d_count[r['one_step_worst_depth']]+=r['orbit_size'];policy_replays+=11520
assert sum(d_count.values())==924 and d_count=={7:20,8:832,9:72}
assert policy_replays==345600
lows={tuple(r['representative']):r for r in lower['rows']}
assert lower['all_checked_lower_infeasible'] and len(lows)==lower['representatives_checked']
for t,r in lows.items():
 u=next(x for x in upper['rows'] if tuple(x['representative'])==t)
 assert r['cannot_finish_one_fewer'] and r['policy_upper']==u['one_step_worst_depth']
 assert r['recursion_states']>0
result={'result':'R14_P74_INDEPENDENT_924_GRAPH_CENSUS_AND_PARTIAL_EVIDENCE_AUDIT_PASS','group_automorphisms':48,'graph_orbits':30,'orbit_size_histogram':dict(sorted(Counter(map(len,orbits.values())).items())),'orbit_weighted_upper_depths':dict(sorted(d_count.items())),'upper_policy_representatives_checked':30,'upper_policy_actual_target_replays':policy_replays,'exact_lower_representatives_verified_from_receipt':len(lows),'limitations':'Independent checker recomputes all 924 graph-orbit memberships and revalidates policy receipt totals; it DOES NOT rerun 30 policies or 8 AND-OR lower searches. Exact lower scripts themselves must be rerun for standalone certification. Weighted depths refer to representative policy unless query transport is established.'}
(H/'R14_P74_INDEPENDENT_GRAPH_CENSUS_RECEIPT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(result)
