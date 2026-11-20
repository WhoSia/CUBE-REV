# CUBE-REV 0.29 — Semantic verification of the 18-frame lower bound

The T manuscript's first contribution is now instantiated in Lean at both roots of the actual certificate. In each fixed corner parity sector, any policy using at most 18 paired color reads has two legal root assignments with identical transcripts and different edge facelets. The corner reply is a known function and both addresses are chosen before it is evaluated.

## What changed

- A first read moves one slot and can reverse its orientation. The verified inverse undoes the move and reversal, transports the inversion parity, and recovers the parent transcript.
- A second read fixes one oriented edge. Reinserting that edge restores the parent's label set, both parity conditions and all colors. The inserted slot answers from a constant and the other queries map to residual positions.
- Both operations satisfy `EdgeLift` for every admissible child word. The validator checks their premises at every address on the original 6,274-node, 43,870-arc graph. Certified nonemptiness and two distinct words are also checked at every node.
- `certified_eighteen_real_slots` restricts the observer to the 24 actual edge positions and guarantees a difference between the two states on those facelets. The 24 oriented label color codes are distinct by kernel reduction.
- The pinned graph uses `native_decide`; the proof exposes the generated evaluation dependency. Incorrect first-read position and second-read orientation are separately rejected with the stored witness pairs left intact.

## Scope at submission

The completed implication is the lower bound in the cubie coordinates and paired observation model. A separate theorem must relate both parity sectors to physically reachable sticker states, including all corner coordinates and legal turns. The nineteen-frame policy currently has a Lean finite certificate check in representative coordinates. Its semantic representative transport, physical corner schedule, and fixed-observation comparison remain to be connected to the same model.

[Reproduction commands](../../formal/029/README.md) · [Lower-bound-first draft](https://app.notion.com/p/41eef561cf9281ce951ad9d30aa097ed)
