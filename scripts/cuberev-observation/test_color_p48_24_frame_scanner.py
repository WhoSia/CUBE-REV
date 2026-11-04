#!/usr/bin/env python3
"""Real single-facelet 6-color probe geometry and reconstruction regressions."""
import unittest
from b6_independent_48sticker_goals import MOVES,word
from construct_color_p48_24_frame_scanner import (
    audit,joint_sticker_orbit,scan_plan,plan_htm_cost,
    reconstruct_from_colors,EDGE_STICKERS,CORNER_STICKERS,
)

class ColorFaceletScanTests(unittest.TestCase):
    def test_joint_sticker_orbit_all_24_by_24(self):
        o=joint_sticker_orbit()
        self.assertEqual(len(o),576)
        self.assertEqual(len(EDGE_STICKERS),24)
        self.assertEqual(len(CORNER_STICKERS),24)

    def test_known_no_reset_24_frame_action_program(self):
        plan=scan_plan()
        self.assertEqual(len(plan),24)
        self.assertEqual({e for e,c,w in plan},set(EDGE_STICKERS))
        self.assertEqual({c for e,c,w in plan},set(CORNER_STICKERS))
        self.assertGreater(plan_htm_cost(plan),0)

    def test_full_p48_reconstruction_from_48_categorical_colors(self):
        plan=scan_plan()
        for turns in ("","U","F R2 U' D L B2",
                      "L F R' F' L' U2 R U R U' R2 U2 R"):
            with self.subTest(turns=turns):
                g=word(turns)
                self.assertEqual(reconstruct_from_colors(g,plan),tuple(g))

    def test_invalid_full_state_rejected(self):
        with self.assertRaises(ValueError):
            reconstruct_from_colors(bytes(48),scan_plan())

    def test_exact_b2_all_262_replays(self):
        r=audit()
        self.assertEqual(r["joint_pairs"],576)
        self.assertEqual(r["frames"],24)
        self.assertGreater(r["constructive_no_reset_htm"],0)

if __name__=="__main__":
    unittest.main()
