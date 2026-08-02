# CUBE-REV 0.8.15 Validation Report

## Official title

**CUBE-REV 0.8.15 — Cognitive Mechanism-axis Lattice, Strategy-transition Signatures & Identifiability-constrained Hypothesis Registry**

## Official decision

> **PASS-MECHANISM-AXIS-LATTICE / PASS-PLANNING-HORIZON-POSITIVE-CONTROL / PASS-STRATEGY-TRANSITION-POSITIVE-CONTROL / PASS-OPEN-CLOSED-LOOP-NEGATIVE-CONTROL / PASS-CAPACITY-TRAIT-NEGATIVE-CONTROL / HOLD-ORIENTATION-EQUIVARIANCE-SINGLE-PAIR / HOLD-CHUNK-BOUNDARY / HOLD-RECOVERY-TRAJECTORY / NO-PARTICIPANT-INSTRUMENT-CHANGE / NO-HUMAN-MECHANISM-CLAIM**

## Executive finding

CUBE-REV 0.8.15 returned the program from release-integrity work to its original cognitive-science question: what latent processes can produce different cube decisions, and which of those processes can the current instrument actually distinguish?

The version did not add another participant-facing variable simply because it was psychologically interesting. It first constructed a mechanism lattice with explicit observables, falsifiers, measurement hazards, and required instrument extensions. It then ran a deterministic synthetic identifiability audit over the existing 28 opaque stimuli and 24 counterbalanced schedules.

The central result is asymmetric:

- deliberately distinct shallow-versus-deeper action policies and a stationary-versus-change-point policy produced separable current traces in the synthetic positive controls;
- open-loop versus closed-loop control and high-versus-low visuospatial capacity were deliberately assigned identical current observables and remained at chance, correctly demonstrating that latent labels cannot be recovered from first action and latency alone;
- the bank contains only one rotationally equivalent stimulus pair, so orientation-equivariance cannot yet support a stable trait interpretation;
- single-action trials contain no within-sequence chunk boundaries or post-error recovery path, so chunk switching and recovery monitoring remain structurally unidentifiable.

These are instrument-identifiability findings. They are not evidence that any participant uses horizon 1, horizon 3, chunks, open-loop control, or a particular capacity state.

## RAVEL closure

### Discover

The preceding versions secured resume, submission, browser, custody, and staging boundaries. That work made the data path more trustworthy but did not itself expand the cognitive theory. The research problem was therefore restated:

> Given the current 28-trial first-action task, which competing cognitive mechanisms yield distinct observable distributions, which collapse into observational equivalence, and what is the minimum non-reactive extension required to separate them?

### Plan

The version separated five tasks:

1. define candidate mechanism axes without prematurely assigning participant traits;
2. calculate stimulus-level signatures that can distinguish shallow and deeper action evaluation under a transparent heuristic;
3. build synthetic positive controls that should be distinguishable;
4. build synthetic negative controls that should remain indistinguishable;
5. audit the existing bank and schedules for rotational, temporal, chunk, and recovery support.

Predeclared interpretation thresholds for repeated pairwise balanced accuracy were:

```text
>= 0.80   IDENTIFIABLE in this synthetic audit
>= 0.65   PARTIAL
<  0.65   NON_IDENTIFIABLE
```

These thresholds are engineering promotion rules, not universal psychometric standards.

### Execute

The implementation models the 24 stickers of a 2×2 cube, all 18 face turns, and all 24 proper whole-cube rotations. For every current stimulus it computes a transparent solved-sticker action heuristic at horizons 1, 2, and 3. The heuristic is intentionally simple and reproducible; it is not asserted to be the participant's objective function or the shortest-path solution metric.

Eleven generators were simulated:

```text
greedy_h1
lookahead_h2
lookahead_h3
strategy_switch_h1_to_h3
perseverative_interference
stochastic_exploration
orientation_frame_alias
open_loop_chunk_unobserved
closed_loop_monitor_unobserved
high_capacity_same_policy_unobserved
low_capacity_same_policy_unobserved
```

