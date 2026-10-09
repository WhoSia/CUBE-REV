# CUBE-REV 0.16 — P11 integrality obstruction, verified overlaps and the 75 unseparated bases

**Version hierarchy:** P11 is an INTERNAL mathematical research division of the single formally titled CUBE-REV 0.16, not a separate titled version. 0.16 remains OPEN.

## I. Exact LP/integer integrality gap in the 28-target component

**Frozen mathematical instance.** The published [P10 table](P10_50_BY_116.json) has 50 target bases, their positive dual numerator weights, and 116 possible positive-base coverage masks for abstract four-action tests. Its incidence-connected components have respectively 22 targets/36 masks and **28 targets/80 masks**. In the second component B the total target weight is **96**; there are **74** masks of coverage mass20 and **6** of mass16. Every allowable mask covers mass at most20.

The linear-programming relaxation of covering B chooses nonnegative real coefficients x_j for these80 masks, requires Σ_(j covering i) x_j≥1 for each target i, and minimizes Σx_j. Taking the given target weights divided by20 yields the elementary lower bound Σx_j≥96/20=**24/5**.

**Exact rational feasible primal certificate.** The 24 nonzero variables indexed into the ORIGINAL 116-column table are (index : coefficient numerator with common denominator75):

```text
2:7, 5:6, 8:24, 9:34, 17:7, 26:4, 36:10, 45:32,
46:32, 50:27, 53:16, 74:11, 82:6, 86:11, 89:42,
97:16, 99:11, 100:4, 103:1, 106:16, 109:16, 112:11,
114:11, 115:5
```

Their integer numerators sum to **360**, so total coefficient mass360/75=24/5. For **each** of the28 targets, the numerators of covering variables sum **exactly75**. An independent Python exact-integer test checks all28 equalities. Hence the LP optimum is **exactly24/5**, independently of floating-point optimization. The separately verified integral optimum is6, so its integrality ratio is **6/(24/5)=5/4**. *No bound based solely on these nonnegative fractional covering inequalities can certify integer optimum6*. Integer combinatorial geometry is indispensable.

## II. Stronger extension-overlap obstruction

Let U be the union of **four pairwise-disjoint mass20** candidate masks in component B. Then weighted mass |U|_w=80. Define overlap |U∩q|_w for any other B-candidate q, whose mass is16 or20.

**Finite certified proposition:** For EVERY such U and EVERY other candidate q, **|U∩q|_w≥8**. The finite universe contains exactly **7,004** distinct four-mask disjoint sets U. The minimum fifth overlap is8 both among mass20 and mass16 q. All four-mask sets belong to ONLY THREE incidence-profile types (four masks described by counts of weight4 targets and weight2 targets):
- two (5,0) and two (3,4): **3,720** instances;
- two (5,0), one (3,4) and one (4,2): **2,672**;
- two (5,0) and two (4,2): **612**.

**Hand arithmetic implication:** Any candidate fifth mask covers mass at most20. Thus its uncovered contribution beyond U is ≤20−8=12, and the five masks collectively cover mass ≤80+12=**92<96**. Consequently no five B candidates can cover B, establishing integer optimum at least6; the existing six-mask P10 construction attains6.

**Critical proof classification:** The arithmetic implication and completeness of the three exhaustive profile categories are elementary once the profile list is known. However **the universal ≥8 overlap premise is still verified by a finite 7,004-quartet certificate**, not by a fully calculation-free theorem about cube faces. It is a stronger, more explanatory invariant than testing only the exact forbidden fifth extensions. A short group/incidence proof of ≥8 remains OPEN, and writing it as if the finite verification were unnecessary would be a logical leap.

## III. Exact meaning of the missing 75 original obligations

The P10 25-word construction covers **all60 positive-dual-weight bases** but must also pass the original **1,192** 3/4/5-source candidate bases. Reconstructing the actual 18-HTM edge-cubie automaton from its six four-cycles, directly replaying all25 concrete legal four-token words, and retesting all1192 target bases yields **1,117 covered, 75 missing**.

- **Seven missing four-element bases:** FOUR have counts (F,B,N)=(1,3,0) and THREE have (3,1,0). All seven lie entirely in the **F∪B** original-position classes, with no N position.
- **68 missing five-element bases:** 22 with counts(2,1,2), 21 with(2,2,1), 16 with(1,2,2), five with(2,0,3) and four with(0,2,3).
- No missing three-element bases; the missing original requirements are mathematically admissible by the prior P5 rank theorem.

These 75 describe the weaknesses of **this specific 25-word positive-only witness**. They do NOT imply all 25-word universal dictionaries fail. A solver run selecting fourteen extra words to repair this fixed witness does NOT imply arbitrary 25-word dictionaries need 39 words: completely replacing words changes the problem.

## IV. A critical invalid deduction that must be blocked

The P6/P7 weighted mass certificate has total **476** and maximum mass20 per chosen word. If a hypothetical **24-word** dictionary covered every positive target, the available total capacity is480 and the slack is only4. Thus each word must cover at least16, which soundly restricts candidates to the previously determined 168 near-tight partitions. **For 25 words, total capacity is500 and slack24**, so the same restriction is INVALID: a 25-word universal dictionary may use words of mass0,4,8,12. In fact a MILP restricted to only168 near-tight candidates returned INFEASIBLE for a 25-word FULL1192 cover, but this cannot prove original M*≥26. The correct theorem remains

```text
25 ≤ M* ≤ 34 ; exact value OPEN.
```

Any future proposed 25-word impossibility proof must either analyze ALL legal action partitions (1,913 unlabeled experiment types) or prove a NEW valid candidate-reduction lemma applying explicitly to 25 words.

## V. Lean formalization — source and kernel boundaries

A new Lean4 v4.34.1 source module [P11Fractional.lean](../../formal/016/P11Fractional.lean) embeds the exact24 rational mask/numerator pairs and the28 B target indices. It specifies kernel-checkable propositions that (i) all28 target coefficient sums equal75; (ii) total coefficient numerator is360; and (iii) a generic fifth-column mass≤20 and overlap≥8 imply total union mass<96. The main [CubeRev016.lean](../../formal/016/CubeRev016.lean) imports the new module, so the isolated Lake build is required to check it. **A successful actual Lean compiler/kernel run has NOT yet been observed**, so status is `LEAN_SOURCE_WRITTEN / KERNEL_PENDING`, not `LEAN_PASS`.

Even if the fractional certificate compiles, **the universal 7,004-quartet overlap≥8 condition is not yet a Lean kernel theorem**, nor is the source table's semantic bridge to 24 physical cubie states. Future goals: implement a separate Lean reflection lemma checking the finite overlap premise from the immutable 80 original 28-target masks, and independently prove the physical 18-action orbit/candidate correspondence.

## Evidence and paper role

The standalone Python stdlib checker [test-p11-integrality-overlap.py](../../scripts/cuberev-016/test-p11-integrality-overlap.py) reads the PUBLIC P10 50×116 table and checks the exact rational cover and all7,004 disjoint four-mask overlaps, without SciPy or an external SAT solver. Separate original-cubie cycle code replays all25 words and classifies the 75. Neither empirical human psychology nor new human solve source material enters these results.

**Scientific opportunity:** the exact integrality gap5/4 and the quartet overlap ≥8 obstruction help explain why weighted duality does not itself prove six experiments. The next substantive pure mathematical problem is a non-enumerative proof of the universal overlap lemma and a valid 25-word reduction involving the 75 zero-dual-weight bases. Do not promote a finite incidence fact to a universal graph-theoretic law without an explicit new theorem and hypotheses.
