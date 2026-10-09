# CUBE-REV 0.19 — P9: Exact Physical Five-Source Five-Word Impossibility and the Six-Word Rank Gate

## Main theorem and scope

Under the real sticker-derived 3×3 Rubik’s Cube's eighteen HTM outer-face actions, a tracked UR edge initially flip zero at one of twelve edge slots, and the complete intrinsic edge-flip observation after each of **five** fixed actions, **no five-word nonadaptive experiment dictionary can identify every one of the original 480 admitted five-position source subsets**.

Let R5 consist of those exact 480 five-position subsets of the frozen original R (|R|=1192). Every word w induces physical observation history h_w. Then:

```
Every D subset of physically realized 5-HTM words with |D| <=5
fails some A in R5, i.e., for all w in D, h_w restricted to A is not injective.
```

This is a **locally reproduced complete SAT-free finite impossibility proof** supported by actual physical action replay and source-locked integer arithmetic, not an unverified HiGHS numerical infeasibility status. The theorem proves **M*_R5(5)>=6**, not that the R5-only optimum equals six. The full original 1192-source minimum M*(5) remains in the integer set {6,7,8}.

## Physical full-fidelity provenance and finite reductions

- Original sticker-derived physical source `physical.json` SHA-256 **9f2119738f92f56485897c1894d2cb721a3d6b0498c5aa14832c71f18b20e2f1**; 1192 source bitmasks, of which exactly 480 have size five.
- Separate complete enumerator `scripts/cuberev-019/export-L5-physical.mjs` explores 18^5=**1,889,568** physical words, producing **14,938** distinct real observation partitions. Independent P9 Python court *replays all 14,938 representatives* against independently constructed eighteen 24-state edge action maps, checking each original output partition block.
- Project these partitions to distinguishability for the 480 original source masks only. There are exactly **3,344** distinct R5 coverage masks.
- Source-specific inclusion dominance: discard an R5 mask C if some physically realized other mask D has C subset D. Retain exactly **2,023** maximal physically realizable R5 cover masks. This elimination is cardinality-preserving for every k: each discarded word may be replaced by a dominating actual 5-HTM word, without losing coverage of R5.

## Exact integer weight bound, pair exclusions and finite exhaustion

The P8 exact rational dual for the R5-only fractional set-cover LP has **80 positive original five-source row weights**, scaled to common denominator312. Their total positive numerator is **W=1480**; every actual five-turn physical experiment covers weighted demand **at most B=312**, independently checked over the full physically realizable column family. Thus any five-word full cover must satisfy, for every subcollection T of t selected experiments,

```
weighted_union(T) >= W - (5-t)*B.
```

Particular valid consequences:
- t=1: every selected experiment covers at least 1480-4×312 = **232** weighted demand. Only **396** of the 2023 inclusion-maximal R5 coverage masks meet the bound.
- t=2: every selected pair has union-weight at least 1480-3×312 = **544**. Out of C(396,2)=78,210 candidate pairs, **61,098** have union-weight below544 and are exactly forbidden; **17,112** remain pairwise compatible.

The independent proof recursively chooses an uncovered R5 requirement with the fewest available distinguishing words and branches on **every** available candidate that can distinguish it, retaining only physically realized candidates compatible with the already chosen experiments. It prunes only when:
1. the remaining number of eligible candidates is below the remaining budget,
2. an uncovered source has no eligible distinguishing candidate,
3. current weighted union + remaining_budget×312 is below1480, or
4. even the sum of the remaining_budget largest possible *new* weighted contributions is below the missing dual weight.

Each exclusion is mathematically necessary for any five-word cover. Crucially the branching **does not fix a global word ordering**; any feasible dictionary must contain a currently eligible word distinguishing the chosen uncovered source, so at least one complete branch would reach it. The exhaustive search visits **1 root, 50 depth-one nodes, and 163 depth-two nodes**, with no feasible continuation. An independent C++ bitset variant constructed from the 544×2887 reduction also reports UNSAT; a separate source-original 480-coordinate audit proves **exact equality of its 396 masks with the directly reconstructed 396 masks**, after correcting for row-index permutation.

