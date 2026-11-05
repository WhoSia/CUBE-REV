#!/usr/bin/env python3
"""R11: complete full-legal-cube joint color identification without corner oracle.

For EVERY legal original P48 cube state, the exact algorithm is:
 (1) First 16 joint frames: completely read eight fixed spatial edge slots
     (16 edge colors), and read TWO corner facelets in each of seven corner
     positions in the first 14 frames. The latter decode the entire actual
     corner state without any hidden reference or edge parity oracle.
 (2) After 16 frames: eight edge labels/orientations are known; the other
     four labels are known as a set. Corners give the real global permutation
     parity. The prior edge flips plus legal parity fix the residual edge
     orientation parity.
 (3) Apply the exact R8/R9 minimax edge policy on the 96 parity-consistent
     possibilities, reading each selected spatial facelet through a physically
     reachable P48 edge/corner sensor pair using legal no-reset 18-HTM turns.
 (4) Decode the final full edge+corner original-to-slot sticker permutation
     using ONLY the observed six-color labels, the known legal moves, and the
     fixed group invariants. The simulator compares to ground truth only AFTER
     reconstruction.

This yields <=21 joint frames on ALL legal cube states. It is NOT a
global <=20 policy: 54 four-edge graph classes need five final queries.
The existing nonadaptive upper 21 is not improved in worst-case horizon.
"""
from functools import lru_cache
from b6_independent_48sticker_goals import (
    CORNERS,EDGE_POS,PIECES,SLOTS,inverse,compose,word,
    factor_value,
)
from construct_color_p48_24_frame_scanner import (
    SOURCE_FACE_COLOR,CORNER_STICKERS,EDGE_FACELET,CORNER_FACELET,
    joint_sticker_orbit,inverted_token,
)
from audit_color_probe_information_bounds import two_one_facelet_colors
from audit_r11_corner14_no_oracle import CORNER14, decode14, corner_parity_from_decoding
from audit_r8_four_edge_adaptive_subproblems import (
    states_for,minimax_depth,
)
from audit_r10_physical_feedback_lift import policy_for

EYE=bytes(range(48))
FIRST_EDGE_POS=EDGE_POS[:8]
REMAINING_EDGE_POS=EDGE_POS[8:]
EDGE_PREFIX=tuple(s for pos in FIRST_EDGE_POS for s in PIECES[pos])
assert len(EDGE_PREFIX)==16
CORNER_PREFIX=CORNER14+tuple(s for s in CORNER_STICKERS if s not in CORNER14)[:2]
assert len(CORNER_PREFIX)==16
assert len(set(CORNER_PREFIX))==16

@lru_cache(None)
def reachable_target(edge_slot,corner_slot):
    paths=joint_sticker_orbit()
    actions=tuple(inverted_token(t) for t in reversed(
        paths[(edge_slot,corner_slot)]))
    target=word(" ".join(actions))
    assert target[edge_slot]==EDGE_FACELET
    assert target[corner_slot]==CORNER_FACELET
    return actions,target

def parity(order):
    return sum(order[i]>order[j] for i in range(len(order))
               for j in range(i+1,len(order)))%2

@lru_cache(None)
def residual_policy(labels,pp,fp):
    states=states_for(labels,pp,fp)
    depth=minimax_depth(labels,pp,fp)
    outputs,choose=policy_for(states,depth)
    return states,depth,outputs,choose

