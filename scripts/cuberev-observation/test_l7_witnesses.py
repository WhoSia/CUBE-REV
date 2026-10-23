#!/usr/bin/env python3
"""Independently check three physical 7-move 1-bit-correcting witnesses.

Each witness resolves one of the only three 4-source sets not achievable at L=6.
The checker reconstructs 54-sticker dynamics on every run; it does not trust
the claimed distances or a serialized observation table.
"""
import unittest
from physical_edges import ACTIONS, edge_transitions
from robust_observation import signatures

WITNESSES = {
    85:  ("U", "R", "F", "R2", "B", "U2", "F"),
    802: ("U", "R", "F", "U", "F", "U2", "F"),
    3208: ("U", "R'", "B", "R", "B", "R", "B"),
    1084: ("B", "F", "D", "B'", "R'", "F", "R"),
}

class L7WitnessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.moves = edge_transitions()

    def test_all_three_witnesses(self):
        self.assertEqual(len(WITNESSES), 4)
        for mask, word in WITNESSES.items():
            with self.subTest(mask=mask):
                self.assertEqual(len(word), 7)
                sig = signatures(self.moves, tuple(ACTIONS.index(a) for a in word))
                ids = [j for j in range(12) if mask & (1 << j)]
                self.assertEqual(len(ids), 5 if mask == 1084 else 4)
                pair_distances = {
                    (a,b): (sig[a] ^ sig[b]).bit_count()
                    for i,a in enumerate(ids) for b in ids[i+1:]
                }
                self.assertEqual(len(pair_distances), 10 if mask == 1084 else 6)
                self.assertGreaterEqual(min(pair_distances.values()), 3)
                print("L7_PHYSICAL_WITNESS_PASS", mask, " ".join(word),
                      "min_distance", min(pair_distances.values()))

if __name__ == "__main__":
    unittest.main()
