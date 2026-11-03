#!/usr/bin/env python3
"""Full 20-tag exchange-graph tests; no hidden physical ZIP required."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit_b6_full_sensor_swap_graph import (
    complete_layouts, connected_components, observed_exchange_graph
)
from verify_b6_geometric_rule import EDGE_NAMES, valid_pairs


class FullB6SensorSwapGraphTests(unittest.TestCase):
    def test_all_156_no_duplicate_designs(self):
        self.assertEqual(len(complete_layouts()), 156)

    def test_symmetric_single_tag_exchange(self):
        graph = observed_exchange_graph()
        for a, near in graph.items():
            for b in near:
                self.assertIn(a, graph[b])
                self.assertEqual(len(a[0] ^ b[0])+len(a[1] ^ b[1]), 2)

    def test_fixed_core_subtotal_and_completeness(self):
        graph = observed_exchange_graph()
        self.assertEqual(
            sum(1 for a, near in graph.items() for b in near
                if a[0] == b[0]) // 2,
            264,
        )
        self.assertEqual(
            sum(map(len, connected_components(graph))),
            156,
        )

    def test_naive_all_pairs_broader_than_positive(self):
        self.assertEqual(len(EDGE_NAMES), 12)
        self.assertTrue(all(len(valid_pairs(h)) == 13 for h in EDGE_NAMES))


if __name__ == "__main__":
    unittest.main()
