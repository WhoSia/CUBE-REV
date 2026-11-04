# CUBE-REV 0.28 — Publication decision, primary-result hierarchy and hostile-review gate

**2026-11-04. Status: research case-study manuscript with a newly closed B5 220-support physical dependency; not submission-ready.** This gate separates a theorem whose **proof is demonstrable** from a theorem whose **novelty and generality are defensible**. Do not confuse a read-only CI PASS with external peer review.

## 1. One coherent scientific question

For legal, fixed-centre, 3×3 Rubik states of bounded symmetric 18-HTM word distance from solved, which **specific originally labelled cubies**, observed in their full physical position and orientation, must be measured to guarantee exact state identification? How does the optimal sensor-placement family change under one-sensor swaps, sensor failures, and increasing radius?

This is a fixed observation problem on a concrete finite physical group action. Its outputs are NOT distances to graph landmarks, NOT a group automorphism action's global determining set, NOT orientation bits only, and NOT an adaptive input-output sequence. The radius restriction is a physical assumption, not a mathematical synonym for a general automaton's state count.

## 2. Results sorted by strength and source independence

| Claim | Scientific status on 2026-11-04 | Independent evidence | Publication role |
| --- | --- | --- | --- |
| `pi_S|B_r` injective iff `H_S ∩ B_(2r)={1}` | Elementary and rigorous for symmetric generators with consistent left action | Algebraic proof | Basic reduction, NOT claimed novelty |
| 3×3 original-cubie stabilizer exact orders and support spectrum | Finite derivation from legal parity and twist/flip constraints | Closed form and tests | Explanatory lemma, likely known algebra |
| `b6=16` and exactly 156 optimal sixteen-cubie layouts | Computationally certified relative to original physical source/archive | Historical negative witnesses + B5 lower bound + 41-target B6 MITM; positive lower-bound algorithm separate but same source physical transitions | Primary case-specific result, only with proof-source declaration |
| 156-layout one-cubie exchange graph has 336 edges and 25 components (`96 + 12×4 + 12×1`) | Precise combinatorial deduction conditional on the positive B6 layout classification | Pure Python geometric counts, independently written JavaScript and 24×3 orbit argument | Strongly communicable **physical case-study geometry** |
| Exact B6 one-erasure minimum `b6^(1)=19`, exactly twelve minimum designs | Lower bound now supported by fresh B5 physical 220/220 replay plus 12HTM two-corner witnesses; upper still uses original B6-positive 156 layouts | Complete 13 real B5 two-sided word pairs found in independent C++ BFS on all 621649 B5 states, separately replayed by Python 48-sticker under 24 rotations and cross-language receipt bridge | Primary robustness case-study result |
| B7 `b7^(1)=20`; exactly one robust 20-tag layout | Original physical 13HTM 6+7 two-edge midpoint witnesses and symmetry, plus B6 corner supports | Standalone 48-sticker midpoint audit, CI | Sharp finite-radius change |
| General exchange failure of resolving/determining sets | **Old prior art**: Boutin 2008/2009 and other group-base literature | Original Boutin PDF inspected | Must NOT be sold as novelty |
| Fault tolerance of graph metric dimension | **Old prior art**: Hernando et al. 2008, Knor et al. 2025, Geneson & Tsai 2026 | Primary PDFs/publisher sources | Explicitly distinguish physical observation output |

The phrase **“independent B5 physical 220 support certificate”** means physical word-pair reproduction independent of the historic 54-facelet B5 source code. It does NOT mean that independent B6 positive 41-goal HTM lower bounds have been completed with a new physical transition model.

## 3. Newly closed, precisely reproducible B5 lemma

Let `E` be any of the `C(12,3)=220` subsets of three originally tagged edge cubies. The finite physically executed lemma asserts that there exist two legal states `x_E,y_E∈B5`, each with an actual symmetric 18-HTM word of length at most five, whose complete original-tag difference support is EXACTLY `E`. Neither abstract set coverage nor a calculated orbit partition alone is accepted as physical evidence.

