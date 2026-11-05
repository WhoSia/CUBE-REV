#!/usr/bin/env python3
"""21-frame full legal Rubik recovery from two fixed single-facelet 6-color probes.

Read 10 full edge cubies + 1 facelet of an eleventh (21 edge colors).
Read 7 full corner cubies (21 corner colors). The still hidden labels and
orientations follow from three *legal-cube* invariants, all checked in P48:
  - corner twist sum = 0 mod 3 determines the last corner orientation,
  - edge and corner permutation parities coincide, selecting the allocation
    of the final two original edge cubie labels,
  - edge flip sum = 0 mod 2 determines the final unread edge's flip.
The one observed facelet on the partial edge distinguishes its orientation.
No full-cubie identity is read directly and no guessed state is compared
to ground truth inside the reconstruction routine. This is an upper bound.
"""
from b6_independent_48sticker_goals import (
    EDGE_POS,CORNERS,PIECES,SLOTS,compose,inverse,word,factor_value,
)
from construct_color_p48_24_frame_scanner import (
    EDGE_STICKERS,CORNER_STICKERS,SOURCE_FACE_COLOR,
    EDGE_FACELET,CORNER_FACELET,joint_sticker_orbit,inverted_token,
)
from audit_color_probe_information_bounds import two_one_facelet_colors

def plan21():
    unseen_edge=EDGE_POS[-1]
    partial_edge=EDGE_POS[-2]
    unseen_corner=CORNERS[-1]
    missing_edge_slots=set(PIECES[unseen_edge])|{PIECES[partial_edge][-1]}
    missing_corner_slots=set(PIECES[unseen_corner])
    selected_e=[p for p in EDGE_STICKERS if p not in missing_edge_slots]
    selected_c=[p for p in CORNER_STICKERS if p not in missing_corner_slots]
    assert len(selected_e)==len(selected_c)==21
    paths=joint_sticker_orbit()
    plan=[]
    for e,c in zip(selected_e,selected_c):
        commands=tuple(inverted_token(t) for t in reversed(paths[(e,c)]))
        frame=word(" ".join(commands))
        assert (frame[e],frame[c])==(EDGE_FACELET,CORNER_FACELET)
        plan.append((e,c,commands))
    return plan,unseen_edge,partial_edge,unseen_corner

def permutation_parity(order):
    return sum(order[i]>order[j] for i in range(len(order))
               for j in range(i+1,len(order)))%2

