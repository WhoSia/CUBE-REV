/-!
CUBE-REV 0.16 — staged Lean 4 formalization.

This file is not a proof of the 24-state optimum 8/10 or the catalogue
lower bound 25. It formalizes the generic reversible-word obstruction and
checks closed arithmetic consequences of an independently proved spectral
formula. Semantic equivalence of the Lean inputs and physical cubie maps is
an independent obligation. Until an actual Lean runner passes this file,
status is LEAN_SOURCE_PENDING_COMPILATION, not LEAN_KERNEL_PASS.
-/
import Init
import P11Fractional
import P12LightGraph

namespace CubeRev016

universe u

/-- A known finite action word of reversible maps is itself a permutation. -/
def evalWord {α : Type u} : List (Equiv α α) → Equiv α α
  | [] => Equiv.refl α
  | a :: rest => a.trans (evalWord rest)

/-- Two distinct states cannot be merged by any preset reversible word. -/
theorem fixed_word_does_not_merge {α : Type u}
    (w : List (Equiv α α)) {x y : α} (hxy : x ≠ y) :
    evalWord w x ≠ evalWord w y := by
  intro hEq
  exact hxy ((evalWord w).injective hEq)

/-- A recorded word can be undone by its inverse. -/
theorem known_history_inverts {α : Type u}
    (w : List (Equiv α α)) (x : α) :
    (evalWord w).symm (evalWord w x) = x := by
  exact (evalWord w).left_inv x

/-- This integer expression is the earlier P8 spectral formula.
Its equivalence with the *physical* 18-move edge action graph is an
external proof obligation, not established by this definition alone. -/
def spectralReturn (t : Nat) : Nat :=
  (18 ^ t + 2 * 16 ^ t + 6 * 14 ^ t + 2 * 12 ^ t + 13 * 10 ^ t) / 24

/-- Closed arithmetic proof, not a graph isomorphism proof. -/
theorem four_turn_return_arithmetic : spectralReturn 4 = 26584 := by
  decide

/-- Fourteen bits cannot label 26,584 different historical strings. -/
theorem four_turn_14_bits_insufficient : 2 ^ (14 : Nat) < spectralReturn 4 := by
  decide

/-- Fifteen bits can label at least 26,584 different historical strings. -/
theorem four_turn_15_bits_suffice_numerically :
    spectralReturn 4 ≤ 2 ^ (15 : Nat) := by
  decide

end CubeRev016
