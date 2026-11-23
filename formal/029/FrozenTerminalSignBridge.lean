import ObservedTerminalParity
import FiftyTwoRootReceipt

namespace CubeRev029.Nineteen

open CubeRev029.Eighteen
open CubeRev029.Physical

set_option autoImplicit false

/-- The exact missing semantic interface between an ORIGINAL physical
edge permutation, its corner permutation, and the frozen representative
word. The two equalities are *named obligations*, not properties inferred
from an arbitrary word or an arbitrary corner-coordinate assignment.

(1) legalCoupling is the physical edge/corner permutation-parity law.
(2) transportedParity is the signed normalization identity for the
actually chosen first-eleven prefix correction.
Neither is a free observation of a sign. -/
theorem normalized_edge_sign_matches_observed_corner_sign
    (firstElevenReplies : List FrameColor)
    (originalWord normalizedWord : Word)
    (corners : CornerCoordinates)
    (legalCoupling :
      parity (originalWord.map (· / 2)) =
        cornerPermutationParity corners)
    (transportedParity :
      parity (normalizedWord.map (· / 2)) =
        (parity (originalWord.map (· / 2)) +
          frozenPrefixSignCorrection firstElevenReplies) % 2) :
    edgeWordSign normalizedWord =
      (observedTerminalCorrectedParity firstElevenReplies corners == 1) := by
  unfold edgeWordSign observedTerminalCorrectedParity correctedCornerParity
  rw [transportedParity, legalCoupling]

/-- A real frozen certificate entry's sign-indexed *eight-read* decoder
recovers a normalized candidate using the sign determined by the paid
corner observations and past prefix correction, PROVIDED that:

* the immutable JSON entry is a member of the accepted source;
* the normalized candidate belongs to its exactly parsed belief;
* the physical parity-coupling and actual normalization parity identities
  have been proved separately.

Those obligations remain explicit. This does not build a total root
selector or prove the existence of a computable corner-coordinate decoder
from observed sticker colors. -/
theorem frozen_root_recovers_with_observed_corner_sign
    (roots : Array Lean.Json)
    (parsed : parsedRepresentativeArray
      (include_str "upper-policy-certificate.json") = .ok roots)
    (entry : Lean.Json) (member : entry ∈ roots.toList)
    (graph : Array (FrozenInstruction Nat Nat Unit))
    (belief : List Word)
    (entryParsed : parseRepresentativeRoot entry = .ok (graph, belief))
    (originalWord normalizedWord : Word)
    (candidate : normalizedWord ∈ belief)
    (firstElevenReplies : List FrameColor)
    (corners : CornerCoordinates)
    (legalCoupling :
      parity (originalWord.map (· / 2)) =
        cornerPermutationParity corners)
    (transportedParity :
      parity (normalizedWord.map (· / 2)) =
        (parity (originalWord.map (· / 2)) +
          frozenPrefixSignCorrection firstElevenReplies) % 2) :
    ((exactEightSectorPolicy 0 graph observation edgeWordSign 0 belief).run
        observation normalizedWord)
        (observedTerminalCorrectedParity firstElevenReplies corners == 1) =
      some normalizedWord := by
  obtain ⟨g, b, matching, recovers⟩ :=
    every_actual_frozen_root_recovers roots parsed entry member
  have same : (graph, belief) = (g, b) := by
    have h : Except.ok (graph, belief) = Except.ok (g, b) :=
      entryParsed.symm.trans matching
    injection h
  rcases Prod.mk.inj same with ⟨sameGraph, sameBelief⟩
  subst g
  subst b
  rw [← normalized_edge_sign_matches_observed_corner_sign
    firstElevenReplies originalWord normalizedWord corners
    legalCoupling transportedParity]
  exact recovers normalizedWord candidate

#print axioms normalized_edge_sign_matches_observed_corner_sign
#print axioms frozen_root_recovers_with_observed_corner_sign

end CubeRev029.Nineteen
