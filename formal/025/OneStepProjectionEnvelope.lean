import Lean
import ImmutableGoalBatch

/-!
CUBE-REV P0-R6I-P9: the exact one-step corner-envelope theorem.
A physical full-cubie move preserves projection through a corner
transition. The action alphabet is inverse-closed, as for all 18 HTM
quarter/half/inverse face moves. Hence exclusion from the COMPLETE
one-step envelope proves the impossibility of an original full-cubie
goal hit after any single legal move. This is not a claim that corners
alone positively certify a whole-cubie goal intersection.
-/
namespace CubeRev025

universe u v w

def cornerImage
    {S : Type u} {C : Type v}
    (projection : S → C) (goal : S → Prop) (c : C) : Prop :=
  ∃ state, goal state ∧ projection state = c

def oneStepCornerEnvelope
    {S : Type u} {C : Type v} {A : Type w}
    (projection : S → C) (goal : S → Prop)
    (cornerMove : C → A → C) (legalActions : A → Prop)
    (c : C) : Prop :=
  cornerImage projection goal c ∨
  ∃ targetCorner action,
    cornerImage projection goal targetCorner ∧
    legalActions action ∧ cornerMove targetCorner action = c

/-- The entire C6 membership image is necessarily contained in C7. -/
theorem corner_image_in_envelope
    {S : Type u} {C : Type v} {A : Type w}
    (projection : S → C) (goal : S → Prop)
    (cornerMove : C → A → C) (legalActions : A → Prop)
    (c : C)
    (h : cornerImage projection goal c) :
    oneStepCornerEnvelope projection goal cornerMove legalActions c :=
  Or.inl h

/-- Exact one-step envelope is minimal among sets that contain C6 and
all legal original HTM one-turn corner images of C6. -/
theorem one_step_envelope_minimal
    {S : Type u} {C : Type v} {A : Type w}
    (projection : S → C) (goal : S → Prop)
    (cornerMove : C → A → C) (legalActions : A → Prop)
    (other : C → Prop)
    (includesGoal : ∀ c, cornerImage projection goal c → other c)
    (includesMoves : ∀ c a,
       cornerImage projection goal c →
       legalActions a → other (cornerMove c a)) :
    ∀ c, oneStepCornerEnvelope projection goal cornerMove legalActions c →
      other c := by
  intro c h
  rcases h with hOriginal | ⟨before, a, hBefore, hAllowed, hEnd⟩
  · exact includesGoal c hOriginal
  · rw [← hEnd]
    exact includesMoves before a hBefore hAllowed

/-- The PREdecessor corner state must occur in exact C7 whenever
one full physical action lands in the original whole-cubie target.
The inverse closure condition is indispensable: a one-sided projected
successor neighborhood is safe only for inverse-closed HTM actions. -/
theorem one_step_corner_preimage_sound
    {S : Type u} {C : Type v} {A : Type w}
    (move : S → A → S) (projection : S → C)
    (cornerMove : C → A → C) (goal : S → Prop)
    (legalActions : A → Prop) (inverse : A → A)
    (commutes : ∀ s a,
      projection (move s a) = cornerMove (projection s) a)
    (inverseAdmissible : ∀ a, legalActions a → legalActions (inverse a))
    (inverseCancels : ∀ c a,
      cornerMove (cornerMove c a) (inverse a) = c)
    (s : S) (a : A)
    (legal : legalActions a)
    (reachesGoal : goal (move s a)) :
    oneStepCornerEnvelope projection goal cornerMove legalActions
      (projection s) := by
  right
  refine ⟨projection (move s a), inverse a, ?_, inverseAdmissible a legal, ?_⟩
  · exact ⟨move s a, reachesGoal, rfl⟩
  · rw [commutes]
    exact inverseCancels (projection s) a

/-- The negative projection-membership branch is a sound one-step
whole-physical-cubie nonreachability certificate, NEVER a positive one. -/
theorem exclude_one_step_from_corner_envelope
    {S : Type u} {C : Type v} {A : Type w}
    (move : S → A → S) (projection : S → C)
    (cornerMove : C → A → C) (goal : S → Prop)
    (legalActions : A → Prop) (inverse : A → A)
    (commutes : ∀ s a,
      projection (move s a) = cornerMove (projection s) a)
    (inverseAdmissible : ∀ a, legalActions a → legalActions (inverse a))
    (inverseCancels : ∀ c a,
      cornerMove (cornerMove c a) (inverse a) = c)
    (s : S)
    (missing : ¬ oneStepCornerEnvelope projection goal cornerMove legalActions
      (projection s)) :
    ∀ a, legalActions a → ¬ goal (move s a) := by
  intro a hLegal hGoal
  exact missing
    (one_step_corner_preimage_sound move projection cornerMove
      goal legalActions inverse commutes inverseAdmissible inverseCancels
      s a hLegal hGoal)

/-- The full one-generator ball operator on actual S-states. -/
def oneStepWholeBall
    {S : Type u} {A : Type w}
    (move : S → A → S) (goal : S → Prop)
    (legalActions : A → Prop) (x : S) : Prop :=
  goal x ∨ ∃ source action, goal source ∧
    legalActions action ∧ move source action = x

/-- Exact transport of one-step reachability under the cube's corner
projection: if the physical state quotient commutes with every 18HTM
generator, taking the existential projection AFTER one move is
literally equivalent to applying the induced corner action to the
entire projected goal. No heuristic estimate is involved.

Consequently C7 = π_C(B7) as an exact equality, provided B7 is
defined as the one-step completion of the full B6 and each physical
18HTM action commutes with corner projection. -/
theorem projection_preserves_one_step_ball
    {S : Type u} {C : Type v} {A : Type w}
    (move : S → A → S) (projection : S → C)
    (cornerMove : C → A → C) (goal : S → Prop)
    (legalActions : A → Prop)
    (commutes : ∀ s a,
       projection (move s a) = cornerMove (projection s) a)
    (c : C) :
    cornerImage projection
      (oneStepWholeBall move goal legalActions) c ↔
    oneStepCornerEnvelope projection goal cornerMove legalActions c := by
  constructor
  · rintro ⟨state, hState, hProjection⟩
    rcases hState with hBase | ⟨source, action, hSource, hAllowed, hMove⟩
    · exact Or.inl ⟨state, hBase, hProjection⟩
    · right
      refine ⟨projection source, action, ⟨source, hSource, rfl⟩,
        hAllowed, ?_⟩
      calc
        cornerMove (projection source) action =
          projection (move source action) := (commutes source action).symm
        _ = projection state := by rw [hMove]
        _ = c := hProjection
  · intro h
    rcases h with ⟨state, hState, hProjection⟩ |
      ⟨before, action, ⟨source, hSource, hBefore⟩, hLegal, hResult⟩
    · exact ⟨state, Or.inl hState, hProjection⟩
    · refine ⟨move source action, Or.inr
        ⟨source, action, hSource, hLegal, rfl⟩, ?_⟩
      calc
        projection (move source action) =
          cornerMove (projection source) action := commutes source action
        _ = cornerMove before action := by rw [hBefore]
        _ = c := hResult

end CubeRev025
