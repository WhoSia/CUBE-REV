#!/usr/bin/env python3
"""Small restricted-LP physical pricing correctness tests."""
import unittest
from dual_priced_columns import price
from physical_edges import ACTIONS,edge_transitions
from orbit_column_generation import signature_cover

class DualPricingTests(unittest.TestCase):
    def test_priced_words_are_real_physical_experiments(self):
        result=price(mutations=20,top=10,proposals=80,keep=8)
        self.assertEqual(result["scope"],"FINITE_PHYSICAL_CANDIDATE_POOL")
        self.assertFalse(result["global_lower_bound_proven"])
        moves=edge_transitions()
        for entry in result["top_priced_words"]:
            self.assertGreater(entry["dual_weight"],1.0)
            word=tuple(ACTIONS.index(a) for a in entry["actions"])
            self.assertEqual(len(word),7)
            self.assertNotEqual(signature_cover(moves,word),0)

if __name__=="__main__":
    unittest.main()
