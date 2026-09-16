# G3-P15-R1 final-input revalidation

## Frozen policies

- **R0:** failed diagnostic baseline using keycode-to-character coercion. It is
  retained only to localize the original 70.9486% disagreement.
- **R1:** recorded Layer L is authoritative for literal output; Layer K may
  classify controls but never supplies an ordinary character.
- **R2:** conservative observable-only subset of R1, excluding any stream with
  `UNKNOWN`, `AMBIGUOUS_OUTPUT`, or `DELETE`.

No adapter rule was selected or changed by optimizing agreement with
`USER_INPUT`. Final-input agreement is a validation target only.

## Full-source result

There were 2,495,387 streams. The 180 streams without a target sentence were
excluded from the validation denominator, leaving 2,495,207.

| Classification | N | Share of eligible |
| --- | ---: | ---: |
| `EXACT_MATCH` | 1,730,213 | 69.3415% |
| `NORMALIZATION_ONLY_MATCH` | 0 | 0.0000% |
| `SOURCE_EXPLAINABLE_MISMATCH` | 0 | 0.0000% |
| `AMBIGUOUS_RECONSTRUCTION` | 279,648 | 11.2074% |
| `UNEXPLAINED_MISMATCH` | 485,346 | 19.4511% |

R1 disagreement is 764,994 / 2,495,207 = **30.6585%**. The 279,648
ambiguous mismatches contain at least one unobservable/ambiguous output or
Delete operation. They are not repaired from keycode.

## Conservative observable-only result

R2 admits 2,211,671 streams (88.6367% of target-eligible streams). Exact
agreement is 1,726,325 / 2,211,671 = **78.0552%**. NFC and CRLF normalization
adds no matches. The remaining 485,346 / 2,211,671 = **21.9448%** mismatch is
not explained by the sealed observable semantics.

## Court verdict

**`SOURCE_INTEGRITY_HOLD`** remains in force. Collector semantics, the adapter,
and the emulator are now explicit, but a high-mass Layer-L gap exists and the
apparently clean R2 subset retains 485,346 unexplained final-input mismatches.
The source therefore does not yet support an authoritative P15 error-state
object. `PARTIAL_OBSERVABILITY_ONLY` is denied because the candidate subset
does not pass reconstruction validation; it must not be used for hazard or
peri-error analysis.

The permitted successor is a bounded source-artifact resolution audit: locate
an original Aalto representation or export semantics that can explain the
R2 mismatch. If none exists, abandon the Aalto error-state lane.
