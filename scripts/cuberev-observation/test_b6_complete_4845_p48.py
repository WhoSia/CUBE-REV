#!/usr/bin/env python3
"""P48 full 4,845-layout classification and fault-injection regression."""
import unittest
from unittest.mock import patch
from verify_b6_complete_4845_p48 import (
    audit, triple_edge_obstructions, two_corner_obstructions,
    adjacent_b5_obstructions, adjacent_b6_obstructions, B5_FOUR_SEEDS
)

class CompleteB6P48Tests(unittest.TestCase):
    def test_all_4845_subsets_have_exclusive_certificate(self):
        grades, survivors=audit()
        self.assertEqual(len(survivors),156)
        self.assertEqual(sum(grades.values()),4689)
        self.assertEqual(grades["missing_3plus_edges"],2255)
        self.assertEqual(grades["nonadjacent_missing_corners"],1798)
        self.assertEqual(grades["B5_adjacent_four"],216)
        self.assertEqual(grades["B6_adjacent_four"],420)

    def test_physical_support_families_are_actual_word_replays(self):
        self.assertEqual(len(triple_edge_obstructions()),220)
        self.assertEqual(len(two_corner_obstructions()),16)
        self.assertEqual(len(adjacent_b5_obstructions()),216)
        self.assertEqual(len(adjacent_b6_obstructions()),420)

    def test_tampered_b5_word_does_not_pass(self):
        broken=list(B5_FOUR_SEEDS)
        pair,a,b=broken[0]
        broken[0]=(pair,a,b+" U")
        with patch("verify_b6_complete_4845_p48.B5_FOUR_SEEDS",tuple(broken)):
            with self.assertRaises(AssertionError):
                adjacent_b5_obstructions()

    def test_truncated_b5_witness_manifest_does_not_pass(self):
        with patch("verify_b6_complete_4845_p48.B5_FOUR_SEEDS",B5_FOUR_SEEDS[:8]):
            with self.assertRaises(AssertionError):
                adjacent_b5_obstructions()

if __name__=="__main__":
    unittest.main()
