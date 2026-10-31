#!/usr/bin/env python3
"""B7 full cubie-factor obstruction certificate using independent 48-sticker physics.

Requires sibling verify_short_support_phase.py. The finite physical witnesses are
upper bounds only; no complete B7 BFS, no HTM optimality, no dynamic sensor costs.
"""
from itertools import combinations
from verify_short_support_phase import initial, play, factors, proper24

WORDS = {
 "C_face12": "U2 R' B D2 B' R U2 R' B D2 B' R",
 "C_body12": "U' B2 U L' F2 L U' B2 U L' F2 L",
 "C_adjacent14": "R' D R F D F' U' F D' F' R' D' R U",
 "E_adjacent13a": "L F R' F' L' U2 R U R U' R2 U2 R",
 "E_adjacent13b": "U F U F2 D' L' U' L U D F2 U2 F'",
 "E_adjacent13c": "F R' F' L' U2 R U R U' R2 U2 R L",
 "E_parallel_opposite14": "F R' D' L' D R L F2 L2 F' L F L F",
 "E_parallel_sameface14": "U' F R' U F' R L' U B' R U' B R' L",
}

def inverse(moves):
    return [(m[:-1] if m.endswith("'") else m if m.endswith("2") else m+"'")
            for m in reversed(moves)]

def diff(s,t):
    a,b=factors(s),factors(t)
    return frozenset(tag for tag in a if a[tag]!=b[tag])

base=factors(initial())
assert len(base)==20
pos={tag:v[0] for tag,v in base.items()}
rotations=proper24()

def orbit(tags):
    return {frozenset(R(pos[t]) for t in tags) for R in rotations}

C=set()
E=set()
for name,word in WORDS.items():
    moves=word.split()
    L=len(moves)
    assert L<=14
    endpoint=diff(initial(),play(word))
    assert len(endpoint)==2
    wanted=3 if name.startswith("C") else 2
    assert all(len(tag)==wanted for tag in endpoint),name

    # Both endpoints are inside B7. Check both midpoint conventions:
    # the original tag labels need NOT agree under left/right transport.
    for cut in range(max(0,L-7),min(7,L)+1):
        prefix,suffix=moves[:cut],moves[cut:]
        d1=diff(play(" ".join(inverse(suffix))),play(" ".join(prefix)))
        d2=diff(play(" ".join(inverse(prefix))),play(" ".join(suffix)))
        assert d1==endpoint,(name,cut)
        for d in (d1,d2):
            assert len(d)==2 and all(len(tag)==wanted for tag in d)
            (C if wanted==3 else E).update(orbit(d))
    print(name,"HTM",L,"physical endpoints PASS")

allC={frozenset(pair) for pair in combinations((pos[t] for t in base if len(t)==3),2)}
allE={frozenset(pair) for pair in combinations((pos[t] for t in base if len(t)==2),2)}
assert C==allC,(len(C),len(allC))
assert E==allE,(len(E),len(allE),allE-E)
assert len(C)==28 and len(E)==66
print("PASS B7 supports: 28/28 two-corner and 66/66 two-edge pairs")
print("PASS 94 minimal support masks; every larger legal support contains a pair")
print("NOT a complete B7 census; physical cubie factors, not orientation-only readout")
