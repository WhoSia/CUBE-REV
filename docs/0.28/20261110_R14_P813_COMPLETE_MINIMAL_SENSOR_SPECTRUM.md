# CUBE-REV 0.28 R14-P8.13 — Complete Minimal B6 Sensor Spectrum

Date: 2026-11-10. Status: new mathematical consequence CONDITIONAL on previously certified physical B6 16-tag complete positive/negative and short-support certificates. Independent finite 20-tag geometry census PASS; NOT a new Rubik 18-HTM source-complete geodesic computation, full-group Lean kernel result or independent T2 seal.

## 1. Exact statement

Let Ω consist of 8 persistently labelled original corners and 12 original edges of the legal fixed-centre 3×3 cube. The sensor set S⊆Ω reads complete original cubie location/orientation, and S is B6-identifying if its joint readout is injective on the symmetric 18-HTM radius-6 ball. It is inclusion-wise minimal if S identifies but no proper subset does. The complete size census is:

| Number of observed tags | Total candidate sets | Identifying sets | Inclusion-wise minimal |
|---:|---:|---:|---:|
| 16 | 4,845 | 156 | 156 |
| 17 | 1,140 | 672 | 276 |
| 18 | 190 | 174 | 0 |
| 19 | 20 | 20 | 0 |
| 20 | 1 | 1 | 0 |

By the inherited 15-tag exclusion, no smaller sensor set identifies. Thus the COMPLETE minimal size spectrum in this exact physical B6 model is M6 = {16,17}, with 156+276=432 inclusion-wise minimal identifying sets. For 17 sensors, 12 minimal omit 2 adjacent corners + 1 edge, and 264 minimal omit 1 corner + 2 edges. The old P8.12 theorem constructed only the first 12; it remains true but is now strictly strengthened.

## 2. Conditional proof: exhaustive omitted-tag types

Write O=Ω∖S. Exact B6 identification is equivalent to H(O)∩B12={identity} under the inherited symmetric 18 HTM radius-doubling lemma.

Inherited physical inputs:
(A) exactly 156 positive size-16 original-tag layouts, each omitted 4-tag pattern consisting of 2 adjacent corners ∂h plus an edge pair in a 13-pair family P(h), for 12 original cube edges h; all 4,689 other omission patterns fail.
(B) every three-edge omitted set supports an actual ≤5+≤5 physical collision (220 triple-edge masks); any nonadjacent pair of omitted corners supports an actual ≤6+≤6 physical collision (16 corner-pair masks).
(C) exact spatial face-normal criterion for P(h), independently validated in the past against P48 physical labels.

Newly checked finite incidence: every one of the 66 unordered original edge pairs belongs to P(h) for at least one h. Distribution of number of h for a given pair: multiplicity1=24 pairs, multiplicity2=6, multiplicity3=24, multiplicity4=12; total incidences 24+2*6+3*24+4*12=156.

*17 sensors, omission 1 corner + 2 edges.* In the entire legal oriented-cubie group, the single omitted corner is fixed (corner twist sum=0; corner permutation identity), and the two omitted edges cannot transpose (corner and edge permutation parity must agree); only their joint flip can vary. So H({c,e1,e2})=H({e1,e2}). For every edge pair the new 66-pair coverage gives a positive size-16 layout omitting those same edges and two corners. Its stabilizer contains H({e1,e2}) and is certified to exclude B12 nonidentity states. Therefore all 8*C(12,2)=528 1C+2E omissions are identifying.

*17 sensors, omission 2 corners + 1 edge.* The lone edge is forced unchanged and the two omitted corners can only undergo opposite twists. Thus H({c1,c2,e})=H({c1,c2}). If the corners are adjacent, any one of 13 certified size-16 positives with those same corners implies positivity: 12 adjacent corner pairs * 12 omitted edges = 144 positive. If nonadjacent, a certified 2-corner physical short-support obstruction rules out all 16*12=192.

*17 sensors, omission 3 corners or 3 edges.* Three cube corners contain a nonadjacent pair since the cube graph has no triangles, giving 56 negative masks. Three edges are a previously certified physical short-support obstruction, giving 220 negative masks. The complete 17-positive count is 528+144=672; negatives 192+56+220=468; totals C(20,3)=1,140.

*Which 17 positives are minimal?* A positive size-17 sensor set is nonminimal iff it contains at least one positive size-16 set; equivalently its 3-tag omission is contained in some P(h) four-tag omission. For 2C+1E, for each h the graph on 12 edge tags defined by 13 allowed omitted-edge pairs uses exactly 11 edges, with h as its single isolated vertex. Thus 12*11=132 are extendable; 12 are minimal. For 1C+2E, independent exact geometry exhausts all 8*66=528 triples: 264 are contained in at least one known positive four-tag omission and 264 are not, precisely 33 minimal per omitted corner. Thus minimal17=12+264=276. The 264 is not merely a brute-force count: for any original cube corner c, its three incident original core edges h1,h2,h3 have |P(hi)|=13; all three pairwise intersections and their common triple intersection are the SAME three omitted-edge pairs. The identity is independently rechecked from physical cube face normals. Hence inclusion-exclusion gives |P(h1)∪P(h2)∪P(h3)| = 3×13−3×3+3 = 33; the other 66−33=33 possible edge pairs produce inclusion-wise minimal positive 1C+2E 17-sensor sets for this corner. Across eight corners, 8×33=264. This gives a compact local-to-global structural proof of the count, conditional on the inherited P(h) geometric classification.

