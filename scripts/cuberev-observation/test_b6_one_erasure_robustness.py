#!/usr/bin/env python3
"""Regressions of one-erasure 16-positive-core certificates; not 18-tag invalidity."""
import unittest
from itertools import combinations
from audit_b6_one_erasure_robustness import (
    TAGS,CORNERS_TAGS,EDGES_TAGS,positive_missing_four,
    has_certified_16_core,all_erasures_have_16_core,audit,
)

class OneErasureCoreCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.family=positive_missing_four()

    def test_19_all_edge_omissions_certified(self):
        for missing in EDGES_TAGS:
            self.assertTrue(all_erasures_have_16_core(TAGS-{missing},self.family))

    def test_19_corner_omissions_no_16_core_not_invalidity(self):
        for missing in CORNERS_TAGS:
            self.assertFalse(all_erasures_have_16_core(TAGS-{missing},self.family))

    def test_18_no_full_16_core_coverage_only(self):
        for absent in combinations(TAGS,2):
            self.assertFalse(all_erasures_have_16_core(TAGS-set(absent),self.family))

    def test_exact_16_positive_family(self):
        for absent in combinations(TAGS,4):
            is_positive=frozenset(absent) in self.family
            self.assertEqual(is_positive,has_certified_16_core(TAGS-set(absent),self.family))

    def test_counts_and_inference_boundary(self):
        self.assertEqual(audit(),{16:0,17:0,18:0,19:12,20:1})

if __name__=="__main__":
    unittest.main()
