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
