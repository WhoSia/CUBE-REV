#!/usr/bin/env python3
"""Deterministic physical smoke tests. Run: python -m unittest discover -s scripts/cuberev-observation -p 'test_*.py'"""
import unittest
from physical_edges import ACTIONS, edge_transitions
from robust_observation import signatures, feasible_sources, explore
from dictionary_coverage import evaluate
from physical_set_cover import build, greedy, lower_bound
from verify_l7_27_cover import verify, INPUT
from generate_sampled_dictionary import build as regenerate_sample

class PhysicalSmoke(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.moves = edge_transitions()

    def test_18_actions_bijective(self):
        self.assertEqual(len(self.moves),18)
        for row in self.moves:
            self.assertEqual(sorted(row),list(range(24)))

    def test_inverse_actions(self):
        for face in "URFDLB":
            a=ACTIONS.index(face)
            inv=ACTIONS.index(face+"'")
            for initial in range(24):
                self.assertEqual(self.moves[inv][self.moves[a][initial]],initial)

    def test_robust_pair_synthetic(self):
        signs=(0,7)+tuple([0]*10)
        self.assertIn(3, feasible_sources(signs,min_distance=3,max_size=2))
        self.assertNotIn(3, feasible_sources(signs,min_distance=4,max_size=2))

    def test_actual_l2_zero_error_count(self):
        counts=explore(self.moves,2,min_distance=1)
        self.assertEqual(counts["3"],64)
        self.assertEqual(counts["4"],0)

    def test_four_word_dictionary_physical_coverage(self):
        result=evaluate()
        self.assertEqual(result['dictionary_size'],4)
        self.assertEqual(result['coverage_by_size'], {'3':120,'4':60,'5':6})
        self.assertFalse(result['global_minimum_proven'])

    def test_physical_set_cover_four_seeds(self):
        covers=build()
        universe=set().union(*covers)
        self.assertEqual(len(universe),186)
        g=greedy(covers,universe)
        self.assertEqual(g['status'],'COVERED_IN_POOL')
        self.assertEqual(len(set().union(*(covers[i] for i in g['indices']))),186)
        self.assertLessEqual(lower_bound(covers,universe),g['size'])

    def test_l7_constructive_cover_27(self):
        certificate=verify()
        self.assertEqual(certificate['status'],'PHYSICAL_27_WORD_UPPER_BOUND_PASS')
        self.assertEqual(certificate['covered'],{'3':220,'4':495})
        self.assertFalse(certificate['globally_optimal'])

    def test_reproduce_seeded_27_word_dictionary(self):
        import json
        data=json.loads(INPUT.read_text(encoding='utf-8'))
        reconstructed=regenerate_sample()
        self.assertEqual(reconstructed['selected_words'],data['words'])
        self.assertEqual(reconstructed['uncovered_target_count'],0)
        self.assertEqual(len(reconstructed['selected_words']),27)

    def test_bounded_smoke(self):
        with self.assertRaises(AssertionError):
            explore(self.moves,7,min_distance=3)

if __name__=="__main__":
    unittest.main()
