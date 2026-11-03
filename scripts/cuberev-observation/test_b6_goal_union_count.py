#!/usr/bin/env python3
"""Independent cardinality and overlap tests for B6 stabilizer families."""
import sys
import unittest
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_b6_goal_union_count import legal_stabilizer


class B6GoalUnionTests(unittest.TestCase):
    def test_pairwise_common_pure_corner_subgroup(self):
        corners = (0, 1)
        pairs = list(combinations(range(12), 2))
        groups = [legal_stabilizer(corners, pair) for pair in pairs]
        common = set.intersection(*(set(g) for g in groups))
        self.assertEqual(len(common), 3)
        for i, group in enumerate(groups):
            self.assertEqual(len(group), 12)
            for other in groups[i + 1:]:
                self.assertEqual(group & other, common)

    def test_exact_union_formula_for_all_66(self):
        groups = [legal_stabilizer((0, 1), p)
                  for p in combinations(range(12), 2)]
        union = set()
        for m, group in enumerate(groups, 1):
            union.update(group)
            self.assertEqual(len(union), 3 + 9 * m)
        self.assertEqual(len(union), 597)

    def test_all_28_corner_pairs_have_same_structure(self):
        representative_edges = [(0, 1), (0, 2), (1, 2), (3, 9)]
        for corners in combinations(range(8), 2):
            groups = [legal_stabilizer(corners, e) for e in representative_edges]
            common = set.intersection(*(set(s) for s in groups))
            self.assertEqual(len(common), 3)
            self.assertEqual(len(set().union(*groups)), 3 + 9 * 4)

    def test_bad_cubie_indices_fail_closed(self):
        for c, e in [((-1, 1), (0, 1)), ((0, 8), (0, 1)),
                     ((0, 0), (0, 1)), ((0, 1), (3, 3)),
                     ((0, 1), (11, 12))]:
            with self.assertRaises(ValueError):
                legal_stabilizer(c, e)


if __name__ == "__main__":
    unittest.main()
