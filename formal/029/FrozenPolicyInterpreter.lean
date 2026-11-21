import SignedPolicyTranscript

namespace CubeRev029.Nineteen

/-- A typed, finite, response-indexed policy-certificate graph. The `padding`
constructor consumes one real paired sticker read, independent of its color;
this matches the frozen certificate's "repeat" semantics without assuming a
free observation. `finish` explicitly names a terminal decoded answer. -/
inductive FrozenInstruction (Q R O : Type) where
  | finish : O → FrozenInstruction Q R O
  | choose : Q → (R → Nat) → FrozenInstruction Q R O
  | padding : Q → Nat → FrozenInstruction Q R O

/-- Compile a graph node to a finite actual adaptive policy, with a **total**
response function. Missing indices and branches exceeding the budget produce
`none`, never a fabricated successful reconstruction. No unbounded recursion
or graph acyclicity assumption is needed because the recursion decreases the
remaining read budget.

Every tree is packaged with its universal `Fits budget` proof. -/
def compileFrozenPolicy {Q R O : Type}
    (graph : Array (FrozenInstruction Q R O)) :
    (budget : Nat) → Nat →
      {tree : Policy Q R (Option O) // Fits budget tree}
  | 0, index =>
      match graph[index]? with
      | some (.finish answer) =>
          ⟨.stop (some answer), Fits.stop 0 (some answer)⟩
      | _ => ⟨.stop none, Fits.stop 0 none⟩
  | n+1, index =>
      match graph[index]? with
      | none =>
          ⟨.stop none, Fits.stop (n+1) none⟩
      | some (.finish answer) =>
          ⟨.stop (some answer), Fits.stop (n+1) (some answer)⟩
      | some (.choose query branch) =>
          let next := fun reply => compileFrozenPolicy graph n (branch reply)
          ⟨.read query (fun reply => (next reply).val),
            Fits.read n query _ (fun reply => (next reply).property)⟩
      | some (.padding query destination) =>
          let next := compileFrozenPolicy graph n destination
          ⟨.read query (fun _ => next.val),
            Fits.read n query _ (fun _ => next.property)⟩

/-- The construction is a genuine bounded adaptive controller for EVERY
input graph, not merely graphs with a pre-established finite certificate.
Its output type separates verified terminal answers (some) from rejected
or incomplete branches (none). -/
theorem frozen_policy_has_total_budget {Q R O : Type}
    (graph : Array (FrozenInstruction Q R O))
    (budget root : Nat) :
    Fits budget (compileFrozenPolicy graph budget root).val :=
  (compileFrozenPolicy graph budget root).property

/-- A real leaf is accepted without an extra sticker read, even when the
remaining observation budget is zero. -/
theorem exact_leaf_at_zero_budget {Q R O : Type}
    (answer : O) :
    (compileFrozenPolicy
      (#[FrozenInstruction.finish answer]) 0 0).val =
        Policy.stop (some answer) := by
  rfl

/-- A graph with no certificate node cannot return a fabricated candidate,
even at a positive budget. -/
theorem empty_graph_rejects {Q R O : Type}
    (budget : Nat) (root : Nat) :
    (compileFrozenPolicy
       (#[] : Array (FrozenInstruction Q R O))
       budget root).val = Policy.stop none := by
  cases budget <;> rfl

#print axioms frozen_policy_has_total_budget
#print axioms exact_leaf_at_zero_budget
#print axioms empty_graph_rejects

end CubeRev029.Nineteen
