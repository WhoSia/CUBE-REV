import Lean

/-!
CUBE-REV 0.25 P0-R6I-P12-P2. Pure arithmetic necessity:
nontrivial cycle counts of a parity-even permutation with moved support
four or six; and signed nonzero twist differences summing to zero mod 3.
Explicitly NOT a theorem connecting physical original B6 pairs to S8
cycle decompositions. The S8/CP bridge is an independent OPEN obligation.
-/
namespace CubeRev025P12

theorem four_moved_even_cycles
    (n2 n3 n4 n5 n6 : Nat)
    (support : 2*n2 + 3*n3 + 4*n4 + 5*n5 + 6*n6 = 4)
    (evenSign : (n2 + n4 + n6) % 2 = 0) :
    n2 = 2 ∧ n3 = 0 ∧ n4 = 0 ∧ n5 = 0 ∧ n6 = 0 := by
  omega

theorem six_moved_even_cycles
    (n2 n3 n4 n5 n6 : Nat)
    (support : 2*n2 + 3*n3 + 4*n4 + 5*n5 + 6*n6 = 6)
    (evenSign : (n2 + n4 + n6) % 2 = 0) :
    (n3 = 2 ∧ n2 = 0 ∧ n4 = 0 ∧ n5 = 0 ∧ n6 = 0) ∨
    (n4 = 1 ∧ n2 = 1 ∧ n3 = 0 ∧ n5 = 0 ∧ n6 = 0) := by
  omega

theorem two_twists_balanced (positive negative : Nat)
    (support : positive + negative = 2)
    (twist : (positive + 2*negative) % 3 = 0) :
    positive = 1 ∧ negative = 1 := by
  omega

theorem four_twists_balanced (positive negative : Nat)
    (support : positive + negative = 4)
    (twist : (positive + 2*negative) % 3 = 0) :
    positive = 2 ∧ negative = 2 := by
  omega

end CubeRev025P12
