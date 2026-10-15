import Lean
import ProjectionMarginalObstruction

/-!
CUBE-REV 0.25 P0-R6I-P9 — exact conditional corner→edge fiber
support distinguishability. This is the rigorous representation
complexity obstruction behind the next candidate cache architecture,
not a measured new optimization.
-/
namespace CubeRev025

universe u v w

/-- An exact fiber codec labels each corner, then gives a predicate
for allowed edge states from that label. Exact reconstruction must
hold for the WHOLE joint target, not merely for the edge marginal. -/
structure ExactFiberCodec (C : Type u) (E : Type v) (Label : Type w)
    (goal : C → E → Prop) where
  encode : C → Label
  supports : Label → E → Prop
  exact : ∀ c e, goal c e ↔ supports (encode c) e

/-- Equality of compressed fiber labels enforces extensional
equality of the whole edge membership predicate at those corners. -/
theorem same_exact_fiber_label_forces_same_edge_support
    {C : Type u} {E : Type v} {Label : Type w}
    {goal : C → E → Prop}
    (codec : ExactFiberCodec C E Label goal)
    (c₁ c₂ : C)
    (equalLabel : codec.encode c₁ = codec.encode c₂) :
    ∀ e, goal c₁ e ↔ goal c₂ e := by
  intro e
  have h₁ := codec.exact c₁ e
  have h₂ := codec.exact c₂ e
  rw [equalLabel] at h₁
  exact h₁.trans h₂.symm

/-- Fundamental exact index lower bound: corner states with at least
one differing compatible edge MUST carry distinct compressed labels.
Any proposal to identify these two fibers is an incorrect joint-cubie
membership oracle, even if both original separate marginals match. -/
theorem distinguishable_exact_fibers_require_distinct_labels
    {C : Type u} {E : Type v} {Label : Type w}
    {goal : C → E → Prop}
    (codec : ExactFiberCodec C E Label goal)
    (c₁ c₂ : C) (witness : E)
    (different : goal c₁ witness ≠ goal c₂ witness) :
    codec.encode c₁ ≠ codec.encode c₂ := by
  intro hEqual
  have hSame :=
    same_exact_fiber_label_forces_same_edge_support codec c₁ c₂ hEqual witness
  exact different (propext hSame)

/-- If a finite or infinite selection of corner representatives all
have pairwise different compatible-edge membership predicates, an
exact fiber codec must be injective on that selection. This yields
a lower bound on distinct representational labels without assuming
any particular compressed data-structure implementation. -/
theorem pairwise_distinct_fibers_force_injective_labels
    {C : Type u} {E : Type v} {Label : Type w}
    {goal : C → E → Prop}
    (codec : ExactFiberCodec C E Label goal)
    (separates : ∀ c₁ c₂ : C, c₁ ≠ c₂ →
       ∃ e, goal c₁ e ≠ goal c₂ e) :
    Function.Injective codec.encode := by
  intro x y hEqual
  by_contra hDiff
  obtain ⟨w, hw⟩ := separates x y hDiff
  exact (distinguishable_exact_fibers_require_distinct_labels
    codec x y w hw) hEqual

end CubeRev025
