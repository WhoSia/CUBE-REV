# CUBE-REV 0.28 R14-P3 — Exact Parity-Factored Adaptive Beliefs and a Cardinality-Only Quotient Counterexample

**Date:** 2026-11-05. **Status:** general mathematical decomposition (elementary legal-cube group structure), plus an independently executed exact finite residual counterexample. **NOT** a 20-frame construction, full-cube optimality theorem, or a claim about human cognitive state. The full two-probe adaptive color horizon remains 18–21.

## 1. Problem and exact factorization

Use the legal fixed-center oriented Rubik state model. Let E denote the 12-edge signed permutation states with even total edge flip, C denote the eight-corner signed permutation states with total twist zero modulo three. Write E_p and C_p for the states having permutation parity p in {0,1}. The full legal group, as a state *set*, is

    X = (E_0 × C_0) ∪ (E_1 × C_1).

For the full cube, the relevant sizes per parity are
- |E_p| = 12!/2 × 2^11 = 490,497,638,400;
- |C_p| = 8!/2 × 3^7 = 44,089,920;
- |X| = 2 × |E_p| × |C_p| = 43,252,003,274,489,856,000.

Let an observation history h contain all known legal turns and every edge/corner output of the fixed pair of single-six-color probes. For that *realized h*, known turns are known permutations of spatial facelets. Each measured edge color therefore restricts only the unknown **initial edge state**, and each measured corner color restricts only the unknown **initial corner state**. Policy adaptivity is harmless once h is fixed: choices based on earlier colors are fixed by conditioning. Define E_p(h) and C_p(h) as the independently filtered parity-p candidate sets. Then exactly

    B(h) = (E_0(h) × C_0(h)) ∪ (E_1(h) × C_1(h)).

In particular, |B(h)| = |E_0(h)||C_0(h)| + |E_1(h)||C_1(h)|. Treating the edge and corner marginals as independent without the shared parity constraint gives forbidden cross-parity combinations.

**One-frame exact update:** Suppose the current policy picks initial spatial edge-facelet i and corner-facelet j, with observed colors (u,v). For p=0,1 independently,

    E'_p = {e∈E_p(h) : color_edge(e,i)=u};
    C'_p = {c∈C_p(h) : color_corner(c,j)=v}.

The resulting whole belief is the union of parity-matched products E'_p × C'_p. The terminal zero-error condition is
    sum_p |E_p||C_p| = 1.

**Physical caveat:** The separation assumes the known action word and sensor routing are reconstructible from the observed transcript (as in the active P48 six-color model). If the action sequence/pose is itself hidden, observations are noisy, or the same sensor reads an edge-vs-corner ambiguous physical location, these assumptions fail. R11's 576-pair orbit gives free accessibility with *unbounded* known legal turns; action-cost optimality does not follow from this factorization.

## 2. Exact independently implemented finite court

An independent stdlib-only Python program enumerates a **5-edge / 3-corner** subgame with legal relative permutation parity and all edge flip/corner twist constraints. Its chosen corner color triples use a fixed cyclic convention and are NOT independently constructed from P48 source geometry. Therefore the computation is an *algebraic finite validation* of the factorization, not a second 48-sticker geometric oracle.

- E_0 and E_1: 960 states each;
- C_0 and C_1: 27 states each;
- legal combined states: 2×960×27 = 51,840;
- naive unconstrained marginal Cartesian product: 1,920×54 = 103,680 (a 2× overcount before observations).

The experiment observes three sequential pairs of one edge color and one corner color. The second and third queried facelet pairs are deliberately **functions of previous observed colors**, so this is an adaptive-transcript test. The 51,840 legal ground states produce **2,464 distinct transcripts**. For *every* transcript, the directly enumerated full-state count agrees exactly with the parity-factored product formula.

**Cardinality-only abstraction counterexample.** The program finds two realizable histories with the same parity-class marginal cardinalities

    (|E_0|,|E_1|,|C_0|,|C_1|) = (36,36,1,1),

and hence both have 72 joint candidates, but the **same next query** (edge slot 1, corner slot 0) partitions these candidates differently:
- history A: outcome-cell sizes [20,20,20,12];
- history B: outcome-cell sizes [48,24].

The different sorted branch-size profiles cannot be explained by mere renaming of sensor output symbols. Therefore these four **counts alone** are not a sound state equivalence for preserving the complete one-step observation-partition dynamics. A count-only dynamic program would merge states with different future branch structures. The counterexample alone does NOT prove different optimal *remaining minimax depths*, and must not be claimed to.

## 3. Algorithmic consequence and next proof gate

The exact mathematical sufficient representation is the four *candidate sets* (E_0,E_1,C_0,C_1), plus the known pose/action context if turn costs are modeled. This is exact but usually still too large. We must search for a stronger quotient of these candidate sets that preserves, for every allowable paired query, all output-conditioned successor classes (observational bisimulation / backward induction equivalence), not merely |B|, parity-class counts, entropy, or marginal color histograms.

The next high-risk R14 work is to build a canonical representation of partially assigned cubies, their oriented facelet constraints, exact matching feasibility, and parity-conditioned completions. Establish separately:
1. initial-history reconstruction equivalence under legal physical turns;
2. preservation of the edge/corner candidate sets under chosen query and each resulting color pair;
3. preservation of exact minimax depth, including distinguishing the 18–21 full-cube horizon;
4. P48 replay and source-independent physical validation before paper-level promotion.

This research must not substitute the small finite 5-edge/3-corner experiment for the original full-cube difficulty. It is a necessary quotient falsification test and a mathematical bridge, not a final research result.

## 4. Reproducibility and custody

- Repository source: `scripts/cuberev-observation/audit_r14_p3_parity_factored_belief.py`.
- Original Python raw bytes (Drive): https://drive.google.com/file/d/1x9XzsxjkARyd45V3KYUea3w5kNZHTAgp/view
- Exact JSON receipt (Drive): https://drive.google.com/file/d/1NxTJ-LT9gvCC5Xto3Pysut3GT-Bx8Hj7/view
- Local source SHA-256: `2c2abf0e36090a6499f325ff9a672ac1e4776e1677ef93bc2b1ced6820a74227`.
- Local receipt SHA-256: `2e4494cf300d79f9ec661757b09726b2935724998fb1c16f9f3b7b343554a0dd`.
- Independent local execution: PASS (all 2,464 transcripts compared).
- **Drive raw-byte readback:** must be verified before changing status to BYTE_VERIFIED.
- **GitHub remote CI:** not yet asserted PASS for this new source.
- No data from human participants were used; no inference about working memory or intent is justified.

Research OS doctrine: GitHub code/commit + read-only CI, Drive source bytes and receipts, Notion scientific decision record, no `github-actions[bot]` commits.
