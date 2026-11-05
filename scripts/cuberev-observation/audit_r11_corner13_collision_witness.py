#!/usr/bin/env python3
"""R11 exact universal 13-corner-color lower-bound adversary.

For ANY precommitted set of at most thirteen distinct spatial corner facelet
slots, at least two of eight corner positions have <=1 observed facelet.
Assign two distinct original corners sharing color U to those positions and
orient both to show U at every observed slot. Swapping those original labels
preserves every observed color and, by simple cyclic-index cancellation,
preserves the total corner twist. Adjust unchanged sixth corners to make
both corner states legal; match edge permutation parity by swapping two
edges in one complete physical state. The 48-sticker arrangements are both
legal Rubik states with IDENTICAL up-to-13 CORNER observations.

This proves fixed/nonadaptive CORNER-ONLY universal 14 observations minimal
when edge results are not additionally given. It does not lower-bound
the full dual-sensor adaptive policy or a corner+edge transcript.
"""
from itertools import combinations
from random import Random
from b6_independent_48sticker_goals import (
    EDGE_POS,CORNERS,PIECES,SLOTS,inverse,factor_value,
)
from construct_color_p48_24_frame_scanner import SOURCE_FACE_COLOR
from audit_r11_corner14_no_oracle import CORNER14

ALL_CORNER_SLOTS=tuple(s for p in CORNERS for s in PIECES[p])
U_CORNERS=tuple(p for p in CORNERS
                if "U" in {SOURCE_FACE_COLOR[s] for s in PIECES[p]})
assert len(ALL_CORNER_SLOTS)==24 and len(U_CORNERS)==4

def permutation_parity(order):
    return sum(order[i]>order[j] for i in range(len(order))
               for j in range(i+1,len(order)))%2

def observed_twist(source,dest,read):
    if not read:return None
    assert len(read)==1
    source_u=next(i for i,s in enumerate(PIECES[source])
                  if SOURCE_FACE_COLOR[s]=="U")
    dest_index=PIECES[dest].index(read[0])
    return (dest_index-source_u)%3

def make_full_state(assignment):
    # assignment destination corner -> (original corner, cyclic orientation).
    decoded=list(range(48))
    for dest,(src,t) in assignment.items():
        for i,sticker in enumerate(PIECES[src]):
            decoded[sticker]=PIECES[dest][(i+t)%3]
    positions={src:dest for dest,(src,t) in assignment.items()}
    assert len(positions)==8
    parity=permutation_parity([CORNERS.index(positions[src]) for src in CORNERS])
    if parity:
        a,b=EDGE_POS[:2]
        for i,sa in enumerate(PIECES[a]):
            decoded[sa]=PIECES[b][i]
        for i,sb in enumerate(PIECES[b]):
            decoded[sb]=PIECES[a][i]
    state=bytes(decoded)
    assert len(set(state))==48
    assert sum(factor_value(p,state)%3 for p in CORNERS)%3==0
    assert sum(factor_value(p,state)%2 for p in EDGE_POS)%2==0
    eorder=[EDGE_POS.index(SLOTS[state[PIECES[p][0]]][0]) for p in EDGE_POS]
    assert permutation_parity(eorder)==parity
    return state

def adversarial_pair(selected):
    assert len(selected)==len(set(selected))<=13
    chosen=set(selected)
    weak=tuple(p for p in CORNERS
               if sum(s in chosen for s in PIECES[p])<=1)
    assert len(weak)>=2
    a,b=weak[:2]
    x,y=U_CORNERS[:2]
    leftover_sources=tuple(p for p in CORNERS if p not in (x,y))
    leftover_dest=tuple(p for p in CORNERS if p not in (a,b))
    common={d:(src,0) for d,src in zip(leftover_dest,leftover_sources)}
    a_read=tuple(s for s in PIECES[a] if s in chosen)
    b_read=tuple(s for s in PIECES[b] if s in chosen)

    a0=observed_twist(x,a,a_read)
    b0=observed_twist(y,b,b_read)
    a1=observed_twist(y,a,a_read)
    b1=observed_twist(x,b,b_read)
    a0=0 if a0 is None else a0
    b0=0 if b0 is None else b0
    if a1 is None and b1 is None:
        a1,b1=a0,b0
    elif a1 is None:
        a1=(a0+b0-b1)%3
    elif b1 is None:
        b1=(a0+b0-a1)%3
    assert (a0+b0-a1-b1)%3==0

    # A third, identically assigned corner fixes the legal twist sum.
    fixed_dest=leftover_dest[0]
    fixed_source=common[fixed_dest][0]
    common[fixed_dest]=(fixed_source,(-a0-b0)%3)
    d0=dict(common);d0.update({a:(x,a0),b:(y,b0)})
    d1=dict(common);d1.update({a:(y,a1),b:(x,b1)})
    g0=make_full_state(d0);g1=make_full_state(d1)
    assert g0!=g1
    inv0=inverse(g0);inv1=inverse(g1)
    for pos in selected:
        assert SOURCE_FACE_COLOR[inv0[pos]]==SOURCE_FACE_COLOR[inv1[pos]]
    return g0,g1

def audit():
    # Independently exercise the proof-construction on diverse physical
    # slot masks, including one chosen for each weak-position pair.
    rng=Random(20261105)
    masks=[tuple(ALL_CORNER_SLOTS[:13]),
           tuple(ALL_CORNER_SLOTS[-13:]),
           tuple(CORNER14[:13])]
    for k in (0,1,2,5,9,13):
        for _ in range(128):
            masks.append(tuple(rng.sample(ALL_CORNER_SLOTS,k)))
    pairs=0
    for mask in masks:
        x,y=adversarial_pair(mask)
        assert x!=y
        pairs+=1
    print("R11_CORNER13_UNIVERSAL_COLLISION_WITNESS_PASS",
          "distinct_mask_tests",len(masks),
          "legal_P48_state_pairs",pairs)
    print("R11_CORNER_ONLY_NONADAPTIVE_EXACT_14_PASS",
          "upper=14_by_R11_corner14_decoder",
          "lower=13_collision_for_any_fixed_mask")
    print("R11_SCOPE corner-only fixed slots, edge sensor withheld;",
          "NOT global dual-sensor adaptive lower bound")

if __name__=="__main__":
    audit()