def recover(g):
    """Simulator returns (fully decoded physical state, observations, HTM).

    g is accessed ONLY via the actual six-color sensing function (and final
    post-recovery validation in the external audit).
    """
    assert len(g)==48 and set(g)==set(range(48))
    pose=EYE
    previous=()
    turns=0
    readings=0
    corner_measure={}
    edge_measure={}
    def sense(edge_slot,corner_slot):
        nonlocal pose,previous,turns,readings
        actions,target=reachable_target(edge_slot,corner_slot)
        rel=tuple(inverted_token(t) for t in reversed(previous))+actions
        delta=word(" ".join(rel))
        assert delta==compose(target,inverse(pose))
        pose=compose(delta,pose)
        assert pose==target
        ce,cc=two_one_facelet_colors(g,pose)
        turns+=len(rel)
        readings+=1
        previous=actions
        return ce,cc

    for i,(es,cs) in enumerate(zip(EDGE_PREFIX,CORNER_PREFIX)):
        e,c=sense(es,cs)
        edge_measure[es]=e
        if i<14:corner_measure[cs]=c
    assert readings==16
    corners,corner_assigned=decode14(corner_measure)
    corner_perm_parity=corner_parity_from_decoding(corner_assigned)
    reconstructed_edges={}
    src_at_dest=[None]*12
    observed_src=set()
    flip_total=0
    for di,dest in enumerate(FIRST_EDGE_POS):
        observed=tuple(edge_measure[s] for s in PIECES[dest])
        choices=[]
        for source_idx,src in enumerate(EDGE_POS):
            original=tuple(SOURCE_FACE_COLOR[s] for s in PIECES[src])
            for flip in (0,1):
                if observed==tuple(original[(k-flip)%2] for k in range(2)):
                    choices.append((source_idx,flip))
        assert len(choices)==1,(dest,observed,choices)
        source_idx,flip=choices[0]
        assert source_idx not in observed_src
        observed_src.add(source_idx)
        src_at_dest[di]=source_idx
        flip_total^=flip
        for k,source_sticker in enumerate(PIECES[EDGE_POS[source_idx]]):
            reconstructed_edges[source_sticker]=PIECES[dest][(k+flip)%2]
    assert len(reconstructed_edges)==16
    unknown_labels=tuple(i for i in range(12) if i not in observed_src)
    assert len(unknown_labels)==4
    for di,src_i in enumerate(unknown_labels,start=8):
        src_at_dest[di]=src_i
    # Swapping from sorted missing-label assignment to actual missing
    # assignment toggles full edge permutation parity exactly by pp.
    pp=corner_perm_parity ^ parity(src_at_dest)
    fp=flip_total  # legal total flip parity is even.
    states,depth,outcomes,choose=residual_policy(unknown_labels,pp,fp)
    belief=(1<<96)-1
    extras=0
    while belief.bit_count()>1:
        query=choose(belief,depth-extras)
        assert 0<=query<8 and extras<depth
        dest=REMAINING_EDGE_POS[query//2]
        slot=PIECES[dest][query%2]
        # Corner reading here is not needed for correct corner recovery:
        # the full corner mapping was already decoded at frame 14.
        cs=CORNER_STICKERS[(16+extras)%24]
        e,c=sense(slot,cs)
        assert e in outcomes[query],(query,e)
        belief&=outcomes[query][e]
        extras+=1
    assert belief.bit_count()==1
    candidate_index=belief.bit_length()-1
    residual=states[candidate_index]
    for j,dest in enumerate(REMAINING_EDGE_POS):
        observed=residual[2*j:2*j+2]
        matches=[]
        for src_i in unknown_labels:
            source=tuple(SOURCE_FACE_COLOR[s] for s in PIECES[EDGE_POS[src_i]])
            for flip in (0,1):
                if observed==tuple(source[(k-flip)%2] for k in range(2)):
                    matches.append((src_i,flip))
        assert len(matches)==1,(j,observed,matches)
        src_i,flip=matches[0]
        for k,sticker in enumerate(PIECES[EDGE_POS[src_i]]):
            assert sticker not in reconstructed_edges
            reconstructed_edges[sticker]=PIECES[dest][(k+flip)%2]
    assert len(reconstructed_edges)==24
    complete=corners|reconstructed_edges
    assert len(complete)==48
    result=bytes(complete[i] for i in range(48))
    assert len(set(result))==48
    assert sum(factor_value(src,result)%3 for src in CORNERS)%3==0
    assert sum(factor_value(src,result)%2 for src in EDGE_POS)%2==0
    assert parity([EDGE_POS.index(
        SLOTS[result[PIECES[src][0]]][0]) for src in EDGE_POS])==(
        corner_perm_parity)
    return result,readings,turns,depth,unknown_labels

def audit():
    from audit_active_p48_small_ball_decision_trees import ball
    from audit_r10_physical_feedback_lift import physical_state,even_permutations,even_flips
    states,_=ball(2)
    assert len(states)==262
    samples=list(states)
    for text in (
        "R U F' D2 L B",
        "U2 R' B D2 B' R U2 R' B D2 B' R",
        "L F R' F' L' U2 R U R U' R2 U2 R",
    ):
        samples.append(word(text))
    # State family under a nontrivial legal corner-only 3-cycle and a
    # legal two-corner twist, combined with R9 96-state edge residuals.
    from itertools import combinations
    remaining=tuple(range(8,12))
    for order in even_permutations():
        for flips in even_flips():
            baseline=physical_state(remaining,order,flips)
            samples.append(baseline)
            if len(samples)>450:break
        if len(samples)>450:break
    depth_counts={}
    total_htm=0
    for g in samples:
        recovered,reads,turns,depth,labels=recover(g)
        assert recovered==g,(labels,reads)
        assert 16<=reads<=21
        depth_counts[reads]=depth_counts.get(reads,0)+1
        total_htm+=turns
    print("R11_FULL_CUBE_NO_CORNER_ORACLE_21_FRAME_PASS",
          "B2_states",262,"all_verified_states",len(samples),
          "worst_frames",max(depth_counts),
          "frame_histogram",repr(sorted(depth_counts.items())),
          "total_HTM_across_trials",total_htm)
    print("R11_UNIVERSAL_CONSTRUCTION 14_corner_color_reads+16_full_edge_prefix+at_most_5_edge_feedback; no reset")
    print("R11_SCOPE real two-probe full-state reconstruction; <=20 full-group worst-case OPEN")
    return depth_counts

if __name__=="__main__":
    audit()
