#!/usr/bin/env python3
"""Complete exact 5-edge 792-family certification, independently lower-bounding
existing one-step upper policy via direct AND-OR on all 960 parity-fixed states.
Explicit complete one-step policy leaf replay on all 792*960 hidden states.
One source depends on the full P7.3 792-row upper-policy search receipt.
"""
from collections import Counter
from functools import lru_cache
from itertools import permutations,product,combinations
from pathlib import Path
import json,time
H=Path(__file__).resolve().parent
pre=json.loads((H/'R14_P73_ANYTIME_FIVE_EDGE_SEARCH.json').read_text())
assert pre['attempted']==792 and not pre['found_one_step_beaten_by_two_step']
all_types=('UR','UF','UL','UB','DR','DF','DL','DB','FR','FL','BL','BR')
ref={frozenset(r['types']):r for r in pre['rows']}
assert len(ref)==792
statistics=Counter(); rows=[]; checked=0; replays=0; total_calls=0; started=time.monotonic()
for L in combinations(all_types,5):
    prior=ref[frozenset(L)]
    expected=prior['fewest_outcomes_one_step']
    assert prior['two_step_maxleaf']==expected and expected in (5,6,7)
    words=[]
    for p in permutations(range(5)):
        if sum(p[i]>p[j] for i in range(5) for j in range(i+1,5))%2:continue
        for f in product((0,1),repeat=4):
            o=f+(sum(f)%2,)
            words.append(''.join(L[p[i]][(j+o[i])%2] for i in range(5) for j in range(2)))
    assert len(set(words))==960
    masks=[{} for _ in range(10)]
    for ix,w in enumerate(words):
        for q,c in enumerate(w):masks[q][c]=masks[q].get(c,0)|(1<<ix)
    def kids(B,q):return [z for m in masks[q].values() if (z:=B&m)]
    # Lower: full exact AND-OR search, not a heuristic estimate or oracle.
    @lru_cache(None)
    def can_finish(B,budget):
        if B.bit_count()==1:return True
        if budget==0 or B.bit_count()>6**budget:return False
        possibilities=[]
        for q in range(10):
            ch=kids(B,q)
            if len(ch)<2 or max(x.bit_count() for x in ch)>6**(budget-1):continue
            counts=[x.bit_count() for x in ch]
            possibilities.append(((max(counts),len(ch),sum(z*z for z in counts),q),ch))
        for _,cs in sorted(possibilities,key=lambda x:x[0]):
            if all(can_finish(c,budget-1) for c in sorted(cs,key=int.bit_count,reverse=True)):
                return True
        return False
    full=(1<<960)-1
    lower_impossible=not can_finish(full,expected-1)
    assert lower_impossible,('Unexpected shorter exact policy',L,expected)
    total_calls+=can_finish.cache_info().misses
    # Upper: independently build entire one-step choosing policy, and ensure
    # it is a *total*, correct, no-hidden-state-oracle decision tree.
    choice={}
    @lru_cache(None)
    def policy_depth(B):
        if B.bit_count()==1:return 0
        options=[]
        for q in range(10):
            cs=kids(B,q)
            if len(cs)<2:continue
            cnt=[z.bit_count() for z in cs]
            options.append(((max(cnt),len(cs),sum(z*z for z in cnt),q),cs))
        best=min(options,key=lambda z:z[0])
        choice[B]=best[0][-1]
        return 1+max(policy_depth(child) for child in best[1])
    actual=policy_depth(full)
    assert actual==expected
    for ix,w in enumerate(words):
        B=full;count=0
        while B.bit_count()>1:
            q=choice[B]
            B &= masks[q][w[q]]
            count+=1
            assert count<=expected
        assert B==1<<ix
        replays+=1
    checked+=1; statistics[expected]+=1
    rows.append({'types':L,'exact_minimax':expected,'one_step_fewest_outcomes':actual,'two_step_maxleaf':prior['two_step_maxleaf'],
                 'full_and_or_lower_budget':expected-1,'lower_unsatisfiable':True,
                 'exact_and_or_cached_states':can_finish.cache_info().currsize,
                 'complete_policy_nodes':policy_depth.cache_info().currsize,
                 'decoded_initial_states':960})
    if checked%100==0:print('COMPLETE',checked,'of 792','seconds',round(time.monotonic()-started,2),flush=True)
assert checked==792 and replays==792*960
assert dict(statistics)=={5:12,6:672,7:108}
output={'result':'R14_P73_ALL_792_FIVE_EDGE_EXACT_MINIMAX_ONE_STEP_PASS',
        'all_five_edge_sets':792,'states_per_set':960,'total_individual_decoder_replays':replays,
        'exact_minimax_histogram':dict(sorted(statistics.items())),
        'one_step_fewest_outcomes_optimal_sets':792,'two_step_maxleaf_optimal_sets':792,
        'complete_AND_OR_lower_one_below_policy_for_all_sets':True,
        'exact_lower_recursion_total_cached_states':total_calls,
        'rows':rows,'scope':'Exact 960-state known even-parity/even-flip five-edge residuals. No full P48 20-frame result.'}
(H/'R14_P73_ALL_792_EXACT_MINIMAX_RECEIPT.json').write_text(json.dumps(output,indent=2,sort_keys=True)+'\n')
print('R14_P73_ALL_792_FIVE_EDGE_EXACT_MINIMAX_ONE_STEP_PASS',replays,statistics,'seconds',round(time.monotonic()-started,2))
