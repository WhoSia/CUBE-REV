import CornerSignUniqueness

namespace CubeRev029.Physical

open CubeRev029.Eighteen

/-- An explicit Nat-valued physical corner permutation parity, computed
from the ORDERED eight corner-piece identities in initial-pose positions.
The projection forgets cubie twist but retains the positional permutation.
On physically reachable cubes, CornerPermutation.reachable_has_permutation_corners
supplies the requisite complete permutation of all eight identities. -/
def cornerPermutationParity (a : CornerCoordinates) : Nat :=
  parity ((cornerPieceList a).map Fin.val)

/-- The concrete corner-permutation parity is independent of which
coordinate witness represents a given original reachable coloring.
This prevents accidentally treating a noncanonical coordinate witness
as a hidden extra sign observation. -/
theorem corner_permutation_parity_witness_independent
    (s : Coloring) (hs : Reachable s)
    (a b : CornerCoordinates)
    (ha : CornersAgree a s) (hb : CornersAgree b s) :
    cornerPermutationParity a = cornerPermutationParity b := by
  have eq := same_nineteen_replies_force_corner_coordinates
    s s hs hs a b ha hb rfl
  rw [eq]

/-- The actual nineteen charged corner replies determine the concrete
corner permutation parity of any corresponding physically reachable
coordinate witnesses. No corner parity oracle occurs in the assumptions. -/
theorem corner_permutation_parity_from_nineteen_replies
    (s t : Coloring) (hs : Reachable s) (ht : Reachable t)
    (a b : CornerCoordinates)
    (ha : CornersAgree a s) (hb : CornersAgree b t)
    (same : scheduledCornerColors s = scheduledCornerColors t) :
    cornerPermutationParity a = cornerPermutationParity b := by
  exact same_nineteen_replies_force_corner_statistic
    s t hs ht a b ha hb same cornerPermutationParity

/-- The actual sign is a Boolean (0 = even, 1 = odd) and is determined
by the very same nineteen corner replies, not a separately read bit. -/
def cornerPermutationOdd (a : CornerCoordinates) : Bool :=
  cornerPermutationParity a == 1

theorem corner_permutation_odd_from_nineteen_replies
    (s t : Coloring) (hs : Reachable s) (ht : Reachable t)
    (a b : CornerCoordinates)
    (ha : CornersAgree a s) (hb : CornersAgree b t)
    (same : scheduledCornerColors s = scheduledCornerColors t) :
    cornerPermutationOdd a = cornerPermutationOdd b := by
  unfold cornerPermutationOdd
  rw [corner_permutation_parity_from_nineteen_replies
    s t hs ht a b ha hb same]

#print axioms corner_permutation_parity_witness_independent
#print axioms corner_permutation_parity_from_nineteen_replies
#print axioms corner_permutation_odd_from_nineteen_replies

end CubeRev029.Physical
