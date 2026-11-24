#!/usr/bin/env python3
"""Independent geometry-level parity regression for CUBE-REV 0.29.

Reimplements the explicit geometric functions in formal/029/FaceTurns.lean
and tests the 12 quarter-turn generators, all 144 ordered two-turn paths,
then 4,096 fixed-seed random longer lookup-order histories. This is a
computational negative control, NOT a Lean proof of all histories.
"""
from __future__ import annotations
from dataclasses import dataclass
import random

EDGE_NAMES = ['DL', 'BL', 'FL', 'UL', 'DB', 'DF', 'UB', 'UF', 'DR', 'BR', 'FR', 'UR']
CORNER_NAMES = ['UFR', 'URB', 'ULF', 'UBL', 'DRF', 'DBR', 'DFL', 'DLB']
TURN_NAMES = ['U', "U'", 'R', "R'", 'F', "F'", 'D', "D'", 'L', "L'", 'B', "B'"]
NORMAL = {'U': (0,1,0),'R':(1,0,0),'F':(0,0,1),'D':(0,-1,0),'L':(-1,0,0),'B':(0,0,-1)}

def add(a,b): return tuple(x+y for x,y in zip(a,b))
def scale(x,a): return tuple(x*y for y in a)
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def rotate(axis,direction,v): return add(scale(direction,cross(axis,v)),scale(dot(v,axis),axis))

slots=[]
for piece in EDGE_NAMES + CORNER_NAMES:
    ds=[NORMAL[c] for c in piece]
    position=(0,0,0)
    for d in ds: position=add(position,d)
    for d in ds: slots.append((position,d))
assert len(slots)==48 and len(set(slots))==48
slot_index={s:i for i,s in enumerate(slots)}

def build_turn_slot(t):
    axis=NORMAL['URFDLB'[t//2]]
    direction=-1 if t%2==0 else 1
    out=[]
    for position,n in slots:
        moved=(rotate(axis,direction,position),rotate(axis,direction,n)) if dot(position,axis)==1 else (position,n)
        out.append(slot_index[moved])
    assert sorted(out)==list(range(48))
    return out
TURN=[build_turn_slot(t) for t in range(12)]


def inversions(xs): return sum(xs[i]>xs[j] for i in range(len(xs)) for j in range(i+1,len(xs)))
def parity(xs): return inversions(xs)%2

def edge_coords(t):
    src=[]; flips=[]
    for i in range(12):
        k=TURN[t][2*i]
        assert 0<=k<24
        source=k//2
        flip=k%2
        assert TURN[t][2*i+1]==2*source+(1-flip)
        src.append(source); flips.append(flip)
    assert sorted(src)==list(range(12))
    return src,flips

def corner_coords(t):
    src=[];twists=[]
    for i in range(8):
        k=TURN[t][24+3*i]
        assert 24<=k<48
        source=(k-24)//3
        shift=(k-24)%3
        for j in range(3):
            assert TURN[t][24+3*i+j] == 24+3*source+(shift+j)%3
        src.append(source);twists.append(shift)
    assert sorted(src)==list(range(8))
    return src,twists

EDGE=[edge_coords(t) for t in range(12)]
CORNER=[corner_coords(t) for t in range(12)]
for t in range(12):
    ep=parity(EDGE[t][0]);cp=parity(CORNER[t][0]);assert ep==cp==1,(t,ep,cp)

# Apply source reindexing in the EXACT recursive lookup order used by
# edgeCoordinatesAlong and coordinatesAlong (tail first, then head).
def arrays_for_path(path):
    e=list(range(12))
    c=list(range(8))
    ef=[0]*12
    ct=[0]*8
    for t in reversed(path):
        ei,flips=EDGE[t]
        ci,twists=CORNER[t]
        e,ef=([e[ei[i]] for i in range(12)],[ef[ei[i]]^flips[i] for i in range(12)])
        c,ct=([c[ci[i]] for i in range(8)],[(ct[ci[i]]+twists[i])%3 for i in range(8)])
    assert sorted(e)==list(range(12))
    assert sorted(c)==list(range(8))
    assert sum(ct)%3==0
    return e,ef,c,ct

def check_path(path):
    e,ef,c,ct=arrays_for_path(path)
    assert parity(e)==parity(c),(path,e,c,parity(e),parity(c))
    # Directly compose turnSlot on all 48 sticker locations, then check
    # that the derived cubie coordinates match the exact original slots.
    def follow(s):
        for t in path: s=TURN[t][s]
        return s
    for i in range(12):
        for j in range(2):
            assert follow(2*i+j)==2*e[i]+(j^ef[i])
    for i in range(8):
        for j in range(3):
            assert follow(24+3*i+j)==24+3*c[i]+(j+ct[i])%3

# Independent adversarial check for the exact two reindex laws needed
# in EdgeCornerParityInduction.lean, restricted to *genuine permutations*.
rng_reindex=random.Random(0x029C0DE)
for t in range(12):
    edge_src=EDGE[t][0]
    corner_src=CORNER[t][0]
    for trial in range(512):
        e=list(range(12)); c=list(range(8))
        rng_reindex.shuffle(e); rng_reindex.shuffle(c)
        assert parity([e[i] for i in edge_src]) == (parity(e)+parity(edge_src))%2
        assert parity([c[i] for i in corner_src]) == (parity(c)+parity(corner_src))%2

check_path([])
for t in range(12): check_path([t])
for t in range(12):
    for u in range(12): check_path([t,u])
rng=random.Random(0xC0BE029)
for k in range(4096):
    length=rng.randrange(3,71)
    path=[rng.randrange(12) for _ in range(length)]
    check_path(path)
print('PASS geometric slot factorization: all 12 turns x 48 stickers')
print('PASS each basic-turn edge/corner permutation parity = odd')
print('PASS 12 x 512 independent edge/corner parity reindex permutation probes')
print('PASS path tests: 1 empty + 12 one-turn + 144 two-turn + 4096 seeded longer histories')
print('PASS full pose composition vs edge/corner coordinate actions on every tested path')
print('CAVEAT computational validation does not prove all turn sequences in Lean')
