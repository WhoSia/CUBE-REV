#!/usr/bin/env python3
"""Replay five L7 erasure-correcting words against all 715 physical source sets."""
from __future__ import annotations
import itertools,json
from pathlib import Path
from physical_edges import ACTIONS,edge_transitions
from robust_observation import signatures
from sensor_symmetry import rotations,conjugacy_candidate
ROOT=Path(__file__).resolve().parents[2]
PATH=ROOT/"docs/observation-generalization/L7_ERASURE1_5_WORD_COVER.json"
def verify():
    words=json.loads(PATH.read_text())["words"]
    assert len(words)==5 and len({tuple(w) for w in words})==5
    moves=edge_transitions()
    target={sum(1<<a for a in s) for n in (3,4)
            for s in itertools.combinations(range(12),n)}
    cov=[]
    for word in words:
        assert len(word)==7 and all(a in ACTIONS for a in word)
        signs=signatures(moves,tuple(ACTIONS.index(a) for a in word))
        cov.append({sum(1<<a for a in s) for n in (3,4)
            for s in itertools.combinations(range(12),n)
            if all((signs[a]^signs[b]).bit_count()>=2
                   for a,b in itertools.combinations(s,2))})
    union=set().union(*cov)
    assert union==target,(len(union),len(target-union))
    private=[len(c-set().union(*(cov[j] for j in range(5) if j!=i)))
             for i,c in enumerate(cov)]
    # V4 changes both source indices and action labels. Verify exact
    # transported incidence, not only the total cardinalities.
    orbit_verified=0;orbit_words=set()
    for _,_,transform in rotations():
        _,alpha,T=conjugacy_candidate(transform)
        if not (all((T[s]&1)==(s&1) for s in range(24)) and
                all(T[moves[a][s]]==moves[alpha[a]][T[s]]
                    for a in range(18) for s in range(24))):continue
        p=[T[2*i]//2 for i in range(12)]
        for word,coverage in zip(words,cov):
            rotated=tuple(ACTIONS[alpha[ACTIONS.index(a)]] for a in word)
            orbit_words.add(rotated)
            h=signatures(moves,tuple(ACTIONS.index(a) for a in rotated))
            actual={sum(1<<a for a in s) for n in (3,4)
                for s in itertools.combinations(range(12),n)
                if all((h[a]^h[b]).bit_count()>=2
                       for a,b in itertools.combinations(s,2))}
            transported={sum(1<<p[i] for i in range(12) if mask>>i&1)
                         for mask in coverage}
            assert actual==transported
            orbit_verified+=1
    assert orbit_verified==20
    return {"status":"PHYSICAL_ERASURE1_FIVE_WORD_PASS",
            "words":5,"covered":len(union),"private_by_word":private,
            "V4_verified_word_action_pairs":orbit_verified,
            "distinct_V4_orbit_words":len(orbit_words),
            "global_optimum_proven":False}
if __name__=="__main__":print(json.dumps(verify(),sort_keys=True))
