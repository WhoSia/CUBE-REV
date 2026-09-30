# CUBE-REV Generation VII G7-P2 — Large-Scale Human Solve Reconstruction Corpus, Move-by-Move Expert Policy Geometry, Kociemba↔Human Chunk Boundary Alignment, Slack-Lookahead Naturalistic Census & Prospective Experiment Reconstitution

## Scientific identity

G7-P2 uses already-public human solve reconstructions as a naturalistic policy corpus before launching new participant collection.

The primary objects are:
- the competition or published scramble;
- the move-by-move human solution trajectory;
- reconstruction-authored step annotations such as cross / pair / OLL / PLL;
- the exact 3×3 state trajectory induced by those moves;
- CUBE-REV phase coordinates, entry-cost fibers and slack values along that trajectory.

This is Cube mathematics + human strategy analysis. It is not a generic web-scraping project and it does not identify reconstruction annotations with latent cognition.

## Source lanes

Every source must be registered before ingestion.

### A — official structured source
Example: WCA Results Export v2.x.

Allowed use and attribution are governed by the source's explicit export terms.
This lane provides competition/result/scramble authority but usually not move-by-move reconstructions.

### B — public downloadable reconstruction snapshot
Example: a historical database dump explicitly linked for download by the source project.

Raw bytes may be mirrored for internal research only after:
- source URL is recorded;
- retrieval date is recorded;
- raw SHA-256 is recorded;
- data-license status is separately recorded from code-license status.

A repository's software license does not automatically license database contents.

### C — public reconstruction pages without bulk export rights
Examples: reconstruction websites or profile pages.

Do not bulk scrape merely because pages are publicly readable.
Use only:
- an explicit export/API;
- an explicit downloadable dump;
- files supplied manually through the CUBE-REV intake;
- or individually cited pages when scientifically necessary.

## Drive custody

Existing CUBE-REV Drive structure is authoritative.

Manual raw bytes:
`00_RAW_BYTE_MIRROR_INTAKE`

Validated corpus custody:
`20_SECONDARY_DATA_FRONTIER`
- `00_REGISTRY_AND_LICENSES/G7_P2_HUMAN_SOLVE_RECONSTRUCTIONS`
- `10_RAW_SNAPSHOTS/G7_P2_HUMAN_SOLVE_RECONSTRUCTIONS`
- `20_DERIVED_TABLES/G7_P2_HUMAN_SOLVE_RECONSTRUCTIONS`
- `30_RELEASE_CANDIDATES/G7_P2_HUMAN_SOLVE_RECONSTRUCTIONS`

Files never move from intake to raw snapshots until identity, provenance, format and rights status are recorded.

## Canonical solve record

Each source solve maps to one canonical record containing:

- source identity and source-native record ID;
- solver display name and WCA ID when already public;
- event and date;
- official/unofficial status;
- solve time;
- raw scramble;
- raw reconstruction;
- reconstructing author when supplied;
- source/video URLs when supplied;
- raw-byte provenance/hash;
- parsed move/annotation stream;
- geometry eligibility status;
- duplicate-cluster identity.

No private or inferred demographic attributes are added.

## Reconstruction semantics

Raw reconstruction text is never overwritten.

A reconstruction is parsed into ordered events:
- FACE_TURN
- ROTATION
- WIDE_TURN
- SLICE_TURN
- ANNOTATION
- UNKNOWN

Whole-cube rotations `x/y/z` are viewpoint/frame operations in the notation stream. They must not be silently counted as physical face turns.

Human labels such as `// cross`, `// 1st pair`, `// OLL` and `// PLL` are preserved as reconstruction annotations. They are useful method/chunk annotations, not direct evidence that the solver represented the state in exactly that form.

## Initial scientific questions

1. At each human move, what are `q`, `d1`, shortest entry-cost fiber and available +1 slack value?
2. How often do experts choose actions that improve downstream slack geometry without minimizing immediate phase distance?
3. Where do reconstruction-authored boundaries align or misalign with Kociemba G1 crossing, local distance discontinuities and cost-fiber changes?
4. Are apparent policy regularities robust to solver, method, source and duplicate reconstruction?
5. Which naturalistic contrasts should replace or refine the prospective G7-P1 matched-state experiment?

## Duplicate policy

Deduplicate in layers:

1. exact source-native record identity;
2. exact normalized scramble + normalized move stream;
3. same public solver + competition/date/time + scramble;
4. cross-source near-duplicate candidate.

Cross-source duplicates are linked, not deleted. The highest-provenance raw record remains preserved.

## First-stage authority ceiling

G7-P2 may build corpus infrastructure and analyze public reconstruction data.

It must not:
- claim that public-web availability grants unrestricted redistribution rights;
- infer private traits from solver identities;
- equate step comments with cognitive states;
- mix unofficial reconstructed timing with official WCA timing without an explicit join;
- silently drop rotations/wide/slice moves to force compatibility with the current HTM kernel.

## P2 initial gate

PASS_INTAKE_READY requires:
- source registry valid;
- canonical schema valid;
- parser preserves raw event order and annotations;
- Drive intake/raw/derived/release destinations grounded;
- automated acquisition restricted to sources whose access path and reuse status support it;
- manual-intake manifest generated for blocked sources.

PASS_CORPUS_READY requires actual raw snapshots plus deterministic normalization and duplicate audit.

No naturalistic scientific conclusion is authorized before PASS_CORPUS_READY.
