#!/usr/bin/env python3
"""B6 one-erasure SUFFICIENT certificate via archived 16-tag positive cores.

CRITICAL: A valid 17-, 18- or 19-tag sensor set need NOT contain a
valid 16-tag subset. Therefore lack of a 16-core is NOT an invalidity
certificate for larger selected sensor sets. This auditor only proves
constructive upper bounds (plus the exactly-classified 17-tag robust
impossibility via all 16-tag erasures).
"""
from itertools import combinations
from collections import Counter
from verify_b6_geometric_rule import CORNERS, EDGE_NAMES, ENDS, valid_pairs

CORNERS_TAGS = frozenset(("C", tuple(x)) for x in CORNERS)
EDGES_TAGS = frozenset(("E", x) for x in EDGE_NAMES)
TAGS = CORNERS_TAGS | EDGES_TAGS

def positive_missing_four():
    return frozenset(
        frozenset([*(("C", c) for c in ENDS[h]),
                   *(("E", e) for e in pair)])
        for h in EDGE_NAMES for pair in valid_pairs(h)
    )

def has_certified_16_core(observed, positive_missing=None):
    """Sufficient for B6 validity, necessary only when |observed|=16."""
    positive_missing = positive_missing if positive_missing is not None else positive_missing_four()
    missing = TAGS - frozenset(observed)
    return any(missing <= b for b in positive_missing)

def all_erasures_have_16_core(observed, positive_missing=None):
    """Sufficient to be B6 one-erasure robust; NOT necessary for |S|>=18."""
    positive_missing = positive_missing if positive_missing is not None else positive_missing_four()
    return all(has_certified_16_core(frozenset(observed)-{tag}, positive_missing)
               for tag in observed)

def audit():
    family = positive_missing_four()
    assert len(TAGS)==20 and len(family)==156
    assert all(len(b)==4 and len(b&CORNERS_TAGS)==2
               and len(b&EDGES_TAGS)==2 for b in family)
    assert all(has_certified_16_core(TAGS-b,family) for b in family)
    pair_covered=sum(any(frozenset(p)<=b for b in family)
                     for p in combinations(EDGES_TAGS,2))
    mixed_covered=sum(any({c,e}<=b for b in family)
                      for c in CORNERS_TAGS for e in EDGES_TAGS)
    assert (pair_covered,mixed_covered)==(66,96)
    counts={}
    for k in (16,17,18,19,20):
        sufficient_sets=[]
        for absent in combinations(sorted(TAGS),20-k):
            missing=frozenset(absent)
            if all_erasures_have_16_core(TAGS-missing,family):
                sufficient_sets.append(missing)
        counts[k]=len(sufficient_sets)
        print("SENSORS",k,"ONE_ERASURE_CERTIFIED_VIA_16_CORE",len(sufficient_sets))
        if k==19:
            assert len(sufficient_sets)==12
            assert all(m<=EDGES_TAGS for m in sufficient_sets)
        if k==17: assert not sufficient_sets
    assert counts=={16:0,17:0,18:0,19:12,20:1},counts
    print("PROVEN: 17 TAGS CANNOT TOLERATE ONE ERASURE (all resulting 16s classified)")
    print("PROVEN: 12 CONSTRUCTIVE 19-TAG SINGLE-ERASURE DESIGNS; b6^(1) <= 19")
    print("OPEN: actual existence of robust 18-tag designs; 18 no-16-core is INCONCLUSIVE")
    print("66/66 EDGE-PAIR and 96/96 CORNER-EDGE extension coverage")
    return counts

if __name__=="__main__":
    audit()
