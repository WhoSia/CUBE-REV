#!/usr/bin/env python3
"""Evaluate a physical robust observation dictionary, not merely witnesses.

Every dictionary word is replayed on fresh 54-sticker-derived edge transitions.
The union is a valid *coverage certificate*. The greedy utility below chooses a
subset of the supplied dictionary only; it does not assert global optimality.
"""
from __future__ import annotations
import argparse
import itertools
import json
from physical_edges import ACTIONS, edge_transitions
from robust_observation import signatures

SEED_WORDS = (
    ("U","R","F","R2","B","U2","F"),
    ("U","R","F","U","F","U2","F"),
    ("U","R'","B","R","B","R","B"),
    ("B","F","D","B'","R'","F","R"),
)

def covered_by_word(moves, word, min_distance=3, min_size=3, max_size=5):
    sig = signatures(moves, tuple(ACTIONS.index(x) for x in word))
    result = set()
    for r in range(min_size, max_size+1):
        for subset in itertools.combinations(range(12),r):
            if all((sig[a]^sig[b]).bit_count()>=min_distance
                   for a,b in itertools.combinations(subset,2)):
                result.add(sum(1<<i for i in subset))
    return result

def evaluate(words=SEED_WORDS, min_distance=3):
    moves=edge_transitions()
    seen=set()
    rows=[]
    for word in words:
        cov=covered_by_word(moves,word,min_distance)
        rows.append({"word":" ".join(word),"by_size":{
            str(r):sum(m.bit_count()==r for m in cov) for r in range(3,6)},
            "new_coverage":len(cov-seen)})
        seen.update(cov)
    return {"dictionary_size":len(words),"coverage_by_size":{
        str(r):sum(m.bit_count()==r for m in seen) for r in range(3,6)},
        "per_word":rows,"status":"WITNESS_DICTIONARY_COVERAGE_ONLY",
        "global_minimum_proven":False}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--min-distance",type=int,default=3)
    args=ap.parse_args()
    print(json.dumps(evaluate(min_distance=args.min_distance),sort_keys=True))
if __name__=="__main__":main()
