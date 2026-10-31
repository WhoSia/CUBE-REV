#!/usr/bin/env python3
"""B7 global static base count and 24-rotation orbit certificate.

Depends on the *physical* B7 pair-support proof in verify_b7_support_completion.py.
This standalone combinatorial checker does not claim B7 BFS or active readout cost.
"""
from itertools import product,permutations
from collections import Counter

C=list(product((-1,1),repeat=3))
E=[p for p in product((-1,0,1),repeat=3) if p.count(0)==1]
assert len(C)==8 and len(E)==12

valid=Counter()
for mask in range(1<<20):
    nC=(mask&255).bit_count()
    nE=(mask>>8).bit_count()
    # Because ALL pure two-corner and pure two-edge supports occur in B7,
    # exactly the chosen sets with >=7 corners and >=11 edges are bases.
    if nC>=7 and nE>=11:
        valid[nC+nE]+=1
assert dict(valid)=={18:96,19:20,20:1},valid

rots=[]
for p in permutations(range(3)):
    sign=(-1)**sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))
    for s in product((-1,1),repeat=3):
        if sign*s[0]*s[1]*s[2]==1:
            rots.append(lambda v,p=p,s=s:tuple(s[i]*v[p[i]] for i in range(3)))
assert len(rots)==24

# Any 18-tag base omits precisely one corner and one edge.
# Its orbit is determined by the proper 24 cube rotations.
remaining={(c,e) for c in C for e in E}
orbits=[]
while remaining:
    c,e=next(iter(remaining))
    orbit={(R(c),R(e)) for R in rots}
    assert len(orbit)==24 and orbit<=remaining
    remaining-=orbit
    ends=[v for v in C if all(e[i]==0 or e[i]==v[i] for i in range(3))]
    assert len(ends)==2
    min_dist=min(sum(a!=b for a,b in zip(c,v)) for v in ends)
    orbits.append((min_dist,orbit))
assert len(orbits)==4 and not remaining
assert Counter(d for d,_ in orbits)=={0:1,1:2,2:1}

print("PASS exhaustive 1,048,576 candidate tag sets")
print("PASS all B7/global static identifying layouts:",dict(valid))
print("PASS optimal b7=18; exactly 96 optimal layouts in four orbits of 24")
print("PASS omission corner-to-edge distances: 0,1,1,2")
print("PASS one permanent erasure: unique all-20 layout; two erasures impossible")
