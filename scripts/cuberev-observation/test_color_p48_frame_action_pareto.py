#!/usr/bin/env python3
"""Physical-regression for comparing color observation-frame and turn budgets."""
import unittest
from audit_color_p48_frame_action_pareto import audit

class ColorP48ParetoTests(unittest.TestCase):
    def test_all_three_fixed_color_scanners_execute_and_reconstruct(self):
        results=audit()
        self.assertEqual(set(results),{21,22,24})
        self.assertEqual(results[24]["reordered_HTM"],136)
        for n,r in results.items():
            self.assertLessEqual(r["reordered_HTM"],r["initial_HTM"])
            self.assertEqual(len(r["order"]),n)
            self.assertEqual(set(r["order"]),set(range(n)))

if __name__=="__main__":
    unittest.main()
