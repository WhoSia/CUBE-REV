# P15 external near-rival audit: `mikexcohen/typing_errors`

**Status:** registered before CUBE-REV Aalto acquisition and before inspection
of any CUBE-REV substantive Aalto result.

## Object and scope

The external repository identifies itself as *Peri-error timing dynamics in
natural typing*, uses the Aalto 136M Keystrokes corpus, and supplies an
extraction pass plus analysis scripts. Its stated event-locked comparison is
flight and dwell timing around errors versus controls matched by key and
sentence position. It explicitly reports two source concerns: disagreement
between logged final input and a keystroke reconstruction, and nonreliable
participant-metadata joinability. It also emphasizes typist-level bootstrap
uncertainty rather than keystroke-level significance.

This is a near-rival and a diagnostic adversary, not evidence for P15. None of
its findings are imported as CUBE-REV results.

## What is already occupied

- Peri-error flight/dwell descriptions and position-matched controls are not a
  P15 novelty claim.
- A generic observation that timing differs around a typing error is not enough
  for P15.
- Very-large-N p-values are not authority; subject-level resampling is an
  appropriate positive control for uncertainty reporting.

## Reconstruction assumptions to attack independently

| Near-rival design issue | P15 independent audit | P15 consequence if it fails |
| --- | --- | --- |
| Final-input text can disagree with a stream reconstruction | Reconstruct every eligible stream from raw observable keys, compare byte/character-normalized representations under documented normalization, and census disagreement | Preserve both; exclude disagreement cases in a sensitivity; do not silently select a preferred representation |
| Metadata identifiers may not join keystroke streams | Test cardinality, overlap, duplication, and physical invariants before modeling | `NOT_AUTHORIZED`; derive typist baselines from streams only |
| Case-sensitive alignment can create apparent substitutions at capitals | Report case-sensitive and case-normalized diagnostic census, but keep primary target semantics explicit | No word-position claim can rest on capitalization artifact |
| Neighboring errors can contaminate peri-error windows | Analyze episode-collapsed anchors and isolated-error windows in addition to all anchors | Timing pattern is downgraded if it is summed neighboring episodes |
| Rollover may mimic short pre-error timing | Preserve overlap indicator and rerun rollover-excluded timing contrasts | No haste/anticipation language from a rollover-driven pattern |
| A correction can generate a cluster of key-level discrepancies | Make episode collapse primary; key-level events remain diagnostic | Repeated-error persistence is not established by edit mechanics |

## Matching/control logic: reuse only as a positive control

P15 will independently reproduce the narrow positive-control component:
context-matched correct anchors using target key and sentence/position when the
source schema permits, with typist-resampled uncertainty. It will not copy a
derived event table or a conclusion from the near-rival.

P15 extends the question in a prespecified direction the near-rival does not
settle: whether an episode-collapsed error predicts an **elevated future error
hazard** across frozen lags after typist propensity, exact local execution
context, position, and edit mechanics are controlled. A peri-error timing curve
alone cannot distinguish point errors, difficult context, stable person
propensity, and a short persistent failure state.

## Adversarial interpretation rules

1. A reproduced timing contrast is only a positive control, never the P15
   endpoint.
2. A persistence estimate must survive the full P15 compiler and controls; it
   cannot inherit the near-rival's event definition.
3. If P15's result is consistent with local context, capitalization, rollover,
   or adjacent-episode contamination, that explanation wins over a state
   interpretation.
4. Even a surviving P15 persistence signature supports a structural
   cross-corpus comparison with WCA, not a shared cognitive mechanism.

## Sources consulted

- Original Aalto dataset page, accessed 2026-09-15.
- `mikexcohen/typing_errors` repository README and public analysis inventory,
  accessed 2026-09-15.

No Aalto raw byte or CUBE-REV Aalto-derived result was used in this audit.
