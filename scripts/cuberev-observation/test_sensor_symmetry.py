#!/usr/bin/env python3
"""Regression court for certified sensor-preserving cube rotation actions."""
import unittest
from sensor_symmetry import analyze, rotations,conjugacy_candidate
from physical_edges import edge_transitions

class SensorSymmetryTests(unittest.TestCase):
    def test_24_proper_rotations(self):
        r=analyze()
        self.assertEqual(r["tested_proper_cube_rotations"],24)
        self.assertEqual(len(r["certified_sensor_automorphisms"]),4)
        self.assertEqual(r["automaton_intertwining_count"],24)
        self.assertTrue(all(x["flip_readout_preserved"] and x["automaton_intertwines"]
                            for x in r["certified_sensor_automorphisms"]))

    def test_identity_sensor_symmetry(self):
        m=edge_transitions()
        identity=next(t for p,s,t in rotations()
                      if all(t(e)==e for e in ((1,0,0),(0,1,0),(0,0,1))))
        labels,alpha,T=conjugacy_candidate(identity)
        self.assertEqual(T,tuple(range(24)))
        self.assertEqual(alpha,tuple(range(18)))
        self.assertTrue(all(T[m[a][s]]==m[alpha[a]][T[s]]
                            for a in range(18) for s in range(24)))

    def test_readout_is_not_rotation_invariant_in_general(self):
        r=analyze()
        self.assertTrue(any(not x["flip_readout_preserved"]
                            for x in r["rejected_sensor_automorphisms"]))

if __name__=="__main__":
    unittest.main()
