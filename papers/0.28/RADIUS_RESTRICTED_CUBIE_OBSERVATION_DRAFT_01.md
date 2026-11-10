# WORKING PAPER — Radius-Restricted Cubie Observation in the 3×3 Rubik Group

**Draft:** 0.28-D0.5 — Full P48 B6 Physical Classification, Independent No-15 Lower Bound and Irredundant 872-Support Kernel, 2026-11-04. **NOT SUBMISSION-READY.** This is a finite case-study manuscript, not a claim of new general group theory. All 41 B6-positive stabilizer distance classes have now passed both local and remote exact MITM from a fresh 48-moving-sticker physical generator. The complete 4,845-layout B6 classification and sixteen-sensor lower bound are now reconstructed by a separate P48 physical short-support certificate; novelty review remains open.

## Provisional title

**Radius-Restricted Cubie Bases of the Rubik Group: Exact Finite Observation, Stabilizer Geometry, and the Disconnected Exchange Graph of Minimum Sensors**

### Abstract (provisional)

For the legal fixed-center 3×3 Rubik cube, consider the set B_r of states within r symmetric 18-HTM moves of solved, and sensors that each reveal the complete position and orientation of one persistently labelled original corner or edge. We examine the smallest number b_r of original-cubie sensors that distinguish every pair of states in B_r. The elementary stabilizer relation H_S∩B_(2r)={1} reduces radius-restricted identification to finite physical word-metric decisions. **An independently constructed 48-moving-sticker model, combined with explicitly replayed short-support collision words and full-state exact meet-in-the-middle searches, establishes b_6=16 and classifies all 4,845 sixteen-sensor designs, of which exactly 156 are valid.** A 872-member inclusion-wise irredundant physical difference-support certificate proves all 4,689 failures; 220 three-edge supports and 16 nonadjacent-corner supports alone give a new direct no-15-sensor lower bound. Nine of the needed radius-five four-tag collision word pairs were discovered by a separate 621,649-state P48 exact two-sided search, rather than imported from archived proofs. Independently generated 41 B6 stabilizer goal classes were certified to have HTM distance at least thirteen in a second source-independent six-ball search. The 156 minimum designs form a single-sensor swap graph with 336 edges and 25 components (one of size 96, twelve four-cycles and twelve isolates). Against one permanent sensor erasure, the exact radius-six minimum rises to nineteen, with twelve optimal designs; each has exactly 26 positive sixteen-sensor backup cores and a nonuniform failure-specific redundancy profile. We distinguish standard group-action lemmas and prior graph-base theory from new, case-specific physical finite classification results. The broader CUBE-REV program on active information gathering, representation, memory and action cost remains open, not subsumed by this finite static-observation manuscript.

## 1. Scope and evidence policy

Fix the legal, fixed-centre 3×3 Rubik group G and the 18-generator symmetric HTM alphabet T (six faces times quarter, inverse-quarter and half turn). Identify each of the 20 original corner and edge cubies as a persistent labeled physical object; the sensor S reveals each selected object’s current exact *position and orientation*. No stochastic noise, mistaken labels, temporal occlusion or human-behavior data enter the fixed b_r model. The state set is B_r={g∈G: length_T(g)≤r}, centered at identity. Write π_S for the original-cubie sensor projection, H_S for its pointwise stabilizer, and

    b_r := min{|S|: π_S restricted to B_r is injective}.

The literature already studies group bases, graph determining sets and resolving sets under different actions and outputs [1,2]. Our finite-radius identification threshold is NOT the unrestricted action base size. Because the sensing model is *position and orientation of tagged cubies*, it is not the same as metric dimension of the cube Cayley graph, where sensor readings would be distances to selected graph vertices.

### Proposition 1 (radius-doubling reduction)

For a finite group with a symmetric generating alphabet and a consistent left action on a set of fully identified objects,

    π_S is injective on B_r  iff  H_S ∩ B_(2r)={e}.

*Proof.* π_S(x)=π_S(y) iff the group difference x^{-1}y (with the appropriate action convention) fixes all selected original tags; the difference of radius-r words has length ≤2r. Conversely every element of B_(2r) can be split as x^{-1}y with x,y∈B_r by cutting an at-most-2r word at a midpoint and taking inverses as appropriate. Thus every nontrivial short stabilizer element is exactly an ambiguity. QED.

This proposition is an elementary word-metric/group-action identity, not itself a novel theorem.

## 2. New 0.28-D0.5 complete P48 physical classification and lower-bound proof

**2026-11-04 proof upgrade.** The earlier historical B5 no-15 certificate and the original 54-facelet B6 156-design census remain in the provenance record, but are **not necessary premises for the new proof**. All B6 size-16 positive and negative cases now have an executable P48 physical certificate. The 19 historical B6 six-turn *word strings* are inherited candidate witnesses; all their physical actions and resulting supports have been independently recomputed in a new 48-moving-sticker source. The nine crucial B5 four-tag witnesses were discovered afresh in an independent P48 radius-five two-sided MITM. The B6 41-goal positive verification independently computes its own P48 physical goal states and factor transitions.

