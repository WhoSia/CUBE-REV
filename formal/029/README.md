# CUBE-REV 0.29 — Adaptive lower bound and pinned data checks

The main contribution is the impossibility of identifying a fixed-center Rubik's Cube in eighteen paired observations, even with the complete corner configuration disclosed. The nineteen-frame policy attains the bound. This directory advances the Lean verification of those results.

| Component | Verified scope |
| --- | --- |
| `AdaptiveLowerBound.lean` | Finite-budget decision policies, transcript collision against a ranked residual certificate, preservation of budget under known responses and address pullback, and specialization to disclosed corners. |
| `EighteenReadData.lean` | Boolean legality checks, child reconstruction and witness lift over all 43,870 arcs, and the proofs for the flip bit and rank-insertion inversion parity. |
| `NineteenReadData.lean` | Reconstruct the first-color orbit support, enumerate feasible representative edge assignments, check every reply in the frozen trees and each terminal sign class. |
| `*DataReceipt.lean` | Prove equality to the expected finite receipts using Lean's native computation. Each prints its generated native-evaluation trust dependency. |

The policy theorem requires a semantic `ResidualCertificate`. The computed receipt establishes what the executable checker checked. It does not yet construct that semantic certificate: each lift must preserve admissibility and observations for every child completion, and its injectivity must be proved and instantiated. The rank and flip lemmas provide part of the coordinates argument. No complete Lean theorem about the full legal cube is claimed.

## Run

Use the pinned Lean 4.34.1 toolchain and Python 3.

```sh
lake build
python3 check_data.py ../../data/0.29/EIGHTEEN_QUERY_DAG.json.gz /path/to/upper-policy-certificate.json
```

Use the upper-policy JSON from the [S editable bundle](https://drive.google.com/file/d/1g5NCo2vqcjaiHGaSUEiL_OZoy3naY4SV/view). These are the checked input digests:

- Eighteen raw JSON: `dc9841db1f84819e140a02e9d468a7bbaf062e974beff440fed5db3bcf1bd8ce`.
- Nineteen JSON: `80f334520d288b09d0ad2398b596e8910515d312b342cf07ceeb5e4107922227`.

`check_data.py` verifies the input bytes, prepares ignored local copies for `include_str`, and verifies malformed-data controls separately from the pinned computations.
