# G7-P2 reco.nz bounded live probe — receipt

## Verdict
**PASS_RECO_BOUNDED_LIVE_PROBE / BULK_ACQUISITION_HOLD**

## Exact authority
- trigger/science HEAD: `c8da39f5ea422f0280378e9e2fa1d232d3deae57`
- bounded probe run: `36683725641` — SUCCESS
- regular G7-P2 intake run on same head: `36683732964` — SUCCESS
- artifact: `11082494208`
- artifact SHA-256: `387875ffd85ab5eb4b6df6a5537e54691d3544b12834899a2dd0def3da39794a`
- Drive registry receipt: `1h1aOb8JAxW1-OIRXV28r6yCljPSALtbt` — readback verified

## Live probe
Acquisition policy:
- source: reco.nz SSR HTML
- index pages fetched: 1
- puzzle filter: `3x3`
- maximum solves: 5
- request delay: 2000 ms
- robots check: `ABSENT_404`
- raw HTML preserved only during the run
- raw HTML was not uploaded as an artifact

Observed index:
- rows: **50**
- eligible 3×3 rows: **45**

Fetched solves:
- 14134
- 14133
- 14132
- 14131
- 14130

Validation:
- HTTP acquisition succeeded: 5/5
- parsed puzzle = 3×3: 5/5
- nonempty scramble/reconstruction: 5/5
- stage statistics present: 5/5
- raw public release: **NO**

## Interpretation
The live server-rendered HTML is compatible with the G7-P2 parser and acquisition design.

This does **not** authorize a full-site mirror. No explicit bulk export/API or redistribution terms have been grounded. The active mode remains bounded acquisition for validation/research preparation only.

## Next corpus gate
`PASS_CORPUS_READY` still requires a source-authorized or manually supplied raw corpus, deterministic normalization, duplicate audit and exact move-by-move geometry replay.
