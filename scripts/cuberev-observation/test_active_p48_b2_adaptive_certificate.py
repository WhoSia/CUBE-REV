#!/usr/bin/env python3
"""Adversarial receipt checks for exact B2 adaptive advantage over fixed sites."""
import copy
import unittest
from certify_active_p48_b2_adaptive_gap import payload, verify

class B2AdaptiveGapCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt=payload()

    def test_positive_adaptive_two_and_nonadaptive_three(self):
        self.assertGreater(verify(self.receipt),0)

    def test_reject_forged_state_digest(self):
        changed=copy.deepcopy(self.receipt)
        changed["state_sha256"]="0"*64
        with self.assertRaisesRegex(AssertionError,"identity/seal"):
            verify(changed)

    def test_reject_removed_nonadaptive_counterexample(self):
        changed=copy.deepcopy(self.receipt)
        changed["nonadaptive_two_frame_collision_rows"].pop()
        with self.assertRaisesRegex(AssertionError,"1848"):
            verify(changed)

    def test_reject_fabricated_state_collision(self):
        changed=copy.deepcopy(self.receipt)
        changed["nonadaptive_two_frame_collision_rows"][0][-2:]=[0,0]
        with self.assertRaisesRegex(AssertionError,"state indices"):
            verify(changed)

    def test_reject_nonphysical_adaptive_branch(self):
        changed=copy.deepcopy(self.receipt)
        first=next(iter(changed["second_pair_by_first_observation"]))
        changed["second_pair_by_first_observation"][first]=[99,99]
        with self.assertRaisesRegex(AssertionError,"nonphysical"):
            verify(changed)

if __name__=="__main__":
    unittest.main()
