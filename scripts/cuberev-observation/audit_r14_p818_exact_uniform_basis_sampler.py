#!/usr/bin/env python3
"""R14-P8.18: zero-rejection, exactly uniform sampler of physically grounded
B6 minimum and all inclusion-wise minimal tagged-cubie layouts.

This is a *dependent finite combinatorial theorem* (inherited complete
physical 16-positive/negative B6 and short-support certificates), not a
fresh P48 word-metric verification. It relies only on the earlier
geometric classification P(h), checks a total labelled bijection by
exhaustive deterministic rank/unrank, and uses unbiased random ranks.
"""
from itertools import combinations
from fractions import Fraction
import json
import random
from audit_r14_p813_complete_minimal_base_spectrum import (
    EDGES, CORNERS, ENDS, OMEGA, PAIRS, positive16, minimal, P
)

EDGE_ORDER=tuple(sorted(EDGES))
CORNER_ORDER=tuple(sorted(CORNERS))
PAIR_ORDER=tuple(frozenset(q) for q in combinations(EDGE_ORDER,2))
assert len(PAIR_ORDER)==66

def exact16(rank):
    assert 0<=rank<156
    h=EDGE_ORDER[rank//13]
    edge_pair=sorted(PAIRS[h],key=lambda p: tuple(sorted(p)))[rank%13]
    return frozenset({("C",c) for c in ENDS[h]} |
                     {("E",e) for e in edge_pair})

def exact17(rank):
    assert 0<=rank<276
    if rank<12:
        h=EDGE_ORDER[rank]
        return frozenset({("C",c) for c in ENDS[h]} | {("E",h)})
    k=rank-12
    c=CORNER_ORDER[k//33]
    incident=[h for h in EDGE_ORDER if c in ENDS[h]]
    assert len(incident)==3
    extendable=set().union(*(PAIRS[h] for h in incident))
    remaining=[pair for pair in PAIR_ORDER if pair not in extendable]
    assert len(remaining)==33
    pair=remaining[k%33]
    return frozenset({("C",c)}|{("E",e) for e in pair})

def exact_minimal(rank):
    assert 0<=rank<432
    return exact16(rank) if rank<156 else exact17(rank-156)

list16=tuple(exact16(i) for i in range(156))
list17=tuple(exact17(i) for i in range(276))
listall=tuple(exact_minimal(i) for i in range(432))
assert len(set(list16))==156 and len(set(list17))==276
assert set(list16)==set(positive16) and set(list17)==set(minimal[3])
assert set(listall)==set(positive16)|set(minimal[3])
assert len(set(listall))==432
assert all(len(x)==4 for x in list16)
assert all(len(x)==3 for x in list17)

# A 16-sensor layout is a 4-tag omission. Every rank corresponds to
# exactly one h and exactly one of the 13 admissible edge pairs P(h).
# A minimal17 3-tag omission is partitioned into precisely the 12
# two-corner/one-native-edge and 8*33 one-corner/two-edge possibilities.
p16=Fraction(156,432)
p17=Fraction(276,432)
assert p16==Fraction(13,36)
assert p17==Fraction(23,36)
assert 16*p16+17*p17==Fraction(599,36)

# Rejection baselines (random 4 omissions in all C(20,4) candidates,
# or random core h and unrestricted unordered original-edge pair).
p_naive=Fraction(156,4845)
p_core_random=Fraction(13,66)
assert p_naive==Fraction(52,1615)
assert p_core_random==Fraction(13,66)

# Concrete seeded smoke test (not a substitute for the rank bijection).
rng=random.Random(20261111)
samples=3000
selected=[exact_minimal(rng.randrange(432)) for _ in range(samples)]
assert len(selected)==samples
assert all(s in set(listall) for s in selected)

print(json.dumps({
    "result":"R14_P818_REJECTION_FREE_UNIFORM_B6_BASIS_SAMPLER_PASS",
    "scope":"conditional on inherited full physical B6 16-classification",
    "minimum16_exact_unranking_count":len(list16),
    "nonminimum_minimal17_exact_unranking_count":len(list17),
    "all_minimal_exact_unranking_count":len(listall),
    "uniform_minimal_prob16":str(p16),
    "uniform_minimal_prob17":str(p17),
    "uniform_minimal_expected_sensors":str(Fraction(599,36)),
    "naive_unconstrained_random4_acceptance":str(p_naive),
    "core_with_random_edgepair_acceptance":str(p_core_random),
    "rejection_free_uniform_minimum16_acceptance":"1",
    "all_16_and_17_bijections_exhaustively_checked":True,
    "fresh_physical_htm_geodesic_computation":False
},sort_keys=True))
