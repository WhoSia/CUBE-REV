# CUBE-REV 0.16 — Lean formalization gates and a reduced finite-cover contradiction

**Internal P9 only.** The sole formal version remains CUBE-REV 0.16 (OPEN). Pure mathematical theorems and executable certificates are distinct from human psychological conclusions.

## A. Formal proof status (do not confuse four levels)

1. **Mathematical hand proof**: reversibility implies a fixed action word cannot merge distinct states; group inverse undoes a fully recorded move history. This is classical and not claimed novel.
2. **Exact executable finite certificate (PASS)**: the P7 60-weight dual and a new forced-heavy reduction imply there is no size-24 universal four-turn separating dictionary. Python/C++ bitset cover checkers independently terminate.
3. **Lean source/proof obligations (WRITTEN, COMPILER PENDING)**: an isolated Lean 4.34.1 Lake project in [formal/016](../../formal/016/README.md) includes source for generic injectivity and exact arithmetic at four turns. **We have NOT observed a successful Lean compiler/kernel run.** No Lean kernel proof of the P7 value 8/10, P8 physical graph spectrum, or dictionary lower bound 25 is claimed.
4. **Physical semantic bridge (OPEN)**: Lean formalization must reconstruct exactly the 24 physical coordinates, all 18 legal HTM actions and the known-orientation-bit output; a theorem about an asserted abstract integer table is insufficient to establish the original cube result.

A separate GitHub Actions workflow `.github/workflows/cuberev-016-lean.yml` uses the official `leanprover/lean-action@v1` with read-only permissions to build the isolated workspace, pinned to the existing Lean 4.34.1 release. Never claim CI success before a concrete run status/log is checked. Do not use `sorry` or extra axioms as a substitute for a proof.

## B. New exact reduction for the minimum universal word catalogue

Define the frozen P5/P6 universe of 1,192 requisite initial edge-position sets (220 3-sets, 492 4-sets, 480 5-sets) and one legal 4-turn HTM word's ability to distinguish all states in one of these sets. The exact minimum number of such words is `M*`, still UNKNOWN. Previously: independent positive construction using 34 words and dual/finite-search exclusion of 24, so **25≤M*≤34**.

**Human Lemma 1 (dual slack).** The original P6 dual weights on 60 positive-weight target sets have common denominator20 and sum to 476 integer numerator units, while any fixed 4-turn word covers total positive weight at most20. If 24 words covered all targets, each selected word would need positive coverage weight **at least16**: otherwise the total is at most `15 + 23×20 =475<476`. P7's physical finite census gives 168 near-tight candidate observation partitions, weighted costs16 or20.

**Human Lemma 2 (forced heavy singletons).** Exactly ten of the sixty dual-positive bases have weight20. A word distinguishing one such basis cannot distinguish *any other dual-positive target*: the previous 20-capacity would be exceeded. Consequently any hypothetical 24-word cover must spend at least ten words solely on those ten heavy targets. The rest of its at most14 words must cover the 50 other dual-positive bases, of mass `476−200=276`.

**Computer-verifiable reduced core.** Exact deduplication of the P7 168 candidate positive-cover masks gives 126 distinct masks. Ten are the heavy singleton classes, leaving **116 unique positive-coverage patterns** on the remaining **50 targets**, with max **14 words**. Both independent complete-cover engines use exact integer masks, choose an uncovered target and branch over all candidates covering it; a remaining-capacity condition `uncovered_weight≤20×remaining_words` only removes impossible states. Dominance memoization identifies identical covered subsets reached with equal/more already selected words. **Both Python and C++20 enumerate 165 exact memo states and 220 branches, returning UNSAT for the necessary 50×116, size≤14 problem.** This proves the original 24-word dictionary impossible in combination with the physical P6/P7 dual certificate; **does not prove that 25 words are possible**.

Local mathematical proof bundle: `CUBE_REV_016_P9_FORMAL_LEAN_GATE_REDUCED_COVER_PRIVATE_20261009.zip` (22,399 bytes; 19 members), SHA-256 `b25c6cd46edcc007a717c203f50f4e09d35c7266ea0f1410f5e3ba40bac16c37`; ZIP CRC and fresh-source SHA exact checking and two independent search executables PASS. Private Library `/CUBE-REV/0.16/`, while human solve traces are absent. Source-level original mathematical input remains in separately sealed P7 artifact. Public verifier [verify-dual-forced-core.py](../../scripts/cuberev-016/verify-dual-forced-core.py) accepts the mathematical P7 near-dual candidate JSON as an explicit argument.

**Exact optimum unresolved:** no newly verified 25/26/.../33-word construction, and no impossibility proof for length25 or greater. No solver timeout or restricted-candidate experiment is evidence of global infeasibility.

## C. What Lean should prove next

- **L1 (first attainable kernel lemma):** finite reversible word injectivity and static-arithmetic predicates; compile and retrieve checked Lean Actions result. These are intentionally elementary proof-system smoke tests.
- **L2 (generic weak dual):** formal Finset definition of a weighted universe, word coverage, nonnegative weights, and `sum_weights≤capacity×selected_words` via swapping finite sums.
- **L3 (small exact core):** imported 50×116 Boolean incidence matrix and a generated unsatisfiability *proof trace*, checked as Lean data, without trusting a Python/C++ solver's result as an axiom.
- **L4 (physical bridge):** prove all original 104,976 actions map to the exact 168 admitted near-tight partition types under the weighted slack hypothesis, with actual cube action grammar. Independently Lean-check the 34-word complete upper construction.
- **L5 (analytic 8/10):** separate invariant-based lower bounds for the full24 diagnosis/reset optimum; unlike importing 24-bit DP counts as axioms.

A recent adjacent methodology is Florath, *Formal Foundations and Proof-Carrying Certificates for q-ary Covering Codes in Lean 4* (2026, arXiv:2606.09600); its covering-code problem is not identical to this action-constrained set cover, so definitions must be adapted rather than cited as an existing proof.

## D. Responsible research-community contact

Rather than ask for a generic Rubik's Cube breakthrough, publish a **self-contained 50-element weighted set-cover incidence problem** with the exact 116 masks and the 14-word impossibility statement, asking for a conceptual incompatibility certificate or a short human-comprehensible obstruction. Only math-only finite data, theorem and reproduction link should be shared, not source-limited human traces.

Use [Lean Community Zulip](https://leanprover.zulipchat.com/) for help formalizing Finset/certificate checks. Once the mathematical statement and existing bound are clearly written, consider one focused [MathOverflow](https://mathoverflow.net/help/on-topic) question about a combinatorial certificate or reduction—not a broad invitation to solve the entire CUBE-REV project. No post or outreach has been performed.

## E. Paper gate

Strongest primary candidate remains P8's all-length **octahedral directed-face edge action graph** and explicit history-fiber spectrum, supplemented by the 8/10 controlled-diagnosis/reset optimum. The P5–P9 minimal catalogue is a complementary finite-cover result that would become more compelling with a short 14-word impossibility proof, an exact M*, or a Lean-checked proof-carrying certificate. Classical automata, Markov spectrum, and set-cover antecedents must be credited. Model-relative math cannot by itself establish a measured cognitive barrier.
