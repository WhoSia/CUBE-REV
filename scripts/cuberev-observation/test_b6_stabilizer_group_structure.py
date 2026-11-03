#!/usr/bin/env python3
"""Executable group-structure tests for the physical cubie-coordinate law."""
import sys
import unittest
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_b6_stabilizer_group_structure import (
    ELEMENTS,
    IDENTITY,
    commutator,
    compose_coordinates,
    inverse,
    multiply,
    order,
    physical_cubie_record,
)


class B6StabilizerGroupTests(unittest.TestCase):
    def test_all_products_match_oriented_cubie_coordinates(self):
        for a in ELEMENTS:
            for b in ELEMENTS:
                self.assertEqual(
                    physical_cubie_record(multiply(a, b)),
                    compose_coordinates(
                        physical_cubie_record(a), physical_cubie_record(b)
                    ),
                )

    def test_all_associativity_and_inverses(self):
        for a in ELEMENTS:
            self.assertEqual(multiply(a, inverse(a)), IDENTITY)
            self.assertEqual(multiply(inverse(a), a), IDENTITY)
            for b in ELEMENTS:
                for c in ELEMENTS:
                    self.assertEqual(
                        multiply(multiply(a, b), c),
                        multiply(a, multiply(b, c))
                    )

    def test_group_order_center_commutator(self):
        self.assertEqual(Counter(order(a) for a in ELEMENTS),
                         {1: 1, 2: 7, 3: 2, 6: 2})
        center = {a for a in ELEMENTS if all(
            multiply(a, b) == multiply(b, a) for b in ELEMENTS
        )}
        self.assertEqual(center, {(0, 0, 0), (0, 0, 1)})
        self.assertEqual(
            {commutator(a, b) for a in ELEMENTS for b in ELEMENTS},
            {(0, 0, 0), (0, 1, 0), (0, 2, 0)},
        )

    def test_reject_wrong_orientation_composition_convention(self):
        a, b = (1, 1, 0), (0, 2, 0)
        correct = multiply(a, b)
        erroneous = (a[0] ^ b[0],
                     (a[1] + (-1 if a[0] else 1) * b[1]) % 3,
                     a[2] ^ b[2])
        self.assertEqual(correct, (1, 0, 0))
        self.assertNotEqual(correct, erroneous)


if __name__ == "__main__":
    unittest.main()
