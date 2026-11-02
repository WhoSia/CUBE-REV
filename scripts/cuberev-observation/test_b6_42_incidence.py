#!/usr/bin/env python3
"""Regress the exact B6 N-N and F-F 4:2 incidence explanation.

Pure cube combinatorics. The independent *physical witness* and positive
census checks live in the pre-existing geometric bridge scripts.
"""
from itertools import combinations
from verify_b6_geometric_rule import EDGE_NAMES, ENDS, FACES, admissible

def shared_face(a,b):
    return bool(set(a)&set(b))

def check(h):
    ends=ENDS[h]
    opposite=frozenset(tuple(-a for a in x) for x in ends)
    hstar=next(e for e in EDGE_NAMES if ENDS[e]==opposite)
    near={e for e in EDGE_NAMES if e!=h and ENDS[e]&ends}
    far={e for e in EDGE_NAMES if e!=hstar and ENDS[e]&opposite}
    assert len(near)==len(far)==4
    near_expected={frozenset((a,b)) for a,b in combinations(near,2)
                   if not (ENDS[a]&ENDS[b]&ends)}
    far_expected={frozenset((a,b)) for a,b in combinations(far,2)
                  if shared_face(a,b)}
    assert len(near_expected)==len(far_expected)==4
    for family,expected in ((near,near_expected),(far,far_expected)):
        candidate={frozenset(p) for p in combinations(family,2)}
        actual={pair for pair in candidate
                if admissible(h,*tuple(sorted(pair)))}
        assert actual==expected, (h,family,actual,expected)
        assert len(candidate-actual)==2
    return near_expected,far_expected

if __name__=='__main__':
    for h in EDGE_NAMES:
        check(h)
    near,far=check('DL')
    assert {frozenset(p) for p in
            [('UB','UF'),('UB','RB'),('UF','RF'),('RB','RF')]}==far
    assert {frozenset(p) for p in
            [('UB','RF'),('UF','RB')]}==(
        {frozenset(p) for p in combinations(('UB','UF','RB','RF'),2)}-far)
    print('PASS: N cross-endpoint 4:2 split and F common-face C4 4:2 split for all 12 cube edges')
    print('LIMIT: incidence validation does not establish B6 physical sufficiency')
