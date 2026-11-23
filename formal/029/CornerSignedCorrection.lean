import CornerPermutationSign

namespace CubeRev029.Physical

/-- The terminal representative sign requires the physical corner
permutation parity PLUS the explicitly retained original-prefix
position/color-gauge correction. This is only the algebraic sign
interface; it does not assert the required correction was successfully
chosen from every first-eleven physical prefix. -/
def correctedCornerParity (a : CornerCoordinates)
    (prefixCorrection : Nat) : Nat :=
  (cornerPermutationParity a + prefixCorrection) % 2

/-- If the first-eleven transcript has fixed the *same* correction for
both physically reachable candidate states, equality of the charged
nineteen corner responses forces equality of their corrected terminal
signs. The correction is a prior observation-derived parameter, not a
newly observed sign bit. -/
theorem corrected_corner_parity_from_past_and_nineteen_replies
    (s t : Coloring) (hs : Reachable s) (ht : Reachable t)
    (a b : CornerCoordinates)
    (ha : CornersAgree a s) (hb : CornersAgree b t)
    (sameCorner : scheduledCornerColors s = scheduledCornerColors t)
    (correction : Nat) :
    correctedCornerParity a correction =
      correctedCornerParity b correction := by
  unfold correctedCornerParity
  rw [corner_permutation_parity_from_nineteen_replies
    s t hs ht a b ha hb sameCorner]

/-- The correction need not be assumed numerically identical: it
suffices that it was calculated identically from the same past replies.
A future integration theorem must instantiate the two corrections
using the *actual* total prefix-normalization selector. -/
theorem corrected_corner_parity_respects_equal_prefix_corrections
    (s t : Coloring) (hs : Reachable s) (ht : Reachable t)
    (a b : CornerCoordinates)
    (ha : CornersAgree a s) (hb : CornersAgree b t)
    (sameCorner : scheduledCornerColors s = scheduledCornerColors t)
    (correctionS correctionT : Nat)
    (sameCorrection : correctionS = correctionT) :
    correctedCornerParity a correctionS =
      correctedCornerParity b correctionT := by
  subst correctionT
  exact corrected_corner_parity_from_past_and_nineteen_replies
    s t hs ht a b ha hb sameCorner correctionS

#print axioms corrected_corner_parity_from_past_and_nineteen_replies
#print axioms corrected_corner_parity_respects_equal_prefix_corrections

end CubeRev029.Physical
