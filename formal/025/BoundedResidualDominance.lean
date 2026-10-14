import ProjectionWordLanguage

/-!
CUBE-REV 0.25 P0-R6F / TCS — finite-depth right-language INCLUSION,
strictly generalizing equality-based proof-cache reuse.

A reduced product state may contain corner quotient, edge quotient,
last-generator DFA state, and other certificate-relevant information.
The definition is over ONE action word, preserving noncommutative order.

This theorem does not assert that such a simulation relation is cheaply
decidable for the full original cube or that a B9 certificate is complete.
-/
namespace CubeRev025

universe u z

/-- The SUCCESS language from weak is a subset of the SUCCESS language from
strong through depth budget k. This is a preorder, not an equivalence. -/
def boundedRightLanguageIncluded
    {S : Type u} {A : Type z}
    (step : S → A → S)
    (accept : S → Prop) (k : Nat)
    (strong weak : S) : Prop :=
  ∀ word : List A,
    word.length ≤ k →
    accept (runWord step weak word) →
    accept (runWord step strong word)

/-- Reflexivity of the bounded right-language simulation preorder. -/
theorem bounded_right_language_reflexive
    {S : Type u} {A : Type z}
    (step : S → A → S) (accept : S → Prop)
    (k : Nat) (s : S) :
    boundedRightLanguageIncluded step accept k s s := by
  intro _ _ h
  exact h

/-- Transitivity allows antichain-style dominance proof reuse. -/
theorem bounded_right_language_transitive
    {S : Type u} {A : Type z}
    (step : S → A → S) (accept : S → Prop)
    (k : Nat) (x y z : S)
    (hxy : boundedRightLanguageIncluded step accept k x y)
    (hyz : boundedRightLanguageIncluded step accept k y z) :
    boundedRightLanguageIncluded step accept k x z := by
  intro word hLen hz
  exact hxy word hLen (hyz word hLen hz)

/-- A failed stronger state (one admitting every possible success word of
the weaker state) proves that the weaker state also has NO short success. -/
theorem bounded_right_language_absence_transfer
    {S : Type u} {A : Type z}
    (step : S → A → S) (accept : S → Prop)
    (k : Nat) (strong weak : S)
    (hInc : boundedRightLanguageIncluded step accept k strong weak)
    (emptyStrong : ∀ word : List A,
      word.length ≤ k → ¬ accept (runWord step strong word)) :
    ∀ word : List A,
      word.length ≤ k → ¬ accept (runWord step weak word) := by
  intro word hLen hWeak
  exact emptyStrong word hLen (hInc word hLen hWeak)

/-- Prefixing the SAME physical action maps a depth k+1 simulation
to a depth k simulation. Ordered action word order is maintained. -/
theorem bounded_right_language_step_congruence
    {S : Type u} {A : Type z}
    (step : S → A → S) (accept : S → Prop)
    (k : Nat) (strong weak : S) (a : A)
    (hInc : boundedRightLanguageIncluded step accept (k+1) strong weak) :
    boundedRightLanguageIncluded step accept k
      (step strong a) (step weak a) := by
  intro word hLen hWeak
  have hWholeLen : (a :: word).length ≤ k+1 := by
    simpa using (Nat.succ_le_succ hLen)
  have hWhole :
      accept (runWord step strong (a :: word)) :=
    hInc (a :: word) hWholeLen (by simpa only [runWord] using hWeak)
  simpa only [runWord] using hWhole

/-- The preorder is monotone when one shrinks the remaining word budget. -/
theorem bounded_right_language_budget_monotone
    {S : Type u} {A : Type z}
    (step : S → A → S) (accept : S → Prop)
    (large small : Nat) (strong weak : S)
    (hBudget : small ≤ large)
    (hInc : boundedRightLanguageIncluded step accept large strong weak) :
    boundedRightLanguageIncluded step accept small strong weak := by
  intro word hLen hWeak
  exact hInc word (Nat.le_trans hLen hBudget) hWeak

end CubeRev025
