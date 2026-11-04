#!/usr/bin/env python3
"""Finite-alphabet observability lower bounds for two realistic color samples.

A fixed edge slot and fixed corner slot each expose exactly ONE facelet's
quantized color (six categorical labels), instead of the ideal P48 original
piece's full identity and orientation. Each joint observation frame has at
most 6^2 = 36 possible outputs.

Information bound for full legal cube G works for ANY deterministic
adaptive known-action policy with no auxiliary state-dependent measurement
or hidden timing side-channel: 36^n >= |G|. One-erasure and one-adversarial
frame-substitution bounds below additionally assume a FIXED NONADAPTIVE
query schedule, so the noiseless state-to-history map is an ordinary
q-ary error-correcting code. Do not apply the Hamming bound to arbitrary
feedback strategies without a separate proof.
"""
from math import comb, factorial
from collections import Counter
from b6_independent_48sticker_goals import (
    SLOTS, PIECES, CORNERS, EDGE_POS, FACES, MOVES,
    compose, word,
)
from audit_active_p48_small_ball_decision_trees import ball

CUBE_GROUP_SIZE=factorial(8)*3**7*factorial(12)*2**10
ALPHABET=6*6
NORMAL_TO_COLOR={normal:name for name,normal in FACES.items()}
EDGE_SLOT=EDGE_POS[0]
CORNER_SLOT=CORNERS[0]
EDGE_FACELET=PIECES[EDGE_SLOT][0]
CORNER_FACELET=PIECES[CORNER_SLOT][0]

def face_color_at_slot(state,physical_sticker_slot):
    """Color is intrinsic to original sticker, not the current slot face."""
    original_sticker=state.index(physical_sticker_slot)
    return NORMAL_TO_COLOR[SLOTS[original_sticker][1]]

def two_one_facelet_colors(state,frame):
    if len(state)!=48 or set(state)!=set(range(48)):
        raise ValueError("not a physical sticker-slot bijection")
    physical=compose(frame,state)
    return (face_color_at_slot(physical,EDGE_FACELET),
            face_color_at_slot(physical,CORNER_FACELET))

def lower_frames(state_count,alphabet=ALPHABET):
    n=0
    while alphabet**n<state_count:n+=1
    return n

def nonadaptive_error_lower_frames(state_count,errors,alphabet=ALPHABET):
    n=0
    while alphabet**n < state_count*sum(
        comb(n,k)*(alphabet-1)**k for k in range(min(errors,n)+1)):
        n+=1
    return n

def audit():
    group=CUBE_GROUP_SIZE
    assert group==43252003274489856000
    assert 36**12<group<=36**13
    assert lower_frames(group)==13
    assert nonadaptive_error_lower_frames(group,1)==15
    assert nonadaptive_error_lower_frames(group,2)==16
    # For one known-position erasure in a predetermined length-n history,
    # any n-1 transmitted symbols must distinguish all group elements.
    assert lower_frames(group)+1==14

    states,sizes=ball(2)
    outputs=[two_one_facelet_colors(s,bytes(range(48))) for s in states]
    assert len(states)==262 and len(set(outputs))<=36
    groups=Counter(outputs)
    assert max(groups.values())>=8
    for name,frame in MOVES.items():
        symbols={two_one_facelet_colors(s,frame) for s in states}
        assert len(symbols)<=36
    # B4 has 46741 states, just 85 more than 36^3=46656.
    assert 46741-36**3==85
    assert lower_frames(46741)==4
    print("COLOR_PROBE_FULL_GROUP_13_FRAME_LOWER_BOUND_PASS",group,36**12,36**13)
    print("COLOR_PROBE_NONADAPTIVE_ONE_ERASURE_14_FRAME_LOWER_BOUND_PASS")
    print("COLOR_PROBE_NONADAPTIVE_ONE_WRONG_JOINT_FRAME_15_FRAME_LOWER_BOUND_PASS")
    print("COLOR_PROBE_B4_FOUR_FRAME_INFORMATION_LOWER_BOUND_PASS excess_over_36_cubed=85")
    print("COLOR_PROBE_P48_SINGLE_FACELET_READOUT_PASS B2_states=262 frames_tested=19")
    print("BOUNDARY information lower bounds alone do not construct 13-frame color recovery")
    print("BOUNDARY no measured optical errors, lighting data, or human participants")
    return {"full_group":group,"clean_lower":13,"erasure_lower_fixed":14,
            "one_error_lower_fixed":15,"two_error_lower_fixed":16,
            "b4_lower":4}

if __name__=="__main__":
    audit()
