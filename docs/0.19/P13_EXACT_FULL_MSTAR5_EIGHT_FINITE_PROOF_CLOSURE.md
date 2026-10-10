# CUBE-REV 0.19 — P13 Final Closure: The Exact Five-Turn Physical Dictionary Minimum Is Eight

**Result:** Under the single **frozen** physical problem described below,

\[
\boxed{M^{\ast}(5)=8.}
\]

**Evidence grade:** independent **local** computer-assisted finite exact proof. Actual SHA-locked 3×3 cube physical state-transition replays, original source-coverage identity checks, nonnegative **integer** covering-weight certificates, exact sixteen-coordinate incidence automorphisms, and complete integer bitset branches were all checked. **A newly completed remote GitHub Actions independent proof-run receipt (or DRUP/Lean proof) has not yet been obtained; local finitary verification is not a claim of external proof-kernel certification.** The result is for the specified tracked-edge five-bit readout only, **not** full cube-state reconstruction, human memory, FMC move efficiency or motor cost.

## 1. Immutable theorem contract

Fix a tracked UR edge whose intrinsic flip starts at zero and whose unknown *edge position* is among the 12 edge slots. Execute one fixed, nonadaptive length-five word over the actual 18 legal 3×3 cube HTM face-action tokens, observing one intrinsic flip bit **after each action**. Each word defines a physical function \(h_w\colon S\to\{0,1\}^5\), \(|S|=12\). The original source family \(\mathcal R\) comprises precisely **1,192** admitted subsets of sizes 3, 4 and 5 (220 triples, 492 mixed four-sets, 480 five-sets). A word separates a known source \(A\) if \(h_w\) restricted to \(A\) is injective. The dictionary covers \(\mathcal R\) if every \(A\) has **some** separating word in that dictionary. The minimum dictionary cardinality is \(M^*(5)\), with unit cost **per entire five-action word**.

Immutable original-source SHA-256:

`9f2119738f92f56485897c1894d2cb721a3d6b0498c5aa14832c71f18b20e2f1`

The directly replayed physical instance has \(18^5=1,889,568\) legal words and **14,938** distinct original-slot observation partitions. Its original-requirement coverage types restricted to rank-five/six/seven words are **2,295 / 1,144 / 32** distinct original 1,192-bit masks (these are *not* the counts 2,168/1,144/32 of the different R5-only quotient). The actual original R5 (480 five-source requirements) has exact integer minimum **seven**, independently locally verified in P12. This excludes any original seven-word dictionary containing rank<5 or duplicate equivalent covering words: the remaining ≤6 words would cover all R5, contradiction.

## 2. Constructive upper bound — eight physically executable words

```
F' B' L F B
F' B' R F B
F' B' D F B
F L2 B' D2 F
F U2 B R2 F
F' B' U F B
F B L F B
F B R F B
```

Independently replay each length-five word using frozen 18×24 sticker-derived physical edge moves on each of the twelve initially zero-flip starting slots. Its exact original-source coverage masks have sizes respectively **553, 553, 553, 465, 465, 553, 553, 553**; their **union is all 1,192** admitted sources. Thus \(M^*(5)\le8\). This is a physical upper witness, not a numerical MIP suggestion.

## 3. Exact lower bound — the eight disjoint classes by count of rank-seven words

Let \(r(w)\) denote the number of different five-bit observation histories across the twelve starting slots, and let \(t\) count selected dictionary words with \(r(w)=7\). Under this physical system, no realized length-five word has rank greater than seven. P12 implies that every candidate for a full **seven-word** cover has rank ≥5, so \(t=0,1,\ldots,7\) is an **exhaustive** case partition. Duplicate source-identical physical words are never necessary: deleting a duplicate would give a forbidden at-most-six R5 cover.

