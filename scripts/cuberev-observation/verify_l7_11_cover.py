#!/usr/bin/env python3
"""Reconstruct full 54-sticker physical oriented-edge transitions and verify the
11-word L7 one-bit error correcting dictionary against ALL 715 source sets."""
import itertools, json
from pathlib import Path
from physical_edges import ACTIONS, edge_transitions
from robust_observation import signatures

CERT = Path(__file__).resolve().parents[2] / "docs/observation-generalization/L7_ROBUST_11_WORD_COVER.json"

def verify():
    data=json.loads(CERT.read_text(encoding="utf8"))
    words=data["words"]
    assert len(words)==11 and len(set(map(tuple,words)))==11
    moves=edge_transitions()
    universe={sum(1<<i for i in subset)
              for k in (3,4) for subset in itertools.combinations(range(12),k)}
    covered=set()
    word_coverage=[]
    for word in words:
        assert len(word)==7 and all(a in ACTIONS for a in word)
        bits=signatures(moves, tuple(ACTIONS.index(a) for a in word))
        good={sum(1<<i for i in subset)
              for k in (3,4) for subset in itertools.combinations(range(12),k)
              if all((bits[a]^bits[b]).bit_count()>=3
                     for a,b in itertools.combinations(subset,2))}
        covered.update(good)
        word_coverage.append(len(good))
    assert universe==covered, f"missing {len(universe-covered)} source sets"
    return {"status":"PHYSICAL_11_WORD_UPPER_BOUND_PASS",
            "words":11,"triples":220,"quadruples":495,
            "per_word_coverage":word_coverage,"global_optimum_proven":False}

if __name__=="__main__":
    print(json.dumps(verify(),sort_keys=True))
