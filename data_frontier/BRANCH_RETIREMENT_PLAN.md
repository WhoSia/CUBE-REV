# Repository retirement plan — non-destructive preseal

G3-P14 does **not** delete branches or repositories.

The current repository contains many historical stage branches. Cleanup is deferred until the data spine has a stable public release candidate.

## Retirement order

1. Inventory every branch head and open PR.
2. Classify each branch as `ACTIVE`, `MERGED`, `SUPERSEDED_WITH_UNIQUE_BYTES`, or `REDUNDANT`.
3. For every branch with unique scientific/provenance bytes, create an immutable tag or archival bundle before deletion.
4. Merge only material that belongs on the durable main/data spine; do not merge historical execution noise solely to preserve it.
5. Close stale PRs with a pointer to the superseding tag/commit.
6. Delete remote branches only after the preservation receipt is complete.
7. Consider a clean successor repository only after the first secondary-data release has a frozen manifest and DOI-ready package.

## Durable branches proposed

- `main` — public canonical code/history.
- `research/data-spine` — active secondary-data registry, acquisition recipes, schemas and release compiler.
- bounded paper/release branches only while genuinely active.

## Never do

- delete the existing repository before unique commits are inventoried;
- treat branch deletion as data cleanup;
- store large raw datasets in Git history;
- use Git LFS as a substitute for an explicit data-repository/release policy.
