import PhysicalPolicyCompiler
import ElevenPrefix
import EdgeSorting
import ColorGraphCharacter
import PairedPolicyTransport
import RepresentativeRoundTrip

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

/-- The corner component of the *same eleven charged paired replies*
is exactly the fixed first-eleven corner schedule. Sorting the edge
position labels does not grant free or reordered corner observations. -/
def observedFirstElevenCornerColors (initial : Coloring) : List Nat :=
  firstElevenPairedAddresses.map (fun q => (abstractPairRead initial q).2)

theorem observed_first_eleven_corner_clock_exact (initial : Coloring) :
    observedFirstElevenCornerColors initial =
      (cornerFrameAddresses.take 11).map (fun c => initial (cornerSlot c)) := by
  calc
    observedFirstElevenCornerColors initial =
        (firstElevenPairedAddresses.map Prod.snd).map
          (fun c => initial (cornerSlot c)) := by
            simp [observedFirstElevenCornerColors, List.map_map, abstractPairRead]
    _ = (cornerFrameAddresses.take 11).map
          (fun c => initial (cornerSlot c)) := by
            rw [first_eleven_matches_frozen_corner_schedule]

#print axioms observed_first_eleven_corner_clock_exact

/-- Normalization is a function of the transcript returned by the first
eleven paired reads, without access to the unknown cube state. -/
def prefixTranscriptStableOrder (replies : List FrameColor) : List Nat :=
  elevenStableSlotOrder (fun i => (replies.map Prod.fst)[i]!)

theorem actual_prefix_transcript_determines_stable_order
    (initial : Coloring) :
    prefixTranscriptStableOrder
      (firstElevenPairedAddresses.map (abstractPairRead initial)) =
      firstElevenObservedStableOrder initial := by
  simp only [prefixTranscriptStableOrder, firstElevenObservedStableOrder,
    observedFirstElevenColorAt, observedFirstElevenEdgeColors,
    List.map_map]
  rfl

/-- This instantiated form of the general prefix-policy theorem rules out
choosing an eight-read continuation from any later paired reply. -/
theorem paired_prefix_run_uses_only_received_eleven_replies
    (initial : Coloring)
    (next : List FrameColor →
      Policy (Fin 24 × Fin 24) FrameColor Coloring) :
    (Policy.withPrefix firstElevenPairedAddresses [] next).run
      abstractPairRead initial =
      (next (firstElevenPairedAddresses.map (abstractPairRead initial))).run
        abstractPairRead initial := by
  simpa using (Policy.withPrefix_run abstractPairRead initial
    firstElevenPairedAddresses ([] : List FrameColor) next)

/-- The chosen order of the real eleven edge replies satisfies the total
lexicographic comparison, including the original-slot tie break. -/
theorem observed_paired_prefix_sorted (initial : Coloring) :
    List.Pairwise
      (fun i j =>
        elevenSlotLexLE (observedFirstElevenColorAt initial) i j = true)
      (firstElevenObservedStableOrder initial) := by
  exact eleven_stable_slot_order_sorted (observedFirstElevenColorAt initial)

#print axioms actual_prefix_transcript_determines_stable_order
#print axioms paired_prefix_run_uses_only_received_eleven_replies
#print axioms observed_paired_prefix_sorted

/-- The histogram resulting from applying a legal color table to the
actual first-eleven edge answers. Each candidate is one of the 48 allowed
opposite-color-pair symmetries, not a physical cube rotation. -/
def prefixGaugeHistogram (edgeReplies : List Nat)
    (sigma : List Nat) : List Nat :=
  Nineteen.counts (edgeReplies.map (fun c => sigma[c]!))

