# CUBE-REV 0.19 — P6: Collision-Graph Kernel and Restricted Perfect-Hash Families

## Authority and exactness gate
The scientific problem fixes real sticker-derived 18-HTM cube actions, 12 initially flip-zero edge positions, complete intrinsic orientation histories after L physical moves, and the **same original 1192 source subset requirements**. A dictionary succeeds if every admitted source is injectively observed by some selected experiment. The exact M*(4)=34 theorem has externally checked DRUP proofs. For L=5 and L=6 the honest currently established integer intervals remain **6<=M*(5)<=8** and **3<=M*(6)<=4**. No three-word physical L6 impossibility or 7-word physical L5 UNSAT proof is certified in this P6 result.

## Mathematical reclassification — physically constrained restricted perfect hash family
In classical perfect-hash-family notation, a family f_1,...,f_N of functions [n]->[m] identifies each admissible w-subset when one f_j is injective upon it. Our cube experiments h_word:[12]->{0,1}^L are physically realizable members of a severe word-generated subfamily of such maps; the source family is not all w-subsets but a frozen 1192-set, nonuniform family of sizes 3,4,5. Thus CUBE-REV computes minimum cardinality of a **physics-constrained, restricted perfect hash family**. The concept of perfect hashing and probabilistic existence proofs are existing mathematics and are NOT claimed as CUBE-REV discoveries. Reference: Procacci–Sanchis (2017), Perfect and separating hash families: new bounds via the algorithmic cluster expansion local lemma, DOI 10.4171/AIHPD/51, https://www.numdam.org/item/10.4171/aihpd/51.pdf.

The distinctive mathematical contribution, subject to independent novelty comparison, is the exact physical HTM-transducer restriction, nonuniform source-family geometry, sharp finite observation horizons, and proof-carrying exact cover bounds.

## Exact collision-graph formulation, not a relaxation
Let B(w) contain the pairs {i,j} of different initial slots having the same entire L-bit physical observation transcript under word w. The bad-source family of w is F(w)={A in R: exists e in B(w), e subset A}. For any nonempty dictionary D,

`D valid iff intersection_(w in D) F(w) is empty.`

Equivalently, failure occurs iff there is a choice of one collision edge from each B(w) with the union contained in one source A in R. This equivalence holds for all dictionary sizes and can be used for exact k3 and k7 searches. The old 1192-row set-cover encoding and the collision hypergraph are dual descriptions of the SAME finite feasibility problem; do not confuse reduction of descriptive complexity with numerical proof of a stronger bound.

**Sound pair-refinement dominance lemma:** If B(u) is a subset of B(v), then F(u) is a subset of F(v) for every source family R; hence u covers every source distinguished by v and may replace v in any dictionary at no cost. This is a source-family-independent sufficient dominance test. Its converse generally fails: not every source-specific cover-dominance relation is a raw collision-graph edge inclusion.

## Local length-six restricted physical partition audit
Previously materialized real physical length-six candidate exporter enumerates exactly 4,350,976 action words meeting 3<=q<=5 flip-capable F/F'/B/B' quarter turns. It emits 53,528 **distinct observation partitions of rank >=5**; q<=2, q=6 and rank<5 words are excluded by this particular generation rule. Note carefully: this 53,528 count is NOT the count of all length-six physical partitions, nor has it been proved that the omitted partitions are irrelevant to the minimum three-word dictionary.

Physical rank >=5 partitions break down as 25,821 rank5; 23,439 rank6; 4,072 rank7; 152 rank8; 44 rank9. Exact collision-edge subset dominance on these 53,528 partition types, using 66 possible unordered start-state pairs and an independent C++ kernel, retains **18,813** undominated collision graphs and proves that every deleted member may be replaced by a retained stronger physical word *within this restricted family*. New public executable: scripts/cuberev-019/L6_collision_refinement_kernel.cpp. This is a sound candidate-kernel improvement, **not** an exact all-physical k3 impossibility proof.

All 44 choose3 = 13,244 triples of the rank9 words were checked: none covers all 1192 source requirements; their best leaves exactly **4** unmet requirements. All 196 choose3 = 1,235,780 triples among rank8+9 candidates likewise leave at least **4** unmet requirements. This is an exact diagnostic within selected physical candidates but not a theorem ruling out lower-rank words.

