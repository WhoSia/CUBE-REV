#!/usr/bin/env python3
"""Physical irredundancy certificate for the committed 25-word L7 dictionary.

An irredundant dictionary is not necessarily minimum. Reconstruct all 715
source clauses and identify private clauses for each chosen experiment.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
from physical_edges import ACTIONS,edge_transitions
from robust_observation import signatures

ROOT=Path(__file__).resolve().parents[2]
PATH=ROOT/"docs/observation-generalization/L7_ROBUST_25_WORD_COVER.json"

def verify():
    d=json.loads(PATH.read_text())
    moves=edge_transitions()
    target={sum(1<<i for i in sub) for r in (3,4)
            for sub in itertools.combinations(range(12),r)}
    coverage=[]
    for word in d["words"]:
        sig=signatures(moves,tuple(ACTIONS.index(a) for a in word))
        coverage.append({sum(1<<i for i in sub)
                         for r in (3,4)
                         for sub in itertools.combinations(range(12),r)
                         if all((sig[i]^sig[j]).bit_count()>=3
                                for i,j in itertools.combinations(sub,2))})
    assert set().union(*coverage)==target
    private=[len(c-set().union(*(coverage[j] for j in range(len(coverage)) if j!=i)))
             for i,c in enumerate(coverage)]
    assert all(n>0 for n in private), private
    return {"status":"IRREDUNDANT_25_WORDS_PASS",
            "private_clause_counts":private,
            "covered_target_sets":len(target),
            "globally_minimum":False}

if __name__=="__main__":
    print(json.dumps(verify(),sort_keys=True))
