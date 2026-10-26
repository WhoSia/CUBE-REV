#!/usr/bin/env python3
"""Small deterministic sensor-orbit column-generation regression, no MILP."""
import unittest
from orbit_column_generation import columns
from physical_edges import ACTIONS,edge_transitions
from robust_observation import signatures
import itertools

class OrbitColumnGenerationTests(unittest.TestCase):
    def test_seed_dictionary_expands_to_real_columns(self):
        p=columns(mutations=0,top=0)
        self.assertEqual(p["orbit_words"],44)
        self.assertEqual(p["distinct_columns"],38)
        union=0
        for m in p["word_to_cover"].values():union|=m
        self.assertEqual(union,(1<<715)-1)

    def test_symmetry_candidate_columns_have_exact_physical_signatures(self):
        p=columns(seed=20261026,mutations=12,top=5)
        moves=edge_transitions()
        src=[s for k in (3,4) for s in itertools.combinations(range(12),k)]
        for word,mask in p["word_to_cover"].items():
            h=signatures(moves,word)
            reconstructed=sum(1<<i for i,s in enumerate(src)
                if all((h[a]^h[b]).bit_count()>=3 for a,b in itertools.combinations(s,2)))
            self.assertEqual(mask,reconstructed)

if __name__=="__main__":unittest.main()
