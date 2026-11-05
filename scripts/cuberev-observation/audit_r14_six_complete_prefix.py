#!/usr/bin/env python3
"""Independent R14 finite proof of the 12+8 restricted depth-20 obstruction.

Six unknown oriented edges, color types UR UF UL UB FR FL, with known
relative permutation parity and flip sum. 11520 legal states per parity.
A free query can read any of twelve stationary initial edge facelet slots;
this relaxation is stronger than physically routed two-sensor observations.
No CUBE-REV repository imports: Python stdlib only.
"""
from collections import defaultdict
from functools import lru_cache
from itertools import permutations, product
import json

EDGE_TYPES=('UR','UF','UL','UB','DR','DF','DL','DB','FR','FL','BL','BR')
LEFT=(0,1,2,3,8,9)


def parity(p):
    return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2


def make_states(pp,fp):
    states=[]
    for p in permutations(range(6)):
        if parity(p)!=pp:continue
        for flips in product((0,1),repeat=6):
            if sum(flips)%2!=fp:continue
            states.append(''.join(EDGE_TYPES[LEFT[p[i]]][(side+flips[i])%2]
                                  for i in range(6) for side in range(2)))
    assert len(states)==len(set(states))==11520
    return frozenset(states)


def swap_positions(st):
    return st[2:4]+st[:2]+st[4:]


def flip_first_position(st):
    return st[1]+st[0]+st[2:]


def exact_depth_eight(states):
    ordered=sorted(states)
    q_masks=[]
    for slot in range(12):
        masks=defaultdict(int)
        for i,st in enumerate(ordered):
            masks[st[slot]]|=(1<<i)
        q_masks.append(tuple(masks.values()))
    whole=(1<<len(ordered))-1
    @lru_cache(None)
    def possible(mask,left):
        k=mask.bit_count()
        if k==1:return True
        if not left or k>6**left:return False
        options=[]
        for masks in q_masks:
            branches=tuple(mask&c for c in masks if mask&c)
            if len(branches)<2:continue
            maxbranch=max(b.bit_count() for b in branches)
            if maxbranch>6**(left-1):continue
            options.append((maxbranch,branches))
        for _,branches in sorted(options,key=lambda x:x[0]):
            if all(possible(b,left-1) for b in sorted(branches,key=int.bit_count,reverse=True)):
                return True
        return False
    eight_possible=possible(whole,8)
    assert eight_possible is False
    # Constructive non-adaptive nine-read certificate: four complete edge
    # positions plus one facelet of fifth; parity fixes sixth cubie identity
    # and flip-sum fixes remaining edge orientation.
    nine_slots=tuple(range(9))
    assert len({tuple(st[i] for i in nine_slots) for st in ordered})==11520
    info=possible.cache_info()
    return dict(six_unknown_states=len(ordered),eight_possible=eight_possible,
                nine_fixed_slots=list(nine_slots),nine_distinct_traces=11520,
                eight_dp_states=info.currsize,eight_dp_hits=info.hits)


def main():
    base=make_states(0,0)
    # Coordinate permutations give exact combinatorial bijections between
    # the four parity-conditioned games. Their minimax depth is invariant.
    assert frozenset(map(swap_positions,base))==make_states(1,0)
    assert frozenset(map(flip_first_position,base))==make_states(0,1)
    assert frozenset(flip_first_position(swap_positions(s)) for s in base)==make_states(1,1)
    result=exact_depth_eight(base)
    receipt={"theorem":"any 12-read prefix of six complete edge positions cannot guarantee 20 total frames",
             "scope":"first twelve edge observations exactly two distinct facelets each from six spatial edge positions, adaptive order and locations allowed",
             "remaining_edge_types":[EDGE_TYPES[i] for i in LEFT],
             "parity_cases":4,"parity_equivariance":"exact state-set bijection by swapping two complete positions and first position facelet order",
             "residual_minimax_reads":9,"total_min_worst":21,
             "global_adaptive_horizon_not_proven":"18 <= h <= 21",
             "certificate":result}
    print(json.dumps(receipt,indent=2,sort_keys=True))
    print('R14_SIX_COMPLETE_PREFIX_RESTRICTED_NO20_PASS')

if __name__=='__main__':
    main()
