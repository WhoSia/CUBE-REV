import SignedPairedPosterior

namespace CubeRev029.Nineteen

/-- The genuine terminal success predicate is: exactly one possible state,
not merely at most one candidate of each permutation sign. Empty beliefs
must not count as successful identifications. -/
def beliefExactlyOne {S : Type} (belief : S → Prop) : Prop :=
  ∃ state, belief state ∧ ∀ candidate, belief candidate → candidate = state

/-- State embedding with a true left inverse preserves *exact* singleton
beliefs. The proof never enumerates cube states. -/
theorem exactly_one_iff_transported_belief
    {S T : Type}
    (encode : S → T) (decode : T → S)
    (roundTrip : ∀ state, decode (encode state) = state)
    (belief : S → Prop) :
    beliefExactlyOne belief ↔
      beliefExactlyOne (transportedBelief encode belief) := by
  constructor
  · rintro ⟨state, hs, only⟩
    refine ⟨encode state, ⟨state, hs, rfl⟩, ?_⟩
    intro candidate h
    rcases h with ⟨other, ho, hc⟩
    rw [← hc, only other ho]
  · rintro ⟨target, ⟨state, hs, ht⟩, unique⟩
    refine ⟨state, hs, ?_⟩
    intro other ho
    have same : encode other = encode state :=
      (unique (encode other) ⟨other, ho, rfl⟩).trans ht.symm
    have decoded := congrArg decode same
    simpa [roundTrip] using decoded

/-- Terminal identification is preserved in BOTH directions after each
arbitrary ordered, paired-color query/response history. Thus a certified
representative *singleton* leaf and an actual original singleton posterior
are equivalent, provided the signed normalizer is chosen before continuation.
-/
theorem signed_terminal_singleton_iff_after_any_history
    (sigma : List Nat) (hsigma : sigma ∈ symmetries)
    (order : EdgeSlotOrder) (correction : Bool)
    (belief : SignedOriginalState → Prop)
    (history : List (PairedAddress12 × PairedReply12)) :
    beliefExactlyOne
      (beliefAfterTranscript
        (signedOriginalReadInRepresentativeCoordinates sigma order)
        belief history) ↔
    beliefExactlyOne
      (beliefAfterTranscript signedRepresentativePairRead
        (transportedBelief
          (signedRepresentativeEncode sigma order correction)
          belief) history) := by
  have h := exactly_one_iff_transported_belief
    (signedRepresentativeEncode sigma order correction)
    (signedRepresentativeDecode sigma order correction)
    (signed_representative_round_trip sigma hsigma order correction)
    (beliefAfterTranscript
      (signedOriginalReadInRepresentativeCoordinates sigma order)
      belief history)
  rw [signed_paired_posterior_all_histories
    sigma hsigma order correction belief history] at h
  exact h

/-- Physical sticker observations never reveal a *free, independent*
parity bit. Both signed states have identical edge and corner colors.
This is a mathematical negative control against a silently granted
parity oracle in the abstract eight-read continuation. -/
theorem unconstrained_parity_tag_is_unobservable
    (original : CubieAndCornerState)
    (tree : Policy PairedAddress12 PairedReply12 SignedOriginalState) :
    tree.run signedRealPairRead (original, false) =
      tree.run signedRealPairRead (original, true) := by
  exact Policy.run_fixed_reply_equiv tree
    signedRealPairRead (original, false)
    signedRealPairRead (original, true) (by intro query; rfl)

/-- No adaptive paired-color policy of ANY length can correctly output
both versions of a freely chosen sign tag attached to the same underlying
physical cube. For legal cubes the tag must be *derived*, not observed. -/
theorem cannot_recover_an_independent_parity_oracle
    (original : CubieAndCornerState)
    (tree : Policy PairedAddress12 PairedReply12 SignedOriginalState) :
    ¬ (tree.run signedRealPairRead (original, false) = (original, false) ∧
       tree.run signedRealPairRead (original, true) = (original, true)) := by
  intro both
  have equal := unconstrained_parity_tag_is_unobservable original tree
  rw [both.1, both.2] at equal
  have bogus : false = true := congrArg Prod.snd equal
  cases bogus

#print axioms exactly_one_iff_transported_belief
#print axioms signed_terminal_singleton_iff_after_any_history
#print axioms unconstrained_parity_tag_is_unobservable
#print axioms cannot_recover_an_independent_parity_oracle

end CubeRev029.Nineteen
