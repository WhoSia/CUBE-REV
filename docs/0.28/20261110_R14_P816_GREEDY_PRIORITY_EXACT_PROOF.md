# CUBE-REV 0.28 — R14-P8.16: Sensor-Type Priority Turns Random Greedy into a Near-Optimal Constructive Policy

**Date:** 2026-11-10. **Status:** exact conditional mathematical result, supported by independent finite rational DP and a direct argument using the already physically certified 156 B6-positive minimum layouts. **Not:** fresh P48 word-distance execution, full-P48 Lean kernel proof, general-purpose group-base approximation ratio, or a claim about paired sticker observation horizons.

## 1. Three genuinely different algorithms; one exact test environment

Fix the original 20 complete original cubie tag sensors, radius-six full-tag observability, and the inherited exact physical 16-tag positive family. Starting from observing ALL twenty tags, iteratively **remove one currently removable sensor** (its deletion must preserve injectivity of the observation map on the entire B6) until none is removable. A removal is successful iff the resulting omitted-tag set remains in the 1,023-member monotone positive omission DAG: 1 at omission size 0, 20 at 1, 174 at 2, 672 at 3, and 156 at 4.

Define these three randomized policies unambiguously:
- **Uniform removable:** at each stage choose uniformly among all currently removable sensors, without regard to cubie type.
- **Corner-first:** if at least one currently removable **corner** remains, choose uniformly among those corners; otherwise choose uniformly among currently removable edges.
- **Edge-first:** exchange corner and edge in the previous policy.

They are not equivalent to drawing a uniformly random final minimal set; a fixed one-pass random sensor permutation would also be a **different** protocol unless one proves equivalence for its precise retry rule.

## 2. Exact outcomes

The exhaustive finite-DAG rational recurrence
\[
p(\emptyset)=1,\qquad p(O\cup\{t\})\mathrel{+}=\frac{p(O)}{|A_\pi(O)|}
\]
where \(A_\pi(O)\) are the **permitted type-prioritized** moves at omission set O, yields:

| Rule | Prob. finish with optimum 16 sensors | Prob. terminate with nonminimum minimal 17 | Expected sensors |
|---|---:|---:|---:|
| Corner-first | **11/12 ≈ 91.6667%** | 1/12 | 193/12 ≈ 16.08333 |
| Unrestricted uniform removable | **1166/1995 ≈ 58.4461%** | 829/1995 | 32749/1995 ≈ 16.41554 |
| Edge-first | **1/2 = 50%** | 1/2 | 33/2 = 16.5 |

All probabilities are exact fractions, not fitted Monte Carlo estimates, conditioned on inherited B6 physical certification.

## 3. Human-readable corner-first proof, without Markov brute force

The first successful removal MUST be a corner because any corner is removable. A second distinct corner can be removed precisely when it is **adjacent** to the first; there are exactly three choices, each equally likely under the rule. A third removed corner would make all resulting sensor sets nonidentifying by the previously certified nonadjacent-corner short-support obstruction and the triangle-free cube corner graph. Therefore the policy next removes an edge.

For the selected adjacent corner pair let h be their original connecting edge. **Every** one of the twelve edge tags can be omitted alongside the two corners and remain B6-identifying because the lone omitted edge is forced fixed by the legal cube orientation/parity invariants. The corner-first policy therefore selects the first omitted edge uniformly from all 12 edge tags. The certified 13-pair admissibility graph P(h) uses **exactly 11 of the twelve edge tags**; its unique isolated vertex is precisely the native core edge h.

- If the algorithm picks h (probability 1/12), the resulting positive 17-tag design is inclusion-wise minimal: no second edge can be omitted, and no third corner is allowed. It terminates at 17.
- If the algorithm picks any other edge (probability 11/12), that edge belongs to at least one certified P(h) pair, and the algorithm can omit a second edge to reach 16. Every 16-sensor identifying design is globally minimum by the exact prior b6=16 certificate. It terminates there.

Thus probability optimal = 11/12, with no history-dependent conditional probabilities or general random-process result required.

## 4. Human-readable edge-first proof

The first two removed edges form a uniformly random unordered pair among all C(12,2)=66 possibilities. Removing a third edge would be nonidentifying because every three-edge omitted set has a certified short physical collision. The policy therefore removes one corner uniformly from the eight. Every 1C+2E triple is positive by the legal cubie stabilizer reduction and the previously certified 66-pair coverage theorem.

A second removed corner is possible iff the chosen edge pair lies in P(h) for some original core h incident to the already removed corner. Among the **8*66=528** equal-probability (corner,edge-pair) triples, the previously established exact geometry gives **264** that extend to some positive 16-tag omission, and **264** that do not. Hence the probability of getting to the global minimum is 264/528 = 1/2, and the other half ends at inclusion-wise minimal 17. This is a complete derivation, not a guess about greediness.

## 5. What was actually tested and where

The existing [R14-P8.15 Python source](../../scripts/cuberev-observation/audit_r14_p815_orbits_exact_greedy.py) now implements THREE exact rational priority recurrences and asserts the new 11/12 and 1/2 fractions, along with the prior 1166/1995 and 829/1995 uniform fractions. The [read-only Actions gate](../../.github/workflows/cuberev-r14-p815-orbits-greedy.yml) requires each of these outputs. Independent local Python code in the research session reconstructed the three recurrences and reported **corner-first 11/12**, **uniform 1166/1995**, **edge-first 1/2**. The committed source itself was not independently run against remote CI yet; classify the new gate as **SOURCE + LOCAL INDEPENDENT MODEL PASS / REMOTE CI UNVERIFIED**.

Do not conflate this with full-source 41-class P48 geodesic replay. No new Drive raw physical data was produced. No global Lean kernel run was inspected. The correct inference is a *conditional algorithmic theorem about the already certified B6 identifying-set family*, not a claim that choosing original corner tags in a different observation model improves performance.

## 6. Research significance and falsifiers

This is an exact separation between **three well-defined local greedy heuristics** on a physically grounded 20-sensor observation set. It gives a concrete positive design principle (prioritize corner deletions) and exposes failure of an apparently symmetric edge-first strategy. It is logically independent of claiming a new NP-hardness result or generic approximation ratio.

Most important falsifier: if the inherited 66-pair coverage, 13-pair P(h) admissibility, original-stabilizer parity, or the complete 16-positive/short-collision certificates are wrong, every derived fraction must be reconsidered. A failure of the exact rational implementation to reproduce the elementary 11/12 and 1/2 hand proofs would also be a coding-error signal. All assumptions remain visibly inherited.

## 7. Next scientific work

1. Independently validate the 41 full-P48 B12 distance classes and the 872 support masks, with raw-preserved inputs, external CI receipts and no bot commits.
2. Consider alternative deletion-order protocols, weighted sensor costs, noisy/broken observations and failure tolerance only **after formally defining new objectives**, not as unqualified comparisons.
3. Instantiate the finite incidence and group action in Lean using legal cube-tag coordinates, and verify the 12 minimal17 orbits and all 66 edge-pair core options in-kernel rather than passing them as unproved assumptions.
4. Preserve Paper B's unrestricted P8.8 h-adaptive 19-frame question as a separate research programme with its original categorical paired-facelet model.
