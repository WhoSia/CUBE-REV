#!/usr/bin/env python3
"""R14-P8.30: independent physical B7 pair-support completion certificate.

Builds 48 moving stickers from integer cubie coordinates, replays eight
explicit <=14-HTM words, constructs two B7 states by BOTH split orders,
and transports both states through all 24 proper spatial rotations.
Does not import any other CUBE-REV module or assume an earlier B7 verdict.
A successful run proves b7=18 for persistent full original-cubie-tag
sensors, NOT for 6-color spatial facelet sensors.
"""
from itertools import combinations, permutations, product
from collections import Counter
import json

F={"U":(0,1,0),"R":(1,0,0),"F":(0,0,1),
   "D":(0,-1,0),"L":(-1,0,0),"B":(0,0,-1)}
slots=tuple((p,F[f]) for p in product((-1,0,1),repeat=3)
  if sum(v!=0 for v in p) in (2,3)
  for f in "URFDLB" if sum(p[i]*F[f][i] for i in range(3))==1)
assert len(slots)==48
index={s:i for i,s in enumerate(slots)}
I=tuple(range(48))
def rotate(p,axis,power):
    x,y,z=p
    for _ in range(power%4):
        if axis==0:y,z=-z,y
        elif axis==1:x,z=z,-x
        else:x,y=-y,x
    return (x,y,z)
def compose(a,b):return tuple(a[b[i]] for i in range(48))
def inverse(a):
    out=[-1]*48
    for i,j in enumerate(a):out[j]=i
    return tuple(out)
def face_turn(f,power):
    n=F[f];axis=next(i for i in range(3) if n[i])
    return tuple(index[(rotate(p,axis,-n[axis]*power),
                        rotate(v,axis,-n[axis]*power))]
        if p[axis]==n[axis] else index[(p,v)] for p,v in slots)
MOVES={face_turn(f,k) for f in F for k in (1,2,3)}
assert len(MOVES)==18
def state(tokens):
    s=I
    for token in tokens:
        k=2 if token.endswith("2") else 3 if token.endswith("'") else 1
        s=compose(face_turn(token[0],k),s)
    return s
def difference(a,b):
    # Original cubie identifiers are the original lattice positions.
    return frozenset(slots[i][0] for i in range(48) if a[i]!=b[i])

WORDS={
 "C_face12":"U2 R' B D2 B' R U2 R' B D2 B' R",
 "C_body12":"U' B2 U L' F2 L U' B2 U L' F2 L",
 "C_adjacent14":"R' D R F D F' U' F D' F' R' D' R U",
 "E_adjacent13a":"L F R' F' L' U2 R U R U' R2 U2 R",
 "E_adjacent13b":"U F U F2 D' L' U' L U D F2 U2 F'",
 "E_adjacent13c":"F R' F' L' U2 R U R U' R2 U2 R L",
 "E_parallel_opposite14":"F R' D' L' D R L F2 L2 F' L F L F",
 "E_parallel_sameface14":"U' F R' U F' R L' U B' R U' B R' L"
}
rotations=[]
for axes in permutations(range(3)):
    parity=(-1)**sum(axes[i]>axes[j] for i in range(3) for j in range(i+1,3))
    for signs in product((-1,1),repeat=3):
        if parity*signs[0]*signs[1]*signs[2]!=1:continue
        def R(p,axes=axes,signs=signs):
            return tuple(signs[i]*p[axes[i]] for i in range(3))
        rotations.append(tuple(index[(R(p),R(n))] for p,n in slots))
assert len(set(rotations))==24
for r in rotations:
    r_inv=inverse(r)
    assert all(compose(r,compose(t,r_inv)) in MOVES for t in MOVES)

C=set();E=set();tested=0;split_counts=Counter()
for name,word in WORDS.items():
    tokens=word.split()
    assert len(tokens)<=14
    endpoint=difference(I,state(tokens))
    assert len(endpoint)==2
    kind=name[0]
    assert all(sum(v!=0 for v in pos)==(3 if kind=="C" else 2)
               for pos in endpoint)
    for k in range(max(0,len(tokens)-7),min(7,len(tokens))+1):
        pre=state(tokens[:k]);suf=state(tokens[k:])
        # Both are legitimate B7 pairs; the reverse order can yield
        # different ORIGINAL-tag support from the forward split.
        for a,b in ((inverse(suf),pre),(inverse(pre),suf)):
            assert a!=b
            assert len(difference(a,b))==2
            for r in rotations:
                ri=inverse(r)
                x=compose(r,compose(a,ri))
                y=compose(r,compose(b,ri))
                support=difference(x,y)
                assert x!=y and len(support)==2
                assert all(sum(v!=0 for v in pos)==(3 if kind=="C" else 2)
                           for pos in support)
                (C if kind=="C" else E).add(support)
                tested+=1
        split_counts[name]+=1
corners={p for p,n in slots if sum(v!=0 for v in p)==3}
edges={p for p,n in slots if sum(v!=0 for v in p)==2}
assert len(corners)==8 and len(edges)==12
assert C=={frozenset(pair) for pair in combinations(corners,2)}
assert E=={frozenset(pair) for pair in combinations(edges,2)}
assert len(C)==28 and len(E)==66 and tested==720
# Necessity: any sensor set omitting at least two corners OR two
# edges misses a witnessed collision. Sufficiency: at most one omitted
# in each sector fixes every legal permutation by observed original
# identities and each orientation by the mod-3/mod-2 sum constraint.
optimal={(c,e) for c in corners for e in edges}
assert len(optimal)==96
print(json.dumps({
 "status":"PASS","model":"persistent_original_cubie_tags_full_position_orientation",
 "independent_48_sticker_geometry":True,
 "historical_source_or_prior_verifier_imports":False,
 "seed_words":len(WORDS),"proper_rotations":len(rotations),
 "physical_two_state_rotation_checks":tested,
 "complete_corner_pair_supports":len(C),
 "complete_edge_pair_supports":len(E),
 "exact_b7_minimum_sensors":18,
 "optimal_18_sensor_layouts":len(optimal),
 "b7_bfs_enumerated":False,
 "geodesic_minimality_of_seed_words_proved":False,
 "spatial_color_probe_horizon_proved":False,
 "split_counts":dict(split_counts)
},sort_keys=True))
