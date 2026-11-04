#!/usr/bin/env python3
"""Regression and adversarial mutation of B6 exchange/realistic color boundaries."""
import unittest
from collections import Counter
from audit_b6_exchange_line_graph import (
    audit as exchange_audit, positive_omissions, swap_graph, components,
)
from audit_color_probe_information_bounds import (
    audit as color_audit, lower_frames, nonadaptive_error_lower_frames,
    face_color_at_slot, two_one_facelet_colors, ALPHABET
)
from b6_independent_48sticker_goals import word, EDGE_POS, CORNERS

class ExchangeAndColorCourt(unittest.TestCase):
    def test_156_swap_layouts_factor_through_cube_line_graph(self):
        p=exchange_audit()
        self.assertEqual(p["vertices"],156)
        self.assertEqual(p["edges"],336)
        self.assertEqual(p["cube_line_graph_edges"],24)
        self.assertEqual(p["links_per_incident_core_pair"],3)
        self.assertEqual(p["components"],Counter({96:1,4:12,1:12}))

    def test_mutation_one_missing_valid_layout_changes_component_census(self):
        original=positive_omissions()
        edited=dict(original)
        edited.pop(next(iter(edited)))
        mutated=swap_graph(edited)
        self.assertEqual(len(mutated),155)
        self.assertNotEqual(
            Counter(map(len,components(mutated))),
            Counter({96:1,4:12,1:12}))

    def test_color_cardinality_and_error_assumption(self):
        p=color_audit()
        self.assertEqual(p["clean_lower"],13)
        self.assertEqual(p["erasure_lower_fixed"],14)
        self.assertEqual(p["one_error_lower_fixed"],15)
        self.assertEqual(p["b4_lower"],4)
        self.assertEqual(lower_frames(262),2)
        self.assertEqual(nonadaptive_error_lower_frames(262,0),2)

    def test_actual_quantized_sticker_channel_is_not_perfect_cubie_oracle(self):
        solved=word("")
        changed=word("R U F2")
        a=two_one_facelet_colors(solved,solved)
        b=two_one_facelet_colors(changed,solved)
        self.assertEqual(len(a),2)
        self.assertEqual(len(b),2)
        self.assertTrue(all(x in "URFDLB" for x in a+b))
        with self.assertRaises(ValueError):
            two_one_facelet_colors(bytes([0]*48),solved)

if __name__=="__main__":
    unittest.main()
