# CUBE-REV 0.29 Y — Lean proof closure gates and clean-build integrity audit

Date: 2026-11-21. **Status: verification infrastructure and schedule theorem added; the universal 19-frame Lean theorem is not yet compiled or completed.**

## Principal research claim

The primary theorem is the impossibility of universal identification in at most 18 paired frames, even with the entire corner configuration disclosed. The existing U revision provides a Lean physical lower-bound theorem. A 19-frame constructive upper policy is independently checked for the exact frozen 52-representative continuation certificate, all 1,362 first-11 count vectors with 3,215,616 representative-normalized candidate runs, and 1,000 legal physical face-turn scrambles; this strong computational evidence is **not** a substitute for the missing single Lean upper theorem.

## New discrepancies detected and actions

1. **Actual vs idealized corner schedule.** The previous `corner_fourteen_unique` theorem omitted corner position 7, whereas the end-to-end X controller omits position **5**. Y adds `corner_fourteen_unique_missing_five` and exposes the exact 19-frame corner sticker sequence in `NineteenSchedule.lean`. The final fresh corner color `URB[2]` (raw corner index 4) is seen *only at frame 19*. The source-matching script verifies agreement with X's `CORNER_SCHEDULE` and rejects three mutated schedules. These newly added theorem statements still require actual Lean kernel compilation.
2. **Clean CI build input absence.** `EighteenCertified.lean` and `NineteenDataReceipt.lean` use `include_str` on `EIGHTEEN_QUERY_DAG.json` and `upper-policy-certificate.json` respectively. Neither file is stored directly at that path in GitHub; earlier read-only CI attempted `lake build` without first providing them. Y now vendors **compressed base64 copies** of both authoritative certificates under `formal/029/certificate_blobs/`, and `restore_pinned_data.py` independently validates compressed and uncompressed SHA-256 before installing the two exact local JSON inputs. The script rejects a corrupted compressed blob and an incompatible existing JSON. Read-only CI runs this step **before** attempting Lean compilation.
3. **Proof environment.** Lean 4.34.1 is pinned. In this session's local container, neither `lean` nor `lake` is installed, and direct access to the official release binary was unavailable. The GitHub connector's accessible status endpoints have not surfaced a successful read-only Lean workflow run. Do not claim that any **new Y** Lean theorem has compiled or that the axiom audit succeeded.
4. **Correction to the interim review.** Upon closer inspection, the old `corner_fourteen_unique` proof already expands both total-sum hypotheses; that specific alleged missing expansion was not a verified source defect. The actual defect of applicability was the **omitted-corner mismatch**, handled above. No historical claim should be quietly altered.

## Reproduce without network-dependent certificate fetching

From a clean repository checkout, after verifying its tracked files:

```sh
python3 formal/029/restore_pinned_data.py
python3 formal/029/validate_19_corner_schedule.py
cd formal/029
lake build
python3 check_data.py EIGHTEEN_QUERY_DAG.json upper-policy-certificate.json
lake env lean CornerPairDecoder.lean
lake env lean NineteenSchedule.lean
lake env lean PhysicalPolicyCompilerFast.lean
lake env lean PhysicalEighteen.lean
```

Run `#print axioms` for the exact final theorem, review the full build log and preserve a branch+commit+Lean toolchain+certificate-hash receipt. Do not treat static text inspection, `python` assertions or the presence of `#print axioms` commands in source as evidence of a successful Lean run.

| Exact input | Uncompressed SHA-256 | Deterministic gzip SHA-256 |
| --- | --- | --- |
| 18-read DAG | `dc9841db1f84819e140a02e9d468a7bbaf062e974beff440fed5db3bcf1bd8ce` | `92c131615f7ca8a070f108053c7473752c8b9964b6abcf7552ab61dcad05278d` |
| 19-frame policy | `80f334520d288b09d0ad2398b596e8910515d312b342cf07ceeb5e4107922227` | `d9dd5f9c283b9d79a86bcf00cefc51e013bc8d20a1c8c34077316a1c81e3f1d3` |

## Exact remaining universal formal obligations

1. `Reachable s → ∃ legal CornerCoordinates, agree_with_actual_corner_colors s` and invariants (distinct cubies, twist sum zero, parity matching edge permutation) under each of the twelve generators and arbitrary turn words.
2. Universal 48-symmetry/11-position transport of any first-color record, the flip constraint, and the exact permutation-sign correction; not just tests of sorted-prefix count-vector representatives.
3. Reify the frozen validated 52-tree certificate into a total Lean `Policy (Fin 24 × Fin 24) FrameColor Coloring` with `Fits 19` and prove terminal decoding is exactly the input state, with the corner sign unavailable until after the 19th simultaneous read.
4. Apply `physical_nineteen_of_abstract_bounded`, and check the exact theorem's `#print axioms` in the pinned kernel/build environment.
5. Separately formalize the nonadaptive 21-frame optimum if presenting that comparison as fully Lean verified.

**Editorial gate:** Do not remove the qualification on the 19-frame upper bound until items 1–4 have passed. An independently checked finite upper-bound algorithm is strong evidence, but it is not an all-states Lean theorem.
