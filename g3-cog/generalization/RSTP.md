# Reversible-State Transposition Paradigm (RSTP)

RSTP is a **prospective experimental-design family** for separating current-state sufficiency from history-derived control in tasks with exact reversible dynamics. It is not a universal cognitive law, not a claim that all history effects share one mechanism, and not a relabeling of provenance or transportability theory.

## 1. Formal object

An RSTP task supplies

`T = (S, A, {T_a}, s0, K, R, P)`

where:

- `S` is the physical task-state space;
- `A` is the primitive action vocabulary;
- each `T_a:S→S` is an exact transition with a certified inverse on the admitted state space;
- `s0` is a start state;
- `K(h)` is an outcome-blind history-context functional fixed before behavioral outcomes;
- `R` is a representation intervention that may change available information but not physical state or action legality;
- `P(s)` is the admissible probe-action surface.

The primary transposition object is

`T*(s0,hA) = T*(s0,hB) = s*`

with either `K(hA)=K(hB)` for the state-only/control family or `K(hA)≠K(hB)` for the context-divergent family.

If both histories end in a common suffix `c`, write `hA=uA c` and `hB=uB c`. Because `T_c` is injective under the reversible contract,

`T_c(T_uA(s0)) = T_c(T_uB(s0))  =>  T_uA(s0)=T_uB(s0)`.

Thus the common suffix is a **recency shield**: endpoint equality cannot be created by the suffix itself.

## 2. Minimal admission contract

A family is confirmatory-admissible only if all of the following hold prospectively:

1. exact same physical probe state under an authoritative serializer;
2. exact reversibility/injectivity for the actions used by the family;
3. history/context labels computed without behavioral outcomes;
4. a nonempty common suffix when recency is a live rival;
5. matched or prospectively bounded history burden;
6. a nondegenerate probe surface with at least two admissible continuations;
7. representation support changes information only, not state, transition law, or action legality;
8. both a context-equivalent control transposition and a context-divergent transposition exist;
9. instrument/browser validity is certified separately from cognitive validity;
10. failure to satisfy a contract item is reported as design failure rather than repaired after outcomes are seen.

## 3. Scientific estimand

RSTP does **not** ask merely whether history matters. That phenomenon already has strong adjacent evidence, including same-position chess analyses.

The sharper estimand is whether, at an exact transposition,

`P(a_next | s*, h, R)`

contains structured dependence on a prospectively defined `K(h)` and whether that dependence changes under representation support `R` in a way that separates rivals.

At minimum the design distinguishes:

- **state-only control:** action distribution depends on `s*` but not the pre-probe history;
- **generic contextual trace:** different histories shift behavior without the prespecified `K×R` structure;
- **history-derived control / option context:** the `K` contrast survives exact state matching and need not vanish when representation is supplied;
- **representation-maintenance account:** the history contrast is selectively attenuated or reorganized when external identity support is available.

No one of these labels is inferred merely from a significant history effect.

## 4. Portability is an executable claim

RSTP generalization is tested by the same compiler contract on systems with different algebraic structure, not by listing analogous domains.

The current executable suite contains:

- **Cube:** high-constraint noncommuting reversible manipulation with the P7 same-state/different-history family;
- **5×5 torus navigation (`Z5×Z5`):** reversible spatial translation with a landmark-derived context functional;
- **4-bit hypercube (`(Z2)^4`):** involutive feature toggles with exact state-return/transposition structure;
- **`S4` adjacent-transposition system:** a **non-Abelian** permutation action, included specifically to rule out an accidental dependence on commuting transitions.

The non-Cube witnesses each require:

- exhaustive primitive reversibility over the finite state set;
- one context-divergent transposition;
- one context-equivalent control transposition;
- the same common-suffix contract;
- equal primitive-action histograms inside each matched family;
- a nondegenerate probe action surface.

Passing this suite establishes **compiler portability**, not behavioral or psychological universality.

## 5. Generalization ladder

RSTP uses a five-level promotion ladder so that formal generality cannot outrun world contact.

- **G0 — stimulus existence:** one exact transposition family exists.
- **G1 — within-domain design robustness:** multiple families survive nuisance/burden controls.
- **G2 — algebraic portability:** the compiler contract survives qualitatively different reversible state systems. **Current target.**
- **G3 — instrument portability:** the same manipulation/receipt semantics can be realized in a second behavioral task without changing the estimand.
- **G4 — behavioral transport:** prospectively predicted contrasts replicate across at least two task domains.
- **G5 — mechanism invariance:** a shared latent mechanism is supported across domains. This requires additional evidence and is **not** authorized by G2–G4 alone.

## 6. Domain-admission boundary

Candidate domains include reversible graph navigation, edit/undo tasks, assembly/manipulation tasks, and fully specified game transpositions. A domain is rejected if its nominal `state` omits variables that alter the legal or optimal continuation; otherwise a supposed history effect can be an artifact of an under-specified physical state.

For stochastic tasks, RSTP cannot simply reuse exact-state equality. A future stochastic extension would need a separately predeclared equivalence notion over transition kernels or sufficient states and is outside the current contract.

## 7. Anti-slop boundary

RSTP does not claim:

- that exact transpositions are novel mathematical objects;
- that history dependence is novel;
- that all history dependence reflects options, chunks, episodic traces, or hierarchy;
- that a non-Cube toy witness establishes human generalization;
- that reversible dynamics are necessary for cognition in general.

The present contribution candidate is narrower: **a falsifiable experimental compiler that can make physical-state equality exact while independently manipulating a prospectively computed history-derived context and representation support.** Generalization is earned only when the intervention itself, not just the vocabulary, survives transfer.
