#!/usr/bin/env python3
"""Full B2 and parity adversary checks for 22-frame complete-group color scan."""
import unittest
from b6_independent_48sticker_goals import (
    EDGE_POS,PIECES,word,factor_value
)
from construct_color_p48_22_frame_parity_scan import (
    plan22,reconstruction22,audit,
)

class P48TwentyTwoColorFrames(unittest.TestCase):
    def test_22_locations_are_exactly_one_full_missing_edge_and_two_corner_facelets(self):
        frames,missing_edge,missing_corner=plan22()
        self.assertEqual(len(frames),22)
        self.assertTrue(PIECES[missing_edge][0] not in {e for e,c,a in frames})
        self.assertTrue(PIECES[missing_edge][1] not in {e for e,c,a in frames})
        self.assertEqual(sum(j not in {c for e,c,a in frames}
                             for j in PIECES[missing_corner]),2)

    def test_edge_flip_even_parity_under_representative_legal_words(self):
        for seq in ("","U","R","F","D'","B2","U F R' D2 L B"):
            g=word(seq)
            self.assertEqual(sum(factor_value(p,g)%2 for p in EDGE_POS)%2,0)

    def test_reconstruction_replays_actual_p48_color_measurements(self):
        p=plan22()
        for seq in ("","R2 F' D B2 U","L F R' F' L' U2 R U R U' R2 U2 R"):
            g=word(seq)
            self.assertEqual(reconstruction22(g,p),tuple(g))

    def test_exact_all_262_b2_cube_states(self):
        r=audit()
        self.assertEqual(r["frames"],22)
        self.assertEqual(r["states_tested"],262)

if __name__=="__main__":
    unittest.main()
