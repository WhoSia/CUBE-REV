#!/usr/bin/env python3
"""Regress two-probe active observability and no-go for one cubie type."""
import unittest
from b6_independent_48sticker_goals import (
    EDGE_POS, CORNERS, MOVES, EDGE_POSITION, target, factor_value, word, compose
)
from active_p48_fixed_site_scan import (
    joint_position_words, twelve_frame_scan, eleven_frame_scan, reconstruct, reconstruct_with_edge_parity,
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

    def test_eleven_frames_and_edge_flip_legality_recover_full_group_examples(self):
        plan=eleven_frame_scan()
        self.assertEqual(len(plan),11)
        self.assertEqual(len({e for e,c,w in plan}),11)
        self.assertEqual({c for e,c,w in plan},set(CORNERS))
        examples=["","U","F","R U2 F' L B2","U L2 D' F R B",
                  EDGE_ONLY_DIFFERENCE,CORNER_ONLY_DIFFERENCE]
        for w in examples:
            with self.subTest(word=w):
                state=word(w)
                self.assertEqual(reconstruct_with_edge_parity(state,plan),tuple(state))

    def test_every_ten_frame_schedule_on_solved_has_a_pure_double_edge_flip_adversary(self):
        # One edge-position probe per frame can inspect at most ten initial
        # edge locations. Two unseen locations support a legal double flip.
        plan=twelve_frame_scan()[:10]
        sampled={e for e,c,w in plan}
        missing=set(EDGE_POS)-sampled
        self.assertEqual(len(missing),2)
        bypos={v:k for k,v in EDGE_POSITION.items()}
        omitted=frozenset(bypos[p] for p in missing)
        flipped=target("DL",omitted,0,0,1)
        solved=bytes(range(48))
        self.assertNotEqual(flipped,solved)
        for _,_,tokens in plan:
            frame=word(" ".join(tokens))
            self.assertEqual(
                observe(compose(frame,flipped),REF_EDGE),
                observe(compose(frame,solved),REF_EDGE))
            self.assertEqual(
                observe(compose(frame,flipped),REF_CORNER),
                observe(compose(frame,solved),REF_CORNER))

    def test_bad_state_is_rejected(self):
        with self.assertRaisesRegex(ValueError,"complete physical"):
            reconstruct(bytes([0]*48))

if __name__=="__main__":
    unittest.main()
