# BW — Constructive terminal decoder

Base: 1b81d961cf7030073994efff4b1b8595ff57982a. Research checkpoint, not Lean acceptance.

## DFS: constructive inverse
`CornerTranscriptBit.cornerTranscriptBit` is noncomputable and proves factorization, not executable recovery. `CornerPairDecoder.cornerCyclicPair_injective` supplies a finite inverse: search the 24 oriented corners for the observed ordered pair. The actual schedule in `NineteenSchedule` is [0,1,6,7,9,10,18,19,21,22,12,13,3,21,21,21,21,21,4]. Zero-based transcript index pairs by position: 0:(0,1), 1:(12,18), 2:(2,3), 3:(4,5), 4:(10,11), 6:(6,7), 7:(8,9). Position 5 is missing. For the seven decoded oriented IDs x, recover p5 = 28 - sum(x/3), t5 = (3 - sum(x%3)%3)%3. Pack 3*p5+t5. Require exact length 19, valid pairs, distinct piece IDs, consistent repeated address 21, sum <=28 and p5<8. Reject invalid inputs rather than relying on truncated subtraction or default indexing. For legal inputs, finite inverse correctness and conservation imply the original coordinate at every position; alternatively reuse corner_fourteen_unique_missing_five once output legality is established. Compute parity with existing cornerPermutationParity; reuse observedTerminalCorrectedParity for the prefix correction. No state or future replies enter the decoder. Full coordinate decoder preferred over a duplicate sign-only implementation.

## BFS and foundation
`PairedCornerClock.observed_corner_colors_eq_schedule` links charged observations to the schedule. The clock currently discards corner responses for edge decisions; final executable composition must retain them in a logged output. A fresh last sticker does not prove that sign is ambiguous at every earlier state. No such stronger claim is required. `Fits 19` alone permits failure outputs; total recovery on reachable states must be proved separately. Raw-prefix witness and root coverage are independent of corner decoding.

## Research priorities (judgment scores, not measured probabilities)
| Obligation | E | N | U | S | P |
|---|---:|---:|---:|---:|---:|
| Finite inverse | .99 | 1 | .99 | .99 | .98 |
| Missing corner arithmetic | 1 | 1 | .99 | .98 | .99 |
| Charged transcript to executable decoder | .99 | 1 | 1 | .96 | .99 |
| Physical address routing | .87 | 1 | .95 | .89 | .95 |
| Universal prefix coverage | .97 | 1 | .99 | .95 | .98 |
| Prove early sign ambiguity for every state | .30 | .05 | .05 | .40 | .12 |

Acceptance: finite pair inverse, exact schedule extraction, conservation, legal-input totality, malformed-input rejection, no hidden state in executable decoder, pinned Lean CI, axiom audit. No new dependency or alternate enumeration. No CI or implementation acceptance claimed here.
