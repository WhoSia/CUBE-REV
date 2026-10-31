#!/usr/bin/env python3
"""Classify the 156 B6 optimal omitted-piece layouts up to the FULL cube
octahedral symmetry group of order 48, including 24 mirror operations.

This is a pure geometric calculation and uses no archived B6 success IDs.
The mirror maps' HTM-conjugacy is checked separately by
verify_cube_48_symmetry.py; the physical B6 identification iff is inherited
from the prior full B6 certificate.
"""
from itertools import product,permutations
from collections import Counter
from verify_b6_geometric_rule import EDGE_NAMES,midpoint,valid_pairs

M={midpoint(e):e for e in EDGE_NAMES}
rotations=[]
for p in permutations(range(3)):
    parity=(-1)**sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))
    for signs in product((-1,1),repeat=3):
        determinant=parity*signs[0]*signs[1]*signs[2]
        rotations.append((determinant,lambda xyz,p=p,signs=signs:
                          tuple(signs[i]*xyz[p[i]] for i in range(3))))
assert len(rotations)==48

def induced(pair,R):
    return frozenset(M[R(midpoint(e))] for e in pair)

def orbits(items,stabilizer):
    todo=set(items)
    out=[]
    while todo:
        exemplar=next(iter(todo))
        orb={induced(exemplar,R) for R in stabilizer}
        assert orb<=todo
        out.append(frozenset(orb))
        todo-=orb
    return out

for h in EDGE_NAMES:
    stabilizer=[(det,R) for det,R in rotations
                if R(midpoint(h))==midpoint(h)]
    proper=[R for det,R in stabilizer if det==1]
    full=[R for det,R in stabilizer]
    assert len(stabilizer)==4 and len(proper)==2
    success=valid_pairs(h)
    assert len(success)==13
    proper_orbits=orbits(success,proper)
    full_orbits=orbits(success,full)
    assert len(proper_orbits)==8
    assert Counter(map(len,proper_orbits))=={1:3,2:5}
    assert len(full_orbits)==6
    assert Counter(map(len,full_orbits))=={1:1,2:4,4:1}
    splits=sorted(sum(o<=F for o in proper_orbits) for F in full_orbits)
    assert splits==[1,1,1,1,2,2],(h,splits)
    fixed=[sum(all(induced(p,R)==p for R in [R]) for p in success)
           for det,R in stabilizer]
    assert sorted(fixed)==[3,3,5,13]
    assert sum(fixed)//4==6
print("PASS all 12 fixed core edges and full signed 48-element group")
print("PASS 8 proper-24 orbits merge to 6 mirror-invariant symmetry classes")
print("PASS global 156 layouts = 48 + 4*24 + 12")
print("PASS two mirror-equivalent pairs of proper rotation orbits")
print("BOUNDARY: symmetry classification is a consequence of earlier B6 iff")
