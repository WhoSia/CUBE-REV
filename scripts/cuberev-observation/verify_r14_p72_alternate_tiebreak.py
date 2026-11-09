#!/usr/bin/env python3
"""Independent direct-frozenset replay of new simple one-step 495-case rule.
Does not import producer or share bitmask/recursive machinery.
"""
from itertools import permutations,product,combinations
from functools import lru_cache
from collections import Counter
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
old=json.loads((HERE/'R14_P7_ALL_495_LOOKAHEAD_RESULTS.json').read_text())
result=json.loads((HERE/'R14_P72_ALL_495_TIEBREAK_RESULTS.json').read_text())
original={tuple(r['types']):r for r in old['rows']}
variants={tuple(r['types']):r for r in result['rows']}
labels=('UR','UF','UL','UB','DR','DF','DL','DB','FR','FL','BL','BR')
assert len(original)==len(variants)==495
hist=Counter();replays=0
for L in combinations(labels,4):
    words=[]
    for p in permutations(range(4)):
        if sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))%2:continue
        for o3 in product((0,1),repeat=3):
            o=o3+(sum(o3)%2,)
            words.append(''.join(L[p[i]][(j+o[i])%2] for i in range(4) for j in range(2)))
    assert len(set(words))==96
    def children(B,q):
        d={}
        for ix in B:d.setdefault(words[ix][q],set()).add(ix)
        return [frozenset(v) for v in d.values()]
    @lru_cache(None)
    def choose(B):
        choices=[]
        for q in range(8):
            cs=children(B,q)
            if len(cs)<2:continue
            sizes=[len(z) for z in cs]
            choices.append(((max(sizes),len(cs),sum(v*v for v in sizes),q),q))
        return min(choices)[1]
    @lru_cache(None)
    def worst(B):
        if len(B)==1:return 0
        return 1+max(worst(k) for k in children(B,choose(B)))
    whole=frozenset(range(96))
    depth=worst(whole)
    assert depth==variants[L]['few']==original[L]['exact'],(L,depth)
    for target in range(96):
        B=whole; steps=0
        while len(B)>1:
            q=choose(B)
            B=next(ch for ch in children(B,q) if target in ch)
            steps+=1
        assert B==frozenset([target]) and steps<=depth
        replays+=1
    hist[depth]+=1
assert replays==47520 and hist=={3:72,4:369,5:54}
print('R14_P72_INDEPENDENT_ONE_STEP_FEWEST_BRANCHES_47520_DECODERS_PASS',hist,replays)
