#!/usr/bin/env python3
"""Realizable observation-conditioned stopping under one KNOWN erasure.

The public initial candidate SOURCE SET R is provided before execution.
A legal length-7 word is selected in advance (no mid-word action branching).
During execution the controller sees each actual bit or a visible erasure
symbol. It stops only when exactly one source in R is compatible with all
received non-erased readings. The decision never uses the hidden true source.

Worst-case cost ranges over all source states and erasure positions,
including no erasure. This is an executable fixed-word stopping policy;
unlike a source-aware prefix oracle, it has a well-defined information
state. Optimize *per known R* over the five committed words only.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
from physical_edges import ACTIONS,edge_transitions
from robust_observation import signatures
ROOT=Path(__file__).resolve().parents[2]
CERT=ROOT/"docs/observation-generalization/L7_ERASURE1_5_WORD_COVER.json"

def trace_stop(signatures_by_source,source_set,true_source,erasure_position):
    observed=[]
    for depth in range(7):
        bit=(signatures_by_source[true_source]>>depth)&1
        observed.append(None if depth==erasure_position else bit)
        possible=[src for src in source_set
                  if all(v is None or ((signatures_by_source[src]>>t)&1)==v
                         for t,v in enumerate(observed))]
        assert true_source in possible
        if len(possible)==1:return depth+1
    raise AssertionError("source not identified despite certified dictionary word")

def evaluate():
    words=json.loads(CERT.read_text())["words"]
    moves=edge_transitions()
    sigs=[signatures(moves,tuple(ACTIONS.index(a) for a in w)) for w in words]
    histogram={str(i):0 for i in range(1,8)}
    chosen_counts=[0]*len(words)
    total=0;cases=0
    for size in (3,4):
        for group in itertools.combinations(range(12),size):
            choices=[]
            for i,h in enumerate(sigs):
                try:
                    worst=max(trace_stop(h,group,true,erasure)
                              for true in group for erasure in [None,*range(7)])
                    choices.append((worst,i))
                except AssertionError:
                    continue
            assert choices,(group,"no sound length7 policy")
            worst,i=min(choices)
            chosen_counts[i]+=1;histogram[str(worst)]+=1
            total+=worst;cases+=1
    assert cases==715
    return {"status":"OBSERVATION_CONDITIONED_FIXED_WORD_POLICY_PASS",
            "public_information":"source candidate set R",
            "hidden_information":"true source and erasure event",
            "actions":"fixed selected word, no observation-contingent action switch",
            "stop_rule":"unique source compatible with received non-erased symbols",
            "objective":"min over five words of worst-case stopping depth per public R",
            "source_sets":cases,"worst_case_prefix_histogram":histogram,
            "mean_per_source_set_worst_case_moves":total/cases,
            "word_assignments":chosen_counts,
            "fully_adaptive_global_optimum_proven":False}
if __name__=="__main__":print(json.dumps(evaluate(),sort_keys=True))
