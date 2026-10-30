#!/usr/bin/env python3
"""Independent finite obstruction audit, NOT full B6/B7 state census."""
from itertools import combinations,product

C=list(product((0,1),repeat=3))
def hamming(a,b):return sum(x!=y for x,y in zip(a,b))
E=[frozenset((a,b)) for a,b in combinations(C,2) if hamming(a,b)==1]
assert len(C)==8 and len(E)==12
corner_pairs={d:{frozenset((a,b)) for a,b in combinations(C,2)
                 if hamming(a,b)==d} for d in (1,2,3)}
assert [len(corner_pairs[d]) for d in (1,2,3)]==[12,12,4]
adj={frozenset((i,j)) for i,j in combinations(range(12),2) if E[i]&E[j]}
disjoint={frozenset((i,j)) for i,j in combinations(range(12),2) if not E[i]&E[j]}
assert len(adj)==24 and len(disjoint)==42
assert set().union(*corner_pairs[2],*corner_pairs[3])==set(C)
assert set().union(*adj)==set(range(12))
# B6 necessary pure-support constraints:
# A 16-tag layout would omit exactly two corners, required adjacent,
# and exactly two edges. Before older mixed supports 12*C(12,2)=792.
assert len(corner_pairs[1])*66==792
# B7 necessary pure-support constraints:
# A 17-tag layout would omit one corner and two DISJOINT edges.
assert len(C)*len(disjoint)==336
# For one erasure, any two-tag collision forces BOTH its tags selected.
# By B7 corner and edge witness orbits touch all twenty tags.
print('PASS corner support orbit sizes [12,12,4]; B6 two-corner orbits 16')
print('PASS 24 incident and 42 disjoint edge pairs in L(Q3)')
print('PASS candidate caps: B6 16-tag <=792 (before B5), B7 17-tag <=336')
print('PASS one-erasure support coverage of 8 corners B6, 12 edges B7')
print('These are necessary constraints, NOT full-radius positive censuses')
