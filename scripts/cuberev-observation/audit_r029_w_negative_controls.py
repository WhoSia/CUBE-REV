#!/usr/bin/env python3
"""Mutation/negative checks for the W transport, corner, and route audit."""
import json
from pathlib import Path

from audit_r029_w_transport_all_prefixes import (
    COLORS, LABELS, assignments, count_vectors, expected_prefix, permute_vector,
    symmetries, relabel_sign, permutation_parity,
)
from audit_r029_w_corner_geometric_decoder import CORNERS, geometry
from audit_r029_w_joint_routes import table, follow


def run():
    maps=symmetries()
    found=False
    for counts in count_vectors():
        original=expected_prefix(counts)
        canonical=min(permute_vector(counts,m) for m in maps)
        m=next(m for m in maps if permute_vector(counts,m)==canonical)
        order=tuple(sorted(range(11),key=lambda i: COLORS.index(m[original[i]])))
        label_bit=relabel_sign(m)
        position_bit=permutation_parity(order+(11,))
        if label_bit^position_bit:
            word,sign=assignments(original)[0]
            actual=''.join(m[word[i]] for i in order)+''.join(m[c] for c in word[11:])
            corpus=set(assignments(expected_prefix(canonical)))
            assert (actual,sign^position_bit^label_bit) in corpus
            assert (actual,sign) not in corpus, 'Missing the sign correction should be rejected.'
            found=True
            break
    assert found
    # One color cannot identify every oriented corner: the second read is essential.
    all_corner_words=[c[k:]+c[:k] for c in CORNERS for k in range(3)]
    assert len({w[:1] for w in all_corner_words}) < len(all_corner_words)
    assert len({w[:2] for w in all_corner_words}) == len(all_corner_words)
    # Modifying one route must invalidate the advertised endpoint.
    routes=table(); moves=geometry()
    corrupt=list(routes[0])+[0]
    assert follow(moves,routes[0],0)==0 and follow(moves,routes[0],24)==24
    assert (follow(moves,corrupt,0),follow(moves,corrupt,24)) != (0,24)
    return {'status':'PASS','rejected_mutations':3,
            'cases':['omit label/position sign correction','discard second corner read','corrupt joint probe route']}

if __name__=='__main__':print(json.dumps(run(),indent=2))
