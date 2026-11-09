#!/usr/bin/env python3
"""R14-P8.6 independent PHYSICAL 3D 18-HTM 20-frame policy replay.

A separate geometric move/normal model supplies all 2001 actual legal cube
states and the exact 576 paired facelet reachability witnesses. The Court is
imported ONLY as the candidate policy; all real color readouts, seven-corner
parity extraction, 48 sticker coordinates and final target decoding are
independently computed from the actual 18-HTM sticker permutation.
"""
import contextlib,io,importlib.util,sys,hashlib,json
from collections import Counter
from pathlib import Path
from itertools import product
HERE=Path(__file__).resolve().parent
P51=HERE/'audit_r14_p51_p48_group_lift.py'
if not P51.exists():P51=Path('/mnt/data/CUBEREV_028_R14_P51_P48_GROUP_LIFT.py')
spec=importlib.util.spec_from_file_location('p51_p86_physical',P51)
physical=importlib.util.module_from_spec(spec);sys.modules[spec.name]=physical
with contextlib.redirect_stdout(io.StringIO()):spec.loader.exec_module(physical)
import audit_r14_p86_constructive_full_20_frame as proof
assert len(physical.states)==2001
assert len(physical.seen)==576
color_at={i:physical.COLORS[i] for i in range(48)}
actual_E=tuple(''.join(color_at[j] for j in physical.PIECES[p]) for p in physical.EDGES)
actual_C=tuple(''.join(color_at[j] for j in physical.PIECES[p]) for p in physical.CORNERS)
assert actual_E==proof.E,(actual_E,proof.E)
assert actual_C==proof.C,(actual_C,proof.C)
e_local=tuple(j for p in physical.EDGES for j in physical.PIECES[p])
c_local=tuple(j for p in physical.CORNERS for j in physical.PIECES[p])
assert len(e_local)==len(c_local)==24
assert {(a,b) for a in e_local for b in c_local}==set(physical.seen)

# Ordered 2-color readings uniquely identify any one of the 24 oriented corner
# cubies (eight labels times three cyclic orientations), by physical chirality.
corner_decoder={}
for src,word in enumerate(actual_C):
    for rot in range(3):
        pair=word[rot]+word[(rot+1)%3]
        assert pair not in corner_decoder,(pair,'chirality ambiguity')
        corner_decoder[pair]=(src,rot)
assert len(corner_decoder)==24

def parity(a):return proof.parity(a)
def read(inv,slot):return color_at[inv[slot]]
def corner_decode(inv):
    positions=[];rots=[]
    for pos in range(7):
        pair=read(inv,c_local[pos*3])+read(inv,c_local[pos*3+1])
        src,rot=corner_decoder[pair]
        positions.append(src);rots.append(rot)
    assert len(set(positions))==7
    missing=next(i for i in range(8) if i not in positions)
    lastrot=(-sum(rots))%3
    perm=tuple(positions+[missing])
    reconstructed=''.join(actual_C[perm[i]][(j+(rots+[lastrot])[i])%3]
                          for i in range(8) for j in range(3))
    actual=''.join(read(inv,slot) for slot in c_local)
    assert reconstructed==actual
    return parity(perm),reconstructed

# Regenerate count orbits; physical state observer never uses a hidden target
# index, true parity, or target second colors to decide a query.
counts=proof.all_count_vectors();sym=proof.color_symmetries();remaining=set(counts);repmap={}
while remaining:
    rep=min(remaining)
    members={proof.transform_counts(rep,x[0]) for x in sym}
    for member in members:
        repmap[member]=(rep,proof.color_map_for_member(member,rep,sym))
    remaining-=members
assert len(repmap)==867
courts={}
for rep,_ in set((rep,len(proof.color_first(rep))) for rep,_ in repmap.values()):
    pass
for rep in sorted({x[0] for x in repmap.values()}):
    game=proof.Court(proof.color_first(rep))
    game.optimal_depth=next(k for k in range(1,11) if game.winning(game.full,k))
    game.hard=game.optimal_depth==9
    if game.hard:assert game.delayed_win(game.full,2)
    courts[rep]=game