A 27-profile coarse model that records only (F,B,N) source-composition types allows a three-word solution and has fractional LP cost 2.4. This is demonstrably too weak to infer the physical three-word exactness: it discards the positions of which source sets overlap. (The L5 initial 9-profile reduction suffered the analogous failure.)

A separate global numerical MIP attempt with 53,528 word columns and the 1192 source constraints exceeded the local computational budget and made **no** certificate-backed SAT/UNSAT finding. No exact M*(6)=4 promotion follows.

## High-rank collision structure
Every physical L6 word of rank9 among the 53,528 restricted candidates has exactly three size-two collision classes: one pair inside each of the physically distinguished position quartets F={1,5,8,9}, B={3,7,10,11}, and N={0,2,4,6}. There are precisely 44 distinct such partitions in the tested restricted family. This suggests an orbit-level matching/orthogonality model, but an abstract matching argument must retain the original nonuniform 5-source admission rules to be sound.

The strongest pairwise rank>=8 physical observations still leave at least 38 source requirements ambiguous among rank9/rank9 candidates, 68 among rank9/rank8, and 103 among rank8/rank8. A third observation could conceivably remove these residual failures, so those pairwise counts are not a negative proof.

## Next proof-preserving plan

1. **Completeness gate for k3:** Either enumerate and retain all remaining length-six physical partitions, or prove q<=2, q=6 and rank<5 words cannot occur in any three-word optimal dictionary. Without one of these gates, the 18,813 kernel cannot support an exact lower bound.
2. Build **collision hypergraph incidence** rather than 1192-row dense MILP: use initial-state collision pair choices and `F(w)` sets; condition on symmetry-orbit representative first word, derive residual constraints; prefer provable k-aware reductions and independent proof receipts.
3. Test structured 9-history three-matching subcase, then 8/7/6-history branches. Certified symmetry and dominance breaking literature: Bogaerts–Gocht–McCreesh–Nordström (2022/2023), DOI 10.1609/aaai.v36i4.20283, free author version https://jakobnordstrom.se/docs/publications/CertifiedSymmetryDominanceBreaking_AAAI.pdf. Classic branch-and-reduce exact set-cover methods can inspire sound reductions, but new rules need formal proof.
4. L5 remains independently hard: current lower bound 6, upper 8, fractional LP 16/3, k6 first-column symmetry branches 5 unresolved, k7 SAT remains open. Reusing a valid L6 structural lemma requires the correct original source family and independent physical source hash.

## README and historical custody

The root research/current README previously incorrectly claimed 0.18 was the sole open version and M*(4) exactness remained pending. The full old README is preserved in GitHub archive/readme/README_RESEARCH_CURRENT_PRE_019_20261010.md, original blob e795d39b2baabb65f91d1ae487f47d73ab77eff1. Superseded 0.18 status paragraphs were uploaded **verbatim as Markdown** to Google Drive CUBE-REV/90_RESEARCH_CURRENT_ARCHIVE/CUBE_REV_README_018_SUPERSEDED_STATUS_PARAGRAPHS_20261010.md (file 1Ny5Jr0HNYFD1FcVda6kaEyoNbmhuDJC9; SHA256 7bcd81d51c849905699af25d615f1e066ee283494087c78443e0d8e58382589a). Root README now points to the current mathematical horizon profile and proof boundaries without deleting historical scientific material.

## Current GitHub / documentation citations
- 0.19 canonical Notion: https://app.notion.com/p/3f4ef561cf92813d9edfff4911db39d2
- 0.19 P5 observation-horizon theorem: docs/0.19/P5_EXACT_OBSERVABILITY_HORIZONS_COLLISION_PAIRS_AND_ADAPTIVITY.md
- 0.19 P3/P4 integer gap and conditional-dual framework: docs/0.19/P3_GEOMETRIC_SYMMETRY_EXACT_LP_GAP_AND_K7_METHOD.md and docs/0.19/P4_CONDITIONAL_INTEGER_DUALS_AND_K7_HIGHER_ORDER_CUTS.md
