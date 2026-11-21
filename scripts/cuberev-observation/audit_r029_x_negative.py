#!/usr/bin/env python3
"""Deliberately break the end-to-end nineteen-frame decoding assumptions.

The main audit's positive checks are run separately. These mutations must make
a corresponding complete decoder fail rather than quietly produce wrong output.
"""
import argparse
import json
from collections import Counter
from pathlib import Path
from audit_r029_x_end_to_end import policy,leaf_decoder,route_info,forward,walk,recover
from audit_r029_w_transport_all_prefixes import symmetries,corner_pair_decoder
from verify_19_policy_certificate import assignments

if not __debug__:
    raise RuntimeError('This proof audit uses assertions; Python -O/-OO is forbidden.')


def run(path):
    policies=policy(path)
    pairs=0
    example=None
    for rep,nodes in policies.items():
        leaves=leaf_decoder(rep,nodes)
        for (idx,sign),word in leaves.items():
            other=leaves.get((idx,1-sign))
            if other is not None:
                assert other!=word
                pairs+=1
                if example is None:example=(rep,idx,sign,word,other)
    assert pairs>0
    prefix='BURFDBUFFDR'
    original,rep,m,inv,order,corr=route_info(prefix,symmetries(),policies)
    assert order!=tuple(range(11))
    w,sgn=assignments(original)[0]
    transformed=forward(w,m,order)
    wrong=''.join(m[c] for c in w)
    assert transformed!=wrong
    assert transformed in {x for x,_ in assignments(rep)}
    assert wrong not in {x for x,_ in assignments(rep)}
    # Missing the second ordered color loses injectivity of the corner decoder.
    dec=corner_pair_decoder()
    collisions={}
    for pair,value in dec.items():
        collisions.setdefault(pair[0],set()).add(value[0])
    assert any(len(v)>1 for v in collisions.values())
    return {'status':'PASS','negative_controls':3,
            'same_leaf_opposite_sign_witnesses':pairs,
            'examples':[
                'Flipping terminal corner parity selects a different surviving edge word',
                'Omitting original-to-representative 11-slot reorder violates the representative alphabet',
                'Reading only one instead of two cyclic corner stickers fails oriented-cubie injectivity'],
            'scope':'deliberate missing-assumption tests for a 19-frame semantic decoder'}


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--certificate',required=True)
    args=ap.parse_args();print(json.dumps(run(args.certificate),indent=2))