The independent search source `scripts/cuberev-observation/b5_independent_48sticker_seed_search.cpp` generated exactly 621649 distinct B5 physical states and found 13 original word pairs, one per edge triple rotation orbit. The pinned source `data/0.28/B5_13_ORBIT_INDEPENDENT_WORD_PAIR_WITNESSES_20261104.json` preserves all 13 pairs. `verify_b5_three_edge_physical_manifest.py` physically replays both endpoints and every rigidly rotated word in a separate Python 48-sticker engine; `verify_b5_independent_cpp_receipt.py` also binds C++ runtime stdout to the pinned bytes, independent source tags and the actual physical words. Read-only CI PASS: [B5 complete physical run](https://github.com/WhoSia/CUBE-REV/actions/runs/41756861110); its follow-up B6 one-erasure tests: [run 41756953533](https://github.com/WhoSia/CUBE-REV/actions/runs/41756953533).

**Critical negative-control history**: the first C++ implementation used inconsistent named-face quarter-turn signs. Both programs could still agree on the **621649-state number**, but the Python witness replayer correctly rejected the purported pairs. This is precisely why current CI checks original **words and original cubie factors**, not just ball sizes. Corrected C++ semantics are U-,R-,F-,D+,L+,B+ relative to the prescribed positive coordinate-axis rotation. Both sides of all 13 physical word-pairs were freshly generated after fixing the discrepancy.

## 4. Prior art: what is already known

- **Bailey & Cameron (2011), Base size, metric dimension and other invariants of groups and graphs**, DOI 10.1112/blms/bdq096: relates classical group bases, determining sets and graph metric dimension. No novelty claim for the general notion of a determining base.
- **Boutin (2008 preprint, later journal publication), Determining Sets, Resolving Sets, and the Exchange Property**, https://arxiv.org/abs/0808.1427: explicit failure of exchange in existing graph families, positive tree results, discussion of matroid analogies. This defeats any claim that we were first to observe nonmatroidality of identifying sensor sets.
- **Hernando, Mora, Slater, Wood (2008), Fault-Tolerant Metric Dimension of Graphs**, direct author original in 10_PAPERS: already defines deletion of any one landmark; its landmark outputs are **graph distances**, unlike cubie position+orientation.
- **Knor, Sedlar, Škrekovski (2025 journal; 2024 preprint), Fault Tolerance of Metric Basis Can Be Expensive**, DOI 10.1007/s00009-025-02894-3: large fault-tolerance cost is known in generic graph metrics. Avoid generic “surprising sensor failure cost” novelty claims.
- **Geneson & Tsai (2026 published, 2025 preprint), Fault tolerance for metric dimension and its variants**, DOI 10.1016/j.dam.2026.01.009: new upper bounds for fault-tolerant graph metric dimension; update the reference if citing the published rather than arXiv version.
- **Rokicki, Kociemba, Davidson, Dethridge**, the cube group diameter twenty, DOI 10.1137/120867366: exact cube HTM search and symmetry reduction are established technology, not novel algorithms merely because we use them.
- **Harary & Melter (1976), Slater (1975)**: historical primary originals not yet physically owned; user emailed the publishers. Secondary references can support bibliographic history, but do NOT fabricate quotations from originals.

Other relevant source families in Research OS: Laison et al. on base-size sets under different faithful group actions, Seress on permutation group algorithms, multiple graph metric fault-tolerance variants and automata distinguishing sequences. A broad systematic external search of all possible cube-sensing papers is **not yet finished**; no formal global novelty certification exists.

## 5. Three paper directions, and the decision

**A. Generic group-action radius-base theorem:** weak novelty on its own. The radius-doubling characterization is elementary and group-action stabilizers are classical. Do NOT headline an old general lemma.

**B. The finite exact Rubik observation classification:** currently the strongest core. It joins physically defined full-position/orientation sensors, complete radius-specific thresholds and 156 minimum B6 placements, 25 exchange components, and exact one-erasure radius-six/radius-seven transitions. Frame as a carefully verified **computational/discrete mathematics case study**, not a universal new group-theoretic framework.

**C. Adaptive FSM experiment-selection theory:** legitimate but distinct older CUBE-REV scope; combining it here would blur models and make the paper harder to audit. Leave it for another manuscript when its own formal experiment model, optima and prior-art review are ready.

**Decision: pursue B as ONE tightly scoped paper, NOT three inflated papers.** Short preliminary study of A as notation only; C out of scope. Preferred provisional title: *Finite-Radius Identification of the Rubik Group by Oriented Cubie Sensors: Exact Bases, Exchange Components and Erasure Robustness.*

## 6. Hard hostile-review questions

1. **What is measured exactly?** A persistent originally tagged corner/edge's full current position and orientation. Any change to unlabelled observation or single-bit orientation invalidates direct transfer of these thresholds.
2. **Do the 41 B6 HTM goal classes have a truly separate physical verification?** No: the completed C++ MITM is algorithmically independent of an older projection census but uses the original physical 54-facelet move source. A second model is still the highest remaining technical proof gate.
3. **Does “156 optimal B6” follow from the new B5 220-support lemma alone?** No. It also relies on B6 positive 41-goal evidence AND completeness of negative obstruction witnesses, including 19 physical B6 negative-orbit seeds and historical B5 mask coverage.
4. **Why 25 exchange components, not simply a known matroid failure?** The actual cube-dependent incidence rule has `W5 ⊔ C4 ⊔ K2 ⊔ K1` on each fixed missing-corner pair, `24×3=72` cross-core swaps, producing exact topological components. General exchange failure is old; the explicit finite Rubik geometry is the candidate contribution.
5. **Why 19 robust sensors?** Pure two-corner physical B6 witness orbits force all 8 corners; all 220 separately replayed B5 three-edge support witnesses force ≥11 edges. Ten orbit-incidence certificates within the 156 B6-positive layouts show all 12 possible 19-tag omissions of a single edge survive any one loss.
6. **Are the same 13 C++ witnesses automatically correct because a program printed FOUND?** No. CI physically replays both endpoint move words in a different Python engine, checks rotations and cross-language output/pinned manifest equality. Earlier sign-error failures demonstrate that safeguards are active.
7. **Are the observed thresholds and exact layout counts novel?** They are case-specific candidate results whose priority must still be assessed against obscure historical Rubik reconstruction and state inference literature. No blanket “first” claim.
8. **Is the proposed paper currently ready for submission?** No. Missing second physical B6 transition model, formalized evidence package, focused domain novelty search, carefully proofed mathematics, and independent human manuscript review.

## 7. Stop/go gate for a substantive paper

**GO for continued full-paper drafting and figure preparation** because exact finite computations have matching physical receipts, a genuine new independent B5 certificate, and a coherent physical model. **HOLD external submission** until the B6 physical-model-independent 41-target certificate and novelty review are sufficiently strong. If peer review reveals prior exact B6/erasure results, adjust to a reproducibility/independent-certification contribution rather than assert priority.

Priority next: (i) second 48-sticker independent B6 stabilizer distance engine or formal PDB for the 41 target set; (ii) short geometric explanation of four-case 13 survivor criterion; (iii) graph picture of 96+12×4+12 isolated exchange components; (iv) full bibliography, figures and careful error analysis.

## 8. Evidence custody rules

Canonical branch `research/current`; GitHub commits with human author attribution only; Actions read-only without bot-authored history changes. Google Drive archives source bytes and external PDFs, GitHub source and test code is execution custody, Notion stores the research reasoning, changes and rejected hypotheses. All software/workflow counts must refer to observed runs, never a queued run. No deletion of unverified archive branches, no rewriting old C3X/NOMOS/RITHM files. Reconcile every added Git tracked file into the explicit P7 active-only path manifest and check remote P7 CI success.
