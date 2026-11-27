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
