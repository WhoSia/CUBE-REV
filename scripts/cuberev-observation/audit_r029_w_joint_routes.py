#!/usr/bin/env python3
"""Independent face-turn/pose audit for the 576 paired probe routes in Lean.

Checks the fixed 48-sticker geometry rather than using the Lean checker.
The general pose and arbitrary-probe tests are randomized checks of the
compositional laws; the base 576 routes are exhaustively checked.
"""
import ast
import json
from pathlib import Path
from random import Random
from audit_r029_w_corner_geometric_decoder import geometry

HERE = Path(__file__).resolve()
ROOT = next(root for root in (HERE.parents[1], HERE.parents[2]) if (root/'formal/029/ProbeRouteWords.lean').exists())


def table():
    source=(ROOT/'formal/029/ProbeRouteWords.lean').read_text()
    text=source.split('def jointProbeTable : Array (List Turn) := #[',1)[1].split('\n]\n',1)[0]
    values=ast.literal_eval('['+text+']')
    assert len(values)==576
    assert all(all(0<=x<12 for x in w) for w in values)
    return values


def follow(moves,path,slot):
    for t in path:
        slot=moves[t][slot]
    return slot


def inverse(path):
    return tuple(x^1 for x in reversed(path))


def composed_path(routes,probe_edge,probe_corner,target_edge,target_corner,previous):
    return tuple(inverse(routes[24*probe_edge+probe_corner])+tuple(routes[24*target_edge+target_corner])+inverse(previous))


def test():
    moves=geometry()
    paths=table()
    for e in range(24):
        for c in range(24):
            path=paths[24*e+c]
            assert follow(moves,path,0)==e,(e,c,'edge')
            assert follow(moves,path,24)==24+c,(e,c,'corner')
    random=Random(20261121)
    for i in range(4000):
        pe=random.randrange(24);pc=random.randrange(24)
        te=random.randrange(24);tc=random.randrange(24)
        prior=tuple(random.randrange(12) for _ in range(random.randrange(0,18)))
        step=composed_path(paths,pe,pc,te,tc,prior)
        assert follow(moves,prior,follow(moves,step,pe))==te
        assert follow(moves,prior,follow(moves,step,24+pc))==24+tc
    return {'status':'PASS','checked_base_routes':576,'random_prior_pose_tests':4000,
            'result':'both fixed sector probes pull back to arbitrary requested initial stickers',
            'scope':'finite geometric regression; universal Lean proof is JointProbeRouting.lean'}

if __name__=='__main__':
    print(json.dumps(test(),indent=2))