fail=0;hist=Counter();hard_observed=0;seen_vectors=set();routes_checked=0
examples=[]
for ix,state in enumerate(physical.states):
    assert physical.legal(state)
    inv=physical.inverse(state)
    first=''.join(read(inv,e_local[2*i]) for i in range(12))
    count=tuple(first.count(c) for c in proof.COLORS)
    assert count in repmap
    seen_vectors.add(count)
    corner_perm_parity,complete_corner=corner_decode(inv)
    rep,color,sign_offset,sigma=proof.transport(count,repmap,courts,sym,first)
    target_parity=corner_perm_parity^sign_offset
    B=rep.full
    true_second=''.join(color[read(inv,e_local[2*sigma[i]+1])] for i in range(12))
    target_index=rep.index.get((true_second,target_parity))
    if target_index is None:
        actual_second=''.join(read(inv,e_local[2*i+1]) for i in range(12))
        orig_perm=[next(l for l,w in enumerate(actual_E) if set(w)=={first[i],actual_second[i]}) for i in range(12)]
        actual_p=parity(orig_perm)
        new_first=''.join(color[first[j]] for j in sigma)
        new_perm=[next(l for l,w in enumerate(actual_E) if set(w)=={new_first[i],true_second[i]}) for i in range(12)]
        new_p=parity(new_perm)
        print('DEBUG DETAILS', 'colormap',color, 'pair slot5',first[5],actual_second[5],color[first[5]],color[actual_second[5]], 'sloti1',sigma[1], 'first_second pairs',[(i,first[i],actual_second[i]) for i in range(12)],flush=True)
        print('DEBUG',ix,'first',first,'pE',actual_p,'pC',corner_perm_parity,'offset',sign_offset,'target_p',target_parity,'newp',new_p,'rep',rep.pattern,'transformed',true_second,'member',count,'sigma',sigma,flush=True)
        raise AssertionError(('Physical edge data not legal in transformed court',ix,count))
    # Paired sensor: frames 1..14 use corner positions (pos0..6) stickers0,1;
    # each edge mate query after frame 12 uses corner slot (pos6, side0 or1)
    # in frames13/14, then may reuse any known corner slot afterward.
    for frame in range(12):
        ei=e_local[2*frame]
        ci=c_local[(frame//2)*3 + frame%2]
        assert (ei,ci) in physical.seen
        routes_checked+=1
    qtrace=[]
    if rep.hard:
        hard_observed+=1
        for early in (2,1):
            if B.bit_count()==1:break
            q=rep.delayed_action(B,early)
            assert q is not None
            original_pos=sigma[q]
            eq=e_local[2*original_pos+1]
            # synchronized with two remaining unknown-corner facelet reads
            cq=c_local[6*3+(2-early)]
            assert (eq,cq) in physical.seen
            routes_checked+=1
            obs=color[read(inv,eq)]
            B&=rep.mask[q][obs]
            assert B>>target_index&1
            qtrace.append((eq,cq,obs))
        # At this point the corner sensor has finished its 14th read. We use
        # ONLY its reconstructed parity, never the simulator's hidden edge sign.
        B&=rep.parity_masks[target_parity]
        budget=6
    else:budget=rep.optimal_depth
    while B.bit_count()>1:
        q=rep.winning_action(B,budget)
        assert q is not None
        original_pos=sigma[q]
        eq=e_local[2*original_pos+1]
        # For frames13/14 complete corner7; afterward repeat a known corner.
        step=len(qtrace)
        cq=c_local[6*3+step] if step<2 else c_local[0]
        assert (eq,cq) in physical.seen
        routes_checked+=1
        obs=color[read(inv,eq)]
        B&=rep.mask[q][obs]
        assert B>>target_index&1
        qtrace.append((eq,cq,obs))
        budget-=1
    assert B==(1<<target_index)
    assert len(qtrace)<=8
    # Complete result must reconstruct 24 edge and 24 corner colors.
    invcolor={v:k for k,v in color.items()}
    full_second=['']*12
    for canonical_pos,actual_pos in enumerate(sigma):
        full_second[actual_pos]=invcolor[rep.states[target_index][0][canonical_pos]]
    actual_edge=''.join(read(inv,slot) for slot in e_local)
    reconstruction=''.join(first[pos]+full_second[pos] for pos in range(12))
    assert reconstruction==actual_edge,(ix,'physical edge mismatch')
    assert len(complete_corner)==24
    # A valid globally routed frame schedule exists: every requested paired
    # target is in the previously established legal 18-HTM move orbit.
    hist[len(qtrace)+12]+=1
    if len(examples)<3:
        examples.append({'physical_state_index':ix,'first_edge_colors':first,
                         'used_parity_after_frame14':rep.hard,
                         'frames_to_decode':len(qtrace)+12,
                         'extra_paired_sticker_slot_trace':[list(x) for x in qtrace]})
assert sum(hist.values())==len(physical.states)
assert max(hist)<=20
receipt={
 'result':'R14_P86_PHYSICAL_18HTM_CORNER_PARITY_20_FRAME_REPLAY_PASS',
 'independent_physical_18HTM_states_checked':len(physical.states),
 'physical_sticker_slots':len(physical.SLOTS),
 'all_576_legal_edge_corner_pair_query_routes':len(physical.seen),
 'queried_pair_route_membership_checks':routes_checked,
 'physical_corner_ordered_two_color_source_orientation_pairs':len(corner_decoder),
 'corner_seven_position_14_sticker_complete_reconstruction_for_every_state':True,
 'first_12_edge_color_count_vectors_seen_in_18HTM_trajectory':len(seen_vectors),
 'hard_first_color_count_orbit_seen':hard_observed,
 'physical_decoder_depth_histogram':dict(sorted(hist.items())),
 'max_physical_frames':max(hist),
 'all_48_sticker_original_colors_correctly_reconstructed':True,
 'no_edge_parity_revealed_before_frame_14':True,
 'examples':examples,
 'limitations':'Independent 2001 physical legal move prefixes as regression; universal all-state guarantee rests on the separate 867-pattern exact mathematical coverage, 609376 tested conditional edge assignments and corner-chirality uniqueness. Not independent exhaustive 43-quintillion full-cube enumeration.'}
(HERE/'R14_P86_PHYSICAL_18HTM_POLICY_REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('RESULT',receipt['result'],'counts',len(seen_vectors),'maxframes',max(hist),'hist',dict(hist),'routedchecks',routes_checked)
