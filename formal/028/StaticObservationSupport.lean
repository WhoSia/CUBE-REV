import ObservationCovariance

/-!
CUBE-REV 0.28 R14-P8.17.
Pure model-agnostic observation theorem used to articulate the common
language of the A/B single-paper consolidation.

This is an elementary static separation/hitting equivalence.
It is standard mathematics, NOT claimed new group/decision-tree theory.
It does not prove any Rubik 16-tag, 21-frame, or 20-frame numerical result.

STATUS: source only until actual Lean kernel build has been observed.
-/

namespace CubeRev028

universe u v w

/-- A selected family of probes gives an injective combined signature. -/
def signatureInjective
    {X : Type u} {Q : Type v} {Y : Type w}
    (observe : X → Q → Y) (selected : Q → Prop) : Prop :=
  ∀ x y, (∀ q, selected q → observe x q = observe y q) → x = y

/-- Every pair of distinct states is separated by a selected probe. -/
def hitsEveryDifferenceSupport
    {X : Type u} {Q : Type v} {Y : Type w}
    (observe : X → Q → Y) (selected : Q → Prop) : Prop :=
  ∀ x y, x ≠ y → ∃ q, selected q ∧ observe x q ≠ observe y q

theorem signature_injective_iff_hitting_all_pairs
    {X : Type u} {Q : Type v} {Y : Type w}
    (observe : X → Q → Y) (selected : Q → Prop) :
    signatureInjective observe selected ↔
      hitsEveryDifferenceSupport observe selected := by
  classical
  constructor
  · intro h x y hne
    by_contra noProbe
    apply hne
    apply h x y
    intro q hSelected
    by_contra differs
    apply noProbe
    exact ⟨q, hSelected, differs⟩
  · intro h x y hSame
    by_contra hne
    obtain ⟨q, hSelected, differs⟩ := h x y hne
    exact differs (hSame q hSelected)

end CubeRev028
