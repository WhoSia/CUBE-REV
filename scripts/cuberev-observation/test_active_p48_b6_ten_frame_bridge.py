#!/usr/bin/env python3
"""B6 stationary-slot ten-frame nonadaptive bridge and collision controls."""
import json
from pathlib import Path
import unittest
from b6_independent_48sticker_goals import EDGE_POS, CORNERS, SPATIAL, word, inverse
from active_p48_b6_ten_frame_bridge import (
    ten_frame_b6_plan, scan_inverse_factor_signature, audit
)
from verify_b6_negative_19_pairs_p48 import physical_support, transform_word

class ActiveP48B6TenFrameTests(unittest.TestCase):
    def test_exact_ten_frame_geometry_and_actual_inverse_factor_outputs(self):
        self.assertEqual(len(audit()[0]),10)

    def test_multiple_legal_group_states_match_original_tag_factors_of_inverse(self):
        plan,sensors,_=ten_frame_b6_plan()
        from b6_independent_48sticker_goals import factor_value
        for turns in ("","U","R' U' F2 L R2","F2 L B U' F D2",
                      "R U R' U' R' F R F'",
                      "L F R' F' L' U2 R U R U' R2 U2 R"):
            with self.subTest(turns=turns):
                state=word(turns)
                result=scan_inverse_factor_signature(state,plan)
                expected={p:factor_value(p,inverse(state)) for p in sensors}
                self.assertEqual(result,expected)

    def test_construct_explicit_nine_frame_nonadaptive_b5_collision(self):
        plan,_,_=ten_frame_b6_plan()
        selected={e for e,c,t in plan[:9]}
        missing=set(EDGE_POS)-selected
        self.assertEqual(len(missing),3)
        path=(Path(__file__).resolve().parents[2]/
              "data/0.28/B5_13_ORBIT_INDEPENDENT_WORD_PAIR_WITNESSES_20261104.json")
        manifest=json.loads(path.read_text(encoding="utf8"))
        found=None
        for row in manifest["witnesses"]:
            for det,permutation,R in SPATIAL:
                if det!=1:continue
                a=transform_word(row["left"],det,R)
                b=transform_word(row["right"],det,R)
                if physical_support(a,b)==frozenset(missing):
                    found=(a,b)
                    break
            if found:break
        self.assertIsNotNone(found,"13 geometric witness orbits must cover all 220 edge triples")
        a,b=found
        self.assertLessEqual(len(a.split()),5)
        self.assertLessEqual(len(b.split()),5)
        # Inverse preserves word distance, so both are true members of B5 subset B6.
        x=inverse(word(a))
        y=inverse(word(b))
        self.assertNotEqual(x,y)
        self.assertEqual(scan_inverse_factor_signature(x,plan[:9]),
                         scan_inverse_factor_signature(y,plan[:9]))

if __name__=="__main__":
    unittest.main()
