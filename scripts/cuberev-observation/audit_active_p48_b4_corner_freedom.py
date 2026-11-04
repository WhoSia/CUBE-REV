#!/usr/bin/env python3
"""B4 four-edge obstruction and all-or-none corner freedom in full P48 physics.

The historical 2856 minimum bases are NOT imported. Independently builds
all 46741 B4 states and replays one actual <=4/<=4 HTM word-pair seed.
"""
from collections import Counter,defaultdict
from itertools import combinations
from b6_independent_48sticker_goals import EDGE_POS
from audit_active_p48_b4_nonadaptive_horizon import (
    b4_factors,triples,candidates,injective
)
from verify_b6_complete_4845_p48 import physical_orbit

WITNESS=("F2 R2 F2 U2","R2 F2 R2 U2")

def audit():
    t=triples()
    four=physical_orbit(*WITNESS,4)
    assert len(four)==12 and all(len(s)==4 and set(s)<=set(EDGE_POS) for s in four)
    rows=b4_factors()
    edge8=candidates(8,t)
    assert len(edge8)==114
    rejected=set()
    histogram=Counter()
    for selected in edge8:
        omitted=frozenset(EDGE_POS[i] for i in range(12) if i not in selected)
        if not injective(rows,selected+tuple(range(12,20))):
            rejected.add(omitted)
            histogram[0]+=1
            continue
        groups=defaultdict(list)
        for row in rows:
            groups[tuple(row[i] for i in selected)].append(row[12:])
        min_corner=8
        for values in groups.values():
            if len(values)<2:continue
            for a,b in combinations(values,2):
                changed=sum(x!=y for x,y in zip(a,b))
                min_corner=min(min_corner,changed)
        if min_corner<3:
            raise AssertionError("corner-subset invariance fails in B4")
        histogram[28]+=1
    assert rejected==four
    assert histogram==Counter({0:12,28:102}),histogram
    assert sum(count*number for count,number in histogram.items())==2856
    print("ACTIVE_B4_FOUR_EDGE_PHYSICAL_ORBIT_12_PASS")
    print("ACTIVE_B4_102_EDGE_CORES_X_28_CORNER_CHOICES_2856_PASS")
    print("ACTIVE_B4_CORNER_CHOICE_ALL_OR_NONE_PASS",dict(histogram))
    print("BOUNDARY relies on complete full-P48 B4 finite enumeration; not universal group law")
    return histogram

if __name__=="__main__":audit()