**Theorem 2 (exact B6 minimum and complete minimum-layout family).** For the legal fixed-centre 3×3 cube under symmetric 18-HTM actions, original cubies observed with full persistent position and orientation satisfy

    b_6=16,     number of minimum 16-tag bases = 156.

*Proof of the independently reconstructed lower bound.* Let M contain unobserved original cubies. Thirteen separately replayed two-sided B5 word pairs and their proper spatial rotation orbits physically realize every one of the C(12,3)=220 three-edge difference supports. Hence |M∩Edges|≤2. Two 12-HTM physical words, split into actual pairs of six-move B6 endpoint states, realize all 16 pairs of nonadjacent original corners. Hence every pair of unobserved corners must be adjacent. As the cube's vertex graph is triangle-free, |M∩Corners|≤2. Therefore |M|≤4, proving at least sixteen sensors are necessary. An independent 15-sensor audit checks all C(20,5)=15,504 possible five-omission patterns against precisely these 236 actual physical collision supports. This avoids the previous inherited B5 all-15-layout obstruction certificate.

*Physical exclusion and completeness of size sixteen.* A set M of four excluded tags must pass all actual physical short-support checks. Every failing M falls into the following **disjoint first-applicable classes**:

| Obstruction | Number of four-tag omissions |
| --- | ---: |
| Three or four missing edges (B5 220 physical triple-edge support family) | C(12,4)+8 C(12,3)=2,255 |
| Nonadjacent missing corner pair, with fewer than three missing edges (B6 16 physical two-corner supports) | C(8,4)+12 C(8,3)+16 C(12,2)=1,798 |
| Adjacent pair of missing corners plus a specific B5 four-tag physical support | 12×18=216 |
| Adjacent pair of missing corners plus a new B6 four-tag physical support | 12×35=420 |
| Survivors | 12×13=156 |
| **Total** | **4,845** |

The 216 B5 failures are not inherited from the original 54-facelet archive. An independent P48 B5 MITM reconstructs all 621,649 B5 states via 624,124 normal-form paths, generates 121 stabilizer targets from eleven broad geometric omitted-edge candidate orbits and finds nine actual <=5/<=5 HTM word-pair witnesses. A separate Python physical replay checks both words and the 24 proper spatial rotations of each pair; the resulting nine disjoint 24-element support orbits cover precisely 216 missing-four-tag designs, eighteen per adjacent corner core. Two other candidate orbits have no short collision in the exact five-plus-five search. The B6-specific 420 failures are obtained by independent P48 replay of 19 inherited <=6/<=6 historical word pairs under all signed spatial symmetries; there are thirty-five per adjacent corner core, disjoint from the 216.

The 156 survivors are *exactly* the 12 choices of an adjacent missing-corner pair, each with thirteen allowed missing-edge pairs given by the four-case geometric rule. All have been proven **positive** by the separately executed independent physical P48 41-class six-ball MITM: every nonidentity stabilizer representative has distance at least thirteen, so its stabilizer meets B12 only at the identity. Hence these 156 survive, all other 4,689 are physically refuted, and they exhaust all size-sixteen bases. QED.

**Proposition 3 (irredundant short-support exclusion kernel).** The physically replayed obstruction family contains

    220 edge triples + 16 nonadjacent corner pairs
       + 216 B5 adjacent four-tag + 420 B6 adjacent four-tag
       = 872 different physical supports.

This particular 872-member certificate is inclusion-wise irredundant: for each edge-triple support E, the four-omission set E∪{any corner} contains no other support from this family; for each nonadjacent-corner pair C, choose C∪{any two edges}; for each adjacent four-tag support D, choose M=D. Each of the 872 has a private rejected four-omission layout. This does **not** prove that 872 is smallest among all alternative physical collision-support certificate families, nor a new general set-cover theorem. It does show that a short-support hypergraph can be an auditable *basis for every failure of observation* in an otherwise enormous finite physical state system.

