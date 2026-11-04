# WORKING PAPER — Radius-Restricted Cubie Observation in the 3×3 Rubik Group

**Draft:** 0.28-D0.1, 2026-11-03. **NOT SUBMISSION-READY.** This file is a candidate exposition, not a formally peer-reviewed theorem or a claim of novel general group theory. The physical B6=16 and 156-layout classification depend on sealed source algorithms and certificates; cross-engine independence is open.

## Provisional title

**Radius-Restricted Cubie Bases of the Rubik Group: Exact Finite Observation, Stabilizer Geometry, and the Disconnected Exchange Graph of Minimum Sensors**

### Abstract (provisional)

Consider the legal fixed-center 3×3 Rubik group with the symmetric 18-face-turn half-turn metric and twenty labeled original cubies, each observed in its full position and orientation. For a radius-r ball about the solved cube, the minimum number b_r of observed original cubie tags needed to identify every state is an instance of finite, radius-restricted group-action separation. We formalize the criterion H_S ∩ B_(2r)={e}, where H_S is the pointwise oriented-cubie stabilizer of a selected tag set. Previous exact physical certificates and a separately executed two-sided radius-six full-state decision algorithm establish b_6=16 and a family of 156 certified 16-tag layouts, with the full-family completeness depending on the original negative witness coverage. Algebraic parity and orientation counting yield a closed form for stabilizer order and a two-parameter exact support spectrum. For the relevant two-corner/two-edge omissions, the stabilizer is S3×C2 and a shared pure-corner C3 explains the reduction from 88 stabilization target entries to 74 distinct cube states. We also investigate local reconfiguration among the 156 minimum designs. Under the existing geometric B6 classification, the single-original-tag exchange graph has 336 edges and 25 connected components, of sizes 96, twelve 4's, and twelve isolated vertices, giving an explicit failure of the matroid basis-exchange axiom. We explain which deductions are elementary, which are independently verified finite counts, and where a second physical-transition semantics and a further prior-art review are required.

**Keywords:** Rubik group; group action; finite-radius base; oriented cubie; word metric; stabilizer; determining set; exact computation; exchange graph.

## 1. Scope and evidence policy

Fix the legal, fixed-centre 3×3 Rubik group G and the 18-generator symmetric HTM alphabet T (six faces times quarter, inverse-quarter and half turn). Identify each of the 20 original corner and edge cubies as a persistent labeled physical object; the sensor S reveals each selected object’s current exact *position and orientation*. No stochastic noise, mistaken labels, temporal occlusion or human-behavior data enter the fixed b_r model. The state set is B_r={g∈G: length_T(g)≤r}, centered at identity. Write π_S for the original-cubie sensor projection, H_S for its pointwise stabilizer, and

    b_r := min{|S|: π_S restricted to B_r is injective}.

The literature already studies group bases, graph determining sets and resolving sets under different actions and outputs [1,2]. Our finite-radius identification threshold is NOT the unrestricted action base size. Because the sensing model is *position and orientation of tagged cubies*, it is not the same as metric dimension of the cube Cayley graph, where sensor readings would be distances to selected graph vertices.

### Proposition 1 (radius-doubling reduction)

For a finite group with a symmetric generating alphabet and a consistent left action on a set of fully identified objects,

    π_S is injective on B_r  iff  H_S ∩ B_(2r)={e}.

*Proof.* π_S(x)=π_S(y) iff the group difference x^{-1}y (with the appropriate action convention) fixes all selected original tags; the difference of radius-r words has length ≤2r. Conversely every element of B_(2r) can be split as x^{-1}y with x,y∈B_r by cutting an at-most-2r word at a midpoint and taking inverses as appropriate. Thus every nontrivial short stabilizer element is exactly an ambiguity. QED.

This proposition is an elementary word-metric/group-action identity, not itself a novel theorem.

## 2. Existing physical result: b6=16

The archived exact B5 negative witness replay proves b5≥16, and monotonicity B5⊆B6 implies b6≥16. For the B6 upper bound, prior original-cube geometric construction yields 156 candidate 16-tag sets, grouped in eight proper cube-rotation orbits. Every such layout misses precisely two adjacent corners (endpoints of a physical cube edge) and two edges. For each layout H_S has 12 legal configurations, 11 nonidentity. Archived physical construction and signed spatial/inverse covariance reduce the eight representative layouts’ 88 target entries to 41 distance classes. A separately executed exact six-ball meet-in-the-middle decision algorithm, operating on all oriented original cubies and derived from the archived 54-facelet transition oracle, found zero intersections between each of 41 target six-balls and the solved six-ball. This certifies each target has HTM length at least 13 and hence the 156 candidate layouts all identify B6. The separate original negative-witness coverage is needed to conclude these are all the positive 16-tag layouts. Refer to the original proof and source-binary identity ledger [C1,C2].

