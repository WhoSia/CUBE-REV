#!/usr/bin/env python3
"""Geometry-independent cubie action semantics regression for Lean bridge.

Finitely checks 12×8×24 single-corner actions, then composes legal 48-sticker
permutations on reproducible turn words and compares all 24 corner colors to
the abstract corner coordinate action. Not a substitute for Lean compilation.
"""
import hashlib
import json
import sys
from pathlib import Path
from random import Random

ROOT = Path(__file__).resolve().parent
# Prefer the tracked GitHub source layout. ZIP snapshots may have a reproduction/
# copy, but that copy is not present in a clean repository checkout.
REPO = ROOT.parents[1]
SOURCE_ROOTS = (REPO / 'scripts' / 'cuberev-observation', REPO / 'reproduction')
SOURCE = next((folder for folder in SOURCE_ROOTS
               if (folder / 'audit_r029_w_corner_geometric_decoder.py').is_file()
               and (folder / 'audit_r029_w_transport_all_prefixes.py').is_file()), None)
if SOURCE is None:
    raise FileNotFoundError('Missing tracked corner geometry and permutation audit helpers')
sys.path.insert(0, str(SOURCE))
from audit_r029_w_corner_geometric_decoder import geometry, CORNERS, EDGES


def verify():
    moves=geometry()
    solved=tuple(''.join(EDGES+CORNERS))
    assert len(solved)==48
    tables=[]
    local=0
    for move in moves:
        src=[];off=[]
        for i in range(8):
            ss=[move[24+3*i+j]-24 for j in range(3)]
            q,shift=divmod(ss[0],3)
            assert ss==[3*q+(shift+j)%3 for j in range(3)]
            src.append(q);off.append(shift)
            for p in range(8):
                for twist in range(3):
                    color=CORNERS[p][twist:]+CORNERS[p][:twist]
                    observed=''.join(color[ss[j]%3] for j in range(3))
                    final=(twist+shift)%3
                    transformed=CORNERS[p][final:]+CORNERS[p][:final]
                    assert observed==transformed
                    local+=1
        tables.append((src,off))
    assert local==12*8*24
    rng=Random(0x20261121029)
    total=0
    scrambles=1500
    for _ in range(scrambles):
        physical=solved
        coords=[(i,0) for i in range(8)]
        for _ in range(rng.randrange(1,121)):
            t=rng.randrange(12)
            physical=tuple(physical[j] for j in moves[t])
            src,off=tables[t]
            coords=[(coords[src[i]][0],(coords[src[i]][1]+off[i])%3)
                     for i in range(8)]
            assert sorted(p for p,_ in coords)==list(range(8))
            assert sum(twist for _,twist in coords)%3==0
            for i,(piece,twist) in enumerate(coords):
                expected=CORNERS[piece][twist:]+CORNERS[piece][:twist]
                assert ''.join(physical[24+3*i:24+3*i+3])==expected
                total+=3
    src=ROOT/'ReachableCornerCoordinates.lean'
    assert b'reachable_has_oriented_corners' in src.read_bytes()
    return {'status':'PASS','source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),
            'finite_single_corner_actions':local,'physical_legal_turn_scrambles':scrambles,
            'composed_corner_sticker_checks':total,
            'scope':'Finite semantics cross-check only; full Lean compiler pass pending'}

if __name__=='__main__':
    print(json.dumps(verify(),indent=2))
