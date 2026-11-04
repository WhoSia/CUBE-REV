#!/usr/bin/env python3
"""Independent regression of B6 one-erasure theorem against 156 layouts."""
import unittest
from itertools import combinations
from audit_b6_one_erasure_robustness import (
    TAGS, CORNERS_TAGS, EDGES_TAGS, positive_missing_four,
    is_radius6_valid, is_one_erasure_robust, audit,
)

class FaultToleranceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.f=positive_missing_four()

    def test_19_edge_omissions_all_robust(self):
        for missing_edge in EDGES_TAGS:
            self.assertTrue(is_one_erasure_robust(TAGS-{missing_edge}, self.f))

    def test_19_corner_omissions_all_fail(self):
        for missing_corner in CORNERS_TAGS:
            self.assertFalse(is_one_erasure_robust(TAGS-{missing_corner}, self.f))

    def test_18_none_robust(self):
        for absent in combinations(TAGS, 2):
            self.assertFalse(is_one_erasure_robust(TAGS-set(absent), self.f))

    def test_exact_16_positive_family(self):
        for missing in combinations(TAGS, 4):
            good=frozenset(missing) in self.f
            self.assertEqual(good,is_radius6_valid(TAGS-set(missing),self.f))

    def test_full_threshold(self):
        self.assertEqual(audit(),{20:1,19:12,18:0,17:0,16:0})

if __name__ == "__main__":
    unittest.main()
