#!/usr/bin/env python3
"""Abstract 12-element legal B6 stabilizer multiplication audit.

Exactly two corner and two edge tags are omitted; every other oriented
original cubie is fixed. This verifies multiplication in standard cubie
coordinates and the S3 x C2 structure, not a 54-facelet implementation
or any 18-HTM geodesic.
"""
from __future__ import annotations

from collections import Counter
from itertools import product

IDENTITY = (0, 0, 0)
ELEMENTS = tuple(product(range(2), range(3), range(2)))


def multiply(a: tuple[int, int, int],
             b: tuple[int, int, int]) -> tuple[int, int, int]:
    """Physical-coordinate composition LEFT then RIGHT (left o right).

    (s,t,f): s=linked corner+edge swap bit; twists at the two missing
    corner positions are (+t,-t); missing edge flips are (+f,+f).
    Following the cubie-coordinate convention in the existing
    build_b6_stabilizer_goals.py, the RIGHT permutation acts on the
    LEFT orientation vector before orientation values are added.
    """
    s, t, f = a
    u, v, h = b
    return (s ^ u, ((-1 if u else 1) * t + v) % 3, f ^ h)


def inverse(a: tuple[int, int, int]) -> tuple[int, int, int]:
    s, t, f = a
    return (s, (t if s else -t) % 3, f)


def order(a: tuple[int, int, int]) -> int:
    x = IDENTITY
    for k in range(1, 13):
        x = multiply(x, a)
        if x == IDENTITY:
            return k
    raise AssertionError("Not a group of order 12")


def physical_cubie_record(a):
    s, t, f = a
    cp, ep = list(range(8)), list(range(12))
    if s:
        cp[0], cp[1] = cp[1], cp[0]
        ep[0], ep[1] = ep[1], ep[0]
    co, eo = [0] * 8, [0] * 12
    co[0], co[1] = t, (-t) % 3
    eo[0], eo[1] = f, f
    return (tuple(cp), tuple(co), tuple(ep), tuple(eo))


def compose_coordinates(left, right):
    cp, co, ep, eo = left
    p, t, q, f = right
    return (
        tuple(cp[p[i]] for i in range(8)),
        tuple((co[p[i]] + t[i]) % 3 for i in range(8)),
        tuple(ep[q[i]] for i in range(12)),
        tuple((eo[q[i]] + f[i]) % 2 for i in range(12)),
    )


def commutator(a, b):
    return multiply(
        multiply(multiply(a, b), inverse(a)), inverse(b)
    )


def self_test():
    assert len(ELEMENTS) == 12
    assert len(set(ELEMENTS)) == 12
    for a in ELEMENTS:
        assert multiply(a, IDENTITY) == multiply(IDENTITY, a) == a
        assert multiply(a, inverse(a)) == IDENTITY
        assert multiply(inverse(a), a) == IDENTITY
        for b in ELEMENTS:
            assert multiply(a, b) in ELEMENTS
            assert physical_cubie_record(multiply(a, b)) == (
                compose_coordinates(physical_cubie_record(a),
                                    physical_cubie_record(b))
            )
            for c in ELEMENTS:
                assert multiply(multiply(a, b), c) == multiply(
                    a, multiply(b, c)
                )

    assert Counter(order(a) for a in ELEMENTS) == {
        1: 1, 2: 7, 3: 2, 6: 2
    }
    center = {a for a in ELEMENTS if all(
        multiply(a, b) == multiply(b, a) for b in ELEMENTS
    )}
    assert center == {(0, 0, 0), (0, 0, 1)}
    commutators = {commutator(a, b) for a in ELEMENTS for b in ELEMENTS}
    assert commutators == {(0, 0, 0), (0, 1, 0), (0, 2, 0)}

    # The swap (1,0,0) inverts corner twist (0,1,0):
    x, y = (1, 0, 0), (0, 1, 0)
    assert multiply(multiply(x, y), inverse(x)) == inverse(y)
    # Orientation sign depends on the RIGHT permutation: not an arbitrary
    # convention, but derived from the tested cubie-coordinate product.
    assert multiply((1, 1, 0), (0, 2, 0)) == (1, 0, 0)
    assert multiply((0, 2, 0), (1, 1, 0)) == (1, 2, 0)

    print("PASS: all 144 products agree with 8-corner/12-edge cubie coordinates")
    print("PASS: all 1728 associativity triples; inverses and closure")
    print("PASS: 12 elements; order histogram {1:1, 2:7, 3:2, 6:2}")
    print("PASS: central edge flip C2 and corner-twist commutator C3")
    print("RESULT: abstract group is (C3 semidirect C2) x C2 = S3 x C2")
    print("LIMIT: no physical 54-facelet or HTM-distance certification")


if __name__ == "__main__":
    self_test()
