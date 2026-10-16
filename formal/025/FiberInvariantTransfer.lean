import Lean
import FiberAutomorphismStabilizers

/-!
CUBE-REV 0.25 P0-R6I-P11 — shared nonempty exact fiber forces
equality of every corner invariant that must equal an invariant
of every compatible edge. The Rubik full-cubie parity coupling
is a mathematical instance: sign(corner permutation) equals
sign(edge permutation) for every physically legal whole state.
This does not deduce an unproved orbit classification of the 576 pairs.
-/
namespace CubeRev025

universe u v w

/-- In a goal relation with an invariant matching contract on BOTH
coordinates, two corners sharing a nonempty exact edge support
cannot disagree on their corner invariant. The witness edge
belongs to both fibers, hence mediates the equality. -/
theorem nonempty_equal_fibers_agree_on_joint_coordinate_invariant
    {C : Type u} {E : Type v} {Value : Type w}
    (goal : C → E → Prop)
    (cornerInvariant : C → Value)
    (edgeInvariant : E → Value)
    (everyGoalPairCompatible :
      ∀ c e, goal c e →
        cornerInvariant c = edgeInvariant e)
    (c₁ c₂ : C)
    (fiberEqual :
      ∀ e, goal c₁ e ↔ goal c₂ e)
    (nonempty : ∃ e, goal c₁ e) :
    cornerInvariant c₁ = cornerInvariant c₂ := by
  rcases nonempty with ⟨edge, hFirst⟩
  have hSecond : goal c₂ edge :=
    (fiberEqual edge).mp hFirst
  exact (everyGoalPairCompatible c₁ edge hFirst).trans
    (everyGoalPairCompatible c₂ edge hSecond).symm

/-- With Boolean parity, this is the necessary equal-permutation-sign
constraint for two distinct Rubik corner coordinates whose exact
edge sets are literally identical and nonempty, provided every
whole legal cube state has equal corner and edge permutation parity. -/
theorem exact_shared_edge_fiber_requires_equal_cube_permutation_parity
    {C : Type u} {E : Type v}
    (legalGoal : C → E → Prop)
    (cornerParity : C → Bool)
    (edgeParity : E → Bool)
    (legalPermutationParity :
      ∀ c e, legalGoal c e →
        cornerParity c = edgeParity e)
    (c₁ c₂ : C)
    (sameEdgeSupport :
      ∀ e, legalGoal c₁ e ↔ legalGoal c₂ e)
    (hasCompatibleEdge : ∃ e, legalGoal c₁ e) :
    cornerParity c₁ = cornerParity c₂ :=
  nonempty_equal_fibers_agree_on_joint_coordinate_invariant
    legalGoal cornerParity edgeParity legalPermutationParity
    c₁ c₂ sameEdgeSupport hasCompatibleEdge

end CubeRev025
