# CUBE-REV 0.28 — R14-P7.4: Six-edge color-graph orbits, constructive depth upper bounds, and bounded exact lower court

**Research date:** 2026-11-09. **Status:** Independent exhaustive 924-set graph classification; 30 representative deterministic policy executions of all 11,520 parity-conditioned initial states each; exact AND–OR impossibility calculation for **12** of 30 representatives. The other 18 exact minimax lower tests are **NOT certified** by this experiment. Original full physical paired-probe horizon remains **18 ≤ h_adaptive ≤ 21, OPEN**.

## 1. Model and precise domains

Fix any six distinct edge cubie color types from the twelve edges of the cube-color graph `K_(2,2,2)` (opposites UD, RL, FB). Suppose the residual permutation parity and edge-flip parity are known. We execute the even-even reference domain

\[
|X_L|=\frac{6!}{2}\,2^{6-1}=11,520,\qquad |Q_L|=12,
\]

with a query reading exactly one of twelve spatial facelet slots. Legal words are all even permutations of the six original edge labels and flip vectors of even total sum. This is an **edge-only conditional game**, not the coupled 12E/8C physical inverse problem.

## 2. Exact graph automorphism classification (complete)

Independently enumerating all `6!=720` color permutations and retaining the 48 that preserve the three opposite pairs, or separately enumerating `3! × 2^3=48` maps, gives the same orbit partition on all `C(12,6)=924` unordered edge-label type sets.

| Abstract graph orbit size | Orbits | Label sets |
|---:|---:|---:|
| 48 | 14 | 672 |
| 24 | 6 | 144 |
| 16 | 1 | 16 |
| 12 | 7 | 84 |
| 4 | 2 | 8 |
| **Total** | **30** | **924** |

This classification is exact for the abstract edge-label graph. A graph color automorphism is not automatically a legal 48-sticker corner/chirality transformation; any physical P48 claim needs separate proof.

## 3. Executed one-step policy upper bounds (complete on the 30 representatives)

For each orbit representative, explicitly build all 11,520 legal six-edge states, and recursively evaluate the simple deterministic one-step policy

\[
\pi_{\rm few}(B)=\mathop{\rm argmin}_{q}\big(\max_c|B_{q,c}|,\ \#\{c:B_{q,c}\neq\varnothing\},\ \sum_c|B_{q,c}|^2,\ q\big).
\]

The producer reconstructs each original state in every representative by following the chosen query tree to the **correct singleton** (30×11,520 = **345,600** explicit target replays). Its full worst-case representative depth distribution is **3 orbits at depth 7, 25 at depth 8, and 2 at depth 9**. Weighting these **representative** depths by abstract orbit sizes gives 20 / 832 / 72 original type sets at representative depths 7 / 8 / 9, respectively.

**Precise caveat:** The weighted result is an **orbit-weighted statistic of the representative policy**, NOT 924 separately executed greedy policies and not 924 exact minimax depths. The fixed query-index tie-break of `π_few` need not itself commute with an arbitrary source-color graph symmetry; a transported policy, rather than an independently recomputed greedy policy, would be required to transfer a constructive upper bound. Such a transport can be implemented by an explicit signed coordinate bijection after proving parity and flip behavior. This paper does not silently assert it.

## 4. Exact restricted lower gate (12 of 30 representative courts)

For each completed representative, an independent script uses the **full AND–OR feasibility recursion**

\[
\mathrm{Win}(B,k) = (|B|=1)\ \lor\ \bigvee_{q}\bigwedge_{c:B_{q,c}\neq\varnothing}\mathrm{Win}(B_{q,c},k-1)
\]

and establishes `Win(X_L,D_few(L)−1)=false`, so the known constructive policy is exactly minimax on the **12 checked representatives**. This includes a depth-9 representative on which the entire 8-read decision tree was ruled out by the exact recursion. The 12 lower-positive results are in the checkpointed JSON receipt, with the number of visited AND–OR belief-budget nodes per representative.

**Do not promote** to a 30-representative theorem or a 924-label-set exact-depth classification: 18 representatives remain unchecked by AND–OR; prior timed runs stopped before completing them. The lower script writes partial receipts after each successful representative, and individual exact checks on difficult sets may require further pruning, branch-and-bound or distributed memoization. The independent checker **recalculates the entire 924-member graph partition**, validates every reported 30 representative policy receipt and 12 lower receipt, but does **not** execute the full Bellman search on all 12 again. These are distinct evidence grades.

## 5. Falsification and next serious steps

1. Complete exact lower proof for the remaining 18 six-edge representatives. A single counterexample `Win(X_L,D_few−1)=true` would falsify one-step optimality and requires a concrete winning alternative policy; do not mask it by adjusting the tested set.
2. Prove a source-color automorphism induces an **explicit bijection of parity-conditioned state words and spatial query locations**, including corrections to permutation sign and total flip, then independently replay transported policies on all **924×11,520=10,644,480** target states if full direct verification is desired. The abstract orbit set census alone cannot justify unchanged literal policy tie-breaks.
3. Return to full coupled parity `B=E_0×C_0 ∪ E_1×C_1`, stationary pair P48 legal routing and **mixed partially observed** edge/corner prefixes. Even a complete six-edge parity-oracle residual table does not automatically solve the 20-frame global problem.
4. Run read-only CI and check actual remote green status before release; no claimed remote CI success in this court.

## 6. Machine artifacts / proof custody

- `scripts/cuberev-observation/audit_r14_p74_six_edge_orbit_policy.py`: full exact orbit partition and complete 30 representative one-step policies, with 345,600 independent target replays.
- `scripts/cuberev-observation/audit_r14_p74_six_edge_exact_representatives.py`: exact AND–OR D−1 lower for prefix of representatives; writes a checkpoint JSON after **each** completed representative.
- `scripts/cuberev-observation/verify_r14_p74_six_edge_orbit_and_eight_lower.py`: fully independent graph automorphism enumeration (all 720 face permutations) and audit of current lower receipt. The source filename is historical; script reads **current** lower count (12), not a hard-coded eight.
- `R14_P74_SIX_EDGE_ORBIT_POLICY_RECEIPT.json`: 30-row actual policy execution and state replay counts.
- `R14_P74_SIX_EDGE_EXACT_REPRESENTATIVES_RECEIPT.json`: **12-row partial** exact minimax lower proof receipts.
- `R14_P74_INDEPENDENT_GRAPH_CENSUS_RECEIPT.json`: independent 924-type graph orbit and receipt consistency audit.

All SHA256 provenance should be preserved from the exact local bytes, and Drive RAW read-back should precede claims of `BYTE_VERIFIED`. An unrun CI workflow is not evidence of CI success.