| Exactly \(t\) rank-seven words | Complete independent impossibility mechanism | Exact finite court |
|---|---|---:|
| 0 | Seven rank-five words alone cover ≤7×64=448 of 480 admitted five-sources, so fix one physically realized rank-six word. All 1,144 rank-six original source-coverage masks form **74** orbits under 16 verified source-incidence automorphisms. **65** first-orbit cases have exact original-source nonnegative integer duals \(W>6B\), where B is maximum coverage by any of the **3,439** actual rank-five/six masks. In the remaining **9** cases, the integer dual forces every additional word to have coverage ≥\(W-5B\), retaining **180–219** true physical word types. A *separate* standard-library-only, uncovered-rarest-row exhaustive proof enumerates **5,082** finite branches total, all impossible. | 65 integer certificates + 9 finite trees, 5,082 nodes |
| 1 | Fix one of **3** rank-seven first-word orbits; exact integer residual dual rules out the six lower-rank words on **all** raw original masks. | 3 integer duals |
| 2 | Fix one of **44** unordered pair orbits among the 32 actually realized rank-seven masks; exact original-source residual dual rules out five lower-rank words. | 44 integer duals |
| 3 | Fix one of **327** unordered triple orbits; exact original-source residual dual rules out four lower-rank words. | 327 integer duals |
| 4 | All \(\binom{32}{4}=35,960\) rank-seven quadruples form **2,361** orbits. For each representative, choose a rarest unmet source and enumerate **all** original physical low-rank first words distinguishing it; test whether any two further low-rank words complete the remaining sources, including duplicate choices. Source-locked 14 chunk receipts cover all 2,361 representatives *without omission or overlap* and exactly **359,004** first-low choices. All fail. | 2,361 complete reps, 359,004 trials |
| 5 | All \(\binom{32}{5}=201,376\) high-rank quintuples reduce to **12,717** source-automorphism orbit representatives. Each checks every real lower-rank first word and exact residual one-word completion, with **1,934,145** first-low choices. All fail. | 12,717 reps, 1,934,145 trials |
| 6 | All \(\binom{32}{6}=906,192\) high-rank sextuples, followed by **every** real rank-five/six word, fail original 1,192-source coverage. Sixteen sextuples can be completed on 480 five-sources but **none on the full source family**. | 906,192 quadruple-independent combinations |
| 7 | All \(\binom{32}{7}=3,365,856\) high-rank septuples fail even the five-source family (maximum 476/480 five-sources, 1,188/1,192 original sources). | 3,365,856 combinations |

These cases are exhaustive. Every negative assertion is checked using **physical original source-cover masks**, rather than an invalid rank-changing column dominance or an LP time limit.

### Exactness of the nine final finite trees

For first rank-six representative \(u\), let \(Q=\mathcal R\setminus C_u\) be the actual uncovered original-source requirements. Let \(a_i\in\mathbb Z_{\ge0}\) be one of the source-original integer row-weight candidate certificates, and define

\[ W=\sum_{i\in Q}a_i,\qquad B=\max_{v\text{ any physical rank-five/six word}}\sum_{i\in C_v\cap Q}a_i.\]

Any completion by six lower-rank words must choose every word \(v\) with weighted mass ≥\(W-5B\), else the other five words together have weight ≤\(5B\), strictly insufficient. This condition reduces all original **3,439** rank-five/six physically realizable source masks to 180–219 for each of the nine first-word branches. The independent bitset verifier recursively selects the unmet source with the fewest physical distinguishing choices and explores **every** such choice; it only prunes when exact cardinality or exact original-source integer upper bounds prove completion impossible. Result: **5,082 exhaustive nodes**, no cover. In the other 65 first-word orbits the sharper direct strict inequality \(W>6B\) obviates search entirely.

### Why geometry reduction is sound

The 16 signed-coordinate maps induce explicitly checked permutations of all 1,192 source demands and map the entire relevant **physical rank-constrained source-coverage family onto itself**. Some permutations reverse geometric orientation; they are combinatorial incidence automorphisms, **not** executable cube actions. The proof never merges distinct physical experimental columns into one column merely because they share an orbit. It uses symmetry solely to choose a representative *first selected word*, which preserves existence of a dictionary under the verified closure.

