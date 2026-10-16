import Lean
import FiberInvariantTransfer

/-!
CUBE-REV 0.25 P0-R6I-P11 — exact restrictions on transporting
a fixed-source prefix-cylinder no-meet certificate by a symmetry.
A goal-preserving transformation alone is NOT sufficient: original
source must be fixed, primitive move actions must commute after
relabeling, and the relabeling must take the ENTIRE canonical source
language region being certified into a region whose absence was
actually proved. No cube spatial-rotation stabilizer of the
specific fixed scramble is asserted or assumed to exist.
-/
namespace CubeRev025

universe u v

def executeCubeWord
    {S : Type u} {A : Type v}
    (move : S → A → S) (start : S) (word : List A) : S :=
  word.foldl move start

theorem whole_word_commutes_with_action_relabeling
    {S : Type u} {A : Type v}
    (move : S → A → S)
    (transform : S → S) (relabel : A → A)
    (moveEquivariant : ∀ s a,
      transform (move s a) = move (transform s) (relabel a))
    (start : S) (word : List A) :
    transform (executeCubeWord move start word) =
      executeCubeWord move (transform start) (word.map relabel) := by
  induction word generalizing start with
  | nil => rfl
  | cons a tail ih =>
    change transform (List.foldl move (move start a) tail) =
      List.foldl move (move (transform start) (relabel a))
        (tail.map relabel)
    calc
      transform (List.foldl move (move start a) tail) =
          List.foldl move (transform (move start a))
            (tail.map relabel) := ih (move start a)
      _ = List.foldl move (move (transform start) (relabel a))
            (tail.map relabel) := by rw [moveEquivariant start a]

/-- Transfer a source-word nonmeet proof across a full goal-preserving
automorphism only after discharging ALL obligations:
(1) whole-state action equivariance; (2) goal invariance;
(3) the ACTUAL source state is fixed; and
(4) the source canonical language maps inside an ALREADY certified
target canonical language. A generic cube symmetry not fixing
the scrambled start, or not preserving the canonical DFA language,
cannot be used to shrink the remaining 14 source-first-action jobs. -/
theorem sound_original_source_prefix_refutation_transfer
    {S : Type u} {A : Type v}
    (move : S → A → S)
    (transform : S → S) (relabel : A → A)
    (goal : S → Prop)
    (source : S)
    (originalWords : List A → Prop)
    (certifiedWords : List A → Prop)
    (moveEquivariant : ∀ s a,
      transform (move s a) = move (transform s) (relabel a))
    (goalInvariant : ∀ s, goal (transform s) ↔ goal s)
    (sourceFixed : transform source = source)
    (languageTransport : ∀ w,
      originalWords w → certifiedWords (w.map relabel))
    (negativeCertifiedCylinder : ∀ w,
      certifiedWords w → ¬ goal (executeCubeWord move source w)) :
    ∀ w, originalWords w → ¬ goal (executeCubeWord move source w) := by
  intro w hOriginal hGoal
  have hMapped :
      goal (executeCubeWord move source (w.map relabel)) := by
    have hTransform :=
      (goalInvariant (executeCubeWord move source w)).mpr hGoal
    rw [whole_word_commutes_with_action_relabeling
       move transform relabel moveEquivariant source w] at hTransform
    rw [sourceFixed] at hTransform
    exact hTransform
  exact (negativeCertifiedCylinder (w.map relabel)
    (languageTransport w hOriginal)) hMapped

end CubeRev025