Do not describe the two MITM implementations as entirely independent *physical models*: they share original transition semantics. Do not infer a newly independently checkable globally shortest cube solution.

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

## 5A. Exact robustness against one lost original cubie tag (2026-11-04 audit)

**Conditional theorem.** Define a selected original-cubie sensor set S to be *one-erasure robust* at radius six when S\\{t} continues to identify every state in B6 for every t∈S. Using the archived physical classification of *all* positive size-16 B6 sensor sets and independently audited 156-layout incidence geometry, the smallest one-erasure robust design has **19 selected original cubie tags**, and there are **exactly twelve** minimum robust designs: observe all eight corner cubies and any eleven of twelve edge cubies.

The proof uses a concise two-stage argument. Every positive 16-tag design omits exactly two adjacent corners and two edges. An 18-tag set missing two corners fails on erasure of a third corner; one missing two edges fails on erasure of a third edge; and one missing a corner plus edge fails on erasure of the original corner opposite the missing corner, since the resulting nonadjacent omitted corner pair cannot be extended to a positive 16-tag omission. Thus none of the 190 size-18 sets is robust, and upward monotonicity of erasure robustness excludes all smaller sizes. A 19-tag set omitting one corner fails for the same opposite-corner reason. In contrast, each of twelve 19-tag sets omitting one edge is robust: every pair of original edges occurs together in an allowed four-tag omission (66/66 unordered pairs), and every corner-edge pair likewise occurs in an allowed four-tag omission (96/96). The two finite coverage counts are separately checked without assuming the desired robustness answer. See `docs/0.28/B6_SINGLE_ERASURE_ROBUSTNESS_19_TAG_THEOREM.md` and `audit_b6_one_erasure_robustness.py` for the exact argument and reproducibility.

This finite result is about **failure of an original oriented cubie sensor**; it is not Hernando–Mora–Slater–Wood's graph-distance landmark metric dimension and it is not stochastic sensing. No new independent 54-facelet HTM proof of the 156-layout B6 physical classification is claimed.

## 6. Comparison against prior work and novelty caveats

[1] Bailey & Cameron (2011) surveys group-action bases, determining sets and graph metric dimension. The *output function* and action matter, so our original-cubie observation cannot be identified with an arbitrary Cayley-graph vertex-distance landmark. [2] Laison, McNicholas & Seaders (arXiv:1407.6046v1) makes variation across faithful group actions explicit. [3] Boutin (Graphs and Combinatorics 25, 2009) already considers exchange for determining/resolving sets and establishes both positive and negative graph families; no first-ever exchange-failure novelty is asserted. [4] Cameron (1999), §4.14 notes the failure of vector-space-like basis exchange for permutation actions. [5,6,7] fault-tolerant metric dimension literature studies deleted distance landmarks and admits nontrivial and sometimes exponential cost separation; it does NOT transfer numerical sensor thresholds to cubie tags. [8,9] machine distinguishing sequence results concern sequences of inputs and outputs with different epistemic and implementation assumptions.

A domain novelty audit remains open: prior physical Rubik reconstruction papers and graph group-base literature beyond the documents already inspected must be checked before asserting publication novelty or selecting a final journal.

## 7. Reproducibility and empirical boundary

The finite algebra and support programs are in scripts/cuberev-observation. Run

    python -m unittest discover -s scripts/cuberev-observation -p 'test_*.py' -v
    python scripts/cuberev-observation/audit_b6_full_sensor_swap_graph.py

Current CI evidence is the read-only hosted 0.28 observation workflow on canonical research/current. The full B6 geodesic proof separately needs the original archive CUBE_REV_20261030_EXACT_B1_B5_SENSOR_CERTIFICATES.zip, SHA256 002887a198bac812ad360ba536309f2522899d5c28d12fb73bb92062ae889c94, and C++17 original-cubie-oriented search. See docs/0.28/B6_EXACT_16_TWO_CERTIFICATE_CLOSURE.md and docs/0.28/evidence/B6_MITM_41_20261103.md. No simulation or graph count alone establishes a new facelet-level certificate.

