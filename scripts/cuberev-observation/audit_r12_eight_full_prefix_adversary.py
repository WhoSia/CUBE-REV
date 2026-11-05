#!/usr/bin/env python3
"""R12: adversarial obstruction for ANY eight-complete-edge 16-read prefix.

Claim restricted to deterministic policies whose first 16 EDGE readouts
are the two individual spatial facelets at eight distinct edge positions,
possibly in any adaptive/interleaved order. Corners can be freely observed
but cannot add extra EDGE information once we adversarially fix them solved.

An adversary assigns the eight non-U original edge labels as each spatial
edge position is first touched. It can complete the prefix consistently
no matter which unvisited position the policy chooses. The remaining
four original edge labels are the U-star UR/UF/UL/UB. For a given corner
state and the known prefix, 96 fully legal parity-compatible edge states
remain, and the exact R8 physical minimax shows they require FIVE
more edge-color reads. Therefore no such 16+4 strategy identifies all
full cube states in 20 frames. This does NOT rule out early partial
edge observations and mixed prefix structures, nor does it improve the
universal 18 lower bound.
"""
from random import Random
from itertools import permutations,product
from b6_independent_48sticker_goals import EDGE_POS,CORNERS,PIECES,SLOTS,factor_value
from audit_r8_four_edge_adaptive_subproblems import TYPES,states_for,minimax_depth

def parity(a):
    return sum(a[i]>a[j] for i in range(len(a))
               for j in range(i+1,len(a)))%2

LABELS={frozenset(t):i for i,t in enumerate(TYPES)}
U_STAR=tuple(LABELS[frozenset(t)] for t in ("UR","UF","UL","UB"))
assert len(set(U_STAR))==4

def chosen_prefix(seed):
    """One of many color/history-dependent order choices, not the proof."""
    rng=Random(seed)
    all_positions=list(range(12))
    pending={}
    known=list(i for i in range(12) if i not in U_STAR)
    # Choose a new position in an explicitly feedback-dependent way;
    # after revealing its full pair, the following choice changes.
    histories=[]
    for source in known:
        assert all_positions
        r=rng.randrange(len(all_positions))
        pos=all_positions.pop(r)
        pending[pos]=source
        histories.append((pos,tuple(TYPES[source])))
        rng.seed((seed+1)*131+(r+1)*37+(source+1)*43+len(histories)*17)
    assert len(pending)==8 and len(all_positions)==4
    return pending,tuple(all_positions),tuple(histories)

def parity_states(prefix,unknown_dest):
    """Construct all physically legal P48 completions, preserving prefix."""
    assert len(prefix)==8 and len(unknown_dest)==4
    missing=U_STAR
    baseline=[None]*12
    for dest,src in prefix.items():baseline[dest]=src
    for dest,src in zip(sorted(unknown_dest),missing):baseline[dest]=src
    required_pp=parity(baseline) # even corner permutation, must compensate
    candidates=[]
    for p in permutations(range(4)):
        if parity(p)!=required_pp:continue
        for flips in product(range(2),repeat=4):
            if sum(flips)%2:continue
            out=list(range(48))
            for dest,src in prefix.items():
                for k,sticker in enumerate(PIECES[EDGE_POS[src]]):
                    out[sticker]=PIECES[EDGE_POS[dest]][k]
            for j,dest in enumerate(sorted(unknown_dest)):
                src=missing[p[j]]
                for k,s in enumerate(PIECES[EDGE_POS[src]]):
                    out[s]=PIECES[EDGE_POS[dest]][(k+flips[j])%2]
            assert len(set(out))==48
            assert all(out[s]==s for c in CORNERS for s in PIECES[c])
            assert sum(factor_value(e,out)%2 for e in EDGE_POS)%2==0
            out_dest=[]
            for src in EDGE_POS:
                found={SLOTS[out[s]][0] for s in PIECES[src]}
                assert len(found)==1
                out_dest.append(EDGE_POS.index(next(iter(found))))
            assert parity(out_dest)==0
            candidates.append(tuple(out))
    assert len(candidates)==96 and len(set(candidates))==96
    return candidates

def audit():
    outcomes=[]
    for pp in (0,1):
        for flip in (0,1):
            assert len(states_for(U_STAR,pp,flip))==96
            assert minimax_depth(U_STAR,pp,flip)==5
            outcomes.append((pp,flip,5))
    assert len(outcomes)==4
    checked=0
    for seed in range(32):
        prefix,unknown,history=chosen_prefix(seed)
        states=parity_states(prefix,unknown)
        # The revealed 16 edge colors in this conditional family are
        # identical for all 96 legal possible hidden states.
        for pos,original in prefix.items():
            e0,e1=PIECES[EDGE_POS[pos]]
            target_pair=tuple(TYPES[original])
            for state in states:
                found=tuple(next(
                     source_color for source_color,s in
                     ((TYPES[original][k],PIECES[EDGE_POS[original]][k])
                       for k in range(2))
                     if state[s]==dest_slot)
                     for dest_slot in (e0,e1))
                assert found==target_pair
        checked+=len(states)
    assert checked==3072
    print("R12_ADAPTIVE_EIGHT_COMPLETE_EDGE_PREFIX_OBSTRUCTION_PASS",
          "hard_types","UR/UF/UL/UB","residual_minimax",5,
          "parity_classes",4,"constructed_legal_states",checked,
          "sample_feedback_prefixes",32)
    print("R12_LIMIT all 16-read eight-complete-edge prefixes only;",
          "20-frame mixed-prefix global optimum still OPEN")

if __name__=="__main__":
    audit()
