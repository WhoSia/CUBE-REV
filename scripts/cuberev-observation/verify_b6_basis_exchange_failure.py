#!/usr/bin/env python3
"""B6 optimal 16-sensor layouts violate matroid basis exchange.

Uses ONLY the intrinsic 13-edge-pair geometric classification for every
fixed pair of omitted adjacent corners. The prior facelet certificates
are necessary for interpreting the 156 geometric-positive layouts as
actual B6-injective designs and the remaining pairs as failures.
No new 54-facelet or 18-HTM distance computation occurs here.
"""
from __future__ import annotations

from itertools import combinations

from verify_b6_geometric_rule import EDGE_NAMES, valid_pairs


def exchange_failures(omitted_pair_bases):
    """List violated observed-sensor basis-exchange obligations.

    Each omitted pair E corresponds to the observed edge-sensor
    complement of E. A,B are *omission* pairs. To exchange observed
    sensor x in S_A minus S_B (x in B minus A), add y in S_B minus S_A
    (y in A minus B); the new omission set is (A minus y) union x.
    """
    bases = set(map(frozenset, omitted_pair_bases))
    assert all(len(p) == 2 for p in bases)
    violations = []
    for a in sorted(bases, key=lambda q: tuple(sorted(q))):
        for b in sorted(bases, key=lambda q: tuple(sorted(q))):
            for x in sorted(b - a):
                possible_y = sorted(a - b)
                replacements = tuple(
                    frozenset((a - {y}) | {x}) for y in possible_y
                )
                if all(p not in bases for p in replacements):
                    violations.append((a, b, x, replacements))
    return violations


def verify():
    counts = {}
    for h in EDGE_NAMES:
        bases = valid_pairs(h)
        assert len(bases) == 13
        failures = exchange_failures(bases)
        counts[h] = len(failures)
        assert len(failures) == 176, (h, len(failures))
    assert sum(counts.values()) == 12 * 176 == 2112

    h = "DL"
    a = frozenset(("FR", "UR"))  # F-h*: B6-positive class
    b = frozenset(("DR", "UL"))  # P-P: B6-positive class
    x = "DR"                    # observed by S_A, omitted by S_B
    assert a in valid_pairs(h) and b in valid_pairs(h)
    assert x in b - a
    possible = {
        frozenset((a - {y}) | {x}) for y in a - b
    }
    assert possible == {
        frozenset(("DR", "UR")),  # P-h*: old B6-negative class
        frozenset(("DR", "FR")),  # P-F: old B6-negative class
    }
    assert all(p not in valid_pairs(h) for p in possible)
    assert any(
        u == a and v == b and z == x for u, v, z, _ in exchange_failures(valid_pairs(h))
    )

    # Negative-control input: if every 2-set is allowed, exchange
    # MUST hold. This catches an always-failing exchange checker.
    all_pairs = combinations(EDGE_NAMES, 2)
    assert exchange_failures(all_pairs) == []
    print("PASS: each of 12 omitted-corner edges has 13 admissible edge pairs")
    print("PASS: 176 violated ordered basis-exchange obligations per core edge")
    print("PASS: explicit DL witness FR+UR vs DR+UL; DR exchange fails twice")
    print("PASS: full 66-pair family satisfies exchange (negative control)")
    print("RESULT: B6 16-tag geometric-positive family is NOT matroidal")
    print("TRUST: B6 validity/invalidity inherited from earlier physical certificates")
    print("LIMIT: no new independent 54-facelet witness or HTM distance checked")
    return counts


if __name__ == "__main__":
    verify()
