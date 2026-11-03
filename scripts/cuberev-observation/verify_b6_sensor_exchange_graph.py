#!/usr/bin/env python3
"""Exchange graph of CUBE-REV radius-six optimal 16-tag sensor layouts.

Conditioned on the previously established exact physical B6 geometry
criterion, construct nodes = optimal sensor designs that omit the TWO
corner tags incident to a fixed core edge h and TWO original edge tags.
Two nodes are adjacent iff one observed edge-sensor tag can be replaced
by one other tag while preserving 16-tag B6 injectivity.
"""
from __future__ import annotations

from collections import deque
from itertools import combinations

from verify_b6_geometric_rule import EDGE_NAMES, valid_pairs, graph_components


def exchange_graph(core: str):
    vertices = set(valid_pairs(core))
    assert len(vertices) == 13
    neighbors = {v: set() for v in vertices}
    for a, b in combinations(vertices, 2):
        if len(a ^ b) == 2:  # both 2sets: exactly one moved observed tag
            neighbors[a].add(b)
            neighbors[b].add(a)
    assert all(b in neighbors[a] for a in neighbors for b in neighbors[a])
    return neighbors


def components(neighbors):
    rest = set(neighbors)
    out = []
    while rest:
        root = min(rest, key=lambda v: tuple(sorted(v)))
        seen = {root}
        q = deque([root])
        while q:
            for nxt in neighbors[q.popleft()]:
                if nxt not in seen:
                    seen.add(nxt)
                    q.append(nxt)
        rest -= seen
        out.append(frozenset(seen))
    return sorted(out, key=lambda x: (-len(x), min(tuple(sorted(i)) for i in x)))


def audit():
    summaries = {}
    for h in EDGE_NAMES:
        graph = exchange_graph(h)
        comp = components(graph)
        sizes = tuple(map(len, comp))
        m = sum(map(len, graph.values())) // 2
        assert sizes == (8, 4, 1), (h, sizes)
        assert m == 22, (h, m)
        # The original 12-node pair-compatibility graph is
        # W5 disjoint union C4 disjoint union K2 disjoint union K1.
        # Its non-isolated edges become the vertices of the line graph.
        expected = [(5, 8, (3, 3, 3, 3, 4)),
                    (4, 4, (2, 2, 2, 2)), (2, 1, (1, 1)), (1, 0, (0,))]
        assert graph_components(valid_pairs(h)) == expected
        summaries[h] = (sizes, m)

    # A complete uniform 2-subset system has Johnson graph J(12,2):
    # all 66 nodes are connected, degree 2*(12-2)=20.
    all_edges = [frozenset(p) for p in combinations(EDGE_NAMES, 2)]
    uniform = {v: set() for v in all_edges}
    for a, b in combinations(all_edges, 2):
        if len(a ^ b) == 2:
            uniform[a].add(b)
            uniform[b].add(a)
    assert tuple(map(len, components(uniform))) == (66,)
    assert {len(s) for s in uniform.values()} == {20}
    assert sum(map(len, uniform.values())) // 2 == 660

    print("PASS: 12 core edges, 13 B6-positive layouts each")
    print("PASS: every fixed-core single-sensor-exchange graph has components (8,4,1)")
    print("PASS: 22 undirected exchange links, 156 nodes/264 links over all fixed cores")
    print("PASS: complete uniform J(12,2) control is connected and 20-regular")
    print("CONSEQUENCE: a path of individually valid one-tag exchanges cannot cross components")
    print("BOUNDARY: nodes' B6 physical validity inherited from historical facelet certificates")
    return summaries


if __name__ == "__main__":
    audit()
