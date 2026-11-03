#!/usr/bin/env python3
"""Entire 156-layout B6 optimal sensor single-tag swap graph.

Computes all possible single-original-tag exchanges, including changes
in which adjacent pair of original corners is missing. Geometry labels
are derived independently of any former exchange-graph sector counts.
All physical B6 validity grades are inherited from the previous
original 54-facelet-certified four-case rule.
"""
from __future__ import annotations

from collections import Counter, defaultdict, deque
from itertools import combinations

from verify_b6_geometric_rule import EDGE_NAMES, ENDS, valid_pairs


def complete_layouts():
    return frozenset(
        (frozenset(ENDS[h]), frozenset(e))
        for h in EDGE_NAMES for e in valid_pairs(h)
    )


def observed_exchange_graph(layouts=None):
    vertices = complete_layouts() if layouts is None else frozenset(layouts)
    graph = {v: set() for v in vertices}
    for a, b in combinations(vertices, 2):
        corner_delta = len(a[0] ^ b[0])
        edge_delta = len(a[1] ^ b[1])
        # Missing-tag XOR equals observed-tag XOR, regardless of
        # whether the moved tag is a corner or edge.
        if corner_delta + edge_delta == 2:
            graph[a].add(b)
            graph[b].add(a)
    return graph


def connected_components(graph):
    remaining = set(graph)
    components = []
    while remaining:
        root = next(iter(remaining))
        q = deque([root])
        seen = {root}
        while q:
            x = q.popleft()
            for y in graph[x]:
                if y not in seen:
                    seen.add(y)
                    q.append(y)
        remaining.difference_update(seen)
        components.append(frozenset(seen))
    return sorted(components, key=len, reverse=True)


def audit():
    layouts = complete_layouts()
    assert len(layouts) == 156
    graph = observed_exchange_graph(layouts)
    assert len(graph) == 156
    for x, near in graph.items():
        for y in near:
            assert x in graph[y]
            assert len(x[0] ^ y[0]) + len(x[1] ^ y[1]) == 2
    components = connected_components(graph)
    summary = tuple(sorted((len(c) for c in components), reverse=True))
    within_edges = sum(
        1 for x, near in graph.items() for y in near
        if x[0] == y[0]
    ) // 2
    cross_edges = sum(
        1 for x, near in graph.items() for y in near
        if x[0] != y[0]
    ) // 2
    assert within_edges == 12 * 22 == 264
    assert 2 * (within_edges + cross_edges) == sum(len(n) for n in graph.values())
    all_degree_counts = dict(sorted(Counter(map(len, graph.values())).items()))
    print("TOTAL_LAYOUTS", len(layouts))
    print("TOTAL_SWAP_EDGES", within_edges + cross_edges)
    print("WITHIN_FIXED_CORNER_PAIR", within_edges)
    print("CROSS_CORNER_PAIR", cross_edges)
    print("COMPONENT_SIZES", summary)
    print("DEGREE_HISTOGRAM", all_degree_counts)
    print("NOTE: current physical validity inherited from existing B6 certificates")
    return {
        "total": len(layouts),
        "within": within_edges,
        "cross": cross_edges,
        "components": summary,
        "degrees": all_degree_counts,
    }


if __name__ == "__main__":
    audit()
