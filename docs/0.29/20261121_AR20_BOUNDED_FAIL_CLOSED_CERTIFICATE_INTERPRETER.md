# CUBE-REV 0.29 AR20 — A bounded, fail-closed interpreter for finite response-labeled policy graphs

**2026-11-21 · Formal construction implemented in `formal/029/FrozenPolicyInterpreter.lean`.**

The frozen nineteen-frame upper certificate is a finite JSON representation of 52 adaptive decision trees. Its receipt checker verifies allowed response labels, node reachability and terminal candidate-sign multiplicities, but that is not yet a Lean theorem constructing the corresponding `Policy` object or proving exact recovery of an arbitrary physical state.

An alternative to massive direct tree expansion is to first establish one **generic executable interpreter with a proved observation budget**. Such an interpreter can then serve as a small trusted target for all 52 candidate trees, provided the JSON-to-typed-node parsing and semantic correctness of the certificate are also proved.

## 1. Typed instruction graph

The new type `FrozenInstruction Q R O` has three constructors:

- `finish output`: terminal decoded answer (zero new observations).
- `choose query branches`: genuine adaptive query with `branches : R→Nat`, so every possible response has a destination.
- `padding query destination`: deliberately uninformative observation that consumes one **real** query frame and continues to a response-independent destination. It models the existing frozen certificate's `repeat` semantics without adding a free or invisible step.

The table is an array of these typed nodes; the address in the array is a certificate **node index**, not a physical sticker address. The query type will eventually be specialized to a paired edge/corner sticker address and the response type to categorical paired colors.

## 2. Fail-closed compilation and exact read budget

The function
```text
compileFrozenPolicy
  (graph : Array (FrozenInstruction Q R O))
  (fuel root : Nat) :
    { tree : Policy Q R (Option O) // Fits fuel tree }
```
compiles the finite graph recursively on **fuel**, not on graph indices. Even a malformed graph with a cycle cannot cause nontermination, because a fresh nonterminal consumes one unit of fuel.

A valid `finish` node becomes `Policy.stop (some output)`. An unknown index, or a nonterminal node encountered with zero remaining budget, becomes `Policy.stop none`. Therefore a malformed continuation cannot create a fabricated successful state: it produces a distinguishable rejection result. A `choose` node becomes a real `Policy.read`, and a `padding` node also becomes a real `Policy.read` with the same next node on every response. All branches, including unreachable or invalid categorical replies, are structurally bounded by the same `Fits fuel` proof.

The budget proof is not a separate search across the potentially 141,097 certificate nodes. The `Fits fuel` term is constructed **simultaneously** with the policy for each graph node. The source also provides exact no-rejection controls for a real leaf at zero fuel and for missing graph nodes.

The benefit is precise: **once an adapter from a checked JSON certificate to a typed instruction graph is proved semantics-preserving, the observation-budget theorem is already inherited from this generic interpreter.**

## 3. What a valid certificate still must establish

The above compiler is intentionally total for *invalid* graphs, so the existence of a `Fits 8` compiled tree is **not** yet a proof that the frozen certificate gives a correct eight-read strategy. A compiler can always stop with `none`. The remaining substantive obligations must exclude that possibility on all legal continuation states:

1. Prove that each frozen `NineteenReadData.check` representative entry maps to a typed array with exactly the same `read`, `repeat` and `leaf` semantics, including every possible reply branch. Missing reply branches should become typed rejection destinations, not arbitrary defaults.
2. Provide a leaf-specific output decoder returning an exact original representative oriented-edge state when legal corner sign is available. The frozen JSON leaf `["leaf"]` alone carries no state value; a sound interpreter must derive that value from the **posterior and its sign**, not invent a value.
3. Show no feasible physical continuation returns `none`; equivalently every legal state and response history reaches a valid typed leaf before the fuel is exhausted.
4. Prove all actual representative initial states are among the candidates enumerated from their corresponding eleven first colors, without silently importing a free parity oracle. In particular two opposite-sign candidates are **not** equivalent to one physical candidate until actual corner observations eliminate the wrong sign.
5. Compose with the AR1–AR18 signed posterior and causal trace theorems, then the physical nineteen-corner schedule and query routing compiler.

## 4. Adversarial reviewer / mutation cases

- **Cycle injection:** a graph contains `choose q (fun _ => same index)`. The interpreter remains well-founded because fuel decreases. It returns `none` if it reaches zero rather than falsely proving identification.
- **Missing branch:** a child destination points outside the array. The compiled tree is total, but returns `none` for that branch and must fail an explicit certificate-semantic acceptance gate.
- **Padding for free:** a `repeat` instruction is treated as zero new observations. The new `padding` definition instead spends one **actual paired read**; no hidden uncharged frame is introduced.
- **Empty terminal:** an impossible reply path is mistaken for a unique candidate. Returning `none` and using `beliefExactlyOne` keeps that distinction explicit.
- **Unknown terminal sign:** a leaf contains opposite-sign oriented edges. A real terminal decoder must use parity derived from the actual corner facelets no earlier than the available observation frame.

## 5. Source, verification and mathematical assessment

The formal source is `FrozenPolicyInterpreter.lean`, which is independent of the size of the frozen certificate and uses only structural recursors and the existing `Policy/Fits` definitions. It contains `frozen_policy_has_total_budget`, `exact_leaf_at_zero_budget` and `empty_graph_rejects` with `#print axioms` output. Its actual Lean compiler result must be confirmed by the pinned CI before calling the module kernel-checked.

**Director's verdict:** this is a genuine shift away from enumerating independent policies. It isolates one reusable theorem to handle all budgets and paths, leaving the intellectual focus on *meaning*—whether each certificate node's replies and final decoded state agree with the physical observation model. It is **not** the full 19-frame policy proof, and should be positioned as the typed interpreter backbone rather than a theorem about the 52 certificates themselves.
