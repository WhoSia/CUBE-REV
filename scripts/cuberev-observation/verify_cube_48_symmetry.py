#!/usr/bin/env python3
"""Prove geometric MIRROR symmetries normalize the Rubik 18-HTM move set.

Usage: python verify_cube_48_symmetry.py ARCHIVED_B1_B5.zip

For each of 48 signed coordinate permutations, conjugate the ORIGINAL
54-facelet permutations for ALL 18 face turns; match the result to one
of the same 18 generators. This is stronger than checking sensor-set
geometry alone. Reflections are mathematical automorphisms, not spatial
rotations achievable by physically turning the whole cube.
"""
import sys,zipfile
from itertools import product,permutations

assert len(sys.argv)==2
with zipfile.ZipFile(sys.argv[1]) as z:
    scope={"__name__":"source_for_equivariance","__file__":"independent_b4.py"}
    exec(compile(z.read("independent_b4.py"),"independent_b4.py","exec"),scope)

slots=scope["slots"]
loc=scope["loc"]
moves=scope["moves"]
move_index={p:i for i,p in enumerate(moves)}
assert len(slots)==54 and len(moves)==18 and len(move_index)==18
parity_count={1:0,-1:0}
relations=0
for axes in permutations(range(3)):
    parity=(-1)**sum(axes[i]>axes[j] for i in range(3)
                     for j in range(i+1,3))
    for signs in product((-1,1),repeat=3):
        det=parity*signs[0]*signs[1]*signs[2]
        parity_count[det]+=1
        def mirror(v):
            return tuple(signs[i]*v[axes[i]] for i in range(3))
        P=[loc[(mirror(pos),mirror(normal))] for pos,normal in slots]
        assert sorted(P)==list(range(54))
        inv=[0]*54
        for i,j in enumerate(P):inv[j]=i
        for m in moves:
            conjugate=tuple(P[m[inv[i]]] for i in range(54))
            assert conjugate in move_index
            relations+=54
assert parity_count=={1:24,-1:24}
assert relations==48*18*54==46656
print("PASS 24 proper rotations and 24 orientation-reversing mirror maps")
print("PASS 48*18*54=46656 sticker-level conjugacy relations")
print("CAVEAT mathematical mirror symmetry != physical spatial rotation")
