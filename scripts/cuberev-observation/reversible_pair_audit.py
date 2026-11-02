#!/usr/bin/env python3
"""Exact observability of explicit finite reversible machines.

Each action is a permutation, each observation is q(state). Pair-specific
distinguishers are found by reverse BFS on unordered state pairs.
This is a benchmark implementation, not an original general theorem.
"""
from collections import deque
from itertools import combinations

def shortest_distinguishers(actions, q):
    n = len(q)
    if not n or not actions or any(sorted(a) != list(range(n)) for a in actions):
        raise ValueError("Nonempty state set and permutation actions required")
    pairs = list(combinations(range(n), 2))
    incoming = {p: [] for p in pairs}
    for p in pairs:
        for i, a in enumerate(actions):
            nxt = tuple(sorted((a[p[0]], a[p[1]])))
            incoming[nxt].append((p, i))
    words = {p: () if q[p[0]] != q[p[1]] else None for p in pairs}
    queue = deque(p for p in pairs if words[p] is not None)
    while queue:
        target = queue.popleft()
        for p, i in incoming[target]:
            if words[p] is None:
                words[p] = (i,) + words[target]
                queue.append(p)
    for (s, t), w in words.items():
        if w is not None:
            for i in w:
                s, t = actions[i][s], actions[i][t]
            assert q[s] != q[t]
    return words

def signature(actions, q, word, start):
    s = start
    out = [q[s]]
    for i in word:
        s = actions[i][s]
        out.append(q[s])
    return tuple(out)

def preset_distinguishes(actions, q, word):
    return len({signature(actions, q, word, s) for s in range(len(q))}) == len(q)

if __name__ == "__main__":
    a = (1, 2, 3, 0)
    singleton = (1, 0, 0, 0)
    parity = (0, 1, 0, 1)
    assert all(w is not None for w in shortest_distinguishers([a], singleton).values())
    assert not preset_distinguishes([a], singleton, (0,))
    assert preset_distinguishes([a], singleton, (0, 0))
    assert shortest_distinguishers([a], parity)[(0, 2)] is None
    assert shortest_distinguishers([a], parity)[(1, 3)] is None
    print("PASS: C4 two-sensor observability contrast")
