import PhysicalObservation
import EighteenCertified

namespace CubeRev029.Physical

open Eighteen

/-- The 18-frame lower bound for the geometric cube with any fixed edge
and corner probes. The policy may apply any legal face-turn word between
frames, and choose that word adaptively from the previous colors. -/
theorem physical_eighteen_impossible {O : Type u} (e : EdgeProbe) (c : Fin 24)
    {tree : Policy (List Turn) FrameColor O} (bounded : Fits 18 tree) :
    ∃ s t : Coloring, Reachable s ∧ Reachable t ∧ s ≠ t ∧
      (∀ k : Fin 24, s (cornerSlot k) = solved (cornerSlot k) ∧
        t (cornerSlot k) = solved (cornerSlot k)) ∧
      frameTranscript e c s tree = frameTranscript e c t tree := by
  let logged := tree.logged []
  let absolute := accumulate [] logged
  let adapted := absolute.adapt (queryEdge e) (supplyCorner c) id
  have narrow : Fits 18 adapted :=
    Policy.adapt_fits _ _ _ (accumulate_fits [] (Policy.logged_fits bounded []))
  obtain ⟨x, y, hx, hy, different, equal⟩ := certified_eighteen_edge_collision false narrow
  have transfer (w : Word) : adapted.run observeWord w = frameTranscript e c (encodeEdges w) tree := by
    calc
      adapted.run observeWord w =
          absolute.run (fun u path => supplyCorner c path (observeWord u (queryEdge e path))) w := by
        simp [adapted, Policy.adapt_run]
      _ = absolute.run (fun u path => probes e c (paint path u)) (encodeEdges w) :=
        run_congr_state absolute w (encodeEdges w) _ _ (fun path => (observe_encoded e c w path).symm)
      _ = runFrames e c (encodeEdges w) logged := accumulated_run e c (encodeEdges w) logged []
      _ = frameTranscript e c (encodeEdges w) tree := by
        simpa [logged] using frame_logging e c (encodeEdges w) tree []
  refine ⟨encodeEdges x, encodeEdges y, solved_corners_even_sector_reachable hx,
    solved_corners_even_sector_reachable hy, encode_distinct hx hy different, ?_, ?_⟩
  · intro k
    have bound : ¬ (cornerSlot k).val < 24 := by change ¬ 24+k.val < 24; omega
    simp [encodeEdges, bound]
  · rw [← transfer x, ← transfer y]
    exact equal

#print axioms physical_eighteen_impossible

end CubeRev029.Physical
