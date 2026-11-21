#!/usr/bin/env python3
"""Construct one physically legal EDGE configuration whose signed
canonicalization changes when the selected normalization gauge changes.

This is a mutation/negative control for forgetting the chosen color map.
It is NOT a claim that the frozen adaptive policy fails: its actual route
retains the chosen map and applies the corresponding correction.
"""
import json
from audit_r029_hall_burnside_graph_quotient import (
    COLORS, group, act, sign, pair_action, stable_sort_sign_correction,
    vectors, hall_fast,
)

if not __debug__:
    raise RuntimeError('Assertions must be enabled. Never run Python -O.')

LABELS=('DL','BL','FL','UL','DB','DF','UB','UF','DR','BR','FR','UR')
LABEL_INDEX={frozenset(pair):idx for idx,pair in enumerate(LABELS)}
assert len(LABEL_INDEX)==12


def build_legal_edge_word(first):
    """Hall matching, with one orientation choice per selected cubie;
    set the twelfth piece orientation to make total edge flip even."""
    def rec(i, unused, rows, flip):
        if i==11:
            assert len(unused)==1
            last=LABELS[next(iter(unused))]
            last=last[::-1] if flip else last
            return rows+[last]
        for idx in sorted(unused):
            piece=LABELS[idx]
            if first[i] not in piece:
                continue
            bit=piece.index(first[i])
            here=piece[bit]+piece[1-bit]
            ans=rec(i+1,unused-{idx},rows+[here],flip ^ bit)
            if ans is not None:
                return ans
        return None
    return rec(0,set(range(12)),[],0)


def piece_sign(word):
    ids=[LABEL_INDEX[frozenset(pair)] for pair in word]
    assert len(ids)==12 and len(set(ids))==12
    return sign(ids)


def is_edge_flip_even(word):
    return sum(pair!=LABELS[LABEL_INDEX[frozenset(pair)]] for pair in word)%2==0


def normalize_word(word,g):
    first=[p[0] for p in word[:11]]
    order=tuple(sorted(range(11),key=lambda i:COLORS.index(g[first[i]])))
    out=[g[word[i][0]]+g[word[i][1]] for i in order+(11,)]
    return out,order


def prove_negative_control():
    G=list(group())
    universe=[v for v in vectors(11,6) if hall_fast(v)]
    assert len(universe)==1362
    reps=sorted({min(act(g,v) for g in G) for v in universe})
    assert len(reps)==52
    identity={c:c for c in COLORS}
    assert identity in G
    chosen=None
    for rep in reps:
        for h in G:
            if act(h,rep)==rep and stable_sort_sign_correction(h,rep)==1:
                chosen=(rep,h)
                break
        if chosen is not None:
            break
    assert chosen is not None
    rep,changed=chosen
    first=''.join(c*n for c,n in zip(COLORS,rep))
    word=build_legal_edge_word(first)
    assert word is not None
    assert ''.join(p[0] for p in word[:11])==first
    assert is_edge_flip_even(word)
    original_sign=piece_sign(word)
    normalized0,order0=normalize_word(word,identity)
    normalized1,order1=normalize_word(word,changed)
    assert order0==tuple(range(11))
    assert ''.join(p[0] for p in normalized0[:11])==first
    assert ''.join(p[0] for p in normalized1[:11])==first
    correction0=stable_sort_sign_correction(identity,rep)
    correction1=stable_sort_sign_correction(changed,rep)
    assert correction0==0 and correction1==1
    sign0=piece_sign(normalized0)
    sign1=piece_sign(normalized1)
    assert sign0==(original_sign^correction0)
    assert sign1==(original_sign^correction1)
    assert sign1!=sign0
    # Mutation: reuse the original gauge correction for the changed gauge.
    incorrectly_recovered=sign1^correction0
    correctly_recovered=sign1^correction1
    assert correctly_recovered==original_sign
    assert incorrectly_recovered!=original_sign
    return {
        'status':'PASS','purpose':'gauge-forgetting counterexample',
        'color_order':COLORS,'first_histogram':rep,'first_prefix':first,
        'twelve_oriented_edge_pieces':word,
        'edge_flip_even':True,
        'chosen_nontrivial_stabilizer':changed,
        'changed_stable_sort_order':order1,
        'original_edge_permutation_sign':original_sign,
        'normalized_sign_with_identity_gauge':sign0,
        'normalized_sign_with_alternate_gauge':sign1,
        'identity_gauge_correction':correction0,
        'alternate_gauge_correction':correction1,
        'correctly_recovered_original_sign':correctly_recovered,
        'badly_recovered_sign_if_gauge_discarded':incorrectly_recovered,
        'negative_control':'PASS: dropping chosen normalization changes recovered sign',
        'scope':'legal oriented edge array and both gauge encodings; no claim of a full 19-frame policy failure'
    }

if __name__=='__main__':
    print(json.dumps(prove_negative_control(),indent=2,ensure_ascii=False))
