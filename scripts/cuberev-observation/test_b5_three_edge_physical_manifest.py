#!/usr/bin/env python3
"""Independent physical B5 source-manifest verification regression tests."""
import unittest
from verify_b5_three_edge_physical_manifest import (
    B3_DEMONSTRATION, orbit_from_replayed_words, physical_support,
    verify_manifest, rotate_word, proper24,
)

class PhysicalB5TripleWitnessManifestTests(unittest.TestCase):
    def test_b3_known_original_edge_support_orbit_is_12(self):
        orbit=orbit_from_replayed_words("U R2 U'","D B2 D'")
        self.assertEqual(len(orbit),12)
        self.assertTrue(all(len(x)==3 for x in orbit))

    def test_rotated_physical_word_identity(self):
        original=physical_support("U R2 U'","D B2 D'")
        self.assertEqual(len(original),3)
        self.assertEqual(len({frozenset(x) for x in orbit_from_replayed_words(
            "U R2 U'","D B2 D'")}),12)
        self.assertEqual(len(proper24()),24)

    def test_b3_cannot_forge_full_220(self):
        with self.assertRaisesRegex(ValueError,"INCOMPLETE"):
            verify_manifest(B3_DEMONSTRATION,require_complete=True)

    def test_partial_reports_exactly_208_missing(self):
        result=verify_manifest(B3_DEMONSTRATION,require_complete=False)
        self.assertEqual(result["distinct_triple_edge_supports_physically_replayed"],12)
        self.assertEqual(result["missing_triple_edge_supports"],208)
        self.assertFalse(result["full_220_certificate"])

    def test_reject_nonphysical_support(self):
        with self.assertRaisesRegex(ValueError,"Not precisely 3"):
            physical_support("U","U")
        with self.assertRaisesRegex(ValueError,"Non-18HTM"):
            physical_support("M2","R")
        with self.assertRaisesRegex(ValueError,"exceeds five"):
            physical_support("U R L F B D","R")

    def test_reject_empty_and_unstructured_manifest(self):
        for x in ({},{"schema_version":1,"witnesses":[]},
                  {"schema_version":1,"witnesses":[{"left":"U"}]}):
            with self.assertRaises(ValueError):
                verify_manifest(x)

if __name__=="__main__":
    unittest.main()
