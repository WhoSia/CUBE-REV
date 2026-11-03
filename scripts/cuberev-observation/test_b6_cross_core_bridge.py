#!/usr/bin/env python3
"""Cross-core bridge tests independent of the 156-node BFS implementation."""
import sys
import unittest
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_b6_cross_core_bridge import (
    omitted_pair_components, three_cross_core_swaps_certificate
)
from verify_b6_geometric_rule import EDGE_NAMES, ENDS, valid_pairs


class B6CrossCoreBridgeTests(unittest.TestCase):
    def test_all_adjacent_corner_cores_have_three_wheel_links(self):
        for h, k in combinations(EDGE_NAMES, 2):
            if len(ENDS[h] & ENDS[k]) != 1:
                continue
            common = valid_pairs(h) & valid_pairs(k)
            self.assertEqual(len(common), 3)
            for core in (h, k):
                wheel = next(edges for vertices, edges
                             in omitted_pair_components(core)
                             if len(vertices) == 5)
                self.assertTrue(common <= wheel)

    def test_each_of_12_cores_has_wheel_cycle_edge_isolated(self):
        for core in EDGE_NAMES:
            with self.subTest(core=core):
                comps = omitted_pair_components(core)
                self.assertEqual(
                    sorted((len(v), len(e)) for v, e in comps),
                    [(1, 0), (2, 1), (4, 4), (5, 8)]
                )

    def test_exact_named_adjacent_core_bridge(self):
        self.assertEqual(
            valid_pairs("DL") & valid_pairs("DF"),
            {
                frozenset(("BR", "UB")),
                frozenset(("BR", "UR")),
                frozenset(("UB", "UR"))
            }
        )

    def test_full_structural_proof_without_graph_bfs(self):
        self.assertIsNone(three_cross_core_swaps_certificate())


if __name__ == "__main__":
    unittest.main()
