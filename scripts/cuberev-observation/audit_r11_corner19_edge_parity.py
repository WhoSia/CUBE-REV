#!/usr/bin/env python3
"""R11: decode all corners with 19 fixed corner-color reads GIVEN edge parity.

Full legal P48 cube with exact six colors and known actions. This is a
one-bit EDGE-PERMUTATION-PARITY oracle, not the complete-corner oracle
used by R7–R10. It shows precisely what a future joint 20-frame
policy must supply, and what it cannot get for free.

Read all 3 facelets of six fixed spatial corner positions (18), plus one
facelet of a seventh (19). Eight corners are identified using:
  - six complete color triples,
  - edge/corner permutation parity equality (1 bit),
  - partial seventh color fixes that corner's twist,
  - total corner twist sum zero determines last twist.
No original cubie labels are read by the sensor.
"""
from b6_independent_48sticker_goals import (
    EDGE_POS, CORNERS, PIECES, SLOTS, word, factor_value, inverse, compose,
)
from construct_color_p48_24_frame_scanner import (
    EDGE_STICKERS, SOURCE_FACE_COLOR, CORNER_FACELET, EDGE_FACELET,
    joint_sticker_orbit, inverted_token,
)
from audit_color_probe_information_bounds import two_one_facelet_colors
from construct_color_p48_21_frame_legality_scan import permutation_parity

COMPLETE=CORNERS[:6]
PARTIAL=CORNERS[6]
UNREAD=CORNERS[7]
SLOTS_TO_READ=tuple(s for p in COMPLETE for s in PIECES[p])+(PIECES[PARTIAL][0],)
assert len(SLOTS_TO_READ)==19 and len(set(SLOTS_TO_READ))==19

def cubie_parity(state,positions):
    index={p:i for i,p in enumerate(positions)}
    dest=[]
    for source in positions:
        where={SLOTS[state[s]][0] for s in PIECES[source]}
        assert len(where)==1
        dest.append(index[next(iter(where))])
    return permutation_parity(dest)

def corner_twist(state):
    return sum(factor_value(p,state)%3 for p in CORNERS)%3

def decode_corner_colors(colors,known_edge_parity):
    assert set(colors)==set(SLOTS_TO_READ)
    assert known_edge_parity in (0,1)
    recovered=[None]*48
    present=set()
    for dest in COMPLETE:
        slots=PIECES[dest]
        signature=frozenset(colors[s] for s in slots)
        labels=[p for p in CORNERS if
                frozenset(SOURCE_FACE_COLOR[s] for s in PIECES[p])==signature]
        assert len(labels)==1
        src=labels[0]
        assert src not in present
        present.add(src)
        origin={SOURCE_FACE_COLOR[s]:s for s in PIECES[src]}
        for slot in slots:
            recovered[origin[colors[slot]]]=slot
    assert len(present)==6
    missing=sorted(set(CORNERS)-present)
    assert len(missing)==2
    poss=[]
    for first,second in ((missing[0],missing[1]),(missing[1],missing[0])):
        source_to_dest={p:p for p in ()}
        for src in present:
            spatial={SLOTS[recovered[j]][0] for j in PIECES[src]}
            assert len(spatial)==1
            source_to_dest[src]=next(iter(spatial))
        source_to_dest[first]=PARTIAL
        source_to_dest[second]=UNREAD
        indices={p:i for i,p in enumerate(CORNERS)}
        parity=permutation_parity([indices[source_to_dest[p]] for p in CORNERS])
        if parity!=known_edge_parity:
            continue
        for twist_first in range(3):
            trial=recovered.copy()
            for i,src_slot in enumerate(PIECES[first]):
                trial[src_slot]=PIECES[PARTIAL][(i+twist_first)%3]
            first_read=PIECES[PARTIAL][0]
            observed_source=next(i for i in PIECES[first] if trial[i]==first_read)
            if SOURCE_FACE_COLOR[observed_source]!=colors[first_read]:
                continue
            for twist_last in range(3):
                candidate=trial.copy()
                for i,src_slot in enumerate(PIECES[second]):
                    candidate[src_slot]=PIECES[UNREAD][(i+twist_last)%3]
                # Other edge facelets irrelevant to checking corner twist;
                # filler original identity edges are legitimate for factors.
                for edge in EDGE_POS:
                    for edge_slot in PIECES[edge]:
                        candidate[edge_slot]=edge_slot
                assert None not in candidate
                if corner_twist(candidate)!=0:
                    continue
                if any(SOURCE_FACE_COLOR[candidate.index(slot)]!=color
                       for slot,color in colors.items()):
                    raise AssertionError("19-color decoder contradicted observed color")
                poss.append(tuple(candidate[i] for p in CORNERS for i in PIECES[p]))
    assert len(poss)==1,(len(poss),known_edge_parity,colors)
    return poss[0]

def legal_19_frame_plan():
    paths=joint_sticker_orbit()
    edge_selected=EDGE_STICKERS[:19]
    output=[]
    for e,c in zip(edge_selected,SLOTS_TO_READ):
        commands=tuple(inverted_token(t) for t in reversed(paths[(e,c)]))
        frame=word(" ".join(commands))
        assert (frame[e],frame[c])==(EDGE_FACELET,CORNER_FACELET)
        output.append((e,c,commands))
    return output

def audit():
    plan=legal_19_frame_plan()
    from audit_active_p48_small_ball_decision_trees import ball
    states,_=ball(2)
    samples=list(states)
    for seq in (
        "R U F R' U' F'", "U R2 F' B D2 L U2 R'",
        "L F R' F' L' U2 R U R U' R2 U2 R",
        "U2 R' B D2 B' R U2 R' B D2 B' R",
    ):
        samples.append(word(seq))
    total_turns=0
    max_turns=0
    for cube in samples:
        measured={}
        current=bytes(range(48))
        prev=()
        turns=0
        for e,c,commands in plan:
            relative=tuple(inverted_token(t) for t in reversed(prev))+commands
            nxt=word(" ".join(relative))
            current=compose(nxt,current)
            assert current==word(" ".join(commands))
            edge_color,corner_color=two_one_facelet_colors(cube,current)
            assert corner_color==SOURCE_FACE_COLOR[cube.index(c)]
            measured[c]=corner_color
            turns+=len(relative)
            prev=commands
        actual_edge_parity=cubie_parity(cube,EDGE_POS)
        observed=decode_corner_colors(measured,actual_edge_parity)
        truth=tuple(cube[i] for p in CORNERS for i in PIECES[p])
        assert observed==truth
        total_turns+=turns
        max_turns=max(max_turns,turns)
    assert len(samples)==266
    print("R11_P48_CORNER_19_WITH_EDGE_PARITY_PASS",
          "samples",len(samples),"corner_colors",len(SLOTS_TO_READ),
          "edge_parity_oracle_bits",1)
    print("R11_NO_RESET_COLOR_SENSOR_EXECUTION_PASS",
          "trials",len(samples),"aggregate_htm",total_turns,
          "max_trial_htm",max_turns,"joint_orbit",576)
    print("R11_BOUNDARY 19 corners only GIVEN true edge permutation parity;",
          "not a full 19 or 20 frame cube recovery and not measured cognition")
    return len(samples)

if __name__=="__main__":
    audit()
