/-!
CUBE-REV 0.16, INTERNAL P12 — a small Boolean graph-core certificate.

The finite 17-pattern completeness premise is obtained from a separate
80-choose-5 physical-action-derived exact court; it is NOT proved by this
module. The graph lemma is independent and closes the 24-target obstruction
CONDITIONAL on that verified profile list.

STATUS: SOURCE WRITTEN; Lean compiler/kernel outcome must be witnessed before
any claim of LEAN_KERNEL_PASS. No sorry, no extra axioms.
-/
import Lean

namespace CubeRev016

/-- All light-coordinate bit patterns permitted by an exact five-word cover
of the twenty heavy targets, according to the separate finite court. -/
def p12LightProfiles : List Nat :=
  [85,90,95,102,105,119,125,153,165,170,175,187,221,235,238,245,250]

/-- Four light coordinates 1,2,4,7, corresponding to original reduced
target indices 18,29,40,49; bits sum to 150. -/
def p12Core : Nat := 150

def p12ContainsCore (mask : Nat) : Bool :=
  (Nat.testBit mask 1) && (Nat.testBit mask 2) &&
  (Nat.testBit mask 4) && (Nat.testBit mask 7)

/-- Direct Lean finite arithmetic: none of the 17 realized profiles
contains all four chosen light targets. -/
theorem p12_no_profile_contains_four_core :
    p12LightProfiles.all (fun p => !p12ContainsCore p) = true := by
  decide

/-- The ten missing-coordinate pairs of the ten six-light profiles. -/
def p12MissingEdges : List (Nat × Nat) :=
 [(5,7),(3,7),(1,7),(4,6),(2,6),(1,5),
  (2,4),(0,4),(1,3),(0,2)]

/-- The set {1,2,4,7} intersects all ten graph edges. -/
theorem p12_graph_vertex_cover :
    p12MissingEdges.all
      (fun e => Nat.testBit p12Core e.1 || Nat.testBit p12Core e.2) = true := by
  decide

/-- Four mutually disjoint edges yield the purely combinatorial
lower bound of four vertices for any vertex cover. -/
def p12PerfectMatching : List (Nat × Nat) :=
  [(5,7),(4,6),(1,3),(0,2)]

theorem p12_matching_is_in_edge_list :
    p12PerfectMatching.all (fun e => p12MissingEdges.contains e) = true := by
  decide

/-- The four matching edges exhaust the eight distinct light coordinates. -/
theorem p12_matching_covers_all_eight :
    (p12PerfectMatching.flatMap (fun e => [e.1,e.2])).mergeSort (· ≤ ·)
       = [0,1,2,3,4,5,6,7] := by
  decide

/-- Finite confirmation that no 0-, 1-, 2-, or 3-light set can block
the ten six-light patterns. The hand proof uses the perfect matching. -/
def p12HasAtMostThreeBits (t : Nat) : Bool :=
  ((List.range 8).filter (fun i => Nat.testBit t i)).length ≤ 3

theorem p12_three_light_sets_not_enough :
    (List.range 256).all (fun t =>
      (!p12HasAtMostThreeBits t) ||
      (p12LightProfiles.any (fun p =>
         ((List.range 8).all (fun i =>
           !(Nat.testBit t i) || Nat.testBit p i))))) = true := by
  decide

end CubeRev016
