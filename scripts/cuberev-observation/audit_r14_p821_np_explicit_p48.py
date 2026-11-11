#!/usr/bin/env python3
"""CUBE-REV R14-P8.21: bypass unavailable B5 ZIP with the nine IN-REPO
independently discovered P48 5+5 word-pair seeds and nineteen P48 6+6 seeds.

Genuinely replays 48 physical sticker permutations, not pre-labeled outcome
masks. Computes EXACT individual near/parallel (N-P) old/new collision IDs.
The geometric 'no shared endpoint' test is verified AFTER reading physical
outcomes; it is not used to define the physical outcomes.

This is NOT an independent 41-goal B12 positive proof; B5+ B6-negative
word witnesses are the explicit original verification scope.
"""
from collections import Counter
from hashlib import sha256
import json
from itertools import product

from b6_independent_48sticker_goals import (
    EDGE_NAMES, EDGE_POSITION, CORNERS, EDGE_POS,
)
from verify_b6_complete_4845_p48 import (
    B5_FOUR_SEEDS, adjacent_b5_obstructions, adjacent_b6_obstructions,
    ends,
)
from verify_b6_negative_19_pairs_p48 import SEEDS

def midpoint(edge):
    return EDGE_POSITION[edge]

def relative_pairs(core):
    corners=ends(core)
    antipode=frozenset(tuple(-x for x in p) for p in corners)
    star=next(e for e in EDGE_NAMES if ends(e)==antipode)
    near=sorted(e for e in EDGE_NAMES if e!=core and ends(e)&corners)
    parallel=sorted(e for e in EDGE_NAMES
                    if midpoint(e).index(0)==midpoint(core).index(0)
                    and e not in (core,star))
    assert len(near)==4 and len(parallel)==2
    return near, parallel

def main():
    old=adjacent_b5_obstructions()
    newly=adjacent_b6_obstructions()
    assert len(old)==216 and len(newly)==420 and not old&newly
    rows=[]
    physical_old_count=0
    physical_new_count=0
    for h in EDGE_NAMES:
        near,parallel=relative_pairs(h)
        corner_support=ends(h)
        old_pairs,new_pairs=[],[]
        for n,p in product(near,parallel):
            support=corner_support|{EDGE_POSITION[n],EDGE_POSITION[p]}
            assert len(support)==4
            in_old=support in old
            in_new=support in newly
            assert in_old!=in_new,(h,n,p)
            # INDEPENDENT 3D prediction. An original N--P pair has a
            # common cube CORNER endpoint iff it first fails at B6.
            shared=bool(ends(n)&ends(p))
            assert in_old==(not shared),(h,n,p,shared)
            assert in_new==shared,(h,n,p,shared)
            (old_pairs if in_old else new_pairs).append([n,p])
        assert len(old_pairs)==len(new_pairs)==4
        physical_old_count+=len(old_pairs)
        physical_new_count+=len(new_pairs)
        rows.append({'core':h,
                     'already_B5_invalid_NP':old_pairs,
                     'first_B6_invalid_NP':new_pairs})
    assert physical_old_count==physical_new_count==48
    seedbytes=json.dumps({'B5':B5_FOUR_SEEDS,'B6':SEEDS},
                         sort_keys=True,separators=(',',':')).encode()
    print(json.dumps({
        'status':'R14_P821_P48_PHYSICAL_NP_SPLIT_WITHOUT_B5_ARCHIVE_PASS',
        'P48_B5_seeds':len(B5_FOUR_SEEDS),
        'P48_B6_seeds':len(SEEDS),
        'P48_B5_supports_replayed':len(old),
        'P48_B6_supports_replayed':len(newly),
        'cores':len(rows),
        'B5_invalid_NP':physical_old_count,
        'new_B6_invalid_NP':physical_new_count,
        'geometric_rule_B5_bad_iff_no_shared_corner':True,
        'archive_required':False,
        'full_B12_positive_distance_certified_by_this_script':False,
        'seed_text_sha256':sha256(seedbytes).hexdigest(),
        'per_core':rows,
    },sort_keys=True))

if __name__=='__main__':
    main()
