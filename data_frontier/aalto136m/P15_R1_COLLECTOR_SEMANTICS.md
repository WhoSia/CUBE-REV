# P15-R1 collector semantics

Primary collector: `aalto-ui/136m-keystrokes`, commit
`98dcee94dc6c0464b35e8ca43d60e1b225cc621f` (retrieved 2026-09-16).
`typingtest.js` maintains unresolved keypresses across keydown/keypress/keyup;
keydown seeds a static keycode mapping, keypress can overwrite `letter` with
the browser character, and keyup emits press/release/keycode/letter. Thus
`letter` (Layer L), not `keycode` (Layer K), is the source-authoritative token
when present. Keycode classifies controls and validates event identity only.

Layer T is a separately auditable text buffer. It may apply Layer L literals
and observable Backspace operations, but it cannot infer unrecorded selection,
cursor, dead-key, or composition state.

## Sealed source objects

| Object | Git blob |
| --- | --- |
| `public/javascripts/typingtest.js` | `352e3e246cad30b92ed06b9628e41237c7a59b2c` |
| `public/javascripts/keycodes.js` | `44af1e2f535629490a584cf62c8fddd778a52680` |
| `app/models/Keystroke.scala` | `4397058d97aa70256741d7c865c8c1513f99de53` |
| `app/db/Keystrokes.scala` | `2ba5f4cdc1801b4194664f5e569f6ad0226af630` |
| `app/controllers/TypingTest.scala` | `92eba63261ea6bde82291cbbe45a14324999adc7` |

The collector appends a completed record on `keyup`, whereas the observable
text-producing event starts at `keydown` and may be refined by `keypress`.
Layer T therefore uses recorded `PRESS_TIME`, with source keystroke id only as
a deterministic tie-breaker. Source row order remains a separately counted
diagnostic and is not treated as browser event order.

For keycode 8, stored `BKSP`, `BACKSPACE`, or U+0008 is an observable
Backspace control. For keycode 46, stored `DELETE`, `DEL`, or U+007F is an
observable Delete control. This is control classification, not a general
keycode-to-character fallback.
