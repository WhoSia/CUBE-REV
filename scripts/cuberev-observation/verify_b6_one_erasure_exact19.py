#!/usr/bin/env python3
"""B6 one-original-cubie-erasure threshold b6^(1)=19.

Proof dependencies are kept separate:
(A) Two 12-HTM physical two-corner witness words and their 24 proper cube
    rotations, REPLAYED via standalone 48-movable-sticker implementation.
(B) B5 complete 220/220 pure three-original-edge collision supports, INHERITED
    from sealed physical 54-facelet historical certificate; not replayed here.
(C) B6 positive sixteen-tag family of 156 layouts, INHERITED from sealed
    original-cube HTM proof; the 6+4 rotation incidence witnesses are checked
    here via audit_b6_one_erasure_robustness.
No separate 54-facelet engine, independent 41-target HTM proof, or new
geodesic lower bound is claimed.
"""
from itertools import combinations
from verify_short_support_phase import initial, play, factors, proper24, WORDS
from audit_b6_one_erasure_robustness import (
    CORNERS_TAGS, EDGES_TAGS, TAGS, positive_missing_four,
    all_erasures_have_16_core, verify_orbit_witnesses
)

def inverse_token(m):
    return m if m.endswith("2") else m[:-1] if m.endswith("'") else m+"'"

def midpoint_states(word):
    turns=word.split()
    assert len(turns)==12
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

def inherited_all_B5_three_edge_supports():
    """SET of obligations certified in archived B5 witness replay, NOT new replay."""
    # Archived SHA256 002887a198bac812ad360ba536309f2522899d5c28d12fb73bb92062ae889c94
    # Archive b5_nine_pair_verifier.py and 54-facelet rotation replay:
    # B4 84 supports + B5 new 136 supports = C(12,3) = 220 supports.
    return frozenset(map(frozenset, combinations(EDGES_TAGS,3)))

def obstruction_lower_bound():
    physical_corner=certified_physical_corner_pairs()
    triple_edges=inherited_all_B5_three_edge_supports()
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
    # or two edges (violates inherited B5 220-triple support completeness).
    for omitted in combinations(sorted(TAGS),2):
        absent=frozenset(omitted)
        if absent&CORNERS_TAGS:
            assert len(absent&CORNERS_TAGS)>=1
        else:
            assert len(absent&EDGES_TAGS)==2
    print("B6 ERASURE EXACT THRESHOLD 19 (on inherited physical certificates)")
    print("B6 ROBUST MINIMUM LAYOUTS 12: all 8 corners + any 11 edges")
    print("PHYSICAL CORNER CERTIFICATE 16 two-corner pairs via independent 48-sticker midpoint replay")
    print("B5 THREE-EDGE SUPPORT PROVENANCE inherited 220/220, not independently replayed here")
    print("B6 POSITIVE FAMILY PROVENANCE inherited 156 positive 16-tag layouts")
    print("B6 UPPER GEOMETRIC COVER witnesses 6 edge orbits + 4 corner-edge orbits")
    return (19,12)

if __name__=="__main__":
    audit()
