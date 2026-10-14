import Lean

/-!
CUBE-REV 0.25 P0-R6C: abstract proof of SAME-action projected descendant
rejection. The physical 54-sticker cube transitions, finite true B6 goal
ball and source-complete B7/B8 search are verified separately in C++/Go.

This file makes NO claim that a synthetic abstract proof proves the
original 3×3 cube's global 14-move exclusion.
-/

namespace CubeRev025

universe u v w z

/-- If a full goal state must satisfy both its corner and edge image
predicates, any move failing the conjunction is NOT a goal state. -/
theorem rejected_common_action_not_goal
    {S : Type u} {A : Type z} {C : Type v} {E : Type w}
    (step : S → A → S)
    (corner : S → C) (edge : S → E)
    (goal : S → Prop)
    (cornerInGoal : C → Prop) (edgeInGoal : E → Prop)
    (cornerNecessary : ∀ y, goal y → cornerInGoal (corner y))
    (edgeNecessary : ∀ y, goal y → edgeInGoal (edge y))
    (x : S) (a : A)
    (reject : ¬ (cornerInGoal (corner (step x a)) ∧
                  edgeInGoal (edge (step x a)))) :
    ¬ goal (step x a) := by
  intro hGoal
  exact reject ⟨cornerNecessary (step x a) hGoal,
                edgeNecessary (step x a) hGoal⟩

/-- A canonical source prefix is safely prunable if EVERY allowed one-step
child fails to enter BOTH true goal projections under the SAME action. -/
theorem all_canonical_descendants_excluded
    {S : Type u} {A : Type z} {C : Type v} {E : Type w}
    (step : S → A → S)
    (corner : S → C) (edge : S → E)
    (goal : S → Prop)
    (cornerInGoal : C → Prop) (edgeInGoal : E → Prop)
    (allowed : A → Prop)
    (cornerNecessary : ∀ y, goal y → cornerInGoal (corner y))
    (edgeNecessary : ∀ y, goal y → edgeInGoal (edge y))
    (x : S)
    (noAllowedCommonAction : ∀ a, allowed a →
      ¬ (cornerInGoal (corner (step x a)) ∧
         edgeInGoal (edge (step x a)))) :
    ∀ a, allowed a → ¬ goal (step x a) := by
  intro a hAllowed
  exact rejected_common_action_not_goal
    step corner edge goal cornerInGoal edgeInGoal
    cornerNecessary edgeNecessary x a (noAllowedCommonAction a hAllowed)

/-- Corner-only rejection is always also a sound full-goal rejection.
This theorem does NOT assert that corner membership is sufficient. -/
theorem corner_projection_negative_is_sound
    {S : Type u} {C : Type v}
    (corner : S → C) (goal : S → Prop) (cornerInGoal : C → Prop)
    (necessary : ∀ y, goal y → cornerInGoal (corner y))
    (x : S) (reject : ¬ cornerInGoal (corner x)) :
    ¬ goal x := by
  intro hx
  exact reject (necessary x hx)

end CubeRev025
