# CUBE-REV 0.28 R14-P8.15 — Rotation Orbits and the Exact Greedy-Deletion Law

**Date:** 2026-11-10. **Source status:** new independent finite geometric enumeration and exact rational Bellman/Markov recurrence, conditional on the inherited complete physical B6 16-tag certification and short-support obstruction witnesses. The new program was independently prototyped and run in this session. This is not a new 41-class B12 physical MITM run, not a Lean kernel proof of Rubik geometry, and not a proof of the unrestricted P8.8 19-frame adaptive-color question.

## 1. First theorem: only 12 types of minimal 17-sensor design up to proper cube rotation

The 276 inclusion-wise minimal, nonminimum 17-tag B6 identifying sets of P8.13 have these orbits under the group of 24 orientation-preserving spatial cube rotations:

| Omitted sensor types | Number of proper-rotation orbits | Orbit size | Labelled designs |
|---|---:|---:|---:|
| 2 adjacent original corners + their incident original edge | 1 | 12 | 12 |
| 1 original corner + 2 original edges | 11 | 24 each | 264 |
| **Total** | **12** | | **276** |

The 1C+2E result is independently interpretable without treating the number 264 as opaque enumeration. Fix a corner c. Its stabilizer in the 24-element proper rotation group is the cyclic threefold group C3. The 33 eligible omitted-edge pairs that yield minimal17 layouts are permuted by this C3. Every nontrivial C3 rotation acts on the twelve edge slots in four cycles of length 3, so it fixes NO unordered pair of distinct edges. Thus the C3 action on the 33 minimal pairs is free, splitting into exactly 33/3=11 local orbits. Moving c among eight corners creates 11 global 24-member orbits. In the 2C+1E type, the omit-core-edge design is determined by one original edge h, and the twelve cube edges form one proper-rotation orbit; it has stabilizer size two and orbit size twelve. No orientation-reversing reflections were used.

The 156 **minimum** size-16 sensor layouts, separately, form eight proper-rotation orbits. This supplies a more discriminating test than total count 156/276 alone.

## 2. Second theorem: exact distribution of random greedy sensor deletion

**Precisely defined policy.** Start with all 20 original tagged-cubie sensors. At each step identify *all* currently removable sensors whose deletion keeps the B6 state-observation map injective; choose one uniformly at random and remove it. Stop when none is removable. There are at most four successful removals. This policy is not a uniform random sample of the 432 terminal minimal sets; nor is it by definition a one-pass fixed random permutation of candidate sensors. Every completed run outputs a minimal, not necessarily minimum, design.

Let o be the omitted-tag subset, and \(\mathcal P_k\) the valid omission subsets of size k, k=0..4. The 20+174+672+156+1 = 1,023 valid omissions are the states of this monotone finite DAG. Let \(A(o)=\{t\notin o:o\cup\{t\}\in\mathcal P_{|o|+1}\}\) and \(p(o)\) be the probability of reaching o. Starting with \(p(\varnothing)=1\), every valid transition satisfies

\[
 p(o\cup\{t\})\mathrel{+}=\frac{p(o)}{|A(o)|},\qquad t\in A(o).
\]

A state with \(A(o)=\varnothing\) is terminal; its observed-sensor count is \(20-|o|\). **Using exact arbitrary-precision rational arithmetic**, exhaustive dynamic programming returns:

\[
\boxed{\Pr(\text{minimum size 16})=\frac{1166}{1995}\approx0.584461153},
\]

\[
\boxed{\Pr(\text{nonminimum minimal size 17})=\frac{829}{1995}\approx0.415538847}.
\]

The exact mean number of retained sensors is \((16\cdot1166+17\cdot829)/1995=32749/1995\approx16.415538847\). Thus a naive successful-deletion greedy policy has a **strictly positive probability of missing the known optimum**, even though every chosen deletion preserves correctness and only 20 sensors are present. This is a concrete algorithmic and educational counterexample in a physically grounded observation model; it is not a general NP-hardness theorem or a comparison with an optimal random algorithm.

## 3. Output-bias theorem: symmetry of labels is not uniformity of all minimal layouts

The endpoint probabilities are constant inside each proper rotation orbit (all actions and their uniform probabilities are rotation-covariant), but **not necessarily equal across different orbits**.

