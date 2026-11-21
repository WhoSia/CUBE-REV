import FrozenPolicyInterpreter

namespace CubeRev029.Nineteen

/-- A finite sector's candidate identity tag (here a Bool sign) is NOT
another observation: it is a parameter to the terminal decoder that must
be computed from the physical nineteen-corner transcript. -/
def firstCandidateWithSign {S : Type} (sign : S → Bool)
    (bit : Bool) : List S → Option S
  | [] => none
  | state :: tail =>
      if sign state = bit then some state
      else firstCandidateWithSign sign bit tail

/-- Exactly the finite condition checked by each frozen upper-policy leaf:
there are no two *different* candidates with the same permutation sign.
The belief need not be nonempty until a real legal initial state is supplied. -/
def AtMostOnePerSign {S : Type}
    (sign : S → Bool) (belief : List S) : Prop :=
  ∀ a, a ∈ belief → ∀ b, b ∈ belief →
    sign a = sign b → a = b

/-- Every candidate already known to be in a sector is recovered by the
computed sign-specific selector if the sector contains at most one candidate
of either sign. This is a proof for arbitrary finite sectors, not an
enumeration of the frozen 144,736 candidates. -/
theorem first_candidate_is_correct_of_sign_unique {S : Type}
    (sign : S → Bool) :
    ∀ belief : List S, AtMostOnePerSign sign belief →
      ∀ state, state ∈ belief →
        firstCandidateWithSign sign (sign state) belief = some state := by
  intro belief
  induction belief with
  | nil =>
      intro unique state inBelief
      cases inBelief
  | cons head tail ih =>
      intro unique state inBelief
      by_cases same : sign head = sign state
      · have identified : head = state :=
          unique head (by simp) state inBelief same
        simp [firstCandidateWithSign, same, identified]
      · have inTail : state ∈ tail := by
          rcases List.mem_cons.mp inBelief with equal | inTail
          · exact False.elim (same (by simpa [equal]))
          · exact inTail
        have tailUnique : AtMostOnePerSign sign tail := by
          intro a ha b hb eq
          exact unique a (by simp [ha]) b (by simp [hb]) eq
        simpa [firstCandidateWithSign, same] using
          ih tailUnique state inTail

/-- The terminal decoder never produces an item that was absent from
the candidate belief: neither the sign bit nor a default sentinel can
fabricate an edge arrangement. -/
theorem first_candidate_witness_belongs {S : Type}
    (sign : S → Bool) (bit : Bool) (belief : List S)
    (state : S)
    (decoded : firstCandidateWithSign sign bit belief = some state) :
    state ∈ belief ∧ sign state = bit := by
  induction belief with
  | nil => simp [firstCandidateWithSign] at decoded
  | cons head tail ih =>
      by_cases same : sign head = bit
      · simp [firstCandidateWithSign, same] at decoded
        subst state
        exact ⟨by simp, same⟩
      · have rest : firstCandidateWithSign sign bit tail = some state := by
          simpa [firstCandidateWithSign, same] using decoded
        obtain ⟨mem, eq⟩ := ih rest
        exact ⟨by simp [mem], eq⟩

#print axioms first_candidate_is_correct_of_sign_unique
#print axioms first_candidate_witness_belongs

end CubeRev029.Nineteen
