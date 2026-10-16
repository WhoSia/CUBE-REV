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
  -- Bound and explicitly split the few possible cycle counts.  The
  -- unbounded modulo split in a single omega invocation is incomplete.
  have c2 : n2 = 0 ∨ n2 = 1 ∨ n2 = 2 := by omega
  have c3 : n3 = 0 ∨ n3 = 1 := by omega
  have c4 : n4 = 0 ∨ n4 = 1 := by omega
  rcases c2 with h2 | h2 | h2 <;>
    rcases c3 with h3 | h3 <;>
    rcases c4 with h4 | h4 <;>
    omega

theorem six_moved_even_cycles
    (n2 n3 n4 n5 n6 : Nat)
    (support : 2*n2 + 3*n3 + 4*n4 + 5*n5 + 6*n6 = 6)
    (evenSign : (n2 + n4 + n6) % 2 = 0) :
    (n3 = 2 ∧ n2 = 0 ∧ n4 = 0 ∧ n5 = 0 ∧ n6 = 0) ∨
    (n4 = 1 ∧ n2 = 1 ∧ n3 = 0 ∧ n5 = 0 ∧ n6 = 0) := by
  -- Eliminate the impossible 5-cycle directly, then split the 6-
  -- and 4-cycle choices.  Only the remaining few n2 cases need omega.
  have h5 : n5 = 0 := by omega
  have c6 : n6 = 0 ∨ n6 = 1 := by omega
  rcases c6 with h6 | h6
  · have c4 : n4 = 0 ∨ n4 = 1 := by omega
    rcases c4 with h4 | h4
    · have c2 : n2 = 0 ∨ n2 = 1 ∨ n2 = 2 ∨ n2 = 3 := by omega
      rcases c2 with h2 | h2 | h2 | h2 <;> omega
    · omega
  · omega

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


/-!
P12-P4 — Q3 graph isometry consequences, separated from the actual
finite 576-pair census. These are pure conditional mathematics, not
a claim that the graph symmetry has already been lifted to the true
joint CP/CO/EP/EO solved B6 action.
-/
universe u

theorem q3_distance_under_isometric_conjugation
    {V : Type u} (d : V → V → Nat)
    (g gInv perm : V → V)
    (inverseOnImage : ∀ x, gInv (g x) = x)
    (isometry : ∀ x y, d (g x) (g y) = d x y)
    (x : V) :
    d (g x) (g (perm (gInv (g x)))) = d x (perm x) := by
  calc
    d (g x) (g (perm (gInv (g x)))) =
        d (g x) (g (perm x)) := by rw [inverseOnImage x]
    _ = d x (perm x) := isometry x (perm x)

theorem q3_distance_under_inverse_reindexing
    {V : Type u} (d : V → V → Nat)
    (perm permInv : V → V)
    (inverseOnImage : ∀ x, permInv (perm x) = x)
    (symmetric : ∀ x y, d x y = d y x)
    (x : V) :
    d (perm x) (permInv (perm x)) = d x (perm x) := by
  calc
    d (perm x) (permInv (perm x)) = d (perm x) x := by
      rw [inverseOnImage x]
    _ = d x (perm x) := (symmetric x (perm x)).symm

/-- Conditional algebraic form of the observed P12 orbit-mass identity.
No physical assumption establishes the numerical weight premise here. -/
theorem conditional_corner_orbit_mass_conservation
    (orbitSize stabilizerSize weight elementOrder : Nat)
    (orbitStabilizer : orbitSize * stabilizerSize = 48)
    (weightPremise : weight * elementOrder = 8 * stabilizerSize) :
    orbitSize * weight * elementOrder = 384 := by
  calc
    orbitSize * weight * elementOrder =
        orbitSize * (weight * elementOrder) := by
          simp [Nat.mul_assoc]
    _ = orbitSize * (8 * stabilizerSize) := by rw [weightPremise]
    _ = (orbitSize * stabilizerSize) * 8 := by ac_rfl
    _ = 384 := by rw [orbitStabilizer]; omega

end CubeRev025P12