- The eleven 24-element minimal17 1C+2E orbits each have mass **241/6650**. Equivalently each of their 264 individual terminal states has mass **241/159600**.
- The one 12-element minimal17 2C+1E orbit has total mass **337/19950**. Its individual layouts have mass **337/239400**.
- The 156 minimum 16-sensor outcomes occur with **five different per-layout probabilities**: mass table (frequency of labelled layouts) **8143/2872800:48; 53/11970:48; 2843/718200:24; 53/17955:24; 1397/239400:12**. These five values are distributed across eight proper-rotation orbits. An initial proposal that the uniform greedy rule would sample all 156 minimum layouts with identical probability is **falsified** by the exact enumeration; do not repeat it.

A fully separate Python prototype of the finite geometry, 24 spatial rotations and exact rational recursion produced the same **12 minimal17 orbits, eight minimum16 orbits, 1166/1995 and 829/1995**. A seeded 100,000-run Monte Carlo check (seed 20261110) independently yielded 58,413 16-sensor terminal runs and 41,587 17-sensor runs, compatible with exact probabilities. Simulation is diagnostic only; the rational recurrence is the proof object.

## 4. Reproducible regression contract

[New independent script](../../scripts/cuberev-observation/audit_r14_p815_orbits_exact_greedy.py) reconstructs the cube from six outward unit face normals, makes the 13-pair admissibility rule at all 12 edge cores explicit, enumerates all legal identifying omissions of size 0..4, and builds all 24 determinant+1 signed coordinate permutations. It verifies covariance of all 276 minimal17 sets, 12 proper-rotation orbits, eight minimum16 orbits, exactly 432 terminal states, exact rational terminal probabilities, per-layout 16-sensor bias and independently seeded random deletion.

For a **strictly independent alternative implementation**, compare the loop over all P(k) with an inverse recurrence from terminal sets (backward dynamic programming) or a small labelled state Markov-chain linear solve; neither source should assume the claimed fractions beforehand. The new script itself asserts expected fractions as a regression gate, and is conditional on the inherited physical 16-sensor and 3-edge/2-corner short collision results.

No one should claim Lean-certified proof or a new physical 41-class distance run merely from the script or CI PASS. Raw T2 P48 sources and their Drive byte receipts remain prior custody obligations.

## 5. Research meaning, literature and future work

**Cameron & Fon-Der-Flaass (1995)** and **Dalla Volta–Mastrogiacomo–Spiga (2024)** explain the distinction among bases, irredundant bases and matroid-like exchange in other global permutation-group models; neither implies this exact B6 restricted-region greedy law. **Blaha (1992)** studied minimum permutation-group bases and greedy approximation in a much more general setting, not our 20-fixed-tag Markov distribution. The meaningful new question is how \(\mathcal M(B_r)\), the geometry of its exchange adjacency and the distribution of concrete sensor-selection algorithms change with radius r. In future, vary sensor cost, fault/erasure tolerance, and observation-output richness under explicitly new mathematical models.

**Paper A:** Promote only after its central physical B6=16 and 156 positive layouts, 872 negative short-support family and 41 positive geodesic classes are source-first independently auditable. The new 432-family and 12-orbit and greedy probability results are dependent corollaries, not substitutes for the primary certificate.

**Paper B:** Full-group paired-color h_fixed=21, 18<=h_adaptive<=20 and the truly unrestricted 19-frame existence/obstruction are untouched. Counts for full tagged-cubie sensors must not be mixed with paired sticker-frame costs.

**Lean:** P8.9/P8.10 generic files remain SOURCE_PENDING_KERNEL until an actual completed job is inspected. A physically meaningful next bridge should encode the 24-element proper rotation action on 20 cubie-tag slots and the 66-pair incidence, then prove with exact computational reflection or native finite enumeration that the 12 P8.15 orbit representatives are complete. This would make the new theoretical corollary independently kernel checkable while keeping physical-geodesic assumptions explicit.

**Scientific custody:** WhoSia human-authored commits to research/current; read-only GitHub Actions, Notion interpretation, Drive raw paper/P48 evidence custody unchanged. No new user 00_INTAKE batch was requested or modified in this unit.
