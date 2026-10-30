#!/usr/bin/env python3
"""Regression of mathematical claims with the exact full-54 facelet model."""
import unittest
from fullcube_sensor_goal_theorem import audit as sensor_audit
from fullcube_goal_pattern_databases import build_pattern_database

class PhysicalGoalMathTests(unittest.TestCase):
    def test_exact_three_sensor_minimum(self):
        r=sensor_audit()
        self.assertEqual(r["minimum_sensors_for_all_eighteen_single_turn_states"],3)
        self.assertEqual(len(r["all_eight_minimal_face_cover_sensor_sets"]),8)
        self.assertEqual(r["sensor_count_to_impossible_pair_count_frequency"]["2"],
                         {"15":30,"36":36})
    def test_admissible_pattern_distance(self):
        for tags,size,diam in [((0,),24,3),((0,5),528,5),((0,5,10),10560,7)]:
            p=build_pattern_database(tags)
            self.assertEqual(len(p),size)
            self.assertEqual(max(p.values()),diam)
if __name__=="__main__":unittest.main()
