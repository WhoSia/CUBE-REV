#!/usr/bin/env python3
"""Exact full-cube stabilizer *support* census without an HTM search.

The observed objects are ORIGINAL oriented corner/edge tags. The arguments
c and e count omitted corner and edge tags, respectively (0<=c<=8,
0<=e<=12). All other tags must remain in their solved positions and
orientations.

This module proves finite group-legality counts, NOT a bound on the
18-face-turn HTM word length of any state.
"""
from __future__ import annotations

from collections import Counter
from functools import lru_cache
from itertools import permutations, product
from math import comb, factorial


def _parity_balance(n: int) -> int:
    """#even permutations - #odd permutations of n objects."""
    return 1 if n < 2 else 0


def _check(c: int, e: int) -> None:
    if not (isinstance(c, int) and isinstance(e, int)
            and 0 <= c <= 8 and 0 <= e <= 12):
        raise ValueError("Expected 0<=omitted corners<=8 and 0<=omitted edges<=12")


def stabilizer_order(c: int, e: int) -> int:
    """Number of legal cube elements fixing every other original cubie.

    Global corner/edge permutation parities must agree. The independent
    corner-twist and edge-flip zero-sum constraints contribute
    3**max(c-1,0) and 2**max(e-1,0), respectively.
    """
    _check(c, e)
    matched_parities = (
        factorial(c) * factorial(e)
        + _parity_balance(c) * _parity_balance(e)
    ) // 2
    return matched_parities * 3 ** max(c - 1, 0) * 2 ** max(e - 1, 0)


@lru_cache(maxsize=None)
def exact_support_count(c: int, e: int) -> int:
    """States moving or reorienting EXACTLY these c corner and e edge tags.

    Binomial inversion of stabilizer_order on the Boolean lattice of
    possible supports. Includes the identity only at (c,e)=(0,0).
    """
    _check(c, e)
    answer = sum(
        (-1) ** (c - i + e - j) * comb(c, i) * comb(e, j)
        * stabilizer_order(i, j)
        for i in range(c + 1) for j in range(e + 1)
    )
    assert answer >= 0
    return answer


def support_profile(c: int, e: int) -> dict[tuple[int, int], int]:
    """Histogram by support cardinalities, within a fixed omission set."""
    _check(c, e)
    out = {
        (i, j): comb(c, i) * comb(e, j) * exact_support_count(i, j)
        for i in range(c + 1) for j in range(e + 1)
    }
    assert sum(out.values()) == stabilizer_order(c, e)
    return out


def _parity(p: tuple[int, ...]) -> int:
    return sum(p[i] > p[j] for i in range(len(p))
               for j in range(i + 1, len(p))) % 2


def exhaustive_small_profile(c: int, e: int) -> Counter:
    """Independent direct legality enumeration for small omission sets.

    This is an abstract standard 3x3 cubie-coordinate enumeration, not
    a second physical 54-facelet cube engine.
    """
    _check(c, e)
    out: Counter = Counter()
    corner_twists = [
        x for x in product(range(3), repeat=c) if sum(x) % 3 == 0
    ]
    edge_flips = [
        x for x in product(range(2), repeat=e) if sum(x) % 2 == 0
    ]
    edge_perms = [(p, _parity(p)) for p in permutations(range(e))]
    for cp in permutations(range(c)):
        p_cp = _parity(cp)
        for ep, p_ep in edge_perms:
            if p_cp != p_ep:
                continue
            moved_corners = [i for i in range(c) if cp[i] != i]
            moved_edges = [j for j in range(e) if ep[j] != j]
            for twists in corner_twists:
                nc = sum(cp[i] != i or twists[i] != 0 for i in range(c))
                for flips in edge_flips:
                    ne = sum(ep[j] != j or flips[j] != 0 for j in range(e))
                    out[(nc, ne)] += 1
    return out


def self_test() -> None:
    assert stabilizer_order(0, 0) == 1
    assert stabilizer_order(2, 2) == 12
    assert stabilizer_order(8, 12) == 43252003274489856000
    assert exact_support_count(0, 0) == 1
    assert exact_support_count(2, 0) == 2
    assert exact_support_count(0, 2) == 1
    assert exact_support_count(2, 2) == 8
    assert exact_support_count(1, 7) == 0
    assert exact_support_count(6, 1) == 0
    assert {k: v for k, v in support_profile(2, 2).items() if v} == {
        (0, 0): 1, (2, 0): 2, (0, 2): 1, (2, 2): 8,
    }
    tested = 0
    for c in range(4):
        for e in range(4):
            direct = exhaustive_small_profile(c, e)
            formula = Counter({k: v for k, v in support_profile(c, e).items() if v})
            assert direct == formula, (c, e, direct, formula)
            tested += 1
    # Nontrivial case with both permutations of degree four.
    assert exhaustive_small_profile(4, 4) == Counter({
        k: v for k, v in support_profile(4, 4).items() if v
    })
    print("PASS: 17 independent cubie-legality enumerations agree with")
    print("      parity/order formula and Boolean-lattice support inversion")
    print("PASS: (c,e)=(2,2): identity 1, corner-only 2, edge-only 1,")
    print("      mixed four-tag support 8; total 12")
    print("PASS: full legal 3x3 group order 43252003274489856000")
    print("LIMIT: no 18-HTM minimum word lengths or B6 injectivity proved")


if __name__ == "__main__":
    self_test()
