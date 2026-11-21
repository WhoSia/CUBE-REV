# CUBE-REV 0.29 — Adaptive lower bound and pinned data checks

The main contribution is the impossibility of identifying a fixed-center Rubik's Cube in at most eighteen paired observations. The physical Lean theorem gives a collision even when both starting cubes have the same solved corners. The nineteen-frame construction has a checked finite policy and a separately verified physical routing lemma.

| Component | Verified scope |
| --- | --- |
| `AdaptiveLowerBound.lean` | Finite-budget decision policies, transcript collision against a ranked residual certificate, preservation of budget under known responses and address pullback, and specialization to disclosed corners. |
| `EighteenReadData.lean` | Boolean legality checks, child reconstruction and witness lift over all 43,870 arcs, and the proofs for the flip bit and rank-insertion inversion parity. |
| `NineteenReadData.lean` | Reconstruct the first-color orbit support, enumerate feasible representative edge assignments, check every reply in the frozen trees and each terminal sign class. |
| `*DataReceipt.lean` | Prove equality to the expected finite receipts using Lean's native computation. Each prints its generated native-evaluation trust dependency. |

The finite graph now constructs the semantic certificate directly. The two local lift lemmas prove admissibility and observation preservation for **every** admissible child word, including the observed response and injectivity. The parser reconstructs the graph from the original input, and the validator checks the local theorem premises at every address. The actual roots now instantiate the generic policy theorem.

| Component | Verified scope |
| --- | --- |
| `ResidualWord.lean`, `ResidualLift.lean` | Universal insertion, reordering, color, parity and orientation laws for both kinds of read. |
| `SemanticGraph.lean`, `SemanticInput.lean` | Turn the finite validated graph into a semantic adversarial certificate. Return a known color directly, and use a universal lift for every fresh query. |
| `RootCoordinates.lean` | At either root, the assignments have twelve valid oriented edges. The 24 real edge addresses separate distinct assignments. |
| `EighteenCertified.lean` | For either corner parity and every policy with budget 18, distinct 24-facelet edge assignments produce the same paired transcript when the corner colors are a known function. |

| Component | Verified scope |
| --- | --- |
| `FaceTurns.lean`, `EdgeSorting.lean` | Geometric quarter-turn permutations on the 48 non-center stickers and factorization of every even edge permutation into an even number of adjacent swaps. |
| `EdgeOperations.lean`, `EdgeFlips.lean`, `SolvedCornerReachable.lean` | Endpoint checks for 121 ordered pairs of adjacent swaps and 144 ordered pairs of flips. These yield legal turn words for every even-sector edge assignment with all corner stickers fixed. |
| `PhysicalObservation.lean`, `PhysicalEighteen.lean` | Adaptive composition of relative turns and a physical collision for any fixed edge and corner probe pair under every policy with budget at most 18. |
| `JointProbeRouting.lean` | All 576 paired target addresses have legal routing words from a base probe pair. Composition and inverses extend the result to arbitrary fixed probes and prior poses. |
| `NineteenSector.lean` | Every compatible oriented assignment is in the candidate list used at the start of the continuation. The proof applies to any first-color list with exactly one unread edge and to either flip bit. |

The physical lower bound uses native evaluation for the pinned graph and the endpoint table. The universal transition, policy, and realization lemmas are proved in Lean. The 19-frame result still needs a universal proof linking the checked representative policy and the corner decoder to one geometric observation policy. The 21-frame non-adaptive optimum is outside these Lean theorems.

## Run

Use the pinned Lean 4.34.1 toolchain and Python 3.

```sh
lake build
python3 check_data.py ../../data/0.29/EIGHTEEN_QUERY_DAG.json.gz /path/to/upper-policy-certificate.json
```

