# CUBE-REV G3-P34-R2 execution receipt

## Scope and authority

- Binding enumeration authority: `G3-P34-AUTH-v1` (P34-R1).
- Baseline Lane A bank: `p34-bank.json`, SHA-256 `cef57e7943510d15d2bfbb59f18761217599f9d5c7b749511a02d1c371e9ae00`.
- No human data, scientific interpretation, Paper I/H33 mutation, browser installation, or browser launch occurred.

## Executed commands

```text
node g3-cog/p34-runtime/replay-browser-independent.mjs
node --check g3-cog/p34-runtime/replay-browser-independent.mjs
```

The first completed replay localized a receipt-only mismatch: JSON key order in
`family_counts` differed although all three values agreed.  The producer was
changed only to emit the binding `R/L, U/D, F/B` key order and the full replay
was rerun.  The final receipt below is from that second full run.

## Direct replay method

`replay-browser-independent.mjs` derives all transitions through the recovered
canonical `state-adapter.js`; it does not import the Lane A accelerated move
permutation table and does not instantiate Playwright, a DOM, or a renderer.
It regenerates the R1 start/prefix/suffix/core authority, re-enumerates the
196,608 candidate domain, reconciles each admitted duplicate key to the Lane A
bank, recomputes every stored terminal hash and row field, and replays every
synthetic S/R/G fixture.

## Final exact-equivalence result

- Move alphabet/order: exact PASS.
- Enumeration authority: 16 starts, 16 prefixes, 8 suffixes, 96 cores; exact PASS.
- Candidates/admitted/final: 196,608 / 109,184 / 109,184; exact PASS.
- Unique start/terminal hashes: 16 / 107,584; exact PASS.
- Exclusion census and family/QTM counts: exact PASS.
- Row-field mismatches: 0.
- Terminal-state hash mismatches: 0.
- Each S/R/G fixture class: 218,368 PASS / 0 FAIL.
- Residual replay failures: none.

## Artifacts

- `replay-browser-independent.mjs`: 16,310 bytes; SHA-256 `421a4b3922fc1e1895f8f9eb2f4b3a545e108e7f6e71eee8ccd9bd7f6906041c`.
- `p34-r2-replay-receipt.json`: 2,333 bytes; SHA-256 `ea5358dd2839fca95c2955d49f442c1dc0e8e80fceee444507d89e88d37efdc9`.
- Lane A compiler remains `build-bank.mjs`, SHA-256 `3575538d9a988b992044adc67b655423659a77cfc4625fe2b31f364581b19fe0`.
- Canonical state adapter remains SHA-256 `a7a083bbd37a5e111a86cc4669a9a8b539c6968eef6f36d5d783edc94b5cba9b`.

## Boundary and gate

`BROWSER_DEPENDENCY_CLOSED_FOR_SEMANTIC_REPLAY_ONLY`: exact semantic replay no
longer requires the missing Playwright dependency.  No DOM, render, or pixel
equivalence is asserted.  Per the requested R2 gate, P35 is authorized only as
a successor decision/action under this exact-equivalence result; this receipt
does not create P35 or promote any scientific claim.

Final verdict:

`EXACT_CROSS_LANE_SEMANTIC_EQUIVALENCE_PASS / BROWSER_DEPENDENCY_CLOSED_FOR_SEMANTIC_REPLAY_ONLY / NO_DOM_OR_PIXEL_CLAIM / P35_AUTHORIZED_BY_EXACT_CROSS_LANE_SEMANTIC_EQUIVALENCE_ONLY / NO_SCIENTIFIC_PROMOTION`
