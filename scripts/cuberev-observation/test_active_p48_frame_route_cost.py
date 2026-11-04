#!/usr/bin/env python3
"""Adversarial exact HTM route cost for B6/full-group fixed physical readouts."""
import unittest
from b6_independent_48sticker_goals import word,MOVES,inverse,compose
from audit_active_p48_frame_route_cost import (
    ball3_words,shortest_six,exact_route
)
from active_p48_fixed_site_scan import eleven_frame_scan
from active_p48_b6_ten_frame_bridge import ten_frame_b6_plan

class ActiveP48RouteCostTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ball=ball3_words()

    def test_exact_complete_physical_radius_three_ball(self):
        self.assertEqual(len(self.ball),3502)
        self.assertEqual(max(map(len,self.ball.values())),3)

    def test_two_turn_reductions_and_inverse_geodesic(self):
        for w in ("U U'","R2 R2","U R","F' D2 L R'","U2 L R' F"):
            physical=word(w)
            result=shortest_six(physical,self.ball)
            self.assertEqual(word(" ".join(result)),physical)
            self.assertLessEqual(len(result),len(w.split()))

    def test_full_group_eleven_frame_fixed_route(self):
        result=exact_route(eleven_frame_scan(),self.ball)
        self.assertEqual(result["n"],11)
        self.assertEqual(result["completed_pairwise_geodesics"],55)
        self.assertLessEqual(result["best_fixed_frame_sequence_cost"],
                             result["fixed_frame_sequence_cost"])
        self.assertEqual(word(" ".join(result["movement_word"])),
                         word(" ".join(eleven_frame_scan()[result["route"][-1]][2])))

    def test_b6_ten_frame_fixed_route(self):
        result=exact_route(ten_frame_b6_plan()[0],self.ball)
        self.assertEqual(result["n"],10)
        self.assertEqual(result["completed_pairwise_geodesics"],45)
        self.assertLessEqual(result["best_fixed_frame_sequence_cost"],
                             result["fixed_frame_sequence_cost"])

if __name__=="__main__":
    unittest.main()
