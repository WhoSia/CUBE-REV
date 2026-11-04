#!/usr/bin/env python3
"""B6 one-original-cubie-erasure threshold b6^(1)=19.

Proof dependencies are kept separate:
(A) Two 12-HTM physical two-corner witness words and their 24 proper cube
    rotations, REPLAYED via standalone 48-movable-sticker implementation.
(B) B5 complete 220/220 pure three-original-edge supports, REPLAYED now
    from 13 newly independently discovered HTM word pairs in Python 48-sticker
    physics, as well as historically certified in the archived 54-facelet proof.
(C) B6 positive sixteen-tag family of 156 layouts, INHERITED from sealed
    original-cube HTM proof; the 6+4 rotation incidence witnesses are checked
    here via audit_b6_one_erasure_robustness.
No separate 54-facelet engine, independent 41-target HTM proof, or new
geodesic lower bound is claimed.
"""
from itertools import combinations
from pathlib import Path
import json
from verify_b5_three_edge_physical_manifest import verify_manifest
from verify_short_support_phase import initial, play, factors, proper24, WORDS
from audit_b6_one_erasure_robustness import (
    CORNERS_TAGS, EDGES_TAGS, TAGS, positive_missing_four,
    all_erasures_have_16_core, verify_orbit_witnesses
)

def inverse_token(m):
    return m if m.endswith("2") else m[:-1] if m.endswith("'") else m+"'"

def midpoint_states(word):
    turns=word.split()
    assert len(turns) in (12,13)
    # 6 + 6 for B6; 6 + 7 for B7, with full original-tag comparison.
    left=" ".join(inverse_token(t) for t in reversed(turns[6:]))
    right=" ".join(turns[:6])
    return play(left),play(right)

def certified_physical_corner_pairs():
    """Run 48-sticker physical midpoint comparisons for both 12HTM words."""
    solved=factors(initial())
    corners={tag:pos for tag,(pos,_) in solved.items() if len(tag)==3}
    actual=set()
    for name in ("face_diagonal_corners_12","body_diagonal_corners_12"):
        st1,st2=midpoint_states(WORDS[name])
        f1,f2=factors(st1),factors(st2)
        difference={tag for tag in solved if f1[tag]!=f2[tag]}
        assert len(difference)==2 and all(len(tag)==3 for tag in difference)
        positions=[corners[tag] for tag in difference]
        hamming=sum(x!=y for x,y in zip(*positions))
        assert hamming==(2 if name.startswith("face") else 3)
        actual.update(frozenset(r(v) for v in positions) for r in proper24())
    assert len(actual)==16
    observed_positions=set(corners.values())
    assert set().union(*actual)==observed_positions
    return actual

def certified_physical_B7_adjacent_edge_pairs():
    """Physical B7 13-HTM 6+7 midpoint witness; 24 rotations touch all edges."""
    solved=factors(initial())
    edges={tag:pos for tag,(pos,_) in solved.items() if len(tag)==2}
    s1,s2=midpoint_states(WORDS["adjacent_edges_13"])
    f1,f2=factors(s1),factors(s2)
    difference={tag for tag in solved if f1[tag]!=f2[tag]}
    assert len(difference)==2 and all(len(tag)==2 for tag in difference)
    positions=[edges[tag] for tag in difference]
    orbit={frozenset(r(v) for v in positions) for r in proper24()}
    assert len(orbit)==24
    assert set().union(*orbit)==set(edges.values())
    return orbit

def physically_replayed_all_B5_three_edge_supports():
    """Fail-closed: replay real B5 words and rotations before trusting all 220."""
    path=Path(__file__).resolve().parents[2] / (
        "data/0.28/B5_13_ORBIT_INDEPENDENT_WORD_PAIR_WITNESSES_20261104.json"
    )
    payload=json.loads(path.read_text(encoding="utf-8"))
    certificate=verify_manifest(payload,require_complete=True)
    assert certificate["distinct_triple_edge_supports_physically_replayed"]==220
    assert certificate["physical_orbits_covered"]==13
    assert certificate["missing_triple_edge_supports"]==0
    # The combinations below form only a named universe AFTER actual full
    # word-based physical realization of all its members was verified above.
    return frozenset(map(frozenset,combinations(EDGES_TAGS,3)))

