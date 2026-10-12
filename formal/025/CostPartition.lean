/-!
CUBE-REV 0.25 P0-R2 — scaled move-cost partitioning, Lean 4 core theorem.

This proves a completely generic algebraic path-cost safety lemma. The link
from the original physical 54 facelets to the five executable PDB transitions,
and the finite 15,625-allocation computation, are checked by Go/C++, NOT by
this Lean theorem. Do NOT infer global original-cube optimality.
-/
import Lean

namespace CubeRev025

universe u

/-- Exact accumulated nonnegative price for a legal action word. -/
def wordPrice {A : Type u} (price : A → Nat) : List A → Nat
  | [] => 0
  | a :: tail => price a + wordPrice price tail

/-- Any pointwise scaled budget for five quotations bounds the sum of
actual word prices, for EVERY common action word, not five independent words. -/
theorem five_costs_share_one_physical_word {A : Type u}
    (p₀ p₁ p₂ p₃ p₄ : A → Nat) (scale : Nat)
    (budget : ∀ a, p₀ a + p₁ a + p₂ a + p₃ a + p₄ a ≤ scale)
    (word : List A) :
    wordPrice p₀ word + wordPrice p₁ word + wordPrice p₂ word +
      wordPrice p₃ word + wordPrice p₄ word ≤ scale * word.length := by
  induction word with
  | nil => simp [wordPrice]
  | cons a tail ih =>
      dsimp [wordPrice]
      have hb := budget a
      simp only [List.length_cons, Nat.mul_add, Nat.mul_one]
      omega

/-- If a projected quotient's lower distance is no larger than the cost
of the SAME original physical solution word, their joint value is safe. -/
theorem five_admissible_pdb_lower_bounds {A : Type u}
    (p₀ p₁ p₂ p₃ p₄ : A → Nat) (scale : Nat)
    (budget : ∀ a, p₀ a + p₁ a + p₂ a + p₃ a + p₄ a ≤ scale)
    (word : List A) (h₀ h₁ h₂ h₃ h₄ : Nat)
    (hcost₀ : h₀ ≤ wordPrice p₀ word)
    (hcost₁ : h₁ ≤ wordPrice p₁ word)
    (hcost₂ : h₂ ≤ wordPrice p₂ word)
    (hcost₃ : h₃ ≤ wordPrice p₃ word)
    (hcost₄ : h₄ ≤ wordPrice p₄ word) :
    h₀ + h₁ + h₂ + h₃ + h₄ ≤ scale * word.length := by
  have h := five_costs_share_one_physical_word p₀ p₁ p₂ p₃ p₄ scale budget word
  omega

/-- A concrete one-move rejection of raw addition of five overlapping
unit-price patterns. This illustrates the actual physical U-turn issue,
but identifying the real U-turn projection distances stays an external test. -/
theorem five_unpartitioned_units_are_unsound :
    ¬ ((5 : Nat) ≤ 1) := by
  decide

end CubeRev025