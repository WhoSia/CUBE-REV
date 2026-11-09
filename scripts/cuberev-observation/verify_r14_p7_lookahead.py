#!/usr/bin/env python3
"""Independent audit: direct frozenset belief partitions and exact minimax.
Does not import producer or reuse producer's bit masks/recursive routines.
"""
from itertools import combinations,permutations,product
from collections import Counter
from functools import lru_cache
from pathlib import Path
import json,sys
path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('R14_P7_ALL_495_LOOKAHEAD_RESULTS.json')
receipt=json.loads(path.read_text())
assert receipt['result']=='R14_P7_ALL_495_TWO_STEP_LOOKAHEAD_PASS'
assert len(receipt['rows'])==495
rows={tuple(r['types']):r for r in receipt['rows']}
all_types=('UR','UF','UL','UB','DR','DF','DL','DB','FR','FL','BL','BR')
hist_exact=Counter();hist_look=Counter();hist_greedy=Counter();all_replays=0
for n,L in enumerate(combinations(all_types,4),1):
    alternatives=[]
    for p in permutations(range(4)):
        if sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))%2:continue
        for f in product((0,1),repeat=3):
            o=f+(sum(f)%2,)
            alternatives.append(''.join(L[p[i]][(j+o[i])%2] for i in range(4) for j in range(2)))
    assert len(set(alternatives))==96
    def separate(B,q):
        parts={}
        for i in B:parts.setdefault(alternatives[i][q],set()).add(i)
        return [frozenset(s) for s in parts.values()]
    @lru_cache(None)
    def second_best_max(B):
        if len(B)==1:return 1
        return min(max(map(len,parts)) for q in range(8) if len(parts:=separate(B,q))>1)
    def heuristic(B,which):
        opts=[]
        for q in range(8):
            kids=separate(B,q)
            if len(kids)<2:continue
            sizes=[len(s) for s in kids]
            key=(max(second_best_max(v) for v in kids),max(sizes),sum(j*j for j in sizes),q) if which=='two' else (max(sizes),sum(j*j for j in sizes),q)
            opts.append((key,q,kids))
        return min(opts,key=lambda x:x[0])
    @lru_cache(None)
    def greedy_depth(B,which):
        if len(B)==1:return 0
        return 1+max(greedy_depth(c,which) for c in heuristic(B,which)[2])
    @lru_cache(None)
    def possible(B,k):
        if len(B)==1:return True
        if not k or len(B)>6**k:return False
        for q in range(8):
            kids=separate(B,q)
            if len(kids)<2 or max(map(len,kids))>6**(k-1):continue
            if all(possible(v,k-1) for v in sorted(kids,key=len,reverse=True)):return True
        return False
    full=frozenset(range(96))
    expected=rows[L]
    exact=next(k for k in (3,4,5) if possible(full,k))
    two=greedy_depth(full,'two');one=greedy_depth(full,'one')
    assert (exact,one,two)==(expected['exact'],expected['greedy'],expected['two_step']), (L,exact,one,two)
    # Independently execute policy on EACH of the 96 hidden states.
    for st in range(96):
        B=full;steps=0
        while len(B)>1:
            _,q,kids=heuristic(B,'two')
            B=next(v for v in kids if st in v)
            steps+=1
        assert B==frozenset((st,)) and steps<=two
        all_replays+=1
    hist_exact[exact]+=1;hist_greedy[one]+=1;hist_look[two]+=1
assert dict(hist_exact)=={3:72,4:369,5:54}
assert dict(hist_greedy)=={3:72,4:249,5:174}
assert dict(hist_look)=={3:72,4:369,5:54}
assert all_replays==495*96
print('R14_P7_INDEPENDENT_ALL_495_TWO_STEP_EXACT_MINIMAX_PASS',all_replays)
