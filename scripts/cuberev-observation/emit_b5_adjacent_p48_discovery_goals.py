#!/usr/bin/env python3
"""Emit eleven candidate missing-edge-pair orbits for an independent B5 P48 MITM.

The 22 relative cases are a BROAD geometric candidate family; no historical
B5 positive/negative classification or previously published word pairs enter
the construction. The C++ verifier finds which groups have two B5 endpoints.
"""
from itertools import combinations,product
from pathlib import Path
import argparse
from b6_independent_48sticker_goals import (
    CORNERS,EDGE_NAMES,EDGE_POSITION,SPATIAL,target,factor_state,
)

CORE="DL"
def endpoints(e):
    m=EDGE_POSITION[e]
    return frozenset(p for p in CORNERS if all(p[i]==m[i] for i in range(3) if m[i]))

def discovery_orbits():
    near={e for e in EDGE_NAMES if e!=CORE and endpoints(e)&endpoints(CORE)}
    anti=frozenset(tuple(-v for v in p) for p in endpoints(CORE))
    star=next(e for e in EDGE_NAMES if endpoints(e)==anti)
    far={e for e in EDGE_NAMES if e!=star and endpoints(e)&anti}
    parallel={e for e in EDGE_NAMES if EDGE_POSITION[e].index(0)==EDGE_POSITION[CORE].index(0) and e not in (CORE,star)}
    assert (len(near),len(far),len(parallel))==(4,4,2)
    # 22 plausible B5 failures: 10 core spokes, 8 near-parallel, 4 near-antipodal.
    # The 8 near-parallel cases are deliberately UNSORTED BY B5 VERDICT:
    # four actually fail at B5 and four only at B6.
    candidate={frozenset((a,b)) for a,b in combinations(EDGE_NAMES,2)
        if ((CORE in (a,b) and bool((set((a,b))-{CORE})&(near|far|parallel)))
            or (a in near and b in parallel) or (b in near and a in parallel)
            or (star in (a,b) and bool((set((a,b))-{star})&near)))}
    assert len(candidate)==22
    rot=[R for determinant,p,R in SPATIAL
         if determinant==1 and R(EDGE_POSITION[CORE])==EDGE_POSITION[CORE]]
    assert len(rot)==2
    edge_at={position:e for e,position in EDGE_POSITION.items()}
    remaining=set(candidate)
    representatives=[]
    while remaining:
        pair=min(remaining,key=lambda s:tuple(sorted(s)))
        orbit={frozenset(edge_at[R(EDGE_POSITION[e])] for e in pair) for R in rot}
        assert len(orbit)==2 and orbit<=remaining
        remaining-=orbit
        representatives.append(tuple(sorted(pair)))
    assert len(representatives)==11
    return tuple(representatives)

def emit(folder):
    folder=Path(folder)
    folder.mkdir(parents=True,exist_ok=True)
    reps=discovery_orbits()
    lines=[]
    for idx,pair in enumerate(reps):
        for sw,tw,fl in product(range(2),range(3),range(2)):
            if (sw,tw,fl)==(0,0,0):continue
            cube=target(CORE,pair,sw,tw,fl)
            lines.append(" ".join(map(str,[idx]+list(factor_state(cube)))))
    assert len(lines)==121
    (folder/"b5_adjacent_candidate_goals121.txt").write_text("\n".join(lines)+"\n",encoding="utf8")
    (folder/"b5_adjacent_candidate_orbits11.txt").write_text("\n".join(",".join(x) for x in reps)+"\n",encoding="utf8")
    print("P48_B5_CANDIDATES_PASS 22 omissions = 11 proper stabilizer orbits, 121 legal target rows")
    print("REPS",reps)
    return reps

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("output_directory")
    emit(p.parse_args().output_directory)
