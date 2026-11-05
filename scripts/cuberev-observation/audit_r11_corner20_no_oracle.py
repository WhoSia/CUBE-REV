#!/usr/bin/env python3
"""R11: 20 color-only CORNER probes reconstruct all corners, no edge oracle.

19 corner reads (six complete + one partial) suffice if edge permutation
parity is revealed; 20 corner reads (six complete + TWO partial) may remove
the oracle. This verifier exhausts the remaining-two-corner source cases
and checks all legal P48 B2 states and independent long-turn trajectories.

This is not a full 20-frame cube reconstruction: each concurrent edge
channel is still unverified as a universal adaptive edge identifier.
"""
from itertools import combinations
from b6_independent_48sticker_goals import (
    EDGE_POS, CORNERS, PIECES, SLOTS, word, factor_value, compose, inverse
)
from construct_color_p48_24_frame_scanner import (
    EDGE_STICKERS, CORNER_STICKERS, SOURCE_FACE_COLOR,
    EDGE_FACELET,CORNER_FACELET,joint_sticker_orbit,inverted_token
)
from audit_color_probe_information_bounds import two_one_facelet_colors
from construct_color_p48_21_frame_legality_scan import permutation_parity
from audit_r11_corner19_edge_parity import (
    COMPLETE,PARTIAL,UNREAD,SLOTS_TO_READ,corner_twist,
    cubie_parity,decode_corner_colors,legal_19_frame_plan
)

PARTIAL_TWO=PIECES[PARTIAL][:2]
CORNER20=tuple(s for p in COMPLETE for s in PIECES[p])+PARTIAL_TWO
assert len(CORNER20)==20 and len(set(CORNER20))==20

def corner20_decode(colors):
    assert set(colors)==set(CORNER20)
    known={}
    used=set()
    for spatial_corner in COMPLETE:
        observed={slot:colors[slot] for slot in PIECES[spatial_corner]}
        sig=frozenset(observed.values())
        srcs=[p for p in CORNERS if frozenset(SOURCE_FACE_COLOR[i]
             for i in PIECES[p])==sig]
        assert len(srcs)==1
        src=srcs[0]
        assert src not in used
        used.add(src)
        home_by_color={SOURCE_FACE_COLOR[i]:i for i in PIECES[src]}
        for slot,color in observed.items():
            known[home_by_color[color]]=slot
    missing=sorted(set(CORNERS)-used)
    assert len(missing)==2
    completions=[]
    for first,second in ((missing[0],missing[1]),(missing[1],missing[0])):
        for rot in range(3):
            candidate=known.copy()
            for i,source_slot in enumerate(PIECES[first]):
                candidate[source_slot]=PIECES[PARTIAL][(i+rot)%3]
            if any(SOURCE_FACE_COLOR[next(s for s in PIECES[first]
                         if candidate[s]==spatial_slot)]!=colors[spatial_slot]
                   for spatial_slot in PARTIAL_TWO):
                continue
            for other_rot in range(3):
                trial=candidate.copy()
                for i,s in enumerate(PIECES[second]):
                    trial[s]=PIECES[UNREAD][(i+other_rot)%3]
                state=list(range(48))
                for src_slot,dest_slot in trial.items():
                    state[src_slot]=dest_slot
                if corner_twist(state)!=0:continue
                completions.append(tuple(trial[s] for p in CORNERS
                                         for s in PIECES[p]))
    assert len(completions)==1,(
        "20 corner readings ambiguous",len(completions),colors,missing)
    return completions[0]

def make_joint_plan_20():
    paths=joint_sticker_orbit()
    plan=[]
    for e,c in zip(EDGE_STICKERS[:20],CORNER20):
        commands=tuple(inverted_token(t) for t in reversed(paths[(e,c)]))
        assert (word(" ".join(commands))[e],
                word(" ".join(commands))[c])==(EDGE_FACELET,CORNER_FACELET)
        plan.append((e,c,commands))
    return tuple(plan)

