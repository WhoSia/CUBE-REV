#!/usr/bin/env python3
"""Validate every word of the L7 robust 27-experiment 3/4-source cover.

Replays the 18 HTM actions using newly built 54-sticker physical geometry,
independently recomputes each binary observation signature and all 715 source
clauses, and verifies coverage. Produces an inspectable receipt.
"""
from __future__ import annotations
import itertools
import json
from pathlib import Path
from physical_edges import ACTIONS, edge_transitions
from robust_observation import signatures

ROOT=Path(__file__).resolve().parents[2]
INPUT=ROOT/"docs/observation-generalization/L7_ROBUST_27_WORD_COVER.json"

def verify(path:Path=INPUT)->dict:
    raw=json.loads(path.read_text(encoding="utf-8"))
    assert raw["schema"]=="cube-rev.robust-dictionary-v1"
    words=raw["words"]
    assert len(words)==27
    move_tables=edge_transitions()
    covered=set()
    coverage_per_word=[]
    for w in words:
        assert len(w)==7 and all(a in ACTIONS for a in w),w
        sig=signatures(move_tables,tuple(ACTIONS.index(a) for a in w))
        current=set()
        for k in (3,4):
            for src in itertools.combinations(range(12),k):
                if all((sig[a]^sig[b]).bit_count()>=3
                       for a,b in itertools.combinations(src,2)):
                    current.add(sum(1<<j for j in src))
        coverage_per_word.append(len(current))
        covered.update(current)
    by_size={str(k):sum(m.bit_count()==k for m in covered) for k in (3,4)}
    assert by_size=={"3":220,"4":495}, by_size
    return {"status":"PHYSICAL_27_WORD_UPPER_BOUND_PASS",
            "dictionary_size":len(words),"length":7,
            "source_family":"ALL_12_CHOOSE_3_AND_12_CHOOSE_4",
            "one_bit_correction":True,"covered":by_size,
            "per_word_counts":coverage_per_word,
            "globally_optimal":False}

if __name__=="__main__":
    print(json.dumps(verify(),sort_keys=True))
