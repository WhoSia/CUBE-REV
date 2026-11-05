#!/usr/bin/env python3
"""R11: 13 corner color reads suffice with ONE parity bit of edge information.

First 6 spatial corner positions: TWO ordered colors each. A unique oriented
corner type matches each of these 12 ordered-color readings (chirality).
Of the two remaining original corner labels, the known true edge permutation
parity determines which belongs in the seventh spatial corner. One further
seventh-slot color fixes its 3-cycle orientation; corner twist sum fixes
the eighth. Uses 13 physical corner-color observations, no labels/orientations
directly sensed, actual no-reset 18-HTM moves.

This is only the corner subsystem conditioned on a one-bit edge oracle,
NOT an entire 13-frame or 20-frame Rubik cube policy.
"""
from b6_independent_48sticker_goals import (
    EDGE_POS, CORNERS, PIECES, SLOTS, word, factor_value, compose,
)
from construct_color_p48_24_frame_scanner import (
    EDGE_STICKERS, SOURCE_FACE_COLOR, EDGE_FACELET, CORNER_FACELET,
    joint_sticker_orbit, inverted_token,
)
from audit_color_probe_information_bounds import two_one_facelet_colors
from construct_color_p48_21_frame_legality_scan import permutation_parity
from audit_r11_corner14_chirality import pair_catalog
from audit_r11_corner19_edge_parity import cubie_parity

KNOWN6=CORNERS[:6]
SEVENTH=CORNERS[6]
EIGHTH=CORNERS[7]
SLOTS13=tuple(s for p in KNOWN6 for s in PIECES[p][:2])+(PIECES[SEVENTH][0],)
assert len(SLOTS13)==13

def decode13(colors,edge_parity):
    assert set(colors)==set(SLOTS13)
    assert edge_parity in (0,1)
    catalogue=pair_catalog()
    known={}
    source_to_dest={}
    for dest in KNOWN6:
        pair=tuple(colors[s] for s in PIECES[dest][:2])
        source,twist=catalogue[pair]
        assert source not in source_to_dest
        source_to_dest[source]=dest
        for i,s in enumerate(PIECES[source]):
            known[s]=PIECES[dest][(i+twist)%3]
    missing=sorted(set(CORNERS)-source_to_dest)
    assert len(missing)==2
    index={p:i for i,p in enumerate(CORNERS)}
    possibilities=[]
    for first,second in ((missing[0],missing[1]),(missing[1],missing[0])):
        labels=dict(source_to_dest)
        labels[first]=SEVENTH
        labels[second]=EIGHTH
        parity=permutation_parity([index[labels[p]] for p in CORNERS])
        if parity!=edge_parity:continue
        for twist in range(3):
            trial=known.copy()
            for i,s in enumerate(PIECES[first]):
                trial[s]=PIECES[SEVENTH][(i+twist)%3]
            color_src=next(s for s in PIECES[first] if
                           trial[s]==PIECES[SEVENTH][0])
            if SOURCE_FACE_COLOR[color_src]!=colors[PIECES[SEVENTH][0]]:
                continue
            for final_twist in range(3):
                candidate=trial.copy()
                for i,s in enumerate(PIECES[second]):
                    candidate[s]=PIECES[EIGHTH][(i+final_twist)%3]
                state=list(range(48))
                for s,d in candidate.items():
                    state[s]=d
                if sum(factor_value(p,state)%3 for p in CORNERS)%3==0:
                    possibilities.append(tuple(candidate[s] for p in CORNERS
                                               for s in PIECES[p]))
    assert len(possibilities)==1,(len(possibilities),edge_parity)
    return possibilities[0]

def schedule13():
    paths=joint_sticker_orbit()
    return tuple((e,c,tuple(inverted_token(t) for t
                      in reversed(paths[(e,c)])))
                 for e,c in zip(EDGE_STICKERS[:13],SLOTS13))

def replay(state,plan):
    colors={}
    current=bytes(range(48))
    previous=()
    total=0
    for e,c,commands in plan:
        relative=tuple(inverted_token(t) for t in reversed(previous))+commands
        current=compose(word(" ".join(relative)),current)
        assert current==word(" ".join(commands))
        edge_col,corner_col=two_one_facelet_colors(state,current)
        assert corner_col==SOURCE_FACE_COLOR[state.index(c)]
        colors[c]=corner_col
        previous=commands
        total+=len(relative)
    reconstructed=decode13(colors,cubie_parity(state,EDGE_POS))
    assert reconstructed==tuple(state[s] for p in CORNERS for s in PIECES[p])
    return total

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
    p=schedule13()
    turns={replay(state,p) for state in samples}
    assert len(turns)==1
    print("R11_CORNER_13_EDGE_PARITY_ONE_BIT_PASS","physical_states",
          len(samples),"corner_colors",len(SLOTS13),"parity_bits",1)
    print("R11_CORNER13_P48_NO_RESET_PASS","joint_orbit",576,
          "per_trial_htm",next(iter(turns)))
    print("R11_LIMIT not a complete cube identification policy")
if __name__=="__main__":
    audit()
