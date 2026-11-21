import PhysicalPolicyCompiler

namespace CubeRev029.Physical

open Eighteen

/-- An explicit lookup-order rotation from the selected fixed probes to the
requested two original-coordinate sticker addresses. The underlying table
contains all 24×24 address pairs. -/
def baseSetup (e : EdgeProbe) (c : Fin 24)
    (target : Fin 24 × Fin 24) : List Turn :=
  inversePath (jointPath (rawEdgeProbe e) c) ++ jointPath target.1 target.2

/-- Unlike a stored long history, the base setup has a length bounded by the
frozen 576-entry route table, independently of the frame number. -/
theorem baseSetup_addresses (e : EdgeProbe) (c : Fin 24)
    (target : Fin 24 × Fin 24) :
    follow (baseSetup e c target) (edgeSlot e.1 e.2) = edgeNumber target.1 ∧
    follow (baseSetup e c target) (cornerSlot c) = cornerSlot target.2 := by
  have base := joint_routes_checked.2 (rawEdgeProbe e) c
  have goal := joint_routes_checked.2 target.1 target.2
  have edgeUndo :
      follow (inversePath (jointPath (rawEdgeProbe e) c))
        (edgeNumber (rawEdgeProbe e)) = edgeNumber 0 := by
    rw [← base.1]
    exact follow_undo _ _
  have cornerUndo :
      follow (inversePath (jointPath (rawEdgeProbe e) c))
        (cornerSlot c) = cornerSlot 0 := by
    rw [← base.2]
    exact follow_undo _ _
  constructor
  · rw [rawProbe_eq, baseSetup, follow_append, edgeUndo]
    exact goal.1
  · rw [baseSetup, follow_append, cornerUndo]
    exact goal.2

/-- Resetting a previous pose by its inverse has no effect on the original
coloring. This is an equality of the full 48-sticker state, not just the two
colors observed in the next frame. -/
theorem paint_reset (prior : List Turn) (s : Coloring) :
    paint (inversePath prior) (paint prior s) = s := by
  funext slot
  exact congrArg s (follow_undo_forward prior slot)

/-- Before the next paired read we first undo the previous *short* setup,
then apply a new short setup. The complete look-up path stays bounded by
three finite table paths, rather than growing with the number of frames. -/
def boundedStep (e : EdgeProbe) (c : Fin 24) (prior : List Turn)
    (target : Fin 24 × Fin 24) : List Turn :=
  baseSetup e c target ++ inversePath prior

theorem boundedStep_correct (e : EdgeProbe) (c : Fin 24)
    (prior : List Turn) (target : Fin 24 × Fin 24) (original : Coloring) :
    paint (boundedStep e c prior target) (paint prior original) =
      paint (baseSetup e c target) original := by
  rw [boundedStep, paint_append, paint_reset]

theorem baseSetup_read (e : EdgeProbe) (c : Fin 24)
    (target : Fin 24 × Fin 24) (original : Coloring) :
    probes e c (paint (baseSetup e c target) original) =
      abstractPairRead original target := by
  have endpoints := baseSetup_addresses e c target
  apply Prod.ext
  · exact congrArg original endpoints.1
  · exact congrArg original endpoints.2

/-- A directly executable, bounded-length compiler for any abstract paired
policy. Its next turn word is chosen from target addresses and previous
pose only, *before* either color is returned. -/
def compileBounded (e : EdgeProbe) (c : Fin 24)
    (previousSetup : List Turn) :
    Policy (Fin 24 × Fin 24) FrameColor O → Policy (List Turn) FrameColor O
  | .stop output => .stop output
  | .read target next =>
      .read (boundedStep e c previousSetup target)
        (fun reply => compileBounded e c (baseSetup e c target) (next reply))

theorem compileBounded_fits (e : EdgeProbe) (c : Fin 24)
    (prior : List Turn) {n : Nat} {tree : Policy (Fin 24 × Fin 24) FrameColor O}
    (bounded : Fits n tree) : Fits n (compileBounded e c prior tree) := by
  induction bounded generalizing prior with
  | stop n output => exact .stop n output
  | read n target next branches ih =>
      exact .read n (boundedStep e c prior target) _
        (fun response => ih response (baseSetup e c target))

/-- Universal semantic equivalence, valid for *every* coloring of the
48 stickers. No physical legality hypothesis is needed for this compiler. -/
theorem compileBounded_correct (e : EdgeProbe) (c : Fin 24)
    (original : Coloring) (tree : Policy (Fin 24 × Fin 24) FrameColor O)
    (prior : List Turn) :
    runFrames e c (paint prior original) (compileBounded e c prior tree) =
      tree.run abstractPairRead original := by
  induction tree generalizing prior with
  | stop output => rfl
  | read target next ih =>
      let setup := baseSetup e c target
      let step := boundedStep e c prior target
      have pose := boundedStep_correct e c prior target original
      have reply := baseSetup_read e c target original
      simp only [runFrames, compileBounded, Policy.run]
      change runFrames e c (paint step (paint prior original))
          (compileBounded e c setup
            (next (probes e c (paint step (paint prior original))))) =
        (next (abstractPairRead original target)).run abstractPairRead original
      rw [pose, reply]
      exact ih (abstractPairRead original target) setup

/-- The finite route table yields a genuine same-frame-budget *physical*
policy for every correct abstract identification policy. -/
theorem physical_nineteen_of_abstract_bounded (e : EdgeProbe) (c : Fin 24)
    (tree : Policy (Fin 24 × Fin 24) FrameColor Coloring)
    (budget : Fits 19 tree)
    (correct : ∀ s : Coloring, Reachable s →
      tree.run abstractPairRead s = s) :
    ∃ physical : Policy (List Turn) FrameColor Coloring,
      Fits 19 physical ∧
      ∀ s : Coloring, Reachable s →
        runFrames e c s physical = s := by
  refine ⟨compileBounded e c [] tree, compileBounded_fits e c [] budget, ?_⟩
  intro s hs
  simpa using (compileBounded_correct e c s tree []).trans (correct s hs)

#print axioms baseSetup_addresses
#print axioms compileBounded_correct
#print axioms physical_nineteen_of_abstract_bounded

end CubeRev029.Physical
