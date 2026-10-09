# CUBE-REV 0.17 / Internal P1 — Prior literature, novelty, and Drive custody audit

**Audit date:** 2026-10-09. This is a targeted title/abstract/source comparison, NOT a complete systematic review or assertion of scientific priority. Public article/DOI links were checked separately; Drive existence is based on connected Drive title matches and selected source text, not an assertion that every PDF or archived version was enumerated. No file was downloaded or moved without authorization.

## The nearest scientific precedents

| Source | Verified external identifier | Existing Drive | What it establishes / relation to CUBE-REV |
|---|---|---|---|
| Lee & Yannakakis (1994), *Testing Finite-State Machines: State Identification and Verification* | https://doi.org/10.1109/12.272431 | YES — title-matched PDF in Drive | Foundational preset vs adaptive distinguishing experiment and existence/complexity results; CUBE-REV must NOT claim invention of adaptive state diagnosis |
| Rivest & Schapire (1993), *Inference of Finite Automata Using Homing Sequences* | https://doi.org/10.1006/inco.1993.1021 | YES — title-matched PDF | Known learning/identification even without physical reset; separates homing and reset |
| Türker, Ünlüyurt & Yenigün (2016), *Effective Algorithms for Constructing Minimum Cost Adaptive Distinguishing Sequences* | https://www.sciencedirect.com/science/article/pii/S0950584916300192 | YES — title-matched PDF | Minimum-cost ADS algorithms already studied; four-turn feedback advantage not a novel GENERIC concept |
| Lukac, Kameyama, Perkowski & Kerntopf (2019), *Using Homing, Synchronizing and Distinguishing Input Sequences for the Analysis of Reversible Finite State Machines* | https://doi.org/10.2298/FUEE1903417L | NO title-matched file in connected Drive searches | DIRECT reversible-FSM precedent, highest missing-paper reading priority; compare especially converging vs nonconverging RFSM |
| Hierons et al. (2008), *Using Adaptive Distinguishing Sequences in Checking Sequence Constructions* | https://doi.org/10.1145/1363686.1363850 | NO title-matched file found | Direct evidence adaptive vs preset can differ widely, so no general novelty claim for this phenomenon |
| Radionova & Okhotin (2026), *Decision Problems for Reversible and Permutation Automata* | https://doi.org/10.1016/j.ic.2026.105488 | NO title-matched file found | Very recent complexity results for reversible/permutation language decision problems; relevant but their emptiness/equivalence questions differ from observed-feedback identification |
| Demaine, Eisenstat & Rudoy (2018), *Solving the Rubik's Cube Optimally Is NP-complete* | https://doi.org/10.4230/LIPIcs.STACS.2018.24 | YES — title-matched PDF | Variable-size n×n×n optimal entire-cube solving, NOT complexity of a fixed 24-state tracked-edge observation system |
| McKay (1998), *Isomorph-Free Exhaustive Generation* | original graph-enumeration methodology (title verified in Drive) | YES — title-matched PDF | Prior art for canonical augmentation and exact symmetry quotient; CUBE-REV should not claim novelty of general isomorph-free generation |
| Saxena (2004), *On the Set-Covering Polytope: Facets with Coefficients 0,1,2,3* | original title-matched preprint in Drive | YES | Cutting-plane polyhedral literature; 60-positive-dual rational cover and 25-specific defects are applications, not first invention of integer set cover |
| Waller (1976), *Double Covers of Graphs* | https://doi.org/10.1017/S0004972700025053 | NO title-matched file found | Background on graph double covers and octahedral universality; does NOT independently establish that the exact 18-HTM edge-action multigraph was already derived |
| Lammich (2024), *Fast and Verified UNSAT Certificate Checking* | https://doi.org/10.1007/978-3-031-63498-7_26 | NO title-matched file found | Formal LRAT certificate checking; relevant to replacing 24-million-case executable checks with independently checked proof traces |

## Lean/LRAT: **DO NOT MERGE TWO SEPARATE SZEIDER PAPERS**

Drive DOES contain **Stefan Szeider (2026), _Streaming LRAT Certificates into Lean Theorems_**, independently fetched as readable text, whose abstract describes stream-mode and resumable file-mode checked import, chunking and large-certificate scaling. This is a separate title and technical focus from **Szeider (2026), _LRAT-Catcher: Importing SAT Solver Certificates into Lean4 by Reflection_**, at https://arxiv.org/abs/2607.00815 and open implementation https://github.com/leansolving/lrat-catcher . Connected Drive title search did NOT locate a PDF specifically titled _LRAT-Catcher_. Distinguish the papers bibliographically even if same project/authorship; an existing streaming preprint does NOT prove custody of the reflection manuscript.

The LRAT-Catcher implementation includes a way to import an actual LRAT certificate as a Lean proposition with a verified reflection checker and requires separately verified CNF-to-original-theorem encoding. It does NOT automatically solve the Rubik physical-action-to-incidence semantic bridge or validate an unproved '17 profiles complete' assertion.

## Relation to the current candidate manuscript

**Strongest potential distinct model-specific theorem:** exact identity of the 24-state tracked Rubik edge / 18 HTM action-count multigraph `B=10I+CᵀC`, the ordered face-pair double-cover representation, and all-length fiber multiplicity `(18^t+2·16^t+6·14^t+2·12^t+13·10^t)/24`. A targeted search for the precise eigenvalue multiset {18,16,14,12,10} and edge action/orientation found no obvious identical published result, but search absence is NOT proof of originality; retain NOVELTY_PENDING until manual bibliography/citation-chaining and complete original-theorem reading.

**Clearly NOT new in general:** adaptive distinguishing/homing experiments, state-observation congruence, reversible word injectivity, PSD return-maximality, set covering and integrality gaps, graph double covers, and finite LRAT certificate checking.

**Model-specific independently supported but computational:** eight-move tracked-edge diagnosis, ten-move tracked-edge target reset, exact four-action rank count profiles, 24-target near-tight inclusion-minimal graph obstruction, and finite M* interval 25≤M*≤34. Lean kernel success was NOT verified and cannot be inferred from registered CI source.

**Publication positioning:** theoretical computer science (automata, algorithmic experiment design, exact finite-state control) with discrete-mathematical graph/combinatorial theory. The present ideal intrinsic-edge-orientation sensor is NOT an observed human sense and no behavioral data justify an empirical cognitive-science paper. Rubik's Cube serves as a finite physical action-system benchmark, not a proof of general n×n×n complexity.

## Missing-PDF acquisition suggestions (provide public links; no download without user request)

Highest priority external landing pages:
1. Lukac et al. (2019) https://doiserbia.nb.rs/Article.aspx?id=0353-36701903417L
2. Szeider reflection paper (2026) https://arxiv.org/abs/2607.00815
3. Lammich (2024) https://link.springer.com/chapter/10.1007/978-3-031-63498-7_26
4. Hierons et al. (2008) https://doi.org/10.1145/1363686.1363850
5. Radionova & Okhotin (2026) https://doi.org/10.1016/j.ic.2026.105488
6. Waller (1976) https://doi.org/10.1017/S0004972700025053

These are known public article pages / DOI links, not fabricated PDF download URLs. Check access conditions; do not treat abstracts as equivalent to a paper's full proof or claim complete novelty clearance.
