#!/usr/bin/env python3
"""Exact finite *toy-model* regression for posterior transport and online
two-step adversary logic. NOT a full P48 Rubik theorem or Lean kernel proof.
"""
import itertools
import json
from collections import Counter

BITS = list(itertools.product((0, 1), repeat=3))
STATES = tuple(itertools.product(BITS, BITS))
QUERIES = tuple(itertools.product(range(3), repeat=2))
OUTCOMES = tuple(itertools.product((0, 1), repeat=2))


def obs(state, q):
    return state[0][q[0]], state[1][q[1]]


def move_state(state):
    return tuple(tuple(word[(i - 1) % 3] for i in range(3)) for word in state)


def move_query(q):
    return (q[0] + 1) % 3, (q[1] + 1) % 3


def post(belief, q, out):
    return frozenset(x for x in belief if obs(x, q) == out)


def step(belief):
    return frozenset(map(move_state, belief))


assert len(STATES) == 64 and len(QUERIES) == 9 and len(OUTCOMES) == 4
assert len(set(map(move_state, STATES))) == 64
assert len(set(map(move_query, QUERIES))) == 9
for x in STATES:
    for q in QUERIES:
        assert obs(move_state(x), move_query(q)) == obs(x, q)

beliefs = {frozenset(STATES)}
for x in STATES:
    beliefs.add(frozenset((x,)))
for q1 in QUERIES:
    for y1 in OUTCOMES:
        first = post(STATES, q1, y1)
        if first:
            beliefs.add(first)
        for q2 in QUERIES:
            for y2 in OUTCOMES:
                second = post(first, q2, y2)
                if second:
                    beliefs.add(second)

checks = 0
for belief in beliefs:
    for q in QUERIES:
        for y in OUTCOMES:
            assert step(post(belief, q, y)) == post(step(belief), move_query(q), y)
            checks += 1

# Every first query has a feasible first answer for which every second
# query collides on two distinct states; the first answer is genuinely shared.
witnesses = []
for q1 in QUERIES:
    y1 = (0, 0)
    residual = post(STATES, q1, y1)
    assert len(residual) == 16
    for q2 in QUERIES:
        bins = {}
        pair = None
        for x in sorted(residual):
            y2 = obs(x, q2)
            if y2 in bins:
                pair = (bins[y2], x, y2)
                break
            bins[y2] = x
        assert pair and pair[0] != pair[1]
        assert obs(pair[0], q1) == y1 == obs(pair[1], q1)
        assert obs(pair[0], q2) == pair[2] == obs(pair[1], q2)
        witnesses.append((q1, q2, pair))

# Three fixed paired reads distinguish all original toy states.
schedule = ((0, 0), (1, 1), (2, 2))
signatures = {tuple(obs(x, q) for q in schedule) for x in STATES}
assert len(signatures) == len(STATES)

# Equal belief size does not imply equal observation-game partition profiles.
zero = ((0, 0, 0), (0, 0, 0))
a = ((1, 0, 0), (0, 0, 0))
b = ((1, 1, 1), (1, 1, 1))
profile = lambda belief: Counter(
    tuple(sorted(Counter(obs(x, q) for x in belief).values())) for q in QUERIES
)
assert len({zero, a}) == len({zero, b}) == 2
assert profile((zero, a)) != profile((zero, b))

print(json.dumps({
    "status": "TOY_MODEL_EXACT_TRANSPORT_AND_ADVERSARY_PASS",
    "scope": "abstract 3-binary-edge-slot / 3-binary-corner-slot; NOT P48",
    "legal_toy_states": 64,
    "paired_queries": 9,
    "tested_nonempty_beliefs": len(beliefs),
    "tested_fiber_transport_triplets": checks,
    "online_two_step_collision_witnesses": len(witnesses),
    "fixed_three_query_decoder_signatures": len(signatures),
    "cardinality_only_alias_negative_control": True,
}, sort_keys=True))
