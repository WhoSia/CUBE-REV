#!/usr/bin/env python3
"""Exact nonadaptive B4 two-fixed-slot horizon in independent P48 physics.

Every frame reports incoming original identity+full orientation for one
edge site and one corner site. This verifies the 46741-state full B4 ball,
all 84 actual B4 three-edge collisions and all surviving 6/7/8-frame
site sets, with no historical B4 verdict lookup.
"""
import json
from pathlib import Path
from itertools import combinations
from b6_independent_48sticker_goals import (
    MOVES, EDGE_POS, compose, inverse, factor_state,
)
from verify_b6_complete_4845_p48 import physical_orbit

def triples():
    path=Path(__file__).resolve().parents[2]/"data/0.28/B5_13_ORBIT_INDEPENDENT_WORD_PAIR_WITNESSES_20261104.json"
    manifest=json.loads(path.read_text(encoding="utf8"))
    out=set()
    for w in manifest["witnesses"]:
        if max(len(w["left"].split()),len(w["right"].split()))<=4:
            orbit=physical_orbit(w["left"],w["right"],4)
            assert all(len(s)==3 and set(s)<=set(EDGE_POS) for s in orbit)
            out.update(frozenset(EDGE_POS.index(p) for p in s) for s in orbit)
    assert len(out)==84
    return out

def b4_factors():
    eye=bytes(range(48));seen={eye};layer={eye};sizes=[1]
    for _ in range(4):
        next_states={compose(turn,s) for s in layer for turn in MOVES.values()}
        layer=next_states-seen
        seen.update(layer)
        sizes.append(len(layer))
    assert sizes==[1,18,243,3240,43239],sizes
    return tuple(factor_state(inverse(s)) for s in sorted(seen))

def injective(factors,selected):
    seen=set()
    for f in factors:
        signature=tuple(f[i] for i in selected)
        if signature in seen:return False
        seen.add(signature)
    return True

def candidates(k,triangles):
    return [e for e in combinations(range(12),k)
            if not any(t<=set(range(12))-set(e) for t in triangles)]

def audit():
    t=triples()
    six=candidates(6,t);seven=candidates(7,t);eight=candidates(8,t)
    assert (len(six),len(seven),len(eight))==(8,48,114)
    states=b4_factors()
    n6=sum(injective(states,e+tuple(12+c for c in co))
           for e in six for co in combinations(range(8),6))
    n7=sum(injective(states,e+tuple(12+c for c in co))
           for e in seven for co in combinations(range(8),7))
    positive8=[e for e in eight if injective(states,e+tuple(range(12,20)))]
    assert len(states)==46741
    assert n6==n7==0 and len(positive8)==102
    print("ACTIVE_B4_P48_FULL_STATES",len(states))
    print("ACTIVE_B4_EDGE_TRIPLE_PHYSICAL_SUPPORTS",len(t))
    print("ACTIVE_B4_SIX_FRAMES_ALL_224_REPLAYED_FAIL")
    print("ACTIVE_B4_SEVEN_FRAMES_ALL_384_REPLAYED_FAIL")
    print("ACTIVE_B4_EIGHT_FRAMES_102_POSITIVE_OF_114_CANDIDATES")
    print("ACTIVE_B4_NONADAPTIVE_HORIZON_EXACT_8")
    print("ACTIVE_B4_EIGHT_FRAME_WITNESS_EDGE_INDICES",positive8[0])
    print("BOUNDARY adaptive B4 horizon and global HTM movement-cost optimum OPEN")
    return {"states":len(states),"triple_supports":len(t),"six_remaining":len(six),
            "seven_remaining":len(seven),"eight_remaining":len(eight),
            "eight_valid":len(positive8),"witness":positive8[0]}

if __name__=="__main__":audit()
