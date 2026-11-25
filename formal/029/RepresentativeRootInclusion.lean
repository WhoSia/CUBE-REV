import RepresentativeCoverage
import ExecutablePhysicalSignHandoff
import FiftyTwoRootReceipt
import TaggedNineteenRootPolicy

namespace CubeRev029.Nineteen

open Eighteen CubeRev029.Physical

set_option autoImplicit false
set_option maxRecDepth 16000
set_option maxHeartbeats 0

/-!
# BS-3: universal representative-root inclusion

Chosen method (finite inclusion check on PRODUCTION code, not HashSet/forIn
semantics): `coverageCheck` replays the executable gauge + stable sort on
every raw row of the omitted-edge enumeration and requires an exact
certificate prefix. It is proved by ONE additional `native_decide` on the
same SHA-256-pinned JSON. All universal reasoning (rows cover every legal
word, permutation invariance of the gauge and of the sorted prefix) is
kernel-checked below.
-/

/-- All raw first-eleven rows: the exact family `representativeVectors` counts. -/
def rawRows : List (List Nat) :=
  (List.range 12).flatMap fun o => rawWords ((List.range 12).erase o)

/-- The sorted, gauge-normalized first-eleven colors the production
normalizer exposes (stable order of the chosen map's colors). -/
def normalizedPrefix (replies : List FrameColor) : List Nat :=
  (frozenPrefixStableOrder replies).map fun i =>
    (chosenPrefixColorMap replies)[(replies.map Prod.fst)[i]!]!

def rowReplies (row : List Nat) : List FrameColor := row.map fun c => (c, 0)

def coverageCheck (source : String) : Bool :=
  match parsedRepresentativeArray source with
  | .ok roots => rawRows.all fun row => roots.toList.any fun entry =>
      rootFirstColors entry == some (normalizedPrefix (rowReplies row))
  | .error _ => false

/-- NEW native_decide (trust boundary: same immutable JSON as the existing
52-root receipt; evaluates only the Boolean above). -/
theorem representative_prefixes_covered_source :
    coverageCheck (include_str "upper-policy-certificate.json") = true := by
  native_decide

theorem symmetry_color_mem :
    ∀ sigma ∈ symmetries, ∀ c ∈ collation, sigma[c]! ∈ collation := by
  decide +kernel

theorem collation_idx_injective :
    ∀ a ∈ collation, ∀ b ∈ collation,
      collation.idxOf a = collation.idxOf b → a = b := by
  decide +kernel

theorem range_map_getBang (l : List Nat) :
    (List.range l.length).map (fun j => l[j]!) = l := by
  apply List.ext_getElem
  · simp
  · intro i h1 h2
    simp at h1
    first
      | simp [h1]
      | simp [getElem!_pos, h1]

/-- Gauge selection depends on the replies only through the multiset of
first colors: the SELECTED MAP itself (not just its histogram) coincides. -/
theorem chosen_map_perm_invariant (r1 r2 : List FrameColor)
    (h : (r1.map Prod.fst).Perm (r2.map Prod.fst)) :
    chosenPrefixColorMap r1 = chosenPrefixColorMap r2 := by
  have hH : prefixGaugeHistogram (r1.map Prod.fst) =
      prefixGaugeHistogram (r2.map Prod.fst) := by
    funext sigma
    unfold prefixGaugeHistogram
    exact counts_perm (h.map _)
  unfold chosenPrefixColorMap choosePrefixGauge
  rw [hH]

theorem normalized_prefix_perm (replies : List FrameColor)
    (hlen : replies.length = 11) :
    (normalizedPrefix replies).Perm
      ((replies.map Prod.fst).map fun c => (chosenPrefixColorMap replies)[c]!) := by
  have hp := (frozen_prefix_stable_order_perm replies).symm
  have hmap := hp.map (fun i => (replies.map Prod.fst)[i]!)
  have e : (List.range 11).map (fun i => (replies.map Prod.fst)[i]!) =
      replies.map Prod.fst := by
    have := range_map_getBang (replies.map Prod.fst)
    simpa [hlen] using this
  rw [e] at hmap
  have := hmap.map (fun c => (chosenPrefixColorMap replies)[c]!)
  simpa [normalizedPrefix, List.map_map, Function.comp_def] using this

theorem normalized_prefix_sorted (replies : List FrameColor) :
    (normalizedPrefix replies).Pairwise
      (fun a b => collation.idxOf a ≤ collation.idxOf b) := by
  unfold normalizedPrefix
  refine (frozen_prefix_stable_order_sorted replies).map _ (fun i j h => ?_)
  have h' := of_decide_eq_true h
  simp only [frozenPrefixColorRank] at h'
  show collation.idxOf _ ≤ collation.idxOf _
  omega

/-- The sorted prefix is a function of the first-color MULTISET only. -/
theorem normalized_prefix_perm_invariant (r1 r2 : List FrameColor)
    (h1 : r1.length = 11) (h2 : r2.length = 11)
    (hp : (r1.map Prod.fst).Perm (r2.map Prod.fst))
    (hcol : ∀ c ∈ r1.map Prod.fst, c ∈ collation) :
    normalizedPrefix r1 = normalizedPrefix r2 := by
  have hm := chosen_map_perm_invariant r1 r2 hp
  have p1 := normalized_prefix_perm r1 h1
  have p2 := normalized_prefix_perm r2 h2
  rw [← hm] at p2
  have hperm : (normalizedPrefix r1).Perm (normalizedPrefix r2) :=
    p1.trans ((hp.map (fun c => (chosenPrefixColorMap r1)[c]!)).trans p2.symm)
  have mem1 : ∀ a ∈ normalizedPrefix r1, a ∈ collation := by
    intro a ha
    obtain ⟨c, hc, rfl⟩ := List.mem_map.1 (p1.subset ha)
    exact symmetry_color_mem _ (chosen_prefix_color_map_legal r1) c (hcol c hc)
  refine List.Perm.eq_of_pairwise ?_ (normalized_prefix_sorted r1)
    (normalized_prefix_sorted r2) hperm
  intro a b ha hb hab hba
  exact collation_idx_injective a (mem1 a ha) b
    (mem1 b (hperm.symm.subset hb)) (Nat.le_antisymm hab hba)

/-- BS obligation 3: for every reply vector whose first colors are a
permutation of a raw row (e.g. any legal word, by BS-1), the exact
normalized prefix is the prefix of a certificate root. -/
theorem normalized_prefix_has_certified_root
    (roots : Array Lean.Json)
    (parsed : parsedRepresentativeArray
      (include_str "upper-policy-certificate.json") = .ok roots)
    (replies : List FrameColor) (hlen : replies.length = 11)
    (hcol : ∀ c ∈ replies.map Prod.fst, c ∈ collation)
    (row : List Nat) (hrow : row ∈ rawRows)
    (hp : (replies.map Prod.fst).Perm row) :
    ∃ entry ∈ roots.toList,
      rootFirstColors entry = some (normalizedPrefix replies) := by
  have covered := representative_prefixes_covered_source
  unfold coverageCheck at covered
  simp only [parsed] at covered
  simp only [List.all_eq_true, List.any_eq_true, beq_iff_eq] at covered
  obtain ⟨entry, hentry, heq⟩ := covered row hrow
  have hfst : (rowReplies row).map Prod.fst = row := by
    simp [rowReplies, List.map_map, Function.comp_def]
  have hlen' : (rowReplies row).length = 11 := by
    have := hp.length_eq
    simp [rowReplies] at this ⊢
    omega
  have same := normalized_prefix_perm_invariant replies (rowReplies row) hlen hlen'
    (by rw [hfst]; exact hp) hcol
  exact ⟨entry, hentry, by rw [heq, same]⟩

#print axioms normalized_prefix_perm_invariant
#print axioms normalized_prefix_has_certified_root

end CubeRev029.Nineteen
