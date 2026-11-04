#!/usr/bin/env python3
"""B4 complete adaptive five-frame physical replay regression."""
import unittest
from certify_active_p48_b4_five_frame_upper import build

class ActiveB4FiveFrameTests(unittest.TestCase):
    def test_complete_physical_five_frame_policy(self):
        receipt=build()
        self.assertEqual(receipt["states"],46741)
        self.assertEqual(receipt["adaptive_upper"],5)
        self.assertEqual(sum(receipt["depth_histogram"].values()),46741)
        self.assertEqual(receipt["depth_histogram"][5],92)

if __name__=="__main__":unittest.main()
