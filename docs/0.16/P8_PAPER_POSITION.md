# CUBE-REV 0.16 — Manuscript position after the all-length spectral path theorem

**Status:** internal manuscript triage, NOT a publication claim, a separately named P-stage, or a formal 0.17. The current research version 0.16 remains OPEN.

## Manuscript candidate I — best near-term pure-mathematics direction

**Core problem:** A physical action is reversible, but observing only one tracked cubie's endpoint forgets exponentially many possible executed histories. Can the full history-multiplicity distribution be derived **symbolically for every action-word length**, rather than by finite enumeration?

**Proved distinctive mathematical content:** Identify 24 oriented edge coordinates with directed adjacent face pairs of the octahedral six-face graph. The exact 18-HTM literal action-word transition multigraph is `10I + CᵀC`, where C is unsigned incidence of the 12-vertex bipartite double cover of the octahedron graph. Spectrum `{18¹,16²,14⁶,12²,10¹³}`, positive-semidefinite path-power return-maximality and vertex-transitive closed return formula yield the max length-t source-to-endpoint word fiber:

`M_t=(18^t+2·16^t+6·14^t+2·12^t+13·10^t)/24`.

Thus the exact worst-case binary auxiliary history log length is `ceil(log₂M_t)` for known original and final state of the ONE tracked edge, and uniform-iid HTM endpoint forgetting has an explicit all-t spectral chi-squared rate. These are **exact derivations for all t**, unlike finite tables.

**Scientific novelty requirement:** The graph-spectral and automata methods are classical, and related line graph/bipartite double-cover spectra are studied (e.g., Zafari–Alikhani arXiv:2607.00069). Before submitting, confirm that this **particular oriented Rubik-edge action graph isomorphism and resulting sequence** were not published independently. If already known, frame as a reproducible exact application/teaching benchmark, not original spectral discovery.

**Potential supplementary theorem:** controlled state diagnosis8 and physical one-edge reset10 from a complete 24-state ideal binary observer, independently replayed with exact finite courts. Their general relation D≤R≤D+d is classical, but the precise 8/10 finite test has a certified machine-assisted proof.

## Manuscript candidate II — combinatorics of minimal action-test catalogues

The four-action identification-rank formula, 36→34 explicit universal word catalogues, 60-basis rational dual and exact improvement `25≤M*≤34` form a genuinely finite-covering research thread. The **minimum M*** is unknown; a bounded 33-word MILP returned `TIME_LIMIT`, which is not infeasibility. A paper would improve substantially if a verified exact optimum or a short geometric, human-checkable lower certificate replaces large solver dependence. The 36-word lower-construction basis and 216 minimal feedback-gain support antichain are reusable mathematical ingredients.

## Manuscript candidate III — history-vs-state-vs-reset conceptual theory

For a finite reversible action system with a known target, prove/generalize the feedback diagnosis and adaptive physical reset sandwich `D≤R≤D+d`, and combine endpoint fibers with the loss of exact action history. These general results are mostly existing automata/coding-information concepts. Treat as an expository framing/section rather than claiming discovery of finite-state controllability itself.

## Evidence boundaries

- A single tracked UR edge is NOT a full 3×3 solver or fully observed whole-cube endpoint.
- The intrinsic orientation bit per action is an ideal mathematical sensor, NOT a measured human percept.
- Memory capacity and subjective difficulty are NOT inferred from the 15-bit four-action lower bound.
- Distinct literal token words include undoing/canceling operations; changing legal action-word grammar changes multiplicities.
- Published predecessor: Nitinawarat–Atia–Veeravalli (2013), DOI 10.1109/TAC.2013.2261188, already established causal controlled-sensing advantages; Lukac et al. (2019), DOI 10.2298/FUEE1903417L, studied reversible finite-state distinguishing and homing; Zafari–Alikhani (2026), arXiv:2607.00069, study spectral line graph bipartite double-cover families (not identical to the present cube graph).

**Provenance:** full formal proofs in `docs/0.16/P8_SPECTRAL_HISTORY_THEOREM.md`; exact source `scripts/cuberev-016/spectral-history-court.mjs` and test; private hash-sealed mathematical ZIP in Library `/CUBE-REV/0.16/CUBE_REV_016_P8_SPECTRAL_PATH_INFORMATION_THEOREM_PRIVATE_20261009.zip`. Clean extraction and Python/SymPy exact checks passed. GitHub Actions regression was registered but its external job status is not yet independently verified.
