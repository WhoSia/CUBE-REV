# CUBE-REV 0.16 — the 24-target critical obstruction and its light-profile graph

**Internal P12 mathematical research note.** The sole formal version is CUBE-REV 0.16. This result is about the **80 near-tight positive-dual candidate masks arising ONLY in the hypothetical 24-word universal-catalogue proof**; these 80 masks must NOT be imposed when asking whether 25 full words exist.

## Definitions and exact finite theorem

Use the immutable public [P10 50×116 incidence table](P10_50_BY_116.json). Its B incidence component has 28 targets with 20 target weights four and eight target weights two, with exactly 80 allowable candidate masks from the 24-word necessary reduction.

Let H be the 20 targets of weight four, and order the eight weight-two targets as

`L = [14,18,29,31,40,44,46,49]`.

The target indices refer to the exact original P9 reduced-base-ordering, not to face-token or sticker numbering. Let T={18,29,40,49}⊂L. In this ordering, T corresponds to eight-bit mask `150` (binary `10010110`). Its original 12-slot four-edge basis objects are respectively

`{3,6,7,10}, {0,3,7,11}, {0,3,10,11}, {6,7,10,11}`.

**Finite theorem:** No five candidate masks from the prescribed near-tight 80-mask catalogue cover all **24** targets H∪T. Yet removing ANY ONE of those 24 target conditions permits a five-mask cover. Thus H∪T is an **inclusion-minimal unsatisfiable core** for the bounded five-mask covering problem, not merely a smaller hard instance of the former 28-target/80-mask court.

## Profile-completeness lemma (EXACT MACHINE-ASSISTED)

Out of all C(80,5)=**24,040,016** five-mask selections, exactly **3,008** cover all twenty targets H. Their union's covered subset of the eight light targets has EXACTLY the following **17** possible bit patterns, with frequencies:

| Covered L mask | Occurrences | Bits covered |
|---:|---:|---:|
| 85 | 624 | 4 |
| 90 | 312 | 4 |
| 95 | 20 | 6 |
| 102 | 312 | 4 |
| 105 | 312 | 4 |
| 119 | 20 | 6 |
| 125 | 20 | 6 |
| 153 | 312 | 4 |
| 165 | 312 | 4 |
| 170 | 624 | 4 |
| 175, 187, 221, 235, 238, 245, 250 | 20 each | 6 each |

The seven size-four patterns are {85,90,102,105,153,165,170}; the ten size-six patterns are {95,119,125,175,187,221,235,238,245,250}. An independent strict C++20 executable enumerates all24,040,016 five-sets from the public P10-derived masks and verifies the full 17-bin histogram, not just a negative result. A separate Python exact subset-DP proves the 24-target five-cover UNSAT and constructs twenty-four witnesses for each one-target deletion. The complete source table/physical-granularity provenance is preserved in earlier P7–P10 sources. **The completeness of the 17 patterns remains a machine-assisted finite lemma, NOT a non-enumerative theorem.**

## New SHORT GRAPH-THEORETIC obstruction (hand proof once profile completeness is established)

For each of the ten size-six light patterns, take the two light coordinates it **does not** cover. This yields a simple graph G on vertices {0,...,7} with ten edges:

`(5,7),(3,7),(1,7),(4,6),(2,6),(1,5),(2,4),(0,4),(1,3),(0,2)`.

The chosen T has vertex indices {1,2,4,7}. It meets **every one of the ten edges**. Therefore each size-six coverage pattern omits at least one of the four T targets and cannot cover T. The seven size-four patterns are also unable to contain T because **none equals the four-set T** (bitmask150). Consequently **none of the 17 possible patterns covers T**, so a five-mask cover of H∪T is impossible.

Moreover, G contains the four pairwise vertex-disjoint edges

`(5,7),(4,6),(1,3),(0,2)`.

Every vertex cover of G must choose at least one endpoint from each edge, so ANY light-target set that blocks all ten size-six patterns has cardinality≥4. Our choice T uses exactly four vertices and also avoids all seven four-patterns; it is therefore a **minimum-cardinality light-target blocker** of the 17 permitted coverage patterns. This argument uses only vertex-cover/edge-matching combinatorics, with NO 7,004-quadruple search in its logical body.

**Proof boundary:** The graph argument is a human-length proof *conditional on the verified completeness of the 17-profile list*. Deriving that exact list directly from the 18-HTM cubie action grammar without finite enumeration is STILL OPEN. Calling the whole theorem completely noncomputational would be a logical overstatement.

## Stronger triangle-pair uniqueness theorem (follow-up audit)

