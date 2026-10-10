# CUBE-REV 0.20 — P1-E: Exact Real-Rubik Face Grammar, Equatorial Opacity, Three Symmetry Orbits & Rank-Seven-Only Eight-Word Theorem

**Research identity:** CUBE-REV 0.20 — Structural Laws of Physical Identifiability: Action-Transported Observation Codes, Restricted Perfect Hash Families & Proof-Carrying Covering Complexity.

**Evidence grade:** `LOCAL_ORIGINAL_PHYSICAL_FINITE_CERTIFICATE_PASS` for the results marked verified below. External independent GitHub Actions complete-run PASS not asserted. This is a theorem about the fixed physical UR tracked-edge ontology, **not** a theorem about arbitrary Rubik states, blindfolded humans or arbitrary finite transducers. The prior P13 local unrestricted exact `M*(5)=8` proof remains separate.

Original source: `SOURCE/original_physical.json` SHA-256 `9f2119738f92f56485897c1894d2cb721a3d6b0498c5aa14832c71f18b20e2f1`. Original 18 sticker-derived HTM move maps, 24 edge-position/orientation states, 12 initially flip-zero positions, cumulative intrinsic direction bit after every move, 1,192 original 3/4/5-source requirements, unit-cost preset words. This note continues [P1-D archive-24 audit](P0_ARCHIVE24_REAL_RUBIK_CENSUS_LITERATURE_AUDIT.md) and the exact P13 theorem without changing their scope.

## 1. Transported-cut identity

For any legal face turn `a`, let `sigma_a` be its permutation of the 12 edge positions and `f_a(p)` the orientation XOR generated for a tracked edge at position `p` by that turn. For a fixed word `w=a1...aL`, the transported initial-source cut at time `t` is

`C_t = (sigma_{a(t-1)} ... sigma_{a1})^{-1}({p : f_{a_t}(p)=1})`.

The original zero initial orientation makes cumulative observations `Y_t=1_{C_1} xor ... xor 1_{C_t}`. The map `(Y1,...,YL) <-> (1_C1,...,1_CL)` is invertible through successive XOR differences. **Hence the observed partition of the 12 initial edge positions is exactly the membership partition of the transported cuts.** This identity holds at every length for orientation-XOR state systems, independently of the five-turn enumerations.

In the original Rubik convention only the four quarter-turns `F,F',B,B'` make nonempty cuts, each of initial cardinality four. `F2,B2` make zero cuts.

## 2. The exact L=5 rank-seven face-grammar theorem (real physical finite case classification)

Use `I_F={F,F'}`, `I_B={B,B'}`, `H={U2,R2,D2,L2}`, `Q={U,U',R,R',D,D',L,L'}`. All 18^5 original physical action words were independently enumerated (not a guessed free hash family). A word yields exactly **seven distinct orientation-bit histories** across all 12 initial slots **iff** it is in exactly one of these two grammar classes:

**Phase q=3, 128 words:** `I_F H I_B K I_F` or `I_B H I_F K I_B`. Here `H,K` are distinct transverse half-turns, and for *adjacent* transverse faces the sign of the central B/F turn is constrained: with outer F, ordered `H -> K` clockwise along `U,R,D,L` gives B, counterclockwise B'; with outer B, clockwise gives F', counterclockwise F. If H and K are opposite, both signs of the central informative turn are permitted. The signs of both outer informative turns are arbitrary. Exact count: `2 outer faces × 4 outer sign pairs × 4 choices H × (1 opposite × 2 central signs + 2 adjacent × 1 sign) = 128`. Every word has nonempty cuts *only at times* 1,3,5.

**Phase q=4, 512 words:** `I_F I_B Q I_F I_B` with the front/back order separately free to swap in *each* informative pair. All four informative face signs are arbitrary, `Q` is any of eight transverse quarter turns. Exact count: `2 initial face orders × 2^2 initial signs × 8 transverse quarter turns × 2 final face orders × 2^2 final signs = 512`. Every word has nonempty cuts *only at times* 1,2,4,5.

All other words (1,888,928 words, including those with q=0,1,2,5 and off-grammar q=3/4) have at most six histories. Their exclusion is a finite exact check against the original sticker-derived 18x24 maps. This classification is not yet a short purely symbolic human proof independent of a finite physical action-case checker.

## 3. Universal-on-its-domain geometric opacity lemma, and the 16 + 16 disjointness proof

Let `E={UR,UL,RD,DL}`, the four equatorial original source slots with no F/B incident face. Every `F,F',B,B'` fixes E and has zero flip increment on it; every `U2,R2,D2,L2` preserves E setwise with zero flip increment. **Equatorial opacity lemma:** *for a word of arbitrary length built only from these eight moves, all four initial sources of E have the same constant-zero orientation history*. This follows by induction; it is a hand proof grounded in real physical edge support/transport, not a five-step enumeration.

For each of the 128 rank-seven q3 words the three nonempty 4-element transported cuts A,B,C obey

`(|A cap B|, |A cap C|, |B cap C|)=(1,2,1)`, triple intersection empty, `|A union B union C|=8`; its never-flipped four-block is precisely E. The six other nonempty membership atoms have sizes 2,2,1,1,1,1. Thus every q3 rank-seven partition has the block-size multiset **(4,2,2,1,1,1,1)**.

For each of the 512 q4 rank-seven words the four nonempty cuts A,B,C,D have `A cap B = C cap D = empty`, and either `(|A cap C|,|B cap D|)=(3,3)` with crossed pairwise intersections zero or `(|A cap D|,|B cap C|)=(3,3)` with straight pairwise intersections zero. Their union has cardinality ten; **exactly two original equatorial sources never flip**. The membership partition consequently has block-size multiset **(3,3,2,1,1,1,1)**.