**Verified computational chain.** [P48 full 4,845-layout physical audit](../../scripts/cuberev-observation/verify_b6_complete_4845_p48.py), [fresh P48 B5-target generator](../../scripts/cuberev-observation/emit_b5_adjacent_p48_discovery_goals.py), [exact P48 B5 MITM rediscovery](../../scripts/cuberev-observation/discover_b5_adjacent_p48_mitm.cpp), [word-by-word receipt verifier](../../scripts/cuberev-observation/verify_b5_adjacent_p48_discovery_receipt.py), [P48 B6 negative 19 word-pair replay](../../scripts/cuberev-observation/verify_b6_negative_19_pairs_p48.py), and [P48 41-goal positive MITM](../../scripts/cuberev-observation/verify_b6_41_mitm_p48.cpp). The first full pipeline completed with actual remote read-only [CI PASS 41767450421](https://github.com/WhoSia/CUBE-REV/actions/runs/41767450421), including fresh nine-pair discovery, all 4,845 exclusions and 41/41 goal checks. The added 15-sensor and irredundancy checks are a later improvement and require their own workflow result before remote PASS can be claimed for that specific commit. Archived 54-facelet proof and earlier erroneous/orphaned assumptions remain preserved, not overwritten.

**Ambition retained.** This finite theorem does not close the broader questions concerning the earliest radius where short supports emerge, exact action cost of hidden change, representation-dependent identifiability, active sensor policies, limited memory, human reconstruction, or complexity as the family of reversible systems varies. These are explicit next *theorem problems*, not excluded from CUBE-REV merely because this manuscript isolates the precise finite B6 case study.

## 3. Abstract legality and exact support counts

For c original omitted corners and e omitted edges, let δ(n)=1 if n=0 or1, and δ(n)=0 otherwise. All non-omitted original tags must be fixed in position and orientation. The usual legal-cube constraints imply

    A(c,e)=|H(c,e)|
          = (c!e!+δ(c)δ(e))/2 * 3^max(c−1,0) * 2^max(e−1,0).

*Proof sketch.* The permutation of corners and edges must have identical parity; for n≥2, n!/2 permutations have each sign and for n≤1 only the identity is available. The parity-matched count is (c!e!+δ(c)δ(e))/2. The corner-twist sum and edge-flip sum must vanish modulo 3 and 2, contributing 3^max(c−1,0) and 2^max(e−1,0). These standard cubie-coordinate conditions are sufficient as well as necessary for legal states. QED.

Let N(c,e) be the number of legal states whose exact original cubie support equals a specified set of c corners and e edges. Inclusion-exclusion gives

    N(c,e)=Σ_(i=0..c)Σ_(j=0..e)
             (−1)^(c−i+e−j)*binom(c,i)*binom(e,j)*A(i,j).

The exact support counts for c=e=2 are identity 1, corner-only 2, edge-only 1 and all-four-tag support 8. There is no state changing exactly one original corner or exactly one original edge. These formulas say nothing by themselves about original HTM word distances.

## 4. The physical B6 target stabilizer and overlap theorem

For any two specified omitted corner and two specified omitted edge tags, the legal pointwise stabilizer H has order 12. An explicit compensated corner twist t∈C3, simultaneous pair-swap s∈C2, and paired edge flip f∈C2 give

    H ≅ (C3 ⋊ C2) × C2 ≅ S3 × C2.

Its order histogram is 1:1, 2:7, 3:2, 6:2. Let H(C,E_i) be the stabilizer of the *same* omitted corner pair C and a distinct omitted edge pair E_i. Then for i≠j, H(C,E_i)∩H(C,E_j) is precisely the three-element subgroup of pure corner twists. The other nine states in H(C,E_i) all change both original edges E_i, and these edge supports cannot be shared between distinct 2-element E_i. Thus

    |⋃_(i=1..m) H(C,E_i)|=3+9m.

For the eight B6 representative edge pairs, the number of *different nonidentity* states is 2+9·8=74, not 88. This algebraically explains old physical deduplication; reduction 74→41 still relies on checked cube 48-spatial symmetries and inverse distance preservation. No shortest 18-HTM word is inferred from the subgroup's isomorphism class.

## 5. New case-study result: nonmatroidality and the swap graph

For fixed adjacent omitted-corner pair C (endpoints of original cube edge h), the historic B6 physical obstruction classification permits exactly 13 omitted-edge pairs from C(12,2)=66 choices. The allowed-omission graph on twelve original edge tags is

    W5 ⊔ C4 ⊔ K2 ⊔ K1,

with 8+4+1=13 graph edges. The line graph of its 13 allowed edges is the graph of B6-valid one-edge-sensor swaps *while fixing the missing corner pair*. It has 13 vertices, component sizes (8,4,1), and 22 undirected edges.

As explicit failure of matroid basis exchange, choose h=DL with missing original edge pairs E_A={FR,UR} and E_B={DR,UL}. Both define B6-positive 16-tag sensor sets in the physical certificates. The observed sensor DR lies in A but not B. The only replacement sensor from B\A is FR or UR, producing omitted pairs {DR,UR} and {DR,FR}; both are B6-negative in the earlier physical witness census. Thus the family of minimum B6 original-cubie identification sets does NOT satisfy the matroid basis-exchange axiom. Exchange failure of generic determining/resolving sets is prior art [3,4]; the contribution is a specified physical Rubik finite-radius countermodel.

Unlike the fixed-corner calculation, the full graph allows swapping corner sensors too. Construct the complete 156-vertex graph with an edge between two positive 16-tag layouts iff their *observed* 20-tag sets differ by exactly one removed and one added tag. A finite enumeration over the 12 eligible core edges and 13 allowed edge pairs per core, validated against the previous four-class B6 geometric rule, produces

    vertices: 156;
    undirected exchange edges: 336
       = 264 within fixed missing-corner pair
       + 72 changing the missing-corner pair;
    component sizes: 96, (4 repeated 12 times), (1 repeated 12 times);
    number of components: 25.

A more economical geometric proof is available. If h and k are *distinct*, a single-sensor exchange between (h,E) and (k,F) requires the two omitted-corner pairs to share one corner (h,k adjacent cube edges) and E=F. There are 8*binom(3,2)=24 unordered adjacent core-edge pairs. The proper cube rotations act transitively on these pairs, and the four-case B6 positive predicate is rotation covariant; for representative h=DL,k=DF, the common omitted-edge pairs are exactly {BR,UB}, {BR,UR}, and {UB,UR}, all located in the respective wheel W5 components. Hence 24*3=72 cross-corner exchange edges, none incident to a four-cycle or isolated pair. Since the adjacency graph of cube core edges is connected, the twelve eight-design wheel components fuse into the 96-design component. The other components remain twelve four-design cycles and twelve isolated nodes. From the line-graph edge count of W5 (18) and C4 (4), the complete graph has 12*(18+4)+24*3=336 edges.

An exact duplicate-free 156-layout builder, symmetric XOR-one-tag adjacency predicate, component traversal and independent Johnson J(12,2) negative control are committed. A separate Python finite geometric proof checks all 24 adjacent core pairs, and an independently implemented JavaScript face-vector geometry checker reproduces the entire 156-node signature. The paper depends on the historical physical identification of the 13 admitted omitted-edge pairs per core h; these new programs do not certify B6 HTM geodesic exclusions.

**Interpretation.** Always maintaining size-16 B6 injectivity and changing just one sensor is insufficient to move between arbitrary optimal designs, even if changing which corner cubies are omitted is allowed. This is a conditional counterexample to a restricted neighborhood-search policy; it is NOT a proof of failure for arbitrary reconfiguration algorithms, intermediate suboptimal designs, multi-sensor swaps or relaxed sensor cost.

## 5A. Exact one-original-cubie sensor erasure threshold at radius six (2026-11-04 restored)

**Conditional exact theorem: b6^(1)=19 and exactly 12 minimum robust layouts.** Here a sensor is an originally labelled oriented cubie, and a set S is one-erasure robust if S\\{t} remains injective on the entire B6 state set after any one selected tag t is lost. The twelve optimal robust designs each observe **all eight original corners and eleven of the twelve original edges**. The result depends on three separately sourced physical certificates, not on the claim that every larger valid set contains a valid 16-tag sublayout.

For the lower bound, the previous 2026-10-31 48-sticker physical audit gives explicit 12-HTM words changing only two original corners, with face-diagonal (12 supports) and body-diagonal (4 supports) rotational orbits. Split at move six: both actual physical midpoint states belong to B6, and the original-tag difference support is still exactly those two corners; this midpoint claim is replayed, not inferred from endpoint support alone. Every corner appears in a pure two-corner collision. An observer that loses any corner tag has at most one sensor detecting that collision, which the adversary can then erase. **All eight corners are mandatory**.

Independently, the original archived B5 proof provides **84 B4 +136 new B5 =220** actual physical difference supports on every triple of original edge cubies, all other original cubies agreeing. This is a historical 54-facelet nine-orbit representative replay certificate, and its exact provenance is retained separately; our new short code does not redo the full old replay. If two original edge tags are omitted, choose any third: an existing B5⊆B6 three-edge collision is distinguishable by at most that one selected third tag, which is deleted in the one-erasure test. Therefore **at least eleven original edge sensors are mandatory**, giving b6^(1)≥8+11=19.

For the upper bound, the existing B6 classification certifies 156 positive size-16 layouts, and geometric coverage shows every unordered edge-edge missing pair (66/66) and every corner-edge missing pair (96/96) embeds in an allowed four-tag omission. Consequently any choice of 19 tags observing all corners and all but one edge remains B6-valid after any further single erasure. The 24 proper cube rotations reduce the sufficient extension check to **six edge-pair orbits and four corner-edge orbits**, with explicit positive-layout witnesses (ten representatives total) and a separate full finite auditor. Hence b6^(1)≤19, and the necessary all-eight-corners condition excludes the eight alternative nineteen-tag designs. The exact count of minimum robust layouts is twelve. In fact these twelve designs together with the complete 20-tag set exhaust **all 13 one-erasure robust subsets** at B6. An independently replayed physical 13-HTM pure-two-original-edge witness, cut into actual 6+7 move B7 midpoint states and transported by 24 spatial rotations, forces all twelve edge sensors for one-erasure robustness at B7; the B6 two-corner witnesses already force all eight corners. Hence **only the full twenty-tag set is robust for every radius r≥7**, giving a sharp 13→1 change in the number of robust subsets between B6 and B7. This phase-transition statement restores the earlier 2026-10-31 support diagram and uses no B8 census.

**Scientific boundary and corrected reasoning.** A prior same-day claim of exact 19 based on the false converse that all valid 17-/18-tag sets contain a valid size-16 sublayout was retracted; that converse remains **false**. The final proof restores the independently archived *short-support physical witnesses* from the earlier chat and uses those to prove the lower bound. In particular, it does not need to classify all 17-tag B6-valid sets. The exact theorem is a new integration of historically known case-specific physical facts, not a new source-independent 18-HTM shortest-path proof or a general new fault-tolerance theorem; see `docs/0.28/B6_SINGLE_ERASURE_ROBUSTNESS_19_TAG_THEOREM.md`, `verify_b6_one_erasure_exact19.py` and the original phase diagram `docs/observation-generalization/CUBEREV028_SHORT_SUPPORT_PHASE_DIAGRAM_20261031.md`.

### 5A.1. Fresh, independent physical proof of the B5 triple-edge support completeness (2026-11-04)

The original archived 54-facelet B5 study reports 84 B4 and 136 new B5 physical three-edge support classes, totaling `C(12,3)=220`. Initially, the new 48-sticker verifier could replay only one known B3 representative and its 12-support spatial orbit. **That 12/220 partial stage is now superseded by a full independent 220/220 physical reproduction.**

A new C++17 physical cube implementation tracks all 48 distinguishable moving original stickers, applies each of the symmetric 18 outer-face HTM moves, and performs a complete identity-centered B5 BFS. The exact distinct-state counts at depths 0–5 are respectively `1,18,243,3240,43239,574908`, summing to `621649`. For each of the thirteen spatial-rotation orbits on original-edge triples, the algorithm projects the 48-sticker configurations to **the 42 stickers on the other seventeen original cubies**, and finds two distinct B5 states with identical projected observations. It extracts one real pair of two-sided HTM words of length at most five for every orbit. This is a source-independent search algorithm, not a restatement of the earlier 54-facelet archive.

The thirteen newly discovered word pairs are fixed in `data/0.28/B5_13_ORBIT_INDEPENDENT_WORD_PAIR_WITNESSES_20261104.json`. An *independently implemented Python 48-sticker physical engine* then replays each pair and all 24 proper spatial rotations of BOTH move sequences, checking exact original-cubie position+orientation factors. It obtains `220/220` different original three-edge support sets, with none missing. A cross-language receipt verifier additionally parses the **live C++ stdout**, checks all thirteen original edge triples and orbit sizes against its own physical geometry, and requires exact equality of the generated word pairs with the pinned manifest. CI actually compiles the C++ search, reruns its B5 state census and seed discovery, and replays the words with Python. Thus the B5 triple-edge support existence lemma used to prove `b6^(1)≥19` no longer depends solely on the historical ZIP. Read-only CI `41756861110` and later `41756953533` both succeeded.

A real discrepancy surfaced during the cross-engine audit: an early C++ generator used a different quarter-turn sign convention for some faces, causing the Python physical witness verifier to reject its purported supports. Rather than interpreting a `621649` state-count match as sufficient, the generator's HTM sign convention was aligned to the independent Python physical model (`U-,R-,F-,D+,L+,B+` relative to the chosen positive coordinate rotations); the entire B5 BFS and witness extraction were rerun. The rejected intermediate manifests remain traceable through Git commits and CI failures. This negative control is substantial: the same state count does **not** certify the identical physical meaning of named HTM words.

The new result is **a complete, self-contained finite computational certificate for the B5 pure-three-edge support family**, not an original generic theorem about fault-tolerant metric dimension. It does NOT independently reprove the 41 stabilizer HTM-distance exclusions establishing the B6-positive 156 sixteen-tag layouts: that physical upper-certificate gate remains separate. Source: `docs/0.28/B5_220_THREE_EDGE_INDEPENDENT_PHYSICAL_REPLAY_GATE.md`.

### 5A.2. Thirteen-orbit certificate minimality within the rotation-saturation format

The 220 unordered original-edge triples split under 24 proper cube rotations into exactly thirteen orbits of sizes `4,4,8,12,12,12,24,24,24,24,24,24,24`. A proof format based on a two-sided physical word pair plus all rigid rotations cannot cover two different support orbits from the same seed pair. Thus **at least one representative per orbit is necessary**, and thirteen actual pairs as above suffice. This is only a minimality statement about this **specific orbit-saturated finite-witness format**. It is not a lower bound for all possible mathematical proofs or all other computational certificate encodings.

## 5B. Independent P48 physical certification of all 41 B6-positive distance classes (2026-11-04)

**Theorem 5B (computational, conditional only on the specified cubie observation model and the geometry of candidate layouts).** Every one of the 156 geometrically proposed sixteen-original-cubie observation sets S is injective on the entire 18-HTM solved ball B6.

**Proof and exhaustive certificate.** The 48 individually labelled moving stickers are reconstructed from lattice positions and outward normals, with each of the 18 HTM moves induced by the corresponding face-layer rotation. From these independently generated physical transitions, we derive the full 20-factor oriented-original-cubie action table. For each of the eight proper-rotation orbits of proposed sixteen-tag layouts, we independently generate the 11 nonidentity elements of its twelve-element stabilizer, parameterized by matching corner/edge swap parity (2 choices), corner twist (3), and edge flip (2). This gives 88 entries, 74 distinct physical permutations, and 41 distance classes under 48 signed spatial conjugations and inversion; the class-size histogram is 17×1, 19×2, 1×3, and 4×4.

A normal-form enumeration of the complete six-ball generates 8,331,112 word paths and 8,240,087 distinct complete oriented cubie states. Each of the 41 independent target six-balls was exhaustively enumerated, with no exact full-state intersections (341,575,592 goal-path probes in five complete batches). Under the symmetric generating alphabet, B6(1)∩B6(g)=∅ if and only if the HTM distance d(1,g)>12. All forty-one representative nonidentity stabilizer elements consequently have distance at least thirteen. HTM generator conjugation and inversion transport that statement to every nonidentity stabilizer element of each of the 156 proposed layouts; the radius-doubling reduction gives injectivity.

**Independent evidence:** [source-independent P48 proof ledger](../../docs/0.28/P48_B6_41_INDEPENDENT_CLOSURE_AND_BACKUP_CORE_SPECTRUM_20261104.md), [actual GitHub Actions SUCCESS 41763106125](https://github.com/WhoSia/CUBE-REV/actions/runs/41763106125), original executable sources `b6_independent_48sticker_goals.py` and `verify_b6_41_mitm_p48.cpp`. The workflow executed six adversarial source tests, 324 ordered two-turn full-physical-versus-factor consistency checks, and five complete MITM batches. The generated P48 table and raw 41-target permutation bytes have SHA-256 `33ab96ee24228febc89740676078d7abb0967a468b3aba338e4e6ea75eb3a021` and `f73c09094a4ed327f4ab8f9295c3dd1cbdc139b312e3d52ea998591a3ff685b9`, respectively.

**Limits.** This is a source-independent second physical *positive* B6 certification, not a new 156-layout *negative/completeness* census or an exact claim that all 41 geodesic distances equal 13. The B5 no-fifteen-sensors negative proof remains a separate source-qualified obligation. Proof of priority over earlier cubie-identification literature is also not provided by a successful CI.

## 5C. A fault-specific backup-core multiplicity theorem

For each omitted original edge e, let S_e contain the other eleven edges and all eight corners. These twelve choices are exactly the previously established minimum one-erasure-robust B6 nineteen-tag layouts. For any one of the nineteen selected sensors v, define

    m_e(v) = #{T : T is a positive B6 16-tag base, T ⊆ S_e \ {v}}.

Under the physically certified 156-layout classification, each S_e contains **26 distinct** minimal sixteen-tag sub-bases, and the numbers of such backup bases after loss of a sensor are not uniform:

| Lost sensor type | Number of candidate sensors with given m_e(v) |
| --- | --- |
| Edge | m=1: four, m=2: one, m=3: four, m=4: two |
| Corner | m=4: two, m=6: four, m=10: two |

These distributions hold for each of the twelve choices of e. The number of backup-core–single-failure incidences is 26+52=78, also proved by double counting: each 16-tag sub-base lies in the 19-tag design with exactly three additional sensors and survives precisely those three single deletions, so 78=3×26. Among all 66 unordered omitted-edge pairs, the number of compatible omitted-corner edges is 1 for 24 pairs, 2 for six, 3 for 24, and 4 for twelve. Consequently every pair of omitted edges admits at least one B6-positive 16-tag completion.

This is a conditional exact **finite cubie-geometry** theorem (source: `audit_b6_single_erasure_core_multiplicities.py`), not a general new fault-tolerant-base theorem. It refines the robustness result by quantifying how many surviving minimal bases certify each single erasure, and supplies a potential explanatory link to the previously certified fragmented exchange graph.

## 6. Comparison against prior work and novelty caveats

[1] Bailey & Cameron (2011) surveys group-action bases, determining sets and graph metric dimension. The *output function* and action matter, so our original-cubie observation cannot be identified with an arbitrary Cayley-graph vertex-distance landmark. [2] Laison, McNicholas & Seaders (arXiv:1407.6046v1) makes variation across faithful group actions explicit. [3] Boutin (Graphs and Combinatorics 25, 2009) already considers exchange for determining/resolving sets and establishes both positive and negative graph families; no first-ever exchange-failure novelty is asserted. [4] Cameron (1999), §4.14 notes the failure of vector-space-like basis exchange for permutation actions. [5,6,7] fault-tolerant metric dimension literature studies deleted distance landmarks and admits nontrivial and sometimes exponential cost separation; it does NOT transfer numerical sensor thresholds to cubie tags. [8,9] machine distinguishing sequence results concern sequences of inputs and outputs with different epistemic and implementation assumptions.

A domain novelty audit remains open: prior physical Rubik reconstruction papers and graph group-base literature beyond the documents already inspected must be checked before asserting publication novelty or selecting a final journal.

## 7. Reproducibility and empirical boundary

The finite algebra and support programs are in scripts/cuberev-observation. Run

    python -m unittest discover -s scripts/cuberev-observation -p 'test_*.py' -v
    python scripts/cuberev-observation/audit_b6_full_sensor_swap_graph.py

Current CI evidence is the read-only hosted 0.28 observation workflow on canonical research/current. The historical B6 geodesic checker uses archive CUBE_REV_20261030_EXACT_B1_B5_SENSOR_CERTIFICATES.zip (SHA256 002887a198bac812ad360ba536309f2522899d5c28d12fb73bb92062ae889c94), but the new **independent P48 B6-positive geodesic proof does not require that archive**: generate the new table/goals with `python scripts/cuberev-observation/b6_independent_48sticker_goals.py --emit OUT`, then compile and run `verify_b6_41_mitm_p48.cpp` in five bounded batches. The B6 negative/completeness certificate is now independently physically reconstructed through the new P48 4,845-layout checker; the older archive remains preserved as a separate historical source. See docs/0.28/B6_EXACT_16_TWO_CERTIFICATE_CLOSURE.md and docs/0.28/evidence/B6_MITM_41_20261103.md. No simulation or graph count alone establishes a new facelet-level certificate.

## 8. Paper gate before a submission

1. Read Boutin (2009) entire original paper; check definitions of minimal determining/resolving bases and graph-family exchange results before writing a strong novelty claim.
2. Refactor the full 156-layout swap count into an independently replayable small 20-tag certificate with all component memberships, group rotation orbits and nontrivial positive/negative physical witnesses.
3. **Independent P48 B6 positive and negative completeness DONE**: all 4,845 size-sixteen designs physically classified and all 41 positive distance classes checked on hosted read-only CI 41767450421. A new third-party raw-sticker checker, an independent proof-kernel review and certificate archival beyond the 30-day Actions retention remain desirable.
4. Separate source-level proofs and computational certifications from general mathematical results. Obtain a genuinely shorter *HTM word-metric* positive proof or clearly label finite exhaustive MITM as the main verification.
5. Establish experiment-independent model definition, literature coverage, complete certificate custody, and methodological limitations. Add bibliographic entries only for versions actually read.

### A distinct, stronger CUBE-REV research question: action-dependent observation

The full-cubie original-tag sensors defining `b_r` are **not** spatially fixed readout stations. If a persistent original-cubie sensor already supplies the piece's full labelled position and orientation, applying known deterministic legal turns cannot distinguish states that the initial fixed-tag output failed to distinguish: every later output is determined by the initial output and the known action word. In contrast, a fixed *spatial slot probe* reads whichever moving cubie enters the monitored position, permitting genuinely new information to arrive over time.

A separate [P48 active-observation implementation](../../scripts/cuberev-observation/active_p48_fixed_site_scan.py) establishes, under the **idealized full original-identity-and-orientation output** assumption, an exact **eleven joint observation-frame horizon** for reconstructing an *unrestricted* legal 3×3 cube with one fixed edge-site probe and one fixed corner-site probe. A constructive joint orbit of 96 edge/corner site pairs gives eleven predetermined full-state interrogation frames; the missing twelfth edge factor is forced by edge-flip parity. Conversely, any adaptive ten-frame policy leaves at least two initial edge positions unread; flipping those two edges produces a legal indistinguishable alternate initial configuration. [Seven executable adversarial tests](../../scripts/cuberev-observation/test_active_p48_fixed_site_scan.py) passed in [read-only P48 CI 41773806842](https://github.com/WhoSia/CUBE-REV/actions/runs/41773806842). This result is for unrestricted `G`, **not** an asserted optimal horizon for the radius-restricted `B_6`, an RGB camera, or a minimum HTM action-cost policy.

**Prior-art warning:** a 2017 MIT 6.111 [Rubik's Cube Solving Robot report](https://web.mit.edu/6.111/www/f2017/projects/jeswiezy_Project_Final_Report.pdf) already describes two physical RGB color sensors (one corner and one edge) and sequential turns to scan a cube; a 2022 ICSPS [monocular state recognition study](https://ieeexplore.ieee.org/document/10218571/) also addresses fewer visual sensors. Thus two-site active cube reading is *prior art*. The general deterministic observation no-gain lemma is elementary. The demanding open question is how sensor output fidelity, observation frames, HTM move cost, feedback/adaptation and prior radius interact, and whether genuinely new boundary theorems or testable cognitive predictions can be obtained. This axis should be researched seriously rather than claimed as part of the exact static `b_6` result without a proper model.

### 2026-11-10 — Minimal/irredundant base distinction and exchange-graph reading

Re-reading Bailey & Cameron (2011) and Boutin's owned 2008 arXiv manuscript confirms that a permutation-group base is defined by a *trivial pointwise stabilizer*, whereas its minimality and the exchange property require separate arguments. An inclusion-wise minimal base need not be a minimum-cardinality base. In general graphs determining sets and resolving sets do not satisfy a universal exchange axiom; Boutin supplies concrete graph families with and without it. Thus our finite b6 arrangement-exchange graph (156 minimum layouts, 336 edges, 25 components) does **not** become a matroid simply because it consists of bases, and the counts require independent physical membership replay.

New primary prior-art gap: Dalla Volta, Mastrogiacomo & Spiga (2024), *On the Cardinality of Irredundant and Minimal Bases of Finite Permutation Groups*, Journal of Algebraic Combinatorics 60:569–587, DOI 10.1007/s10801-024-01343-w, provides an openly accessible publisher article. Its direct distinction between cardinality spectra of irredundant and minimal bases must be compared with both our all-minimum b6 layouts and the inclusion-wise irredundant witness family; the current targeted Drive search did not locate its owned PDF. No general result in that paper is yet claimed to imply or contradict the Rubik-specific 156/336/25 enumeration.

Full owned-paper and expanded missing-original status: [R14-P8.11 audit](../../docs/0.28/20261110_R14_P811_EXISTING_PAPERS_MISSING_ORIGINAL_AUDIT.md).
## References (verified works; unfinished bibliography)

[1] Bailey, R. F., and Cameron, P. J. (2011). Base size, metric dimension and other invariants of groups and graphs. *Bull. London Math. Soc.*, 43, 209–242. DOI 10.1112/blms/bdq096. Drive: https://drive.google.com/file/d/1PSS1zaeX_CD6VVuxrP1H6AfrYXscktuV/view.

[2] Laison, J. D., McNicholas, E. M., and Seaders, N. (2014 arXiv v1, manuscript contains later revision date). Base Size Sets and Determining Sets. arXiv:1407.6046. Drive: https://drive.google.com/file/d/1qSqBE5DQ4AS_UwnEzrzdxzyXtwNbQHjb/view.

[3] Boutin, D. L. (2009 issue; 2010 online). Determining Sets, Resolving Sets, and the Exchange Property. *Graphs and Combinatorics*, 25, 789–806. DOI 10.1007/s00373-010-0880-6. arXiv:0808.1427. The original author's full-text manuscript and arXiv version have been located; the published journal final text has NOT been line-by-line compared. See https://people.hamilton.edu/documents/ExchangeProperty.pdf and https://arxiv.org/abs/0808.1427.

[4] Cameron, P. J. (1999). *Permutation Groups*. Cambridge University Press, §§4.13–4.14. Drive: https://drive.google.com/file/d/14WWOUzTUy7PVuFcrvr5cnX0O2Fsfxqif/view.

[5] Knor, M., Sedlar, J., and Škrekovski, R. (2024). Fault tolerance of metric basis can be expensive. arXiv:2410.03656v1. Drive: https://drive.google.com/file/d/1JxybKs-9dikTL29gi7My2w9DFckJdFxD/view.

[6] Geneson, J., and Tsai, S.-F. (2025). Fault tolerance for metric dimension and its variants. arXiv:2502.02731v1. Drive: https://drive.google.com/file/d/1wM3wAv6CrhN7KWk7ABqB1_byuaD_wwOo/view.

[7] Mora, M., Souto-Salorio, M. J., and Tarrío-Tobar, A. D. (2022). Resolving sets tolerant to failures in three-dimensional grids. *Mediterranean Journal of Mathematics*, 19, 188. DOI 10.1007/s00009-022-02096-1. Drive: https://drive.google.com/file/d/1am5MEkxH0pACWoTaDBCuTKwmfzEgNdPi/view.

[8] Lee, D., and Yannakakis, M. (1994). Testing finite-state machines: State identification and verification. *IEEE Trans. Computers*, 43(3), 306–320. Drive: https://drive.google.com/file/d/1yp5Mc5-4mTeNpu7DyuHKIH4gEuz-BIwk/view.

[9] Hierons, R. M., Jourdan, G.-V., Ural, H., and Yenigun, H. (2008). Using Adaptive Distinguishing Sequences in Checking Sequence Constructions. *ACM SAC*. DOI 10.1145/1363686.1363850. Drive: https://drive.google.com/file/d/1Qd8bFEAoicsDAiauAXDugyQJYseJwBHp/view.

[10] Seress, Á. (2003). *Permutation Group Algorithms*. Cambridge University Press. Drive: https://drive.google.com/file/d/1kUj3ajt6Fq_O8S9omgyUEHnbTAazItne/view.

[11] Godsil, C., and Royle, G. (2001). *Algebraic Graph Theory*. Springer. Drive: https://drive.google.com/file/d/1rQ5TqfBPo14aaL-Z6zZABRLiCvezD12u/view.