def recover21(physical_state,configuration=None):
    if len(physical_state)!=48 or set(physical_state)!=set(range(48)):
        raise ValueError("invalid physical original-to-slot P48 permutation")
    if configuration is None:configuration=plan21()
    plan,last_edge,partial_edge,last_corner=configuration
    measured={}
    actual_frame=bytes(range(48))
    previous=()
    for spatial_e,spatial_c,commands in plan:
        frame=word(" ".join(commands))
        relative_commands=tuple(inverted_token(t) for t in reversed(previous))+commands
        delta=word(" ".join(relative_commands))
        actual_frame=compose(delta,actual_frame)
        assert actual_frame==frame
        previous=commands
        actual_e=inverse(frame)[EDGE_FACELET]
        actual_c=inverse(frame)[CORNER_FACELET]
        assert (actual_e,actual_c)==(spatial_e,spatial_c)
        color_e,color_c=two_one_facelet_colors(physical_state,frame)
        measured[spatial_e]=color_e
        measured[spatial_c]=color_c
    assert len(measured)==42
    recovered=[None]*48
    found_edges=set();found_corners=set()
    for destination,stickers in PIECES.items():
        if destination in (last_edge,partial_edge,last_corner):continue
        wanted=frozenset(measured[p] for p in stickers)
        matches=[source for source,original in PIECES.items()
                 if len(original)==len(stickers) and
                 frozenset(SOURCE_FACE_COLOR[j] for j in original)==wanted]
        assert len(matches)==1
        source=matches[0]
        source_by_color={SOURCE_FACE_COLOR[j]:j for j in PIECES[source]}
        for slot in stickers:
            recovered[source_by_color[measured[slot]]]=slot
        (found_edges if len(stickers)==2 else found_corners).add(source)
    assert len(found_edges)==10 and len(found_corners)==7
    absent_corner=next(iter(set(CORNERS)-found_corners))
    abs_corner_stickers=PIECES[absent_corner];dst_corner=PIECES[last_corner]
    twisted=[]
    for t in range(3):
        trial=recovered.copy()
        for i,src in enumerate(abs_corner_stickers):
            trial[src]=dst_corner[(i+t)%3]
        twist_total=sum(factor_value(p,trial)%3 for p in CORNERS)%3
        if twist_total==0:twisted.append(trial)
    assert len(twisted)==1
    recovered=twisted[0]
    corner_index={p:i for i,p in enumerate(CORNERS)}
    corner_destinations=[]
    for source in CORNERS:
        spatial={SLOTS[recovered[j]][0] for j in PIECES[source]}
        assert len(spatial)==1
        corner_destinations.append(corner_index[next(iter(spatial))])
    corner_parity=permutation_parity(corner_destinations)
    remaining_edges=sorted(set(EDGE_POS)-found_edges)
    assert len(remaining_edges)==2
    edge_index={p:i for i,p in enumerate(EDGE_POS)}
    candidate_states=[]
    for first_label,second_label in (
        (remaining_edges[0],remaining_edges[1]),
        (remaining_edges[1],remaining_edges[0])):
        edge_destinations=[]
        for source in EDGE_POS:
            if source==first_label:destination=partial_edge
            elif source==second_label:destination=last_edge
            else:
                dests={SLOTS[recovered[j]][0] for j in PIECES[source]}
                assert len(dests)==1
                destination=next(iter(dests))
            edge_destinations.append(edge_index[destination])
        if permutation_parity(edge_destinations)!=corner_parity:continue
        options=[]
        read_slot=next(j for j in PIECES[partial_edge] if j in measured)
        assert len([j for j in PIECES[partial_edge] if j in measured])==1
        for flip in range(2):
            trial=recovered.copy()
            for i,src in enumerate(PIECES[first_label]):
                trial[src]=PIECES[partial_edge][(i+flip)%2]
            origin_at_read=next(src for src in PIECES[first_label]
                                if trial[src]==read_slot)
            if SOURCE_FACE_COLOR[origin_at_read]==measured[read_slot]:
                options.append(trial)
        assert len(options)==1
        recovered_with_partial=options[0]
        for flip in range(2):
            trial=recovered_with_partial.copy()
            for i,src in enumerate(PIECES[second_label]):
                trial[src]=PIECES[last_edge][(i+flip)%2]
            assert None not in trial and set(trial)==set(range(48))
            if sum(factor_value(p,trial)%2 for p in EDGE_POS)%2==0:
                if any(SOURCE_FACE_COLOR[trial.index(dst)]!=color
                       for dst,color in measured.items()):
                    raise AssertionError("inferred state contradicts sampled color")
                candidate_states.append(tuple(trial))
    assert len(candidate_states)==1
    return candidate_states[0]

def audit():
    plan=plan21()
    from audit_active_p48_small_ball_decision_trees import ball
    states,_=ball(2)
    for g in states:assert recover21(g,plan)==tuple(g)
    for seq in ("L F R' F' L' U2 R U R U' R2 U2 R",
                "R F2 B' L2 U R D' F",
                "U2 R' B D2 B' R U2 R' B D2 B' R"):
        state=word(seq)
        assert recover21(state,plan)==tuple(state)
    print("COLOR_P48_21_FRAME_FULL_GROUP_CONSTRUCTION_PASS 21 edge + 21 corner facelet colors")
    print("COLOR_P48_21_FRAME_CUBIE_PARITIES_PASS corner_twist,edge_swap,edge_flip")
    print("COLOR_P48_21_FRAME_B2_ALL_262_STATES_PASS")
    print("COLOR_FULL_GROUP_IMPROVED_BOUNDS 13 <= h_color <= 21")
    print("BOUNDARY assumes legal fixed-centre cube, exact six-color classifications, known turns")
    return {"frames":21,"B2_replays":len(states)}

if __name__=="__main__":
    audit()
