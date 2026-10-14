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


/-- Same two-class quotient, but now a shard starts from one exact initial
18HTM generator (one low-class or one high-class initial last face). -/
def transferPair (state : Nat × Nat) : Nat × Nat :=
  (faceLowNext state.1 state.2, faceHighNext state.1 state.2)

/-- Under repeated depth-limited source DFS to radius R, an exact first-move
shard contributes depth-d canonical suffix words (R-d+1) times each.
This quantity excludes the R+1 visits to the empty source root. -/
def weightedFirstActionShard : Nat → Nat × Nat → Nat
  | 0, _ => 0
  | k+1, state =>
      (k+1)*(state.1+state.2) +
        weightedFirstActionShard k (transferPair state)

/-- Original normal-form B10 can be exactly split into 18 disjoint
first-action classes with the 11 empty-prefix iterative root calls separate.
These are recursive CALL counts and not counts of distinct physical cubes. -/
theorem exact_B10_first_action_shard_counts :
    weightedFirstActionShard 10 (1,0) = 17489205559 ∧
    weightedFirstActionShard 10 (0,1) = 14279876542 ∧
    11 + 9 * weightedFirstActionShard 10 (1,0) +
         9 * weightedFirstActionShard 10 (0,1) = 285921738920 := by
  decide

end CubeRev025