Each generator produced 240 sessions, yielding 2,640 sessions across all 24 schedules. Session-level observables were restricted to quantities derivable from the current instrument: action agreement with each heuristic horizon, action and face entropy, repetition rates, mean and dispersion of latency, and early-versus-late differences.

### Verify

The full run used:

```text
seed                    8152026
mechanisms              11
sessions per mechanism  240
simulated sessions      2640
stimuli                  28
schedules                24
pairwise split repeats   31
```

The independent test suite reran the generator twice and required byte-identical deterministic outputs, exact bank/orbit counts, two positive controls, two negative controls, and registry prohibitions.

### Iterate

The first registry test incorrectly required every axis to contain a `falsifier` field, although non-identifiable axes correctly expressed their boundary through `required_extension` or `measurement_hazard`. The test was repaired to accept all three explicit epistemic controls rather than weakening the registry.

The larger conceptual iteration was to reject an attractive but invalid inference: because working-memory capacity or open-loop control is cognitively meaningful, it does not follow that the current first-action trace identifies it. Those mechanisms were retained in the lattice but demoted from estimands to extension requirements.

## Track A — Mechanism-axis registry

The registry adopts two governing rules:

```text
BEHAVIORAL_SIGNATURE_FIRST_PSYCHOLOGICAL_LABEL_SECOND
NO_TRIALWISE_SELF_REPORT_ADDED_IN_0_8_15
```

| Axis | Current status | Present observables | Main boundary |
|---|---|---|---|
| Planning horizon | synthetic identifiability tested | first action, latency, state-specific horizon values | matching a heuristic is not proof of conscious lookahead |
| Strategy arbitration | synthetic identifiability tested | position, action, latency, previous action | item-order mixture can imitate change |
| Orientation equivariance | bank support audited | rotational pair and transformed action | only one pair exists |
| Chunk retrieval/switching | partial or unidentifiable | motif repetition, action consistency | no within-sequence boundary timing |
| Open/closed loop | negative-control non-identifiable | first action only | subsequent states/actions absent |
| Recovery monitoring | not identifiable | none | no error opportunity and recovery trajectory |
| Visuospatial capacity | do not infer as trait | first action, latency | compensatory policies can be observationally identical |
| Metacognitive monitoring | post-task only | global confidence and guess | trialwise probing may change strategy |

Forbidden claims include inferring working-memory capacity from first-action traces, conscious planning from latency alone, chunking without repeated motifs or boundary timing, and recovery strategy without an observed error and subsequent trajectory.

## Track B — Stimulus-level horizon audit

Among 28 stimuli:

```text
h1 versus h2 optimum sets disjoint     9
h2 versus h3 optimum sets disjoint     8
h1 versus h3 optimum sets disjoint    13
h1 versus h2 optimum sets different   23
h2 versus h3 optimum sets different   19
all three optimum sets identical       3
```

Thus the current bank contains many states on which the chosen transparent heuristic predicts different first actions at different depths. This is a necessary positive-control condition for testing horizon-sensitive signatures.

It is not sufficient for a psychological planning-depth claim because:

- the solved-sticker score is only one surrogate utility;
- multiple actions can tie at a horizon;
- a memorized pattern policy can match a deeper heuristic without online simulation;
- motor or orientation preferences can produce the same first action;
- the task observes only the first move, not the imagined continuation.

## Track C — Synthetic identifiability controls

### Overall classifier

A nearest-centroid classifier over eleven standardized session features achieved:

```text
test sessions       924
overall accuracy    0.7208
balanced accuracy   0.7208
```

The overall score is descriptive only. It mixes deliberately separable and deliberately identical generators, so it is not the promotion criterion.

### Predeclared pairwise controls

Each pair was evaluated across 31 repeated train/test splits.

| Contrast | Mean balanced accuracy | SD | Min–max | Decision |
|---|---:|---:|---:|---|
| greedy h1 vs lookahead h3 | 1.0000 | 0.0000 | 1.0000–1.0000 | IDENTIFIABLE positive control |
| stationary h1 vs h1→h3 switch | 1.0000 | 0.0000 | 1.0000–1.0000 | IDENTIFIABLE positive control |
| open-loop vs closed-loop after identical first action | 0.5148 | 0.0312 | 0.4583–0.5893 | NON_IDENTIFIABLE negative control |
| high vs low capacity with identical compensated policy | 0.5108 | 0.0335 | 0.4524–0.5714 | NON_IDENTIFIABLE negative control |

