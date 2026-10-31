#!/usr/bin/env python3
"""Exact B6 corner-pair obstruction SUBSYSTEM, not a full B6 state census.

Assumptions: two independently replayed pure-two-corner 12-HTM words provide
the 12 face-diagonal and four body-diagonal corner difference supports in B6.
No claim that adjacent-corner differences are absent in B6.
"""
from itertools import product, combinations
from collections import Counter

C = list(product((-1, 1), repeat=3))
pairs = list(combinations(range(8), 2))
distance = lambda a, b: sum(x != y for x, y in zip(a, b))
certified = {(i, j) for i, j in pairs if distance(C[i], C[j]) in (2, 3)}
assert len(certified) == 16

allowed = []
for mask in range(256):
    S = {i for i in range(8) if mask & (1 << i)}
    if all(i in S or j in S for i, j in certified):
        allowed.append(S)
counts = Counter(map(len, allowed))
assert counts == {6: 12, 7: 8, 8: 1}, counts

for S in allowed:
    if len(S) == 6:
        omitted = [C[i] for i in range(8) if i not in S]
        assert distance(*omitted) == 1

# One permanent sensor erasure: both endpoints of EVERY observed
# two-factor difference must be selected.
assert {i for edge in certified for i in edge} == set(range(8))

print("PASS: 16 guaranteed B6 two-corner supports")
print("PASS: finite corner-cover profile (size : #sets)", dict(sorted(counts.items())))
print("PASS: 6-corner choices must omit adjacent corners (12 possibilities)")
print("PASS: even these partial witnesses force all 8 corners for 1-erasure")
print("LIMIT: additional B6 physical supports may eliminate candidates")
