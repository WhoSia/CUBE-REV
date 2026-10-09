# CUBE-REV 0.17 — internal P2: 25-word rigidity and three structural light-profile signatures

**Formal version remains 0.17 OPEN (sole active version); 0.16 is CLOSED and preserved as a historical source.** This internal P2 is NOT a separately named formal version. The inherited exact finite set-cover model is the original one-edge Rubik 18-HTM four-action dictionary over 1,192 source bases. No human cognition, full-cube solve, or externally verified novelty follows.

## New theorem: a 25-word solution, if one exists, must have exactly ten dedicated heavy-singleton words and fifteen positive-mass others

The original independently checked 60-positive-basis dual has integer numerator weights summing to 476. Every real four-turn word w distinguishes positive bases of total mass c(w)≤20, where c(w) belongs to {0,4,8,12,16,20}. Exactly **ten** positive bases have individual weight **20**; each demands a DISTINCT word. By the capacity bound a word covering such a heavy base has c(w)=20 and covers **no other** positive basis. Label these ten obligatory categories H. The remaining fifty positive bases have aggregate mass **276**.

**Exact inherited small-core premise.** Among all real words of positive mass at least16 that do not hit the ten heavy bases, the unique positive-incidence masks are exactly the 116-column table [P10_50_BY_116.json](../0.16/P10_50_BY_116.json). This is the public near-tight physical-derivation input, not a restriction arbitrarily imposed on 25-word solutions. Its full fifty-target set requires at least **15** masks, established by the independent 22-target component minimum9 and 28-target component minimum6, or by a separate exact 14-cover search (165 memo states, 220 branches, 52 capacity prunes). This is an **EXECUTABLE FINITE prerequisite**, not a newly obtained fully symbolic theorem.

**Claim (conditional on that physically grounded small-core certificate):** If a 25-word original universal catalogue W exists, then:
1. exactly ten words in W cover one of the ten weight20 heavy positive bases, one per base;
2. the other **fifteen** words each have **positive** dual mass and cover none of those ten bases;
3. among all 25 words at least **nineteen** have c(w)=20;
4. the fifteen nonheavy words satisfy the exact necessary defect bound
   Σ(20-c(w))≤300−276=24, or Σ((20-c(w))/4)≤6.

**Proof.** At least ten words are required for ten distinct heavy singleton bases. If **eleven or more** words touch any heavy basis, at most fourteen words remain to cover the other fifty positive bases. If **any word has c(w)=0**, the same at-most-fourteen remainder holds after removing ten obligatory heavy words and that zero-mass word. But fourteen words can carry only 280 mass at capacity20. If even one of fourteen has c(w)≤12, the maximum becomes 13·20+12=272<276, impossible. Therefore every hypothetical fourteen-word cover is entirely made of words with c(w)∈{16,20}, which belong to the **complete** original near-tight 116-column projection, where the existing 14-cover UNSAT certificate rules out such a cover. Contradiction in both cases. Thus there are precisely ten heavy and fifteen nonheavy words and no zero-mass words. Each nonmaximal positive-mass word loses at least four capacity units. The residual 15-word loss budget is ≤24, so at most six of them can be nonmaximal. All ten heavy words already have c=20, and at least nine of the other fifteen do: **19 full-mass words minimum.** QED.

**Crucial scope:** The old 168 near-tight family was required to disprove k=24. We do NOT restrict all fifteen remaining candidates in a hypothetical k=25 to that family: some may have c=4,8,12,16, and their zero-dual incidence is essential. The new statement is a rigorously justified **STRUCTURE OF ANY HYPOTHETICAL SOLUTION**, not proof that M*≥26 or M*=25. Current exact interval: **25≤M*≤34**.

Independent stdlib regression: [test-mstar25-rigidity.py](../../scripts/cuberev-017/test-mstar25-rigidity.py). It imports the public 50x116 incidence and redoes the complete fourteen-word UNSAT branching, rather than trusting a hardcoded truth value; it checks the original 165/220/52 certificate and exact integer inequalities.