/-- The frozen Python policy enumerates permutations of URFDLB,
not permutations of the internal BDFLRU color-code indices. We map each
image tuple back to an array indexed by the actual internal color code.
This explicit enumeration order matters whenever multiple mappings tie
for the lexicographically least representative histogram. -/
def frozenRouteOrderedColorMaps : List (List Nat) :=
  ((Nineteen.permutationsOf Nineteen.collation 6).map
    (fun images => (List.range 6).map
      (fun code => images[Nineteen.collation.idxOf code]!))).filter
    (fun sigma => (List.range 6).all
      (fun code =>
        sigma[Nineteen.opposite code]! ==
          Nineteen.opposite sigma[code]!))

/-- Every reconstructed table is a member of the same finite 48-element
opposite-pair-preserving color action already certified by Lean. -/
theorem frozen_route_ordered_maps_legal :
    ∀ sigma ∈ frozenRouteOrderedColorMaps,
      sigma ∈ Nineteen.symmetries := by
  decide +kernel

theorem frozen_route_ordered_maps_have_48_members :
    frozenRouteOrderedColorMaps.length = 48 := by
  decide +kernel

/-- Python's first enumeration candidate is the identity mapping. Hence
starting the strict-improvement fold at identity reproduces the
first-minimum tie rule of route_info, rather than preferring an
arbitrarily positioned identity candidate at a later tie. -/
theorem frozen_route_order_starts_with_identity :
    frozenRouteOrderedColorMaps.head? = some (List.range 6) := by
  decide +kernel

