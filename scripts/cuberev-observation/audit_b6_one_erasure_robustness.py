#!/usr/bin/env python3
"""B6 one-erasure SUFFICIENT certificate via archived 16-tag positive cores.

CRITICAL: A valid 17-, 18- or 19-tag sensor set need NOT contain a
valid 16-tag subset. Therefore lack of a 16-core is NOT an invalidity
certificate for larger selected sensor sets. This auditor only proves constructive upper bounds by positive 16-cores.
The exact 19-tag minimum is proved SEPARATELY from pure-two-corner B6
and complete pure-three-edge B5 physical short-support witnesses in
verify_b6_one_erasure_exact19.py.
"""
from itertools import combinations
from collections import Counter
from verify_b6_geometric_rule import (CORNERS, EDGE_NAMES, ENDS, FACES,
                                      valid_pairs, midpoint, proper_rotations)

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


def verify_orbit_witnesses():
    """10 constructive orbit representatives imply 66/66 and 96/96 coverage.

    Proper cube rotations preserve admissibility, independently checked by
    verify_b6_geometric_rule.verify_geometry. Every unordered edge pair can
    be rotated to {DL,f}; its 11 possibilities fall into six orbits under
    the two rotations fixing DL. Every corner-edge pair can be rotated to
    {(-1,-1,-1),e}; its 12 possibilities fall into four orbits under three
    rotations fixing that original corner.
    """
    mid_to_edge={midpoint(e):e for e in EDGE_NAMES}
    def rotate_edge(r,e): return mid_to_edge[r(midpoint(e))]
    corner0=(-1,-1,-1)
    st_edge=[r for r in proper_rotations() if rotate_edge(r,"DL")=="DL"]
    st_corner=[r for r in proper_rotations() if r(corner0)==corner0]
    assert len(st_edge)==2 and len(st_corner)==3
    def orbit_partition(stabilizers,elements):
        unseen=set(elements)
        orbits=[]
        while unseen:
            seed=min(unseen)
            orbit=frozenset(rotate_edge(r,seed) for r in stabilizers)
            assert orbit <= unseen
            unseen-=orbit
            orbits.append(orbit)
        return frozenset(orbits)
    edge_orbits=orbit_partition(st_edge,set(EDGE_NAMES)-{"DL"})
    corner_orbits=orbit_partition(st_corner,EDGE_NAMES)
    expected_edge=frozenset(map(frozenset,[
        ("BL","DF"),("BR","UF"),("DB","FL"),
        ("DR","UL"),("FR","UB"),("UR",)]))
    expected_corner=frozenset(map(frozenset,[
        ("BL","DB","DL"),("BR","DF","UL"),
        ("DR","FL","UB"),("FR","UF","UR")]))
    assert edge_orbits==expected_edge,(edge_orbits,expected_edge)
    assert corner_orbits==expected_corner,(corner_orbits,expected_corner)
    # Entries (representative second edge, certificate core h).
    # Every listed allowed pair is exactly {DL,rep}.
    edge_witnesses={"BL":"UR","BR":"DB","DB":"UR",
                    "DR":"UF","FR":"DF","UR":"UL"}
    for f,h in edge_witnesses.items():
        assert frozenset(("DL",f)) in valid_pairs(h),(f,h)
    # Entries (representative edge, certificate edge pair).
    # The omitted corners are endpoints(DL), one of which is corner0.
    corner_witnesses={
        "BL":("DF","BL"),"BR":("UR","BR"),
        "DR":("UL","DR"),"FR":("UR","FR")}
    assert corner0 in ENDS["DL"]
    for e,pair in corner_witnesses.items():
        assert e in pair
        assert frozenset(pair) in valid_pairs("DL"),(e,pair)
    assert len(edge_witnesses)==len(edge_orbits)==6
    assert len(corner_witnesses)==len(corner_orbits)==4
    return edge_orbits,corner_orbits

def audit():
    family = positive_missing_four()
    assert len(TAGS)==20 and len(family)==156
    assert all(len(b)==4 and len(b&CORNERS_TAGS)==2
               and len(b&EDGES_TAGS)==2 for b in family)
    assert all(has_certified_16_core(TAGS-b,family) for b in family)
    verify_orbit_witnesses()
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
    print("LIMIT: 18 no-16-core is INCONCLUSIVE ALONE; exact b6^(1)=19 separately follows from physical B5 220-triple and B6 two-corner supports")
    print("66/66 EDGE-PAIR and 96/96 CORNER-EDGE extension coverage")
    return counts

if __name__=="__main__":
    audit()
