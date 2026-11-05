#!/usr/bin/env python3
"""R9: full physical color-feedback-vs-fixed-query separation, four-edge court.

96 legal configurations per known remaining four edge types and prescribed
edge permutation/flip parity. For ALL 495 subsets x ALL FOUR parity choices:
- calculate exact shortest PRECOMMITTED slot set for every legal arrangement;
- compare with independently obtained R8 exact worst-case adaptive depth;
- extract and replay a conditional policy on all 96 states.
This is a corner-oracle, arbitrary-edge-slot-access residual problem, NOT
a 20-frame full-cube solution and NOT measured human cognition.
"""
from collections import Counter
from itertools import combinations
from audit_r8_four_edge_adaptive_subproblems import (
    TYPES, states_for, minimax_depth, graph_shape,
    verify_constructive_policy,
)

SLOT_SETS = {q: tuple(combinations(range(8), q)) for q in (3, 4)}

def fixed_depth(states):
    assert len(states) == 96
    # Two readouts have <= 36 transcripts; cannot distinguish 96 states.
    for q in (3, 4):
        for slots in SLOT_SETS[q]:
            if len({tuple(state[i] for i in slots) for state in states}) == 96:
                return q, slots
    # Parity gives this five-slot universal distinguishing schedule.
    slots = (0, 1, 2, 3, 4)
    assert len({tuple(state[i] for i in slots) for state in states}) == 96
    return 5, slots

def verify_fixed_replay(states, slots):
    transcripts = {}
    for i, state in enumerate(states):
        read = tuple(state[j] for j in slots)
        assert read not in transcripts, (i, transcripts.get(read))
        transcripts[read] = i
    assert len(transcripts) == len(states) == 96

def audit():
    crossed = Counter()
    graph_counter = Counter()
    parity_cases = 0
    policy_replays = 0
    exemplars = {}
    for remaining in combinations(range(12), 4):
        by_parity = []
        for pp in (0, 1):
            for fp in (0, 1):
                states = states_for(remaining, pp, fp)
                fixed, slots = fixed_depth(states)
                adaptive = minimax_depth(remaining, pp, fp)
                assert adaptive <= fixed <= 5
                assert fixed-adaptive in (0, 1), (remaining, pp, fp, fixed, adaptive)
                verify_fixed_replay(states, slots)
                # The original R8 policy routine extracts and replays all
                # 96 physical-color branches, not just a feasibility boolean.
                verify_constructive_policy(remaining, pp, fp, adaptive)
                policy_replays += len(states)
                parity_cases += 1
                by_parity.append((adaptive, fixed))
        assert len(set(by_parity)) == 1, (remaining, by_parity)
        pair = by_parity[0]
        crossed[pair] += 1
        shape = graph_shape(remaining)
        graph_counter[(shape, pair)] += 1
        exemplars.setdefault(pair, remaining)

    expected = {(3,4):72, (4,4):225, (4,5):144, (5,5):54}
    assert crossed == expected, crossed
    assert parity_cases == 1980
    assert policy_replays == 1980*96
    assert sum(n for (a,f),n in crossed.items() if f>a) == 216
    # In the audited graph family, fixed 4 precisely corresponds to all
    # four unobserved edge types having incidence degree at most 2.
    for (shape,(adaptive,fixed)),count in graph_counter.items():
        degrees, components = shape
        assert (fixed == 4) == (degrees[0] <= 2), (shape,fixed)
        assert count > 0
    adaptive_sum = sum(a*n for (a,f),n in crossed.items())
    fixed_sum = sum(f*n for (a,f),n in crossed.items())
    assert (adaptive_sum, fixed_sum) == (1962, 2178)
    print("R9_EXACT_FEEDBACK_SEPARATION_PASS",
          "remaining_subsets=495", "parity_cases=1980",
          "adaptive_better=216", "equal=279",
          "adaptive_depth_sum=1962", "fixed_depth_sum=2178")
    print("R9_CROSSTAB_ADAPTIVE_FIXED",
          ";".join(f"{a}:{f}:{crossed[(a,f)]}" for a,f in sorted(crossed)))
    print("R9_ALL_PARITY_EXPLICIT_POLICY_REPLAY_PASS",
          "physical_conditional_states",policy_replays)
    for (a,f),remaining in sorted(exemplars.items()):
        print("R9_EXEMPLAR", "adaptive",a,"fixed",f,
              "remaining_types","/".join("".join(TYPES[i]) for i in remaining))
    print("R9_BOUNDARY complete corner oracle and free edge slot access;",
          "not a global color-cube adaptive upper bound")
    return crossed

if __name__=="__main__":
    audit()
