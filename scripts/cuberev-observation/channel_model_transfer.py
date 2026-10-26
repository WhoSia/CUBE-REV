#!/usr/bin/env python3
"""Physical observation dictionaries under explicitly different channel models.

This is a comparative benchmark, NOT a claim that erasure/burst-error
distinguishing experiments or coding bounds are new. The source family
consists of all 3- and 4-element subsets of twelve edge starts. Exactly
one experiment in a dictionary must distinguish all sources in each set.

Noise models:
  substitution1: <=1 arbitrary flipped bit, pair distance >=3.
  erasure1: <=1 known-position erased bit, pair distance >=2.
  burst_erasure2: any <=2 consecutive erased positions are known; for
                  each pair at least one unequal position survives each
                  possible two-position consecutive erasure window.
"""
from __future__ import annotations
import itertools,json,argparse
from pathlib import Path
from physical_edges import ACTIONS,edge_transitions
from robust_observation import signatures

ROOT=Path(__file__).resolve().parents[2]
MODELS=("substitution1","erasure1","burst_erasure2")
SOURCE_TUPLES=[tuple(s) for r in (3,4) for s in itertools.combinations(range(12),r)]
ALL_SOURCE_MASKS=[sum(1<<s for s in group) for group in SOURCE_TUPLES]

def distinguishes_pair(a:int,b:int,length:int,model:str)->bool:
    d=a^b
    if model=="substitution1":return d.bit_count()>=3
    if model=="erasure1":return d.bit_count()>=2
    if model=="burst_erasure2":
        return all(d & ~((3<<k)&((1<<length)-1))
                   for k in range(length-1))
    raise ValueError(model)

def word_coverage(moves,word,model):
    sig=signatures(moves,tuple(ACTIONS.index(a) for a in word))
    n=len(word)
    good={(a,b) for a,b in itertools.combinations(range(12),2)
          if distinguishes_pair(sig[a],sig[b],n,model)}
    return {mask for mask,grp in zip(ALL_SOURCE_MASKS,SOURCE_TUPLES)
            if all(p in good for p in itertools.combinations(grp,2))}

def audit(path:Path):
    data=json.loads(path.read_text(encoding="utf8"))
    words=data["words"]
    assert len({tuple(w) for w in words})==len(words)
    moves=edge_transitions()
    report={"source_certificate":path.name,"dictionary_size":len(words),
            "length":7,"family_size":len(SOURCE_TUPLES),
            "models":{},"scope":"fixed pre-existing physical dictionary"}
    for model in MODELS:
        coverage=[word_coverage(moves,w,model) for w in words]
        union=set().union(*coverage)
        by_size={str(r):sum(m.bit_count()==r for m in union) for r in (3,4)}
        report["models"][model]={"covered_by_size":by_size,
           "total_covered":len(union),"full_cover":len(union)==len(ALL_SOURCE_MASKS),
           "private_sets_per_word":[len(c-set().union(
               *(coverage[j] for j in range(len(coverage)) if j!=i)))
               for i,c in enumerate(coverage)]}
    assert report["models"]["substitution1"]["full_cover"]
    assert report["models"]["erasure1"]["full_cover"]
    return report

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--certificate",type=Path,
        default=ROOT/"docs/observation-generalization/L7_ROBUST_11_WORD_COVER.json")
    args=ap.parse_args()
    print(json.dumps(audit(args.certificate),sort_keys=True,indent=2))
