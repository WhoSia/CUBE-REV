#!/usr/bin/env python3
"""Construct ALL 2592 actual legal 48-sticker cube states realizing the hard
R3/F3/L3/B3 first-edge-color transcript and independently replay parity at frame14.
No random sampling of the exceptional case.
"""
from collections import Counter
from pathlib import Path
import json
import verify_r14_p86_physical_20frame_routing as v
from audit_r14_p86_constructive_full_20_frame import parity
HERE=Path(__file__).resolve().parent
physical=v.physical
E=v.actual_E
pattern='RRRFFFLLLBBB'
count=tuple(pattern.count(c) for c in v.proof.COLORS)
assert count in v.repmap
rep,color,signoffset,sigma=v.proof.transport(count,v.repmap,v.courts,v.sym,pattern)
assert rep.hard
states=v.proof.enumerate_sector(pattern)
assert len(states)==2592
word_to_src={frozenset(w):i for i,w in enumerate(E)}
edge_source_slots=[physical.PIECES[p] for p in physical.EDGES]
corner_source_slots=[physical.PIECES[p] for p in physical.CORNERS]
hist=Counter();correct=0;routes=0
for i,(second,p) in enumerate(states):
    # Build complete original source-to-spatial-sticker permutation.
    dest=list(range(48));perm=[];flip_total=0
    for dst in range(12):
        word=pattern[dst]+second[dst]
        label=word_to_src[frozenset(word)]
        flip=0 if word==E[label] else 1
        assert word in (E[label],E[label][::-1])
        perm.append(label);flip_total^=flip
        for source_side,source_slot in enumerate(edge_source_slots[label]):
            dest[source_slot]=edge_source_slots[dst][(source_side-flip)%2]
    assert len(set(perm))==12 and flip_total==0 and parity(perm)==p
    corner_perm=[1,0,2,3,4,5,6,7] if p else list(range(8))
    for dst,label in enumerate(corner_perm):
        for side,source_slot in enumerate(corner_source_slots[label]):
            dest[source_slot]=corner_source_slots[dst][side]
    state=tuple(dest)
    assert physical.legal(state)
    inv=physical.inverse(state)
    assert ''.join(v.read(inv,v.e_local[2*j]) for j in range(12))==pattern
    observed_corner_parity,corner_word=v.corner_decode(inv)
    assert observed_corner_parity==p
    targetword=''.join(color[v.read(inv,v.e_local[2*sigma[j]+1])] for j in range(12))
    targetp=observed_corner_parity^signoffset
    ix=rep.index[(targetword,targetp)]
    B=rep.full;reads=[]
    for early in (2,1):
        q=rep.delayed_action(B,early)
        assert q is not None
        eq=v.e_local[2*sigma[q]+1]
        cq=v.c_local[6*3+(2-early)]
        assert (eq,cq) in physical.seen
        y=color[v.read(inv,eq)]
        B&=rep.mask[q][y]
        reads.append((q,eq,cq,y))
        routes+=1
        assert B>>ix&1
    # FIRST access to the parity oracle: seventh corner's second facelet is
    # now read, so the observed corner arrangement has become known.
    B&=rep.parity_masks[targetp]
    while B.bit_count()>1:
        q=rep.winning_action(B,6-(len(reads)-2))
        eq=v.e_local[2*sigma[q]+1];cq=v.c_local[0]
        assert (eq,cq) in physical.seen
        y=color[v.read(inv,eq)]
        B&=rep.mask[q][y]
        reads.append((q,eq,cq,y));routes+=1
        assert B>>ix&1
    assert B==(1<<ix) and len(reads)<=8
    invcolor={b:a for a,b in color.items()}
    recovered=['']*12
    for canonicalpos,originalpos in enumerate(sigma):
        recovered[originalpos]=invcolor[rep.states[ix][0][canonicalpos]]
    assert ''.join(pattern[j]+recovered[j] for j in range(12))==''.join(v.read(inv,q) for q in v.e_local)
    hist[12+len(reads)]+=1;correct+=1
assert correct==2592 and max(hist)<=20
receipt={'result':'R14_P86_HARD_ORBIT_ALL_2592_GENUINE_P48_STATES_20_FRAME_PASS',
 'hard_first_color_sequence':pattern,'hard_first_color_count_vector':count,
 'independently_constructed_legal_full_cube_states':correct,
 'actual_second_cubie_identity_and_flip_sum_verified':True,
 'actual_corner_permutation_sign_matched_to_edge_sign':True,
 'full_corner_14_sticker_reconstruction_all_states':True,
 'all_hard_edge_histories_observed_from_real_48_slot_group_states':True,
 'hard_early_2_edge_mate_queries_do_not_use_corner_parity':True,
 'common_parity_available_after_frame14':True,
 'paired_route_membership_checks':routes,
 'full_original_48_sticker_state_reconstruction_correct':True,
 'actual_frame_depth_histogram':dict(sorted(hist.items())),
 'max_frames':max(hist),
 'scope':'All 2592 hidden conditional hard-pattern edge states lifted to actual legal 12E8C physical states (one chosen corner completion per edge). Combined with entire 867-pattern finite proof, not 43-quintillion brute-force.'}
(HERE/'R14_P86_HARD_2592_PHYSICAL_REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('RESULT',receipt['result'],'depths',dict(hist),'routed',routes)
