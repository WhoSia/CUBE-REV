#!/usr/bin/env python3
"""Stress-test 2-step population lookahead outside the all-four-edge theorem."""
from itertools import permutations,product
from functools import lru_cache
from collections import Counter
import json
from pathlib import Path
SETS=[('UR','UF','UL','UB','FR'),('UR','UF','UL','UB','FR','FL')]
rows=[]
for L in SETS:
    n=len(L); words=[]
    for p in permutations(range(n)):
        if sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))%2:continue
        for fs in product((0,1),repeat=n-1):
            o=fs+(sum(fs)%2,)
            words.append(''.join(L[p[i]][(j+o[i])%2] for i in range(n) for j in range(2)))
    masks=[{} for _ in range(2*n)]
    for i,w in enumerate(words):
        for q,c in enumerate(w):masks[q][c]=masks[q].get(c,0)|(1<<i)
    def kids(B,q):return [z for m in masks[q].values() if (z:=B&m)]
    @lru_cache(None)
    def onestep(B):
        if B.bit_count()==1:return 1
        return min(max(x.bit_count() for x in cs) for q in range(2*n) if len(cs:=kids(B,q))>1)
    selected={}
    @lru_cache(None)
    def solve(B):
        if B.bit_count()==1:return 0
        opts=[]
        for q in range(2*n):
            cs=kids(B,q)
            if len(cs)<2:continue
            sizes=[x.bit_count() for x in cs]
            opts.append(((max(onestep(c) for c in cs),max(sizes),sum(v*v for v in sizes),q),cs))
        chosen=min(opts,key=lambda x:x[0]);selected[B]=chosen[0][3];return 1+max(solve(c) for c in chosen[1])
    whole=(1<<len(words))-1
    dep=solve(whole)
    replay=Counter()
    for ix,w in enumerate(words):
        B=whole;steps=0
        while B.bit_count()>1:
            q=selected[B]
            B &= masks[q][w[q]]
            steps+=1
        assert B==1<<ix
        replay[steps]+=1
    assert max(replay)==dep and sum(replay.values())==len(words)
    rows.append({'types':list(L),'legal_states':len(words),'lookahead_two_step_depth':dep,'prior_minimax_depth':7 if n==5 else 9,'cached_beliefs':solve.cache_info().currsize,'all_start_states_replayed':len(words),'replay_depth_histogram':dict(sorted(replay.items()))})
    print('two-step residual',n,dep,'believes',solve.cache_info().currsize,flush=True)
result={'result':'R14_P7_FIVE_SIX_TWO_STEP_STRESS_TEST_PASS','rows':rows}
Path(__file__).with_name('R14_P7_FIVE_SIX_LOOKAHEAD_RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
