# G3-P11 — Cross-task RSTP prediction isomorphism

This document pre-seals what is shared between the Cube and navigation instruments before any human outcome exists.

## Shared causal skeleton

Both tasks instantiate:

1. exact physical-state transposition at a probe state `s*`;
2. an outcome-blind history-context functional `K(h)`;
3. a context-equivalent control family and a context-divergent family;
4. a representation intervention `R` that may change available identity information but cannot change physical state, transition law, goal, or legal actions;
5. first committed action as the primary response;
6. latency only as a secondary response;
7. opaque cell identity and a session manifest sealed before response.

The action alphabets are **not** identified across tasks. Cube moves and navigation directions are not treated as homologous response categories.

## Domain mapping

| Component | Cube instrument | Navigation instrument |
| --- | --- | --- |
| physical state | exact cube configuration | exact torus position |
| history | passive six-move cube sequence | passive six-step route |
| `K(h)` | prospectively computed task/option context | prospectively computed landmark-context state |
| `R=1` | stable neutral pair-identity markers | stable neutral place-identity labels |
| probe | same cube configuration | same `(1,1)` torus position |
| response | first committed legal cube move | first committed N/E/S/W move |
| nondegeneracy | at least two near/equal admissible continuations | two exactly optimal continuations (`N`,`E`) |

Legacy field `O` is retained only as the six-cell encoding of **context-equivalent control (`O=0`) vs context-divergent family (`O=1`)**. P11 does not promote `O` as a universal psychological option variable.

## Cross-task effect metric

For each task, define history divergence within a matched cell family by normalized Jensen–Shannon divergence

`D = JSD(P_A, P_B) / ln(2)`, so `0 <= D <= 1`.

The two presealed contrasts are:

`Delta_K = D(context-divergent, R0) - D(context-equivalent control, R0)`

`Delta_R = D(context-divergent, R0) - D(context-divergent, R1)`.

These contrasts compare **structure**, not raw action identities or raw effect magnitudes.

## Rival predictions

- **State-only controller:** `Delta_K ≈ 0`; history divergence should not systematically exceed the control family once `s*` and goal are fixed.
- **Generic episodic/history trace:** both control and divergent histories may differ, but selective `Delta_K > 0` is not required.
- **History-derived control/context account:** `Delta_K > 0` is expected; the effect may remain under `R=1`.
- **Representation-maintenance account:** `Delta_K > 0` under `R=0`, with selective attenuation/reorganization under `R=1`, yielding positive `Delta_R` under the presealed sign convention.

A result in one task does not authorize inference about the other. Cross-task promotion requires the same qualitative rival-separating contrast pattern under separately valid instruments.

## Promotion boundary

Passing browser certification in both tasks is **RSTP G3 instrument portability** only. It does not establish behavioral transport (`G4`) or mechanism invariance (`G5`). Human collection remains separately gated.