## New intermediate 17-profile classification: only three five-word heavy-cover signatures

Reconstruct the original **80** candidate masks for the conditional hypothetical 24-word contradiction from P10's complete heavy20/light8 indices. Give each word the type `hH lL` where h is the number of distinguished weight4 heavy targets and l the number of distinguished weight2 light targets in the small B component.

The indexed **82,160 triple / 3,160 pair** exact source reconstruction yields 3,008 five-word combinations covering all twenty heavy targets, now further partitioned by the multiset of five word types:

| Multiset of word types | Exact completions | Light-profile outcomes |
|---|---:|---|
| 5H0L ×3, 4H2L ×2 | **2,628** | 4-light patterns only |
| 5H0L ×2, 4H2L ×2, 4H0L ×1 | **180** | 4-light patterns only |
| 5H0L ×3, 4H2L ×1, 3H4L ×1 | **200** | 6-light patterns only, ten masks ×20 |

These are the **ONLY THREE signature types in the exact census**. The first two families yield all 2,808 realizations of the seven four-light masks, while the third gives all 200 realizations of the ten six-light masks. The seven four-light masks are the previously known seven-of-eight F₂³ affine hyperplanes; the ten six-light masks are complements of two-vertex edges of the previously known two-triangle-plus-exterior-edge graph.

**Analytic consequence, conditional on three-type completeness:** A family with only two 4H2L light-bearing words can cover at most four of eight light indices, so no six-light pattern is possible. A six-light realization necessarily invokes the **3H4L + 4H2L** geometry and reaches exactly six light indices. Thus the 17-pattern classification is reduced to proving from original face-incidence algebra **why no other five-word type signatures can cover the twenty heavy targets**, followed by deriving the seven affine hyperplanes and ten graph edges as possible unions. This is a much more targeted **NONENUMERATIVE PROOF GOAL** than enumerating 24,040,016 quintets, but that crucial first step remains computationally checked, not hand-proved.

Independent finite source: [test-profile-signatures.py](../../scripts/cuberev-017/test-profile-signatures.py) uses a 20-coordinate pair-inverted bitset index over 80 raw masks, completely and uniquely reconstructs the 3,008 five-sets, and checks both the three-type counts and the existing 17-profile frequency table. It is a second check of the model-specific finite result, not an oracle for new theoretical generalization.

## Formal certificate levels / reproducibility

- **Lean 0.17 generic observation congruence and Z4 parity source:** real **BUILD/KERNEL PASS**, pinned Lean4 v4.34.1 [Actions run 37941314665](https://github.com/WhoSia/CUBE-REV/actions/runs/37941314665), after fixing the missing Lake manifest and import-first grammar error. This is NOT a Lean proof of P10's 14-UNSAT, 17-profile completeness, real 18-HTM physical semantics, or exact M*.
- **Machine exact:** 50x116 small-core no-fourteen-cover; 80-mask 17-profile and the new 3-signature counts. Source-to-physical-action equivalence inherits earlier executable test, NOT verified in Lean.
- **Human deduction:** the 25-word ten-heavy/fifteen-other/no-zero-mass and ≥19-full-mass conclusion follows from the precise dual and certified14-UNSAT premises.
- **OPEN:** a Lean checked physical incidence bridge and verifiable SAT UNSAT proof of the full 1,323 maximal masks at k25; a nonenumerative completeness classification; complete prior-art and manuscript court.

**Next best attack:** encode ten dedicated heavy-choice categories and fifteen remaining positive-mass categories into an exact PB/SAT instance, retaining all 1,192 bases, every c≥4 type and the six-unit defect budget. Seek a *checkable* UNSAT certificate; branch-and-bound timeouts without certificates are not mathematical lower bounds. For 17 profiles, derive a short group-action obstruction for the two missing 5-word type signatures before enumerating further.
