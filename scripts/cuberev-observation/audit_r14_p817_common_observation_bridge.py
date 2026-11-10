#!/usr/bin/env python3
"""CUBE-REV R14-P8.17: static cover vs adaptive decision tree.

This is a tiny, completely independently enumerable 6-state / 3-query
ternary-response counterexample and a generic exact solver. It validates
the mathematical *bridge* used to write a unified paper; it is NOT an
additional Rubik-state theorem, a reconstruction of 48 physical facelets,
or proof that the cube's sensor counts and frame depths are comparable.
"""
from itertools import combinations
from functools import lru_cache
import json

STATES = ("A0", "A1", "A2", "B0", "B1", "B2")
QUERIES = ("q0", "q1", "q2")
# q0 detects whether A/B; q1 distinguishes A's three members;
# q2 distinguishes B's three members.
READOUT = {
    "A0": (0, 0, 0),
    "A1": (0, 1, 0),
    "A2": (0, 2, 0),
    "B0": (1, 0, 0),
    "B1": (1, 0, 1),
    "B2": (1, 0, 2),
}

def output(x, query):
    return READOUT[x][QUERIES.index(query)]

def injective(xs, query_set):
    signatures = {tuple(output(x,q) for q in query_set) for x in xs}
    return len(signatures) == len(xs)

def support(x,y):
    return frozenset(q for q in QUERIES if output(x,q)!=output(y,q))

PAIRS = tuple(combinations(STATES,2))
SUPPORTS = {p:support(*p) for p in PAIRS}
assert len(PAIRS)==15 and all(SUPPORTS.values())
for k in range(4):
    for qs in combinations(QUERIES,k):
        hitting = all(bool(SUPPORTS[p]&set(qs)) for p in PAIRS)
        assert hitting == injective(STATES,qs)

STATIC_OPT = min(k for k in range(4)
                 if any(injective(STATES,qs) for qs in combinations(QUERIES,k)))
assert STATIC_OPT == 3
assert all(not injective(STATES,qs) for qs in combinations(QUERIES,2))

# Exact AND-OR Bellman minimax, with explicit branch certificates and
# no assumption that information gain is equivalent to optimality.
@lru_cache(None)
def solve(belief):
    if len(belief) <= 1:
        return (0, None, ())
    best = None
    for q in QUERIES:
        groups = {}
        for x in belief:
            groups.setdefault(output(x,q),[]).append(x)
        branches = tuple((v,tuple(sorted(xs))) for v,xs in sorted(groups.items()))
        if any(len(xs)==len(belief) for _,xs in branches):
            continue # no progress; never helps a shortest exact tree
        children=tuple((v, solve(xs)[0]) for v,xs in branches)
        candidate=(1+max(depth for _,depth in children),q,branches)
        if best is None or candidate[0]<best[0]:
            best=candidate
    assert best is not None, ("indistinguishable belief",belief)
    return best

DEPTH, FIRST_QUERY, ROOT_BRANCHES = solve(STATES)
assert DEPTH == 2 and FIRST_QUERY == "q0"
assert len(ROOT_BRANCHES)==2
assert all(solve(group)[0]==1 for _,group in ROOT_BRANCHES)
# Any binary-depth-1 protocol cannot distinguish six non-identical
# states: direct exhaustive check of all three queries suffices.
assert not any(injective(STATES,(q,)) for q in QUERIES)

# Verify actual online reconstruction of all six states.
policy = {
    0: "q0",
    1: {"A": "q1", "B": "q2"}
}
decoded = {}
for x in STATES:
    first = output(x,"q0")
    second = output(x,"q1" if first==0 else "q2")
    decoded[(first,second)] = x
assert len(decoded)==6
for x in STATES:
    first=output(x,"q0")
    assert decoded[(first, output(x,"q1" if first==0 else "q2"))]==x

print(json.dumps({
    "status":"R14_P817_GENERIC_OBSERVATION_HYPERGRAPH_BELLMAN_PASS",
    "scope":"six-state illustrative model, NOT Rubik geometry",
    "hidden_states":len(STATES),
    "queries":len(QUERIES),
    "pair_supports":len(SUPPORTS),
    "static_minimum_query_count":STATIC_OPT,
    "adaptive_minimax_query_depth":DEPTH,
    "first_adaptive_query":FIRST_QUERY,
    "exactly_decoded_states":len(decoded),
    "full_cube_physical_certificate_replayed":False
},sort_keys=True))
