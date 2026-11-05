#!/usr/bin/env python3
"""R11/R12: adversarial completion defeats EVERY 16-full-edge-prefix strategy.

The scope is intentionally a NARROW but important policy class:
the first 16 edge-sensor frames observe both individual facelets of exactly
8 distinct original spatial edge positions (order and selected positions
may depend on all preceding edge and corner colors). The other four spatial
edge positions are not read in that prefix.

Adversary fixes the true corners as solved. Choose any of the 54 physical
four-edge COLOR-TYPE sets L for which the exact R8/R9 minimax residual depth
is five, even with the full corner oracle and free arbitrary slot access.
Whenever a policy encounters a NEW edge position, an unused edge type
from the complement of L is assigned to it, with orientation zero.
After eight such fully observed positions, all of L remain unobserved.
Complete the four remaining edge assignments with the permutation parity
matching the fixed corners, and flips of even parity. The same prefix
history is then compatible with all 96 parity-conditioned residual states,
requiring FIVE additional edge color queries in the worst case.

Thus NO policy in this 16-complete-cubies-first structural class identifies
the FULL legal cube in 20 color frames. It says NOTHING about policies
which partially visit more than eight edge positions during first 16 reads.
The mathematical online adversary proof covers arbitrary such policies;
the execution samples varied deterministic selectors as regression tests.
"""
from itertools import combinations
from b6_independent_48sticker_goals import (
    EDGE_POS,CORNERS,PIECES,SLOTS,factor_value,inverse,
)
from construct_color_p48_24_frame_scanner import SOURCE_FACE_COLOR
from audit_r8_four_edge_adaptive_subproblems import TYPES,graph_shape,states_for,minimax_depth

def inversion(order):
    return sum(order[i]>order[j] for i in range(len(order))
               for j in range(i+1,len(order)))%2

def construct_adversarial_state(leftover,selector,salt):
    unused_labels=[i for i in range(12) if i not in leftover]
    destinations={}
    transcript=[]
    for step in range(8):
        unvisited=[i for i in range(12) if i not in destinations]
        target=selector(tuple(transcript),tuple(unvisited),salt)
        assert target in unvisited
        # Any adaptive location choice can be answered by a different,
        # previously unused label from the complement of the bad set.
        source=unused_labels[step]
        destinations[target]=source
        transcript.append((target,TYPES[source]))

    final_positions=tuple(i for i in range(12) if i not in destinations)
    assert len(final_positions)==4
    remaining=list(leftover)
    for dest,src in zip(final_positions,remaining):
        destinations[dest]=src
    source_order=[destinations[i] for i in range(12)]
    if inversion(source_order):
        a,b=final_positions[:2]
        destinations[a],destinations[b]=destinations[b],destinations[a]
    source_order=[destinations[i] for i in range(12)]
    assert inversion(source_order)==0
    # A full original-sticker-to-spatial-slot P48 state, with corners solved.
    g=list(range(48))
    for dest_i,src_i in destinations.items():
        for k,sticker in enumerate(PIECES[EDGE_POS[src_i]]):
            g[sticker]=PIECES[EDGE_POS[dest_i]][k]
    state=bytes(g)
    assert len(set(state))==48
    assert all(state[s]==s for p in CORNERS for s in PIECES[p])
    assert sum(factor_value(p,state)%2 for p in EDGE_POS)%2==0
    inv=inverse(state)
    for dest_i,read in transcript:
        actual=tuple(SOURCE_FACE_COLOR[inv[s]]
                     for s in PIECES[EDGE_POS[dest_i]])
        assert actual==tuple(read)
    for dest_i in final_positions:
        assert destinations[dest_i] in leftover
    # Fix the exactly same 16 color outcomes at the eight read positions.
    # There are 96 legal residual arrangements under solved corner parity.
    label_tuple=tuple(sorted(leftover))
    base=[destinations[i] for i in range(12)]
    for position,src in zip(final_positions,label_tuple):
        base[position]=src
    needed_parity=inversion(base)
    assert len(states_for(label_tuple,needed_parity,0))==96
    assert minimax_depth(label_tuple,needed_parity,0)==5
    return state,transcript,final_positions

