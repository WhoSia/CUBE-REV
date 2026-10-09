# 0.17 internal P1 — size-independent candidate domination for the original four-turn dictionary

**Exact original problem:** U contains the 1,192 eligible 3/4/5-original-edge-position source bases from 0.16 P5; C(w)⊆U is the collection separated by one exactly-four-HTM-action word w with known initial flip0. M* is the minimum number of words whose C(w) union is U.

## General replacement theorem (hand proof; valid for ALL k)

If `C(u)⊆C(v)`, then any separating catalogue containing u can replace u by v without losing any covered target. If v was already in the catalogue, u may simply be deleted. Consequently there exists a cardinality-optimal solution using **only inclusion-maximal covering families C(w)**. This theorem needs NO weighted-dual-score restriction, no hypothesis that the catalogue size is24, no group symmetry assumption and no MILP. It remains valid for k=25 and all other k.

## Exact model-relative census and limitation

Reconstruct 18^4=104,976 literal words from the original independently frozen 24-edge-state action maps, collapsing to **1,913 distinct output partitions** on the twelve known-flip-zero initial edge slots. From those partitions derive coverage on all **1,192 admissible minimal basis sets** (220 triples,492 quadruples,480 quintuples). Exactly **1,477 different basis-coverage bitsets** arise, including an empty pattern. Removing every bitset dominated by another leaves **1,323 inclusion-maximal candidate families**. The union of these still covers all1,192 mandatory bases. Thus the complete M* problem can be restricted to this 1,323-family set **for ANY cardinality**, including a possible 25-word solution.

The reduction is real but modest (1,913→1,323; not 1,913→168). The earlier 168 near-tight partition restriction was sound only within a HYPOTHETICAL 24-word contradiction and cannot be imposed on k25. A representative cost histogram across the inclusion-maximal families of the frozen P6 weighted dual is: {0:727,4:340,8:76,12:12,16:6,20:162}. **Low dual-weight families must not be silently discarded**: some may distinguish otherwise challenging zero-dual-weight bases.

An independent local Python full1192-basis/1913-partition incidence check returns exactly the same counts. [Public physics-grounded Node regression](../../scripts/cuberev-017/test-global-dominance-court.mjs) derives its 104,976 actions directly from the 0.15 physical oracle, without trusting the private 1913-partition JSON. A numerical full 1,323-candidate MILP with nonzero relative optimality gap returned a 36-word feasible catalogue (worse than the already certified 34-word upper), and **no new exact optimum**. It cannot be used to claim a 31-word lower bound or M*=36.

## Valid k=25 numerical slack invariant

Retain the 60-positive-basis rational dual numerator sum 476 and per-word positive mass ≤20. For any hypothetically successful **25**-word catalogue, total unused weighted capacity is at most `25·20−476=24`. Each selected word of mass c consumes defect `20−c`. Thus, without restricting ALL words to the old 168 classes, a 25-word solution must satisfy the EXACT necessary budget inequality:

`Σ_(selected words) (20−c(w)) ≤ 24.`

For example at most one zero-mass word can appear; at most one mass4 word can appear; and the summed deficits of any mass8/12/16 words must fit the remaining budget. This is a **NEW SOUND 25-SPECIFIC BRANCH BUDGET**, unlike the invalid 24-only near-tight exclusion. It does not prove 25 infeasible. A future exact solver should combine (i) inclusion-maximal basis-coverage masks, (ii) this 25-word weighted defect budget, (iii) the 1,132 original zero-dual basis constraints and (iv) independently checked nonexistence certificates.

**Current certified interval:** 25≤M*≤34. No false discovery of M*=25 or M*≥26.
