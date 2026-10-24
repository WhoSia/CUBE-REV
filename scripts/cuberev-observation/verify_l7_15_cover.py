#!/usr/bin/env python3
"""Standalone replay of the 15-word one-bit-correcting L7 dictionary."""
from __future__ import annotations
import itertools,json
from pathlib import Path
from physical_edges import ACTIONS,edge_transitions
from robust_observation import signatures
FILE=Path(__file__).resolve().parents[2]/"docs/observation-generalization/L7_ROBUST_15_WORD_COVER.json"
def verify():
    d=json.loads(FILE.read_text(encoding="utf-8"))
    assert len(d["words"])==15 and len({tuple(w) for w in d["words"]})==15
    moves=edge_transitions()
    unions=set()
    details=[]
    target={sum(1<<j for j in s) for k in (3,4)
            for s in itertools.combinations(range(12),k)}
    for word in d["words"]:
        assert len(word)==7 and all(x in ACTIONS for x in word)
        sig=signatures(moves,tuple(ACTIONS.index(x) for x in word))
        covered={sum(1<<j for j in s)
                 for k in (3,4) for s in itertools.combinations(range(12),k)
                 if all((sig[a]^sig[b]).bit_count()>=3
                        for a,b in itertools.combinations(s,2))}
        unions.update(covered)
        details.append(len(covered))
    assert unions==target,(len(unions),len(target-unions))
    return {"status":"PHYSICAL_15_WORD_COVER_PASS",
            "selected":15,"covered_triples":220,"covered_quadruples":495,
            "per_word_coverage":details,"global_optimum_proven":False}
if __name__=="__main__":
    print(json.dumps(verify(),sort_keys=True))
