#!/usr/bin/env python3
"""Tests for the B6 optimal-sensor swap graph and uniform Johnson control."""
import sys
import unittest
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_b6_geometric_rule import EDGE_NAMES
from verify_b6_sensor_exchange_graph import components, exchange_graph


class B6SensorExchangeGraphTests(unittest.TestCase):
    def test_every_core_component_size(self):
        for h in EDGE_NAMES:
            graph = exchange_graph(h)
            with self.subTest(core=h):
                self.assertEqual(len(graph), 13)
                self.assertEqual(sorted(map(len, components(graph))), [1, 4, 8])
                self.assertEqual(sum(map(len, graph.values())) // 2, 22)

    def test_explicit_other_component_unreachable(self):
        graph = exchange_graph("DL")
        a = frozenset(("FR", "UR"))
        b = frozenset(("DR", "UL"))
        self.assertIn(a, graph)
        self.assertIn(b, graph)
        self.assertFalse(any(a in x and b in x for x in components(graph)))

    def test_graph_edges_exactly_one_sensor_swap(self):
        graph = exchange_graph("DL")
        for a, adjacent in graph.items():
            for b in adjacent:
                self.assertEqual(len(a ^ b), 2)
                self.assertIn(a, graph[b])

    def test_complete_two_subset_control_connected(self):
        vertices = [frozenset(c) for c in combinations(range(6), 2)]
        graph = {a: {b for b in vertices if len(a ^ b) == 2}
                 for a in vertices}
        self.assertEqual(list(map(len, components(graph))), [15])
        self.assertEqual({len(x) for x in graph.values()}, {8})


if __name__ == "__main__":
    unittest.main()
