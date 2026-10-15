import Lean
import OneStepProjectionEnvelope

/-!
CUBE-REV 0.25 P0-R6I-P9: a finite obstruction to a common
research inference. Matching the two separate corner/edge goal
marginals is a necessary condition for a full-cubie membership, but
NOT sufficient: the joint relation need not be a Cartesian product.
We prove both the general necessary condition and a two-by-two
explicit finite counterexample. Thus P9's exact C6/C7/E6 projected
gate remains a ONE-SIDED exclusion, never a positive whole-cube meet.
-/
namespace CubeRev025

universe u v

def cornerMarginal
    {C : Type u} {E : Type v}
    (goal : C → E → Prop) (corner : C) : Prop :=
  ∃ edge, goal corner edge

def edgeMarginal
    {C : Type u} {E : Type v}
    (goal : C → E → Prop) (edge : E) : Prop :=
  ∃ corner, goal corner edge

/-- Full target membership implies BOTH coordinate margins. The
reverse implication requires independence (a rectangular target),
which the actual cube's correlated permutation/orientation constraints
and bounded-depth goal generally cannot provide. -/
theorem whole_goal_implies_both_marginals
    {C : Type u} {E : Type v}
    (goal : C → E → Prop) (c : C) (e : E)
    (whole : goal c e) :
    cornerMarginal goal c ∧ edgeMarginal goal e := by
  exact ⟨⟨e, whole⟩, ⟨c, whole⟩⟩

/-- Witness that joint goal membership cannot generally be
reconstructed by independently crossing corner and edge marginals:
on the two-point diagonal relation both individual marginals pass for
(false,true), whereas the exact joint membership fails. -/
theorem independent_marginals_not_sufficient :
    cornerMarginal (fun (c e : Bool) => c = e) false ∧
    edgeMarginal (fun (c e : Bool) => c = e) true ∧
    ¬ ((false : Bool) = true) := by
  refine ⟨⟨false, rfl⟩, ⟨true, rfl⟩, ?_⟩
  decide

end CubeRev025
