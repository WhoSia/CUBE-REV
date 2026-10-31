#!/usr/bin/env python3
"""B6 corner omission orbit-stabilizer verification.

Computes the proper rotational action on adjacent omitted CORNER pairs.
This is a symmetry certificate, not a B6 positive-sensor-layout certificate.
"""
from itertools import product, permutations, combinations

corners=list(product((-1,1), repeat=3))
rotations=[]
for perm in permutations(range(3)):
    sign=(-1)**sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3))
    for s in product((-1,1), repeat=3):
        if sign*s[0]*s[1]*s[2]==1:
            rotations.append(lambda v,perm=perm,s=s:
                tuple(s[i]*v[perm[i]] for i in range(3)))

assert len(rotations)==24
distance=lambda a,b:sum(x!=y for x,y in zip(a,b))
adjacent={frozenset((a,b)) for a,b in combinations(corners,2)
          if distance(a,b)==1}
assert len(adjacent)==12

representative=next(iter(adjacent))
orbit={frozenset(R(v) for v in representative) for R in rotations}
stabilizer=[R for R in rotations
            if frozenset(R(v) for v in representative)==representative]

assert orbit==adjacent
assert len(stabilizer)==2
assert len(orbit)*len(stabilizer)==len(rotations)
print('PASS 24 proper rotations / 12 adjacent-corner omitted-pair orbit')
print('PASS stabilizer order 2; orbit-stabilizer identity 12*2=24')
print('LIMIT: B6 positive 16-tag base count remains unresolved')
