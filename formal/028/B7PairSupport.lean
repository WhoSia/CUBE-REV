import StaticObservationSupport

/-!
CUBE-REV 0.28 R14-P8.31.

A small abstract Lean bridge for the P8.30 B7 full-original-tag
finite witness certificate. A collision on two tags forces any
identifying sensor set to observe at least one of those tags.

This file does NOT formalize the 48-sticker physical engine, the
720 finite witness checks, all HTM moves, or the numerical b7=18.
It formalizes the logical hitting obligation conditional on witnessed
collisions; the physical certificate remains a separately tested input.
-/

namespace CubeRev028

inductive OriginalTag where
  | corner : Fin 8 → OriginalTag
  | edge : Fin 12 → OriginalTag
  deriving DecidableEq

/-- Two distinct states coincide on every original tag other than a and b. -/
def pairCollision
    {X : Type} {Y : Type}
    (observe : X → OriginalTag → Y) (a b : OriginalTag) : Prop :=
  ∃ x y, x ≠ y ∧
    ∀ q, q ≠ a → q ≠ b → observe x q = observe y q

/-- A complete identification signature must hit a witnessed collision pair. -/
theorem identifying_set_hits_pair
    {X : Type} {Y : Type}
    (observe : X → OriginalTag → Y)
    (selected : OriginalTag → Prop)
    (a b : OriginalTag)
    (hCollision : pairCollision observe a b)
    (hIdentify : signatureInjective observe selected) :
    selected a ∨ selected b := by
  classical
  by_contra neither
  have ha : ¬ selected a := by
    intro h
    exact neither (Or.inl h)
  have hb : ¬ selected b := by
    intro h
    exact neither (Or.inr h)
  obtain ⟨x, y, hne, sameOutside⟩ := hCollision
  apply hne
  apply hIdentify x y
  intro q hq
  have hqa : q ≠ a := by
    intro h
    subst q
    exact ha hq
  have hqb : q ≠ b := by
    intro h
    subst q
    exact hb hq
  exact sameOutside q hqa hqb

/-- The corner-pair portion of the P8.30 physical certificate. -/
theorem identifying_set_hits_all_corner_pairs
    {X : Type} {Y : Type}
    (observe : X → OriginalTag → Y)
    (selected : OriginalTag → Prop)
    (everyCornerPair :
      ∀ a b : Fin 8, a ≠ b →
        pairCollision observe (.corner a) (.corner b))
    (hIdentify : signatureInjective observe selected)
    (a b : Fin 8) (hab : a ≠ b) :
    selected (.corner a) ∨ selected (.corner b) := by
  exact identifying_set_hits_pair observe selected (.corner a) (.corner b)
    (everyCornerPair a b hab) hIdentify

/-- The edge-pair portion of the P8.30 physical certificate. -/
theorem identifying_set_hits_all_edge_pairs
    {X : Type} {Y : Type}
    (observe : X → OriginalTag → Y)
    (selected : OriginalTag → Prop)
    (everyEdgePair :
      ∀ a b : Fin 12, a ≠ b →
        pairCollision observe (.edge a) (.edge b))
    (hIdentify : signatureInjective observe selected)
    (a b : Fin 12) (hab : a ≠ b) :
    selected (.edge a) ∨ selected (.edge b) := by
  exact identifying_set_hits_pair observe selected (.edge a) (.edge b)
    (everyEdgePair a b hab) hIdentify

end CubeRev028
