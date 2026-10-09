# CUBE-REV 0.20 — PREPARATORY CHARTER ONLY (NOT OPENED)

## Formal-name proposal — awaiting 0.19 closure

**CUBE-REV 0.20 — Laws of Physically Constrained Identification: Restricted Perfect Hash Families, Action-Transported Observation Codes & Certified Covering Complexity**

**Authority status: PROPOSED / NOT ACTIVATED.** This document exists to avoid losing 0.19's conceptual findings. It must not supersede active 0.19, cannot claim an exact physical \(M^*(5)\) yet, and must not promote a new version before the original 1192-source k7 SAT or k7 UNSAT proof is independently checked.

## The primitive research question

> For a reversible physical transducer with a bounded sensor and an admissible family of candidate initial states, which structural invariants determine when identification becomes possible, how the minimum size of a nonadaptive experiment dictionary changes with observation length, and which additional information access rights reduce that cost?

General finite ontology (a formal **proposal**, not yet a theorem):

- Finite physical transition system \(T=(Q,\Sigma,\delta,o)\) with actual state set Q, executable action alphabet \(\Sigma\), deterministic transition \(\delta\), sensor output o and **initial hypotheses** \(S\subseteq Q\).
- Source-family contract \(\mathcal R\subseteq 2^S\), potentially nonuniform and with constraints inherited from geometry.
- Fixed preset word w of length L gives an actual **ordered** physical output trace \(h_w:S\to Y^L\) and corresponding observation partition \(\pi_w\).
- Physically constrained restricted perfect-hash covering number \(M_T(\mathcal R,L)=\min\{|D|:D\subseteq\Sigma^L,\forall A\in\mathcal R,\exists w\in D\text{ s.t. }h_w|_A\text{ injective}\}\), infinite if impossible. A reset or no-reset policy is part of the contract.
- Other incomparable costs (worst preset universal length, adaptive minimax policy depth, sensor memory, total action count, expected action count) must never be conflated with dictionary cardinality.

## Existing 0.19 evidence to carry as **frozen baseline**, not universal conclusions

- Current full physical fixed-source horizon profile (local finite computer-assisted evidence): no dictionary for L<=3, \(M^*(4)=34\) externally checked, \(M^*(6)=4\), \(M^*(7)=3\), \(M^*(8)=2\), \(M^*(L>=9)=1\); original full \(M^*(5)\) **still exactly one of 7 or 8**.
- Restricting the 1192 original source requests to its admitted 480 five-source subfamily at L5 gives exact **seven** experiment words by P12 locally checked 445 integer weight certificates and finite exhaustion. This is a proper restricted-family theorem, not full original M*=7.
- Standard fractional covering LP for all original five-HTM sources is exactly \(16/3\), and for original five-element sources alone exactly \(185/39\). Difference \(23/39\), *not* fractional turns. The ordinary fractional bound is exhausted and integer combinatorial structure is essential.
- L5 original physical all-k quotient is 544x2887; for original k7 the source-validated rank gate gives 544x2403, 16 incidence automorphisms give 69 high-rank first-word orbit representatives, and original dual weighted-mass yields 102979 valid pair exclusions on the rank-eligible columns.
- 0.19 P13 proved independently that any seven-word R5 dictionary requires at least two words with rank>=6, by 1144 source-volume cases and 32 source-original exact integer dual exceptions. Empirical R7/rank7 class proof branches may be added only after all original source and group-closure checks pass.
- Fixed universal identification first horizon9; adaptive full 12-state minimax horizon7 on the same *ideal* orientation-bit sensor. No transfer to human perception or full cube-state recovery is asserted.

## Proposed mathematically substantive 0.20 work packages

### A. Representation theorem for transported physical observation cuts

Write each legal move on tracked states as \((p,b)\mapsto(\sigma_a(p),b\oplus f_a(p))\). Derive exact conditions on the transported support sets \((\sigma_{a_1}\cdots\sigma_{a_{t-1}})^{-1}(\operatorname{supp}f_{a_t})\) that force a first identifiable horizon. The concrete 0.19 four-slot support and Hamming-mass proof are worked examples, not an unrestricted theorem for every transducer.

### B. Restricted perfect-hash-family bounds specific to realized transducers

Formalize \(M_T(\mathcal R,L)\) with a source-specific collision hypergraph and derive a necessary/sufficient hyperedge-transversal condition for a k-word dictionary. Characterize when source-family extension \(\mathcal R\subset\mathcal R'\) strictly raises the **integer** minimum, despite identical alphabet and number of observations. Compare with existing perfect/separating hash families, covering arrays and separating systems; explicitly state prior art versus new physical constraints.

### C. A proof-carrying hierarchy for integer covering obstructions

Move beyond the exhausted ordinary row-weight LP optimum using validity-preserving conditional duals, high-order collision edge unions, symmetry with explicit witness permutations, and pseudo-Boolean integer cutting-plane certificates. Formalize the exact reduction lineage: physical word -> observation partition -> original source coverage -> support implication -> dominance quotient -> group orbit -> k-specific cuts -> external proof. Study VeriPB/CakePB for proof logging rather than overinterpret MIP timeouts.

### D. Feedback versus preset separation as an automata result

Specify admissible sensing and control access rights. Compare preset words of finite length, resettable nonadaptive dictionaries, observation-dependent adaptive policies and memory-limited controllers with identical physical state and source contracts. Establish theorem hypotheses before considering attention, memory or human cognitive claims.

### E. External validity and falsification

Pre-register a *separate* physical sensor/sticker validation and controlled orientation convention counter-tests. FTC? Avoid transferring partial edge orientation to the full cube's 43 quintillion state ontology. Optional FMC, WCA, video transcription and human timing data remain **auxiliary**. Do not treat behavioral recordings as proof of a deterministic cube-state combinatorial theorem.

## Gate to activate 0.20

1. Obtain a physically replayed **seven-word full-original** L5 dictionary (thus M*(5)=7), OR source-linked and independently DRUP/VeriPB checked full-original **k<=7 UNSAT** plus real eight-word upper (thus M*(5)=8).
2. Preserve the original 1192-source SHA256, complete P12 restricted-seven proof, P13 final source-court CNF/proof/witness, independent verifier logs, and exact version-specific README/Notion/Drive receipts.
3. Explicitly freeze what 0.19 proved (scope, quantifiers, L length convention, source-family membership, action alphabet, noise/reset/adaptivity). A method that only times out or has a candidate unsat numerical MIP is insufficient.
4. Then and only then activate the formal 0.20 name, specify falsifiable P0 targets and a self-contained reader's theorem/limitations outline.

## Literature to read before novelty claims

- Bogaerts, Gocht, McCreesh & Nordström, *Certified Dominance and Symmetry Breaking for Combinatorial Optimisation* (JAIR 2023), https://doi.org/10.1613/jair.1.14296
- Koops et al., *Practically Feasible Proof Logging for Pseudo-Boolean Optimization* (CP 2025), https://doi.org/10.4230/LIPIcs.CP.2025.21
- Shangguan & Ge, *Separating Hash Families: A Johnson-type bound and New Constructions* (SIAM J. Discrete Math. 2016), https://doi.org/10.1137/15M103827X
- Procacci & Sanchis, *Perfect and separating hash families: new bounds via the algorithmic cluster expansion local lemma* (2017), https://doi.org/10.4171/AIHPD/51

**Do not cite this proposed charter as established 0.20 results.** Its purpose is to keep mathematics and evidence boundaries ready for the next formal generation.
