#!/usr/bin/env python3
"""Independent bounded enumeration checking reversible_pair_audit.py."""
from itertools import permutations, product
from reversible_pair_audit import shortest_distinguishers, signature, preset_distinguishes

def brute_pair(actions, q, s, t, maxlen):
    # Enumerate all action words until the pair graph bound is reached.
    frontier = [(s, t, ())]
    for _ in range(maxlen + 1):
        new = []
        for x, y, word in frontier:
            if q[x] != q[y]:
                return word
            for i, a in enumerate(actions):
                new.append((a[x], a[y], word + (i,)))
        frontier = new
    return None

def main():
    checked = 0
    for n in (2, 3, 4):
        for action in permutations(range(n)):
            for q in product((0, 1), repeat=n):
                actions = [action]
                actual = shortest_distinguishers(actions, q)
                for (s, t), word in actual.items():
                    expected = brute_pair(actions, q, s, t, n * (n - 1) // 2 - 1)
                    assert (word is None) == (expected is None), (n, action, q, s, t)
                    if word is not None:
                        assert len(word) == len(expected)
                        assert signature(actions, q, word, s)[-1] != signature(actions, q, word, t)[-1]
                checked += 1
    a = (1, 2, 3, 0)
    assert preset_distinguishes([a], (1, 0, 0, 0), (0, 0))
    print(f"PASS: {checked} explicit reversible single-generator/output systems (n=2..4)")

if __name__ == "__main__":
    main()
