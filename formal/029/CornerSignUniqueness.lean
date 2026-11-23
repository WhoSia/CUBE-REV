import CornerPermutation
import NineteenCornerTranscript

namespace CubeRev029.Physical

/-- The actual nineteen corner-color replies determine the entire
oriented corner-coordinate assignment of any reachable cube, not merely
the colors printed at the fourteen distinct probed sticker addresses.
The chosen coordinates must correspond to the stated original coloring. -/
theorem same_nineteen_replies_force_corner_coordinates
    (s t : Coloring) (hs : Reachable s) (ht : Reachable t)
    (a b : CornerCoordinates)
    (ha : CornersAgree a s) (hb : CornersAgree b t)
    (same : scheduledCornerColors s = scheduledCornerColors t) :
    a = b := by
  have colors := same_nineteen_corner_answers_force_all_corner_colors
    s t hs ht same
  funext i
  apply cornerCyclicPair_injective
  rw [cornerCyclicPair_colors, cornerCyclicPair_colors]
  apply Prod.ext
  · exact (ha i 0).symm.trans ((colors i 0).trans (hb i 0))
  · exact (ha i 1).symm.trans ((colors i 1).trans (hb i 1))

/-- Every function on the corner coordinates, including any *specific*
permutation-sign function later defined on cornerPieceList, is constant
on the physically reachable fibers of the nineteen charged replies.
This is a conditional theorem about an explicitly supplied function;
it neither defines the parity nor grants a free parity observation. -/
theorem same_nineteen_replies_force_corner_statistic
    (s t : Coloring) (hs : Reachable s) (ht : Reachable t)
    (a b : CornerCoordinates)
    (ha : CornersAgree a s) (hb : CornersAgree b t)
    (same : scheduledCornerColors s = scheduledCornerColors t)
    (statistic : CornerCoordinates → β) :
    statistic a = statistic b := by
  rw [same_nineteen_replies_force_corner_coordinates
    s t hs ht a b ha hb same]

/-- In particular, the complete oriented corner-piece identity list
agrees, including its ordering; merely comparing multiset membership
would lose the permutation sign. -/
theorem same_nineteen_replies_force_corner_piece_order
    (s t : Coloring) (hs : Reachable s) (ht : Reachable t)
    (a b : CornerCoordinates)
    (ha : CornersAgree a s) (hb : CornersAgree b t)
    (same : scheduledCornerColors s = scheduledCornerColors t) :
    cornerPieceList a = cornerPieceList b := by
  exact congrArg cornerPieceList
    (same_nineteen_replies_force_corner_coordinates
      s t hs ht a b ha hb same)

#print axioms same_nineteen_replies_force_corner_coordinates
#print axioms same_nineteen_replies_force_corner_statistic
#print axioms same_nineteen_replies_force_corner_piece_order

end CubeRev029.Physical