## 4. Exact theorem and resulting observation-horizon profile

Every possible dictionary with ≤7 distinct physical length-five experiments falls into one of the eight rank-seven-count cases and is impossible. Combined with the independently replayed eight-word cover,

\[
\boxed{M^{\ast}(5)=8.}
\]

Consequently the original fixed-source horizon profile, with evidence grades kept separate, is:

| Observation horizon L | Exact fixed dictionary cardinality | Evidence grade |
|---|---:|---|
| 0,1,2,3 | impossible / infinity | analytic structural confinement |
| 4 | **34** | independent DRUP-checked 0.18 physical theorem |
| 5 | **8** | **P13 independent local exact finite proof; new remote CI receipt pending** |
| 6 | **4** | P7 independent local finite proof; new remote CI receipt pending |
| 7 | **3** | independent local physical rank / collision-pair finite proof |
| 8 | **2** | independent local physical rank / collision-pair finite proof |
| L≥9 | **1** | independently replayed nine-action universally distinguishing word plus 8-action obstruction |

This progression counts fixed observation experiment *words*, not turns in an FMC solution. Its striking nonlinearity is a physical restricted perfect-hash-family phenomenon under this exact source ontology.

## 5. Reproducibility, independent verification boundaries and P14 handoff

Local independent runner stages:
1. Reproduce `original_physical.json`, `original_move_maps.txt`, `original_L5_partitions.tsv` from the source oracle; verify SHA and exact 14,938-partition count.
2. Re-run P9/P12 original 480-five-source complete exact finite proof (445 rank-specific integer duals and all t4/t5/t6 original R5 cases). Rechecked in P13.
3. Run `P13_verify_t0_rank5_rank6_exhaustive.py` using 65 explicit original-source row-weight certificate lists, the 9 original-source integer duals and actual frozen partitions (no LP/SAT); expects 74 first rank-six orbits, 65 positive strict duals and exactly 5,082 exhaustive branch nodes.
4. Run `P13_verify_rank7_1to3_integer_duals.py` on **374** explicit original-row integer certificates and all 3,439 raw physically feasible lower-rank masks; expects 3/44/327 complete symmetry orbits.
5. Run the independent `P13_verify_rank7_four_chunked_independent.py` on all **14 disjoint slices** whose union is exactly 0..2360; every representative's remaining 3-word cover is exhaustively checked. Receipt compiler asserts 2,361 total reps and 359,004 attempted first lower-rank choices.
6. Run `P13_verify_R7_count_5_6_7.py` on all original rank-seven quintuple/sextuple/septuple possibilities.
7. Run `P13_compile_exact_full_Mstar5_eight.py` which checks all receipt source hashes, subcase totals and replays the actual full eight-word physical witness. It must print `CUBE_REV_019_FULL_ORIGINAL_PHYSICAL_MSTAR5_EXACT_EIGHT_LOCAL_FINITE_PROOF_PASS`.

All verification scripts and source-locked explicit integer certificates are included in the **P13 final closure ZIP** and its SHA256 manifest. The explicit source-census and integer-branch codes can be audited and rerun without any SAT solver. Numerical LP is used only to **propose** some nonnegative integer duals, never as the proof of impossibility. A fully independent remote GitHub Actions completed-run receipt or proof-assistant/kernel formalization remains an additional open *verification* milestone and must not be invented.

**0.20 is prepared rather than silently activated.** The successor research programme aims to generalize this exact physical finite calculation into structural theorems for action-transported observation cuts, restricted perfect hash families, collision-hypergraph obstruction certificates, and the gap between preset and feedback-controlled state identification. Formal version promotion remains gated by canonical evidence archive and independent CI receipts.