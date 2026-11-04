#!/usr/bin/env python3
"""Regression for exact P48 B4 fixed-slot and 2856-base decomposition."""
import unittest
from audit_active_p48_b4_nonadaptive_horizon import audit as horizon
from audit_active_p48_b4_corner_freedom import audit as corners

class B4PhysicalObservationTests(unittest.TestCase):
    def test_full_b4_eight_frame_horizon(self):
        r=horizon()
        self.assertEqual((r["states"],r["eight_valid"]),(46741,102))

    def test_102_times_28_corner_freedom(self):
        h=corners()
        self.assertEqual(h[28],102)
        self.assertEqual(h[0],12)

if __name__=="__main__":
    unittest.main()
