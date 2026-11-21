import SignedTerminalIdentification

namespace CubeRev029.Nineteen

/-- The representative-color transcript logged by a continuation
controller executed against the actual physical paired sensor. The
logged transcript contains the representative query and relabeled reply,
while the actual query sent to the sensor is pulled back first.

The chosen color map and slot order are already fixed here; no future
reply is inspected while choosing the address. -/
def transportedSignedTranscriptPolicy
    (sigma : List Nat) (order : EdgeSlotOrder)
    (tree : Policy PairedAddress12 PairedReply12 SignedRepresentativeState) :
    Policy PairedAddress12 PairedReply12
      (List (PairedAddress12 × PairedReply12)) :=
  (tree.logged []).adapt
    (queryToOriginal order.forward)
    (responseToRepresentative sigma) (fun x => x)

/-- Logging a continuation and transporting its physical queries costs
precisely the same budget as executing the underlying policy. -/
theorem transported_signed_transcript_preserves_budget
    (sigma : List Nat) (order : EdgeSlotOrder)
    (tree : Policy PairedAddress12 PairedReply12 SignedRepresentativeState)
    {budget : Nat} (fits : Fits budget tree) :
    Fits budget (transportedSignedTranscriptPolicy sigma order tree) := by
  exact Policy.adapt_fits
    (queryToOriginal order.forward)
    (responseToRepresentative sigma) (fun x => x)
    (Policy.logged_fits fits [])

/-- For ANY adaptive continuation tree, the exact ordered
representative-address and relabeled-reply history produced by executing
its translated physical addresses is the history of running that tree on
the signed representative state.

No static query schedule is assumed and no artificial parity reply is
added. By the branch-wise proof, the next address is selected before its
reply is observed. -/
theorem transported_signed_policy_transcript_exact
    (sigma : List Nat) (hsigma : sigma ∈ symmetries)
    (order : EdgeSlotOrder) (correction : Bool)
    (state : SignedOriginalState)
    (tree : Policy PairedAddress12 PairedReply12 SignedRepresentativeState) :
    (transportedSignedTranscriptPolicy sigma order tree).run
        signedRealPairRead state =
      tree.transcript signedRepresentativePairRead
        (signedRepresentativeEncode sigma order correction state) := by
  have observeAgree :
      ∀ query : PairedAddress12,
        responseToRepresentative sigma query
          (signedRealPairRead state
            (queryToOriginal order.forward query)) =
        signedRepresentativePairRead
          (signedRepresentativeEncode sigma order correction state)
          query := by
    intro query
    exact (signed_paired_reply_equivariant
      sigma hsigma order correction state query).symm
  have sameLogged := Policy.run_fixed_reply_equiv
    (tree.logged [])
    (fun (s : SignedOriginalState) q =>
      responseToRepresentative sigma q
        (signedRealPairRead s (queryToOriginal order.forward q)))
    state
    signedRepresentativePairRead
    (signedRepresentativeEncode sigma order correction state)
    observeAgree
  simpa [transportedSignedTranscriptPolicy, Policy.adapt_run,
         Policy.logged_run] using sameLogged

#print axioms transported_signed_transcript_preserves_budget
#print axioms transported_signed_policy_transcript_exact

end CubeRev029.Nineteen
