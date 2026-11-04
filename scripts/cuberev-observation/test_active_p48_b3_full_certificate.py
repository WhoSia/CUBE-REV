#!/usr/bin/env python3
"""B3 exact adaptive four-vs-six physical certificate adversarial regressions."""
import copy
import unittest
from certify_active_p48_b3_adaptive_gap import payload,verify

class ActiveB3FullDecisionCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt=payload()

    def test_full_adaptive_four_tree_and_nonadaptive_five_exclusion(self):
        hist=verify(self.receipt)
        self.assertEqual(sum(hist.values()),3502)
        self.assertLessEqual(max(hist),4)

    def test_reject_corrupt_state_universe_hash(self):
        candidate=copy.deepcopy(self.receipt)
        candidate["states_sha256"]="0"*64
        with self.assertRaisesRegex(AssertionError,"physical state universe"):
            verify(candidate)

    def test_reject_missing_first_query_branch(self):
        candidate=copy.deepcopy(self.receipt)
        branches=candidate["adaptive_tree"]["branches"]
        branches.pop(next(iter(branches)))
        with self.assertRaisesRegex(AssertionError,"missing/forged branch"):
            verify(candidate)

    def test_reject_nonphysical_root_query(self):
        candidate=copy.deepcopy(self.receipt)
        candidate["adaptive_tree"]["query"]=[99,99]
        with self.assertRaisesRegex(AssertionError,"nonphysical query"):
            verify(candidate)

    def test_reject_forged_nonadaptive_upper(self):
        candidate=copy.deepcopy(self.receipt)
        candidate["nonadaptive_six"]["edges"]=[0]*6
        with self.assertRaisesRegex(AssertionError,"invalid six-frame witness"):
            verify(candidate)

if __name__=="__main__":
    unittest.main()
