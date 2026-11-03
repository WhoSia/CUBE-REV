#!/usr/bin/env python3
"""Matroid basis-exchange countermodel tests for B6 sensor designs."""
import sys
import unittest
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_b6_basis_exchange_failure import exchange_failures
from verify_b6_geometric_rule import EDGE_NAMES, valid_pairs


class B6BasisExchangeTests(unittest.TestCase):
    def test_explicit_named_exchanges_both_fail(self):
        h = "DL"
        a = frozenset(("FR", "UR"))
        b = frozenset(("DR", "UL"))
        x = "DR"
        valid = valid_pairs(h)
        self.assertIn(a, valid)
        self.assertIn(b, valid)
        self.assertIn(x, b-a)
        possible = {frozenset((a - {y}) | {x}) for y in a-b}
        self.assertEqual(
            possible,
            {frozenset(("DR", "UR")), frozenset(("DR", "FR"))},
        )
        self.assertTrue(possible.isdisjoint(valid))

    def test_all_twelve_core_edges_identical_failure_counts(self):
        for core in EDGE_NAMES:
            with self.subTest(core=core):
                self.assertEqual(len(valid_pairs(core)), 13)
                self.assertEqual(len(exchange_failures(valid_pairs(core))), 176)

    def test_uniform_two_omission_family_has_basis_exchange(self):
        self.assertEqual(
            exchange_failures(combinations(EDGE_NAMES, 2)), []
        )

    def test_local_one_pair_family_has_no_violation(self):
        self.assertEqual(
            exchange_failures([("FR", "UR")]), []
        )

    def test_invalid_omission_size_rejected(self):
        with self.assertRaises(AssertionError):
            exchange_failures([("FR", "UR", "DL")])


if __name__ == "__main__":
    unittest.main()