*18 and more sensors.* An omitted pair of nonadjacent corners fails; all other 2-tag omissions are positive: 2 edges (subgroup of an already positive 1C+2E omission), 1 corner+1 edge (subgroup), or 2 adjacent corners (subgroup of positive 2C+1E omission). Therefore 18-sensor positives=C(20,2)-16=174. But every positive 2-tag omission can add at least one omitted tag and remain positive by the previous 17 classifications; none is minimal. Likewise every 19-/20-sensor set has a positive lower-cardinality subset. Every positive 16-sensor set is minimal since no 15-tag design identifies. QED, with the historical B6 physical inputs explicitly assumed.

## 3. Independent implementation and falsifier

Source: scripts/cuberev-observation/audit_r14_p813_complete_minimal_base_spectrum.py. It reconstructs the geometric 12 edges/8 corners and the old four-case admissibility rule from six 3D face-normal vectors WITHOUT importing prior cube scripts. It enumerates 20 choose k omission sets for k=0..4, all 66 edge-pair P(h)-coverages, and all single-tag minimality tests, and asserts the complete table. Separate local Python implementation in this session independently returned:
- P16=156, P17=672, P18=174, P19=20, P20=1;
- minimal16=156, minimal17=276, minimal18=0, minimal19=0, minimal20=0;
- minimal17 split 264 for 1C+2E and 12 for 2C+1E;
- 66-pair coverage histogram 1:24, 2:6, 3:24, 4:12.
The new source has not been shown to PASS remote CI. This geometry computation does not repeat physical 41-target B12 HTM MITM or the complete 4,845 original-facelet certificates.

## 4. New literature and scientific boundary

Three new original PDFs were read in central 00_INTAKE, renamed according to the Research OS author-year-title convention and moved IN PLACE to central 10_PAPERS. Original file IDs, new file names, byte sizes and parent folders were independently read back. RAW PDF SHA-256 readback remains PENDING.

- Cameron & Fon-Der-Flaass (1995), Bases for Permutation Groups and Matroids, European Journal of Combinatorics 16:537–544, full journal article: https://drive.google.com/file/d/1xiWPj55Bhs-1C-tr3EskIdkxhR15rhuF/view . Their Thms 2.1/2.4 show uniform lengths, reordering invariance and matroid bases equivalent for IRREDUNDANT group/set-family bases. Not the radius-restricted Rubik B6 model.
- Tarski (1975), An Interpolation Theorem for Irredundant Bases of Closure Structures, Discrete Mathematics 12:185–192, original journal scan: https://drive.google.com/file/d/1OFkyQKO5g7cE-k1_cDJCPcil9ak7p5Uc/view . Scan text extraction DEGRADATION HOLD: verified core topic, but not every proof detail.
- Lucchini, Morigi & Moscatiello (2021), Primitive Permutation IBIS Groups, arXiv 2102.12803v1 preprint: https://drive.google.com/file/d/1RjNaoK-Ss_sXu0csod08jsQQMja0VEh_/view . Primitive permutation-group O'Nan-Scott analysis; cannot assume our restricted radius-six sensor closure is a primitive IBIS group.

For any S of observed original tags define closure cl_B6(S) as all tags t such that whenever two B6 states have the same readouts for S they also agree at t. This is an extensive, monotone, idempotent FINITE CLOSURE OPERATOR. Its generating sets equal B6-identifying S. Since it has inclusion-wise minimal generating sets of two different sizes, it is not matroidal. The repository's 2026-11-03 direct 16-minimum basis-exchange counterexample predates this paper, and is not newly invented here.

Remove all THREE newly acquired originals from the prior missing-original queue. Six older unresolved originals remain (Harary & Melter 1976; Slater 1975; Hennie 1964; Vasilevskii 1973; Hopcroft 1971; Sokolovskii 1971); the 1970s original titles and translated editions require targeted ownership checks. No unsupported claims of global Drive absence.

## 5. Next scientific gates

Paper A: integrate this complete 432-layout theorem as a COROLLARY of physical B6 16-positive/4,845-classification, not a substitute for independent 41-class geodesic proof. Derive a small orbit-based analytic explanation for the uniform 33 minimal 1C+2E omissions per cube corner.
Paper B: the unrestricted 19-frame whole-group categorical adaptive policy remains OPEN, and M-star/b_r/h cost models remain DISTINCT. A pairwise shortest separating query is not a global policy.
Lean: formalize legal 1C+2E / 2C+1E stabilizer reductions and the new 66-pair geometric coverage, then instantiate the prior P8.9 P8.10 generic Lean results with exact physical P48 data. Claim kernel PASS only after an observed successful build.
Custody: human WhoSia author and committer, research/current, GitHub Actions read-only; Notion holds scientific interpretation, Drive holds PDF bytes, and new physical T2 raw receipts were not generated.
