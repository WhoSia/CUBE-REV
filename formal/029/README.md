# CUBE-REV 0.29 — Adaptive lower bound and pinned data checks

The main contribution is the impossibility of identifying a fixed-center Rubik's Cube in eighteen paired observations, even with the complete corner configuration disclosed. The nineteen-frame policy attains the bound. This directory advances the Lean verification of those results.

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

The pinned graph validity proof uses `native_decide` and prints its generated trust dependency. The universal transition and policy lemmas do not use that decision procedure. The cubie model lower bound is connected through both real certificate roots. The physical reachability of every compatible cubie word from legal face turns and the semantic connection of the 19-frame representative policy remain separate proof obligations.

## Run

Use the pinned Lean 4.34.1 toolchain and Python 3.

```sh
lake build
python3 check_data.py ../../data/0.29/EIGHTEEN_QUERY_DAG.json.gz /path/to/upper-policy-certificate.json
```

Use the upper-policy JSON from the [S editable bundle](https://drive.google.com/file/d/1g5NCo2vqcjaiHGaSUEiL_OZoy3naY4SV/view). These are the checked input digests:

- Eighteen raw JSON: `dc9841db1f84819e140a02e9d468a7bbaf062e974beff440fed5db3bcf1bd8ce`.
- Nineteen JSON: `80f334520d288b09d0ad2398b596e8910515d312b342cf07ceeb5e4107922227`.

`check_data.py` verifies the input bytes, prepares ignored local copies for `include_str`, and verifies malformed-data controls separately from the pinned computations. It also runs the two negative controls that corrupt an arc while preserving the stored node witnesses.
