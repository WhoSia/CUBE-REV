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

/- A multivariate M* is an infimum over feasible resource costs, not a
   scalar of human IQ or a result derived from solve times. If the expanded
   action/observation/budget regime admits every witness from the old regime,
   the new *attained* minimal integer cardinality cannot be larger. -/
def AttainedMinimum (P : Nat → Prop) (n : Nat) : Prop :=
  P n ∧ ∀ k, k < n → ¬ P k

theorem expanded_opportunity_minimum_cannot_increase
    (restrict expand : Nat → Prop) (m n : Nat)
    (included : ∀ k, restrict k → expand k)
    (mAttained : AttainedMinimum restrict m)
    (nAttained : AttainedMinimum expand n) :
    n ≤ m := by
  have impossible : ¬ m < n := by
    intro hm
    exact (nAttained.2 m hm) (included m mAttained.1)
  exact Nat.le_of_not_gt impossible

/- A deterministic perfect-information solver must assign different solving
   words to different exact group states. The proof assumes real HTM group
   right-action injectivity; the finite 62-state physical witnesses are separately
   certified by their original complete 54-sticker solver. -/
theorem exact_full_solve_word_assignment_injective
    {State Word : Type}
    (act : State → Word → State)
    (actInjective : ∀ w, Function.Injective (fun s => act s w))
    (goal : State)
    (algorithmFor : State → Word)
    (correct : ∀ s, act s (algorithmFor s) = goal) :
    Function.Injective algorithmFor := by
  intro s t sameWord
  have hs : act s (algorithmFor s) = goal := correct s
  have ht : act t (algorithmFor s) = goal := by
    rw [sameWord]
    exact correct t
  exact (actInjective (algorithmFor s)) (hs.trans ht.symm)

/- P3-R2: deterministic observation policy cannot solve two distinct EXACT physical
   states when they share one observation and each legal action word is a bijection.
   This is an order/indistinguishability theorem, not a theorem of observed cognition. -/
theorem identical_observation_blocks_two_distinct_exact_full_solves
    {State Observation Word : Type}
    (observe : State → Observation)
    (act : State → Word → State)
    (action_injective : ∀ w, Function.Injective (fun s => act s w))
    (goal : State)
    (a b : State) (sameObservation : observe a = observe b)
    (distinct : a ≠ b)
    (policy : Observation → Word) :
    ¬ (act a (policy (observe a)) = goal ∧
       act b (policy (observe b)) = goal) := by
  intro h
  have sameWord : policy (observe a) = policy (observe b) :=
    congrArg policy sameObservation
  have sameTarget : act a (policy (observe a)) =
      act b (policy (observe a)) := by
    calc
      act a (policy (observe a)) = goal := h.1
      _ = act b (policy (observe b)) := h.2.symm
      _ = act b (policy (observe a)) := by rw [sameWord]
  exact distinct (action_injective (policy (observe a)) sameTarget)

theorem rank_reversal_example :
    ¬ ∃ f : Nat → Nat → Nat, IsBiMono f ∧
      f 6 9 = 10 ∧ f 5 7 = 12 := by
  exact vector_PDB_Pareto_reversal_forbids_bimonotone_exact_prediction
    6 5 9 7 10 12 (by decide) (by decide) (by decide)

/- This counterexample instantiates one actual P8-R6 real cubie U intervention.
   The general theorem is about order, not about exact PDB group physics. -/

end CUBE_REV
