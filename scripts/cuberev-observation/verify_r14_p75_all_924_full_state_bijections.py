#!/usr/bin/env python3
"""Completely reconstruct ALL 924 independent legal 11520-word state spaces,
then prove an explicit 11520-state *set equality* against signed transport
from each orbit representative. This avoids reliance on imported Bellman scores.
"""
from itertools import permutations,combinations,product
from functools import lru_cache
from collections import Counter
from pathlib import Path
import json,time
H=Path(__file__).resolve().parent
z=json.loads((H/'R14_P75_ALL_924_EXACT_MINIMAX_RECEIPT.json').read_text())
assert z['result']=='R14_P75_ALL_924_EXACT_MINIMAX_COVARIANT_COURT_PASS'
def par(p):return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2
perms=tuple(p for p in permutations(range(6)) if not par(p))
flips=tuple(f+(sum(f)%2,) for f in product((0,1),repeat=5))
assert len(perms)*len(flips)==11520
@lru_cache(None)
def words(L):
 return frozenset(''.join(L[p[i]][s^f[i]] for i in range(6) for s in range(2)) for p in perms for f in flips)
started=time.monotonic();count=0;row_counter=Counter()
for row in z['signed_source_query_transport_witnesses']:
 L=tuple(row['L']);rep=tuple(row['representative']);c=row['color_map'];qmap=row['target_to_source_query_map']
 # row maps L->rep, not rep->L.
 # Full inverse state bijection is implied by injectivity if image has 11520
 # elements and lies in the independent target legal state set.
 source=words(L)
 image={''.join(c[w[qmap[q]]] for q in range(12)) for w in source}
 independent=words(rep)
 assert len(source)==len(image)==len(independent)==11520,(L,len(image),len(independent))
 assert image==independent,L
 count+=11520;row_counter[row['depth']]+=1
 if sum(row_counter.values())%100==0:print('EXACT_BIJECTIONS',sum(row_counter.values()),'of 924',round(time.monotonic()-started,2),flush=True)
receipt={'result':'R14_P75_INDEPENDENT_ALL_924_FULL_STATE_SET_BIJECTIONS_PASS',
 'type_sets':len(z['signed_source_query_transport_witnesses']),
 'full_legal_start_states_independently_enumerated_and_transported':count,
 'size_per_set':11520,'weighted_exact_depth_histogram_from_separately_certified_court':dict(row_counter),
 'condition':'Every signed transported 11520-state set exactly equals independently generated target 11520 legal words, not only sampled checks.',
 'scope':'Parity-even and flip-even six edge color words. No physical full cube P48 lift. Bellman optimality derived from independently recorded P7.4/P7.5 exact representatives.'}
(H/'R14_P75_INDEPENDENT_ALL_924_STATE_BIJECTIONS_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(receipt['result'],count,round(time.monotonic()-started,2))