## 8. Paper gate before a submission

1. Read Boutin (2009) entire original paper; check definitions of minimal determining/resolving bases and graph-family exchange results before writing a strong novelty claim.
2. Refactor the full 156-layout swap count into an independently replayable small 20-tag certificate with all component memberships, group rotation orbits and nontrivial positive/negative physical witnesses.
3. Independently implement 54-facelet physical action/HTM neighborhood or certify the original-oracle outputs with an external checker; test the 41 positive classes, and two explicit negative swap cases.
4. Separate source-level proofs and computational certifications from general mathematical results. Obtain a genuinely shorter *HTM word-metric* positive proof or clearly label finite exhaustive MITM as the main verification.
5. Establish experiment-independent model definition, literature coverage, complete certificate custody, and methodological limitations. Add bibliographic entries only for versions actually read.

## References (verified works; unfinished bibliography)

[1] Bailey, R. F., and Cameron, P. J. (2011). Base size, metric dimension and other invariants of groups and graphs. *Bull. London Math. Soc.*, 43, 209–242. DOI 10.1112/blms/bdq096. Drive: https://drive.google.com/file/d/1PSS1zaeX_CD6VVuxrP1H6AfrYXscktuV/view.

[2] Laison, J. D., McNicholas, E. M., and Seaders, N. (2014 arXiv v1, manuscript contains later revision date). Base Size Sets and Determining Sets. arXiv:1407.6046. Drive: https://drive.google.com/file/d/1qSqBE5DQ4AS_UwnEzrzdxzyXtwNbQHjb/view.

[3] Boutin, D. L. (2009 issue; 2010 online). Determining Sets, Resolving Sets, and the Exchange Property. *Graphs and Combinatorics*, 25, 789–806. DOI 10.1007/s00373-010-0880-6. arXiv:0808.1427. Full text still awaiting inventory.

[4] Cameron, P. J. (1999). *Permutation Groups*. Cambridge University Press, §§4.13–4.14. Drive: https://drive.google.com/file/d/14WWOUzTUy7PVuFcrvr5cnX0O2Fsfxqif/view.

[5] Knor, M., Sedlar, J., and Škrekovski, R. (2024). Fault tolerance of metric basis can be expensive. arXiv:2410.03656v1. Drive: https://drive.google.com/file/d/1JxybKs-9dikTL29gi7My2w9DFckJdFxD/view.

[6] Geneson, J., and Tsai, S.-F. (2025). Fault tolerance for metric dimension and its variants. arXiv:2502.02731v1. Drive: https://drive.google.com/file/d/1wM3wAv6CrhN7KWk7ABqB1_byuaD_wwOo/view.

[7] Mora, M., Souto-Salorio, M. J., and Tarrío-Tobar, A. D. (2022). Resolving sets tolerant to failures in three-dimensional grids. *Mediterranean Journal of Mathematics*, 19, 188. DOI 10.1007/s00009-022-02096-1. Drive: https://drive.google.com/file/d/1am5MEkxH0pACWoTaDBCuTKwmfzEgNdPi/view.

[8] Lee, D., and Yannakakis, M. (1994). Testing finite-state machines: State identification and verification. *IEEE Trans. Computers*, 43(3), 306–320. Drive: https://drive.google.com/file/d/1yp5Mc5-4mTeNpu7DyuHKIH4gEuz-BIwk/view.

[9] Hierons, R. M., Jourdan, G.-V., Ural, H., and Yenigun, H. (2008). Using Adaptive Distinguishing Sequences in Checking Sequence Constructions. *ACM SAC*. DOI 10.1145/1363686.1363850. Drive: https://drive.google.com/file/d/1Qd8bFEAoicsDAiauAXDugyQJYseJwBHp/view.

[10] Seress, Á. (2003). *Permutation Group Algorithms*. Cambridge University Press. Drive: https://drive.google.com/file/d/1kUj3ajt6Fq_O8S9omgyUEHnbTAazItne/view.

[11] Godsil, C., and Royle, G. (2001). *Algebraic Graph Theory*. Springer. Drive: https://drive.google.com/file/d/1rQ5TqfBPo14aaL-Z6zZABRLiCvezD12u/view.
