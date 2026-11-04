#!/usr/bin/env python3
"""Active fixed-site probes vs persistent original-tag sensors in P48 physics.

A fixed spatial site reports identity+full orientation of whichever cubie
occupies it. A persistent labelled sensor instead follows ONE original cubie.
These channels are distinct; exact reconstruction claims only the former.
"""
from collections import deque
from itertools import product
from b6_independent_48sticker_goals import (
    CORNERS, EDGE_POS, MOVES, PIECES, SLOTS, compose, inverse, word
)

REF_EDGE=EDGE_POS[0]
REF_CORNER=CORNERS[0]

def destination(position,permutation):
    slots={SLOTS[permutation[i]][0] for i in PIECES[position]}
    if len(slots)!=1:raise AssertionError("disassembled piece")
    return next(iter(slots))

def inverse_token(token):
    return token if token.endswith("2") else token[:-1] if token.endswith("'") else token+"'"

def joint_position_words():
    """Build 12x8 exact joint source-site orbit under the HTM actions."""
    ref=(REF_EDGE,REF_CORNER)
    queue=deque([ref])
    forward={ref:()}
    while queue:
        pair=queue.popleft()
        for token,m in MOVES.items():
            nxt=(destination(pair[0],m),destination(pair[1],m))
            if nxt not in forward:
                forward[nxt]=forward[pair]+(token,)
                queue.append(nxt)
    if len(forward)!=len(EDGE_POS)*len(CORNERS):
        raise AssertionError("the two cubie-type position orbits are not jointly transitive")
    actions={}
    for pair,path in forward.items():
        reverse=tuple(inverse_token(t) for t in reversed(path))
        frame=word(" ".join(reverse))
        if (destination(pair[0],frame),destination(pair[1],frame))!=ref:
            raise AssertionError("wrong reference-frame mapping")
        actions[pair]=reverse
    return actions

def twelve_frame_scan():
    """Twelve predetermined pairs cover all 12 edge and all 8 corner sites."""
    pairs=joint_position_words()
    out=[(e,CORNERS[i%8],pairs[(e,CORNERS[i%8])])
         for i,e in enumerate(EDGE_POS)]
    assert len(out)==12
    assert {p for p,c,a in out}==set(EDGE_POS)
    assert {c for p,c,a in out}==set(CORNERS)
    return out

def observe(state,position):
    """Read original cubie label and full oriented sticker tuple at fixed site."""
    hits=[]
    for label,stickers in PIECES.items():
        if {SLOTS[state[i]][0] for i in stickers}=={position}:
            hits.append((label,tuple(state[i] for i in stickers)))
    if len(hits)!=1:raise AssertionError("nonunique piece occupying fixed slot")
    return hits[0]

def reconstruct(initial_state,plan=None):
    """Execute scan using known relative moves and undo each frame action."""
    if plan is None:plan=twelve_frame_scan()
    if sorted(initial_state)!=list(range(48)):
        raise ValueError("not a complete physical sticker permutation")
    collected={}
    last=bytes(range(48))
    relative_actions=[]
    for _,_,commands in plan:
        frame=word(" ".join(commands))
        delta=compose(frame,inverse(last))
        last=compose(delta,last)
        assert last==frame
        physical=compose(frame,initial_state)
        reverse=inverse(frame)
        for site in (REF_EDGE,REF_CORNER):
            label,current=observe(physical,site)
            original_slots=tuple(reverse[s] for s in current)
            if label in collected and collected[label]!=original_slots:
                raise AssertionError("inconsistent time-series measurements")
            collected[label]=original_slots
        relative_actions.append(delta)
    if set(collected)!=set(PIECES):
        raise AssertionError("not all physical pieces ever observed")
    recovered=[None]*48
    for label,slots in collected.items():
        for sticker,slot in zip(PIECES[label],slots):
            recovered[sticker]=slot
    if tuple(recovered)!=tuple(initial_state):
        raise AssertionError("failed to recover initial 48-sticker state")
    return tuple(recovered),relative_actions