/-- Each candidate carries a proof of membership in the allowed 48.
The explicit URFDLB iteration order is essential to match the frozen
route_info implementation on histograms with tied minimizers. -/
def choosePrefixGauge (replies : List FrameColor) :
    {sigma : List Nat // sigma ∈ Nineteen.symmetries} :=
  (frozenRouteOrderedColorMaps.attach.map
    (fun candidate =>
      (⟨candidate.val,
        frozen_route_ordered_maps_legal candidate.val candidate.property⟩ :
        {sigma : List Nat // sigma ∈ Nineteen.symmetries}))).foldl
    (fun best candidate =>
      if Nineteen.lexLess
          (prefixGaugeHistogram (replies.map Prod.fst) candidate.val)
          (prefixGaugeHistogram (replies.map Prod.fst) best.val)
      then candidate else best)
    ⟨List.range 6, by decide +kernel⟩

/-- Concrete adversarial tie regression: color histogram
(U,R,F,D,L,B) = (2,4,0,0,3,2). An internal-code ordered fold chooses a
DIFFERENT legal mapping, whose combined parity can also change. The
frozen-order selector must use the exact original route_info map. -/
def frozenTieProbeReplies : List FrameColor :=
  ([5,5,4,4,4,4,3,3,3,0,0] : List Nat).map (fun c => (c, 0))

theorem frozen_tie_probe_selects_original_route_map :
    (choosePrefixGauge frozenTieProbeReplies).val =
      [3,5,4,2,0,1] := by
  decide +kernel

#print axioms frozen_route_ordered_maps_legal
#print axioms frozen_route_ordered_maps_have_48_members
#print axioms frozen_route_order_starts_with_identity
#print axioms frozen_tie_probe_selects_original_route_map

def chosenPrefixColorMap (replies : List FrameColor) : List Nat :=
  (choosePrefixGauge replies).val

theorem chosen_prefix_color_map_legal (replies : List FrameColor) :
    chosenPrefixColorMap replies ∈ Nineteen.symmetries :=
  (choosePrefixGauge replies).property

/-- The *observed* prefix fixes an allowed relabeling. In particular the
candidate map preserves every oriented edge sticker response, and its
orientation offsets sum to an even number. The exact signed sorting
cocycle and representative-tree statewise correctness remain separate. -/
theorem chosen_prefix_gauge_edge_equivariant (replies : List FrameColor) :
    ∀ edge : Fin 24, ∀ side : Bool,
      sticker
          (Nineteen.relabeledOrientedEdge (chosenPrefixColorMap replies) edge)
          side =
        (chosenPrefixColorMap replies)[sticker edge.val side]! := by
  exact Nineteen.symmetry_preserves_oriented_edge_colors
    (chosenPrefixColorMap replies) (chosen_prefix_color_map_legal replies)

theorem chosen_prefix_gauge_even_flip_offset (replies : List FrameColor) :
    (((List.range 12).map
      (Nineteen.relabeledEdgeSwap (chosenPrefixColorMap replies))).sum % 2) = 0 := by
  exact Nineteen.symmetry_even_flip_offset
    (chosenPrefixColorMap replies) (chosen_prefix_color_map_legal replies)

#print axioms chosen_prefix_color_map_legal
#print axioms chosen_prefix_gauge_edge_equivariant
#print axioms chosen_prefix_gauge_even_flip_offset

/-- The color gauge is computed from edge colors only. Even if the
first eleven corner replies differ, an identical ordered edge transcript
selects the same exact proof-carrying symmetry table. -/
theorem chosen_prefix_gauge_ignores_corner_replies
    (first second : List FrameColor)
    (sameEdges : first.map Prod.fst = second.map Prod.fst) :
    chosenPrefixColorMap first = chosenPrefixColorMap second := by
  unfold chosenPrefixColorMap choosePrefixGauge
  rw [sameEdges]

/-- The 12-edge permutation sign induced by the SELECTED color map equals
the sign of the three opposite-pair blocks. This specializes the existing
48-symmetry character theorem to a deterministic actual-prefix gauge and
does not silently replace it with the (different) stable-sort parity. -/
theorem chosen_prefix_gauge_sign_character (replies : List FrameColor) :
    parity (Nineteen.inducedTwelveEdgePermutation
      (chosenPrefixColorMap replies)) =
    parity (Nineteen.inducedThreePairPermutation
      (chosenPrefixColorMap replies)) := by
  exact Nineteen.induced_edge_sign_is_three_pair_sign
    (chosenPrefixColorMap replies) (chosen_prefix_color_map_legal replies)

/-- If two original cube states return exactly the same eleven initial
edge colors at the paired addresses, they select identical color gauges,
irrespective of the corner transcripts or subsequent queries. -/
theorem same_actual_edge_prefix_selects_same_color_gauge
    (first second : Coloring)
    (sameEdges : observedFirstElevenEdgeColors first =
      observedFirstElevenEdgeColors second) :
    chosenPrefixColorMap
      (firstElevenPairedAddresses.map (abstractPairRead first)) =
    chosenPrefixColorMap
      (firstElevenPairedAddresses.map (abstractPairRead second)) := by
  apply chosen_prefix_gauge_ignores_corner_replies
  simpa [observedFirstElevenEdgeColors, List.map_map] using sameEdges

#print axioms chosen_prefix_gauge_ignores_corner_replies
#print axioms chosen_prefix_gauge_sign_character
#print axioms same_actual_edge_prefix_selects_same_color_gauge

/-- The SAME transcript-selected legal gauge is a valid adapter for
each current simultaneous edge-and-corner observation. The corner response
is unchanged and no extra sign bit is exposed as a sensor reply. -/
theorem chosen_gauge_paired_response_transport
    (replies : List FrameColor)
    (order : Fin 12 → Fin 12)
    (state : Nineteen.CubieAndCornerState)
    (query : Nineteen.PairedAddress12) :
    Nineteen.relabeledPairRead
      (Nineteen.representativePairState
        (chosenPrefixColorMap replies) order state) query =
    Nineteen.responseToRepresentative
      (chosenPrefixColorMap replies) query
      (Nineteen.realPairRead state
        (Nineteen.queryToOriginal order query)) := by
  exact Nineteen.paired_response_equivariant
    (chosenPrefixColorMap replies)
    (chosen_prefix_color_map_legal replies) order state query

/-- Any continuation transferred with this already-received color gauge
has exactly the same worst-case number of charged paired reads. This is a
conditional theorem about an arbitrary provided continuation tree. -/
theorem chosen_gauge_paired_transport_fits
    {OutputRep OutputOriginal : Type}
    (replies : List FrameColor) (order : Fin 12 → Fin 12)
    (decode : OutputRep → OutputOriginal)
    {budget : Nat}
    {tree : Policy Nineteen.PairedAddress12
      Nineteen.PairedReply12 OutputRep}
    (fits : Fits budget tree) :
    Fits budget
      (Nineteen.transportPairedPolicy
        (chosenPrefixColorMap replies) order decode tree) := by
  exact Nineteen.transportPairedPolicy_fits
    (chosenPrefixColorMap replies) order decode fits

/-- The selected gauge is not only a relabeling of stored state arrays:
every adaptive branch of any given representative paired policy is
transported back to the real paired response game. Correctness of a
concrete frozen representative tree remains an independent obligation. -/
theorem chosen_gauge_paired_transport_run
    {OutputRep OutputOriginal : Type}
    (replies : List FrameColor) (order : Fin 12 → Fin 12)
    (decode : OutputRep → OutputOriginal)
    (tree : Policy Nineteen.PairedAddress12
      Nineteen.PairedReply12 OutputRep)
    (state : Nineteen.CubieAndCornerState) :
    (Nineteen.transportPairedPolicy
       (chosenPrefixColorMap replies) order decode tree).run
         Nineteen.realPairRead state =
      decode (tree.run Nineteen.relabeledPairRead
        (Nineteen.representativePairState
          (chosenPrefixColorMap replies) order state)) := by
  exact Nineteen.transportPairedPolicy_run
    (chosenPrefixColorMap replies)
    (chosen_prefix_color_map_legal replies) order decode tree state

#print axioms chosen_gauge_paired_response_transport
#print axioms chosen_gauge_paired_transport_fits
#print axioms chosen_gauge_paired_transport_run

/-- The chosen prefix gauge has an actual inverse in the same
48-element automorphism family, not an unverified inverse table. -/
theorem chosen_prefix_gauge_inverse_is_legal (replies : List FrameColor) :
    Nineteen.inverseColorTable (chosenPrefixColorMap replies) ∈
      Nineteen.symmetries := by
  exact Nineteen.inverse_color_table_is_symmetry
    (chosenPrefixColorMap replies) (chosen_prefix_color_map_legal replies)

/-- The inverse of the selected table restores each oriented edge
identity, including its sticker-side orientation. This remains valid for
every possible past reply list, including unreachable transcripts. -/
theorem chosen_prefix_gauge_restores_oriented_edge
    (replies : List FrameColor) (edge : Fin 24) :
    Nineteen.relabelEdgeValue
      (Nineteen.inverseColorTable (chosenPrefixColorMap replies))
      (Nineteen.relabelEdgeValue
        (chosenPrefixColorMap replies) edge.val) = edge.val := by
  exact Nineteen.inverse_color_table_restores_oriented_edge
    (chosenPrefixColorMap replies) (chosen_prefix_color_map_legal replies) edge

/-- The concrete chosen gauge composes with ANY separately justified
twelve-slot position permutation to round-trip the original paired
edge/corner state. This guarantees original-coordinate recovery once a
valid representative output has been obtained; it does NOT establish
correctness of a frozen representative decision tree. -/
theorem chosen_gauge_original_state_round_trip
    (replies : List FrameColor)
    (order : Nineteen.EdgeSlotOrder)
    (state : Nineteen.CubieAndCornerState) :
    Nineteen.decodeRepresentativePairState
      (chosenPrefixColorMap replies) order
      (Nineteen.representativePairState
        (chosenPrefixColorMap replies) order.forward state) = state := by
  exact Nineteen.representative_pair_state_round_trip
    (chosenPrefixColorMap replies)
    (chosen_prefix_color_map_legal replies) order state

#print axioms chosen_prefix_gauge_inverse_is_legal
#print axioms chosen_prefix_gauge_restores_oriented_edge
#print axioms chosen_gauge_original_state_round_trip






#print axioms observed_first_eleven_edge_color_count
#print axioms first_eleven_observed_stable_order_perm
#print axioms observed_paired_prefix_stable_parity_witness

end CubeRev029.Physical
