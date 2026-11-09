#!/usr/bin/env python3
"""Exact 495-residual finite audit: one-step balance vs two-step lookahead.
Compares each policy to fresh exact AND-OR minimax for fixed parity 0.
No imports from CUBE-REV.
"""
from itertools import combinations, permutations, product
from collections import Counter
from functools import lru_cache
import json
from pathlib import Path
TYPES=('UR','UF','UL','UB','DR','DF','DL','DB','FR','FL','BL','BR')
def even(p):return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2==0
rows=[]
for L in combinations(TYPES,4):
    words=[]
    for p in permutations(range(4)):
        if not even(p):continue
        for flips in product((0,1), repeat=3):
            o=flips+(sum(flips)%2,)
            words.append(''.join(L[p[i]][(j+o[i])%2] for i in range(4) for j in range(2)))
    assert len(set(words))==96
    cells=[{} for _ in range(8)]
    for i,w in enumerate(words):
        for q,c in enumerate(w): cells[q][c]=cells[q].get(c,0)|(1<<i)
    def children(B,q):return [c for m in cells[q].values() if (c:=B&m)]
    @lru_cache(None)
    def min_worst_one_step(B):
        if B.bit_count()==1:return 1
        return min(max(ch.bit_count() for ch in kids) for q in range(8) if len(kids:=children(B,q))>1)
    @lru_cache(None)
    def two_step_score(B,q):
        kids=children(B,q)
        return max(min_worst_one_step(ch) for ch in kids)
    def choose(B,lookahead):
        opts=[]
        for q in range(8):
            kids=children(B,q)
            if len(kids)<2:continue
            counts=[v.bit_count() for v in kids]
            key=(two_step_score(B,q),max(counts),sum(t*t for t in counts),q) if lookahead else (max(counts),sum(t*t for t in counts),q)
            opts.append((key,q,kids))
        return min(opts,key=lambda z:z[0])
    @lru_cache(None)
    def greedy(B,lookahead):
        if B.bit_count()==1:return 0
        _,q,kids=choose(B,lookahead)
        return 1+max(greedy(v,lookahead) for v in kids)
    @lru_cache(None)
    def win(B,k):
        if B.bit_count()==1:return True
        if k==0 or B.bit_count()>6**k:return False
        for q in range(8):
            kids=children(B,q)
            if len(kids)<2 or max(z.bit_count() for z in kids)>6**(k-1):continue
            if all(win(z,k-1) for z in sorted(kids,key=int.bit_count,reverse=True)):return True
        return False
    root=(1<<96)-1
    d1=greedy(root,False);d2=greedy(root,True)
    exact=next(k for k in range(1,6) if win(root,k))
    assert exact<=d1 and exact<=d2
    rows.append({'types':list(L),'exact':exact,'greedy':d1,'two_step':d2})
exact_hist=dict(sorted(Counter(r['exact'] for r in rows).items()))
g_hist=dict(sorted(Counter(r['greedy'] for r in rows).items()))
two_hist=dict(sorted(Counter(r['two_step'] for r in rows).items()))
regret1=Counter(r['greedy']-r['exact'] for r in rows)
regret2=Counter(r['two_step']-r['exact'] for r in rows)
result={'result':'R14_P7_ALL_495_TWO_STEP_LOOKAHEAD_PASS',
 'all_four_edge_labels':495,'exact_hist':exact_hist,'one_step_hist':g_hist,'two_step_hist':two_hist,
 'one_step_regret':dict(regret1),'two_step_regret':dict(regret2),
 'two_step_better_cases':sum(r['two_step']<r['greedy'] for r in rows),
 'two_step_worse_cases':sum(r['two_step']>r['greedy'] for r in rows),
 'witness_improvement':next((r for r in rows if r['two_step']<r['greedy']),None),
 'witness_worsening':next((r for r in rows if r['two_step']>r['greedy']),None),
 'rows':rows,'scope':'Parity-conditioned four original edge types, 96 legal states each; greedy two-step minimax of largest leaf POPULATION, not full Bellman depth.'}
print({k:v for k,v in result.items() if k not in ('rows',)},flush=True)
Path(__file__).with_name('R14_P7_ALL_495_LOOKAHEAD_RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
