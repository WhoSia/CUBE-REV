#!/usr/bin/env python3
"""Fail-closed regressions for independent P48 B6 goal construction.

No historical 54-facelet archive, prior B6-positive verdicts, or target
checksums are imported. Does NOT assert any goal has HTM distance >=13.
"""
import unittest
from collections import Counter
from b6_independent_48sticker_goals import (
    MOVES, SPATIAL, EDGE_NAMES, SLOTS, layout_orbits, target, word,
    compose, inverse, conjugate, generate, valid_pairs, audit,
)

class IndependentB6P48GoalTests(unittest.TestCase):
    def test_physical_inverse_and_48_spatial_conjugations(self):
        eye=bytes(range(48))
        self.assertEqual(len(SLOTS),48)
        self.assertEqual(len(MOVES),18)
        self.assertEqual(len(SPATIAL),48)
        for token,turn in MOVES.items():
            inverted=token if token.endswith("2") else token[:-1] if token.endswith("'") else token+"'"
            self.assertEqual(compose(turn,MOVES[inverted]),eye)
        all_moves=set(MOVES.values())
        self.assertTrue(all(conjugate(m,p) in all_moves for _,p,_ in SPATIAL for m in MOVES.values()))

    def test_eight_layout_orbits_not_predicated_on_historical_positive_masks(self):
        self.assertTrue(all(len(valid_pairs(e))==13 for e in EDGE_NAMES))
        self.assertEqual(sorted(map(len,layout_orbits())),[12,12,12,24,24,24,24,24])

    def test_independently_constructed_targets_reproduce_88_74_41(self):
        entries,states,classes=generate()
        self.assertEqual(len(entries),88)
        self.assertEqual(len(states),74)
        self.assertEqual(len(classes),41)
        self.assertEqual(Counter(map(len,classes)),Counter({1:17,2:19,3:1,4:4}))

    def test_known_nontrivial_13_htm_edge_flip_end_state(self):
        known="L F R' F' L' U2 R U R U' R2 U2 R"
        expected=target("DL",frozenset(("UF","UR")),0,0,1)
        self.assertEqual(word(known),expected)
        self.assertNotEqual(expected,bytes(range(48)))

    def test_all_generated_targets_have_true_sticker_permutation_and_inverse(self):
        targets,states,classes=generate()
        for goal in states:
            self.assertEqual(sorted(goal),list(range(48)))
            self.assertEqual(compose(goal,inverse(goal)),bytes(range(48)))
        self.assertEqual(set().union(*classes),states)

    def test_incorrect_swaps_do_not_match_known_control(self):
        known=word("L F R' F' L' U2 R U R U' R2 U2 R")
        self.assertNotEqual(known,target("DL",frozenset(("UF","UR")),1,0,1))
        self.assertNotEqual(known,target("DL",frozenset(("UF","UR")),0,1,1))

if __name__=="__main__":
    unittest.main()
