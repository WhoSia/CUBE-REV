/-!
CUBE-REV 0.23 P3-R0 — Finite PDB Rank-Reversal and Multivariate Opportunity
Theorems about orders and feasible resource sets.
NO claims of human cognitive ability or full-cube complexity. There is no sorry or axiom.
-/
namespace CUBE_REV

def IsMono (f : Nat → Nat) : Prop := ∀ a b, a ≤ b → f a ≤ f b

def IsBiMono (f : Nat → Nat → Nat) : Prop :=
  ∀ a b c d, a ≤ c → b ≤ d → f a b ≤ f c d

theorem single_PDB_rank_reversal_forbids_monotone_exact_prediction
    (hMain hAlt dMain dAlt : Nat)
    (rank : hAlt ≤ hMain) (trueCost : dMain < dAlt) :
    ¬ ∃ f : Nat → Nat, IsMono f ∧
        f hMain = dMain ∧ f hAlt = dAlt := by
  intro ex
  rcases ex with ⟨f, mono, eqMain, eqAlt⟩
  have ordered : dAlt ≤ dMain := by
    rw [← eqMain, ← eqAlt]
    exact mono hAlt hMain rank
  exact (Nat.not_le_of_gt trueCost) ordered

theorem vector_PDB_Pareto_reversal_forbids_bimonotone_exact_prediction
    (cMain cAlt eMain eAlt dMain dAlt : Nat)
    (corner : cAlt ≤ cMain) (edges : eAlt ≤ eMain)
    (trueCost : dMain < dAlt) :
    ¬ ∃ f : Nat → Nat → Nat, IsBiMono f ∧
        f cMain eMain = dMain ∧ f cAlt eAlt = dAlt := by
  intro ex
  rcases ex with ⟨f, mono, eqMain, eqAlt⟩
  have ordered : dAlt ≤ dMain := by
    rw [← eqMain, ← eqAlt]
    exact mono cAlt eAlt cMain eMain corner edges
  exact (Nat.not_le_of_gt trueCost) ordered

theorem constraint_relaxation_preserves_feasibility
    {Action : Type} {Req : Type}
    (satisfies : Action → Req → Prop)
    (requiredTight requiredLoose : List Req)
    (subset : ∀ x, x ∈ requiredLoose → x ∈ requiredTight)
    (a : Action)
    (feasibleTight : ∀ x, x ∈ requiredTight → satisfies a x) :
    ∀ x, x ∈ requiredLoose → satisfies a x := by
  intro x hx
  exact feasibleTight x (subset x hx)

theorem action_expansion_preserves_witness
    {Action : Type} (a : Action) (poolSmall poolLarge : List Action)
    (included : ∀ x, x ∈ poolSmall → x ∈ poolLarge)
    (witness : a ∈ poolSmall) :
    a ∈ poolLarge := by
  exact included a witness

theorem rank_reversal_example :
    ¬ ∃ f : Nat → Nat → Nat, IsBiMono f ∧
      f 6 9 = 10 ∧ f 5 7 = 12 := by
  exact vector_PDB_Pareto_reversal_forbids_bimonotone_exact_prediction
    6 5 9 7 10 12 (by decide) (by decide) (by decide)

/- This counterexample instantiates one actual P8-R6 real cubie U intervention.
   The general theorem is about order, not about exact PDB group physics. -/

end CUBE_REV
