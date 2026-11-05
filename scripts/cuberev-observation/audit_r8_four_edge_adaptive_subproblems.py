#!/usr/bin/env python3
"""R8: exact 4-unknown-edge adaptive decisions after 8 complete edge reads.

The initial 16 facelet queries fully determine eight original edge cubies.
The other four edge TYPES, the required permutation parity, and the required
total flip parity are then known (complete true corners granted as oracle).

For each of all 495 possible sets of four remaining ORIGINAL edge types and
all four parity combinations, enumerate every one of the 96 legal relative
edge arrangements, and solve the exact worst-case adaptive decision tree
over eight original spatial facelet query positions. Arbitrary access to
those eight facelets is granted: not an HTM route-cost experiment.

A 5-read continuation always exists (two full edges + one partial; permutation
parity then determines last two labels, and flip parity last orientation).
This study does not claim any 20-frame full-cube policy or human behavior.
"""
from functools import lru_cache
from itertools import combinations, permutations, product
from collections import Counter
from b6_independent_48sticker_goals import EDGE_POS, PIECES, SLOTS, FACES

FACES_INV={v:k for k,v in FACES.items()}
TYPES=tuple(tuple(FACES_INV[SLOTS[j][1]] for j in PIECES[p])
            for p in EDGE_POS)
assert len(TYPES)==len(set(map(frozenset,TYPES)))==12
SIX=tuple(FACES)

def inversion_parity(p):
    return sum(p[i]>p[j] for i in range(len(p))
               for j in range(i+1,len(p)))%2

def states_for(remaining, permutation_parity, flip_parity):
    candidates=[]
    for perm in permutations(range(4)):
        if inversion_parity(perm)!=permutation_parity:continue
        for flip in product(range(2),repeat=4):
            if sum(flip)%2!=flip_parity:continue
            candidates.append(tuple(TYPES[remaining[perm[pos]]][(side+flip[pos])%2]
                                    for pos in range(4) for side in range(2)))
    assert len(candidates)==len(set(candidates))==96
    return candidates

def minimax_depth(remaining, permutation_parity, flip_parity):
    states=states_for(remaining,permutation_parity,flip_parity)
    outcomes=[]
    for slot in range(8):
        outcomes.append(tuple(sum(1<<i for i,s in enumerate(states)
                                  if s[slot]==color) for color in SIX))
    whole=(1<<96)-1
    @lru_cache(None)
    def can(mask,depth):
        if mask.bit_count()==1:return True
        if depth==0:return False
        for responses in outcomes:
            parts=tuple(mask&v for v in responses if mask&v)
            if len(parts)<2:continue
            if depth==1:
                if all(p.bit_count()==1 for p in parts):return True
            elif all(can(p,depth-1) for p in parts):
                return True
        return False
    # Two observations have at most 6^2=36 outcomes <96 states.
    if can(whole,3):return 3
    if can(whole,4):return 4
    return 5

def graph_shape(remaining):
    edges=[TYPES[j] for j in remaining]
    counts=Counter(c for e in edges for c in e)
    degrees=tuple(sorted(counts.values(),reverse=True))
    adjacency={c:set() for c in counts}
    for a,b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    unseen=set(adjacency)
    comps=[]
    while unseen:
        seed=unseen.pop()
        stack=[seed];size=1
        while stack:
            v=stack.pop()
            for w in adjacency[v]&unseen:
                unseen.remove(w);size+=1;stack.append(w)
        comps.append(size)
    return degrees,tuple(sorted(comps,reverse=True))

def predicted_depth(shape):
    degree,components=shape
    if degree in ((4,1,1,1,1),(3,2,2,1)):return 5
    if degree==(2,2,1,1,1,1) and components==(4,2):return 3
    return 4

def audit():
    aggregate=Counter()
    by_shape=Counter()
    examples={}
    parity_checks=0
    for remaining in combinations(range(12),4):
        shape=graph_shape(remaining)
        observed=[]
        for perm_parity in (0,1):
            for flip_parity in (0,1):
                result=minimax_depth(remaining,perm_parity,flip_parity)
                observed.append(result)
                parity_checks+=1
        assert len(set(observed))==1,(remaining,observed)
        depth=observed[0]
        assert depth==predicted_depth(shape),(remaining,shape,depth)
        aggregate[depth]+=1
        by_shape[(shape[0],shape[1],depth)]+=1
        examples.setdefault(depth,remaining)
    assert aggregate=={3:72,4:369,5:54},aggregate
    assert parity_checks==1980
    assert sum(by_shape.values())==495
    assert sum(n for (degree,components,depth),n in by_shape.items() if depth==5)==54
    budget_numerator=sum(depth*count for depth,count in aggregate.items())
    assert budget_numerator==1962
    print("R8_FOUR_EDGE_ADAPTIVE_MINIMAX_PASS",
          "subsets=495","parity_cases=1980",
          "depth3=72","depth4=369","depth5=54")
    for (degree,components,depth),num in sorted(by_shape.items()):
        print("R8_GRAPH_CLASS",degree,components,
              "depth",depth,"subsets",num)
    print("R8_STAGED_ORACLE_EDGE_POLICY_PASS",
          "prefix=16","residual_max=5","total_worst=21",
          "mean_budget_numerator=1962","denominator=495")
    print("R8_BOUNDARY 54 four-edge color graphs obstruct the 16+4 staged strategy;",
          "global full-cube adaptive horizon remains 18..21")
    return aggregate

if __name__=="__main__":
    audit()
