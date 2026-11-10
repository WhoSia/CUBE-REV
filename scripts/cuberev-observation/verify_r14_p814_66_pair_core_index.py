#!/usr/bin/env python3
"""R14-P8.14: replay deterministic 66 edge-pair -> positive16-core index.

Read-only finite provenance checker; original 41-class physical B12
positivity is inherited from earlier certificates, NOT re-proven here.
"""
from collections import Counter
from itertools import combinations
from pathlib import Path
import json
from audit_r14_p813_complete_minimal_base_spectrum import EDGES, PAIRS

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/"data/0.28/R14_P814_ALL_66_EDGE_PAIRS_POSITIVE16_CORE_INDEX_20261110.json"

def main():
    index=json.loads(SOURCE.read_text(encoding="utf-8"))
    assert index["schema"]=="CUBE_REV_R14_P814_66_EDGE_PAIR_CORE_PROOF_INDEX_V1"
    assert index["pair_count"]==66 and len(index["rows"])==66
    pairs={frozenset(pair) for pair in combinations(EDGES,2)}
    witnessed=set()
    hist=Counter()
    unique=0
    selected_cores=Counter()
    for record in index["rows"]:
        q=frozenset(record["edge_pair"])
        assert len(q)==2 and q<=set(EDGES) and q not in witnessed
        witnessed.add(q)
        expected=sorted(h for h in EDGES if q in PAIRS[h])
        assert expected and record["all_positive16_cores"]==expected
        assert record["selected_positive16_core"]==expected[0]
        assert q in PAIRS[record["selected_positive16_core"]]
        selected_cores[record["selected_positive16_core"]]+=1
        hist[len(expected)]+=1
        if len(expected)==1: unique+=1
    assert witnessed==pairs
    assert hist=={1:24,2:6,3:24,4:12}
    assert index["core_multiplicity_histogram"]=={str(k):v for k,v in hist.items()}
    assert unique==index["unique_core_pair_count"]==24
    assert sum(selected_cores.values())==66
    print(json.dumps({
      "result":"R14_P814_66_PAIR_CORE_INDEX_REPLAY_PASS",
      "all_edge_pairs":len(witnessed),
      "positive16_selected_layouts":66,
      "uniquely_available_core":unique,
      "candidate_core_multiplicities":dict(sorted(hist.items())),
      "physical_B12_41_class_replayed":False
    },sort_keys=True))

if __name__=="__main__":
    main()
