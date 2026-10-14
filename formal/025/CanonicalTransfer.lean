import Lean

/-!
CUBE-REV 0.25 P0-R6E — exact canonical action grammar transfer identity.

The original source normal form has six faces URFDLB, each with
three 18HTM generator powers. Adjacent equal faces are forbidden,
and commuting opposite faces are kept only in increasing face order.
The 6 faces collapse under permutation of the three opposite-face
axes to two classes (index0..2, index3..5). Counts of legal words
ending in each class obey the 2×2 integer transfer T=[[6,6],[9,6]].

This Lean theorem certifies the EXACT algebraic characteristic
recurrence conditional on that combinatorial transfer.
Independent Go checks each 18-generator adjacency count against T.
-/
namespace CubeRev025

/-- Number of legal canonical words after extending by one move:
new low-ending =6L+6H, new high-ending =9L+6H. -/
def faceLowNext (low high : Nat) : Nat := 6*low+6*high
def faceHighNext (low high : Nat) : Nat := 9*low+6*high

/-- Characteristic polynomial of T is X²−12X−18.
Hence total canonical word counts satisfy c[n+2]=12*c[n+1]+18*c[n]. -/
theorem two_class_canonical_grammar_characteristic
    (low high : Nat) :
    (faceLowNext (faceLowNext low high) (faceHighNext low high) +
     faceHighNext (faceLowNext low high) (faceHighNext low high))
    =
    12*(faceLowNext low high + faceHighNext low high) +
    18*(low+high) := by
  simp only [faceLowNext, faceHighNext]
  omega

/-- The first two exact source canonical action layers. -/
theorem canonical_source_first_two_word_layers :
    (9+9 : Nat)=18 ∧
    (faceLowNext 9 9 + faceHighNext 9 9)=243 := by
  decide

end CubeRev025