The negative controls are a required success, not a failure. The implementation must not manufacture information about a latent variable after both generators have been defined to produce the same observed action and latency process.

### What the positive controls establish

They establish only that the current feature construction can distinguish these deliberately separated synthetic generators under the present bank and schedule design. They do not establish:

- that real participants optimize solved stickers;
- that a participant matching h3 performs explicit three-step search;
- that early/late change is endogenous strategy switching rather than fatigue, learning, or item mixture;
- that nearest-centroid classification is an adequate final human estimator.

## Track D — Orientation and schedule audits

### Rotational support

The 28 stimuli occupy 27 whole-cube rotational orbits. The only repeated orbit is:

```text
CR086-S002
CR086-S003
```

Exactly one proper rotation maps the first state to the second. Across 24 schedules:

```text
S002 before S003   18 schedules
S003 before S002    6 schedules
separation range    7–21 trials
mean separation     10.5 trials
```

The audit therefore returns:

```text
SINGLE_ROTATIONAL_PAIR_INSUFFICIENT_FOR_STABLE_TRAIT_INFERENCE
```

A single pair can serve as a canary or exploratory within-person contrast, but cannot separate stable object-centered mapping, viewer-centered aliasing, memory of the earlier item, and order effects.

### Schedule-position mixture

Horizon-discriminating item rates in the first and second halves differ by at most 0.0714 within a schedule. Across the 24 schedules the signed mean difference is 0, while mean absolute difference is 0.0714.

Counterbalancing therefore removes the average directional imbalance but does not make every individual schedule locally exchangeable. Any human change-point model must condition on stimulus identity or state-level discrimination, not merely compare the first 14 and last 14 trials.

## Track E — Required future instrument extensions

The 0.8.15 promotion decision does not add participant burden. It specifies what a later instrument would need.

### Orientation-equivariance extension

Require multiple rotational families, multiple rotations per family, balanced direction/order, and transformed-action scoring. A single duplicate orbit must not carry a trait interpretation.

### Chunk-boundary extension

Require short multi-action trajectories containing repeated structural motifs, timestamps for each action, and planned motif-boundary perturbations. First-action repetition alone is insufficient.

### Open/closed-loop and recovery extension

Require intermediate cube states, subsequent action timestamps, controlled error opportunities or naturally identified deviations, undo/reset/continue signatures, and preservation of the full correction path.

### Strategy-transition extension

Retain counterbalancing, add enough horizon-discriminating states to both early and late windows, and estimate a state-conditioned change point rather than a raw half difference.

### Metacognitive boundary

Retain non-reactive global post-task measures. Trialwise confidence is not introduced until a separate reactivity experiment shows that it does not alter the action policy being measured.

## Scientific and engineering separation

No participant page, cognitive bank, schedule, Collector file, production entry, or Apps Script contract is changed in 0.8.15. The version is an offline research layer that audits what the existing instrument could support and what a later version would need.

The analysis outputs may be regenerated and Factory-linked later, but they must not be joined to participant rows as if they were observed latent states. Horizon scores are stimulus annotations; mechanism labels in the synthetic dataset are simulation truth only.

## Official result

```text
PASS_IDENTIFIABILITY_LATTICE_WITH_NEGATIVE_CONTROLS
```

Interpretation:

- planning-horizon-sensitive first-action signatures: eligible for later human estimand design, not yet a human finding;
- within-session strategy transition: eligible only with state-conditioned analysis and item-mixture controls;
- orientation equivariance: bank expansion required;
- chunking and recovery: trajectory instrument required;
- open/closed loop and capacity traits: prohibited from current-trace inference;
- trialwise confidence: withheld because it may be reactive.

## Next boundary

The next version should not indiscriminately add all missing measurements. It should design the smallest participant-safe extension that breaks the highest-value observational equivalences while preserving the existing blinded task and non-reactive measurement boundary.
