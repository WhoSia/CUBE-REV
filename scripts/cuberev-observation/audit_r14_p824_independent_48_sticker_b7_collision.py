#!/usr/bin/env python3
"""R14-P8.24: independent 48 moving sticker audit of an explicit 13-HTM
word and an actual B7 collision of two states that are identical on 16
original full-cubie-tag observations.

No import from original 54-facelet or historical P48 engines.
The lower radius B6 positivity of this layout is an INHERITED,
separate 41-class physical certificate, NOT re-proven here.
"""
from itertools import product, permutations
import json

F={"U":(0,1,0),"R":(1,0,0),"F":(0,0,1),
   "D":(0,-1,0),"L":(-1,0,0),"B":(0,0,-1)}
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def det(a,b,c):
    return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])
slots=tuple((p,F[f]) for p in product((-1,0,1),repeat=3)
            if sum(v!=0 for v in p) in (2,3)
            for f in "URFDLB" if dot(p,F[f])==1)
assert len(slots)==48
idx={s:i for i,s in enumerate(slots)}
pieces={}
for p in sorted(set(p for p,_ in slots)):
    ids=[idx[(p,n)] for n in F.values() if dot(p,n)==1]
    if len(ids)==3:
        ids.sort(key=lambda i:0 if abs(slots[i][1][1]) else 1
                 if abs(slots[i][1][0]) else 2)
        if det(*(slots[i][1] for i in ids))==-1:ids[1],ids[2]=ids[2],ids[1]
        assert det(*(slots[i][1] for i in ids))==1
    else:
        assert len(ids)==2
        ids.sort(key=lambda i:0 if abs(slots[i][1][1]) else 1
                 if abs(slots[i][1][2]) else 2)
    pieces[p]=tuple(ids)
assert sorted(map(len,pieces.values()))==[2]*12+[3]*8
def rotate(p,axis,k):
    x,y,z=p
    for _ in range(k%4):
        if axis==0:y,z=-z,y
        elif axis==1:x,z=z,-x
        else:x,y=-y,x
    return x,y,z
def move(face,power):
    n=F[face];axis=next(i for i,x in enumerate(n) if x)
    moved=[]
    for p,normal in slots:
        if p[axis]==n[axis]:
            p,normal=rotate(p,axis,-n[axis]*power),rotate(normal,axis,-n[axis]*power)
        moved.append(idx[(p,normal)])
    return tuple(moved)
def compose(a,b):return tuple(a[b[i]] for i in range(48))
def inverse(p):
    out=[-1]*len(p)
    for i,j in enumerate(p):out[j]=i
    return tuple(out)
def state(tokens):
    answer=tuple(range(48))
    for tok in tokens:
        power=2 if tok.endswith("2") else 3 if tok.endswith("'") else 1
        answer=compose(move(tok[0],power),answer)
    return answer

w="L F R' F' L' U2 R U R U' R2 U2 R".split()
assert len(w)==13
core=tuple(F["D"][i]+F["L"][i] for i in range(3))
omitted_corners=sorted(p for p in pieces if len(pieces[p])==3
                       and all(p[i]==core[i] for i in range(3) if core[i]))
omitted_edges=sorted(tuple(F[a][i]+F[b][i] for i in range(3))
                     for a,b in (("U","F"),("U","R")))
omitted=set(omitted_corners+omitted_edges)
assert len(omitted)==4
goal=list(range(48))
for firstpos,secondpos in (omitted_corners,omitted_edges):
    a,b=pieces[firstpos],pieces[secondpos]
    for i in range(len(a)):
        if len(a)==2:
            goal[a[i]]=a[(i+1)%2]
            goal[b[i]]=b[(i-1)%2]
got=state(w)
assert got==tuple(goal)
actual_support={p for p,stickers in pieces.items() if any(got[i]!=i for i in stickers)}
assert actual_support==set(omitted_edges)
assert sum(i!=v for i,v in enumerate(got))==4

# With word multiplication state(w)=state(suffix) o state(prefix),
# define x=state(suffix)^-1 (7 moves), y=state(prefix) (6 moves).
# Then x^-1 o y = goal, so each observed ORIGINAL tag has equal
# position/orientation in x and y, even though the states differ.
x=inverse(state(w[6:]))
y=state(w[:6])
assert x!=y and compose(inverse(x),y)==got
kept=set(pieces)-omitted
assert len(kept)==16
assert all(x[i]==y[i] for p in kept for i in pieces[p])

# Propagate through all 24 proper spatial rotations. This orbit has
# 24 DISTINCT original-tag omitted layouts; the witness can be rotated
# physically by known face-conjugation.
orbit=set()
for axes in permutations(range(3)):
    sign=(-1)**sum(axes[i]>axes[j] for i in range(3) for j in range(i+1,3))
    for signs in product((-1,1),repeat=3):
        if sign*signs[0]*signs[1]*signs[2]!=1:continue
        orbit.add(frozenset(tuple(signs[i]*p[axes[i]] for i in range(3))
                            for p in omitted))
assert len(orbit)==24

print(json.dumps({
    "status":"R14_P824_EXPLICIT_PHYSICAL_B7_TWO_STATE_16TAG_COLLISION_PASS",
    "known_18HTM_word_length":len(w),
    "first_state_max_word_length":7,
    "second_state_max_word_length":6,
    "observed_original_tag_count":len(kept),
    "witness_original_tag_difference_count":len(actual_support),
    "original_moving_stickers":sum(i!=v for i,v in enumerate(got)),
    "proper_rotation_distinct_omitted_four_tag_layouts":len(orbit),
    "conditional_B6_physical_positive_certificate":"INHERITED_NOT_REPLAYED",
    "conditional_exact_critical_radius_for_24_layouts":7,
    "proves_all_156_B6_minima_fail_at_B7":False,
    "new_B7_global_minimum_tag_count":"UNKNOWN"
},sort_keys=True))