Since a partition determines its multiset of block cardinalities, these two highest-rank phase families can *never* be equal.

Independent actual-position label symmetry under the 16 transverse dihedral/reflection and F/B swap permutations `D4 × C2` shows: q3 has a single free orbit of 16 different partition keys, q4 has two orbits of 8 different partition keys each. Hence **16 + 16 = 32 distinct maximum-rank physical observation partitions, no intersection**, with exactly three symmetry orbits. The orbit calculation concerns these original source partitions; generic optimal-cover orbit-variable quotienting without an incidence proof is NOT authorised.

## 4. A new, small proof of the rank-seven-only eight-word minimum

For each rank-seven partition `P`, define `cover(P)={A in original 1192 admitted source subsets : P|_A injective}`. The 16 q3 partitions each cover **465 =148 triples+217 quartets+100 quintuples**, the 16 q4 partitions each cover **553=154+231+168**.

Union of *all* 16 q3 partitions covers 604 of 1192 original requirements. Union of *all* 16 q4 partitions covers 1110. Both unions together cover all 1192. Their phase-exclusive complements provide exactly **82 original requirements that only q3 rank-seven partitions cover** and **588 requirements that only q4 rank-seven partitions cover**.

For 82 q3-exclusive requirements **every one of the 16 q3 columns covers exactly 41**. Thus a rank-seven-only dictionary must select at least `ceil(82/41)=2` q3 words.

For 588 q4-exclusive requirements, their requirement-to-16-column incidence has 87 distinct nonzero masks and 36 distinct inclusion-minimal masks (all 4-bit). **A 12-row exact obstruction** is enough to force at least 6 q4 rank-seven words. In order of *ascending numeric canonical partition key* (not input word or face order), the source admission masks and incidence bitmasks are:

| Original source mask | Supports among the 16 q4 rank-seven partition columns |
| ---: | --- |
| 848 | `0x0303` |
| 773 | `0x0cc0` |
| 369 | `0x1105` |
| 625 | `0x1206` |
| 357 | `0x2448` |
| 613 | `0x2888` |
| 327 | `0x4450` |
| 583 | `0x4890` |
| 102 | `0x6018` |
| 339 | `0x8121` |
| 595 | `0x8222` |
| 51 | `0x9024` |

The independent verifier checks each actual mask against the original source inventory and checks **all C(16,5)=4,368 possible five-column sets**, finding at least one of these 12 masks unhit in every case. Six q4 columns suffice; a witness on the full 36 minimal source-support masks has indices `[0,2,3,6,9,11]` under the same canonical partition ordering.

The original P13 positive physical eight-word dictionary consists of **exactly two** q3 words `F L2 B' D2 F`, `F U2 B R2 F`, and **six** q4 words. Direct physical replay confirms it covers all 1,192 requirements. We therefore have the independent physically exact restricted theorem:

`M*_rank7-only(5) = 2 + 6 = 8`.

**Scope limit:** this proof by 82+588 phase-exclusive witnesses does **not** exclude a mixed dictionary using lower-rank words and <=7 total words. That unrestricted lower bound is furnished by the original complete P13 t=0..7 finite proof; this new court offers a concise physical explanation of why the *all-maximal-rank* subproblem needs eight.

## 5. Adversarial four-cycle perturbation: 16+16 is not determined by flip supports alone

Preserve the original 12 initial edge positions, all 18 labelled actions, original F/B move maps and 4-source flip cut sets, all four other transverse face maps, and the relation `R' = R^{-1}, R2=R^2`. Change only the **nonphysical** R generator on its same four affected source positions `{0,4,8,11}`: replace its original cycle `(0 11 4 8)` by `(0 4 8 11)`. This preserves reversible 4-cycles, action count and informative action supports; however the nonphysical R2 now moves equatorial edges into F/B incidence positions and breaks the real-cube equatorial opacity lemma.

Exhaustive 18^5 words on this perturbed **NONCUBE** 18x24 model yield **28** q3 distinct rank-seven partitions (128 words), **16** q4 distinct rank-seven partitions (448 words), total unique partitions 15,158, compared with the original Rubik **16** q3 and **16** q4 (128+512 words; 14,938 all partitions). A concrete perturbed q3 word `F R B D2 F` has source equatorial position RD acquiring nonzero flip increments, impossible under the real-cube q3 maximal-rank word grammar. This refutes universality based only on flip-support counts, elementary bijectivity and named 4-cycle algebra.

**Resulting mathematical boundary:** the strong original 16+16 partition theorem is about **physically coupled face-turn permutation geometry**, not bare cardinal information-theoretic bounds.

## 6. Reproduction, next research axis, evidence levels

- Exact C++ 18^5 real physical word enumerator: `scripts/cuberev-020/census-L5-transport-cuts.cpp`.
- New C++ rank-seven word-and-transported-cut record generator: `scripts/cuberev-020/emit-L5-rank7-geometry.cpp`.
- New independent Python action-grammar, incidence geometry and three-orbit checker: `scripts/cuberev-020/verify-L5-rank7-grammar.py`.
- New independent Python 82+588 phase-exclusive original-source 12-row covering court: `scripts/cuberev-020/verify-L5-rank7-phase-cover.py`.
- Old original P13 exact theorem: [P13 proof](../0.19/P13_FINAL_EXACT_PHYSICAL_MSTAR5_EIGHT.md). No old P13 frozen source or case receipts overwritten.
- The next *mathematical* attack is to replace even the complete five-step face-grammar enumeration by a small symbolic proof from genuine cube turn cycles, and then connect the 12-row obstruction to a more general conditional finite covering theorem on transported cut systems. The previous q3 vs q4 distinction derives from actual Rubik edge transport rather than abstract binary-output capacity alone.
