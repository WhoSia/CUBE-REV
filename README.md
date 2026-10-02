# CUBE-REV — research/current

> Active research branch. Historical execution scaffolds are intentionally pruned from this branch.

CUBE-REV studies exact reversible state spaces, search/representation geometry, and human planning. The current active phase is **Generation VII G7-P7**.

## Active scientific spine

### reco.nz — naturalistic reconstruction spine
Current P7 treats reco.nz as the core naturalistic human-solve source.

Active authority:
- frozen 12,941-row index population;
- bounded body acquisition only;
- max 10 solve bodies per run;
- no de-facto bulk mirror by chaining unlimited runs;
- raw public redistribution remains HOLD;
- annotations are preserved as measurements, not treated as latent cognition.

Current P7 campaign:
- 40 prospectively frozen solve bodies;
- 4 batches × 10;
- campaign complete: **40/40 acquisition + 40/40 exact replay**;
- exact move-prefix states across P7 campaign: **2,149**;
- private batch artifacts are sealed in Drive custody;
- P4 predecessor body corpus: 20 solves;
- combined body-level naturalistic corpus available to current analysis: **60 solves**;
- this campaign is CLOSED to further source contact. Any additional reco.nz body acquisition requires new source authority or a new prospective constitution.

### exact cube / search geometry
The reusable exact authority is kept independently of its historical generation labels:

`crates/cuberev-core/`
`crates/search-geometry-core/`
`scripts/cube/`

The search core contains the exact 3×3 cubie representation, phase-1 geometry, projected PDBs, phase-2 support, and five-rival planning representations used by G7.

### active reconstruction core

`core/reco/`
- reco.nz bounded-acquisition policy
- reconstruction method ontology
- frozen sampling geometry

`scripts/reco/`
- reco.nz HTML parsing
- reconstruction move/annotation lexing

### current phase

`g7/p7/`
- P7 preseal
- reco.nz campaign constitution/manifest
- current Court criteria and source boundaries

`scripts/g7-p7/`
- current bounded campaign selection/acquisition/tests

`.github/workflows/`
- only workflows that may still execute in P7 or its immediate successor should remain here.

## Current inference boundary

P7 may compare:
- naturalistic reconstruction trajectories;
- exact cube states and five-rival search geometry;
- WCA official attempt/scramble context;
- future authorized prospective participant behavior.

It must not equate reconstruction annotations with internal cognitive states, reconstruction frequencies with WCA frequencies, or computational representations with human representations without behavioral evidence.

## Repository active-set policy

Files belong on `research/current` only if they are one of:

1. **ACTIVE_CORE** — reusable executable code/schema used by current or immediate-next work;
2. **ACTIVE_PHASE** — current P7 constitution, manifests, tests, and workflows;
3. **ACTIVE_DATA_AUTHORITY** — current source/linkage definitions that are still consumed.

Closed-phase workflows, one-off materializers, phase-specific closure tests, and superseded prose are removed from the active branch after their authority is preserved.

Historical bytes remain recoverable through:
- Git history;
- archive branch `archive/pre-p7-active-prune-20261002`;
- GitHub Actions artifacts;
- Google Drive scientific custody receipts.

Drive archive ledger:
**CUBE-REV — Repository Active-Set Archive Ledger**

Latest blocking active-set receipt:
- tracked files: **66**
- legacy candidates: **0**
- unclassified files: **0**
- workflow run: `36981110448` — SUCCESS
- audit artifact: `11215198981`
- artifact SHA-256: `17c21a64c066d7d4eef234c11a903227a6c7b065b5cfba5fa4dabe72129bc2bc`
- Drive audit custody: `1vnmAK40dAjcvOyAFU2yfvSYBmqhy-jSV`

The machine-readable allow/retire contract lives at `g7/p7/active-set-manifest.json`. The blocking audit fails if any retired or unclassified path re-enters `research/current`.

## Rust workspace

```text
crates/
├─ cuberev-core/
└─ search-geometry-core/
```

Validation:

```bash
cargo fmt --all --check
cargo check --workspace
cargo test --workspace
```

## Naming doctrine

Stage suffixes are operation-sensitive, not lineage defaults.

Use `Court` only when live alternatives, fixed adjudication criteria, binding verdicts, and downstream authority changes are all present. Otherwise prefer the actual operation: `Campaign`, `Census`, `Compiler`, `Materialization`, `Replication`, `Gate`, `Audit`, `Validation`, `Seal`, etc.

G7-P7 retains `Court` because it independently satisfies that qualification. Future phase names must classify the operation before choosing the suffix.
