import RepresentativeRoundTrip
import GraphPosteriorCovariance

namespace CubeRev029.Nineteen

/-- A formal parity tag is included in both the source and representative
state. It is not assumed to have already been proved equal to the physical
corner permutation sign. That separate legality link is an open gate. -/
abbrev SignedOriginalState := CubieAndCornerState × Bool
abbrev SignedRepresentativeState := RelabeledAndCornerState × Bool

/-- The correction is determined by the *observed prefix* and the chosen
color-map/slot-sort witness, never by the current or future color reply.
Here it is deliberately supplied as a fixed parameter: its cocycle formula
is another theorem obligation. -/
def signedRepresentativeEncode (sigma : List Nat) (order : EdgeSlotOrder)
    (correction : Bool) (state : SignedOriginalState) :
    SignedRepresentativeState :=
  (representativePairState sigma order.forward state.1,
    Bool.xor state.2 correction)

def signedRepresentativeDecode (sigma : List Nat) (order : EdgeSlotOrder)
    (correction : Bool) (state : SignedRepresentativeState) :
    SignedOriginalState :=
  (decodeRepresentativePairState sigma order state.1,
    Bool.xor state.2 correction)

/-- Encoding and decoding retain *both* the actual inverse cubie map and
the exact parity correction; cancellation is a genuine round trip for
every edge array and corner coloring, without assuming global cube legality. -/
theorem signed_representative_round_trip
    (sigma : List Nat) (hsigma : sigma ∈ symmetries)
    (order : EdgeSlotOrder) (correction : Bool)
    (state : SignedOriginalState) :
    signedRepresentativeDecode sigma order correction
      (signedRepresentativeEncode sigma order correction state) = state := by
  rcases state with ⟨original, bit⟩
  apply Prod.ext
  · exact representative_pair_state_round_trip sigma hsigma order original
  · cases bit <;> cases correction <;> rfl

def signedRealPairRead (state : SignedOriginalState)
    (query : PairedAddress12) : PairedReply12 :=
  realPairRead state.1 query

def signedRepresentativePairRead (state : SignedRepresentativeState)
    (query : PairedAddress12) : PairedReply12 :=
  relabeledPairRead state.1 query

/-- The parity bit is deliberately NOT an extra sensor output. Both paired
reads still reveal only one edge color and one corner color per frame. -/
theorem signed_paired_reply_equivariant
    (sigma : List Nat) (hsigma : sigma ∈ symmetries)
    (order : EdgeSlotOrder) (correction : Bool)
    (state : SignedOriginalState) (query : PairedAddress12) :
    signedRepresentativePairRead
       (signedRepresentativeEncode sigma order correction state) query =
      responseToRepresentative sigma query
        (signedRealPairRead state (queryToOriginal order.forward query)) := by
  exact paired_response_equivariant sigma hsigma order.forward state.1 query

/-- A complete policy can be transferred at the *same exact observation
budget* when its correctness on the signed normalized states is proved.
The query coordinate and response color transforms occur before branching;
the correction is fixed before this continuation starts. -/
theorem signed_original_policy_of_certified_representative
    (sigma : List Nat) (hsigma : sigma ∈ symmetries)
    (order : EdgeSlotOrder) (correction : Bool)
    (admissible : SignedOriginalState → Prop)
    (tree : Policy PairedAddress12 PairedReply12 SignedRepresentativeState)
    {budget : Nat}
    (fits : Fits budget tree)
    (certified : ∀ state, admissible state →
      tree.run signedRepresentativePairRead
        (signedRepresentativeEncode sigma order correction state) =
          signedRepresentativeEncode sigma order correction state) :
    ∃ physical : Policy PairedAddress12 PairedReply12 SignedOriginalState,
      Fits budget physical ∧ ∀ state, admissible state →
        physical.run signedRealPairRead state = state := by
  exact transport_certified_policy
    (signedRepresentativeEncode sigma order correction)
    (signedRepresentativeDecode sigma order correction)
    (queryToOriginal order.forward)
    (responseToRepresentative sigma)
    signedRealPairRead signedRepresentativePairRead
    admissible tree fits
    (by
      intro state hs q
      exact (signed_paired_reply_equivariant
        sigma hsigma order correction state q).symm)
    certified
    (by
      intro state hs
      exact signed_representative_round_trip
        sigma hsigma order correction state)

#print axioms signed_representative_round_trip
#print axioms signed_paired_reply_equivariant
#print axioms signed_original_policy_of_certified_representative

end CubeRev029.Nineteen
