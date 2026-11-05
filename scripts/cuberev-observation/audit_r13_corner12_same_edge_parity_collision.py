#!/usr/bin/env python3
"""R11/R13 exact 13-read fixed CORNER optimum given one correct EDGE parity bit.

Every fixed set of <=12 spatial corner facelets admits TWO distinct legal
full P48 states sharing:
  - the same COMPLETE edge configuration (hence the same known parity bit),
  - the same observed corner facelet colors.
Proof constructive:
 * If at least three corner spatial positions have <=1 read facelet:
   assign three U-containing source corner labels to them, show U wherever
   a slot is observed, and cycle those three labels (an EVEN permutation).
   Corner twist totals can be matched by free shifts at unread positions,
   or cancel automatically if all three have a U-colored observed slot.
 * If precisely two positions have <=1 observed facelet (possible for <=12
   only when both are completely unobserved and all others have >=2):
   change the twists of those two, +1 and -1, holding labels fixed.
All other corners and ALL edges can be identical in the two legal states.
An actual finite P48 verifier tests masks with seeded random variation.
This is the fixed corner-only parity-oracle query problem, NOT the global
dual-sensor adaptive identification problem.
"""
from itertools import combinations
from random import Random
from b6_independent_48sticker_goals import (
    CORNERS,EDGE_POS,PIECES,SLOTS,factor_value,inverse
)
from construct_color_p48_24_frame_scanner import SOURCE_FACE_COLOR

ALL=tuple(s for p in CORNERS for s in PIECES[p])
U=tuple(p for p in CORNERS if "U" in
        tuple(SOURCE_FACE_COLOR[s] for s in PIECES[p]))
assert len(U)==4

def parity(order):
    return sum(order[i]>order[j] for i in range(len(order))
               for j in range(i+1,len(order)))%2

def construct(assigned):
    """Dest -> (source,cyclic twist); edge arrangement shared and legal."""
    assert len(assigned)==8 and set(assigned)==set(CORNERS)
    assert set(src for src,t in assigned.values())==set(CORNERS)
    s=list(range(48))
    for dest,(src,twist) in assigned.items():
        for k,st in enumerate(PIECES[src]):
            s[st]=PIECES[dest][(k+twist)%3]
    edges=list(range(48))
    dst_by_src={src:dest for dest,(src,t) in assigned.items()}
    perm=parity([CORNERS.index(dst_by_src[src]) for src in CORNERS])
    if perm:
        a,b=EDGE_POS[:2]
        for k,st in enumerate(PIECES[a]):s[st]=PIECES[b][k]
        for k,st in enumerate(PIECES[b]):s[st]=PIECES[a][k]
    state=bytes(s)
    assert len(set(state))==48
    assert sum(factor_value(p,state)%3 for p in CORNERS)%3==0
    assert sum(factor_value(p,state)%2 for p in EDGE_POS)%2==0
    edge_perm=parity([EDGE_POS.index(SLOTS[state[PIECES[src][0]]][0])
                      for src in EDGE_POS])
    assert edge_perm==perm
    return state

def needed_u_twist(src,dest,selected):
    read=tuple(s for s in PIECES[dest] if s in selected)
    assert len(read)<=1
    if not read:return None
    q=next(k for k,s in enumerate(PIECES[src])
           if SOURCE_FACE_COLOR[s]=="U")
    return (PIECES[dest].index(read[0])-q)%3

def construct_collision(mask):
    selected=set(mask)
    assert len(selected)==len(mask)<=12
    weak=tuple(p for p in CORNERS
               if sum(s in selected for s in PIECES[p])<=1)
    assert len(weak)>=2
    if len(weak)==2:
        a,b=weak
        assert all(s not in selected for p in weak for s in PIECES[p])
        # Leave exactly same labels and same edge state in both trials.
        d0={p:(p,0) for p in CORNERS}
        d1=dict(d0)
        d1[a]=(a,1);d1[b]=(b,2)
    else:
        a,b,c=weak[:3]
        weak3=(a,b,c)
        src3=U[:3]
        leftover_dest=tuple(p for p in CORNERS if p not in weak3)
        leftover_src=tuple(p for p in CORNERS if p not in src3)
        common={d:(s,0) for d,s in zip(leftover_dest,leftover_src)}
        d0=dict(common);d1=dict(common)
        target_sum=0
        zero_read_positions=[]
        for dest,source0,source1 in zip(weak3,src3,src3[1:]+src3[:1]):
            t0=needed_u_twist(source0,dest,selected)
            t1=needed_u_twist(source1,dest,selected)
            if t0 is None:
                zero_read_positions.append(dest);t0=0
            if t1 is None:t1=0
            d0[dest]=(source0,t0)
            d1[dest]=(source1,t1)
        sum0=sum(t for p,t in d0.values())%3
        sum1=sum(t for p,t in d1.values())%3
        if zero_read_positions:
            dest=zero_read_positions[0]
            src,t=d1[dest]
            d1[dest]=(src,(t+sum0-sum1)%3)
            sum1=sum(t for p,t in d1.values())%3
        assert sum1==sum0
        # Common unchanged corner corrects both twist totals.
        fix=leftover_dest[0]
        src,t=common[fix]
        d0[fix]=(src,(-sum0)%3)
        d1[fix]=(src,(-sum0)%3)
    g0=construct(d0);g1=construct(d1)
    assert g0!=g1
    # Exact same edges, not merely parity, so any amount of observed edge
    # color information is also identical between these two states.
    assert all(g0[s]==g1[s] for p in EDGE_POS for s in PIECES[p])
    i0=inverse(g0);i1=inverse(g1)
    assert all(SOURCE_FACE_COLOR[i0[s]]==SOURCE_FACE_COLOR[i1[s]]
               for s in selected)
    return g0,g1

def audit():
    rng=Random(28011105)
    masks=[(),tuple(ALL[:12]),tuple(ALL[-12:])]
    for n in range(13):
        for _ in range(160):
            masks.append(tuple(rng.sample(ALL,n)))
    for k in range(8):
        # Two completely unread corners, six with two readings: worst case
        # for the corner-twist adversary.
        unread=CORNERS[k:k+2] if k<7 else (CORNERS[-1],CORNERS[0])
        mask=tuple(PIECES[p][0] for p in CORNERS if p not in unread)+tuple(
            PIECES[p][1] for p in CORNERS if p not in unread)
        assert len(mask)==12
        masks.append(mask)
    for mask in masks:construct_collision(mask)
    print("R13_CORNER12_KNOWN_EDGE_PARITY_COLLISION_PASS",
          "P48_legal_mask_trials",len(masks),
          "same_complete_edges",True)
    print("R13_CORNER_FIXED_EDGE_PARITY_OPTIMUM_13",
          "lower_via_12_slot_even_parity_collision",
          "upper_via_6_complete_plus_1_partial_corner_decoder")
    print("R13_SCOPE fixed corner-only observation, known edge parity;",
          "no full-cube adaptive 20 bound")
if __name__=="__main__":audit()
