#!/usr/bin/env python3
"""Exact B6 19-tag backup-core multiplicities under a single lost sensor.

Conditional on the previously certified 156 valid B6 size-16 layouts.
Counts alone are not a new B6-positive physical HTM distance certificate.
"""
from collections import Counter
from b6_independent_48sticker_goals import EDGE_NAMES, CORNERS, EDGE_POSITION, valid_pairs

def endpoints(edge):
    m=EDGE_POSITION[edge]
    return frozenset(c for c in CORNERS if all(c[i]==m[i] for i in range(3) if m[i]))

def audit():
    layouts={(h,pair) for h in EDGE_NAMES for pair in valid_pairs(h)}
    assert len(layouts)==156
    edge_hist=Counter({1:4,2:1,3:4,4:2})
    corner_hist=Counter({4:2,6:4,10:2})
    for omitted_edge in EDGE_NAMES:
        # S has all eight corners and eleven edges, excluding omitted_edge.
        cores={(h,pair) for h,pair in layouts if omitted_edge in pair}
        assert len(cores)==26
        lost_edge={f:sum(pair==frozenset((omitted_edge,f)) for h,pair in cores)
                   for f in EDGE_NAMES if f!=omitted_edge}
        lost_corner={c:sum(c in endpoints(h) for h,pair in cores)
                     for c in CORNERS}
        assert Counter(lost_edge.values())==edge_hist
        assert Counter(lost_corner.values())==corner_hist
        assert min(lost_edge.values())==1
        assert min(lost_corner.values())==4
        # Each 16-tag core has 3 additional sensors in its containing
        # 19-tag design, hence is contained in 3 of the 19 single-erasure
        # post-failure sensor sets. Double count to obtain 3*26=78.
        assert sum(lost_edge.values())==26
        assert sum(lost_corner.values())==52
        assert sum(lost_edge.values())+sum(lost_corner.values())==3*len(cores)==78
    multiplicity=Counter(pair for h,pair in layouts)
    assert len(multiplicity)==66
    assert Counter(multiplicity.values())==Counter({1:24,2:6,3:24,4:12})
    assert all(m>0 for m in multiplicity.values())
    print("PASS 12 robust 19-tag designs each contain 26 B6 16-tag backup cores")
    print("PASS deleted edge: counts 1x4, 2x1, 3x4, 4x2")
    print("PASS deleted corner: counts 4x2, 6x4, 10x2")
    print("PASS 78 deletion-core incidences = 3*26")
    print("PASS all 66 omitted-edge pairs occur; multiplicities 1x24, 2x6, 3x24, 4x12")
    print("LIMIT: inherits physical B6 positivity of 156 geometry-selected layouts")
    return {"cores_per_robust_19":26,"failure_core_incidences":78,
            "edge_failure_multiplicity":dict(edge_hist),
            "corner_failure_multiplicity":dict(corner_hist)}

if __name__=="__main__":
    audit()
