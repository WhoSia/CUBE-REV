import PhysicalPolicyCompiler
import ElevenPrefix
import EdgeSorting

namespace CubeRev029.Physical

open Eighteen

/-- Exactly the edge half of the *actual charged paired replies* at the
eleven frozen original-pose addresses, not a freely provided color oracle.
The companion corner colors are received in the same eleven frames. -/
def observedFirstElevenEdgeColors (initial : Coloring) : List Nat :=
  firstElevenPairedAddresses.map (fun q => (abstractPairRead initial q).1)

theorem observed_first_eleven_edge_color_count (initial : Coloring) :
    (observedFirstElevenEdgeColors initial).length = 11 := by
  simpa [observedFirstElevenEdgeColors] using first_eleven_address_count

/-- Total observation-to-slot lookup. The guard only supplies a default
outside the eleven actually sampled positions; the stable sorter itself
uses exactly the unique slot IDs 0 through 10. -/
def observedFirstElevenColorAt (initial : Coloring) (i : Nat) : Nat :=
  (observedFirstElevenEdgeColors initial)[i]!

/-- The original-coordinate observations themselves determine one unique
eleven-slot permutation even if first-sticker colors repeat. -/
def firstElevenObservedStableOrder (initial : Coloring) : List Nat :=
  elevenStableSlotOrder (observedFirstElevenColorAt initial)

theorem first_eleven_observed_stable_order_perm (initial : Coloring) :
    (List.range 11).Perm (firstElevenObservedStableOrder initial) := by
  exact eleven_stable_slot_order_perm (observedFirstElevenColorAt initial)

/-- Real paired-frame edge responses have a concrete, sign-certified
adjacent-swap normalization. The same trace rearranges repeated *colors*
and distinct *positions* without confusing them. The theorem is
independent of reachability and has no future-read assumptions. -/
theorem observed_paired_prefix_stable_parity_witness (initial : Coloring) :
    ∃ swaps : List Nat,
      adjTrace swaps (List.range 11) = firstElevenObservedStableOrder initial ∧
      adjTrace swaps ((List.range 11).map (observedFirstElevenColorAt initial)) =
        (firstElevenObservedStableOrder initial).map (observedFirstElevenColorAt initial) ∧
      (∀ i ∈ swaps, i < 10) ∧
      swaps.length % 2 = parity (firstElevenObservedStableOrder initial) := by
  exact eleven_stable_slot_order_certified (observedFirstElevenColorAt initial)

#print axioms observed_first_eleven_edge_color_count
#print axioms first_eleven_observed_stable_order_perm
#print axioms observed_paired_prefix_stable_parity_witness

end CubeRev029.Physical
