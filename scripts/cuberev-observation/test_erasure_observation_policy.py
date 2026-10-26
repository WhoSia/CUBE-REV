#!/usr/bin/env python3
"""Small tests for exact source-row V4 and observable erasure stopping."""
import itertools,unittest
from global_dual_obligations import row_orbits,sensor_source_group,transport
from erasure_observation_policy import trace_stop
from physical_edges import ACTIONS,edge_transitions
from robust_observation import signatures
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]
class Court(unittest.TestCase):
    def test_source_orbit_partition(self):
        orbits=row_orbits()
        universe=set().union(*(set(o) for o in orbits))
        self.assertEqual(len(universe),715)
        self.assertEqual(sum(len(o) for o in orbits),715)
        self.assertTrue(set(len(o) for o in orbits)<={1,2,4})
    def test_actual_receiver_never_guesses_wrong(self):
        words=json.loads((ROOT/"docs/observation-generalization/L7_ERASURE1_5_WORD_COVER.json").read_text())["words"]
        moves=edge_transitions()
        histories=[signatures(moves,tuple(ACTIONS.index(a) for a in word)) for word in words]
        for group in itertools.combinations(range(12),3):
            for h in histories:
                if all((h[a]^h[b]).bit_count()>=2 for a,b in itertools.combinations(group,2)):
                    for true in group:
                        for erased in [None,0,3,6]:
                            depth=trace_stop(h,group,true,erased)
                            self.assertTrue(1<=depth<=7)
                    break
            else:self.fail("source triple has no correcting 5-word experiment")
if __name__=="__main__":unittest.main()
