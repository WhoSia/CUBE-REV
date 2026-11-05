#!/usr/bin/env python3
"""Independent Python/P48 cross-check of R8 local edge-certificate census.

Uses the repository's 3D-generated 48-sticker physical PIECES/SLOTS rather
than the independent C++ edge-name catalog. Full corners are granted as
an oracle and their parity is fixed; this is NOT a human or adaptive policy.
"""
import unittest
from collections import Counter
from itertools import combinations, permutations, product
from b6_independent_48sticker_goals import EDGE_POS, PIECES, SLOTS, FACES, word, factor_value

INVERSE_FACES={v:k for k,v in FACES.items()}
COLORS=tuple(tuple(INVERSE_FACES[SLOTS[s][1]] for s in PIECES[p])
             for p in EDGE_POS)
assert len(COLORS)==12 and len(set(map(frozenset,COLORS)))==12

def even_permutation(seq):
    return sum(seq[i]>seq[j] for i in range(len(seq))
               for j in range(i+1,len(seq)))%2==0

def possibilities(mask, stop=2):
    """Count exact corner-parity-compatible edge hypotheses, up to stop."""
    unobserved=set(mask)
    incomplete=[i for i in range(12)
                if any((i,j) in unobserved for j in (0,1))]
    choices=0
    for labels in permutations(incomplete):
        rem=[incomplete.index(j) for j in labels]
        if not even_permutation(rem):
            continue
        flips=[]
        for dest,src in zip(incomplete,labels):
            options=tuple(flip for flip in (0,1)
                          if all(COLORS[src][(k+flip)%2]==COLORS[dest][k]
                                 for k in (0,1) if (dest,k) not in unobserved))
            if not options:break
            flips.append(options)
        if len(flips)!=len(incomplete):continue
        for chosen in product(*flips):
            if sum(chosen)%2==0:
                choices+=1
                if choices>=stop:return stop
    return choices

class R8PhysicalEdgeCertificateCourt(unittest.TestCase):
    def test_catalog_and_legal_turn_orientation(self):
        self.assertEqual(sorted(Counter(c for edge in COLORS for c in edge).values()),[4]*6)
        for actions in ("", "U", "R", "F", "D2", "U R F' L2 D B'"):
            state=word(actions)
            self.assertEqual(sum(factor_value(p,state)%2 for p in EDGE_POS)%2,0)

    def test_all_four_omitted_facelet_masks(self):
        hist=Counter()
        for mask in combinations(product(range(12),range(2)),4):
            hist[possibilities(mask)==1]+=1
        self.assertEqual(hist[True],9426)
        self.assertEqual(hist[False],1200)

    def test_all_five_omitted_facelet_masks(self):
        hist=Counter()
        for mask in combinations(product(range(12),range(2)),5):
            hist[possibilities(mask)==1]+=1
        self.assertEqual(hist[True],26400)
        self.assertEqual(hist[False],16104)

    def test_explicit_17_read_certificate_for_true_solved_edge_state(self):
        catalog={frozenset(COLORS[i]):i for i in range(12)}
        example=[("UR","U"),("UR","R"),("UF","U"),("UL","U"),
                 ("UB","U"),("DR","R"),("DF","D")]
        mask=tuple((catalog[frozenset(edge)],COLORS[catalog[frozenset(edge)]].index(face))
                   for edge,face in example)
        self.assertEqual(len(mask),7)
        self.assertEqual(possibilities(mask),1)
        # Enlarging an omitted set weakens information.
        missing_eighth=(catalog[frozenset("FR")],COLORS[catalog[frozenset("FR")]].index("F"))
        self.assertEqual(possibilities(mask+(missing_eighth,)),2)

if __name__=="__main__":
    unittest.main()
