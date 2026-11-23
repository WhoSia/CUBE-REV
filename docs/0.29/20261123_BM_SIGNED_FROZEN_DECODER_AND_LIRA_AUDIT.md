# CUBE-REV 43 / BM — Frozen Decoder Sign Interface and Independent CI Audit

**Date:** 2026-11-23. Branch: `research/current`. Work area: frozen signed terminal decoder; Claude owns the turn-word/edge-coordinate induction. **No global physical Fits 19 claimed.**

## 1. Independent verification of prior BG–BL

Read-only pinned GitHub Actions run [45190959094](https://github.com/WhoSia/CUBE-REV/actions/runs/45190959094), associated with `566b6abd9240df891acd1df9988d2b230a0cf5c0`, has a completed **success** job. The GitHub run-job endpoint independently reports success for `Compile pinned Lean package`, `Independently replay data certificates and negative controls`, and `Inspect new theorem dependencies and compilation`. This supersedes earlier uncertainty for the exact compiled SHA, but not for any subsequent commits.

The independent Claude review caught two material previous coding problems: BJ needed to unfold `cornerPermutationOdd` to rewrite, and BL's unqualified `parity` was silently elaborated as an implicit variable before repair. The repair is in `fda1e9b` and `566b6ab` respectively. All newly authored proof modules should use `set_option autoImplicit false`.

**Commit author correction:** GitHub's mapped `author.login` and `committer.login` of prior GPT-6 commits resolve to `WhoSia`, but those are **account handles**, not the raw Git author/committer name strings. Claude independently observed that older GPT-6 commits used the raw name `OOZ OON\" Kim`. The previous claim that raw git names were both literally `WhoSia` was wrong. The current GitHub connector's commit payload does not expose the raw name strings; it cannot certify them. No history rewrite. For future commits, independent raw Git metadata verification is required; do not report mapped login as a raw-name audit. If the write connector cannot force raw author and committer names, halt source writes requiring an exact literal name and use authenticated Claude/terminal git instead.

## 2. New formal bridge: typed premises, genuine frozen certificate

Source: `formal/029/FrozenTerminalSignBridge.lean`.

The module explicitly sets `set_option autoImplicit false` and introduces:

1. `normalized_edge_sign_matches_observed_corner_sign`. This equates the actual frozen `edgeWordSign normalizedWord` with the corrected physical corner parity `observedTerminalCorrectedParity firstElevenReplies corners == 1` **if and only if the following two supplied physical/normalization premises are available for the chosen original and normalized words** (only the forward implication is proved):
  - `legalCoupling : parity(originalWord.labels) = cornerPermutationParity corners`
  - `transportedParity : parity(normalizedWord.labels) = (parity(originalWord.labels) + frozenPrefixSignCorrection firstElevenReplies) % 2`

2. `frozen_root_recovers_with_observed_corner_sign`. Consumes the **actual** parsed immutable frozen certificate entry through `every_actual_frozen_root_recovers`, the candidate's membership in its parsed belief, the two sign premises, and proves its sign-indexed eight-read decoder returns exactly `some normalizedWord` when supplied the corrected corner sign.

This is more than generic parity algebra because the second lemma applies the existing frozen root *semantic certificate* with its real `edgeWordSign` input, not a hypothetical decoder. It does **not** establish the still-open premises. In particular, no theorem currently supplies the required original physical edge-word witness, edge/corner parity coupling for all reachable states, or the universal normalized root selection and belief-membership conditions from all real ordered first-eleven replies.

## 3. Next verification and acceptance gates

- **BM-A** pinned compilation at the new source SHA: no `sorryAx`, no unknown implicit variables, expected axioms inspected.
- **BM-B** physical coupling: build original physical edge coordinate representation and prove parity agrees with `cornerPermutationParity` by legal-turn induction; every face turn has a preexisting `edge_corner_turn_sign_agree` generator receipt, which does not by itself prove the all-turn result.
- **BM-C** normalized parity: prove the chosen past-determined permutation and legal color-gauge action induce *exactly* `frozenPrefixSignCorrection` for the corresponding normalized word. Check sign direction and inverse `paint` convention on adversarial tie transcripts.
- **BM-D** root membership: total selection of actual normalized representative roots for every reachable first-eleven transcript, along with proof the normalized actual state belongs to the corresponding frozen belief.
- **BM-E** implementation: construct a terminal sign function of the *actual* nineteen charged paired replies (corner reconstruction, not hidden corner coordinates); prove the computed Boolean equals this corrected parity. Noncomputable `Classical.choose` factorization is logically sufficient to establish existence but not executable parity retrieval.
- **BM-F** end-to-end: a single physical `Fits 19` policy only after BM-B through BM-E are composed and pinned full CI succeeds.

**Coordination:** Claude may own BM-B physical edge-coordinate/turn induction; GPT-6 owns the independently defined bridge, proof ledger, and BM-C/BM-D analysis. Neither should overwrite `EdgeSorting.lean` or the other's current files.

## 4. LIRA/JEV re-grade after independent critical review

Scores in [0,1] are **subjective evidence-management judgments**, not calibrated theorem-truth probabilities. Assign C only to claims at their exact quantifier and semantic scope; known missing premises force HOLD independently of weighted score.

| Claim / task | E | C | G | L | Disposition |
| --- | ---: | ---: | ---: | ---: | --- |
| BG universal bubble totality at pinned `566b6ab` | .97 | .99 | 1.00 | .15 | ACCEPT only for exact algorithmic normalizer scope |
| BL observed-correction information flow at pinned `566b6ab` | .94 | .95 | .95 | .35 | ACCEPT only for factorization statement |
| BL/BM edgeWordSign equals actual frozen required physical corner sign on all reachable cubes | .38 | .20 | .12 | .96 | HOLD: unproved coupling and normalization |
| BM frozen certificate recovers with explicit parity premises | .67 | .70 | .56 | .83 | SOURCE-ONLY until BM build accepted |
| Executable causal terminal sign for all physical states | .36 | .21 | .15 | .96 | HOLD: constructive observation decoder missing |
| All physical first-eleven transcripts select correct root/belief | .40 | .25 | .17 | .97 | HOLD: no all-history proof |
| Unconditional full physical Fits 19 | .33 | .08 | .04 | .95 | HOLD until all noncompensatory gates pass |

The earlier LIRA C=.77 for the *meaningfulness of the physical terminal sign* was an overstatement; it applied only to the shallow, definitionally constructed BL information-flow theorem. Scores for a conditional theorem and a physical interpretation must never be mixed. L values within .05 are effectively tied at current uncertainty.

## 5. Falsification scenarios and sign semantics

1. Same physical corner 19-reply record with different first eleven edge histories: the physical corner parity must match, but the **corrected representative sign may differ** because selected gauges and slot orders differ.
2. Same first eleven edge colors with different corner observations: the prefix normalization correction must stay fixed.
3. A selected representative state not contained in the parsed `sector (List.range 12) 0 firstCodes` violates the new BM theorem's `candidate` hypothesis and prevents a global upper conclusion.
4. A root selector fallback `none` or failed parse remains an identification failure even though `Fits 8` technically holds.
5. A sign computed before the 19th charged corner read violates causality unless an independent theorem proves early observability for that history.
6. Swapping between original and inverse color relabeling can negate the effective correction on tied gauge histograms, despite parity arithmetic being internally consistent.

## 6. Source commits

- BM source `d10406dd298db05fad2b315f7a872ecf7a98af99`
- Lake registration `dac09c7dc6165f0fabdbd8034cfcf9aefde8fad3`
- Read-only CI registration `ce59f82fc794d4cc89de4350d689c1644cffe9cf`

**BM CI verdict:** not independently observed at writing time. The green `566b6ab` receipt is valid only for the older tree. GitHub mapped login may be `WhoSia`, but raw author/committer names must be independently checked by Git CLI.
