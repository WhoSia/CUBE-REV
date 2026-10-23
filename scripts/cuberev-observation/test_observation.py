#!/usr/bin/env python3
"""Deterministic physical smoke tests. Run: python -m unittest discover -s scripts/cuberev-observation -p 'test_*.py'"""
import unittest
from physical_edges import ACTIONS, edge_transitions
from robust_observation import signatures, feasible_sources, explore
from dictionary_coverage import evaluate

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

    def test_bounded_smoke(self):
        with self.assertRaises(AssertionError):
            explore(self.moves,7,min_distance=3)

if __name__=="__main__":
    unittest.main()
