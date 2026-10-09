#!/usr/bin/env python3
"""CUBE-REV 0.16 P10 — exact SMALL combinatorial witness check.
Requires Python stdlib. This proves the frozen 50x116 abstract covering
statement; the original cube action-to-cover-table bridge belongs to P7/P9.
"""
import json
from pathlib import Path
from collections import Counter

D=json.loads((Path(__file__).resolve().parents[2]/
 'docs/0.16/P10_50_BY_116.json').read_text())
W=list(map(int,D['weights']));Q=list(map(int,D['coverage_masks']))
assert len(W)==50 and len(Q)==116 and len(set(Q))==116
assert sum(W)==276
def mass(m):
    v=0
    while m:
        b=m & -m
        v+=W[b.bit_length()-1]
        m^=b
    return v
assert Counter(map(mass,Q))=={20:110,16:6}
seen=set();components=[]
for i in range(50):
    if i in seen: continue
    comp={i}
    while True:
        before=len(comp)
        for q in Q:
            if any(q>>j&1 for j in comp):
                comp.update(j for j in range(50) if q>>j&1)
        if len(comp)==before: break
    seen.update(comp)
    components.append(comp)
components.sort(key=len)
assert list(map(len,components))==[22,28]
A,B=components
QA=[q for q in Q if any(q>>i&1 for i in A)]
QB=[q for q in Q if any(q>>i&1 for i in B)]
assert (len(QA),len(QB))==(36,80)
assert sum(W[i] for i in A)==180 and sum(W[i] for i in B)==96
assert all(not any(q>>j&1 for j in B) for q in QA)
assert all(not any(q>>j&1 for j in A) for q in QB)
# A needs at least 9 words by 8*20 < 180.
assert 8*20<180
# B: any 5-cover needs 4 disjoint 20-mass sets plus either a
# disjoint 16-mass set or one 20-mass set with exactly 4 mass overlap.
P20=[q for q in QB if mass(q)==20]
P16=[q for q in QB if mass(q)==16]
assert (len(P20),len(P16))==(74,6)
quads=extend16=extend20=0
for a in range(74):
    for b in range(a+1,74):
        if P20[a]&P20[b]:continue
        ab=P20[a]|P20[b]
        for c in range(b+1,74):
            if ab&P20[c]:continue
            abc=ab|P20[c]
            for d in range(c+1,74):
                if abc&P20[d]:continue
                used=abc|P20[d]
                assert mass(used)==80
                quads+=1
                extend16+=sum(not (used&q) for q in P16)
                extend20+=sum(mass(used&q)==4 for v,q in enumerate(P20)
                    if v not in (a,b,c,d))
assert (quads,extend16,extend20)==(7004,0,0)
B6=[23093502280704,774056186273792,4303356016,16783456,2199023256344,985182819581952]
A9=[8796093087744,35184640524288,67108865,274877906946,137438953476,33554560,3801088,68857888768,592705486848]
for C,chosen,valid in ((A,A9,QA),(B,B6,QB)):
    assert set(chosen)<=set(valid)
    union=0
    for q in chosen:union|=q
    assert all(union>>i&1 for i in C)
print('CUBE_REV_016_P10_SPLIT_CORE_EXACT_PASS')
print('A_22_MIN_9 B_28_MIN_6 TOTAL_50_MIN_15')
print('B_DISJOINT_MASS20_FOURTUPLES',quads,'EXTENSIONS_16',extend16,'EXTENSIONS_20',extend20)
