# CUBE-REV 0.28 — R14-P8.12: Minimal-17 Tagged Sensors and Four Newly Read Primary Papers

Date 2026-11-10. Status: mathematical deduction conditional on the previously certified complete physical B6 16-tag classification; new independent finite geometry PASS; NOT a fresh 41-class original-HTM MITM re-run, complete minimal-size spectrum or Lean-kernel certification.

## 1. Intake and actual text reading

Four newly placed PDF files in the central Research OS 00_INTAKE were identified by reading the scholarly PDF body (rather than relying on filename), renamed in the established author-year-title-publication convention and moved in place to the central 10_PAPERS folder. Each original ID, new title, PDF byte size and target parent was verified via a new Drive metadata read. The original bytes were NOT re-uploaded or SHA-256 checked this cycle.

| Source and issue | Original Drive ID | Distinct research effect |
|---|---|---|
| Dalla Volta, Mastrogiacomo & Spiga (2024), On the Cardinality of Irredundant and Minimal Bases of Finite Permutation Groups, Journal of Algebraic Combinatorics 60:569–587, DOI 10.1007/s10801-024-01343-w | 1PSR0EbmFyavef6cl4HKLmrHhW7p1f6x7 | Thm 1.1: possible irredundant ordered-group-base lengths form an interval; Thm 1.2: inclusion-wise minimal unordered-group-base sizes need not form an interval. The radius-restricted Rubik case does not literally meet the global group-base hypotheses. |
| Smetsers, Moerman & Jansen (2016), Minimal Separating Sequences for All Pairs of States, LATA 2016 LNCS 9618:181–193, DOI 10.1007/978-3-319-30000-9_14 | 1uGE1727C2GeMbgtaOcjdqpRkxzd_df7- | O(m log n) partition refinement returns shortest sequences for pairs of inequivalent FSM states, improving Moore's O(mn) algorithm. Not an optimal single global adaptive tree. |
| Alur, Courcoubetis & Yannakakis (1995), Distinguishing Tests for Nondeterministic and Probabilistic Machines, STOC 1995:363–372, DOI 10.1145/225058.225161 | 1Jc4Ke2cK2aSSDh2cf17705Mx5UMul8DS | Preset existence PSPACE-complete; adaptive existence EXPTIME-complete in the specified nondeterministic/probabilistic models, NOT a new complexity classification of deterministic P48. |
| Chow (1978), Testing Software Design Modeled by Finite-State Machines, IEEE TSE SE-4(3):178–187, DOI 10.1109/TSE.1978.231496 | 1PLcpu5vjALMj04Ue59BbTU7lB-_PrDbB | Definition 7 explicitly calls a characterization set an input-word set distinguishing each pair. W-method assumes a specified minimal/reachable fixed-start FSM model, not our full-group color-pair game. |

## 2. New conditional theorem: there are twelve minimal but nonminimum 17-tag B6 designs

Let O consist of all 8 tagged original corners and 12 tagged original edges, and B6 be the symmetric 18-HTM radius-six ball. Full-tag observation reports original cubie position plus orientation. For an original edge h, let d(h) be its two endpoint original corner tags and define the 17-observed-tag set:

S_h = O minus (d(h) union {h}).

Claim: all 12 S_h are B6-injective, and each loses B6-injectivity after removing ANY one of its 17 observed tags. Thus the inclusion-wise minimal identifying set cardinality spectrum M6 contains both 16 and 17, and there are AT LEAST 12 minimal/nonminimum 17-tag sets.

**Positive proof.** In the entire legal Rubik cubie group, stabilizer H(d(h),{h}) of all other original oriented tags has three elements: identity plus the two balanced twists of the pair of omitted corners. With only one omitted edge, its permutation and flip are necessarily identity by legal permutation parity matching and total flip parity; only balanced twists of two omitted corners remain. Thus H(d(h),{h}) = H(d(h),empty). For each h, the previously physically certified 16-tag positive classification has 13 allowed omitted-edge pairs P(h). Pick any p in P(h). Then H(d(h),empty) is a subgroup of H(d(h),p), and the existing complete 41-geodesic-class positive certificate proves H(d(h),p) intersection B12 = {identity}. Therefore H(d(h),{h}) intersection B12 = {identity}. By the established radius-doubling lemma S_h identifies B6. This step inherits an earlier physical positive certificate; the newly executed source does not recheck 41 HTM classes.

**Minimality proof.** Every valid 16-tag design, according to the inherited 4,845-complete physical classification, omits precisely two adjacent corners d(k) plus a 2-edge pair in P(k). The certified 13-pair omitted-edge graph P(h) has structure W5 disjoint-union C4 disjoint-union K2 disjoint-union K1, with its unique isolated vertex equal to the core edge h. Remove one tag from S_h. If it is a corner, the resulting 16-tag set omits three corners and is not one of the 156 valid layouts. If it is an edge e, its omitted pair {h,e} is not in P(h) because h is isolated. Therefore all immediate size-16 subsets fail. By monotonicity of observation sufficiency, all still smaller subsets fail. QED.

