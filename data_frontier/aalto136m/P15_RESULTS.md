# G3-P15 result: SOURCE-INTEGRITY_HOLD

The immutable original Aalto archive was acquired and placed in private,
owner-only Drive custody as a 16-part byte-preserving split. Archive SHA-256:
`5fb217e0e1273017a6789c5c7ebcc00eed624f2f6426c284da2077a88e270420`.

The full four-shard source census observed 2,495,387 transcriptions from
168,593 source participants and 121,291,605 raw rows. Filename and metadata
participant identifiers have a one-to-one intersection of 168,593, with one
metadata-only identifier (`3`); metadata remains unused in confirmatory work.

The first conservative stream compiler reported final-input versus reconstructed
stream disagreement in 1,770,441 / 2,495,387 streams (70.949%). This is not an
error-rate result and is not comparable to the near-rival's reported figure.
The source includes non-displayable/KEYCODE fallback values, modifier keys, and
180 missing-target streams; the current adapter deliberately refuses to guess
the missing keycode-to-output mapping. Therefore reconstruction sensitivity,
episode semantics, repeated-error hazard, timing geometry, and any cross-corpus
claim are **not authorized**.

No P15 cognitive or failure-state-persistence verdict is issued. The next
authorized work is a bounded adapter mapping audit against raw keycode classes,
with a synthetic/known-key validation set and a rerun of the source-integrity
census before any hazard analysis.
