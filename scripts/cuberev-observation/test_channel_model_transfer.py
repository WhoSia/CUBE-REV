#!/usr/bin/env python3
"""Channel-model semantic tests: error correction versus known erasures."""
import unittest
from channel_model_transfer import distinguishes_pair,audit,ROOT

class ChannelModelTransferTests(unittest.TestCase):
    def test_substitution_vs_one_erasure(self):
        # Two differences permit one known erasure but not one unknown flip.
        x=0b0000000;y=0b0000011
        self.assertFalse(distinguishes_pair(x,y,7,"substitution1"))
        self.assertTrue(distinguishes_pair(x,y,7,"erasure1"))

    def test_consecutive_erasure_is_not_arbitrary_two_erasure(self):
        # Differences at ends survive every contiguous erased pair.
        self.assertTrue(distinguishes_pair(0,0b1000001,7,"burst_erasure2"))
        # Both differences inside a length-two window: ambiguity.
        self.assertFalse(distinguishes_pair(0,0b0000110,7,"burst_erasure2"))

    def test_existing_11_word_dictionary(self):
        d=audit(ROOT/"docs/observation-generalization/L7_ROBUST_11_WORD_COVER.json")
        self.assertEqual(d["dictionary_size"],11)
        self.assertTrue(d["models"]["substitution1"]["full_cover"])
        self.assertTrue(d["models"]["erasure1"]["full_cover"])
        self.assertGreaterEqual(d["models"]["erasure1"]["total_covered"],
                                d["models"]["substitution1"]["total_covered"])

if __name__=="__main__":
    unittest.main()
