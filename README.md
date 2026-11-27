# CUBE-REV 0.30

## Exact Adaptive Identification under Delayed Invariants: End-to-End Formal Verification & Structural Generalization

CUBE-REV studies exact query complexity for finite hidden states under restricted adaptive observations, with the fixed-center Rubik's Cube as its first fully specified physical instance. The project combines combinatorial reductions, certificate-producing search, executable policies, and Lean verification.

## Verified baseline — 0.29

**Exactly 19 paired observation frames are necessary and sufficient** in the following model: deterministic noiseless observations, one fixed edge sticker probe and one fixed corner sticker probe, both queried simultaneously after a legal face-turn word selected from prior replies. Legal turns are free; only frames are charged. The output is the original 48-moving-sticker coloring, not a shortest solution word.

- Final theorem: [`physical_paired_optimum_nineteen`](formal/029/PairedCornerClock.lean).
- Lower bound: [`physical_eighteen_impossible`](formal/029/PhysicalEighteen.lean), even with solved corners.
- Exact verified commit: [`1a720ad9937db08274874b33ea049e473613eae7`](https://github.com/WhoSia/CUBE-REV/commit/1a720ad9937db08274874b33ea049e473613eae7).
- [Read-only CI #45803745408](https://github.com/WhoSia/CUBE-REV/actions/runs/45803745408): success, 159 Lake build jobs, no `sorryAx` occurrences in the retrieved log.
- Trust boundary: `propext`, `Classical.choice`, `Quot.sound`, plus native evaluation of `fifty_two_frozen_roots_semantically_accepted`, `representative_prefixes_covered_source`, `joint_routes_checked`, `pair_actions_match`, and `Eighteen.checked`. These five finite checks are not native-free kernel proofs.

This is a computer-assisted exact theorem with disclosed evaluation dependencies. It is not a theorem about move-optimal solving, randomized expected cost, noisy sensors or larger cubes. Submission readiness remains separate from proof acceptance.

## 0.30 research program

1. Preserve and independently reproduce the exact 0.29 result; reconcile active-set custody and the manuscript with the final theorem and its actual trust boundary.
2. Develop a finite-state framework for delayed invariant information: posterior fibers, restricted query complexity, side-information timing, and simultaneous auxiliary observations.
3. Extract structural explanations and simpler certificates or strategies from the Hall/Burnside/sign reductions; benchmark against the existing immutable certificates.
4. Generalize only when a precise theorem or counterexample supports the extension.

The 0.30 general theory is a research program, not yet a claimed general optimality theorem.

### Structural bounds and separating examples

The terminal-label model distinguishes four costs: maximum state-specific separating certificate, early-label adaptive depth, delayed-label adaptive depth, and fixed separating query-set size. In that order the costs are nondecreasing (unit-cost deterministic static queries).

The abstract [Lean module](formal/029/DelayedInvariantIdentification.lean) now contains candidate realized-path certificate and exclusive-witness lower-bound lemmas. Exact compiler acceptance for these new statements is pending; the previously accepted Bellman and timing-composition baseline is unchanged.

Run `node scripts/cuberev-observation/audit_r030_certificate_gaps.mjs` for the exhaustive 4-state/2-binary-query/2-label census and three extremal family checks. One-hot identification gives (1, n-1, n-1, n-1); block indexing gives (d, d, kd, kd); binary-tree routing gives (d, d, d, 2^d-1). These are abstract examples with unrestricted finite observation tables, not additional physical cube results or a novelty claim.

### Cross-domain identification: targets and controlled interventions

The structural program now compares exact hidden-state recovery, behavioral identification, partial identification and decision sufficiency. The transferred perspective is grounded in classical query learning, rival-model experimental design, partial identification and structural identifiability, not a claim of new general epistemology. A finite Boolean-polynomial audit separates interaction degree from query count: over GF(2), degree at most d in n variables has M=sum_{j<=d} binom(n,j) coefficients, exactly M binary evaluations suffice and are necessary for complete recovery; a single coefficient indexed by S requires exactly 2^|S| evaluations. One-factor-at-a-time tests at the all-zero baseline cannot identify general interactions. These are classical interpolation/rank facts and deliberately synthetic controls, not evidence of real admissions or arbitrary software identifiability.

The source audit is the `structure` section of `scripts/cuberev-observation/audit_r030_certificate_gaps.mjs` (n=1..3, every degree, all query subsets). The scientific next gate is whether a target/constraint distinction supplies an independent structural explanation of the existing physical cube result; do not indefinitely expand elementary toy formalizations.

### Signed matching rigidity: an explanatory structural gate

For a feasible bipartite compatibility matrix with reference perfect matching M, contract the matched edges and direct an arc i -> j whenever row i can take M(j), omitting loops. Every other perfect matching corresponds exactly to a vertex-disjoint collection of simple directed cycles; a cycle of length l changes relative permutation sign by (-1)^(l-1). Thus the sign class of M has exactly one matching iff there is no odd directed cycle and no pair of vertex-disjoint even directed cycles. Both sign classes have at most one matching iff there is no directed cycle, or exactly one simple directed cycle and its length is even. Equivalently, there is at most one non-singleton strongly connected component, which must be a directed even cycle. Given one matching, the latter test is linear in graph size with standard SCC algorithms (the audit uses transitive closure).

For cube residual edges, if each observed cubie has at least one color and exactly one residual slot is entirely unread, each matching has one orientation completion after imposing the global flip constraint. Therefore this test characterizes the sign-indexed terminal leaf condition in that submodel. Two or more unread edge slots instead admit orientation ambiguity even for fixed matching and sign. Zero unread slots need explicit flip filtering; do not apply the raw matching criterion as an equivalence in that case.

The registered audit checks all 4,165 loopless digraphs on 1..4 labeled vertices with diagonal matching and all 106,920 four-edge residual matrices (choose 4 of the 12 edges of K(2,2,2), three ordered singleton colors, one blank row): 45,126 feasible, 34,344 sign-injective, direct enumeration/cycle/SCC discrepancies zero. These are matrix counts, not frequencies of frozen policy leaves or uniform physical states. No new 19-frame proof is claimed. Classical matching/cycle theory; compare Robertson, Seymour & Thomas (1999), *Permanents, Pfaffian orientations, and even directed circuits*, Annals 150:929-975, https://annals.math.princeton.edu/1999/150-3/p05 (not a claim of identical theorem).

### Four-character counting and the actual frozen leaves

Let A0,A1 be the compatibility matrices for edge orientation 0 and 1, with rows in original position order and columns in increasing label rank. The number N(p,f) of completions with inversion parity p and flip residue f equals

    [per(A0+A1) + (-1)^f per(A0-A1)
     + (-1)^p det(A0+A1) + (-1)^(p+f) det(A0-A1)] / 4.

This follows by expanding products over assignments and applying character orthogonality on C2 x C2. The implemented counter uses the equivalent four-sector subset DP, not direct determinant evaluation. For an already used label set U, appending label j contributes inversion parity |{i in U : i>j}| mod 2 and the selected orientation bit. No frozen search engine is imported.

The audit reads the compressed frozen upper-policy artifact, checks both pinned SHA-256 values, traverses all 52 representative trees, and counts completions from each complete leaf observation record. Observed 141097 nodes, 73962 leaves, 144736 flip-zero completions; 70774 two-candidate leaves (opposite signs), 3188 singleton leaves. Last edge read counts 0/1/2: 17048/54690/2224. In 13535 leaves with no blank slot, ignoring flip parity gives multiple matchings in at least one permutation-sign sector. These are counterfactual counts on the same records, not a verification of the altered game's policy or uniform physical probabilities. The four-sector leaf check and mass conservation are complementary to the existing exhaustive response verifier, not its replacement. Tested also 23760 synthetic three-edge records by explicit enumeration. The prior SCC result directly applies to the 17048 one-blank leaves, not all leaves.

### Prefix polytopes and forest enumeration

For a graph H of distinct two-color edge types, let r(S) count edges touching color subset S. This coverage function is integer, monotone and submodular. By Hall, a color histogram x from k distinct edges is feasible precisely when x is a nonnegative integer vector, sum x=k and x(S)<=r(S) for all S. For k<|E| in the cube model at least one blank edge allows the flip residue to be corrected. For k=|E| the support below is the orientation-unrestricted combinatorial histogram support; fixed flip constraints may remove some histograms.

Equivalently the unrestricted prefix layers are lattice points of the Minkowski sum of coordinate triangles conv(0,e_u,e_v), sliced at sum x=k. Hall ensures the integer-point equivalence: assign each color token to a distinct incident edge; conversely all points in the Minkowski sum obey the cuts. In the top layer this is the graphical zonotope sum [e_u,e_v]. The classical forest formula (Postnikov, *Permutohedra, Associahedra, and Beyond*, Proposition 2.4, https://math.mit.edu/~apost/papers/permutohedron_full.pdf) gives 1083 top-layer points for K(2,2,2). Direct forest coefficients by edge count are 1,12,66,212,408,384, giving Ehrhart polynomial 1+12t+66t^2+212t^3+408t^4+384t^5. All 13 unrestricted layers: 1,6,21,56,126,246,426,666,939,1198,1362,1362,1083; 7492 total. The audit compares all 15625 bounded lattice candidates with endpoint-selection DP, all 4096 submodular inequalities, and forest enumeration. This extends the previous 11-color histogram view to the entire prefix polytope; it is not a new 19-frame optimality proof or a novelty claim.

### Parity-constrained discrete polymatroids: rank blindness and exchange failure

For each full color histogram x, orient each edge toward its selected endpoint. Two orientations of the same histogram differ by a balanced directed subgraph of the first orientation, decomposable into edge-disjoint directed cycles. Consequently a histogram admits both orientation parities iff any (equivalently every) orientation in its fiber contains an odd directed cycle. A cycle reversal changes orientation parity by its length modulo 2. This is a parity refinement of classical indegree-sequence/cycle-reversal theory (Gioan 2007, Proposition 4.10), not a claim of a new general cycle-reversal theorem.

In the fixed EighteenReadData label convention, the K(2,2,2) top layer has 222 even-only, 216 odd-only and 645 shared histograms, hence legal flip-zero support 867 and flip-one support 861. Both parity-restricted families violate the necessary base-exchange axiom of discrete polymatroids (Herzog & Hibi 2002, Theorem 2.3). In URFDLB order, even-sector x=(4,0,2,4,0,2), y=(4,0,2,3,2,1) and i=B force the sole possible exchange j=L; x-e_B+e_L=(4,0,2,4,1,1) has counts (0,1), so is not even-feasible. The odd-sector witness is in the audit. All 2,741,706 unrestricted ordered-pair/excess-coordinate tests pass; even and odd failures are 37,596 and 40,968 respectively. Counts are of exchange obligations, not distinct pairs.

For a nonempty graph with a fixed reference orientation and weight vector w, unrestricted support maximum H(w)=sum_uv max(w_u,w_v). Choose a maximizing orientation of parity b, and let delta=min_uv |w_u-w_v|. The parity-p maximum is H(w) if p=b, otherwise H(w)-delta: flipping a minimum-gap edge suffices, and any opposite-parity assignment must flip an odd, nonempty set of edges. This holds also with ties. For indicator weights of subsets S, delta=0 iff some edge does not cross the cut. Thus on any nonbipartite graph both parity supports have identical subset-rank maxima, while a bipartite graph with at least one edge has a cut where one parity maximum drops. For the cube all 64 ranks coincide although the weighted objective w=(5,0,3,4,2,1) separates the supports (even maximum 44, odd 45). Subset-rank descriptions alone therefore cannot recover either parity family.

The graph zonotope vertices are exactly acyclic-orientation histograms: strict compatible topological weights expose each acyclic orientation uniquely; a generic exposing weight for a vertex chooses an acyclic orientation. Enumeration gives 210 even and 216 odd vertices. Every odd-only histogram is an odd vertex; the even-only set contains 210 vertices and 12 nonvertices. All 12 latter points are midpoints of pairs of odd-support histograms. Thus the legal even support is precisely all integral points of its own convex hull, whereas the odd hull has exactly 12 missing lattice points. This conclusion is for the fixed edge-orientation convention, and the odd sector is a counterfactual control rather than a legal complete cube edge state. Audits independently enumerate all orientations, exchange obligations, integer midpoints, and 729 weight vectors in {-1,0,1}^6. The parity support-function proof is elementary; the cube-specific enumerations are computational. These are optional 0.30 structural investigations, not dependencies of the accepted 0.29 19-frame theorem.

## Reproduce

Use Lean 4.34.1 (pinned by the package) and Python 3:

```sh
cd formal/029
python3 restore_pinned_data.py
python3 validate_19_corner_schedule.py
lake build
```

See the [formal package](formal/029/README.md), [working manuscript](papers/0.29/20261122_AX_LEAN_FIRST_PHYSICAL_IDENTIFICATION_WORKING.md), and [repository policy](REPOSITORY_POLICY.md). The pinned source bytes are restored from committed compressed data and verified against their digests.

## Research custody

- Single active branch: `research/current`. No bot-authored commits.
- [Notion research ledger](https://app.notion.com/p/422ef561cf92811c8d5dea6e254222db?pvs=204) records scientific decisions and evidence status.
- [Drive archive](https://drive.google.com/drive/folders/1xpUKiXclYvGGPMpE9dVDhp2lOc_YJzRS) preserves exact retired bytes and manifests. No removal without verified custody and dependency review.
- [Historical README at the pre-transition commit](https://github.com/WhoSia/CUBE-REV/blob/ad79a52ecbff844553ec8b89696aead6bc3d0711/README.md) retains the earlier research lineage.
- [P7 active-set manifest](g7/p7/active-set-manifest.json) is a strict inventory; the audit is not relaxed to hide unregistered changes.
