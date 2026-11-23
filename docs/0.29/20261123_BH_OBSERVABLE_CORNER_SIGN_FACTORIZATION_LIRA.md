# CUBE-REV 43 / BH — Observable Terminal Bit: Formalization and Decision Reassessment

**Date:** 2026-11-23. **Track:** independent corner-sign/physical policy integration. **Status:** three human-attributed source commits, not yet compiler accepted. **Claude non-conflict:** no edits to `EdgeSorting.lean`.

## Concrete source changes

- `formal/029/CornerTranscriptBit.lean` (commit `21e9ebec3e37fba037705ff037812ab33ec9f789`) introduces a *noncomputable*, classical-choice-defined `cornerTranscriptBit`. The proposed theorem `corner_transcript_bit_correct` shows it equals any corner-extensional Boolean of a reachable cube when fed its **actual nineteen scheduled corner colors**, using `same_nineteen_corner_answers_force_all_corner_colors`. The accompanying `corner_transcript_bit_fiber_constant` expresses the necessary fiber-constancy principle.
- `formal/029/lakefile.toml` (commit `078db50cb056b74a2913cfb0218074d32fdefb31`) registers this new module as a default target.
- `.github/workflows/cuberev029-lean.yml` (commit `5be06871086b9732136d41dd047e46b6b7d6f7fb`) requests explicit Lean compilation of this module in the pinned **read-only** validation job.

**Acceptance gate:** The above are source-level propositions until the exact combined revision passes pinned Lean 4.34.1 CI, and `#print axioms` is inspected. The local runtime does not provide Lean/Lake. Neither a passed build nor a particular axiom list is claimed by this note.

## Mathematical proof, stated without Lean implementation assumptions

Let `S` be reachable cube states, `O : S → Y` the *nineteen-frame* actual corner-color observation history and `b : S → Bool` a Boolean invariant of the complete corner sticker coloring. The existing uniqueness theorem establishes

`O(s) = O(t) ⇒ CornerColors(s) = CornerColors(t)`.

Because `b` is corner-extensional,

`O(s) = O(t) ⇒ b(s) = b(t)`.

Thus `b` factors through the observation image: there exists `f : O(S) → Bool` such that `b = f ∘ O`. A total extension to all histories can select any compatible reachable witness and return `false` outside the realizable observation image. This is the classical choice definition in the Lean source. In particular, the factorization is **not** a secret oracle: it depends on the completed observation vector, not on an unobserved state argument.

**CRITICAL operational caveat:** The function built with `Classical.choose` is generally noncomputable and not yet a practical executable parity decoder. A mathematically defined abstract feedback policy may use such a function as a post-observation map, but a deployable controller needs a computable finite reconstruction. Further, corner-extensionality must be proved for the **particular terminal parity/sign** demanded by the frozen signed-sector policy, including its past-selected position+gauge correction.

## Remaining BE/BG/BH handoffs

1. **BH-A (physical sign specialization):** Define the corner permutation sign for reachable `Coloring` from `reachable_has_permutation_corners`, and prove it is independent of the chosen legal coordinate witness. Theorem `corner_fourteen_unique_missing_five` already supports reconstruction of corner coordinates; the explicit parity definition/transport is not yet identified as accepted.
2. **BH-B (same transcript -> same required sign):** Show the actual final `edgeWordSign` requested by the frozen decoder equals the legal-corner parity combined with the **correct** selected position+gauge cocycle. Do not claim an arbitrary edge sign depends only on corner colors without this legal-state equation.
3. **BH-C (computable decoder):** Replace the classical existential selector by a certified lookup/coordinate reconstruction on a complete and verified finite corner space, or prove executability from the finite representation; ensure the complete nineteen replies are inputs, never a hidden-state oracle.
4. **BG-A (total root matching):** Transport arbitrary first-eleven ordered original responses into the exact representative coordinates before using `matchingFrozenRoot`, and certify the chosen root's belief contains the transported state.
5. **BG-B (all-history signed transport):** Instantiate `transported_signed_policy_transcript_exact` for every reachable state, chosen gauge, stable slot order, and actual frozen continuation tree. Then decode back to original coordinates.
6. **Global completion:** assemble one original-state `Fits 19` policy whose decoder depends only on paid replies. Do not promote any partial theorem to this claim.

## LIRA v2: evidence quality, claim support, generalization, action value, and risk

All numbers below are **expert workflow judgments**, not calibrated probabilities. Keep `E=0.30D+0.20I+0.20R+0.20F+0.10S` and separate `C` from `G`. **Risk (K)** is a new 0–1 direction where higher means greater chance of a misleading or blocking research claim, not physical risk. Distinguish source availability, theorem acceptance, and causal integration before awarding support.

| Claim / next action | E | C | G | L | K | Status |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| BH factorization, conditional on corner-extensional bit | .600 | .820 | .700 | .770 | .250 | SOURCE-ONLY; Lean pending |
| Particular frozen terminal sign is corner-extensional with correct cocycle | .470 | .370 | .230 | .940 | .780 | HOLD, P0 |
| Executable corner-bit function from nineteen real replies | .340 | .210 | .130 | .880 | .850 | HOLD, P0 |
| Normalized root selection on all original ordered histories | .455 | .300 | .180 | .910 | .830 | HOLD, P0 |
| Unconditional `Fits 19` theorem | .300 | .080 | .040 | .920 (work priority only) | .960 | HOLD, NOT CLAIMABLE |

The high L for the global theorem means resolving the proof gap is strategically important, **not** that announcing the theorem is recommended. Publishing an unconditional claim remains forbidden until every hard gate passes. The earlier 0.29 BG score ledger is a different snapshot and should not be overwritten without this explicit history.

## Decision gate / adversarial review

- If the `CornerTranscriptBit` build fails, **E and C for compiler-acceptance remain unconfirmed** irrespective of mathematical plausibility. Correct source and rerun.
- If two legal states have the same 19 corner replies but different proposed required sign after appropriate past correction, the sign specialization is false; identify which past-dependent gauge/order information was improperly omitted.
- If two states share corner replies but have different past edge histories, it is generally *not legitimate* to treat a past-selected sign correction as a function of corner colors alone. The final decoder should be a function of the **full paired transcript** and the remembered gauge, not of corner colors alone. The BH theorem covers only the corner-dependent component.
- Re-score with independent reviewer judgments and sensitivity bounds. When L values are within ±0.05, treat tasks as tied rather than invent a strict preference.
- Keep final verdict gates non-compensatory: absent compiler acceptance, causal sign readout, all-history root matching, or all-state validity implies HOLD.

## Coordination

Claude owns the sorting proof and its compilation repairs; this BH module and ledger are GPT-6-owned. All commits must display authenticated `WhoSia` as **both** GitHub author and committer. No bot commits; GitHub Actions must remain read-only. No force-push or `main` migration.
