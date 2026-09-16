# P15-R1 Layer-L adapter schema

## Frozen precedence

`Layer L (stored LETTER) -> observable operation -> Layer T buffer`.
`Layer K (KEYCODE/timestamps)` supplies physical identity, control consistency,
and timing only. It never supplies a character when Layer L is present.

| Layer-L class | Buffer operation | Authority |
| --- | --- | --- |
| one Unicode code point | `EMIT_LITERAL` | authoritative stored token |
| `BKSP`/`BACKSPACE`, or U+0008 with K=8 | `BACKSPACE` | remove final observable code point only |
| `DELETE`/`DEL`, or U+007F with K=46 | `DELETE` | ambiguous without cursor; no mutation |
| SHIFT/CTRL/ALT and navigation/modifier labels | `NON_TEXT` | no buffer mutation |
| missing token | `UNKNOWN` | excluded/flagged, never K-derived |
| other multi-character token | `AMBIGUOUS_OUTPUT` | excluded/flagged |

R0's `chr(KEYCODE)` fallback is retained solely as the failed diagnostic
baseline. R1 cannot be tuned to maximize final-input agreement.

## Protocol delta

- Preserved: raw K fields, stored L bytes, event order, press/release timing.
- Changed from R0: no keycode-to-character coercion; collector control labels
  are explicit operations.
- Lost/unknown: cursor, selection, IME/dead-key composition, and browser events
  not present in the export.
- Falsifier: any emitted character derived from K when L exists, or any
  ambiguous edit silently rewritten as a literal.

Layer T event order is `(PRESS_TIME, KEYSTROKE_ID)`. Missing timestamps remain
explicit and sort after observed press times; no timestamp is imputed.