Use the upper-policy JSON from the [S editable bundle](https://drive.google.com/file/d/1g5NCo2vqcjaiHGaSUEiL_OZoy3naY4SV/view). These are the checked input digests:

- Eighteen raw JSON: `dc9841db1f84819e140a02e9d468a7bbaf062e974beff440fed5db3bcf1bd8ce`.
- Nineteen JSON: `80f334520d288b09d0ad2398b596e8910515d312b342cf07ceeb5e4107922227`.

`check_data.py` verifies the input bytes, prepares ignored local copies for `include_str`, and builds the physical lower bound against the pinned data. It verifies malformed-data controls separately, including two corruptions of an arc that preserve the stored node witnesses.


## W upper-bound bridge audit and V replay erratum (2026-11-21)

The physical eighteen-frame lower-bound theorem is the principal result. Formalizing the complete nineteen-frame **upper** policy is still an open Lean task: compose the first-eleven-color orbit transport, the universal fourteen-corner-sticker decoder, the validated representative continuation tree, and `JointProbeRouting.joint_frame_after_pose` into one policy with both addresses selected before the replies.

A new standalone Python suite audits this bridge without relying on the search algorithm:

```sh
python3 scripts/cuberev-observation/check_r029_w_upper_bridge.py \
  --certificate /path/to/upper-policy-certificate.json
```

It verifies all 52 frozen representative policy trees (141,097 nodes), all 1,362 feasible first-color count vectors, 3,215,616 oriented assignment transports, all 48 color relabelings' parity behavior, all 576 joint physical target routes, the 24 oriented corner two-color pairs, the twelve move generators' cubie invariants, and negative controls. The policy input SHA-256 remains `80f334520d288b09d0ad2398b596e8910515d312b342cf07ceeb5e4107922227`.

**Important erratum:** V's `worked-physical-replay.json` assigns the URB cubie to the URB position while claiming first two colors U,L there, which is physically impossible. The W suite **must reject** that raw witness. It also tests the distinct `worked-physical-replay-corrected.json`, whose corner labels and twists are physically consistent and whose fourteen reads are explicitly scheduled. Do not describe the corrected state as the same random sample as V.

These are independently executable finite regression checks, **not a newly compiled Lean proof** of the nineteen-frame upper bound. See [W audit ledger](../../docs/0.29/20261121_W_UPPER_BRIDGE_AND_ERRATUM.md) and [W receipt](../../docs/0.29/20261121_W_UPPER_BRIDGE_RECEIPT.json). The current container used for the W audit did not have the Lean executable; the historical lower-bound Lean build evidence is preserved separately.


## X: entire nineteen-frame controller, bounded physical compiler, and trust boundary

The new [X end-to-end audit](../../docs/0.29/20261121_X_END_TO_END_CLOSURE.md) drives the exact frozen 52-tree decision policy all the way from canonicalizing the first eleven observed edge colors to the final corner-parity selection and inverse coordinate map. It passes for 3,215,616 count-vector-normalized edge records (one sorted eleven-color record for each of 1,362 feasible count vectors) and for 1,000 legal geometric face-turn scrambles at fixed probes `DL[1]`, `DLB[1]`, recovering every one of the 48 non-center stickers in at most 19 paired frames. Three malformed-decoder controls are rejected. This is a finite/computational proof audit, **not a new Lean certificate of the full upper theorem**.

Three additional formal modules have been added:

- `PhysicalPolicyCompiler.lean`: turns any abstract paired-read policy into a physical fixed-probe policy with the same frame budget;
- `PhysicalPolicyCompilerFast.lean`: constructs a bounded-length legal setup at each frame by resetting from the previous canonical pose, instead of expanding a turn history exponentially;
- `CornerPairDecoder.lean`: under the explicit corner piece-sum and twist-sum conservation hypotheses, gives uniqueness of all 8 oriented corners from 14 cyclically ordered stickers.

**Build status:** the X execution container has no `lean`/`lake`. A read-only pinned GitHub Actions job was added in `.github/workflows/cuberev029-lean.yml`; a successful build and axiom report for these *new* modules has not yet been obtained by the agent. Do not represent their theorem statements as kernel-checked until the CI logs are inspected and the assumptions about Reachable states are discharged. The separate existing 18-frame geometric lower-bound theorem was compiled in the previous U verification.

With the complete [X reproducibility ZIP](https://drive.google.com/file/d/1Ump-hWOEx7XBJ5C2b3UwmiFxemJO-ztu/view), run `lake build` from `formal/029` after unpacking; then execute the seven range commands from the X ledger to regenerate the finite receipts.
