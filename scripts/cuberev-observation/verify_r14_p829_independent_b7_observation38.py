#!/usr/bin/env python3
"""Standalone R14-P8.29 38-facelet witness sanity check.
No imports from previous CUBE-REV modules. Checks only physical collision,
not 288 historical conjugacies or shortest-path optimality.
"""
from itertools import product
import json

F = {"U": (0, 1, 0), "R": (1, 0, 0), "F": (0, 0, 1),
     "D": (0, -1, 0), "L": (-1, 0, 0), "B": (0, 0, -1)}
def dot(a, b):
    return sum(x*y for x, y in zip(a, b))
slots = tuple((p, F[f]) for p in product((-1, 0, 1), repeat=3)
              if sum(t != 0 for t in p) in (2, 3)
              for f in "URFDLB" if dot(p, F[f]) == 1)
assert len(slots) == 48
idx = {s: i for i, s in enumerate(slots)}
def rotate(p, axis, k):
    x, y, z = p
    for _ in range(k % 4):
        if axis == 0:
            y, z = -z, y
        elif axis == 1:
            x, z = z, -x
        else:
            x, y = -y, x
    return x, y, z
def face(f, k):
    n = F[f]
    axis = next(i for i, v in enumerate(n) if v)
    return tuple(idx[(rotate(p, axis, -n[axis]*k),
                      rotate(t, axis, -n[axis]*k))]
                 if p[axis] == n[axis] else idx[(p, t)]
                 for p, t in slots)
def compose(a, b):
    return tuple(a[b[i]] for i in range(48))
def inverse(a):
    out = [-1]*48
    for i, j in enumerate(a):
        out[j] = i
    return tuple(out)
def state(tokens):
    perm = tuple(range(48))
    for s in tokens:
        power = 2 if s.endswith("2") else 3 if s.endswith("'") else 1
        perm = compose(face(s[0], power), perm)
    return perm

word = "L F R' F' L' U2 R U R U' R2 U2 R".split()
x = inverse(state(word[6:]))
y = state(word[:6])
d = state(word)
assert len(word) == 13
assert x != y
assert compose(inverse(x), y) == d
positions = {p for p, n in slots}
core = tuple(F["D"][i]+F["L"][i] for i in range(3))
excluded_corners = {p for p in positions if sum(v != 0 for v in p) == 3
                    and all(p[i] == core[i] for i in range(3) if core[i])}
excluded_edges = {tuple(F[a][i]+F[b][i] for i in range(3))
                  for a, b in (("U","F"),("U","R"))}
assert len(excluded_corners) == len(excluded_edges) == 2
observed = [i for i,(p,n) in enumerate(slots)
            if p not in excluded_corners | excluded_edges]
assert len(observed) == 38
assert all(x[i] == y[i] for i in observed)
assert sum(i != j for i, j in enumerate(d)) == 4
print(json.dumps({"status":"PASS","scope":"independent_physical_38_sticker_check",
                  "observed_stickers":len(observed),"two_states_distinct":x!=y,
                  "difference_moved_stickers":4,
                  "b7_global_minimum_proved":False},sort_keys=True))