def eleven_frame_scan():
    """Eleven edge-site visits, all eight corner-site visits, no reset."""
    pairs=joint_position_words()
    plan=[(e,CORNERS[i%8],pairs[(e,CORNERS[i%8])])
          for i,e in enumerate(EDGE_POS[:-1])]
    assert len(plan)==11
    assert len({p for p,c,a in plan})==11
    assert {c for p,c,a in plan}==set(CORNERS)
    return plan

def reconstruct_with_edge_parity(initial_state,plan=None):
    """Recover the unobserved twelfth edge from legal cube parity constraints.

    The eleven complete edge readings give eleven destination slots and eleven
    orientation bits. On legal fixed-centre cubes, the last edge position is
    the remaining slot and its orientation is forced by sum(flips) == 0 mod 2.
    All eight original corners are visited in these same eleven frames.
    """
    if plan is None:plan=eleven_frame_scan()
    if sorted(initial_state)!=list(range(48)):
        raise ValueError("not a complete physical sticker permutation")
    recovered={}
    current_frame=bytes(range(48))
    for _,_,tokens in plan:
        frame=word(" ".join(tokens))
        relative=compose(frame,inverse(current_frame))
        current_frame=compose(relative,current_frame)
        assert current_frame==frame
        observed_state=compose(frame,initial_state)
        undo=inverse(frame)
        for site in (REF_EDGE,REF_CORNER):
            label,sticker_slots=observe(observed_state,site)
            original_slots=tuple(undo[j] for j in sticker_slots)
            if label in recovered and recovered[label]!=original_slots:
                raise AssertionError("conflicting original-slot observations")
            recovered[label]=original_slots
    known_edges={p:slots for p,slots in recovered.items() if p in EDGE_POS}
    if len(known_edges)!=11 or not set(CORNERS)<=set(recovered):
        raise AssertionError("scan did not cover eleven edges and eight corners")
    missing_label=next(iter(set(EDGE_POS)-set(known_edges)))
    occupied=set()
    parity_sum=0
    for slots in known_edges.values():
        d={SLOTS[j][0] for j in slots}
        assert len(d)==1
        destination_position=d.pop()
        assert destination_position in EDGE_POS
        occupied.add(destination_position)
        parity_sum+=PIECES[destination_position].index(slots[0])
    assert len(occupied)==11
    missing_position=next(iter(set(EDGE_POS)-occupied))
    missing_flip=(-parity_sum)%2
    recovered[missing_label]=tuple(
        PIECES[missing_position][(i+missing_flip)%2] for i in range(2))
    result=[None]*48
    for label,slots in recovered.items():
        for origin,physical in zip(PIECES[label],slots):
            result[origin]=physical
    if tuple(result)!=tuple(initial_state):
        raise AssertionError("eleven frames did not reconstruct legal state")
    return tuple(result)

def audit():
    sites=joint_position_words()
    plan=twelve_frame_scan()
    assert len(sites)==96 and len(plan)==12
    samples={"solved":bytes(range(48))}
    for name,m in MOVES.items():samples["one_"+name]=m
    for a,b in product(tuple(MOVES)[:6],repeat=2):
        samples["two_"+a+"_"+b]=word(a+" "+b)
    samples["long13"]=word("L F R' F' L' U2 R U R U' R2 U2 R")
    for name,state in samples.items():
        got,_=reconstruct(state,plan)
        assert got==tuple(state),name
    short_plan=eleven_frame_scan()
    for name,state in samples.items():
        assert reconstruct_with_edge_parity(state,short_plan)==tuple(state),name
    print("ACTIVE_P48_EXACT_11_FRAME_FULL_GROUP_SCAN_PASS tested_states=",len(samples))
    longest=max(len(w) for p,c,w in plan)
    print("ACTIVE_P48_96_JOINT_SITE_ORBIT_PASS")
    print("ACTIVE_P48_12_FRAME_TWO_PROBE_RECONSTRUCTION_PASS tested_states=",len(samples))
    print("ACTIVE_P48_MAX_REFERENCE_FRAME_WORD_LENGTH",longest)
    print("BOUNDARY not a shortest-move or shortest-observation-policy theorem")
    print("BOUNDARY persistent original-tag vs stationary site probes are distinct")
    return len(samples)

if __name__=="__main__":
    audit()
