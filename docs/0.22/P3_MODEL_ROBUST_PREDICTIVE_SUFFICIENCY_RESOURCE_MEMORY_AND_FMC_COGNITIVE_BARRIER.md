# CUBE-REV 0.22 P3 — Model-Robust Predictive Sufficiency & Resource-Relative Controller Memory: Joint-State Versus Predictive-State Quotients, Nonstationary Cost Policies, Original-Source Decoding & Finite Physical Counterexamples

**Active exact version:** CUBE-REV 0.22 — Cost-Sensitive Physical Identification & Finite-State Decision Semantics: Exact Turn–Observation Pareto Geometry, Task-Relative History Sufficiency, Observation-Automaton Structure & Evidence-Constrained Human Search. [Canonical 0.22 Notion](https://app.notion.com/p/3f5ef561cf9281d8b77ede12f15718d3).

**Status:** P3 PHYSICAL CONTROLLED-PREDICTIVE RANK THEOREMS PASS / LAST-BIT FOREVER-INCOMPLETE RANK-13 PHYSICAL OBSTRUCTION PASS / PROVENANCE-OUTPUT AND NONSTATIONARY COST COUNTEREXAMPLES PASS / EXISTING THREE-SCRAMBLE TWO-SOLVER FMC SOURCE CONTRAST PASS / HUMAN LATENT COGNITION AND GLOBAL OPTIMAL-FSC MINIMALITY HOLD.

## 1. Intellectual provenance and the original cognitive barrier

General POMDP belief-state Markov sufficiency, predictive-state representations (PSR), controlled tests and dynamic quotient refinement predate this project. CUBE-REV already developed claim-relative/dynamic quotients and accumulated-path sufficiency in G3-P23/P26/P27/P29. Preserve [0.19 M-star source-dependent physical observability](../0.19/P13_FINAL_EXACT_PHYSICAL_MSTAR5_EIGHT.md), [0.20 physically transported observation cuts](../0.20/P0_P2_TRANSPORTED_CUTS_AND_NONNESTED_DICTIONARY_EXTENSION.md), [0.21 P7/P8 physical sensor bound and cost frontier](../0.21/P8_EXACT_TURN_QUERY_MEAN_COST_PARETO_MOORE_MINIMALITY_AND_BELIEF_SUFFICIENCY.md), [0.22 P0 prior-relative decision counterexamples](P0_TASK_RELATIVE_PHYSICAL_BELIEF_SUFFICIENCY_ACTION_CONGRUENCE_AND_PRIOR_COUNTEREXAMPLES.md), [P1 two-candidate action congruence](P1_TASK_CONDITIONED_BELIEF_CONGRUENCE_PHYSICAL_PAIR_MINIMALITY_AND_SILENT_PROTOCOL_SEPARATION.md) and [P2 modelling-objection court](P2_OPTIMAL_POLICY_QUOTIENT_AND_ADVERSARIAL_BELIEF_STATE_AUDIT.md).

The original **cognitive barrier** question is **NOT** that a human literally carries around the P7 24-bit mask. It asks how physical solution possibilities, available information, representations and externally written candidates are selectively transformed into *actually evaluated and committed search* under finite time, prior knowledge, costs and cognitive limits. Exact physics supplies falsifiable benchmark structures, not an empirical estimate of hidden human internal states. The FMC fewest-moves regime supplies naturalistic human branch exploration and choices that are not observable in mere WCA outcome rows.

## 2. Exact real physical predictive test semantics

The original full-sticker 3×3 move oracle generates **18 legal HTM physical turns** on **24 physical position/orientation states** of one tracked UR edge (12 slots × 2 intrinsic flip states). State \(s=2p+b\), where \(p\in\{0,\ldots,11\}\), \(b\in\{0,1\}\). The exact read after a legal turn is the transported edge's intrinsic flip bit \(O(T_a s)=T_a(s)\bmod 2\). This 24-state physical ontology includes unknown initial flips; **it is deliberately wider than the original 12 flip-zero source-only P7 task**. Other cubies can satisfy global cube flip-parity constraints, so tracking either flip of a single edge is physically meaningful.

For each fixed legal face-turn word \(w=a_1\dots a_d\), define a controlled observation test \(t=(w,z)\), where \(z\) is either:
- **FULL:** the **entire ordered** \(d\)-bit sequence of actual post-turn intrinsic flip readings, or
- **FINAL:** **only** the single flip bit after the final turn; intermediate readings are unavailable to this measurement interface.

Let \(r_t(s)\in\{0,1\}\) indicate whether the deterministic physical state \(s\) produces the specified transcript. For an arbitrary initial probability mixture \(p\in\Delta^{23}\), the observable prediction is \(P(t\mid p)=\sum_s p(s)r_t(s)\). Test prediction matrices have one column for each of the 24 original physical states; a normalizing all-ones row is included.

**Exact original-physical enumeration and modular linear algebra** (field prime \(1000003\)):

| Maximum legal turn-word length | FULL ordered transcript matrix rank | FINAL one-bit-only matrix rank |
| --- | ---: | ---: |
| 0 | 1 | 1 |
| 1 | **4** | **4** |
| 2 | **24** | **13** |
| 3 | 24 | 13 |

**Theorem P3-A (source-specific controlled predictive completeness):** The 18 genuine physical turn actions permit a finite collection of length-at-most-two **full multi-time binary outcome tests** whose 24 indicator rows are independent over \(GF(1000003)\). Their nonzero determinant mod the prime proves the corresponding integer minor is nonzero, hence the 24 rows are independent over \(\mathbb R\). Therefore their controlled-test probabilities **uniquely determine every probability distribution over the original 24 physical edge states** under the frozen known transition/observation law. The certificate includes the 24 concrete legal test words and bit transcripts. It does **not** say the predicted state is a 24-component human mental representation, nor that all 24 tests are read in a single trial.

This theorem establishes an important negative boundary: a linear PSR for *this exact all-read observational interface* need not use fewer coordinates than the underlying 24-state generative basis. The **specific instance computation**, not general PSR theory, is the new verified result.

## 3. Theorem P3-B — last-bit-only observations forever lose source-location mixture information

For every legal word \(w\), the exact physical edge move permutations have the affine intrinsic flip form

\[
T_w(2p+b)=2\sigma_w(p)+(b\oplus e_w(p)).
\]

Consequently for any final-bit event row \(r_{w,z}\),

\[
r_{w,z}(2p)+r_{w,z}(2p+1)=1,\quad \forall p=0,\ldots,11.
\]

All final-bit-only rows, over words of **arbitrary length**, therefore lie in a linear subspace

\[
\{r\in\mathbb R^{24}:r_{2p}+r_{2p+1}=c\ \text{for every }p\}
\]

of dimension \(13\) (twelve independent orientation differences plus one common pair sum). Physically legal two-turn tests attain rank **13**. Thus the entire infinite test family that reads **only the final intrinsic edge flip** has exact linear rank **13**, not 24. Increasing the number of unobserved turns cannot repair this loss.

**Concrete exact observational equivalence witness:** Mixture A starts at physical slot 0 with unknown flip equally 0 or 1, while mixture B starts at physical slot 1 with unknown flip equally 0 or 1. They are distinct distributions on the 24-state physical ontology, yet any legal word's final flip bit is uniform \(1/2,1/2\) for both. Their final-only predictions **agree for every legal turn word, not merely the length-three enumeration**. Nonetheless one specific two-turn **FULL** bit-history observation test in the external receipt separates their distributions through multi-time correlations.

This is a distinction between *what the observation channel retains*, NOT evidence that retaining information earlier is always cheaper or beneficial when observations themselves are priced. In particular the uniform-within-slot flip mixture differs from the original P7 assumption that the tagged piece's initial flip was known to be zero.

## 4. Theorem P3-C — same current physical posterior, different required origin-label output

Fix the **same original two-source prior** over flip-zero original slots 0 and 1 (physical coordinates 0 and 2). Apply the **same genuine legal two-move sequence** \(U,F\), initially leaving the first move unobserved and reading the intrinsic bit after the second; the two original possibilities emit opposite bits and therefore become identified. The two legal histories are then followed by their respective *known* silent physical transport words:

| True original source slot | Shared first turns | Bit after F | Further legal silent turns | Final physical state | Required original label |
| --- | --- | ---: | --- | ---: | ---: |
| 0 | U,F | 1 | F-prime, U-prime | **0** | **0** |
| 1 | U,F | 0 | U2 | **0** | **1** |

Both are possible branches of the **same prior and genuine transition/observation law**. At the end, both have **the identical physical posterior \(\delta_0\)**; all future intrinsic-bit observations from the same current state have the same laws. Yet if the task requires reporting **which ORIGINAL slot** the piece occupied, the correct answers differ. Therefore future bit-predictive equivalence and identical current physical posterior are not sufficient for an *origin provenance* output contract. Preserve the accumulated known inverse permutation or original-source posterior/source-label map. This implements the earlier G3-P29 source/path warning in a new explicit real-cube counterexample.

The histories may have different elapsed-turn counts; the source-naming obstruction does not claim they have identical remaining resource budgets or identical complete action logs. It proves the failure of **physical-posterior-only** output sufficiency.

## 5. Theorem P3-D — identical physical belief, stage-dependent cost, different optimal first action

Take the **same actual original three flip-zero slot support** \(S=\{0,1,3\}\) with the **same uniform prior** \(1/3\) per source, a maximum of two legal HTM turns, and an intrinsic-bit observation after each move at zero reading price. At first stage, change the hypothetical exogenous **cost per named legal face action**; after the first step, all legal turns cost 1:

- **Schedule F:** at the first turn F/F-prime costs 1, B/B-prime costs 4, others cost 10.
- **Schedule B:** at the first turn B/B-prime costs 1, F/F-prime costs 4, others cost 10.

Using the actual 18 legally realizable turn+bit responses, there are exactly four first moves enabling identification of all three sources by the second turn: F/F-prime/B/B-prime. First F isolates one source; B then separates the remaining two; first B isolates a different source; F separates the remaining two. The continuation happens with probability \(2/3\).

The exact optimal expected cost is **\(1+(2/3)\cdot1=5/3\)** for both cost schedules. Under Schedule F the only optimal first moves are F/F-prime; under Schedule B they are B/B-prime. Therefore **the same posterior over the same real physical source states, same horizon, same legal moves and same observations, under different phase-dependent objective costs requires disjoint optimal first-action sets**.

The choice of artificially assigned face action costs is only a **mathematical adversarial test**. It does not assert F moves are cognitively easier than B moves for actual FMC solvers. The result establishes that a proposed information-state quotient must include a changed task cost schedule **when that schedule cannot be recovered from a known fixed external task descriptor**.

## 6. Actual existing FMC evidence — a matched three-scramble naturalistic contrast

P3 adds a **source-audited matched-scramble historical comparison**, distinct from the pre-existing eight intentionally selected FMC process cases, rather than a new participant experiment.

Two genuine FMC World 2026 competition solvers have independently published reconstructions for **the same three final-round competition scrambles**:
- [Yurii Riabov's three attempt-specific author reports](https://333.fm/wca/reconstruction/FMCWorld2026/2018RIAB01).
- [Qijun Miao's three attempt-specific author reports](https://333.fm/wca/reconstruction/FMCWorld2026/2014MIAO02).

Source scramble words were separately checked for equality at each attempt and conservatively stored once per attempt in the [P3 provenance/attempt ledger](../../data/cuberev-022/p3_fmc_matched_scramble_author_evidence.json). Both authors' official final results for attempts 1, 2, 3 are **19, 19, 23 HTM**.

| Attempt; same actual original scramble | Riabov public **retrospective report** | Miao public **retrospective report** | Both final HTM |
| --- | --- | --- | ---: |
| 1 | About **45 EO candidates checked**, 19-move result found about 20 minutes in | Describes coverage and alternatives; total EO checks **not reported** | 19 |
| 2 | About **55 EO candidates checked**, 19-move result found about 15 minutes in | Retrospectively regards initial DR variant as an unfavorable detour; total EO checks **not reported** | 19 |
| 3 | Reports roughly **70 EOs written, 30 checked**; uncertainty over whether a revisited HTR was really checked on the alternate side; 23 found about 25 minutes in | Reports less additional exploration under the pressure of earlier results; no numerical EO check count | 23 |

These authors' statements are **actual naturalistic historical reports**, not invented actions. Counts and times are approximate **self-reports**; no frame timestamps, scanner logs, or full candidate-evaluation sequences are available. Miao's absence of numeric EO check counts is **UNKNOWN, not zero**. Riabov's uncertainty about a potential mistaken HTR revisit is **explicitly reported uncertainty**, not direct evidence of a memory defect. Miao's reported pressure is an introspective explanatory claim, not independently identified causal evidence.

This is an unusually informative small sample because **the external challenge is matched within each attempt**: the scramble and endpoint solution length coincide, but the authors describe distinct candidate coverage, route selection and search limits. It illustrates **outcome-to-process nonidentifiability** without requiring hundreds of participants; it does not identify actual internal posterior distributions or estimate general-population effect sizes.

### Reconnect to the cognitive barrier without illicit equivalences

Let \(F(\sigma)\) be the mathematical feasible solution/branch universe of scramble \(\sigma\), \(W\) the externally written candidates, \(E\) the actually evaluated candidates, \(C\) the chosen branches and \(Y\) the submitted endpoint. The unobserved \(E\) is not automatically a subset of \(W\): some real evaluations may never be written, and some written candidates may never be tested. Therefore **do not impose a universal chain \(F\supseteq W\supseteq E\)** without data or definitions supporting it. A low final HTM count could result from excellent coverage, lucky alignment with search specialties, efficient representation, early preservation of a good fallback, or other mechanisms. A final score does not identify the latent evaluated set, nor its subjective costs.

The **empirically supported gap** in Riabov attempt 3 is the author's approximate distinction between **candidates written and candidates checked**; the **scientific unknowns** are the exact chronological search trace, cognitive beliefs about candidates, and unrecorded alternatives. The TCS theorems show why retaining a time sequence can be decisive for *one ideal oracle*, not why a real FMC solver consciously held a 24-dimensional belief vector.

## 7. Predicative model, scientific falsification gate and next stage

A task-relative information-state proposal \(\Xi_\theta(h)\) is sufficient when **for every admitted future controlled test** the predicted output distribution, relevant costs, termination and source-decoding outputs are preserved. Predictive-state representations may be smaller than world-state beliefs in some models, but in this actual 24-state single-edge full-read protocol, the matrix is rank 24 already at two-turn horizon. Under a final-only protocol, rank is forever 13, with physically explicit aliasing distributions. Thus state dimension is **observation-protocol relative**, not a universal invariant of "the puzzle."

External prior art: [Littman, Sutton & Singh (NeurIPS 2001)](https://proceedings.neurips.cc/paper/2001/hash/1e4d36177d71bbb3558e43af9577d70e-Abstract.html) introduced predictive representations from action-conditioned tests; original G3 quotient mechanisms predate this chapter. P3's contribution is the **physically legal Rubik instance**, exact 24/13 rank separation, all-word final-bit upper bound, explicit original-source provenance alias, stage-cost policy switch and matched actual FMC source contrast.

**Next P4 candidate (not achieved here):** *Cognitive Search Barrier & Observation-Limited Policy Identifiability: Matched-Scramble Process Bounds, Partial-Order Branch Coverage, Predictive-State Falsification & Epistemic Separation Certificates*. Keep it mathematical + existing FMC evidence first. Full original twelve-source globally minimal FSC, causal measurement of psychological beliefs, video/VFMC engineering, and participant recruitment remain HOLD.

## 8. Independent certificate and preserved caveats

[Actual physical P3 predictive, provenance, stage-cost and source-matched FMC executable](../../scripts/cuberev-022/verify-p3-predictive-rank-provenance-cost-fmc.mjs); [public historical FMC source-limited ledger](../../data/cuberev-022/p3_fmc_matched_scramble_author_evidence.json).

**[GitHub Actions P3 definitive physical/external check #38062179286 — SUCCESS](https://github.com/WhoSia/CUBE-REV/actions/runs/38062179286)**, [source-run receipt/artifact #11673416931](https://github.com/WhoSia/CUBE-REV/actions/runs/38062179286/artifacts/11673416931), artifact ZIP SHA256 **020665d5589289fceeffa839699818c3a1366f224c51be5fb161f2c68ce53393**. The CI reruns exact sticker-derived maps, two-turn multi-time rank 24, provable rank-13 terminal-only obstruction and mixed-state witness, real same-prior provenance histories, nonstationary-cost action switching, and the six matched actual FMC authored attempts.

**Meaning of PASS:** all internal numerical/physical assertions and manually source-curated metadata constraints are consistent, and explicit references allow independent review. It does **not** mean that CI automatically reread each original third-party web page, measured human cognition, or checked unobserved search branches. The ongoing legacy **P7 repository active-set governance CI** may still fail on new tracked paths; it is unrelated to the physical P3 proof and has not been silently repaired.

**Final P3 grade:** EXACT PHYSICAL PREDICTIVE-STATE TEST THEOREM PASS / INFINITE FINAL-ONLY NO-GO PASS / ORIGINAL-SOURCE DECODING AND PHASE COST COUNTEREXAMPLES PASS / FMC MATCHED SMALL-N SOURCE AUDIT PASS / HUMAN INTERNAL COGNITIVE MECHANISM AND ALL-POLICY OPTIMAL CONTROLLER MEMORY HOLD.
