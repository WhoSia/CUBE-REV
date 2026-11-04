#!/usr/bin/env python3
"""Check physically replayed P48 B3 adaptive policy HTM cost distribution."""
import unittest
from audit_active_p48_b3_policy_motion_cost import profile

class ActiveB3PolicyCostTests(unittest.TestCase):
    def test_all_3502_b3_states_and_fixed_frame_costs(self):
        report=profile()
        self.assertEqual(report["states"],3502)
        self.assertEqual(sum(report["observation_histogram"].values()),3502)
        self.assertEqual(report["observation_histogram"][4],16)
        self.assertEqual(sum(report["htm_histogram"].values()),3502)
        self.assertLessEqual(report["max_htm"],24)
        self.assertGreaterEqual(report["n_distinct_physical_transitions"],4)
        self.assertGreater(report["mean_htm_denominator"],0)
        self.assertGreater(report["nonadaptive_fixed_frame_optimized_htm"],0)

if __name__=="__main__":
    unittest.main()
