#!/usr/bin/env python3
"""Check 14-sticker corner reconstruction against geometric quarter-turns.

Independent Python transcription of the 48-slot geometry in FaceTurns.lean.
Tests both side choices of every face and reproducible random legal turn words.
Does not claim a Lean-level theorem.
"""
from itertools import product
from random import Random
import json

COLORS = 'URFDLB'
EDGES = ('DL', 'BL', 'FL', 'UL', 'DB', 'DF', 'UB', 'UF', 'DR', 'BR', 'FR', 'UR')
CORNERS = ('UFR', 'URB', 'ULF', 'UBL', 'DRF', 'DBR', 'DFL', 'DLB')
NORMAL = dict(U=(0,1,0), D=(0,-1,0), R=(1,0,0), L=(-1,0,0), F=(0,0,1), B=(0,0,-1))


def add(a, b): return tuple(x+y for x,y in zip(a,b))
def scale(m, a): return tuple(m*x for x in a)
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def cross(a,b):
    return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def rotate(axis,sgn,v): return add(scale(sgn,cross(axis,v)),scale(dot(v,axis),axis))


def geometry():
    slots=[]
    for name in EDGES + CORNERS:
        normals = tuple(NORMAL[c] for c in name)
        location = (sum(v[0] for v in normals),sum(v[1] for v in normals),sum(v[2] for v in normals))
        for direction in normals:slots.append((location, direction))
    assert len(slots)==48 and len(set(slots))==48
    index={v:i for i,v in enumerate(slots)}
    result=[]
    for t in range(12):
        face=COLORS[t//2]
        axis=NORMAL[face]
        sign=-1 if t%2==0 else 1
        perm=[]
        for p,n in slots:
            q=(rotate(axis,sign,p),rotate(axis,sign,n)) if dot(p,axis)==1 else (p,n)
            perm.append(index[q])
        assert sorted(perm)==list(range(48))
        result.append(perm)
    return result


def paint(colors, turn):
    return tuple(colors[i] for i in turn)


def decode_14(state):
    """Read two ordered colors at corner positions 0..6; derive eighth twist."""
    used=[]
    twists=[]
    lookup={}
    for cubie in CORNERS:
        for twist in range(3):
            rotated=cubie[twist:]+cubie[:twist]
            key=rotated[:2]
            assert key not in lookup
            lookup[key]=(cubie,twist,rotated)
    for i in range(7):
        a,b=state[24+3*i:24+3*i+2]
        cubie,twist,rotated=lookup[a+b]
        assert state[24+3*i:24+3*i+3]==tuple(rotated)
        assert cubie not in used
        used.append(cubie)
        twists.append(twist)
    (last,)=set(CORNERS)-set(used)
    final=(-sum(twists))%3
    reconstructed=tuple(''.join(c[t:]+c[:t] for c,t in zip(used+[last], twists+[final])))
    return reconstructed,tuple(used+[last]),tuple(twists+[final])


def check():
    moves=geometry()
    original=tuple(''.join(EDGES+CORNERS))
    assert len(original)==48
    conditions=0
    for i,t in enumerate(moves):
        state=paint(original,t)
        decoded,pieces,twists=decode_14(state)
        assert decoded==state[24:], (i, decoded, state[24:])
        assert sum(twists)%3==0
        conditions+=1
    random=Random(0xC0BE029)
    history=[]
    state=original
    for i in range(3000):
        t=random.randrange(12)
        history.append(t)
        state=paint(state,moves[t])
        decoded,pieces,twists=decode_14(state)
        assert decoded==state[24:]
        assert sum(twists)%3==0
        assert len(set(pieces))==8
        conditions+=1
    return {'status':'PASS','single_face_turns':12,'random_legal_turns':3000,
            'decoded_full_corner_states':conditions,
            'basis':'two cyclically ordered colors at seven corner positions plus final twist constraint',
            'scope':'independent geometry regression, not exhaustive over 8!·3^7 states'}

if __name__=='__main__':
    print(json.dumps(check(),indent=2))
