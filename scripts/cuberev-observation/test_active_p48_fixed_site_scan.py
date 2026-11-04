#!/usr/bin/env python3
"""Regress two-probe active observability and no-go for one cubie type."""
import unittest
from b6_independent_48sticker_goals import (
    EDGE_POS, CORNERS, MOVES, factor_value, word, compose
)
from active_p48_fixed_site_scan import (
    joint_position_words, twelve_frame_scan, reconstruct,
    REF_CORNER, REF_EDGE, observe
)

CORNER_ONLY_DIFFERENCE="U2 R' B D2 B' R U2 R' B D2 B' R"
EDGE_ONLY_DIFFERENCE="L F R' F' L' U2 R U R U' R2 U2 R"

class ActiveP48ScannerTests(unittest.TestCase):
    def test_96_joint_site_positions_and_12_coverage(self):
        paths=joint_position_words()
        self.assertEqual(len(paths),96)
        self.assertLessEqual(max(map(len,paths.values())),6)
        scan=twelve_frame_scan()
        self.assertEqual(len(scan),12)
        self.assertEqual({e for e,c,w in scan},set(EDGE_POS))
        self.assertEqual({c for e,c,w in scan},set(CORNERS))

    def test_reconstruction_from_stationary_site_probes(self):
        cases=["","U R F' D2 L B'","R F R2 D U'","U2 D F2 B L' R2",
               EDGE_ONLY_DIFFERENCE,CORNER_ONLY_DIFFERENCE]
        for s in cases:
            with self.subTest(word=s):
                initial=word(s)
                result,relative_actions=reconstruct(initial)
                self.assertEqual(result,tuple(initial))
                self.assertEqual(len(relative_actions),12)

    def test_corner_only_probe_cannot_detect_pure_edge_change(self):
        identity=bytes(range(48))
        altered=word(EDGE_ONLY_DIFFERENCE)
        self.assertNotEqual(identity,altered)
        for pos in CORNERS:
            self.assertEqual(factor_value(pos,identity),factor_value(pos,altered))
        for token in MOVES:
            original=compose(MOVES[token],identity)
            changed=compose(MOVES[token],altered)
            self.assertEqual(observe(original,REF_CORNER),
                             observe(changed,REF_CORNER))

    def test_edge_only_probe_cannot_detect_pure_corner_change(self):
        identity=bytes(range(48))
        altered=word(CORNER_ONLY_DIFFERENCE)
        self.assertNotEqual(identity,altered)
        for pos in EDGE_POS:
            self.assertEqual(factor_value(pos,identity),factor_value(pos,altered))
        for token in MOVES:
            original=compose(MOVES[token],identity)
            changed=compose(MOVES[token],altered)
            self.assertEqual(observe(original,REF_EDGE),
                             observe(changed,REF_EDGE))

    def test_bad_state_is_rejected(self):
        with self.assertRaisesRegex(ValueError,"complete physical"):
            reconstruct(bytes([0]*48))

if __name__=="__main__":
    unittest.main()
