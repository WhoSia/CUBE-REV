#!/usr/bin/env python3
"""Fail-closed, archive-free regression for the algebraic support census."""
from __future__ import annotations

import sys
import unittest
from collections import Counter
from math import comb, factorial
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_stabilizer_support_spectrum import (
    exact_support_count,
    exhaustive_small_profile,
    stabilizer_order,
    support_profile,
)


class SupportSpectrumTests(unittest.TestCase):
    def test_regression_22(self):
        self.assertEqual(stabilizer_order(2, 2), 12)
        self.assertEqual(
            {k: v for k, v in support_profile(2, 2).items() if v},
            {(0, 0): 1, (2, 0): 2, (0, 2): 1, (2, 2): 8},
        )

    def test_full_cube_order(self):
        self.assertEqual(stabilizer_order(8, 12), 43252003274489856000)

    def test_no_single_moved_tag(self):
        for e in range(13):
            self.assertEqual(exact_support_count(1, e), 0)
        for c in range(9):
            self.assertEqual(exact_support_count(c, 1), 0)

    def test_sum_and_positivity_every_valid_parameter(self):
        for c in range(9):
            for e in range(13):
                profile = support_profile(c, e)
                self.assertTrue(all(v >= 0 for v in profile.values()))
                self.assertEqual(sum(profile.values()), stabilizer_order(c, e))
                self.assertEqual(
                    sum(comb(c, i) * comb(e, j) * exact_support_count(i, j)
                        for i in range(c + 1) for j in range(e + 1)),
                    stabilizer_order(c, e),
                )

    def test_independent_small_coordinate_enumerations(self):
        for c in range(4):
            for e in range(4):
                with self.subTest(c=c, e=e):
                    self.assertEqual(
                        exhaustive_small_profile(c, e),
                        Counter({k: v for k, v in support_profile(c, e).items() if v}),
                    )
        self.assertEqual(
            exhaustive_small_profile(4, 4),
            Counter({k: v for k, v in support_profile(4, 4).items() if v}),
        )

    def test_reject_naive_wrong_count_models(self):
        # Wrong model #1: ignores linked permutation parity.
        naive_without_parity = factorial(2) * factorial(2) * 3 * 2
        self.assertEqual(naive_without_parity, 24)
        self.assertNotEqual(naive_without_parity, stabilizer_order(2, 2))
        # Wrong model #2: ignores free orientation choices.
        naive_without_orientations = factorial(2) * factorial(2) // 2
        self.assertEqual(naive_without_orientations, 2)
        self.assertNotEqual(naive_without_orientations, stabilizer_order(2, 2))

    def test_invalid_input_fail_closed(self):
        for args in [(-1, 2), (2, -1), (9, 0), (0, 13),
                     (1.5, 2), (2, None)]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                stabilizer_order(*args)
            with self.subTest(args=args), self.assertRaises(ValueError):
                exact_support_count(*args)


if __name__ == "__main__":
    unittest.main()
