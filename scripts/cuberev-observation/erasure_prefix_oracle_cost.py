#!/usr/bin/env python3
"""Earliest prefix with known-single-erasure correction for each source set.

This is a post hoc source-aware oracle metric, not an implementable
online policy for unknown source states. Each cost is counted in HTM
moves, not seconds or joules, and no sensor-read cost is assumed.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
from physical_edges import ACTIONS,edge_transitions
from robust_observation import signatures
ROOT=Path(__file__).resolve().parents[2]
CERT=ROOT/"docs/observation-generalization/L7_ERASURE1_5_WORD_COVER.json"
def analyze():
    words=json.loads(CERT.read_text())["words"]
    moves=edge_transitions()
    histories=[signatures(moves,tuple(ACTIONS.index(a) for a in w)) for w in words]
    histogram={str(k):0 for k in range(1,8)}
    choices={}
    for size in (3,4):
        for subset in itertools.combinations(range(12),size):
            best=None
            for wi,h in enumerate(histories):
                for prefix in range(1,8):
                    mask=(1<<prefix)-1
                    if all(((h[a]^h[b])&mask).bit_count()>=2
                           for a,b in itertools.combinations(subset,2)):
                        candidate=(prefix,wi)
                        if best is None or candidate<best:best=candidate
                        break
            assert best is not None,subset
            histogram[str(best[0])]+=1
            choices[",".join(map(str,subset))]={"prefix":best[0],"word_index":best[1]}
    total=sum(int(k)*count for k,count in histogram.items())
    return {"status":"ERASURE_FIVE_WORD_PREFIX_ORACLE_PASS","sources":715,
            "prefix_histogram":histogram,"mean_prefix":total/715,
            "worst_prefix":max(int(k) for k,v in histogram.items() if v),
            "semantic_caveat":"SOURCE_AWARE_ORACLE_NOT_AN_ONLINE_POLICY",
            "not_actual_sensor_energy_or_wall_clock":True}
if __name__=="__main__":
    print(json.dumps(analyze(),sort_keys=True))
