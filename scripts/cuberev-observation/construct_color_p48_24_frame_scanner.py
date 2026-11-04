#!/usr/bin/env python3
"""24-frame constructive full-Rubik recovery using TWO single-facelet color probes.

Unlike an ideal original cubie ID+orientation sensor, each stationary probe
returns only ONE of six categorical face colors at one fixed moving-sticker
slot. This script constructs real 18-HTM frame words that let a stationary
edge-facelet probe and corner-facelet probe interrogate every one of the 48
moving facelet slots in 24 predetermined frames.

A joint BFS on the 24 edge-facelet x 24 corner-facelet *spatial* orbit
provides 576 addressable pairs. Each chosen frame maps two specified initial
facelet slots to the two physical readout slots; known inverse action maps
the resulting colors back to initial spatial facelet positions. Full edge
and corner color triples/pairs, each with a unique home cubie, reconstruct
the 48-sticker permutation for any legal cube state.

Upper bound 24 is constructive, NOT claimed optimal. No actual RGB hardware,
calibration, color noise, or human results are supplied.
"""
from collections import deque
from b6_independent_48sticker_goals import (
    CORNERS, EDGE_POS, FACES, PIECES, SLOTS, MOVES, compose, inverse, word,
)
from audit_color_probe_information_bounds import (
    EDGE_FACELET, CORNER_FACELET, face_color_at_slot, two_one_facelet_colors,
)

EDGE_STICKERS=tuple(sorted(i for p in EDGE_POS for i in PIECES[p]))
CORNER_STICKERS=tuple(sorted(i for p in CORNERS for i in PIECES[p]))
assert len(EDGE_STICKERS)==len(CORNER_STICKERS)==24
SOURCE_FACE_COLOR={i:next(f for f,n in FACES.items() if n==SLOTS[i][1])
                   for i in range(48)}

def inverted_token(token):
    return token if token.endswith("2") else (
        token[:-1] if token.endswith("'") else token+"'")

def joint_sticker_orbit():
    home=(EDGE_FACELET,CORNER_FACELET)
    queue=deque([home]);found={home:()}
    while queue:
        a,b=queue.popleft()
        for token,turn in MOVES.items():
            after=(turn[a],turn[b])
            if after not in found:
                found[after]=found[(a,b)]+(token,)
                queue.append(after)
    expected={(a,b) for a in EDGE_STICKERS for b in CORNER_STICKERS}
    assert set(found)==expected and len(found)==576
    return found

def scan_plan():
    paths=joint_sticker_orbit()
    plan=[]
    for e,c in zip(EDGE_STICKERS,CORNER_STICKERS):
        reverse=tuple(inverted_token(token) for token in reversed(paths[(e,c)]))
        frame=word(" ".join(reverse))
        assert (frame[e],frame[c])==(EDGE_FACELET,CORNER_FACELET)
        plan.append((e,c,reverse))
    assert len(plan)==24
    assert {e for e,c,actions in plan}==set(EDGE_STICKERS)
    assert {c for e,c,actions in plan}==set(CORNER_STICKERS)
    return plan

