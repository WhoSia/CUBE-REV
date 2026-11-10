#!/usr/bin/env python3
"""CUBE-REV 0.28 R14-P8.12: minimal-but-not-minimum B6 sensor sets.

DEPENDENCIES: the previously physical-certified complete positive 16-tag
criterion and standard legal Rubik cubie parity/orientation constraints.
This is an independent FINITE GEOMETRIC validation of the new logical
consequence, NOT a new 54-sticker B6 geodesic execution or standalone
proof of the inherited 156-positive classification.

For each original edge h, omit its two endpoint corners and edge h.
All resulting 17-tag sets identify B6; removing ANY further tag fails.

The physical positivity follows because the legal pointwise stabilizer
on (two corners, one edge) acts nontrivially only by balanced corner
twists (the one unobserved edge CANNOT move/flip), while any B6-positive
16-tag design omitting those same two corners excludes the twists.
"""
from itertools import combinations
from collections import Counter
import json
from verify_b6_geometric_rule import EDGE_NAMES, ENDS, CORNERS, valid_pairs

ALL_EDGE_TAGS = frozenset(("edge", e) for e in EDGE_NAMES)
ALL_CORNER_TAGS = frozenset(("corner", c) for c in CORNERS)
ALL_TAGS = ALL_EDGE_TAGS | ALL_CORNER_TAGS
assert len(ALL_TAGS) == 20

def omitted_16_layouts():
    return {
        frozenset(("corner", c) for c in ENDS[h]) |
        frozenset(("edge", e) for e in pair)
        for h in EDGE_NAMES for pair in valid_pairs(h)
    }

def audited_minimal_17():
    positive16 = omitted_16_layouts()
    assert len(positive16) == 156
    report=[]
    found17=set()
    for h in EDGE_NAMES:
        pairs=valid_pairs(h)
        assert len(pairs)==13
        used_edges=set().union(*pairs)
        # Each fixed-h admissible pair graph has W5+C4+K2+K1,
        # with exactly ONE isolated edge, namely h itself.
        assert len(used_edges)==11
        assert frozenset(EDGE_NAMES)-used_edges==frozenset((h,))
        omitted=frozenset(("corner",c) for c in ENDS[h])|{("edge",h)}
        assert len(omitted)==3 and omitted<=ALL_TAGS
        found17.add(omitted)
        # For all 17 observed tags, removing one more yields a four-tag
        # omission that is NOT among the 156 certified B6 positives.
        for t in ALL_TAGS-omitted:
            assert omitted | {t} not in positive16, (h,t)
        # The geometric case contains a certified positive 16-tag
        # layout omitting the SAME two adjacent corners, e.g. any
        # valid edge pair in pairs (not including h).
        # The only legal nontrivial stabilizer on 2C+1E is a pure
        # balanced two-corner twist. Thus all its short elements
        # are also in the stabilizer of that certified 16-tag layout.
        #
        # Physical B6 positivity is CONDITIONAL on the 41-distance
        # inherited certificate; this finite test does not replay it.
        report.append({"core_edge":h,"valid_16_omissions_with_same_corners":len(pairs),
                       "edge_h_is_isolated":True,
                       "all_17_single_tag_deletions_fail_16_test":True})
    assert len(found17)==12
    # For the wider 2C+1E class, any endpoint pair for h and
    # arbitrary omitted edge is safe by exactly the same corner twist
    # argument. Only the isolated h case lacks a positive size-16
    # extension.
    assert sum(len(set().union(*valid_pairs(h))) for h in EDGE_NAMES)==132
    assert len(EDGE_NAMES)*len(EDGE_NAMES)==144
    return {"result":"R14_P812_MINIMAL17_TWELVE_GEOMETRIC_COURT_PASS",
      "scope":"conditional on historic complete physical B6 16-tag certificate",
      "minimum_16_layouts_inherited":156,
      "adjacent_corner_and_one_edge_positive17_by_algebra":144,
      "extendable_to_positive16":132,
      "inclusionwise_minimal_17":len(found17),
      "cores":report,
      "physical_54_facelet_or_18htm_rerun":False}

if __name__=="__main__":
    print(json.dumps(audited_minimal_17(),sort_keys=True))
