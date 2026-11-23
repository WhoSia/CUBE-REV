# CUBE-REV 43 / BG — LIRA/JEV Evidence and Decision Ledger

**Date:** 2026-11-23. **Scientific role:** independent integration review of 0.29 physical nineteen-frame upper bound while Claude works on `EdgeSorting.lean`. **Status:** source-grounded research audit, not a new Lean theorem. **Baseline examined:** `52d26dd09cd1366c296d44c9761b776b4112d81b` on `research/current`.

## 1. LIRA protocol (adaptation of the previously defined 0–1 JEV scheme)

Track four separate numbers for every *claim* and *candidate action*; none is a posterior truth probability.

- **E (evidence quality):** `0.30 D + 0.20 I + 0.20 R + 0.20 F + 0.10 S`. D = directness of evidence to exact proposition; I = independence of evidence; R = reproducibility including pinned environment; F = falsification / negative-control power; S = scope match.
- **C (claim support):** researcher-assessed alignment of actual available evidence with the **stated** claim, conditional on its precise quantifiers and premises. Always state the proposition; do not let a high score for a conditional lemma bleed into an unconditional theorem.
- **G (generalization coverage):** fraction-like ordinal research assessment of which target domain/quantifiers are genuinely covered. This is **not** a sampled statistical fraction, not a proportion of solved cube states, and not numerically inferred from the count 52.
- **L (next-action priority):** `0.35 Rel + 0.30 Disc + 0.20 Ready + 0.15 Feas`. Rel = relevance to unconditional physical `Fits 19`; Disc = discrimination of competing explanations/failure modes; Ready = availability of prerequisite artifacts; Feas = estimated practical execution feasibility. Larger L means work sooner, not greater probability of success.

Each input is a transparent **judgment call** in [0,1], and the three component domains differ. Report three decimals, keep factors visible, and change scores when new receipts arrive. Never describe numerical judgments as empirical calibration. Independent reviewer scores and sensitivity ranges are required before treating close recommendations as strict ranks.

**Non-compensatory gates (override any weighted score):** missing pinned compiler success, an unproven branch invariant, absent observational causality, mismatched signed coordinate mapping, or missing all-state totality force HOLD on any purported final physical upper theorem. An algorithmic or mathematical implication can be ACCEPTED only within the assumptions actually checked.

Label every entry `FACT`, `INFER`, `PLAN`, or `HOLD`. Each entry needs source revision, theorem or artifact, failure mode/counterexample target, and a specific re-evaluation trigger. LIRA is a decision record, not a substitute for proof.

## 2. Source-level audit (baseline 52d26dd)

1. `formal/029/FiftyTwoRootReceipt.lean`: `fifty_two_frozen_roots_semantically_accepted` invokes `native_decide` on the immutable `upper-policy-certificate.json`, and `every_actual_frozen_root_recovers` yields sign-indexed eight-read recovery conditional on parsed-source membership. **It is not a theorem that every original ordered eleven-reply transcript maps to one of these roots.**
2. `formal/029/SectorStatewiseValidity.lean`: `statewise_sector_valid_iff_semantic` converts feasible reply-fiber branch validity into a finite surviving-state check. It does not prove that the initial original-state belief is mapped exactly into the representative belief attached to a frozen root.
3. `formal/029/ExactEightSector.lean`: `exact_eight_sector_recovers_given_terminal_sign` consumes `StatewiseSectorValid` and a true member of the candidate belief and returns `some state` **when supplied `sign state` at the terminal decoder**. The sign is not a free sensor response.
4. `formal/029/PairedCornerClock.lean`: `withCornerClock_run` discards corner colors for future edge-query selection, and the paired schedule records real corner observations. `same_paired_corner_colors_force_all_legal_corners` identifies the entire original corner coloring from equal actual scheduled observations on legal states. This **does not yet prove that the leaf's edge-sign argument is computable from those replies** after all coordinate transports.
5. `formal/029/SignedPairedPosterior.lean`: `signed_paired_posterior_all_histories` provides a generic transported posterior result, conditional on the chosen representation and observation correspondence. This is not the global theorem connecting the actual chosen `URFDLB` normalizer with every frozen JSON root.
6. `formal/029/TaggedNineteenRootPolicy.lean`: `matchingFrozenRoot` and `continuationFromFrozenRoots` are actual selectors; the named recovery theorem is conditional on the matching actual root and original state membership. A default/fallback branch must not be silently counted as identification.

## 3. First transparent LIRA scoring pass (provisional analyst scores)

Scores are scoped to the **precise claim** stated in each row, not the final unconditional theorem.