def fixed_selector(history,available,salt):
    return available[0]

def reverse_selector(history,available,salt):
    return available[-1]

def feedback_selector(history,available,salt):
    h=sum(ord(c) for dest,colors in history for c in colors)
    return available[(salt+3*h+len(history))%len(available)]

def audit():
    graph_cases={}
    for leftover in combinations(range(12),4):
        deg,components=graph_shape(leftover)
        if deg==(4,1,1,1,1):
            graph_cases.setdefault("star",leftover)
        if deg==(3,2,2,1):
            graph_cases.setdefault("triangle_pendant",leftover)
        if len(graph_cases)==2:break
    assert len(graph_cases)==2
    test_count=0
    for name,leftover in graph_cases.items():
        for selector in (fixed_selector,reverse_selector,feedback_selector):
            for salt in range(16):
                g,h,unseen=construct_adversarial_state(leftover,selector,salt)
                assert len(h)==8 and len(unseen)==4
                test_count+=1
        print("R12_ADVERSARIAL_OBSTRUCTION_CLASS_PASS",
              "shape",name,"leftover_sources","/".join(
                  "".join(TYPES[i]) for i in leftover))
    assert test_count==96
    print("R12_FULL_EDGE_PREFIX_NO20_THEOREM_WITNESS_PASS",
          "physical_complete_states",test_count,
          "bad_graph_classes",2,"residual_minimax_depth",5)
    print("R12_SCOPE 16 readings are EXACTLY 8 complete spatial edge positions;"
          " mixed/partial-prefix universal 20-frame question remains OPEN")

def audit_r14_seven_complete_prefix_gate():
    """Strengthen R12: adaptive selection of SEVEN complete positions in 14 reads.

    At each newly encountered spatial edge position during the first 14
    reads, an online adversary assigns one unused edge type from the
    complement of {UR,UF,UL,UB,FR}.  Since all first-14 readings cover
    exactly 7 complete positions, the complementary 5 types remain entirely
    unread regardless of adaptive position order.  The *existing* R11
    exact 960-state 5-edge minimax shows that 6 further reads are never
    universally enough, even with free corner state and free slot access.

    This does not cover partial/mixed prefixes before the 14th reading.
    """
    from audit_r11_five_edge_20frame_gate import positions, make_states, solver
    hard = positions(("UR", "UF", "UL", "UB", "FR"))
    complement = tuple(i for i in range(12) if i not in hard)
    assert len(hard) == 5 and len(complement) == 7
    counts=[]
    for pp in (0,1):
        for fp in (0,1):
            states=make_states(hard,pp,fp)
            query,outcomes=solver(states)
            no_six=query((1<<960)-1,6)==-2
            assert no_six,(pp,fp)
            # R11 also provides a precommitted seven-slot distinguishing
            # witness: read 2+2+2+1 remaining facelets.
            slots=(0,1,2,3,4,5,6)
            assert len({tuple(s[i] for i in slots) for s in states})==960
            counts.append((pp,fp,len(states),query.cache_info().currsize))
    assert len(counts)==4
    print("R14_ADAPTIVE_SEVEN_COMPLETE_PREFIX_NO20_PASS",
          "observed_initial_complete=7", "observations_prefix=14",
          "forced_remaining_labels=UR/UF/UL/UB/FR",
          "residual_legal_states_per_parity=960",
          "residual_minimax=7","parity_cases=4")
    print("R14_SCOPE any seven-complete first14 prefix, including"
          " adaptive choice/order; mixed/partially observed prefixes OPEN")
    return counts

if __name__=="__main__":
    audit()
    audit_r14_seven_complete_prefix_gate()