The twelve core edges give twelve distinct S_h. For each h and **any** edge e, the same whole-group stabilizer equality proves that omission d(h) union {e} is B6-positive. Thus all 12*12=144 two-adjacent-corners-plus-one-edge omission triples are valid 17-tag layouts. For each fixed h, 11 of the 12 possible e are vertices of at least one edge of P(h), and these 132 layouts contain a valid size-16 sensor subset. Only e=h in each of the 12 cores is not extendable to any valid four-tag omission; these twelve are exactly the inclusion-wise minimal 17 designs IN THIS SPECIFIED SECTOR. No conclusion is drawn about every other 17-tag layout or larger minimal cardinalities.

This new result is distinct from the repository's EARLIER 2026-11-03 explicit matroid-basis exchange counterexample, which remains older prior work. Do not claim new general matroid exchange theory.

## 3. Independent geometry check and evidence levels

New source: scripts/cuberev-observation/audit_r14_p812_minimal17_sensor_spectrum.py. It runs the earlier precise 13-pair geometric criterion for all 12 h, verifies that h is the only isolated edge tag per h, reconstructs all 156 valid 16-tag omitted designs, and rejects each of 12*17=204 putative 16-tag deletions.

A SECOND local Python implementation, independently reconstructed from the face-normal vectors, returned GEOMETRIC_INDEPENDENT_PASS with exact output: positive16=156; positive17 in chosen sector=144; 17 layouts containing a valid size16 subset=132; minimal17 in chosen sector=12. This independently validates geometry, NOT 54-facelet distance closure or original source bytes.

## 4. Methodological pairwise-versus-global caveat from new Smetsers paper

With the ideal P48 complete legal state geometry, the entire vector of 48 moving facelet colors uniquely determines the configuration. Any two distinct original cube states therefore differ at a single named edge or corner facelet slot. As each of 24 edge-facelet slots and 24 corner-facelet slots can participate in a physically routable paired query, there exists a query that separates THAT PAIR in exactly ONE paired read. Consequently the largest shortest pair-separating length is 1, despite the proven GLOBAL adaptive minimax lower bound 18. The pair-specific query depends on the two known hypothetical states; it is not one universally distinguishing query for all hidden states. Thus generic shortest pair-separator algorithms may help with conditional beliefs, but their maximum output length cannot be promoted to a nontrivial unrestricted P8.8 lower bound.

## 5. Updated missing-original and literature gates

REMOVE from former ten missing papers: Dalla Volta et al. 2024; Smetsers et al. 2016; Alur et al. 1995; Chow 1978. These are now canonical owned PDFs.

Remaining earlier SIX original-full-text gaps: Harary & Melter (1976), Slater (1975), Hennie (1964), Vasilevskii (1973), Hopcroft (1971), Sokolovskii (1971). Existing publisher correspondence for Harary/Slater should be checked, not duplicated. Exact source edition/translation may need more work for Vasilevskii and Sokolovskii.

Additional newly revealed original-article candidates not located in scoped Drive searches:
- Cameron & Fon-Der-Flaass (1995), Bases for Permutation Groups and Matroids, European Journal of Combinatorics 16(6):537–544, DOI 10.1016/0195-6698(95)90035-7.
- Tarski (1975), An Interpolation Theorem for Irredundant Bases of Closure Structures, Discrete Mathematics 12(2):185–192, DOI 10.1016/0012-365X(75)90033-3.
- Lucchini, Morigi & Moscatiello (2021), Primitive Permutation IBIS Groups, JCTA 184:105516, DOI 10.1016/j.jcta.2021.105516. University author manuscript available at https://hdl.handle.net/11585/846160.

Do not label the PDFs absent from the ENTIRE Drive corpus: these are negative targeted title-and-author searches plus separate original-ID checks, not an all-file byte census. Bailey & Cameron 2011, Boutin 2008, Cameron 1999, Gill 1961, Lee & Yannakakis 1994, Soucha & Bogdanov 2020, Angluin 1987, Hierons & Türker 2016/2017 and the other already audited originals ARE owned.

## 6. Next scientific and formal proof gates

P8.12: establish the exact full minimal-size spectrum M6, starting with 17-tag arrangements that omit three corners or one corner and two edges. A computed geometry-only count is insufficient; any newly claimed B6-positive case needs physical stabilizer support plus the exact B12 search or monotonic proof from inherited positive cases.

P8.8: 19-frame full P48 mixed-mate strategy versus universal collision/adversarial obstruction remains OPEN. Existing fixed-first-twelve lower 20 is restricted.

P8.9/P8.10: Lean generic covariance/adversary modules are source pending actual kernel verdict; physical P48 transport and original 384/2,304 collision witness import remain separate.

Paper A: new 17-minimal spectrum corollary should appear after central minimum16/156 classification, not replace the main certified physical statement. It is a conditional consequence of source 41-class positive and 4,845-layout complete negative proofs.

Raw PDFs remain in Drive; GitHub artifacts are researcher-level T1 evidence and must be human WhoSia-authored on research/current. No bot writeback or unverified remote CI PASS.
