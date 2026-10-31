#!/usr/bin/env python3
"""Partition all 66 omitted-edge pairs at fixed omitted adjacent corners.

Usage: python verify_b6_obstruction_filtration.py ARCHIVED_B1_B5.zip
Replays the 19 actual B6 physical witness pairs via the sibling bridge, not
by reading hardcoded B6 successful mask IDs. It classifies B5-failed, B6-new
physical failures, and 13 not excluded (positive sufficiency is from earlier
B6 full-state census, NOT this checker).
"""
from collections import Counter
from itertools import combinations
from verify_b6_geometric_bridge import (
    EDGE_NAMES, ENDS, b5_eligible, physical_obstructions, full,
    scope
)
N=scope["N"]
def midpoint(e):
    return tuple(N[e[0]][i]+N[e[1]][i] for i in range(3))

expected={
"h-N":(4,0,0),"h-P":(2,0,0),"h-F":(4,0,0),"h-h*":(0,1,0),
"N-N":(0,2,4),"N-P":(4,4,0),"N-F":(0,16,0),"N-h*":(4,0,0),
"P-P":(0,0,1),"P-F":(0,8,0),"P-h*":(0,2,0),
"F-F":(0,2,4),"F-h*":(0,0,4)
}
order=("h","N","P","F","h*")

for h in EDGE_NAMES:
    core=ENDS[h]
    opposite=frozenset(tuple(-x for x in p) for p in core)
    star=next(e for e in EDGE_NAMES if ENDS[e]==opposite)
    near={e for e in EDGE_NAMES if e!=h and ENDS[e]&core}
    far={e for e in EDGE_NAMES if e!=star and ENDS[e]&opposite}
    parallel={e for e in EDGE_NAMES
              if midpoint(e).index(0)==midpoint(h).index(0)
              and e not in (h,star)}
    groups={"h":{h},"N":near,"P":parallel,"F":far,"h*":{star}}
    assert tuple(map(len,groups.values()))==(1,4,2,4,1)
    assert set().union(*groups.values())==set(EDGE_NAMES)
    corner_bits=sum(1<<(12+scope["corner_xyz"].index(c))
                    for c in core)
    counts=Counter()
    for e,f in combinations(EDGE_NAMES,2):
        edge_bits=(1<<EDGE_NAMES.index(e))|(1<<EDGE_NAMES.index(f))
        omitted=corner_bits|edge_bits
        selected=full^omitted
        if selected not in b5_eligible: grade=0
        elif omitted in physical_obstructions: grade=1
        else: grade=2
        a=next(k for k,s in groups.items() if e in s)
        b=next(k for k,s in groups.items() if f in s)
        if order.index(a)>order.index(b):a,b=b,a
        counts[(a+"-"+b,grade)]+=1
    assert {(pair,tuple(counts[(pair,i)] for i in range(3)))
            for pair in expected} == set(expected.items())
    assert tuple(sum(counts[(part,i)] for part in expected)
                 for i in range(3))==(18,35,13)
print("PASS all 12 core edges, 66 pair labels each, no success-ID oracle")
print("PASS filtration 18 previously B5-failed | 35 new B6 witnesses | 13 unexcluded")
for pair,grades in expected.items():
    print(f"{pair:5} B5bad={grades[0]:2} B6-new={grades[1]:2} survive={grades[2]:2}")
print("BOUNDARY: surviving 13 pairs are known B6-positive only via prior positive census")
