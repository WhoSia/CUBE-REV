#!/usr/bin/env python3
"""Independent algebraic explanation of the 88-to-74 B6 goal reduction.

Fix TWO omitted corner tags. Vary the pair of omitted edge tags.
Every 12-state stabilizer has the same three-element pure-corner-twist
subgroup; all nine remaining states affect BOTH omitted edges.
Distinct edge-pair stabilizers thus intersect in exactly those 3 states.
This does not prove any 18-HTM geodesic bound.
"""
from __future__ import annotations

from itertools import combinations, product


def legal_stabilizer(corner_pair: tuple[int, int],
                     edge_pair: tuple[int, int]) -> frozenset:
    ci, cj = sorted(corner_pair)
    ei, ej = sorted(edge_pair)
    if not (0 <= ci < cj < 8 and 0 <= ei < ej < 12):
        raise ValueError("Need two distinct legal corners and two distinct legal edges")
    out = set()
    for swap, twist, flip in product(range(2), range(3), range(2)):
        cp = list(range(8))
        ep = list(range(12))
        co = [0] * 8
        eo = [0] * 12
        if swap:
            cp[ci], cp[cj] = cp[cj], cp[ci]
            ep[ei], ep[ej] = ep[ej], ep[ei]
        co[ci], co[cj] = twist, (-twist) % 3
        eo[ei], eo[ej] = flip, flip
        assert sum(co) % 3 == sum(eo) % 2 == 0
        state = (tuple(cp), tuple(co), tuple(ep), tuple(eo))
        out.add(state)
    assert len(out) == 12
    return frozenset(out)


def audit_all_edge_pairs() -> None:
    corners = (0, 1)
    pairs = list(combinations(range(12), 2))
    families = [(pair, legal_stabilizer(corners, pair)) for pair in pairs]
    assert len(families) == 66
    shared_corner_twists = set.intersection(*(set(s) for _, s in families))
    assert len(shared_corner_twists) == 3
    for _, states in families:
        assert len(states & shared_corner_twists) == 3
    for i, (_, s) in enumerate(families):
        for _, t in families[i + 1:]:
            assert s & t == shared_corner_twists

    # Each novel omitted-edge pair contributes precisely 12-3=9 states.
    for m in (1, 2, 3, 8, 13, 66):
        union = set().union(*(s for _, s in families[:m]))
        assert len(union) == 3 + 9 * m, (m, len(union))

    # The 8 positive B6 layout-representative edge pairs form one case:
    # eight times eleven nonidentity entries, but only 74 different
    # nonidentity states; fourteen repeated pure corner twists.
    union_8 = set().union(*(s for _, s in families[:8]))
    assert len(union_8) - 1 == 74
    assert 8 * 11 - 74 == 14
    print("PASS: 66 possible omitted-edge pairs and 2145 pairwise intersections")
    print("PASS: shared subgroup of size 3; 9 distinct states per edge pair")
    print("PASS: for 8 different edge pairs: 88 entries => 74 distinct nonidentity states")
    print("LIMIT: this is an abstract cubie legality check, not 54-facelet replay")
    print("LIMIT: 41 full-48/inverse distance classes require separate symmetry proof")


if __name__ == "__main__":
    audit_all_edge_pairs()
