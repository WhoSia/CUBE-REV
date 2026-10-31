#!/usr/bin/env python3
"""Derive the 8 optimal B6 rotation types from the intrinsic geometric graph.

Imports verify_b6_geometric_rule.py; uses ONLY elementary geometry, proper
rotations, and Burnside's lemma. No archived 156 success flags are consulted.
"""
from collections import Counter
from verify_b6_geometric_rule import (
    EDGE_NAMES, ENDS, midpoint, valid_pairs, proper_rotations
)

ROT=proper_rotations()
BY_MID={midpoint(e):e for e in EDGE_NAMES}

def classify(h,pair):
    core=ENDS[h]
    opp_corners=frozenset(tuple(-u for u in corner) for corner in core)
    hstar=next(e for e in EDGE_NAMES if ENDS[e]==opp_corners)
    near={e for e in EDGE_NAMES if e!=h and ENDS[e]&core}
    far={e for e in EDGE_NAMES if e!=hstar and ENDS[e]&opp_corners}
    side={e for e in EDGE_NAMES
          if midpoint(e).index(0)==midpoint(h).index(0)
          and e not in (h,hstar)}
    if pair<=near:return "near-cycle"
    if pair<=(far|{hstar}):return "far-wheel"
    if pair==side:return "side-pair"
    raise AssertionError(f"unclassified admissible pair {pair}")

def verify():
    for h in EDGE_NAMES:
        core=ENDS[h]
        stabilizer=[R for R in ROT
                    if frozenset(R(c) for c in core)==core]
        assert len(stabilizer)==2
        pairs=valid_pairs(h)
        frequencies=Counter(classify(h,p) for p in pairs)
        assert frequencies=={"near-cycle":4,"far-wheel":8,"side-pair":1}
        fixed=Counter()
        for p in pairs:
            if all(frozenset(BY_MID[R(midpoint(e))] for e in p)==p
                   for R in stabilizer):
                fixed[classify(h,p)]+=1
        assert fixed=={"near-cycle":2,"side-pair":1},(h,fixed)
        types={name:(amount+fixed[name])//2
               for name,amount in frequencies.items()}
        assert types=={"near-cycle":3,"far-wheel":4,"side-pair":1}
        assert sum(types.values())==8
        assert len(pairs)==13
        assert 12*len(pairs)==5*24+3*12==156
    print("PASS all 12 core edges: stabilizer order2, fixed admissible pairs3")
    print("PASS Burnside orbit types near3 + far4 + side1 = 8")
    print("PASS global orbit-size distribution 5×24 + 3×12 = 156")
    print("LIMIT: requires separate B6 physical proof that the rule is exact")

if __name__=="__main__":verify()