def reconstruct_from_colors(state,plan=None):
    if plan is None:plan=scan_plan()
    if len(state)!=48 or set(state)!=set(range(48)):
        raise ValueError("not an oriented 48-sticker bijection")
    initial_spatial_colors={}
    present_frame=bytes(range(48))
    previous_commands=()
    for original_edge_slot,original_corner_slot,commands in plan:
        frame=word(" ".join(commands))
        relative=compose(frame,inverse(present_frame))
        present_frame=compose(relative,present_frame)
        assert present_frame==frame
        # Actual relative word = inverse(previous absolute word) then next.
        # No imaginary reset between frames; verify on all 48 stickers.
        actual_relative=tuple(inverted_token(t) for t in
                              reversed(previous_commands))+commands
        assert word(" ".join(actual_relative))==relative
        previous_commands=commands
        edge_color,corner_color=two_one_facelet_colors(state,frame)
        recovered_edge=inverse(frame)[EDGE_FACELET]
        recovered_corner=inverse(frame)[CORNER_FACELET]
        assert (recovered_edge,recovered_corner)==(
            original_edge_slot,original_corner_slot)
        for slot,color in ((recovered_edge,edge_color),
                           (recovered_corner,corner_color)):
            if slot in initial_spatial_colors and initial_spatial_colors[slot]!=color:
                raise AssertionError("conflicting single-sticker measurements")
            initial_spatial_colors[slot]=color
    assert len(initial_spatial_colors)==48

    # Each cube edge/corner has a unique unordered set of 2/3 face colors.
    signature_to_home={}
    for home,stickers in PIECES.items():
        signature=frozenset(SOURCE_FACE_COLOR[i] for i in stickers)
        assert signature not in signature_to_home
        signature_to_home[signature]=home
    recovered=[None]*48
    for spatial_position,spatial_stickers in PIECES.items():
        observed=frozenset(initial_spatial_colors[i] for i in spatial_stickers)
        home=signature_to_home.get(observed)
        if home is None:raise AssertionError("unrecognized original cubie colors")
        by_color={SOURCE_FACE_COLOR[i]:i for i in PIECES[home]}
        assert len(by_color)==len(spatial_stickers)
        for observed_slot in spatial_stickers:
            original_sticker=by_color[initial_spatial_colors[observed_slot]]
            if recovered[original_sticker] is not None:
                raise AssertionError("duplicated original sticker")
            recovered[original_sticker]=observed_slot
    if tuple(recovered)!=tuple(state):
        raise AssertionError("the color scan failed to reconstruct full physical P48")
    return tuple(recovered)

def plan_htm_cost(plan):
    """Executable (not globally shortest) no-reset HTM length."""
    previous=()
    total=0
    for _,_,next_commands in plan:
        relative=tuple(inverted_token(t) for t in reversed(previous))+next_commands
        total+=len(relative)
        assert word(" ".join(relative))==compose(
            word(" ".join(next_commands)),inverse(word(" ".join(previous))))
        previous=next_commands
    return total

def audit():
    orbit=joint_sticker_orbit()
    plan=scan_plan()
    from audit_active_p48_small_ball_decision_trees import ball
    states,_=ball(2)
    for state in states:
        assert reconstruct_from_colors(state,plan)==tuple(state)
    for token in MOVES:
        state=word(token)
        assert reconstruct_from_colors(state,plan)==tuple(state)
    for w in ("L F R' F' L' U2 R U R U' R2 U2 R",
              "R2 U2 F L D' B R U2 F2 B' D",
              "U2 R' B D2 B' R U2 R' B D2 B' R"):
        state=word(w)
        assert reconstruct_from_colors(state,plan)==tuple(state)
    print("COLOR_P48_JOINT_STICKER_ORBIT_PASS 576 edge-corner facelet pairs")
    print("COLOR_P48_24_FRAME_FULL_STICKER_SCANNER_PASS all 48 facelets read")
    print("COLOR_P48_B2_ALL_262_STATES_REPLAY_PASS")
    print("COLOR_P48_GEOMETRY_MAX_ABSOLUTE_FRAME_WORD",max(len(w) for e,c,w in plan))
    print("COLOR_P48_NO_RESET_ACTION_UPPER_HTM",plan_htm_cost(plan))
    print("COLOR_FULL_GROUP_BOUNDS 13 <= optimal_clean_frames <= 24")
    print("BOUNDARY ideal quantized color labels, no sensor noise or action-cost optimality")
    return {"joint_pairs":len(orbit),"frames":len(plan),
            "max_absolute_frame_word":max(len(w) for e,c,w in plan),
            "constructive_no_reset_htm":plan_htm_cost(plan)}

if __name__=="__main__":
    audit()
