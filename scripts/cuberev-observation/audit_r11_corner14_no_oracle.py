#!/usr/bin/env python3
"""R11: exact fourteen-color complete-corner decoder, no corner/edge oracle.

Under the full physical 3x3 P48 color model, for EACH fixed corner spatial
position, observing ANY TWO of its three facelet colors uniquely identifies
which original corner label and cyclic orientation occupies it. Seven such
corner positions consume 14 single-facelet colors; the eighth corner label
is then the unassigned one, and its twist follows from the legal corner-twist
sum mod 3. This decoder uses no real edge/permutation/corner ground truth.

We also transport these observations to the two fixed edge/corner sensing
positions by actual legal HTM turns, without resets, and audit all B2 states.
Not a <=20-frame full cube identification policy: edge state remains unknown.
"""
from b6_independent_48sticker_goals import (
    CORNERS, EDGE_POS, PIECES, SLOTS, FACES, inverse, compose, word,
    factor_value,
)
from construct_color_p48_24_frame_scanner import (
    EDGE_STICKERS, SOURCE_FACE_COLOR, EDGE_FACELET, CORNER_FACELET,
    joint_sticker_orbit, inverted_token,
)
from audit_color_probe_information_bounds import two_one_facelet_colors
from audit_active_p48_small_ball_decision_trees import ball

IDENTITY=bytes(range(48))
SEVEN=CORNERS[:-1]
LAST=CORNERS[-1]
CORNER14=tuple(slot for pos in SEVEN for slot in PIECES[pos][:2])
assert len(CORNER14)==len(set(CORNER14))==14

def oriented_corner_signature(source, dest, twist, read_stickers):
    spatial=PIECES[dest]
    original=PIECES[source]
    return tuple(SOURCE_FACE_COLOR[original[
        (spatial.index(slot)-twist)%3]] for slot in read_stickers)

def decode14(measured):
    """Return original->spatial sticker mapping ONLY for 24 corner stickers.

    measured maps the 14 selected original spatial corner-slot indexes to
    measured actual 6-color labels. No hidden state or edge parity is input.
    """
    assert set(measured)==set(CORNER14)
    decoded={}
    assigned={}
    for dest in SEVEN:
        facelets=PIECES[dest][:2]
        signature=tuple(measured[j] for j in facelets)
        matches=[(src,twist) for src in CORNERS for twist in range(3)
                 if oriented_corner_signature(src,dest,twist,facelets)
                    ==signature]
        assert len(matches)==1,(dest,signature,matches)
        src,twist=matches[0]
        assert src not in assigned
        assigned[src]=(dest,twist)
    assert len(assigned)==7
    last_src=next(iter(set(CORNERS)-set(assigned)))
    last_twist=(-sum(t for dest,t in assigned.values()))%3
    assigned[last_src]=(LAST,last_twist)
    assert len(assigned)==8
    for src,(dest,twist) in assigned.items():
        for i,original in enumerate(PIECES[src]):
            decoded[original]=PIECES[dest][(i+twist)%3]
    assert len(decoded)==24
    assert all(
        SOURCE_FACE_COLOR[next(src for src,target in decoded.items()
                               if target==slot)]==color
        for slot,color in measured.items()
    )
    return decoded,assigned

def corner_parity_from_decoding(assigned):
    position_index={pos:i for i,pos in enumerate(CORNERS)}
    order=[position_index[assigned[src][0]] for src in CORNERS]
    return sum(order[i]>order[j] for i in range(8)
               for j in range(i+1,8))%2

def frame14():
    paths=joint_sticker_orbit()
    assert len(paths)==576
    pairs=tuple(zip(EDGE_STICKERS[:14],CORNER14))
    plan=[]
    for edge,corner in pairs:
        commands=tuple(inverted_token(token) for token in
                       reversed(paths[(edge,corner)]))
        target=word(" ".join(commands))
        assert (target[edge],target[corner])==(
            EDGE_FACELET,CORNER_FACELET)
        plan.append((edge,corner,commands,target))
    return tuple(plan)

def observe14(state,plan):
    current=IDENTITY
    previous=()
    measured={}
    htm=0
    for edge,corner,commands,target in plan:
        relative=tuple(inverted_token(x) for x in reversed(previous))+commands
        delta=word(" ".join(relative))
        assert delta==compose(target,inverse(current))
        current=compose(delta,current)
        assert current==target
        edge_color,corner_color=two_one_facelet_colors(state,current)
        assert edge_color==SOURCE_FACE_COLOR[inverse(state)[edge]]
        measured[corner]=corner_color
        previous=commands
        htm+=len(relative)
    return measured,htm

def audit():
    # Exact 8 destinations x 3 possible omitted faces x 24 configurations.
    for dest in CORNERS:
        for missing in range(3):
            keep=tuple(x for i,x in enumerate(PIECES[dest]) if i!=missing)
            signatures={oriented_corner_signature(src,dest,t,keep)
                        for src in CORNERS for t in range(3)}
            assert len(signatures)==24,(dest,missing,len(signatures))
    print("R11_CORNER_TWO_FACELET_LOCAL_BIJECTION_PASS",
          "positions",8,"two_facelet_choices_per_position",3,
          "oriented_cubie_signatures_each",24)

    plan=frame14()
    states,_=ball(2)
    assert len(states)==262
    sample_words=(
        "U R F' D2 L B U' F2",
        "R U' B2 D F L' U2 R' B F",
        "L F R' F' L' U2 R U R U' R2 U2 R",
    )
    tested=tuple(states)+tuple(word(x) for x in sample_words)
    sumhtm=0
    for g in tested:
        measured,htm=observe14(g,plan)
        mapping,assigned=decode14(measured)
        for src in CORNERS:
            for sticker in PIECES[src]:
                assert mapping[sticker]==g[sticker]
        assert sum(factor_value(src,g)%3 for src in CORNERS)%3==0
        assert sum(t for d,t in assigned.values())%3==0
        sumhtm+=htm
    print("R11_CORNER14_FULL_STATE_WITHOUT_ORACLE_P48_PASS",
          "frames",14,"B2_replays",len(states),
          "long_controls",len(sample_words),"trials",len(tested),
          "executed_turns_sum",sumhtm)
    print("R11_SCOPE full corner reconstruction by frame14;",
          "not full cube <=20 or human-cognition evidence")
    return len(tested)

if __name__=="__main__":
    audit()
