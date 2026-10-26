#!/usr/bin/env python3
"""Physical counterexample: same Hamming distance, different burst survival.

Rebuilds 54-sticker-induced oriented-edge transitions and checks the
specific 7-HTM word L' F B' D U2 B F'. In particular, a distance-two
pair at nonconsecutive time positions survives every consecutive
two-observation erasure but cannot correct one arbitrary substitution.
The eleven-word existing dictionary has equal per-word substitution and
burst-erasure coverage; that is an observed finite certificate, NOT a
general law of the physical automaton.
"""
from __future__ import annotations
import json
from physical_edges import ACTIONS,edge_transitions
from robust_observation import signatures
from channel_model_transfer import (MODELS,word_coverage,ROOT,audit,
                                    distinguishes_pair)

WITNESS=("L'","F","B'","D","U2","B","F'")
SOURCE_PAIR=(1,3)
EXPECTED={ "substitution1":12,"erasure1":125,"burst_erasure2":44 }

def run():
    moves=edge_transitions()
    codes=signatures(moves,tuple(ACTIONS.index(a) for a in WITNESS))
    a,b=SOURCE_PAIR
    assert codes[a]==62 and codes[b]==28
    difference=codes[a]^codes[b]
    assert difference==34 and difference.bit_count()==2
    assert not distinguishes_pair(codes[a],codes[b],7,"substitution1")
    assert distinguishes_pair(codes[a],codes[b],7,"burst_erasure2")
    counts={model:len(word_coverage(moves,WITNESS,model)) for model in MODELS}
    assert counts==EXPECTED,(counts,EXPECTED)
    incumbent=audit(ROOT/"docs/observation-generalization/L7_ROBUST_11_WORD_COVER.json")
    assert all(incumbent["models"][m]["full_cover"] for m in MODELS)
    # More strongly, compare the whole physical source-coverage family per
    # experiment, rather than merely the total union count.
    from channel_model_transfer import word_coverage as cover
    words=json.loads((ROOT/"docs/observation-generalization/L7_ROBUST_11_WORD_COVER.json").read_text())["words"]
    equal=all(cover(moves,w,"substitution1")==cover(moves,w,"burst_erasure2") for w in words)
    assert equal
    return {"status":"PHYSICAL_TIME_STRUCTURE_COUNTEREXAMPLE_PASS",
            "actions":list(WITNESS),"initial_pair":list(SOURCE_PAIR),
            "binary_signatures_lsb_time_order":[codes[a],codes[b]],
            "xor_difference":difference,"difference_time_positions":[1,5],
            "source_coverage_counts":counts,
            "incumbent_11_words_equal_substitution_and_burst":equal,
            "incumbent_full_cover_each_model":True,
            "novelty_unverified":True}

if __name__=="__main__":
    print(json.dumps(run(),indent=2,sort_keys=True))
