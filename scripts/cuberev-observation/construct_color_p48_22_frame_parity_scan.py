#!/usr/bin/env python3
"""22 predetermined frames suffice for full P48 cube recovery from two 6-color probes.

Construction reads 11 of the 12 edge cubies IN FULL (22 edge facelets)
and all 7 corners plus one facelet of the remaining corner (22 corner
facelets). Full colors identify the known 11 edges and 7 corners uniquely.

Remaining original cubie LABELS are determined by the permutation of
physical cubie identities. A single known color fixes the residual
corner's unique cyclic orientation; the remaining edge has two possible
flips, of which exactly one satisfies the legal global edge-flip parity.
No direct original-cubie ID/orientation sensor is used, and no hidden
ground-truth state is inspected during reconstruction (only for testing).

This is a constructive upper bound, not the minimum color-frame horizon.
"""
from b6_independent_48sticker_goals import (
    EDGE_POS,CORNERS,PIECES,MOVES,compose,inverse,word,factor_value,
)
from construct_color_p48_24_frame_scanner import (
    EDGE_STICKERS,CORNER_STICKERS, SOURCE_FACE_COLOR,
    EDGE_FACELET,CORNER_FACELET,joint_sticker_orbit,inverted_token,
)
from audit_color_probe_information_bounds import two_one_facelet_colors

def plan22():
    excluded_edge=EDGE_POS[-1]
    excluded_corner=CORNERS[-1]
    chosen_edges=[i for i in EDGE_STICKERS if i not in PIECES[excluded_edge]]
    chosen_corners=[i for i in CORNER_STICKERS if i!=PIECES[excluded_corner][1]
                    and i!=PIECES[excluded_corner][2]]
    assert len(chosen_edges)==len(chosen_corners)==22
    paths=joint_sticker_orbit()
    result=[]
    for e,c in zip(chosen_edges,chosen_corners):
        actions=tuple(inverted_token(t) for t in reversed(paths[(e,c)]))
        frame=word(" ".join(actions))
        assert (frame[e],frame[c])==(EDGE_FACELET,CORNER_FACELET)
        result.append((e,c,actions))
    return result,excluded_edge,excluded_corner

def reconstruction22(initial_state,configuration=None):
    if len(initial_state)!=48 or set(initial_state)!=set(range(48)):
        raise ValueError("invalid P48 original-to-slot permutation")
    if configuration is None:configuration=plan22()
    plan,last_edge,last_corner=configuration
    measured={}
    present=bytes(range(48))
    previous=()
    for e,c,actions in plan:
        frame=word(" ".join(actions))
        relative=compose(frame,inverse(present))
        relative_words=tuple(inverted_token(t) for t in reversed(previous))+actions
        assert word(" ".join(relative_words))==relative
        present=compose(relative,present)
        previous=actions
        assert present==frame
        colors=two_one_facelet_colors(initial_state,frame)
        original_edge=inverse(frame)[EDGE_FACELET]
        original_corner=inverse(frame)[CORNER_FACELET]
        assert (original_edge,original_corner)==(e,c)
        for slot,color in ((e,colors[0]),(c,colors[1])):
            if slot in measured and measured[slot]!=color:
                raise AssertionError("contradictory color observation")
            measured[slot]=color
    assert len(measured)==44
    recovered=[None]*48
    assigned_edges=set();assigned_corners=set()
    for spatial_position,slots in PIECES.items():
        if spatial_position in (last_edge,last_corner):continue
        colors=frozenset(measured[s] for s in slots)
        matches=[p for p,original_slots in PIECES.items()
                 if len(original_slots)==len(slots) and
                 frozenset(SOURCE_FACE_COLOR[j] for j in original_slots)==colors]
        assert len(matches)==1
        label=matches[0]
        (assigned_edges if len(slots)==2 else assigned_corners).add(label)
        color_to_original={SOURCE_FACE_COLOR[j]:j for j in PIECES[label]}
        for dst in slots:
            original=color_to_original[measured[dst]]
            assert recovered[original] is None
            recovered[original]=dst
    assert len(assigned_edges)==11 and len(assigned_corners)==7
    missing_edge_label=next(iter(set(EDGE_POS)-assigned_edges))
    missing_corner_label=next(iter(set(CORNERS)-assigned_corners))
    source_corner=PIECES[missing_corner_label]
    target_corner=PIECES[last_corner]
    observed_corner_sticker=next(j for j in target_corner if j in measured)
    assert len([j for j in target_corner if j in measured])==1
    corner_options=[]
    for twist in range(3):
        entries={source_corner[i]:target_corner[(i+twist)%3] for i in range(3)}
        original_sticker=next(src for src,dst in entries.items()
                              if dst==observed_corner_sticker)
        if SOURCE_FACE_COLOR[original_sticker]==measured[observed_corner_sticker]:
            corner_options.append(entries)
    assert len(corner_options)==1
    for original,slot in corner_options[0].items():
        assert recovered[original] is None
        recovered[original]=slot
    edge_home=PIECES[missing_edge_label]
    edge_destination=PIECES[last_edge]
    feasible=[]
    for flip in range(2):
        candidate=recovered.copy()
        for i,src in enumerate(edge_home):
            candidate[src]=edge_destination[(i+flip)%2]
        state=tuple(candidate)
        assert None not in state and set(state)==set(range(48))
        # The globally even edge-orientation sum is invariant under legal
        # Rubik turns. This is the *only* reason a completely unread edge's
        # orientation can be deduced from 22 color samples.
        if sum(factor_value(original,state)%2 for original in EDGE_POS)%2==0:
            feasible.append(state)
    assert len(feasible)==1
    return feasible[0]

def audit():
    conf=plan22()
    assert len(conf[0])==22
    from audit_active_p48_small_ball_decision_trees import ball
    states,_=ball(2)
    for state in states:assert reconstruction22(state,conf)==tuple(state)
    for seq in ("L F R' F' L' U2 R U R U' R2 U2 R",
                "F R2 U' D L B2 R2 F D'","U2 R' B D2 B' R U2 R' B D2 B' R"):
        actual=word(seq)
        assert reconstruction22(actual,conf)==tuple(actual)
    print("COLOR_P48_22_FRAME_LEGAL_PARITY_RECONSTRUCTION_PASS full_group_constructive")
    print("COLOR_P48_22_FRAME_EDGE_11_FULL_CORNER_7_PLUS_1_PASS")
    print("COLOR_P48_22_FRAME_B2_ALL_262_STATES_PASS")
    print("COLOR_FULL_GROUP_IMPROVED_BOUNDS 13 <= h_color <= 22")
    print("BOUNDARY edge-flip parity assumes legal Rubik states, not arbitrary sticker permutations")
    return {"frames":22,"states_tested":len(states)}

if __name__=="__main__":
    audit()
