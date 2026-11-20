import SemanticInput
import RootCoordinates

namespace CubeRev029.Eighteen

private def certificateBytes : String := include_str "EIGHTEEN_QUERY_DAG.json"

private def graph : Graph := (loadSemantic certificateBytes).toOption.getD default

private theorem checked : graph.valid := by native_decide

private def rootNode (parity : Bool) : Fin graph.nodes.size :=
  if parity then ⟨graph.odd, checked.2.1⟩ else ⟨graph.even, checked.1⟩

private theorem root_position (parity : Bool) :
    graph.pos (rootNode parity).val = root parity.toNat := by
  cases parity
  · exact checked.2.2.1
  · exact checked.2.2.2.1

/-- Eighteen edge-sticker reads are insufficient in either corner-induced
parity sector, even when arbitrary absolute edge slots may be queried.
The output type is arbitrary, so the lower bound applies to every decoder. -/
theorem certified_eighteen_edge_collision {O : Type u} (parity : Bool)
    {tree : Policy Address Nat O} (fit : Fits 18 tree) :
    ∃ s t, Completes (root parity.toNat) s ∧ Completes (root parity.toNat) t ∧ s ≠ t ∧
      tree.run observeWord s = tree.run observeWord t := by
  have room : 18 ≤ (graph.pos (rootNode parity).val).budget := by simp [root_position, root]
  have obstruction := (graph.certificate checked).collision (rootNode parity) room fit
  change ∃ s t, Completes (graph.pos (rootNode parity).val) s ∧
    Completes (graph.pos (rootNode parity).val) t ∧ s ≠ t ∧
    tree.run observeWord s = tree.run observeWord t at obstruction
  rwa [root_position] at obstruction

/-- Both addresses are chosen before each response. The disclosed corner
configuration determines its color, so arbitrary access to that function
does not prevent two distinct legal edge completions sharing the record. -/
theorem certified_eighteen_paired_transcript {C : Type v} {B : Type w} {O : Type u}
    (parity : Bool) (corner : C → B)
    {tree : Policy (Address × C) (Nat × B) O} (fit : Fits 18 tree) :
    ∃ s t, Completes (root parity.toNat) s ∧ Completes (root parity.toNat) t ∧ s ≠ t ∧
      tree.transcript (fun state (q : Address × C) => (observeWord state q.1, corner q.2)) s =
      tree.transcript (fun state (q : Address × C) => (observeWord state q.1, corner q.2)) t := by
  have room : 18 ≤ (graph.pos (rootNode parity).val).budget := by simp [root_position, root]
  have obstruction :=
    (graph.certificate checked).paired_transcript_collision (rootNode parity) corner room fit
  change ∃ s t, Completes (graph.pos (rootNode parity).val) s ∧
    Completes (graph.pos (rootNode parity).val) t ∧ s ≠ t ∧
    tree.transcript (fun state (q : Address × C) => (observeWord state q.1, corner q.2)) s =
    tree.transcript (fun state (q : Address × C) => (observeWord state q.1, corner q.2)) t
    at obstruction
  rwa [root_position] at obstruction

/-- The two initial completions differ on an actual edge facelet. The
observer's action type is restricted to the 24 real edge sticker addresses. -/
theorem certified_eighteen_real_slots {C : Type v} {B : Type w} {O : Type u}
    (parity : Bool) (corner : C → B)
    {tree : Policy ((Fin 12 × Bool) × C) (Nat × B) O} (fit : Fits 18 tree) :
    ∃ s t, Completes (root parity.toNat) s ∧ Completes (root parity.toNat) t ∧
      faceletColor s ≠ faceletColor t ∧
      tree.transcript (fun state (q : (Fin 12 × Bool) × C) =>
        (faceletColor state q.1, corner q.2)) s =
      tree.transcript (fun state (q : (Fin 12 × Bool) × C) =>
        (faceletColor state q.1, corner q.2)) t := by
  let slot : ((Fin 12 × Bool) × C) → Address := fun q => (q.1.1.val, q.1.2)
  let reply : ((Fin 12 × Bool) × C) → Nat → Nat × B := fun q a => (a, corner q.2)
  have bounded := Policy.adapt_fits slot reply id (Policy.logged_fits fit [])
  obtain ⟨s, t, hs, ht, distinct, same⟩ := certified_eighteen_edge_collision parity bounded
  refine ⟨s, t, hs, ht, fun eq => distinct (root_facelets_separate hs ht (congrFun eq)), ?_⟩
  simpa only [Policy.adapt_run, Policy.logged_run, List.reverse_nil, List.nil_append,
    id_eq, slot, reply, faceletColor] using same

#print axioms certified_eighteen_edge_collision
#print axioms certified_eighteen_paired_transcript
#print axioms certified_eighteen_real_slots

end CubeRev029.Eighteen
