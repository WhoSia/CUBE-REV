#!/usr/bin/env python3
"""CUBE-REV B6 exact erasure threshold, provenance-separated regressions."""
import unittest
from itertools import combinations
from verify_b6_one_erasure_exact19 import (
    certified_physical_corner_pairs, certified_physical_B7_adjacent_edge_pairs,
    physically_replayed_all_B5_three_edge_supports,
    obstruction_lower_bound, audit
)
from audit_b6_one_erasure_robustness import (
    TAGS, CORNERS_TAGS, EDGES_TAGS, positive_missing_four,
    all_erasures_have_16_core,
)

class ExactNineteenTests(unittest.TestCase):
    def test_independent_48_sticker_physical_corner_pair_orbits(self):
        pairs=certified_physical_corner_pairs()
        self.assertEqual(len(pairs),16)
        self.assertEqual(len(set().union(*pairs)),8)
        self.assertEqual(sorted(sum(a!=b for a,b in zip(*p)) for p in pairs),
                         [2]*12+[3]*4)

    def test_B7_13HTM_adjacent_edge_midpoint_orbit(self):
        pairs=certified_physical_B7_adjacent_edge_pairs()
        self.assertEqual(len(pairs),24)
        self.assertEqual(len(set().union(*pairs)),12)

    def test_B5_three_edge_coverage_physically_replayed_220(self):
        family=physically_replayed_all_B5_three_edge_supports()
        self.assertEqual(len(family),220)
        self.assertTrue(all(frozenset(p) in family
                            for p in combinations(EDGES_TAGS,3)))

    def test_lower_bound(self):
        self.assertEqual(obstruction_lower_bound(),19)

    def test_twelve_constructive_nineteen_layouts(self):
        positive=positive_missing_four()
        self.assertEqual(len(positive),156)
        for absent in EDGES_TAGS:
            self.assertTrue(all_erasures_have_16_core(TAGS-{absent},positive))

    def test_exact_nineteen_and_completeness(self):
        self.assertEqual(audit(),(19,12))

if __name__=="__main__":
    unittest.main()
