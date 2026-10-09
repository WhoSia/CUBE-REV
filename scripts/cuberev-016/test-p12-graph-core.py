#!/usr/bin/env python3
"""CUBE-REV 0.16: exact P12 four-light graph/24-target critical-cover court.
This tests the necessary NEAR-TIGHT catalogue for a hypothetical 24-word
solution only. It is not a proof about arbitrary 25-word catalogues.
"""
import json, sys
from pathlib import Path
HERE=Path(__file__).resolve().parents[2]
D=json.loads((HERE/'docs/0.16/P10_50_BY_116.json').read_text())
C=json.loads((HERE/'docs/0.16/P12_CORE_CERTIFICATE.json').read_text())
W=D['weights'];Q=list(map(int,D['coverage_masks']))
H=C['heavy20'];L=C['light8'];S=C['minimal_light4']
assert len(Q)==116 and len(W)==50 and len(H)==20 and len(L)==8
assert sum(W[i] for i in H)==80 and sum(W[i] for i in L)==16
near=[(j,q) for j,q in enumerate(Q) if any((q>>i)&1 for i in H+L)]
assert len(near)==80
allbits=sum(1<<i for i in H+S)
def solve(target,k=5):
    proj={q&target for _,q in near if q&target}
    proj=[p for p in proj if not any(q!=p and q&p==p for q in proj)]
    options={i:[p for p in proj if p>>i&1] for i in H+S if target>>i&1}
    memo=set()
    def rec(covered,slots):
        missing=target&~covered
        if not missing:return []
        if not slots or (covered,slots) in memo:return None
        if max((p&missing).bit_count() for p in proj)*slots<missing.bit_count():return None
        i=min((i for i in options if missing>>i&1),key=lambda i:len(options[i]))
        for p in sorted(options[i],key=lambda p:(p&missing).bit_count(),reverse=True):
            rest=rec(covered|p,slots-1)
            if rest is not None:return [p]+rest
        memo.add((covered,slots));return None
    return rec(0,k)
assert solve(allbits) is None
for t in H+S:
    sol=solve(allbits^(1<<t))
    assert sol is not None and len(sol)<=5,t
assert C['light8_bitmask_of_core']==sum(1<<L.index(i) for i in S)==150
patterns={int(k):int(v) for k,v in C['light_profiles_17_with_multiplicity'].items()}
assert len(patterns)==17 and sum(patterns.values())==3008
assert len([k for k in patterns if k.bit_count()==4])==7
assert len([k for k in patterns if k.bit_count()==6])==10
assert all(p&150!=150 for p in patterns)
edges=[tuple(i for i in range(8) if not ((p>>i)&1)) for p in patterns if p.bit_count()==6]
assert sorted(edges)==sorted(map(tuple,C['missing_pair_edges']))
assert len(edges)==10 and all(any((150>>i)&1 for i in e) for e in edges)
matching=C['matching']
assert len(matching)==4 and len({i for e in matching for i in e})==8
assert all(tuple(e) in edges for e in matching)
# A matching of size four forces a vertex cover of size >=4.
for size in range(4):
    from itertools import combinations
    for vertices in combinations(range(8),size):
        t=sum(1<<i for i in vertices)
        assert any((p&t)==t for p in patterns if p.bit_count()==6)
# Hand over the exact candidate words to independent C++ court via stdin file.
if len(sys.argv)==3 and sys.argv[1]=='--emit':
    with open(sys.argv[2],'w') as f:
        for _,q in near:
            f.write(str(sum(1<<i for i,j in enumerate(H+L) if (q>>j)&1))+'\n')
print('CUBE_REV_016_P12_24_CRITICAL_TARGETS_17_LIGHT_PROFILES_PYTHON_PASS')
