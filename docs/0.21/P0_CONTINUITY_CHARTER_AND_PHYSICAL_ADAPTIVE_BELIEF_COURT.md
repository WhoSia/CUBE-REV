# CUBE-REV 0.21 — P0 Continuity Charter and Physical Adaptive-Reconstruction Benchmark

**Formal title:** Active Reconstruction of the Rubik's Cube: Observation-Driven Action Selection, Belief-State Dynamics, Physical Information Access & the Limits of Adaptive Solving

**Scientific status:** 0.21 OPEN, physical P0 baseline audit in progress. This version is a continuous *extension*, not a replacement or reset of CUBE-REV 0.18, 0.19 or 0.20.

## Source-preserving chain

1. **0.18 exact:** 18 legal HTM moves of physical 3×3 Rubik, original tracked UR-edge 24 states, 12 zero-orientation starting slots, 1,192 source subsets, four-turn preset universal requirement-dictionary minimum `M*(4)=34`. The original physical DRUP certificates are separate from P0 adaptive results.
2. **0.19 exact:** five-turn preset dictionary minimum `M*(5)=8` on the same ontology, exact horizon profiles and frozen unrestricted P13 receipts. Preserve the original mathematical statements and different degrees of external certification.
3. **0.20 structural:** transported orientation cuts, physical equatorial opacity, rank-seven partition split 16+16, action grammar q3 128 versus q4 512, symmetry orbits 16+8+8, restricted rank-seven-only dictionary minimum 2+6=8 and the explicit noncube R-cycle falsifier. [Real finite independent P1-E proof PASS](https://github.com/WhoSia/CUBE-REV/actions/runs/38039068732); original [0.20 theory](../0.20/P1_E_EXACT_REAL_RUBIK_FACE_GRAMMAR_EQUATORIAL_OPACITY_AND_RANK7_EIGHT.md). Do not conflate this finite court with the separate complete P13 unrestricted mixed-rank lower proof.
4. **0.15 genuine predecessor:** [`urMoveAutomaton`, `adaptiveOrientationDepth`](../../scripts/cuberev-015/ur-fiber-tomography.mjs) already implements an adaptive orientation-only belief search on the same sticker-derived 24-state oracle. This is an inherited baseline, not something to discard or claim to invent in 0.21.

## The first 0.21 physical mathematical problem

Let the original 24 oriented-edge states be `X={0,...,23}`, actions `A` the original 18 legal HTM quarter/half face turns. Each original sticker-derived action `T_a` is a bijection of `X`; observation `o(s)=s mod 2` (up to relabelling of bit zero/one, which does not change identification depth). For nonempty possible-current-state set `B⊆X`, the physically legal observation branch is

`B[a,z]={T_a(s):s∈B and o(T_a(s))=z}`.

A preset word is chosen *before* observations. An adaptive policy chooses the next action from the observation history (equivalently, from a correctly propagated belief state when it is sufficient). These are distinct from **a finite dictionary of independently reset preset words**, as used by the 0.18/0.19 M-star definitions.

Define `W(B,0)↔(|B|≤1)`, and for `d≥1`:

`W(B,d) ↔ (|B|≤1) ∨ ∃a∈A ∀z∈{0,1}, [B[a,z]=∅ ∨ W(B[a,z],d-1)]`.

Then the worst-case adaptive identification depth `D(B)=min{d:W(B,d)}` if this set is nonempty, otherwise infinity. The policy takes **one physical legal face turn per step** and its sensor sees the post-turn tracked-edge orientation. The minimax recursion is an exact finite-horizon Bellman predicate, not a claim about human adaptive strategies.

Immediate mathematical sanity tests:
- For each legal turn `a`, branch sets `B[a,0]`, `B[a,1]` are disjoint and their union is exactly `T_a(B)`.
- Each branch cardinality is at most that of B; the union cardinality stays |B| because all T_a are bijections.
- The number of distinct output histories after a d-depth binary policy is at most `2^d`; hence `D(B)≥ceil(log2|B|)` for any finite D. This necessary bound alone is not sufficient.
- `W(B,d)` is monotone in d; the original `adaptiveOrientationDepth` uses a finite-horizon search and cannot automatically be interpreted as a physically executed full-cube solve.
- Under identical start state and sensor protocol, adaptive minimax for B is at most optimal *single fixed-word* identification depth for B, but comparisons to `M*(4)=34` and `M*(5)=8` are categorically invalid (dictionary size counts independently reset experiments across many requirements, while D counts moves in one adaptive trajectory).

## Planned direct empirical court, no abstract substitution

1. Regenerate `urMoveAutomaton()` from actual 3×3 sticker model, not a guessed 24-state lookup.
2. Recompute and independently compare the historic adaptiveOrientationDepth result for original source supports and additional random or exhaustive small `B` masks; diagnose discrepancies rather than editing old receipts.
3. Produce a machine-checkable policy witness for at least one physical nontrivial source belief, with every nonempty observation branch and final singleton verified by direct sticker-derived transport; compare with preset-word minimum for **the same B**.
4. Test immediate-reward greedy versus worst-case adaptive lookahead with real face turns: either find and publish a physical finite counterexample or publish a negative search domain without extrapolation.
5. Extend only after verifying physically consistent jointly tracked edge/corner transpositions and the observation coordinate conventions.

## Governance and open historical obligations

Never change 0.18–0.20 exact results to make the new problem seem novel. Keep CI `contents:read` and no bot commits; write from WhoSia only. Former `g7/p7/active-set-manifest.json` legacy allowlist failures and distinct unrestricted P13 proof-certification level are historical operational issues, not scientific rewrites. Related follow-on memory, human reactivity, actual WCA speedcubing, FMC and vision reconstruction remain Harvest unless a valid physical causal/measurement bridge is established.

**Canonical live Notion 0.21:** https://app.notion.com/p/3f5ef561cf92815e86efc7d923b6ffa8

**Open research question:** what changes first when an observer switches from an open-loop fixed physical manipulation to a closed-loop state-contingent physical manipulation, and how much of this advantage survives the transition from one tracked UR edge to the joint actual cube state?
