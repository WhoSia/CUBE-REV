"""Exact continuation checks for a fixed eleven-edge first-colour scan.

This program uses only the Python standard library. It constructs valid words
directly from the cubie labels and gates the use of parity at the leaf.
"""
from collections import Counter
from functools import cache
from itertools import permutations, product
from math import factorial, prod
import json

COLORS = "URFDLB"
LABELS = ("DL", "BL", "FL", "UL", "DB", "DF", "UB", "UF", "DR", "BR", "FR", "UR")
OPPOSITES = {frozenset(pair) for pair in ("UD", "RL", "FB")}

def parity(order):
    return sum(x > y for i, x in enumerate(order) for y in order[i + 1:]) % 2

def representative_prefixes():
    symmetry = []
    for perm in permutations(COLORS):
        mapping = dict(zip(COLORS, perm))
        if {frozenset(mapping[c] for c in pair) for pair in OPPOSITES} == OPPOSITES:
            symmetry.append(tuple(perm.index(c) for c in COLORS))
    supported = set()
    for omitted in range(12):
        for first in product(*(label for i, label in enumerate(LABELS) if i != omitted)):
            supported.add(tuple(first.count(c) for c in COLORS))
    assert len(supported) == 1362 and len(symmetry) == 48
    return Counter(min(tuple(key[i] for i in indices) for indices in symmetry)
                   for key in supported)

def candidate_words(prefix):
    words = {}
    def place(position, unused, order, flipped, unread):
        if position == 11:
            i, = unused
            last = LABELS[i][::-1] if flipped else LABELS[i]
            word = unread + last
            assert word not in words
            words[word] = parity(order + (i,))
            return
        seen = prefix[position]
        for j in unused:
            label = LABELS[j]
            if seen in label:
                bit = label.index(seen)
                place(position + 1, unused - {j}, order + (j,),
                      flipped ^ bit, unread + label[1 - bit])
    place(0, set(range(12)), (), 0, "")
    return words

def evaluate(words):
    cells = [{} for _ in range(13)]
    signs = [0, 0]
    for i, (word, sign) in enumerate(words.items()):
        bit = 1 << i
        signs[sign] |= bit
        for q, c in enumerate(word):
            cells[q][c] = cells[q].get(c, 0) | bit
    all_words = signs[0] | signs[1]

    @cache
    def wins(candidates, budget, terminal_sign):
        size = candidates.bit_count()
        if size <= 1:
            return True
        if terminal_sign and all((candidates & sign).bit_count() <= 1 for sign in signs):
            return True
        if budget == 0 or size > (6 ** budget) * (2 if terminal_sign else 1):
            return False
        alternatives = []
        for row in cells:
            parts = [subset for m in row.values() if (subset := candidates & m)]
            if len(parts) > 1:
                parts.sort(key=int.bit_count, reverse=True)
                alternatives.append((parts[0].bit_count(), tuple(parts)))
        alternatives.sort()
        return any(all(wins(part, budget - 1, terminal_sign) for part in parts)
                   for _, parts in alternatives)

    depths = {key: next(d for d in range(14) if check(d)) for key, check in (
        ("edge_only", lambda d: wins(all_words, d, False)),
        ("early_sign", lambda d: all(wins(sign, d, False) for sign in signs)),
        ("late_sign", lambda d: wins(all_words, d, True)),
    )}
    result = depths
    wins.cache_clear()
    return result

def audit():
    rows = []
    for representative, orbit_size in sorted(representative_prefixes().items()):
        prefix = ''.join(c * k for c, k in zip(COLORS, representative))
        words = candidate_words(prefix)
        ordered = orbit_size * factorial(11) // prod(factorial(k) for k in representative)
        rows.append({"prefix": prefix, "orbit_size": orbit_size, "candidates": len(words),
                     "ordered_prefixes": ordered, "edge_assignments": ordered * len(words),
                     **evaluate(words)})
    total = sum(row["edge_assignments"] for row in rows)
    assert len(rows) == 52 and total == factorial(12) * 2**11
    print(json.dumps({"total_edges": total, "rows": rows}, indent=2))

if __name__ == "__main__":
    audit()
