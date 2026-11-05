#!/usr/bin/env python3
"""R11: exact 960-state parity-conditioned FIVE-edge feedback obstruction.

After 14 edge-color reads at seven complete edge positions, exactly five
original edge types remain, 960 legal assignments for a given known edge
permutation parity and flip parity. Can six more edge single-facelet reads
always finish a 20-frame policy? NO for the designated physical type set.

The exact minimax solver enumerates all ten spatial initial facelets at
each color-conditional decision-tree node, not only preset schedules.
The first 14 edge slots need not be globally optimal, so this does not
rule out other full-cube 20-frame adaptive policies.

Uses independently P48-generated original sticker color pairs, compares
all four parity conditions, and replays positive policies on all 960 states.
"""
from functools import lru_cache
from itertools import permutations,product
from audit_r8_four_edge_adaptive_subproblems import TYPES
from audit_r9_feedback_fixed_separation import fixed_depth as unused_fixed_depth

FACE_COLORS="URFDLB"
assert len(TYPES)==12

def parity(arr):
    return sum(arr[i]>arr[j] for i in range(len(arr))
               for j in range(i+1,len(arr)))%2

def positions(name_parts):
    catalog={frozenset(x):i for i,x in enumerate(TYPES)}
    return tuple(catalog[frozenset(x)] for x in name_parts)

def make_states(types,pp,fp):
    result=[]
    for perm in permutations(range(5)):
        if parity(perm)!=pp:continue
        for flip in product(range(2),repeat=5):
            if sum(flip)%2!=fp:continue
            result.append(tuple(TYPES[types[perm[j]]][(k+flip[j])%2]
                                for j in range(5) for k in range(2)))
    assert len(result)==len(set(result))==960
    return result

def solver(states):
    outcomes=tuple(
        {c:sum(1<<i for i,state in enumerate(states) if state[slot]==c)
         for c in FACE_COLORS}
        for slot in range(10)
    )
    @lru_cache(None)
    def query(mask,remaining):
        if mask.bit_count()==1:return -1
        if remaining==0 or mask.bit_count()>6**remaining:return -2
        choices=[]
        for j,symbol_masks in enumerate(outcomes):
            children=tuple(mask&v for v in symbol_masks.values() if mask&v)
            if len(children)<2:continue
            worst=max(x.bit_count() for x in children)
            if worst>6**(remaining-1):continue
            choices.append((worst,j,children))
        for _,j,children in sorted(choices):
            if all(query(child,remaining-1)!=-2
                   for child in sorted(children,key=int.bit_count,reverse=True)):
                return j
        return -2
    return query,outcomes

def replay(states,tree,outcomes,depth):
    full=(1<<len(states))-1
    for i,state in enumerate(states):
        subset=full
        remaining=depth
        while subset.bit_count()>1:
            idx=tree(subset,remaining)
            assert 0<=idx<10
            subset &= outcomes[idx][state[idx]]
            remaining-=1
            assert remaining>=0
        assert subset==1<<i

def audit():
    easy=positions(("UR","UF","UL","UB","DR"))
    hard=positions(("UR","UF","UL","UB","FR"))
    seen={}
    for tag,types in (("six_possible",easy),("six_impossible",hard)):
        values=[]
        for pp in (0,1):
            for fp in (0,1):
                states=make_states(types,pp,fp)
                tree,outcomes=solver(states)
                assert tree((1<<960)-1,5)==-2
                root6=tree((1<<960)-1,6)
                possible=root6>=0
                assert possible==(tag=="six_possible"),(tag,pp,fp,root6)
                if possible:
                    replay(states,tree,outcomes,6)
                else:
                    # Known 7-read schedule: three complete edge positions
                    # + one colored facelet of the fourth. Remaining labels
                    # fixed by known permutation parity and last flip by
                    # total even flip parity.
                    fixed=(0,1,2,3,4,5,6)
                    symbols={tuple(s[i] for i in fixed) for s in states}
                    assert len(symbols)==960
                values.append(possible)
                print("R11_FIVE_EDGE_CASE",
                      tag,"pp",pp,"flip",fp,
                      "six_read_solution",possible,
                      "dp_cache_states",tree.cache_info().currsize)
        assert len(set(values))==1
        seen[tag]=values[0]
    assert seen=={"six_possible":True,"six_impossible":False}
    print("R11_FIVE_EDGE_STAGED_14_PLUS_6_OBSTRUCTION_PASS",
          "states_per_parity=960","parity_cases=8",
          "hard_min_reads=7","easy_min_reads=6")
    print("R11_BOUNDARY only the seven-complete-edge prefix is refuted;",
          "full cube 18..21 remains OPEN")

if __name__=="__main__":
    audit()