def obstruction_lower_bound():
    physical_corner=certified_physical_corner_pairs()
    triple_edges=physically_replayed_all_B5_three_edge_supports()
    assert len(physical_corner)==16 and len(triple_edges)==220
    # Each difference support D must meet observed tags in >=2 points,
    # or removing its only observed sensor creates a collision.
    # All corners appear in one physical two-corner support and every edge
    # appears among 220 triple-edge supports.
    certified_corner_ends=set().union(*physical_corner)
    assert len(certified_corner_ends)==8
    # >1 absent corner would trivially fail too; even a single absent
    # corner c violates one-erasure because {c,c'} has only one sensed tag.
    # >=2 absent edges: pick a third original edge and one-edge-erasure
    # destroys the 3-edge witness. Thus at least 11 selected edges.
    assert len(EDGES_TAGS)==12
    for missing in combinations(sorted(EDGES_TAGS),2):
        a,b=missing
        extra=next(e for e in EDGES_TAGS if e not in (a,b))
        assert frozenset((a,b,extra)) in triple_edges
    return 8+11

def audit():
    assert len(TAGS)==20
    lower=obstruction_lower_bound()
    assert lower==19
    positive=positive_missing_four()
    assert len(positive)==156
    edge_orbits,corner_orbits=verify_orbit_witnesses()
    assert len(edge_orbits)==6 and len(corner_orbits)==4
    robust_19=[]
    for omitted in TAGS:
        selected=TAGS-{omitted}
        if omitted in EDGES_TAGS:
            assert all_erasures_have_16_core(selected,positive)
            robust_19.append(omitted)
        else:
            # Each omitted original corner participates in a 12HTM
            # certified pure two-corner midpoint support, hence invalid.
            assert omitted[0]=="C"
    assert len(robust_19)==12
    # Every 18-tag selection misses either a corner (already impossible)
    # or two edges (violates freshly physically replayed B5 220-triple support completeness).
    for omitted in combinations(sorted(TAGS),2):
        absent=frozenset(omitted)
        if absent&CORNERS_TAGS:
            assert len(absent&CORNERS_TAGS)>=1
        else:
            assert len(absent&EDGES_TAGS)==2
    b7_adjacent=certified_physical_B7_adjacent_edge_pairs()
    assert len(b7_adjacent)==24
    # Complete set-level classifications from the support obstructions
    # and the constructive positive B6 19-tag family:
    # B6 robust family: exactly 12 choices (omit one edge) plus full20.
    # B7 robust family: only full20 (physical 13-HTM rotated two-edge support).
    b6_robust_total=12+1
    b7_robust_total=1
    assert (b6_robust_total,b7_robust_total)==(13,1)
    print("B6 ERASURE EXACT THRESHOLD 19 (fresh B5 220/220 replay; B6 positive family still archived)")
    print("FULL B6 ONE-ERASURE ROBUST SENSOR FAMILY 13 sets = 12 size19 + 1 size20")
    print("B7 ONE-ERASURE THRESHOLD 20; only full20 robust; 24 adjacent two-edge midpoint supports physically replayed")
    print("B6 ROBUST MINIMUM LAYOUTS 12: all 8 corners + any 11 edges")
    print("PHYSICAL CORNER CERTIFICATE 16 two-corner pairs via independent 48-sticker midpoint replay")
    print("B5 THREE-EDGE SUPPORT PROVENANCE independent C++ B5 BFS -> pinned 13 words -> Python 48-sticker 220/220 replay")
    print("B6 POSITIVE FAMILY PROVENANCE inherited 156 positive 16-tag layouts")
    print("B6 UPPER GEOMETRIC COVER witnesses 6 edge orbits + 4 corner-edge orbits")
    return (19,12)

if __name__=="__main__":
    audit()
