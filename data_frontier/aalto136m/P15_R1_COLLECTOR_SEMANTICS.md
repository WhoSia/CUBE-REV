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
