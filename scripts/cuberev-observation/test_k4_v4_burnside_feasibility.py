#!/usr/bin/env python3
import unittest
from k4_v4_burnside_feasibility import audit
class K4V4OrbitTests(unittest.TestCase):
    def test_exact_action_and_source_orbits(self):
        result=audit()
        self.assertEqual(result["distinct_action_word_orbits"],153264960)
        self.assertEqual(result["source_row_orbits"],190)
        self.assertEqual(result["source_row_orbits_by_target_size"],{"3":55,"4":135})
        self.assertFalse(result["k4_global_decision_proven"])
if __name__=="__main__":
    unittest.main()
