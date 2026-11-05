#!/usr/bin/env python3
"""Exact legal-cube P48 21-frame color reconstruction regression tests."""
import unittest
from b6_independent_48sticker_goals import EDGE_POS,CORNERS,word,factor_value
from construct_color_p48_21_frame_legality_scan import (
    plan21,recover21,audit,permutation_parity
)

class P48TwentyOneColorFrames(unittest.TestCase):
    def test_21_facelet_pairs_are_real_joint_position_orbit_queries(self):
        schedule=plan21()
        self.assertEqual(len(schedule[0]),21)
        self.assertEqual(len({e for e,c,w in schedule[0]}),21)
        self.assertEqual(len({c for e,c,w in schedule[0]}),21)

    def test_cube_parity_and_corner_twist_invariants_under_face_moves(self):
        from b6_independent_48sticker_goals import SLOTS,PIECES
        for seq in ("","U","R","F","D'","B2","L' U2 F R B D'"):
            physical=word(seq)
            self.assertEqual(sum(factor_value(p,physical)%2 for p in EDGE_POS)%2,0)
            self.assertEqual(sum(factor_value(p,physical)%3 for p in CORNERS)%3,0)
            def parity(labels):
                pos={p:i for i,p in enumerate(labels)}
                dest=[pos[next(iter({SLOTS[physical[j]][0] for j in PIECES[p]}))]
                      for p in labels]
                return permutation_parity(dest)
            self.assertEqual(parity(EDGE_POS),parity(CORNERS))

    def test_actual_full_color_reconstruction_without_ideal_labels(self):
        plan=plan21()
        for seq in ("","F' R U2 D L B2","L F R' F' L' U2 R U R U' R2 U2 R"):
            state=word(seq)
            self.assertEqual(recover21(state,plan),tuple(state))

    def test_complete_b2_all_262_states(self):
        result=audit()
        self.assertEqual(result["frames"],21)
        self.assertEqual(result["B2_replays"],262)

if __name__=="__main__":
    unittest.main()
