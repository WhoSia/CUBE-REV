import SignedRepresentativePolicy

namespace CubeRev029.Nineteen

/-- This observation is asked at a representative-coordinate address, but
it uses exactly one original physical edge/corner probe and relabels the
returned edge color. No extra oracle supplies the parity tag. -/
def signedOriginalReadInRepresentativeCoordinates
    (sigma : List Nat) (order : EdgeSlotOrder)
    (state : SignedOriginalState) (query : PairedAddress12) :
    PairedReply12 :=
  responseToRepresentative sigma query
    (signedRealPairRead state (queryToOriginal order.forward query))

theorem signed_observations_match
    (sigma : List Nat) (hsigma : sigma ∈ symmetries)
    (order : EdgeSlotOrder) (correction : Bool)
    (state : SignedOriginalState) (query : PairedAddress12) :
    signedRepresentativePairRead
       (signedRepresentativeEncode sigma order correction state) query =
      signedOriginalReadInRepresentativeCoordinates sigma order state query := by
  exact signed_paired_reply_equivariant
    sigma hsigma order correction state query

/-- The signed normalizer is injective because its inverse (including
parity correction and the edge-slot inverse) is actually constructed. -/
theorem signed_representative_encode_injective
    (sigma : List Nat) (hsigma : sigma ∈ symmetries)
    (order : EdgeSlotOrder) (correction : Bool) :
    Function.Injective
      (signedRepresentativeEncode sigma order correction) := by
  intro left right equality
  have inverseEquality := congrArg
    (signedRepresentativeDecode sigma order correction) equality
  simpa [signed_representative_round_trip
    sigma hsigma order correction left,
    signed_representative_round_trip
    sigma hsigma order correction right] using inverseEquality

/-- Exact equality of the *sets* of possible remaining signed states after
a single query and its reply, not merely equality of their cardinalities.
All replies remain categorical paired sticker colors. -/
theorem signed_paired_posterior_one_step
    (sigma : List Nat) (hsigma : sigma ∈ symmetries)
    (order : EdgeSlotOrder) (correction : Bool)
    (belief : SignedOriginalState → Prop)
    (query : PairedAddress12) (reply : PairedReply12) :
    transportedBelief (signedRepresentativeEncode sigma order correction)
      (posterior
        (signedOriginalReadInRepresentativeCoordinates sigma order)
        belief query reply) =
    posterior signedRepresentativePairRead
      (transportedBelief (signedRepresentativeEncode sigma order correction)
        belief) query reply := by
  exact transported_posterior_covariance
    (signedRepresentativeEncode sigma order correction)
    (fun q : PairedAddress12 => q)
    (fun r : PairedReply12 => r)
    (by intro a b h; exact h)
    (signedOriginalReadInRepresentativeCoordinates sigma order)
    signedRepresentativePairRead
    (signed_observations_match sigma hsigma order correction)
    belief query reply

/-- A transcript is the exact ordered list of pairs of query addresses and
responses. Unlike a histogram, it retains order, causal response labels
and the distinction between edge and corner addresses. -/
def beliefAfterTranscript
    {S Q R : Type}
    (observe : S → Q → R) (belief : S → Prop) :
    List (Q × R) → S → Prop
  | [] => belief
  | (query, reply) :: tail =>
      beliefAfterTranscript observe
        (posterior observe belief query reply) tail

/-- All-history signed bisimulation: the normalized posterior after ANY
finite ordered transcript equals the transported original posterior.

The theorem is parametric in the correction bit, but fixes that bit before
the history begins. To apply it to the actual nineteen-frame strategy,
the selected gauge and its computed correction must be proved determined
from the preceding eleven observations. -/
theorem signed_paired_posterior_all_histories
    (sigma : List Nat) (hsigma : sigma ∈ symmetries)
    (order : EdgeSlotOrder) (correction : Bool)
    (belief : SignedOriginalState → Prop)
    (history : List (PairedAddress12 × PairedReply12)) :
    transportedBelief (signedRepresentativeEncode sigma order correction)
      (beliefAfterTranscript
        (signedOriginalReadInRepresentativeCoordinates sigma order)
        belief history) =
    beliefAfterTranscript signedRepresentativePairRead
      (transportedBelief (signedRepresentativeEncode sigma order correction)
        belief) history := by
  induction history generalizing belief with
  | nil => rfl
  | cons entry tail ih =>
      rcases entry with ⟨query, reply⟩
      change
        transportedBelief (signedRepresentativeEncode sigma order correction)
          (beliefAfterTranscript
            (signedOriginalReadInRepresentativeCoordinates sigma order)
            (posterior
              (signedOriginalReadInRepresentativeCoordinates sigma order)
              belief query reply) tail) =
        beliefAfterTranscript signedRepresentativePairRead
          (posterior signedRepresentativePairRead
            (transportedBelief
              (signedRepresentativeEncode sigma order correction)
              belief) query reply) tail
      rw [ih (posterior
        (signedOriginalReadInRepresentativeCoordinates sigma order)
        belief query reply)]
      rw [signed_paired_posterior_one_step
        sigma hsigma order correction belief query reply]

/-- A genuinely distinct pair of signed possible initial states remains
distinct in representative coordinates. This prevents a quotient proof from
silently merging two opposing terminal parity hypotheses. -/
theorem signed_ambiguity_survives_normalization
    (sigma : List Nat) (hsigma : sigma ∈ symmetries)
    (order : EdgeSlotOrder) (correction : Bool)
    (belief : SignedOriginalState → Prop)
    (ambiguous : Ambiguous belief) :
    Ambiguous
      (transportedBelief
        (signedRepresentativeEncode sigma order correction) belief) := by
  exact transported_belief_preserves_ambiguity
    (signedRepresentativeEncode sigma order correction)
    (signed_representative_encode_injective
      sigma hsigma order correction) belief ambiguous

#print axioms signed_representative_encode_injective
#print axioms signed_paired_posterior_one_step
#print axioms signed_paired_posterior_all_histories
#print axioms signed_ambiguity_survives_normalization

end CubeRev029.Nineteen