def test_state(cube,plan):
    frame=bytes(range(48))
    previous=()
    readings={}
    turns=0
    for e,c,commands in plan:
        delta_commands=tuple(inverted_token(t) for t in reversed(previous))+commands
        delta=word(" ".join(delta_commands))
        frame=compose(delta,frame)
        assert frame==word(" ".join(commands))
        color_e,color_c=two_one_facelet_colors(cube,frame)
        assert color_e==SOURCE_FACE_COLOR[cube.index(e)]
        assert color_c==SOURCE_FACE_COLOR[cube.index(c)]
        readings[c]=color_c
        turns+=len(delta_commands)
        previous=commands
    result=corner20_decode(readings)
    expected=tuple(cube[s] for p in CORNERS for s in PIECES[p])
    assert result==expected
    return turns

def corner_source_pair_samples():
    """168 physically legal states, all choices for last-two labels and twists."""
    samples=[]
    for first,second in combinations(CORNERS,2):
        remainder=sorted(set(CORNERS)-{first,second})
        for chosen in ((first,second),(second,first)):
            for tw in range(3):
                c=list(range(48))
                mapping=dict(zip(remainder,COMPLETE))
                mapping[chosen[0]]=PARTIAL
                mapping[chosen[1]]=UNREAD
                for src,dst in mapping.items():
                    phase=tw if src==chosen[0] else 0
                    for i,s in enumerate(PIECES[src]):
                        c[s]=PIECES[dst][(i+phase)%3]
                # Determine the final corner twist from the exact original
                # P48 factor-value convention, rather than using naive tw signs.
                success=[]
                for final_rot in range(3):
                    trial=c.copy()
                    for i,s in enumerate(PIECES[chosen[1]]):
                        trial[s]=PIECES[UNREAD][(i+final_rot)%3]
                    if sum(factor_value(p,trial)%3 for p in CORNERS)%3==0:
                        success.append(trial)
                assert len(success)==1
                cube=success[0]
                # Fix edge permutation parity to match actual corners.
                from audit_r11_corner19_edge_parity import cubie_parity
                if cubie_parity(cube,CORNERS)==1:
                    e0,e1=EDGE_POS[:2]
                    for i in range(2):
                        cube[PIECES[e0][i]]=PIECES[e1][i]
                        cube[PIECES[e1][i]]=PIECES[e0][i]
                assert cubie_parity(cube,EDGE_POS)==cubie_parity(cube,CORNERS)
                assert sum(factor_value(p,cube)%2 for p in EDGE_POS)%2==0
                samples.append(bytes(cube))
    assert len(samples)==168
    return samples

def audit():
    from audit_active_p48_small_ball_decision_trees import ball
    base,_=ball(2)
    samples=list(base)+corner_source_pair_samples()
    for seq in (
        "U R F U' R' F'", "L F R' F' L' U2 R U R U' R2 U2 R",
        "U2 R' B D2 B' R U2 R' B D2 B' R",
        "F R B L D2 U R F' L2 U2 B",
    ):
        samples.append(word(seq))
    plan=make_joint_plan_20()
    turns=[test_state(cube,plan) for cube in samples]
    assert len(samples)==262+168+4
    assert len(set(turns))==1, "fixed schedule should have fixed turn cost"
    print("R11_CORNER_20_NO_PARITY_ORACLE_PASS",
          "tested_physical_states",len(samples),
          "corner_color_reads",len(CORNER20),
          "edge_oracle_bits",0)
    print("R11_CORNER20_P48_NO_RESET_PASS",
          "joint_facelet_frames",len(plan),
          "physical_joint_orbit",576,
          "per_trial_htm",max(turns))
    print("R11_BOUNDARY corner state fully identified in 20 color reads;",
          "no complete-edge or full-cube 20-frame decoder is claimed")

if __name__=="__main__":
    audit()
