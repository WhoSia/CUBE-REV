# CUBE-REV 0.16 — manuscript architecture and release gate

**Document type:** internal publication design, NOT a claim of journal acceptance, a finished article, a new empirical human result, or a formal project title. CUBE-REV 0.16 remains OPEN while its successor may begin as an **organic change of explanatory scale** according to the NOMOS/Research OS version doctrine.

## Current best paper: theoretical computer science with discrete-mathematical core

**Working manuscript title (not the formal CUBE-REV version name):**

> *Reversible Experiments and Forgotten Action Histories in a Rubik Edge Automaton*

**Target community:** theoretical computer science (automata and algebraic/graph combinatorics) first; discrete applied mathematics second. Journal scopes of Theoretical Computer Science (algorithms, automata, complexity, formal methods) and Discrete Applied Mathematics (combinatorial algorithms and applications) accommodate this mathematical rather than human-experimental contribution. A purely discrete-math journal demands an especially strong novel general theorem beyond one finite object. Cognitive science is **not an empirically supported venue** for the current intrinsic-bit ideal-sensor results.

### Draft abstract — provisional

We study exact-state identification, feedback-controlled reset, and historical action-word reconstruction in a finite reversible automaton induced by a tracked edge of the Rubik's Cube. The action alphabet consists of eighteen half-turn-metric face tokens, and the tracked edge has twenty-four physical position–orientation coordinates. We distinguish invertibility of a known action word from identifiability of an unknown initial state and reconstructibility of an unrecorded action history. The action-count multigraph of the twenty-four edge states admits an incidence representation over an oriented double cover of the octahedral face graph, with exact spectrum \(18,16,14,12,10\) and multiplicities \(1,2,6,2,13\). This yields a closed expression for the maximum number of length-\(t\) action words sharing a single-edge endpoint and the corresponding information-log requirement. For an ideal one-bit orientation report after each legal turn, exact decision-tree computations give an eight-action minimum for adaptive state diagnosis and ten actions for adaptive reset of the tracked edge. We also characterize a four-action feedback experiment rank via face-incidence counts and provide finite proof certificates for separating-word covering bounds. The work isolates distinct information and control obstructions in a reversible group action; it does not model human perception of cubie orientation, human memory, or full-cube solving. The originality of the model-specific graph identification and numerical optima remains subject to a targeted prior-art audit.

### Main theorems and proof authority

1. **Algebraic path-multiplicity theorem (strongest):** exact 24-state action-count adjacency `B=10I+CᵀC` and spectrum `{18¹,16²,14⁶,12²,10¹³}`. With the initial and final coordinate of only the tracked edge known and all literal HTM words allowed, maximal endpoint fiber
   `(18^t+2*16^t+6*14^t+2*12^t+13*10^t)/24`, all integer t≥0. Human-length incidence/spectral proof and independent physical finite oracle: YES. **Lean formalization of physical equivalence: OPEN.**
2. **Adaptive identification/control theorem:** on all24 possible source coordinates, optimal binary feedback identification needs **8 moves** and exact physical reset of that one edge to target coordinate0 needs **10**. Exhaustive complete Bellman + replayed decision trees, independent C++/Python/Node checks: YES. **Non-Bellman analytic lower bound / Lean: OPEN.**
3. **Four-action rank and support theorem:** exact formula in terms of F/B/other initial-position counts, 216 minimal strict-feedback supports, 1331 total winning supports, 124 value types. Geometric upper proof plus compact 36-word finite lower certificate: YES. **Proof without the short finite catalogue: OPEN.**
4. **Minimum separating-experiment dictionary:** concrete 34-word upper and exact dual/cut lower25 for all1192 admissible source bases. The exact `M*∈[25,34]` is **OPEN**. Put this in a secondary independent combinatorics paper or technical appendix until the exact minimum or new generally transferable theorem is established.
5. **P12 short graph core:** a 24-target inclusion-minimal obstruction in the 80 near-tight candidates under the **HYPOTHETICAL 24-word only** dual mass restriction. A 17-profile finite completeness certificate, ten-edge missing-pair graph, four-edge matching, and four-vertex cover give a compact mixed human/finite proof. This is NOT the same as a globally valid reduction for25 full words.

### Four manuscript failure gates before release

- **Novelty gate:** compare original published material for cube-edge action automata, algebraic graph spectra, distinguishing/homing sequences, and constrained set-cover; do not call generic controlled sensing or finite state belief sufficiency novel.
- **Model gate:** repeat exact move-map derivation from real 18 face tokens, eliminate dependence on source ordering by independent isomorphism and action-tree replay.
- **Proof gate:** each human proof step, executable finite certificate, and Lean kernel formalization must have a separate authority label. GitHub CI registration != successful kernel pass; no `sorry`/extra axioms, and no one-model computer test called an unrestricted theorem.
- **Claim gate:** one tracked edge != solved 3×3; intrinsic flip-bit != visible human sensor; literal action word multiplicity != minimum human memory. Publication venues and title must reflect mathematical automata model.

## Why a sequel can start without forcibly closing 0.16

[NOMOS-0.872](https://app.notion.com/p/3f4ef561cf9281f5bf45d72d2274f4a6) explicitly allows an older version to remain open while the following version expands the evolving scientific question. Research OS's September mainline doctrine promotes an internal sub-question when it becomes the scientific center, but October's residual-descent rule warns that a long chain of solved local leftovers may lose the original explanatory scale.

Thus version 0.16 is the exact Rubik one-edge case study and paper-preparation owner. A prospective CUBE-REV 0.17 should ask a **strictly larger question**, not merely search another finite certificate for the same 80 columns: which algebraic invariants of a reversible group action and observation partition bound identification, reset, and loss of historical action identity, uniformly across different state spaces and sensor frames? Formalized proofs and transferable lower-bound structures are central. The original cognitive question remains a future falsifiable *human* project, never smuggled into present mathematical authority.

**Proposed 0.17 formal title for opening after project inheritance check:**
*CUBE-REV 0.17 — Reversible Observation Automata, Reconstruction Complexity & Proof-Carrying Information Bounds.*

This is a proposal, not evidence of an opened canonical page. No automatic closure of 0.16 is justified.
