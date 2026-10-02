# CUBE-REV repository policy

CUBE-REV uses GitHub as the compact executable/reproducibility layer, not as the historical archive.

## Durable branches

- `main` — deployed/public surface. Keep stable unless a deliberate public release or deployment transition is authorized.
- `research/current` — the single active research branch. All current experiments, schemas, manifests, receipts, analysis code, and release-preparation metadata belong here.

Do not create one branch per stage, court, generation, experiment, receipt, or snapshot. Temporary branches are allowed only for genuinely risky refactors or destructive migrations and must be merged or deleted promptly.

## Historical continuity

- Notion stores the canonical scientific narrative, verdicts, and lineage.
- Google Drive stores large raw data, literature, immutable byte snapshots, bundles, and release candidates.
- Git commit SHAs/tags identify important executable freezes.
- Branches are not archival snapshots.

The pre-P14 full-history bundle is the recovery surface for retired branches. Once a branch is represented in that sealed bundle and no longer serves the current executable lineage, delete the remote branch.

## Continuous cleanup rule

At every stage transition:

1. remove superseded scripts, manifests, receipts, and experiment trees from the live research branch when they are not required to reproduce or interpret the current active lineage;
2. do not preserve obsolete stage trees merely because they are historically interesting;
3. prefer commit SHA/tag + Notion/Drive provenance over branch accumulation;
4. never put large raw datasets into Git history;
5. keep the remote branch set minimal: normally `main` + `research/current`, plus explicitly justified release branches that are still operationally needed (for example an active Paper 1 / Zenodo publication branch).

Practical rule:

> If deleting an old branch or artifact would not prevent reproduction, interpretation, deployment, or publication maintenance of the current active work, it should usually be retired.
