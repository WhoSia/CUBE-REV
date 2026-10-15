# CUBE-REV 0.25 P0-R6I — Weighted Prefix-Cutset Optimization for Proof-Carrying Cube Search: Regular-Language Cylinder Measures, Compositional Refutation Certificates, Cost-Aware Partitioning & Verified Antichain Reuse

## Current precise scientific status, 2026-10-15

**Official fixed-center original WCA Seoul Summer 2026 3×3 Final A1, unrestricted 18 HTM: the last GLOBAL physical certified shortest-path interval remains 16≤d18(s)≤18.** Full original source-B9 vs solved-B6 zero intersection was certified by [R6E physical Actions #38520307408](https://github.com/WhoSia/CUBE-REV/actions/runs/38520307408). Only the source-B10 U and D first-action cylinders have been physically completed with independent Go receipts ([first-U](https://github.com/WhoSia/CUBE-REV/actions/runs/38525480526), [first-D](https://github.com/WhoSia/CUBE-REV/actions/runs/38524132916)); **16 first-action B10 cylinders remain open**. R6I's math, planning and source-B7 variable-cutset court cannot itself certify global lower17.

## I. Exact conservation law for graded canonical-prefix cylinders

Let A be the exact 18 legal physical HTM action alphabet, with inherited canonical DFA: no two consecutive turns on the same face, commuting opposite-face turns fixed in the increasing face order. Let q_p be the DFA state after legal prefix p, |p|=m≤R, and c(q,j) the number of legal length-j continuation words after q.

Define the IDDFS canonical recursive-CALL mass for the cylinder rooted at p:

    W_R(p) = Σ_(j=0)^(R−m) (R−m−j+1)c(q_p,j).

It counts iterative re-visits, not distinct physical cubies and not CPU seconds. Empty continuation contributes R−m+1; nonempty continuations begin in exactly one allowed next generator. Thus, for every legal prefix p shorter than R:

    W_R(p) = (R−m+1) + Σ_(a in Allowed(q_p)) W_R(pa).

This identity is EXACT at every finite R. Every full cut tree splits nodes into ALL legal children and stops at a prefix-free set P. Let I(P) be the set of its strict interior prefixes. Then:

    N_R = Σ_(u in I(P)) (R−|u|+1) + Σ_(p in P) W_R(p).

No word disappears or appears twice. The statement presupposes a structurally complete prefix tree, not merely a lucky numeric sum. At R=10, the original canonical source IDDFS total N10=285,921,738,920. This is the invariant for every proposed R6I partition, regardless of job count or greedy scheduling policy.

## II. Lean4: variable-depth proof certificates are compositional

[Formal Lean4 WeightedPrefixCutset.lean](../../formal/025/WeightedPrefixCutset.lean) defines a graded variable-depth physical/canonical proof type. A leaf DISCHARGES the entire remaining-depth ordered-action absence obligation with an actual prefix refutation. An internal SPLIT proves the current original full-target absence and supplies a complete child refutation for every DFA-admissible next physical turn. The proof tree carries both the whole physical state and the canonical last-move grammar state.

- weighted_cutset_compose: a complete variable-depth proof tree yields a complete source prefix refutation.
- weighted_cutset_sound: no legal ordered action word of the declared remaining depth reaches the actual target.
- exact_weighted_cylinder_split: the exact finite-call work conservation identity in Lean core over the explicit finite list of allowable next actions.
- weighted_cutset_antichain_reuse: from a proved strong-node cutset refutation, a weak node inherits the certificate only if (1) all weak-node admissible future words are admissible at the strong node and (2) every success word of the weak node is also a success word of the strong node, preserving SAME physical generator order and full grammar context.

This last theorem prevents an unsound cache from equating corners, edge PDB scalars or differently allowed suffix languages. It is a conditional mathematical reuse principle, not an implemented fast physical antichain detector.

[Lean4 CI #38666516207](https://github.com/WhoSia/CUBE-REV/actions/runs/38666516207) initially failed because Finset was unavailable under the repository's lean-core-only imports. The source was repaired to use finite action lists and foldl, and [#38666686777](https://github.com/WhoSia/CUBE-REV/actions/runs/38666686777) completed SUCCESS (15 build jobs). After adding the antichain inclusion theorem, [#38666788536](https://github.com/WhoSia/CUBE-REV/actions/runs/38666788536) also completed SUCCESS. This formalizes the generic implication, NOT original B10 physical geodesic proof.

## III. A spectral Kraft equality for nonuniform Rubik normal-form words

The canonical HTM grammar has six faces with three powers each. Group terminal faces into low {U,R,F} and high {D,L,B}. The low terminal face allows 6 low and 9 high successor actions; the high terminal face allows 6 low and 6 high. Let

    t = sqrt(3/2),   λ = 6+6t = 6+3sqrt(6),   Z=9(t+1).

Assign each action a last-face weight v(a)=t for low, 1 for high. The next-action grammar identities become:

    6t+9=λt,        6t+6=λ.

For each nonempty legal canonical prefix p=a1...am, define the spectral cylinder boundary measure

    μ([p]) = v(am) / (Z λ^(m−1)).

At depth 1, the nine low and nine high actions sum to (9t+9)/Z=1. At EVERY deeper prefix the sum of all legal child cylinder measures equals its parent measure, because the positive eigenvector satisfies Σ_legal a v(a)=λv(last). Thus any finite prefix-free and COMPLETE canonical cutset P obeys the exact weighted Kraft-type equality:

    Σ_(p in P) μ([p]) = 1.

This is not the ordinary uniform b-ary Kraft inequality and is not a distribution over distinct Rubik group elements; the measure is on infinite LEGAL ACTION WORDS. It is a naturally derived finite-state Markov/Parry-type boundary measure. Finite-R call weights W_R differ from μ and should be used, not μ alone, for exact actual IDDFS proof accounting. The spectral equality follows by elementary algebra from the verified normal-form transfer. The real-square-root eigenvector and infinite boundary limit are a paper-level derivation, NOT claimed separately Lean-kernel formalized.

## IV. Cost-aware minimax scheduling: exact mathematics vs explicit hypothetical prices

[Independent Go variable-depth planner](../../scripts/cuberev-025/p0_r6i_weighted_cutset_go/main.go) uses TWO independent exact original 18-symbol grammar counts: a recursive DFA node decomposition and length-by-length 18-letter suffix dynamic programming. Every candidate is a true prefix-free, fully exhaustive tree; its interior+leaf word-call mass is exactly 285,921,738,920. It tests six maximum-leaf budgets and serial longest-processing-time placement on 4 and 8 identical hypothetical workers.

Actual single-shard original physical calibrations: first D B10 561.99s peak1,341,156KiB, first U B10 711.50s peak1,341,212KiB. **An additional 20 seconds per job of goal-ball initialization is an UNMEASURED modeling assumption**, not a measured independent component. Descendant-shard per-word physical cost is extrapolated from its first-action class; actual physical geometry and pruning rate differ across prefixes. The greedy selection is NOT a proof of global minimum schedule among all valid cutsets.

[Read-only Go Actions #38666621086](https://github.com/WhoSia/CUBE-REV/actions/runs/38666621086) COMPLETED SUCCESS. Its exact grammar and hypothetical 4-worker outputs:

| Maximum leaves | Actual leaves | Exact internal calls | Hypothetical runner seconds | Hypothetical 4-worker makespan |
|---:|---:|---:|---:|---:|
|18|18|11|11,461.410|3,108.970s|
|30|29|21|11,681.410|3,108.970s|
|45|43|31|11,961.410|3,006.117s|
|60|60|41|12,301.410|3,117.164s|
|80|74|51|12,581.410|3,173.559s|
|120|116|81|13,421.410|3,397.164s|

With eight hypothetical workers, 18 jobs predict 1,835.480s vs 43 jobs 1,530.492s; 60 jobs rise to 1,584.978s. Therefore **43 is better IN THIS HEURISTIC/UNMEASURED COST MODEL** under those worker counts, NOT a proven optimal cutset nor confirmed physical speedup. Rebuilding ~8.24M complete goal cubies in every independent job introduces real time/memory overhead that the current hypothetical setup parameter may underestimate.

## V. Crucial original 54-sticker physical regression using a real mixed-depth cutset

[Original physical C++17 43-cylinder pilot](../../scripts/cuberev-025/p0_r6i_mixed_prefix_physical_cpp/main.cpp) and [independent Go 18-action audit](../../scripts/cuberev-025/p0_r6i_mixed_cut_audit_go/main.go) execute the concrete frontier: split first physical U action ID0 into its 15 exact legal second-action prefixes and first D ID9 into its 12 exact legal second-action prefixes; leave the OTHER SIXTEEN first actions as length1 leaves. The 43 leaves are prefix-free. The only strict interior prefix states are root [], [0], [9], all checked against the actual complete CP/CO/EP/EO solved-side ball. Original WCA 54-sticker state, 18-turn physical solution, actual 18HTM turns and 4,608 packed-to-complete-physical turn regressions all remain mandatory. Every leaf is exhaustively tested to the given source depth with exact per-canonical-word visited+soundly skipped receipts.

[Read-only physical Actions #38666962684](https://github.com/WhoSia/CUBE-REV/actions/runs/38666962684) completed BOTH original B3/B3 and full original B6/B7 jobs SUCCESS. Actual independent Go receipts:

- B3/B3: 43 mixed-depth leaves, 3 internal nodes, 10 internal IDDFS calls, full canonical baseline3,784=112 actually visited+3,672 safely omitted, entire full cubie goal intersections0, independent Go PASS.
- B6(goal)/B7(source): goal B6=8,240,087 real whole-cubie states, 43 leaves, 3 internal nodes, 22 internal IDDFS calls; **120,213,368=674,769 visited+119,538,599 safely omitted**; full CP/CO/EP/EO intersections0, **19.65s wall and 1,340,432KiB peak RSS**, independent Go PASS.

This certifies a nonuniform ORIGINAL PHYSICAL mixed-depth source prefix cover at R7, not just symbolic regular-language combinatorics. It does NOT certify R10/B6 original global lower17. Comparing 19.65s to a different time/runner is not a defensible speedup experiment; no matched replicated physical D/E/43-way wall comparison has yet been performed.

## VI. Next exact theoretical and engineering agenda

1. **Prove actual optimal cutset under a declared cost objective**, perhaps finite automaton DP tracking a Pareto set (leaf count, depth, exact source call mass, estimated setup cost, max shard, RAM) and independently checking predecessor certificates. The current largest-estimated-leaf greedy splitting policy is a baseline, not an optimality theorem.
2. **Make spectral measure formal and operational:** build algebraic positive eigenvector and Kraft-weight mass conservation in a formal proof; distinguish boundary-measure balance from finite horizon IDDFS counts.
3. **Validate cost assumptions:** separately measure complete B6 goal construction versus original source-prefix projection search, across multiple actual depth2 cylinder prefixes and matched runner/hardware; do not assume repeated 20s setup or uniform physical prune rates.
4. **Antichain reuse implementation:** extract a cheap, checkable finite-depth DFA-language inclusion certificate before applying R6I antichain theorem to prune real original physical source states. Record cache-construction time, retained whole-cubie correctness and RAM; a method that worsens cost is a valid negative result.
5. **Long physical frontier:** 16 other first-action B10 cylinders remain unproved; any global lower17 requires the entire original B10(s)∩B6(e)=∅ or another genuinely equivalent original source-complete certificate. Do not confuse a complete REGULAR WORD decomposition with a completed physical 16-move-exclusion computation.

**Governance:** all Git commits author+committer WhoSia; bot contributions forbidden; Actions contents:read, no writeback; C++17 original physical engine, Go independent DFA/work audits, Lean4 pure mathematics; protected human 451 original reconstructions never publicly exposed.
