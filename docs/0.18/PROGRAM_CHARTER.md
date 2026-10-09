# CUBE-REV 0.18 — Robust Reconstructibility, Noisy Observation Automata & Adversarial Information Bounds

**Official formal version: OPEN / SINGLE ACTIVE CUBE-REV MAINLINE, 2026-10-09.** [Canonical Notion](https://app.notion.com/p/3f4ef561cf9281ef9bb6ca82f8c80d06). Predecessor [0.17 CLOSED](https://app.notion.com/p/3f4ef561cf92811e8da1dde0478bfd1e); 0.16 CLOSED. P0/P1/P2 are internal research sections, NOT new version names or branches.

## Scientific source: the actual 3×3 Rubik's Cube

This is **CUBE** research. The baseline laboratory is the physically derived 18-HTM move alphabet, 24 position/flip coordinates of the tracked UR edge, and legal observation reports after each physical face action. Group actions, reversible finite automata, SAT, PB, information theory and coding theory are **instruments to explain the Cube**, not reasons to detach the project into an unrelated automata lab.

Theoretical generalization must supply an actual translation into the frozen Rubik's Cube transition semantics, an explicit place where it fails, and a path to 3×3 complete-state sensing or empirical human methods without conflating these. In particular, a 24-state edge automaton is not a complete cube solver or a measured human visual channel.

## Core scientific question

Given a legal Rubik's Cube action history, sensor observations that may be missing/noisy/adversarial, and a specified target (state/edge/history or physical reset), when is the true source or past action history reconstructible? What are the minimal observations/actions needed to guarantee reconstruction under the stated corruption model?

Noise definitions must distinguish stochastic independent BSC epsilon, adversarial bounded t flips, erasures, action execution errors, unknown action words and memory-loss of history. Any result states assumptions about feedback control, initial prior, sensory reads and cost units.

## Exact source-constrained Mstar court — equal priority with robustness

For all 1,192 original admissible source subsets in the frozen 12 flip-zero slot model, an experiment is one 4-token literal legal 18-HTM sequence; 4 post-action intrinsic flip reports produce a partition. **Mstar** is the minimum number of such fixed experiments that collectively separate all 1,192 source subsets (different subset may choose a different experiment). It is NOT minimal physical cube solve length or one common universal diagnostic word.

**UPDATED SOURCE AUTHORITY 2026-10-10:** The *physical* original 1192-basis bound **Mstar≥30** has independent DRUP checking from the full 1323-column k29 CNF. **The old P6 34-word upper-bound claim FAILED actual sticker-derived Rubik physical replay** ([run 37947421965](https://github.com/WhoSia/CUBE-REV/actions/runs/37947421965)); its separate hand-coded edge-ring verifier is insufficient as physical semantics. Hence Mstar≤34 is RETRACTED and the earlier 25..34 or 30..34 two-sided intervals are not active. A [37-word repaired HTM candidate](P0_REPAIRED_37_WORD_PHYSICAL_WITNESS.json) has been committed for independent CI re-verification; do NOT claim a certified 37 upper until that run passes. The exact optimum remains unresolved. Original 60 dual-positive basis weights came from the sealed P6 rational certificate and are newly exposed as a math-only numeric court: [P0 weights](P0_60_POSITIVE_DUAL_WEIGHTS.json). They have weight sum 476 and per-word maximum20; the original P10 50×116 mathematical subcore remains independently checkable.

The [physical Node exporter](../../scripts/cuberev-018/export-mstar-physical.mjs) independently reconstructs all 104,976 four-turn words and 1,913 distinct observer partitions, all 1,192 source bases, the 1,477 unique coverage masks and 1,323 inclusion-maximal candidate masks, with one actual HTM witness per mask. No invalid 24-word-only near-tight restriction is used for k25. The frozen positive dual gives 596 maximal masks with mass>0 (162 mass20,6 mass16,12 mass12,76 mass8,340 mass4); 727 mass0 masks remain in the unrestricted model. Candidate dominance is universally valid, but the removal of mass0 masks requires the rigorously proved special k25 lemma.

## SAT proof and adversarial regression gates

- Strengthened [k25 PB-SAT court](../../scripts/cuberev-018/solve-mstar25-pb.py) includes all1192 coverage clauses, exact k25, heavy categories and the total defect bound. This is a **sound necessary-condition reduct** conditional on prior 0.17 P2 dual/14-cover exact certificate. It can exclude k25 ONLY if externally checked and the reduct soundness is independently audited. It MUST NOT certify k26 and higher.
- **Unrestricted original court** [solver](../../scripts/cuberev-018/solve-mstar-unrestricted.py) uses ALL 1,323 maximal candidates, ALL original 1,192 coverage clauses and ONLY the at-most-k cardinality constraint. A verified UNSAT proof here is a stronger, reduction-independent lower-bound certificate. The separate dual60-only k25 SAT run is a positive consistency control.
- In either route, a valid SAT witness must be replayed by the independent [24-edge physical move oracle](../../scripts/cuberev-018/verify-sat-witness-physical.mjs) against all 1,192 bases. Any UNSAT must produce a complete CNF + DRUP trace, with a separately pinned DRAT checker reporting VERIFIED on exactly those bytes. Solvers running out of budget, producing unverified UNSAT status or outputting no witness leave the interval unchanged.
- Never equate an abstract CNF UNSAT proof with a *Lean kernel proof of the physical source-to-CNF bridge*: proof-carried combinatorics and semantic model validation are separate evidence statuses.
- [Read-only PB CI](../../.github/workflows/cuberev-018-mstar25-proof.yml) and [unrestricted SAT/DRUP CI](../../.github/workflows/cuberev-018-mstar-unrestricted.yml) use contents: read, no bot-authored commits; all generated artifacts stay as job artifacts, NOT large repository data files.

## Version-flow and publication integrity

0.17 is CLOSED as a stage, but unfinished exact Mstar, non-enumerative 17-profile derivation, physical HTM Lean semantics and theory-CS publication claims are **inherited into 0.18**, not retroactively marked PASS. Do not run simultaneous officially OPEN version tracks. GitHub single current research branch; stable main untouched. No private human behavior rows publicly pushed; mathematical-only source can be reviewed openly. Cite Lee–Yannakakis, Rivest–Schapire, reversible FSM and LRAT proof literature as antecedents, and give credit rather than overclaiming elementary group-action theorems.

**Current gate at opening: 0.18 OPEN / Mstar exact UNKNOWN / robust noisy experiment court NOT YET RESEALED / physical Lean semantic bridge OPEN.**