| ID | Claim or action | D | I | R | F | S | E | C | G | Rel | Disc | Ready | Feas | L | Status |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| BG-01 | Immutable 52-root *conditional* signed decoding receipt | .90 | .65 | .85 | .80 | .85 | .815 | .88 | .57 | .90 | .75 | .90 | .70 | .825 | FACT (pinned run must still match current SHA) |
| BG-02 | Actual corner clock and same-corner-observation uniqueness | .90 | .70 | .80 | .65 | .90 | .790 | .88 | .70 | .95 | .85 | .80 | .80 | .868 | FACT, limited to its named theorem |
| BG-03 | Total original-to-52-sector signed posterior transport | .40 | .45 | .35 | .65 | .45 | .455 | .30 | .18 | 1.00 | 1.00 | .60 | .55 | .853 | HOLD (missing bridge) |
| BG-04 | Terminal decoder's sign derived from actual 19 corner replies | .45 | .50 | .45 | .65 | .50 | .505 | .35 | .24 | 1.00 | .95 | .65 | .70 | .870 | HOLD (missing causal sign function) |
| BG-05 | BE/BF universal executable bubble normalizer totality | .70 | .45 | .25 | .65 | .70 | .550 | .35 | .20 | .88 | .70 | .65 | .75 | .761 | HOLD; Claude owns compilation and completion |

**Arithmetic checks:** BG-01 E = .270+.130+.170+.160+.085 = .815; BG-02 E = .270+.140+.160+.130+.090 = .790; BG-03 E = .120+.090+.070+.130+.045 = .455; BG-04 E = .135+.100+.090+.130+.050 = .505; BG-05 E = .210+.090+.050+.130+.070 = .550.

**L recomputation:** BG-01 = .315+.225+.180+.105 = .825; BG-02 = .3325+.255+.160+.120 = .8675; BG-03 = .350+.300+.120+.0825 = .8525; BG-04 = .350+.285+.130+.105 = .870; BG-05 = .308+.210+.130+.1125 = .7605.

Treat BG-02, BG-03 and BG-04 as **joint P0**: the score differences (≤ .018) are far below plausible reviewer uncertainty. In particular the ranking cannot be used to defer BG-03. These are task priorities, not claim-validation rankings.

## 4. The actual semantic interface that is missing

Let `s` be a reachable original physical state, `h` its eleven actual paired responses, `g(h)` the chosen color gauge, `o(h)` the positional adapter, `r(h)` its frozen root selector, and `b(h)` the corresponding representative posterior.

A valid handoff must establish **all** of:

1. **Selection totality:** every physically reachable `h` selects a *valid* root `r(h)`; a default branch is not a proof.
2. **Belief exactness:** `encode(g(h),o(h),s) ∈ b(h)` for every feasible original state with history `h`, and the signed correspondence does not merge states that have different original identities. Ideally show bidirectional posterior equivalence (not just membership).
3. **Reply/branch commutation:** an actual next original-coordinate edge query under the transported policy yields exactly the representative reply used by the checked frozen tree; hold inductively for all feasible eight-read branches, not solely on a selected leaf.
4. **Sign causality:** define a decoder `cornerSignFromReplies : List (paired query × paired response) → Bool` whose input is only completed observations, and prove that on every reachable state *at frame nineteen* it equals the signed sector's required terminal sign. Do not substitute a direct `sign s` oracle.
5. **Original round trip:** combine signed edge output and fully reconstructed corner coloring to obtain the *original* state, with no unknown representative-coordinate component.
6. **Budget:** exact eleven paired reads followed by exact eight paired continuation reads, without free observations or early availability of the terminal sign, then instantiate the already proved physical compiler.

Suggested proof sequencing: BG-03 (selection and posterior), BG-04 (terminal observable sign), then end-to-end 19-frame policy. A useful immediate tactic is a **typed interface lemma** whose explicit hypotheses expose (1)–(5); mark it conditional rather than asserting any hypothesis is automatically true. No new theorem statement should assert a universal `Fits 19` before all gates hold.

## 5. Counterexample and adversarial probes

- Two distinct ordered eleven-color histories with the same histogram and different positional parity; verify selector and combined gauge/position sign correction agree with frozen `route_info`. Historical evidence reports 80 tied-gauge histograms and 36 combined-sign divergences; use original pinned examples rather than fabricate new ones.
- A physically reachable first-eleven history for which `matchingFrozenRoot` gives `none` despite histogram orbit support: if any exists, total selection fails.
- A representative state selected into a root whose belief excludes it: root recognition alone is insufficient.
- A continuation that reaches a leaf before frame nineteen: ensure eight actual paired reads still occur and the sign is not consulted until all corner colors are available.
- Two legal corner colorings with identical first eighteen observed corner colors but divergent terminal information: prove a sign function cannot be evaluated earlier by accident, and verify that frame nineteen does resolve the intended ambiguity.
- Equal original corner readouts and equal decoded edge output but different final original coloring: if possible, inverse-coordinate transport is insufficient.

## 6. Coordination and delivery

Claude exclusively owns `formal/029/EdgeSorting.lean` and its direct sorting proof dependencies until it hands off a compiled commit. GPT-6 owns this BG ledger, the 52-sector/corner causal proof architecture, and related manuscript review, avoiding overlapping edits. Work only on `research/current`, avoid force pushes, preserve `main`, and never permit `github-actions[bot]` authored or committed changes. Each successful commit must be checked for both human author and committer `WhoSia`. Existing GitHub Actions may compile read-only.

**Stop/go rule:** no task-score threshold can override a missing proof dependency or a failed pinned compiler. Reassess scores after new pinned CI results, new counterexamples, an independent Claude review, or a completed bridge theorem.
