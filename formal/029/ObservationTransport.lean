import AdaptiveLowerBound

namespace CubeRev029

/-- Two state-dependent observation functions give the same policy result if
they agree at *every possible query* on the two fixed states. This is stronger
than agreeing along a preselected schedule: the induction covers every reply
branch reached by the adaptive policy. -/
theorem Policy.run_fixed_reply_equiv
    {S T Q R O : Type}
    (tree : Policy Q R O)
    (leftObserve : S → Q → R) (leftState : S)
    (rightObserve : T → Q → R) (rightState : T)
    (agree : ∀ query, leftObserve leftState query =
                       rightObserve rightState query) :
    tree.run leftObserve leftState = tree.run rightObserve rightState := by
  induction tree with
  | stop output => rfl
  | read query next ih =>
      change (next (leftObserve leftState query)).run leftObserve leftState =
        (next (rightObserve rightState query)).run rightObserve rightState
      rw [agree query]
      exact ih (rightObserve rightState query)

/-- A general policy transport theorem, intended for use after the first
eleven edge colors have fixed one normalizing color map and query permutation.

The actual representative-policy certificate, the response-equivariance of
the concrete Rubik-cube normalization, and its inverse are *premises* here.
They must be discharged in cube-specific Lean code. The theorem does NOT
assert that such witnesses already exist for all first-eleven histories.

The representative policy may branch adaptively: at each node the address is
mapped before the reply is returned, using only the fixed normalization.
Transport does not increase the number of remaining observation frames. -/
theorem transport_certified_policy
    {S T Q₁ Q₂ R₁ R₂ : Type}
    (toRepresentative : S → T)
    (fromRepresentative : T → S)
    (queryToOriginal : Q₂ → Q₁)
    (replyToRepresentative : Q₂ → R₁ → R₂)
    (originalObserve : S → Q₁ → R₁)
    (representativeObserve : T → Q₂ → R₂)
    (admissible : S → Prop)
    (representativePolicy : Policy Q₂ R₂ T)
    {budget : Nat}
    (withinBudget : Fits budget representativePolicy)
    (observationEquivariance : ∀ s, admissible s → ∀ q,
      replyToRepresentative q (originalObserve s (queryToOriginal q)) =
        representativeObserve (toRepresentative s) q)
    (representativeCorrect : ∀ s, admissible s →
      representativePolicy.run representativeObserve (toRepresentative s) =
        toRepresentative s)
    (roundTrip : ∀ s, admissible s →
      fromRepresentative (toRepresentative s) = s) :
    ∃ originalPolicy : Policy Q₁ R₁ S,
      Fits budget originalPolicy ∧
        ∀ s, admissible s →
          originalPolicy.run originalObserve s = s := by
  refine ⟨representativePolicy.adapt queryToOriginal
    replyToRepresentative fromRepresentative,
    Policy.adapt_fits queryToOriginal replyToRepresentative
      fromRepresentative withinBudget, ?_⟩
  intro s hs
  have sameRun :
      representativePolicy.run
        (fun (state : S) q =>
          replyToRepresentative q (originalObserve state (queryToOriginal q))) s =
      representativePolicy.run representativeObserve (toRepresentative s) :=
    Policy.run_fixed_reply_equiv representativePolicy
      (fun (state : S) q =>
        replyToRepresentative q (originalObserve state (queryToOriginal q))) s
      representativeObserve (toRepresentative s)
      (observationEquivariance s hs)
  rw [Policy.adapt_run, sameRun, representativeCorrect s hs, roundTrip s hs]

#print axioms Policy.run_fixed_reply_equiv
#print axioms transport_certified_policy

end CubeRev029
