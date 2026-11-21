import LegalEdgeSymmetry
import ObservationTransport

namespace CubeRev029.Nineteen

open Eighteen

/-- An edge facelet is the choice of one of twelve edge slots and one of its
two sticker sides. A complete paired read also selects a corner facelet. -/
abbrev EdgeAddress12 := Fin 12 × Bool
abbrev PairedAddress12 := EdgeAddress12 × Fin 24
abbrev PairedReply12 := Nat × Nat

/-- Genuine cubie identities and orientation are recorded in Fin 24.
The second component records the 24 original-pose corner sticker colors.
Neither representation assumes that the cube has already been reconstructed. -/
abbrev CubieAndCornerState := (Fin 12 → Fin 24) × (Fin 24 → Nat)
abbrev RelabeledAndCornerState := (Fin 12 → Nat) × (Fin 24 → Nat)

def realPairRead (s : CubieAndCornerState) (q : PairedAddress12) :
    PairedReply12 :=
  (sticker (s.1 q.1.1).val q.1.2, s.2 q.2)

def relabeledPairRead (s : RelabeledAndCornerState) (q : PairedAddress12) :
    PairedReply12 :=
  (sticker (s.1 q.1.1) q.1.2, s.2 q.2)

/-- Only the edge position gets reindexed; the corner address is unchanged.
The selected address is fixed before the paired reply is received. -/
def queryToOriginal (order : Fin 12 → Fin 12) (q : PairedAddress12) :
    PairedAddress12 :=
  ((order q.1.1, q.1.2), q.2)

def responseToRepresentative (sigma : List Nat) (_ : PairedAddress12)
    (response : PairedReply12) : PairedReply12 :=
  (sigma[response.1]!, response.2)

/-- Transport the actual initial edge cubies through a chosen color
relabeling and a chosen permutation of edge positions, while retaining
the initial corner colors unchanged for the terminal parity decoder. -/
def representativePairState (sigma : List Nat) (order : Fin 12 → Fin 12)
    (s : CubieAndCornerState) : RelabeledAndCornerState :=
  (fun i => relabelEdgeValue sigma (s.1 (order i)).val, s.2)

/-- Universal same-frame equivariance of paired edge/corner observations.
The corner reply is unchanged; the edge reply is relabeled. It holds even
before imposing the legality constraints on the twelve cubies. -/
theorem paired_response_equivariant
    (sigma : List Nat) (hsigma : sigma ∈ symmetries)
    (order : Fin 12 → Fin 12) (s : CubieAndCornerState)
    (q : PairedAddress12) :
    relabeledPairRead (representativePairState sigma order s) q =
      responseToRepresentative sigma q (realPairRead s (queryToOriginal order q)) := by
  rcases s with ⟨pieces, corners⟩
  rcases q with ⟨⟨index, side⟩, corner⟩
  apply Prod.ext
  · exact symmetry_relabelEdgeValue_responses sigma hsigma
      (pieces (order index)).val (pieces (order index)).isLt side
  · rfl

/-- The actual address/reply adapter. A representative policy may branch
on previous paired colors; the corresponding real address is chosen before
the current frame's colors are returned. -/
def transportPairedPolicy {OutRep OutReal : Type}
    (sigma : List Nat) (order : Fin 12 → Fin 12)
    (decode : OutRep → OutReal)
    (tree : Policy PairedAddress12 PairedReply12 OutRep) :
    Policy PairedAddress12 PairedReply12 OutReal :=
  tree.adapt (queryToOriginal order) (responseToRepresentative sigma) decode

theorem transportPairedPolicy_fits
    {OutRep OutReal : Type} (sigma : List Nat) (order : Fin 12 → Fin 12)
    (decode : OutRep → OutReal)
    {budget : Nat} {tree : Policy PairedAddress12 PairedReply12 OutRep}
    (fit : Fits budget tree) :
    Fits budget (transportPairedPolicy sigma order decode tree) := by
  exact Policy.adapt_fits (queryToOriginal order)
    (responseToRepresentative sigma) decode fit

/-- Concrete instance of AC's generic response-equivariant policy transport:
the paired real-state run is exactly the representative run followed by the
provided inverse-output decoder. No assumptions about any precomputed tree,
response branch or particular legal scramble are hidden in this theorem. -/
theorem transportPairedPolicy_run
    {OutRep OutReal : Type} (sigma : List Nat) (hsigma : sigma ∈ symmetries)
    (order : Fin 12 → Fin 12) (decode : OutRep → OutReal)
    (tree : Policy PairedAddress12 PairedReply12 OutRep)
    (state : CubieAndCornerState) :
    (transportPairedPolicy sigma order decode tree).run realPairRead state =
      decode (tree.run relabeledPairRead
        (representativePairState sigma order state)) := by
  have equivalent := Policy.run_fixed_reply_equiv tree
    (fun (s : CubieAndCornerState) q =>
      responseToRepresentative sigma q
        (realPairRead s (queryToOriginal order q))) state
    relabeledPairRead (representativePairState sigma order state)
    (by
      intro q
      exact (paired_response_equivariant sigma hsigma order state q).symm)
  change (tree.adapt (queryToOriginal order)
      (responseToRepresentative sigma) decode).run realPairRead state =
    decode (tree.run relabeledPairRead
      (representativePairState sigma order state))
  calc
    (tree.adapt (queryToOriginal order)
        (responseToRepresentative sigma) decode).run realPairRead state =
      decode (tree.run
        (fun (s : CubieAndCornerState) q =>
          responseToRepresentative sigma q
            (realPairRead s (queryToOriginal order q))) state) := by
          exact Policy.adapt_run (queryToOriginal order)
            (responseToRepresentative sigma) decode realPairRead state tree
    _ = _ := congrArg decode equivalent

#print axioms paired_response_equivariant
#print axioms transportPairedPolicy_fits
#print axioms transportPairedPolicy_run

end CubeRev029.Nineteen
