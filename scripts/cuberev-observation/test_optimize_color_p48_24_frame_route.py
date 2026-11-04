#!/usr/bin/env python3
"""Adversarial and physical tests of the 24-frame 6-color action-route optimizer."""
import unittest
from b6_independent_48sticker_goals import compose,inverse,word
from optimize_color_p48_24_frame_route import (
    audit,normalized,directed_transition,
)
from construct_color_p48_24_frame_scanner import scan_plan

class ColorP48RouteOptimizationTests(unittest.TestCase):
    def test_htm_adjacent_same_face_reductions_are_exact(self):
        self.assertEqual(normalized(("R","R'")),())
        self.assertEqual(normalized(("U","U")),("U2",))
        self.assertEqual(normalized(("L2","L2")),())
        self.assertEqual(normalized(("F'","F'")),("F2",))
        self.assertEqual(normalized(("B2","B'")),("B",))

    def test_real_48_sticker_transition_not_just_cost_arithmetic(self):
        plan=scan_plan()
        for first in plan[:5]:
            for second in plan[5:10]:
                source=first[2];destination=second[2]
                delta=directed_transition(source,destination)
                self.assertEqual(word(" ".join(delta)),
                                 compose(word(" ".join(destination)),
                                         inverse(word(" ".join(source)))))

    def test_complete_optimized_b2_color_scan(self):
        result=audit()
        self.assertEqual(result["frames"],24)
        self.assertEqual(set(result["order"]),set(range(24)))
        self.assertLess(result["heuristic_htm"],result["initial_reduced_htm"])
        self.assertLessEqual(result["heuristic_htm"],169)

if __name__=="__main__":
    unittest.main()
