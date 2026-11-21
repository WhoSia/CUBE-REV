import JointProbeRouting

namespace CubeRev029.Physical

open Eighteen

/-- The raw edge sticker address underlying a fixed edge probe. -/
def rawEdgeProbe (e : EdgeProbe) : Fin 24 :=
  ⟨2 * e.1.val + e.2.toNat, by
    have h := e.1.isLt
    have hb : e.2.toNat ≤ 1 := by cases e.2 <;> decide
    omega⟩

/-- Reading an original-state address pair, not the rotated frame. -/
def abstractPairRead (state : Coloring) (q : Fin 24 × Fin 24) : FrameColor :=
  (state (edgeNumber q.1), state (cornerSlot q.2))

/-- A choice of an already-proved simultaneous routing word.
Crucially, the requested address pair and the prior pose are selected before
this frame returns either color. -/
noncomputable def stepTo (e : EdgeProbe) (c : Fin 24)
    (prior : List Turn) (q : Fin 24 × Fin 24) : List Turn :=
  Classical.choose (joint_frame_after_pose (rawEdgeProbe e) c q.1 q.2 prior)

theorem rawProbe_eq (e : EdgeProbe) :
    edgeSlot e.1 e.2 = edgeNumber (rawEdgeProbe e) := by
  apply Fin.ext
  rfl

theorem stepTo_correct (e : EdgeProbe) (c : Fin 24)
    (prior : List Turn) (q : Fin 24 × Fin 24) (initial : Coloring) :
    probes e c (paint (stepTo e c prior q) (paint prior initial)) =
      abstractPairRead initial q := by
  have h := Classical.choose_spec
    (joint_frame_after_pose (rawEdgeProbe e) c q.1 q.2 prior)
  have h0 := h initial
  simpa only [probes, abstractPairRead, rawProbe_eq, stepTo] using h0

/-- Compile any abstract paired-sticker decision policy into a physical
fixed-probe policy. A state-dependent history of face-turns is carried
explicitly as `prior`; it is not an additional observation. -/
noncomputable def compilePaired (e : EdgeProbe) (c : Fin 24)
    (prior : List Turn) :
    Policy (Fin 24 × Fin 24) FrameColor O → Policy (List Turn) FrameColor O
  | .stop output => .stop output
  | .read q next =>
      let step := stepTo e c prior q
      .read step (fun reply => compilePaired e c (step ++ prior) (next reply))

/-- Compiling does not change the number of observation frames. -/
theorem compilePaired_fits (e : EdgeProbe) (c : Fin 24)
    (prior : List Turn) {n : Nat} {tree : Policy (Fin 24 × Fin 24) FrameColor O}
    (bounded : Fits n tree) : Fits n (compilePaired e c prior tree) := by
  induction bounded generalizing prior with
  | stop n output => exact .stop n output
  | read n q next branches ih =>
      let step := stepTo e c prior q
      exact .read n step _ (fun response => ih response (step ++ prior))

/-- The physical sequence and the abstract simultaneous reads produce
exactly the same output for every 48-sticker coloring, not just legal cubes. -/
theorem compilePaired_correct (e : EdgeProbe) (c : Fin 24)
    (initial : Coloring) (tree : Policy (Fin 24 × Fin 24) FrameColor O)
    (prior : List Turn) :
    runFrames e c (paint prior initial) (compilePaired e c prior tree) =
      tree.run abstractPairRead initial := by
  induction tree generalizing prior with
  | stop output => rfl
  | read q next ih =>
      let step := stepTo e c prior q
      have reply := stepTo_correct e c prior q initial
      simp only [runFrames, compilePaired, Policy.run]
      change runFrames e c (paint step (paint prior initial))
          (compilePaired e c (step ++ prior)
            (next (probes e c (paint step (paint prior initial))))) =
        (next (abstractPairRead initial q)).run abstractPairRead initial
      rw [reply, ← paint_append]
      exact ih (abstractPairRead initial q) (step ++ prior)

/-- A precisely typed bridge: as soon as an abstract nineteen-read
policy is certified, the physical fixed-probe upper bound follows without
additional frame cost. -/
theorem physical_nineteen_of_abstract (e : EdgeProbe) (c : Fin 24)
    (tree : Policy (Fin 24 × Fin 24) FrameColor Coloring)
    (budget : Fits 19 tree)
    (correct : ∀ s : Coloring, Reachable s →
      tree.run abstractPairRead s = s) :
    ∃ physical : Policy (List Turn) FrameColor Coloring,
      Fits 19 physical ∧
      ∀ s : Coloring, Reachable s →
        runFrames e c s physical = s := by
  refine ⟨compilePaired e c [] tree, compilePaired_fits e c [] budget, ?_⟩
  intro s hs
  change runFrames e c (paint [] s) (compilePaired e c [] tree) = s
  exact (compilePaired_correct e c s tree []).trans (correct s hs)

#print axioms stepTo_correct
#print axioms compilePaired_correct
#print axioms physical_nineteen_of_abstract

end CubeRev029.Physical
