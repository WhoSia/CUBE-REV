#!/usr/bin/env python3
"""B6 one-erasure robustness, conditional on archived 156 positive 16-tag layouts.

No physical HTM shortest-path decision is done here. The positive family is
the independently archived four-case geometry (verify_b6_geometric_rule).
"""
from itertools import combinations
from collections import Counter
from verify_b6_geometric_rule import CORNERS, EDGE_NAMES, ENDS, valid_pairs

CORNERS_TAGS = frozenset(("C", tuple(x)) for x in CORNERS)
EDGES_TAGS = frozenset(("E", x) for x in EDGE_NAMES)
TAGS = CORNERS_TAGS | EDGES_TAGS

def positive_missing_four():
    return frozenset(
        frozenset([* (("C", c) for c in ENDS[h]),
                   * (("E", e) for e in pair)])
        for h in EDGE_NAMES
        for pair in valid_pairs(h)
    )

def is_radius6_valid(observed, positive_missing=None):
    """All 16-tag bases are in the archived certified positive family."""
    positive_missing = positive_missing if positive_missing is not None else positive_missing_four()
    missing = TAGS - frozenset(observed)
    return any(missing <= b for b in positive_missing)

def is_one_erasure_robust(observed, positive_missing=None):
    positive_missing = positive_missing if positive_missing is not None else positive_missing_four()
    return all(is_radius6_valid(frozenset(observed) - {tag}, positive_missing)
               for tag in observed)

def audit():
    family = positive_missing_four()
    assert len(TAGS) == 20 and len(family) == 156
    assert all(len(b) == 4 and len(b & CORNERS_TAGS) == 2
               and len(b & EDGES_TAGS) == 2 for b in family)
    assert all(is_radius6_valid(TAGS-b, family) for b in family)
    # Each two-edge omission extends to some allowed four-tag omission.
    pair_covered = sum(any(frozenset(pair) <= b for b in family)
                       for pair in combinations(EDGES_TAGS, 2))
    assert pair_covered == 66, pair_covered
    # Every (corner, edge) omission also extends to some positive layout.
    mixed_covered = sum(any({c,e} <= b for b in family)
                        for c in CORNERS_TAGS for e in EDGES_TAGS)
    assert mixed_covered == 96, mixed_covered
    counts = {}
    for omitted_n in (0,1,2,3,4):
        by_type=Counter()
        robust_sets=[]
        for missing_tuple in combinations(sorted(TAGS), omitted_n):
            missing=frozenset(missing_tuple)
            obs=TAGS-missing
            if is_one_erasure_robust(obs,family):
                robust_sets.append(missing)
                by_type[(len(missing&CORNERS_TAGS),
                         len(missing&EDGES_TAGS))]+=1
        counts[20-omitted_n]=len(robust_sets)
        if omitted_n==1:
            assert len(robust_sets)==12
            assert all(m <= EDGES_TAGS for m in robust_sets)
        if omitted_n>=2: assert not robust_sets
        print(f"SENSORS {20-omitted_n} ROBUST_LAYOUTS {len(robust_sets)} TYPES {dict(by_type)}")
    assert counts == {20:1,19:12,18:0,17:0,16:0}, counts
    print("B6 SINGLE ERASURE THRESHOLD 19 (CONDITIONAL POSITIVE FAMILY)")
    print("PAIR COVERAGE 66/66; MIXED TAG COVERAGE 96/96")
    return counts

if __name__ == "__main__":
    audit()
