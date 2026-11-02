#!/usr/bin/env python3
"""B6 near/far obstruction, algebraic consequence of 16 archived physical witnesses.

This script DOES NOT regenerate physical witnesses; consult verify_b6_nf_four_seeds.py.
It certifies the exact hypergraph transversal statement by exhaustive check.
"""
from itertools import combinations
N = ('DB','DF','LB','LF')
F = ('UB','UF','RB','RF')
W = frozenset(frozenset((n,f)) for n in N for f in F)
assert len(W) == 16
U = N+F

def hits(S):
    return all(bool(set(S) & set(edge)) for edge in W)

minimal=[]
for k in range(len(U)+1):
    for S in combinations(U,k):
        s=set(S)
        if hits(s) and all(not hits(s-{v}) for v in s):
            minimal.append(frozenset(s))
assert set(minimal)=={frozenset(N),frozenset(F)}
for k in range(9):
    for s in combinations(U,k):
        assert hits(s)==(set(N).issubset(s) or set(F).issubset(s))
print('PASS: 16 cross-class pair witnesses, exactly two minimal hitting sets (N,F)')
print('PASS: complete bipartite K4,4 cover equivalence over all 256 sensor choices')
print('LIMIT: necessary condition for b6 identification with DL endpoint corners omitted')
