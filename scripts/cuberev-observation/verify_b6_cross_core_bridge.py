#!/usr/bin/env python3
"""A compact geometry-only certificate of the 96+12*4+12 swap decomposition.

Unlike a brute-force traversal of the entire 156-node swap graph, this
reconstructs its components from one representative adjacent pair of core
cube edges, rotationally invariant 12-core incidence, and disjoint line
graphs of W5, C4 and K2. It does not check B6 physical distance classes.
"""
from __future__ import annotations

from itertools import combinations

from verify_b6_geometric_rule import EDGE_NAMES, ENDS, valid_pairs, graph_components


def omitted_pair_components(core):
    admissible = valid_pairs(core)
    remaining = set(EDGE_NAMES)
    components = []
    while remaining:
        seed = min(remaining)
        vertices = {seed}
        wave = [seed]
        while wave:
            v = wave.pop()
            for p in admissible:
                if v in p:
                    for w in p:
                        if w not in vertices:
                            vertices.add(w)
                            wave.append(w)
        remaining -= vertices
        e = {p for p in admissible if p <= vertices}
        components.append((frozenset(vertices), frozenset(e)))
    return components


def three_cross_core_swaps_certificate():
    core_pairs = [
        (h, k) for h, k in combinations(EDGE_NAMES, 2)
        if len(ENDS[h] & ENDS[k]) == 1
    ]
    assert len(core_pairs) == 24  # 8 cube vertices * C(3,2)
    for h in EDGE_NAMES:
        assert sum(h in pair for pair in core_pairs) == 4

    wheel_edges = {}
    cycle_edges = {}
    single_edges = {}
    for h in EDGE_NAMES:
        c = omitted_pair_components(h)
        assert sorted((len(v), len(e)) for v, e in c) == [
            (1, 0), (2, 1), (4, 4), (5, 8)
        ]
        wheel_edges[h] = next(e for v, e in c if len(v) == 5)
        cycle_edges[h] = next(e for v, e in c if len(v) == 4)
        single_edges[h] = next(e for v, e in c if len(v) == 2)
        assert len(wheel_edges[h]) == 8
        assert len(cycle_edges[h]) == 4
        assert len(single_edges[h]) == 1

    cross_count = 0
    for h, k in core_pairs:
        common = valid_pairs(h) & valid_pairs(k)
        assert len(common) == 3, (h, k, common)
        assert common <= wheel_edges[h] & wheel_edges[k]
        cross_count += len(common)

    # No other pair of omitted corner sets allows a 1-tag swap:
    # equal supports -> within-core exchange; intersect at exactly one
    # corner -> possible cross-core exchange requiring equal omitted
    # edge pairs; intersect at zero corners -> >=2 corner swaps.
    for h, k in combinations(EDGE_NAMES, 2):
        if len(ENDS[h] & ENDS[k]) != 1:
            assert len(ENDS[h] ^ ENDS[k]) == 4

    assert cross_count == 24 * 3 == 72
    assert graph_components(valid_pairs("DL")) == [
        (5, 8, (3, 3, 3, 3, 4)), (4, 4, (2, 2, 2, 2)),
        (2, 1, (1, 1)), (1, 0, (0,)),
    ]
    shared = valid_pairs("DL") & valid_pairs("DF")
    assert shared == {
        frozenset(("BR", "UB")),
        frozenset(("BR", "UR")),
        frozenset(("UB", "UR")),
    }

    # Each wheel line graph is connected with 8 vertices, and the 12
    # core edges form one connected graph through the 24 adjacent
    # core-edge pairs. Every adjacent core pair has three links wholly
    # between their wheel line graphs; hence all wheel components join.
    seen = {"DL"}
    while True:
        nxt = seen | {
            k for h, k in core_pairs if h in seen
        } | {
            h for h, k in core_pairs if k in seen
        }
        if nxt == seen:
            break
        seen = nxt
    assert seen == set(EDGE_NAMES)
    assert cross_count == 72

    # A wheel W5 has degree profile 4,3,3,3,3, so its line graph has
    # C(4,2)+4*C(3,2)=18 links, versus 4 for C4 and 0 for K2.
    fixed_edges = 12 * (18 + 4)
    assert fixed_edges == 264
    assert fixed_edges + cross_count == 336
    print("PASS: 24 adjacent pairs of omitted-corner edges, each with exactly three shared admissible edge pairs")
    print("PASS: all 72 cross-core swaps connect ONLY the wheel components")
    print("PASS: per core 8+4+1, globally one 96 plus twelve 4 plus twelve isolated designs")
    print("PASS: 336 total one-tag links = 264 fixed-core + 72 cross-core")
    print("PASS: DL–DF witness pairs {BR,UB}, {BR,UR}, {UB,UR}")
    print("LIMIT: all positive/negative B6 membership inherited from original 54-facelet certificates")


if __name__ == "__main__":
    three_cross_core_swaps_certificate()
