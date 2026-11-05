#!/usr/bin/env python3
"""R11: full LEGAL Rubik reconstruction in 21 joint color frames using only
14 DISTINCT corner facelet colors and 21 distinct edge facelet colors.

The existing R2 construction spent 21 unique corner observations; spatial
corner chirality proves two ordered facelet colors fully identify a corner's
type AND twist, allowing seven complete corner pairs (14 readings) plus
corner-twist parity to recover all 8 corners. The resulting corner
permutation parity then completes R2's 21-edge-facelet reconstruction.

Frames 15-21 still physically read the fixed corner probe, but its seven
readings are REDUNDANT to the decoder and may simply revisit known slots.
All actions are legal actual 18-HTM face turns with no hidden frame reset.
No claim of <21 FULL-CUBE frames; adaptive 18..21 still open.
"""
from b6_independent_48sticker_goals import (
    EDGE_POS,CORNERS,PIECES,SLOTS,compose,inverse,word,factor_value,
)
from construct_color_p48_24_frame_scanner import (
    SOURCE_FACE_COLOR, EDGE_FACELET, CORNER_FACELET,
    joint_sticker_orbit,inverted_token,
)
from audit_color_probe_information_bounds import two_one_facelet_colors
from construct_color_p48_21_frame_legality_scan import (
    plan21,permutation_parity
)
from audit_r11_corner14_chirality import READ,decode14

def joint21_plan():
    original,unread_edge,partial_edge,unread_corner=plan21()
    edge_slots=[x[0] for x in original]
    corner_slots=list(READ)+list(READ[:7])
    assert len(edge_slots)==len(corner_slots)==21
    assert len(set(edge_slots))==21
    assert len(set(corner_slots))==14
    paths=joint_sticker_orbit()
    output=[]
    for e,c in zip(edge_slots,corner_slots):
        commands=tuple(inverted_token(t) for t in reversed(paths[(e,c)]))
        frame=word(" ".join(commands))
        assert (frame[e],frame[c])==(EDGE_FACELET,CORNER_FACELET)
        output.append((e,c,commands))
    return tuple(output),unread_edge,partial_edge

def decode_35_colors(edge_colors,corner_colors,unread_edge,partial_edge):
    assert len(edge_colors)==21
    assert set(corner_colors)==set(READ)
    corner_map=decode14(corner_colors)
    recovered=[None]*48
    for src,dst in zip((s for p in CORNERS for s in PIECES[p]),corner_map):
        recovered[src]=dst
    found_edges=set()
    for destination in EDGE_POS:
        stickers=PIECES[destination]
        if not all(slot in edge_colors for slot in stickers):
            continue
        signature=frozenset(edge_colors[slot] for slot in stickers)
        matches=[p for p in EDGE_POS if
                 frozenset(SOURCE_FACE_COLOR[s] for s in PIECES[p])==signature]
        assert len(matches)==1
        source=matches[0]
        assert source not in found_edges
        found_edges.add(source)
        source_by_color={SOURCE_FACE_COLOR[j]:j for j in PIECES[source]}
        for slot in stickers:
            recovered[source_by_color[edge_colors[slot]]]=slot
    assert len(found_edges)==10
    missing=sorted(set(EDGE_POS)-found_edges)
    assert len(missing)==2
    corner_index={p:i for i,p in enumerate(CORNERS)}
    corner_destinations=[]
    for source in CORNERS:
        spatial={SLOTS[recovered[j]][0] for j in PIECES[source]}
        assert len(spatial)==1
        corner_destinations.append(corner_index[next(iter(spatial))])
    corner_parity=permutation_parity(corner_destinations)
    edge_index={p:i for i,p in enumerate(EDGE_POS)}
    solutions=[]
    partial_read_slots=[s for s in PIECES[partial_edge] if s in edge_colors]
    assert len(partial_read_slots)==1
    partial_read=partial_read_slots[0]
    for first,second in ((missing[0],missing[1]),(missing[1],missing[0])):
        edge_dest=[]
        for source in EDGE_POS:
            if source==first: dest=partial_edge
            elif source==second:dest=unread_edge
            else:
                spatial={SLOTS[recovered[j]][0] for j in PIECES[source]}
                assert len(spatial)==1
                dest=next(iter(spatial))
            edge_dest.append(edge_index[dest])
        if permutation_parity(edge_dest)!=corner_parity:continue
        for flip in range(2):
            trial=recovered.copy()
            for i,source_slot in enumerate(PIECES[first]):
                trial[source_slot]=PIECES[partial_edge][(i+flip)%2]
            read_source=next(s for s in PIECES[first] if
                             trial[s]==partial_read)
            if SOURCE_FACE_COLOR[read_source]!=edge_colors[partial_read]:
                continue
            for last_flip in range(2):
                candidate=trial.copy()
                for i,s in enumerate(PIECES[second]):
                    candidate[s]=PIECES[unread_edge][(i+last_flip)%2]
                assert None not in candidate and len(set(candidate))==48
                if sum(factor_value(p,candidate)%2 for p in EDGE_POS)%2!=0:
                    continue
                assert all(SOURCE_FACE_COLOR[candidate.index(slot)]==color
                           for slot,color in edge_colors.items())
                assert all(SOURCE_FACE_COLOR[candidate.index(slot)]==color
                           for slot,color in corner_colors.items())
                solutions.append(tuple(candidate))
    assert len(solutions)==1
    return solutions[0]

