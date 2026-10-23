#!/usr/bin/env python3
"""Reproduce the sampled L7 physical set-cover search (seed=25).

Algorithm reuse: CUBE-REV 0.18 original exact incidence/set-cover approach.
This is a reproducible heuristic candidate search, not a global proof of
optimality and not an exhaustive list of all L7 observation words.
"""
from __future__ import annotations
import itertools
import json
import random
from physical_edges import ACTIONS,edge_transitions
from robust_observation import signatures
from dictionary_coverage import SEED_WORDS

def candidate_coverage(sign):
    valid_pairs={(a,b) for a in range(12) for b in range(a+1,12)
                 if (sign[a]^sign[b]).bit_count()>=3}
    result=set()
    for r in (3,4,5):
        for group in itertools.combinations(range(12),r):
            if all(pair in valid_pairs for pair in itertools.combinations(group,2)):
                result.add(sum(1<<j for j in group))
    return result

def build(seed=25,samples=13000):
    rng=random.Random(seed)
    moves=edge_transitions()
    fixed=[tuple(ACTIONS.index(a) for a in w) for w in SEED_WORDS]
    candidates=fixed+[tuple(rng.randrange(18) for _ in range(7)) for _ in range(samples)]
    words=[];covers=[];whole=set()
    for word in candidates:
        covered=candidate_coverage(signatures(moves,word))
        if covered:
            words.append(word);covers.append(covered);whole.update(covered)
    target={sum(1<<a for a in group) for size in (3,4)
            for group in itertools.combinations(range(12),size)}
    uncovered=set(target);chosen=[]
    while uncovered:
        gain,index=max((len(cover&uncovered),i) for i,cover in enumerate(covers))
        if gain==0:break
        chosen.append(index);uncovered.difference_update(covers[index])
    return {"seed":seed,"sampled_candidates":samples,
            "nonempty_candidates":len(covers),"candidate_coverage":{
                str(size):sum(x.bit_count()==size for x in whole) for size in (3,4,5)},
            "uncovered_target_count":len(uncovered),
            "selected_words":[[ACTIONS[a] for a in words[i]] for i in chosen]}

if __name__=="__main__":
    result=build()
    print(json.dumps(result,sort_keys=True))
