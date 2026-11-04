#!/usr/bin/env python3
"""Adversarial independent-P48 B6 negative-orbit reproduction tests."""
import unittest
from b6_independent_48sticker_goals import CORNERS
from verify_b6_negative_19_pairs_p48 import SEEDS, audit, physical_orbit, physical_support

class P48NegativeWitnessTests(unittest.TestCase):
    def test_all_historical_word_pairs_physically_replay_in_p48(self):
        report=audit()
        self.assertEqual(report["supports"],420)
        self.assertEqual(report["proper_orbits"],19)
        self.assertEqual(set(report["per_core"].values()),{35})

    def test_first_real_seed_is_four_original_cubies(self):
        a,b=SEEDS[0]
        self.assertEqual(len(physical_support(a,b)),4)
        self.assertGreater(len(physical_orbit(a,b)),0)

    def test_identity_pair_is_not_forged_negative_witness(self):
        with self.assertRaisesRegex(AssertionError,"four-tag"):
            physical_orbit("U R","U R")

    def test_wrong_word_changes_exact_original_tag_support(self):
        a,b=SEEDS[0]
        baseline=physical_support(a,b)
        self.assertNotEqual(physical_support(a,b+" U"),baseline)

if __name__=="__main__":
    unittest.main()
