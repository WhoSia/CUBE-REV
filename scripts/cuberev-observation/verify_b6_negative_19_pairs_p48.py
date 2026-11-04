#!/usr/bin/env python3
"""Replay 19 historical B6-negative word-pair seeds in independent P48 physics.

The words are inherited historical candidate witnesses, but their endpoints,
full original-cubie differences, and all spatial transport checks are
RECOMPUTED from independently constructed 48 labelled moving stickers.
No archived 54-facelet engine, B5 ZIP or B6 success-mask oracle is imported.
This is not independently exhaustive over every possible negative B6 base.
"""
from collections import Counter
from b6_independent_48sticker_goals import (
    EDGE_POS, CORNERS, EDGE_NAMES, EDGE_POSITION, FACES, SPATIAL,
    word, factor_state, valid_pairs
)

SEEDS = {
 0:("L2 U2 B L' B' U2","L2 F R' F R F2"),
 2:("U R2 F' U F R2","U B' D B' D' B2"),
 3:("U2 R2 F' U F R2","U2 B' D B' D' B2"),
 4:("F2 R2 U2 B U B'","F2 D' F' D R2 U'"),
 7:("D L U2 R' F R","D B L' B' L2 U2"),
 8:("U' R2 B U' B' R2","U' F D' F D F2"),
 9:("U R2 B U' B' R2","U F D' F D F2"),
 10:("R2 F2 U L' U' F2","R2 D R' D R D2"),
 11:("U' F' D2 B R' B'","U' L' F L F2 D2"),
 12:("B2 U' B U' B' U2","B2 R2 D' F D R2"),
 13:("R L2 F U' F U","R B D' B' L2 F2"),
 14:("U' F' D F' D' F2","U' L2 B' U B L2"),
 16:("F L U' L U L2","F B2 R D' R' B2"),
 17:("U D B D' B R2","U B2 R2 F' U' F"),
 21:("R F' D F L2 B2","R L2 B' U B' U'"),
 22:("D' R D' R D R2","D' B2 L U' L' B2"),
 23:("F U' F U' F' U2","F L2 D' B D L2"),
 24:("R D' L B2 R' U","R L' D' L2 B2 R'"),
 26:("U R' B R' B' R2","U D2 L' F L D2")
}
NORMAL_TO_FACE={v:k for k,v in FACES.items()}
EDGE_NAME_BY_POSITION={v:k for k,v in EDGE_POSITION.items()}
PIECES=EDGE_POS+CORNERS

def physical_support(a,b):
    x,y=factor_state(word(a)),factor_state(word(b))
    assert len(x)==len(y)==20
    return frozenset(PIECES[i] for i in range(20) if x[i]!=y[i])

def transform_word(s,det,R):
    result=[]
    for token in s.split():
        suffix=token[1:]
        if det<0 and suffix!="2":
            suffix="" if suffix=="'" else "'"
        result.append(NORMAL_TO_FACE[R(FACES[token[0]])]+suffix)
    return " ".join(result)

def physical_orbit(a,b):
    base=physical_support(a,b)
    if len(base)!=4 or len(base&CORNERS)!=2 or len(base&EDGE_POS)!=2:
        raise AssertionError("not a four-tag two-corner/two-edge collision")
    proper=set()
    for det,p,R in SPATIAL:
        replay=physical_support(transform_word(a,det,R),
                                transform_word(b,det,R))
        predicted=frozenset(R(pos) for pos in base)
        if replay!=predicted:
            raise AssertionError("P48 spatial word transport failed")
        if det==1:proper.add(replay)
    return frozenset(proper)

def core_edge_of(corners):
    matches=[]
    for h in EDGE_NAMES:
        midpoint=EDGE_POSITION[h]
        ends=frozenset(c for c in CORNERS
                       if all(c[i]==midpoint[i] for i in range(3) if midpoint[i]))
        if ends==corners:matches.append(h)
    if len(matches)!=1:raise AssertionError("non-adjacent corner omission")
    return matches[0]

def audit():
    assert len(SEEDS)==19
    supports=set()
    orbit_sizes=[]
    for seed_id,(a,b) in SEEDS.items():
        if len(a.split())>6 or len(b.split())>6:
            raise AssertionError("B6 half-word longer than 6")
        orbit=physical_orbit(a,b)
        if orbit&supports:raise AssertionError("duplicate proper rotation orbit")
        supports.update(orbit)
        orbit_sizes.append(len(orbit))
    assert len(supports)==420, (len(supports),orbit_sizes)
    by_core=Counter()
    for support in supports:
        corners=frozenset(p for p in support if p in CORNERS)
        edges=frozenset(EDGE_NAME_BY_POSITION[p] for p in support if p in EDGE_POS)
        assert len(corners)==len(edges)==2
        core=core_edge_of(corners)
        assert edges not in valid_pairs(core), (core,edges)
        by_core[core]+=1
    assert len(by_core)==12 and set(by_core.values())=={35}
    assert sum(by_core.values())==420
    print("PASS independent P48 physical replay of 19 inherited B6 witness word pairs")
    print("PASS 19 disjoint proper-24 orbits with every signed-48 word replay checked")
    print("PASS 420 distinct four-cubie collision supports; 35 per omitted-corner edge")
    print("PASS zero overlap with 156 independently P48-positive geometric layouts")
    print("LIMIT B5 360 prior failure masks and global B6 negative completeness are separate")
    return {"seeds":19,"proper_orbits":19,"supports":420,
            "per_core":dict(sorted(by_core.items())),
            "orbit_sizes":sorted(orbit_sizes)}

if __name__=="__main__":
    audit()
