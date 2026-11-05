#!/usr/bin/env python3
"""R11: 14 categorical corner-facelet reads suffice for EVERY legal Rubik cube.

Key local fact: for an oriented P48 corner position, the ORDERED pair of
colors at two chosen facelet slots uniquely identifies its original corner
label and its legal 3-cycle orientation. All 8*3=24 such corner states
yield 24 distinct ordered color pairs because of spatial corner chirality.

Read two facelets in seven fixed spatial corner positions (14 readings);
identify their seven original pieces/orientations individually. Remaining
corner label by exclusion, remaining twist by sum modulo three. No edge
parity, edge state, original sticker identities or free state oracle.

This is a corner-subsystem theorem, NOT 14-frame full Rubik identification.
"""
from b6_independent_48sticker_goals import (
    EDGE_POS, CORNERS, PIECES, SLOTS, word, factor_value, compose,
)
from construct_color_p48_24_frame_scanner import (
    EDGE_STICKERS, SOURCE_FACE_COLOR, EDGE_FACELET, CORNER_FACELET,
    joint_sticker_orbit, inverted_token
)
from audit_color_probe_information_bounds import two_one_facelet_colors

KNOWN=CORNERS[:7]
LAST=CORNERS[7]
READ=tuple(s for corner in KNOWN for s in PIECES[corner][:2])
assert len(READ)==14

def pair_catalog():
    signatures={}
    for original in CORNERS:
        src=PIECES[original]
        for twist in range(3):
            # original sticker i occupies target sticker (i+twist) mod 3.
            ordered=(SOURCE_FACE_COLOR[src[(-twist)%3]],
                     SOURCE_FACE_COLOR[src[(1-twist)%3]])
            assert ordered not in signatures,(ordered,original,twist,signatures.get(ordered))
            signatures[ordered]=(original,twist)
    assert len(signatures)==24
    return signatures

def decode14(colors):
    assert set(colors)==set(READ)
    catalog=pair_catalog()
    result={}
    found=set()
    for position in KNOWN:
        slots=PIECES[position]
        signature=tuple(colors[j] for j in slots[:2])
        assert signature in catalog,(position,signature)
        original,twist=catalog[signature]
        assert original not in found
        found.add(original)
        for i,source_slot in enumerate(PIECES[original]):
            result[source_slot]=slots[(i+twist)%3]
    assert len(found)==7
    missing=next(iter(set(CORNERS)-found))
    possible=[]
    for twist in range(3):
        trial=list(range(48))
        for s,d in result.items():
            trial[s]=d
        for i,s in enumerate(PIECES[missing]):
            trial[s]=PIECES[LAST][(i+twist)%3]
        if sum(factor_value(p,trial)%3 for p in CORNERS)%3==0:
            possible.append(tuple(trial[s] for p in CORNERS for s in PIECES[p]))
    assert len(possible)==1
    return possible[0]

def schedule():
    route=joint_sticker_orbit()
    return tuple(
        (e,c,tuple(inverted_token(t) for t in reversed(route[(e,c)])))
        for e,c in zip(EDGE_STICKERS[:14],READ)
    )

def replay(cube,plan):
    colors={}
    previous=()
    frame=bytes(range(48))
    turns=0
    for edge_slot,corner_slot,next_abs in plan:
        delta=tuple(inverted_token(t) for t in reversed(previous))+next_abs
        frame=compose(word(" ".join(delta)),frame)
        assert frame==word(" ".join(next_abs))
        assert (frame[edge_slot],frame[corner_slot])==(EDGE_FACELET,CORNER_FACELET)
        observed_edge,observed_corner=two_one_facelet_colors(cube,frame)
        assert observed_corner==SOURCE_FACE_COLOR[cube.index(corner_slot)]
        colors[corner_slot]=observed_corner
        previous=next_abs
        turns+=len(delta)
    decoded=decode14(colors)
    true=tuple(cube[s] for p in CORNERS for s in PIECES[p])
    assert decoded==true,(decoded,true)
    return turns

def audit():
    catalog=pair_catalog()
    from audit_active_p48_small_ball_decision_trees import ball
    states,_=ball(2)
    samples=list(states)
    from audit_r11_corner20_no_oracle import corner_source_pair_samples
    samples+=corner_source_pair_samples()
    for seq in (
        "U R F U' R' F'", "U2 R' B D2 B' R U2 R' B D2 B' R",
        "L F R' F' L' U2 R U R U' R2 U2 R",
        "R F2 B' L2 U R D' F",
    ):
        samples.append(word(seq))
    assert len(samples)==434
    plan=schedule()
    turns={replay(s,plan) for s in samples}
    assert len(turns)==1
    print("R11_ALL_24_ORDERED_CORNER_COLOR_PAIRS_UNIQUE_PASS",len(catalog))
    print("R11_CORNER_14_NO_EDGE_ORACLE_PASS",
          "physical_states",len(samples),"corner_colors",len(READ),
          "read_corner_positions",len(KNOWN))
    print("R11_CORNER14_P48_NO_RESET_PASS","joint_orbit",576,
          "per_trial_htm",next(iter(turns)))
    print("R11_LIMIT full-cube adaptive bound remains 18..21;",
          "edge identification and joint 20-frame solution not established")
    return len(samples)

if __name__=="__main__":
    audit()
