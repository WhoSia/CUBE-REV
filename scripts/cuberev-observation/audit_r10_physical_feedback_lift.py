#!/usr/bin/env python3
"""R10 gate: lift R9 residual feedback branches to legal no-reset P48 turns.

For one tested representative of each R9 adaptive depth class, create all 96
LEGAL full physical Rubik states with corners solved and only four edges
permuted/flipped. First read sixteen edge facelets (eight complete edges),
then follow a per-color adaptive decision tree of depth 3/4/5. For every
selected edge facelet, choose a corner probe target and navigate via known
18-HTM turn words. Every frame is genuinely applied relative to the
current pose; no free reset, no original-cubie-ID observation.

This is a FREE-CORNER-ORACLE conditional subproblem, NOT a solution of the
full-cube 20-frame identification problem or an action-cost optimum.
"""
from functools import lru_cache
from itertools import combinations, permutations, product
from b6_independent_48sticker_goals import (
    EDGE_POS, CORNERS, PIECES, compose, inverse, word, factor_value,
)
from audit_color_probe_information_bounds import (
    EDGE_FACELET, CORNER_FACELET, two_one_facelet_colors,
)
from construct_color_p48_24_frame_scanner import (
    CORNER_STICKERS, SOURCE_FACE_COLOR, joint_sticker_orbit, inverted_token,
)
from audit_r8_four_edge_adaptive_subproblems import (
    TYPES, states_for, minimax_depth,
)
from audit_r9_feedback_fixed_separation import fixed_depth

HOME=bytes(range(48))

def even_permutations():
    return [p for p in permutations(range(4))
            if sum(p[i]>p[j] for i in range(4)
                   for j in range(i+1,4))%2==0]

def even_flips():
    return [f for f in product(range(2),repeat=4) if sum(f)%2==0]

def physical_state(remaining,permutation,flips):
    out=list(HOME)
    for dest_index,source_index in enumerate(permutation):
        dest=EDGE_POS[remaining[dest_index]]
        source=EDGE_POS[remaining[source_index]]
        for sticker_index,source_sticker in enumerate(PIECES[source]):
            out[source_sticker]=PIECES[dest][(sticker_index+flips[dest_index])%2]
    assert len(set(out))==48
    assert all(out[s]==s for c in CORNERS for s in PIECES[c])
    assert sum(factor_value(p,out)%2 for p in EDGE_POS)%2==0
    return bytes(out)

def policy_for(states,depth):
    outcome=tuple({color:sum(1<<i for i,g in enumerate(states)
                             if g[slot]==color) for color in "URFDLB"}
                  for slot in range(8))
    @lru_cache(None)
    def next_slot(mask,steps):
        if mask.bit_count()==1:return -1
        if steps==0:return -2
        for slot in range(8):
            partitions=tuple(mask&possible for possible in outcome[slot].values()
                             if mask&possible)
            if len(partitions)<2:continue
            if all(next_slot(part,steps-1)!=-2 for part in partitions):
                return slot
        return -2
    assert next_slot((1<<96)-1,depth)>=0
    return outcome,next_slot

def route_to(paths,edge_slot,corner_slot):
    commands=tuple(inverted_token(t) for t in
                   reversed(paths[(edge_slot,corner_slot)]))
    frame=word(" ".join(commands))
    assert frame[edge_slot]==EDGE_FACELET
    assert frame[corner_slot]==CORNER_FACELET
    return commands,frame

def audit():
    paths=joint_sticker_orbit()
    assert len(paths)==576
    exemplars={}
    for rem in combinations(range(12),4):
        dep=minimax_depth(rem,0,0)
        fix,_=fixed_depth(states_for(rem,0,0))
        if (dep,fix) in ((3,4),(4,5),(5,5)):
            exemplars.setdefault((dep,fix),rem)
        if len(exemplars)==3:break
    assert set(exemplars)=={(3,4),(4,5),(5,5)}
    readouts=0
    total_states=0
    total_turns=0
    worst_turns=0
    for (depth,fixed),remaining in sorted(exemplars.items()):
        state_colors=states_for(remaining,0,0)
        outputs,policy=policy_for(state_colors,depth)
        actual_states=[physical_state(remaining,p,f)
                       for p in even_permutations() for f in even_flips()]
        assert len(actual_states)==96
        complement=[i for i in range(12) if i not in remaining]
        prefix_edges=[slot for i in complement for slot in PIECES[EDGE_POS[i]]]
        assert len(prefix_edges)==16
        for idx,g in enumerate(actual_states):
            frame=HOME
            last_commands=()
            turns=0
            first_colors=[]
            for step,edge_slot in enumerate(prefix_edges):
                corner_slot=CORNER_STICKERS[step]
                commands,target=route_to(paths,edge_slot,corner_slot)
                delta_commands=(tuple(inverted_token(x)
                                      for x in reversed(last_commands))
                                + commands)
                delta=word(" ".join(delta_commands))
                assert delta==compose(target,inverse(frame))
                frame=compose(delta,frame)
                assert frame==target
                color_e,color_c=two_one_facelet_colors(g,frame)
                assert color_e==SOURCE_FACE_COLOR[g.index(edge_slot)]
                assert color_c==SOURCE_FACE_COLOR[g.index(corner_slot)]
                first_colors.append(color_e)
                turns+=len(delta_commands)
                last_commands=commands
                readouts+=1
            # All eight preobserved edge labels, flips are completely known.
            assert len({frozenset(first_colors[2*k:2*k+2])
                        for k in range(8)})==8
            posterior=(1<<96)-1
            steps=0
            while posterior.bit_count()>1:
                q=policy(posterior,depth-steps)
                assert 0<=q<8 and steps<depth
                edge_slot=PIECES[EDGE_POS[remaining[q//2]]][q%2]
                corner_slot=CORNER_STICKERS[(16+steps)%24]
                commands,target=route_to(paths,edge_slot,corner_slot)
                delta_commands=(tuple(inverted_token(x)
                                      for x in reversed(last_commands))
                                + commands)
                delta=word(" ".join(delta_commands))
                assert delta==compose(target,inverse(frame))
                frame=compose(delta,frame)
                assert frame==target
                edge_color,corner_color=two_one_facelet_colors(g,frame)
                assert edge_color==state_colors[idx][q],(
                    depth,idx,q,edge_color,state_colors[idx][q])
                assert corner_color==SOURCE_FACE_COLOR[g.index(corner_slot)]
                posterior&=outputs[q][edge_color]
                steps+=1
                readouts+=1
                turns+=len(delta_commands)
                last_commands=commands
            assert posterior==(1<<idx), (remaining,idx)
            total_states+=1
            total_turns+=turns
            worst_turns=max(worst_turns,turns)
        print("R10_PHYSICAL_FEEDBACK_CLASS_PASS","adaptive",depth,
              "fixed",fixed,"states",96,
              "edge_types","/".join("".join(TYPES[i]) for i in remaining))
    assert total_states==288
    assert readouts>=288*16
    print("R10_NO_RESET_P48_ORACLE_EDGE_LIFT_PASS",
          "physical_states",total_states,
          "physical_color_frames",readouts,
          "reachable_joint_probe_pairs",len(paths),
          "total_executed_htm",total_turns,
          "max_single_trial_htm",worst_turns)
    print("R10_SCOPE residual edge-only with complete corner oracle; full cube 18..21 remains OPEN")

if __name__=="__main__":
    audit()
