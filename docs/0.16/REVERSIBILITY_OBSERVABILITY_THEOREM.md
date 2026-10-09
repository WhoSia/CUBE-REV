# CUBE-REV 0.16 — internal pure-math inverse-information results

**This document belongs ONLY to the existing CUBE-REV 0.16 formal version.** It is not a new project title, empirical cognition theory, or entire-cube solver.

## Exact finite observer model

One tracked Rubik's UR edge, 12 physical edge positions, two intrinsic flip values (24 unknown initial source coordinates). Legal actions are all 18 HTM face tokens; each is a physical permutation of these 24 states. An *ideal* binary orientation report is read immediately AFTER each chosen move, and action choices may depend on previous reports. There is NO extra observation at time zero.

### Three mathematical inverse problems

1. **Known action word:** if the complete executed word `w` is retained, applying `w⁻¹` undoes that word exactly, without any observation. Group-theoretic inversion is trivial relative to a known history.
2. **State diagnosis:** identify the unknown original tracked-edge state by its feedback-controlled sequence of reported bits. For current candidate set `E`, the exact Bellman leaf recursion is `D_h(E)=max_a[D_(h-1)(T_a(E)∩O0)+D_(h-1)(T_a(E)∩O1)]`, with `D_0(E)=1` if nonempty. For full 24-state uncertainty, the exact horizon-0..8 leaf values are **1, 2, 4, 6, 8, 12, 16, 20, 24**. **Minimum worst-case adaptive diagnosis length = 8** moves; the binary cardinality bound alone gives only `ceil(log₂24)=5`. Independent C++ and Python physical-transition complete recursion plus 24 distinct source traces verify both.
3. **Physical restoration to a fixed tracked-edge target:** Let the target be coordinate (slot0,flip0). A controller may stop early on any branch but must send all 24 possible initial edge states to exactly this one physical coordinate. `R_h(E)` holds if `E=∅` or `E={target}`, or there is a legal action `a` for which both feedback successor sets satisfy `R_(h-1)`. Full 24 states return false for h≤9 and true for h=10. **Minimum worst-case adaptive tracked-edge reset length = 10**, verified by independent C++ complete recursion and a physically replayed Python full24 reset decision tree. Known current edge states are individually correctable in at most three moves, but the naive diagnose-then-correct bound8+3=11 is not tight.

### General reversible-state lemma (elementary, classical context)

For |S|>1 possible initial states and purely bijective actions, no single precommitted action word can map all S to an identical exact physical target: composition of bijections is injective. Moreover if a deterministic feedback-and-stop controller maps all initial states in S to one common target, no two initial states can yield the same complete sensor-output path; that would choose the same word and violate injectivity. Therefore at least |S| distinct terminal observation transcripts are necessary, so a binary feedback policy of depth h requires at least `h≥ceil(log₂ |S|)`. The model-specific extra delay (diagnosis8, reset10) comes from the constrained geometry of legal moves and observation bits, NOT from a universally new theorem that reversible systems are opaque.

### Lost historical word versus finding a correction word

Starting from known tracked-edge source coordinate (slot0,flip0), there are 18⁴=104,976 four-action token words. Exactly **26,584** yield the SAME ending tracked-edge coordinate (slot0,flip0). Thus if ONLY starting and ending tracked-edge coordinates are known, a worst-case fixed-length external record sufficient to reconstruct the EXACT four-token history must represent at least 26,584 alternatives and hence contain at least **15 bits** (14 bits have only 16,384 possibilities). This **does not** apply unchanged when the entire cube state, the executed token log, extra visual clues, or a restricted grammar is available. For independently uniformly chosen four-token words, direct endpoint counting yields conditional Shannon entropy of the unrecorded word given final *edge coordinate* ≈13.039762202 bits; this is not a biological memory estimate.

## Separate minimum catalogue theorem inside 0.16

The four-action 1,192-basis universal separating-word dictionary from the earlier P5/P6 sequence has a new exact interval **25≤M*≤34**. The original P6 60-support rational dual certificate has integer numerator mass 476 and all legal words cover at most20 dual units. All 104,976 words yield exactly 1,913 distinct full original-slot observation partitions, with dual-coverage numerator distribution 0:1,317; 4:340; 8:76; 12:12; 16:6; 20:162. Any hypothetical 24-word solution has capacity≤480 and needs≥476, so it cannot select a word of weight≤12 (that wastes≥8). All selected words must lie in only **168** partition types with weights16/20. A complete 60-bit, 168-candidate C++ exact-depth ≤24 cover search explores **144 exact covered-set states /243 branch expansions** and proves those 60 positive dual bases cannot ALL be covered. Independently a SciPy/HiGHS 60×168 integer feasibility check returned INFEASIBLE. The C++ exact integer DFS, with sound remaining-mass branch pruning, is the reproducible machine-assisted proof. The previous 34-word explicit covering construction persists. **Exact minimum M* remains OPEN** and neither solver's partial time limit is an optimality proof.

## Literature context and limits

Preset/adaptive distinguishing and homing sequences for reversible/permutation automata are CLASSICAL. See Lukac et al. (2019), DOI [10.2298/FUEE1903417L](https://doi.org/10.2298/FUEE1903417L), and the homing-sequence automata inference line, DOI [10.1006/inco.1993.1021](https://doi.org/10.1006/inco.1993.1021). The novelty here is the **specific bounded cube action/sensor finite optimum**, not the generic existence of reversible ambiguity.

The original informal puzzle — why people sometimes cannot reverse their scramble from memory — **is not solved as a cognitive claim**. The mathematics isolates which extra assumptions would be needed: word retention, partial-state sensing, a fixed vs adaptive policy, an explicit target, sensor noise and a memory constraint. The observed four-turn 15-bit side-log lower bound is for reconstructing the exact *historical word from a single edge-coordinate endpoint*, NOT a claim about people's cognitive thresholds.

Authoritative receipts, full action trees, per-endpoint counts and independent C++/Python/Node proof programs are preserved under the private CUBE-REV 0.16 Library custody and the canonical 0.16 Notion §§23–25. GitHub public tests use only math/model geometry, not original private human solve traces.