**Therefore no five-word physical dictionary covers all 480 original five-state requirements**, yielding the claimed local complete finite theorem. The verifier neither requests nor trusts any SAT solver, LP floating-point status, or fixed reduced-column enumeration order.

## Consequence for the full original 1192-source k=6 court

A five-turn word of observed partition rank r<=4 is not injective on *any* five-element source subset. If a six-word dictionary for the full original family included such a word, its five remaining words would have to cover all R5, contradicting the certified P9 theorem. Hence:

```
Any six-word full R-cover must consist of six words with physical output rank >=5.
```

This is a necessary **k=6-specific** condition; it must NOT be transferred to a seven-word dictionary without re-proof.

In the exact full-source 544×2887 original physical quotient:
- 484 columns have physical observation rank 4; 2403 rank>=5.
- The separate P0 integer dual W=384, per physical word B=72, implies every selected six-word dictionary member has dual weight >=384-5×72=24. This previously left 1877 columns; 153 of them have physical rank4.
- Combining the rank>=5 P9 theorem and exact W384/B72 dual retains **1,724** candidate columns (the 2887 were reduced without changing any original set-cover k).
- For any pair of selected words in a six-word full dictionary, their weighted original-70-row union must be >=384-4×72=96. Of C(1724,2)=**1,485,226** candidate pairs, **947,894** fail this exact integer test and are forbidden. **537,332** pairs remain pairwise feasible. The pair filter is a necessary condition, not a k6 SAT/UNSAT conclusion.

The original k7 court remains separately governed by its weaker 247,348 valid pair clauses; P9's six-word rank theorem does not justify applying rank>=5 to arbitrary seven-word solutions.

## Reproduction, custody, and next proof gates

- Public Python complete finite verifier: [prove-L5-five-source-k5-impossibility.py](../../scripts/cuberev-019/prove-L5-five-source-k5-impossibility.py).
- New independent read-only CI source: [cuberev-019-l5-five-source-k5-court.yml](../../.github/workflows/cuberev-019-l5-five-source-k5-court.yml). The new workflow must regenerate real original physical source, all 18^5 words /14,938 partition classes, eighteen physical move maps, check exact 480-source k5 branching and retain an independent receipt. **GitHub Actions successful runtime receipt is still UNVERIFIED** and is not implied by this committed workflow.
- Existing full original k6/k7 SAT/DRUP source [prove-L5-k7-k6.py](../../scripts/cuberev-019/prove-L5-k7-k6.py) now invokes P9 physical proof as a strict precondition before placing rank4 exclusion clauses in the k6 CNF. The original source-locked exact rational P8 gate precedes P9.
- Canonical independently SHA-256-verified P9 local full physical proof ZIP: [Google Drive file](https://drive.google.com/file/d/1F2C_yLs3szW8Ucro2Rnbr2hFYa0CJ3CV/view) (SHA256 **c029105f843ae0a364d7bdb8b4a9ba7c0985ba860e23211afc5982be5809ee31**, 930,329 bytes). It includes full original physical source and real move maps, all 14,938 physical 5-HTM partitions, dual, pure-Python certificate checker, source-matrix parity audit scripts, k6 rank-gate receipt and SHA256 file manifest.
- The next *integer* question is not whether the five-source k5 subproblem is infeasible (locally complete now), but whether **six** physically realized 5-HTM words can cover **all 1,192** original requirements. Only a physically replayed six-word witness or independently checked six-word UNSAT certificate can settle it. If k6 is UNSAT, attack k7 separately.
- Mathematical ancestry: restricted perfect-hash families, set cover, covering/design theory, pseudo-Boolean proof logging, conditional dual inequalities, action-induced observation partitions. Do not misrepresent these classical concepts as independently new.

## Evidence boundaries

- Five-source-only k5: **complete physical local finite proof PASS**.
- Full-source k6: **unresolved**.
- Full-source k7: **unresolved**.
- Full-source k8 positive witness: **physical replay PASS**.
- Full fractional L5 optimum 16/3 and five-source-only fractional L5 optimum 185/39: **exact rational primal/dual certificates PASS**.
- New P9 CI: **source committed; actual completed execution not verified**.
