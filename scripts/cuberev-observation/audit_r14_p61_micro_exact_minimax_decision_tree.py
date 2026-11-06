#!/usr/bin/env python3
"""R14-P6.1 exact AND-OR minimax of a 648-state parity-coupled 3E+3C sensor court.

Standalone (no imports from CUBE-REV or P48). A policy verifier replays
all 648 hidden legal states and validates the exact worst horizon.
"""
from collections import Counter
from functools import lru_cache
from itertools import permutations,product
import json

E=('UR','UF','UL')
C=('URF','UFL','ULB')

def parity(p):
    return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2

def sector(types,mod):
    n=len(types)
    groups=[[],[]]
    for perm in permutations(range(n)):
        for prefix in product(range(mod),repeat=n-1):
            orient=prefix+((-sum(prefix))%mod,)
            word=''.join(types[perm[i]][(j+orient[i])%mod] for i in range(n) for j in range(mod))
            groups[parity(perm)].append(word)
    return groups

es=sector(E,2);cs=sector(C,3)
states=tuple((a,b) for p in (0,1) for a in es[p] for b in cs[p])
assert len(states)==648 and len(set(states))==648
queries=tuple(product(range(6),range(9)))
mask_by_q=[]
for q in queries:
    cells={}
    for i,(e,c) in enumerate(states):
        y=e[q[0]]+c[q[1]]
        cells[y]=cells.get(y,0)|(1<<i)
    assert sum(v.bit_count() for v in cells.values())==648
    mask_by_q.append(cells)
all_states=(1<<648)-1

def children(B,qi):
    return {y:B&M for y,M in mask_by_q[qi].items() if B&M}

@lru_cache(None)
def winning(B,budget):
    if B.bit_count()==1:return True
    if not budget or B.bit_count()>36**budget:return False
    for qi in range(len(queries)):
        cells=children(B,qi)
        if len(cells)<2:continue
        if max(x.bit_count() for x in cells.values())>36**(budget-1):continue
        if all(winning(x,budget-1) for x in sorted(cells.values(),key=int.bit_count,reverse=True)):
            return True
    return False

assert not winning(all_states,2)
assert not winning(all_states,3)
assert winning(all_states,4)

@lru_cache(None)
def construct(B,budget):
    if B.bit_count()==1:
        return {'end':(B.bit_length()-1)}
    assert winning(B,budget) and budget
    for qi in range(len(queries)):
        cells=children(B,qi)
        if len(cells)<2:continue
        if all(winning(x,budget-1) for x in sorted(cells.values(),key=int.bit_count,reverse=True)):
            return {'q':qi,'branches':{y:construct(x,budget-1) for y,x in sorted(cells.items())}}
    raise AssertionError('unreachable')

tree=construct(all_states,4)

def replay(state_index,node):
    s=states[state_index]
    depth=0
    while 'q' in node:
        qi=node['q'];q=queries[qi]
        y=s[0][q[0]]+s[1][q[1]]
        assert y in node['branches'],(state_index,q,y)
        node=node['branches'][y];depth+=1
    assert node['end']==state_index,(node,state_index)
    return depth

replay_depths=Counter(replay(i,tree) for i in range(648))
assert max(replay_depths)==4

# 54 independent explicit root-action obstruction witnesses for any depth-3 tree:
# whatever its root query, at least one nonempty color branch fails exact
# remaining 2-query winning predicate. Does not rely on a fixed policy.
root_obstructions=[]
for qi,q in enumerate(queries):
    hard=[(y,b.bit_count()) for y,b in sorted(children(all_states,qi).items()) if not winning(b,2)]
    assert hard,(q, 'unexpected depth-3 success')
    root_obstructions.append({'query':q,'bad_output':hard[0][0],'remaining_state_count':hard[0][1]})
assert len(root_obstructions)==54

# The certificate requires only exact bitsets of legal states and the
# completely enumerated set of 54 paired facelet queries.
def nodes(node):
    if 'end' in node:return (1,0)
    pairs=[nodes(x) for x in node['branches'].values()]
    return (1+sum(a for a,b in pairs),1+sum(b for a,b in pairs))
node_count,action_nodes=nodes(tree)
output={
    'result':'R14_P61_EXACT_648_STATE_MINIMAX_4_AND_NO3_PASS',
    'model':'3 oriented edge pieces x 3 oriented corner pieces, matched permutation sign, edge flip sum 0, corner twist sum 0',
    'legal_hidden_states':648,'allowed_paired_color_queries':54,
    'exact_worst_case_minimax_depth':4,
    'three_query_policy_impossible':True,'four_query_policy_exists':True,
    'full_state_decoder_replays':648,'replay_depth_histogram':dict(sorted(replay_depths.items())),
    'policy_nodes':node_count,'policy_action_nodes':action_nodes,
    'root_query':queries[tree['q']],
    'depth_3_root_adversary_certificate':root_obstructions,
    'complete_depth4_policy_tree':tree,
    'memoization_states':winning.cache_info().currsize,
    'scope':'separate 648-state miniature zero-error full game, not global 3x3x3 20-frame solution',
}
print(json.dumps(output,indent=2,sort_keys=True))
