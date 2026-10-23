#!/usr/bin/env python3
"""Bounded, reproducible L=7 robust observation *witness search*.

This deliberately does not label bounded search failure as UNSAT. The 54-sticker
physical_edges module supplies the physical 18x24 move permutations.
"""
from __future__ import annotations
import argparse, json, time
from physical_edges import ACTIONS, edge_transitions

def search(length: int = 7, min_distance: int = 3,
           targets: tuple[int,...] = (85,802,3208),
           max_nodes: int = 1_000_000) -> dict:
    moves=edge_transitions()
    # For each start slot maintain the actual oriented-edge state and the
    # observation history. Distances between histories are checked exactly.
    states=tuple(range(0,24,2))
    remaining=set(targets)
    witnesses={}
    expanded=0

    def visit(depth: int, state: tuple[int,...], codes: tuple[int,...],
              prefix: tuple[int,...]) -> None:
        nonlocal expanded
        if expanded>=max_nodes or not remaining: return
        expanded+=1
        # If pairwise distance cannot reach threshold even with all remaining
        # observations, this target is impossible along the current prefix.
        candidates=[]
        for mask in remaining:
            ids=[j for j in range(12) if mask>>j&1]
            pairs=[(a,b) for ix,a in enumerate(ids) for b in ids[ix+1:]]
            if all((codes[a]^codes[b]).bit_count()+(length-depth)>=min_distance
                   for a,b in pairs):
                candidates.append((mask,pairs))
        if not candidates: return
        if depth==length:
            for mask,pairs in candidates:
                if all((codes[a]^codes[b]).bit_count()>=min_distance
                       for a,b in pairs):
                    witnesses[mask]=[ACTIONS[j] for j in prefix]
            remaining.difference_update(witnesses)
            return
        for action,move in enumerate(moves):
            ns=tuple(move[s] for s in state)
            nc=tuple(c|((s&1)<<depth) for c,s in zip(codes,ns))
            visit(depth+1,ns,nc,prefix+(action,))
            if expanded>=max_nodes or not remaining: return

    visit(0, states, (0,)*12, ())
    return {"length":length,"min_distance":min_distance,
            "max_nodes":max_nodes,"visited_prefix_nodes":expanded,
            "witnesses":{str(k):v for k,v in sorted(witnesses.items())},
            "unresolved_targets":sorted(remaining),
            "status":"WITNESSES_FOUND" if not remaining else "BOUNDED_SEARCH_UNKNOWN",
            "not_an_exhaustive_unsat_certificate":True}

def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--length",type=int,default=7)
    ap.add_argument("--max-nodes",type=int,default=300_000)
    ap.add_argument("--targets",type=int,nargs="+",default=[85,802,3208])
    args=ap.parse_args()
    print(json.dumps(search(length=args.length,targets=tuple(args.targets),
                            max_nodes=args.max_nodes),sort_keys=True))
if __name__=="__main__": main()
