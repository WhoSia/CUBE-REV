#!/usr/bin/env python3
"""Physically certify the Klein-four action on L7 robust covering columns.

The true orbit operates simultaneously on experiment words and source-set
rows. Two rotated columns generally cover RE-LABELED sources, so picking just
one orbit representative without transforming rows is unsound.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
from sensor_symmetry import analyze,rotations,conjugacy_candidate
from physical_edges import ACTIONS,edge_transitions
from robust_observation import signatures

CERT=Path(__file__).resolve().parents[2]/"docs/observation-generalization/L7_ROBUST_11_WORD_COVER.json"
SOURCES=tuple(sum(1<<i for i in c) for k in (3,4) for c in itertools.combinations(range(12),k))

def cover(moves,word):
    hist=signatures(moves,word)
    return frozenset(mask for mask in SOURCES if
        all((hist[a]^hist[b]).bit_count()>=3
            for a,b in itertools.combinations(
                [i for i in range(12) if mask>>i&1],2)))

def audit():
    moves=edge_transitions()
    raw=json.loads(CERT.read_text(encoding="utf8"))
    original=[tuple(ACTIONS.index(a) for a in word) for word in raw["words"]]
    assert len(original)==11
    symmetries=[]
    for _,_,transform in rotations():
        _,alpha,T=conjugacy_candidate(transform)
        if all((T[x]&1)==(x&1) for x in range(24)) and all(
            T[moves[a][x]]==moves[alpha[a]][T[x]]
            for a in range(18) for x in range(24)):
            permutation=tuple(T[2*i]//2 for i in range(12))
            assert sorted(permutation)==list(range(12))
            symmetries.append((alpha,permutation))
    assert len(symmetries)==4
    generated={}
    for word in original:
        sig=signatures(moves,word)
        cov=cover(moves,word)
        for alpha,p in symmetries:
            transformed=tuple(alpha[a] for a in word)
            transformed_signatures=signatures(moves,transformed)
            assert all(transformed_signatures[p[i]]==sig[i] for i in range(12))
            transformed_coverage=cover(moves,transformed)
            transported=frozenset(sum(1<<p[i] for i in range(12) if mask>>i&1) for mask in cov)
            assert transformed_coverage==transported
            generated[transformed]=transformed_coverage
    assert set().union(*(cover(moves,w) for w in original))==set(SOURCES)
    return {"status":"SENSOR_ORBIT_COLUMNS_AND_ROWS_PASS",
            "source_family_size":len(SOURCES),
            "sensor_group_order":len(symmetries),
            "original_words":len(original),
            "orbit_words":len(generated),
            "distinct_incidence_columns":len(set(generated.values())),
            "checked_word_symmetry_pairs":len(original)*len(symmetries),
            "global_robust_Mstar_unchanged":True}
if __name__=="__main__":
    print(json.dumps(audit(),sort_keys=True))