The ten-edge missing-pair graph splits **EXACTLY** into two vertex-disjoint triangles with vertices `{1,3,7}` and `{2,4,6}` (three edges each), plus the four exterior edges `{0,2},{0,4},{1,5},{5,7}`.

**Hand proof that the size-four vertex cover is UNIQUE.** Every vertex cover must choose at least two vertices from each triangle, so a four-vertex cover has exactly two in each and no exterior vertex `0` or `5`. The exterior edges incident to `0` then force `2,4`; those incident to `5` force `1,7`. Thus every four-vertex cover equals **`{1,2,4,7}`**, and direct substitution verifies that it covers all ten edges. This replaces the earlier matching-only minimality argument by a strictly stronger uniqueness result, with no finite enumeration in the graph proof.

**Further affine structure of the seven size-four light profiles.** Label the eight light indices by three-bit vectors `i∈F₂³`. For each `a∈{001,011,101,111}` and parity `b∈{0,1}`, let the affine hyperplane be `H_(a,b)={i:a·i=b mod2}`. These four normals yield eight affine four-subsets; the EXACT observed seven size-four light profiles are ALL except **`H_(111,1)`**, whose eight-bit mask is `150`. The complementary `H_(111,0)` has mask `105`. This identifies the four-target blocker also as the SINGLE missing member of this eight-hyperplane family. Independent stdlib integer verification is in [test-p12-triangle-uniqueness.py](../../scripts/cuberev-016/test-p12-triangle-uniqueness.py); Lean source adds finite unique-cover Boolean reflection but has NOT been compiler-certified.

**Precise authority boundary:** The two-triangle argument and affine classification are analytical *conditional on the ten-edge/17-mask input*. The claim that ONLY these seventeen profiles arise from the 80 legal near-tight masks still depends on exhaustive 24,040,016-combination checking. No claim that the entire physical Rubik-edge classification is now non-enumerative; exact original dictionary minimum remains `25≤M*≤34`.

## Relationship to the original M* open problem

The full universal four-action dictionary must separate **1,192** source bases. Its verified optimum interval remains

`25 ≤ M* ≤ 34.`

The 80 near-tight candidates are a VALID restriction only for a hypothetical **24-word** catalogue (dual weight476 versus total capacity480). They are **NOT** a valid restriction for 25 words (capacity500, slack24). The new 24-target core refines how the old ≥25 bound is proved; **it does not imply M*≥26 or M*=25**.

## Independent missing-75 audit: what does NOT work

The earlier 25-word construction for only the **sixty positive-weight dual targets** fails on 75 of the full1,192 bases (seven 4-source, sixty-eight 5-source). Each of those75 individually has at least one legal four-action physical word of MAXIMAL dual-positive coverage weight20 that also distinguishes it. Thus **no single missing target forces a lower-weight word**. A valid 25-word impossibility proof must exploit joint incompatibility or a new 25-specific dual/cutting system.

Across all **1,913** distinct physically derived four-action output partitions, the 162 partitions of full dual-positive coverage weight20 are sufficient to distinguish the 75 bases **individually**, and their incidence graph on the 75 target bases has two components of sizes 7 and68. This segmentation does not prove that these high-weight words alone form a 25-word universal catalogue, and low-weight candidates can connect different components.

## Lean proof levels

Source [P12LightGraph.lean](../../formal/016/P12LightGraph.lean) formalizes the finite 17-profile exclusion of core mask150, the ten-edge graph vertex cover, the four-disjoint-edge matching, and nonblocking by three-or-fewer chosen light indices. It is imported in `CubeRev016.lean`. **A real Lean compiler/kernel PASS has NOT been witnessed.** Its proof of the Boolean graph facts, even if it compiles, depends on an embedded list of 17 masks; it does not prove the physical 80×28 incidence, the C(80,5) completeness, or the full cube semantics.

An eventual **fully trusted chain** is: physical 24-state move grammar → 1,913 partitions → sound near-tight restriction for 24 words → 80×28 incidence → Lean-checked 17-profile completeness → Lean-checked graph lemma → original M*≥25. Avoid inserting arbitrary action-table axioms or silently granting generated assertions.

## Next research and paper use

This 24-target core is now small enough for targeted SAT/LRAT/Lean-reflection certificates or for a direct combinatorial explanation of the 17 profiles. Separately search for genuinely **25-word-valid** cuts using the seven F/B-only missing four-source bases plus the sixty-eight missing five-source bases; the 24-word near-tight restriction must not be recycled.

For a manuscript, place this graph-cover obstruction as a *certified constrained experimental-design result*. Its most natural field is **theoretical computer science / discrete mathematics and automata theory**, with an optional longer-term cognitive interpretation but NO current human-sensing experiment. The paper's central theorem should be the exact action-system mathematics, not a general behavioral claim.
