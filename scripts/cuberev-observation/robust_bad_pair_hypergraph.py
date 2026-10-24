#!/usr/bin/env python3
"""Exact bad-pair hypergraph view of robust observation dictionaries.

For a fixed length-L physical word, an edge (i,j) is 'bad' when the Hamming
distance between observation histories is < 2t+1. A source subset R is
covered iff it is independent in that bad-pair graph. A dictionary fails R
iff every word's bad-pair graph contains some edge entirely inside R.
This equivalence is exact; it works also for nonzero error tolerance.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
from physical_edges import ACTIONS,edge_transitions
from robust_observation import signatures

ROOT=Path(__file__).resolve().parents[2]
CERT=ROOT/"docs/observation-generalization/L7_ROBUST_11_WORD_COVER.json"

def check():
    words=json.loads(CERT.read_text())["words"]
    moves=edge_transitions()
    graphs=[]
    for word in words:
        codes=signatures(moves,tuple(ACTIONS.index(a) for a in word))
        bad={(a,b) for a,b in itertools.combinations(range(12),2)
             if (codes[a]^codes[b]).bit_count()<3}
        graphs.append(bad)
    counts={3:0,4:0}
    for size in (3,4):
        for source in itertools.combinations(range(12),size):
            induced=set(itertools.combinations(source,2))
            # Need at least one experiment with no bad edge in the source.
            assert any(not (bad & induced) for bad in graphs)
            counts[size]+=1
    # Structural summary only: no false global-optimality assertion.
    return {"status":"BAD_PAIR_HYPERGRAPH_11_CERT_PASS",
            "bad_edges_per_word":[len(x) for x in graphs],
            "independent_source_counts":counts,
            "general_theorem":"covered iff some experiment has zero bad pairs inside source",
            "global_minimum_proven":False}

if __name__=="__main__":
    print(json.dumps(check(),sort_keys=True))