def replay(cube,configuration):
    plan,last_edge,partial_edge=configuration
    frame=bytes(range(48))
    previous=()
    measured_edge={}
    measured_corner={}
    turns=0
    for e,c,commands in plan:
        delta_commands=tuple(inverted_token(t) for t in reversed(previous))+commands
        relative=word(" ".join(delta_commands))
        frame=compose(relative,frame)
        assert frame==word(" ".join(commands))
        assert inverse(frame)[EDGE_FACELET]==e
        assert inverse(frame)[CORNER_FACELET]==c
        edge_color,corner_color=two_one_facelet_colors(cube,frame)
        assert edge_color==SOURCE_FACE_COLOR[cube.index(e)]
        assert corner_color==SOURCE_FACE_COLOR[cube.index(c)]
        measured_edge[e]=edge_color
        if c in READ:measured_corner[c]=corner_color
        turns+=len(delta_commands)
        previous=commands
    decoded=decode_35_colors(measured_edge,measured_corner,last_edge,partial_edge)
    assert decoded==tuple(cube)
    return turns

def audit():
    from audit_active_p48_small_ball_decision_trees import ball
    from audit_r11_corner20_no_oracle import corner_source_pair_samples
    states,_=ball(2)
    samples=list(states)+corner_source_pair_samples()
    for seq in (
        "L F R' F' L' U2 R U R U' R2 U2 R",
        "U2 R' B D2 B' R U2 R' B D2 B' R",
        "R U F' L2 B D R' B2",
        "F R B L D2 U R F' L2 U2 B",
    ):
        samples.append(word(seq))
    assert len(samples)==434
    config=joint21_plan()
    turns={replay(cube,config) for cube in samples}
    assert len(turns)==1
    print("R11_FULL_CUBE_21_FRAMES_35_UNIQUE_COLOR_READS_PASS",
          "physical_states",len(samples),"edge_distinct",21,
          "corner_distinct",14,"joint_frames",21)
    print("R11_FULL21_P48_NO_RESET_PASS",
          "joint_orbit",576,"per_trial_htm",next(iter(turns)))
    print("R11_SCOPE complete legal full-group constructive 21-frame upper;",
          "nonadaptive optimum still 21, adaptive 18..21 OPEN")
    return len(samples)

if __name__=="__main__":
    audit()
