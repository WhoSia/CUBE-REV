#!/usr/bin/env python3
"""Check the finite Q3 line-graph combinatorics used in CUBE-REV 0.28.

This is independent of Rubik sticker/turn physics. It DOES NOT verify that
the inherited 13-HTM physical witness has adjacent-edge-only support.
"""
from itertools import combinations, product

vertices = list(product((0, 1), repeat=3))
edges = [frozenset((u, v)) for u, v in combinations(vertices, 2)
         if sum(x != y for x, y in zip(u, v)) == 1]
assert len(vertices) == 8 and len(edges) == 12

adjacent_pairs = {frozenset((i, j)) for i, j in combinations(range(12), 2)
                  if edges[i] & edges[j]}
assert len(adjacent_pairs) == 24
assert {sum(i in p for p in adjacent_pairs) for i in range(12)} == {4}

independent = []
for k in range(13):
    for choice in combinations(range(12), k):
        selected = set(choice)
        if all(not p <= selected for p in adjacent_pairs):
            independent.append(choice)
max_size = max(map(len, independent))
maximum = [a for a in independent if len(a) == max_size]
assert max_size == 4 and len(maximum) == 9
assert 12 - max_size == 8
assert {i for pair in adjacent_pairs for i in pair} == set(range(12))

print("Q3=8 vertices, 12 edges; L(Q3)=12 vertices, 24 edges, degree 4")
print("max independent size=4; maximum independent sets=9; vertex-cover=8")
print("PASS — independent combinatorial check, not physical-cube witness check")
