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
