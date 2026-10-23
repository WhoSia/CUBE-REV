#!/usr/bin/env python3
"""Re-check 25-word robust L7 cover with 54-sticker physical move projection."""
from __future__ import annotations
import itertools,json
from pathlib import Path
from physical_edges import ACTIONS,edge_transitions
from robust_observation import signatures

ROOT=Path(__file__).resolve().parents[2]
PATH=ROOT/"docs/observation-generalization/L7_ROBUST_25_WORD_COVER.json"

def verify():
    obj=json.loads(PATH.read_text(encoding="utf-8"))
    words=obj["words"]
    assert len(words)==25 and len({tuple(x) for x in words})==25
    moves=edge_transitions()
    complete=set()
    for word in words:
        assert len(word)==7
        hist=signatures(moves,tuple(ACTIONS.index(x) for x in word))
        for size in (3,4):
            for subset in itertools.combinations(range(12),size):
                if all((hist[a]^hist[b]).bit_count()>=3 for a,b in itertools.combinations(subset,2)):
                    complete.add(sum(1<<a for a in subset))
    counts={str(k):sum(x.bit_count()==k for x in complete) for k in (3,4)}
    assert counts=={"3":220,"4":495},counts
    return {"status":"PHYSICAL_25_WORD_UPPER_BOUND_PASS","counts":counts,
            "dictionary_size":25,"global_optimum_proven":False}

if __name__=="__main__":
    print(json.dumps(verify(),sort_keys=True))
