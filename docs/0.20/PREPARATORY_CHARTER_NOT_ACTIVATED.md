# CUBE-REV 0.20 — Preparatory Charter (Proposal, Not Yet Activated)

## Formal name — proposed

**CUBE-REV 0.20 — Structural Laws of Physical Identifiability: Action-Transported Observation Codes, Restricted Perfect Hash Families & Proof-Carrying Covering Complexity**

**Status: PROPOSED / PREPARED / NOT ACTIVATED.** Version 0.19 now has a complete **local** finite-proof horizon profile for its *frozen physical UR-edge source family*, including the P13 local result \(M^*(5)=8\). The exact P13 theorem remains subject to independently checked external CI/other proof receipts. This draft **does not** count as opening 0.20 or as establishing any of its proposed general statements beyond those explicitly marked as elementary derived lemmas.

## Primitive question

**When does the geometry of physically executable actions, rather than the raw sensor alphabet size, determine the cost of identifying an initially ambiguous physical state?**

Distinguish four costs that are frequently but wrongly conflated: (i) size of a resettable **fixed nonadaptive experiment dictionary**; (ii) length of one preset experiment that identifies every hypothesis; (iii) minimax number of actions in an **adaptive feedback** strategy; (iv) actual physical action, memory, observation, measurement-noise and human cognitive costs.

## Finite object and exact notation

Let a *physical observation transducer* be \(\mathsf T=(Q,\Sigma,\delta,o,S)\), where Q is finite, \(\Sigma\) legal executable actions, \(\delta:Q\times\Sigma\to Q\) a deterministic transition, \(o:Q\to Y\) a physical sensor, and \(S\subseteq Q\) the admissible initial states. Fixed word \(w\in\Sigma^L\) determines \(h_w:S\to Y^L\). Given a restricted, explicitly specified source family \(\mathcal R\subseteq2^S\), define

\[
M_{\mathsf T}(\mathcal R,L)=\min\{ |\mathcal D| : \mathcal D\subseteq\Sigma^L,\ \forall A\in\mathcal R\ \exists w\in\mathcal D\text{ with }h_w|_A\text{ injective}\}.
\]

If no dictionary works, define \(M=\infty\). Dictionary cost is one per complete experimental word, not number of turns spent executing a selected word. The source set and reset/feedback/measurement convention are always part of the theorem statement.

## Frozen CUBE-REV 0.19 reference experiment (not a universal theory)

The exact **local computer-assisted finite** fixed-oracle horizon profile is: \(M^*(0\ldots3)=\infty,\ M^*(4)=34,\ M^*(5)=8,\ M^*(6)=4,\ M^*(7)=3,\ M^*(8)=2,\ M^*(L\ge9)=1\). The L4 value has independent external DRUP proof; L5 closure has separate integer certificates, exhaustive physical branches and original physical eight-word witness, while new independent external CI completion remains to be checked. The physical oracle tracks only one edge orientation from 12 initial slots, not 3×3 cube-state identification.

The original 480 permitted five-element sources at L5 have exact local integer optimum **7**, but the full original 1192 permitted sources have exact local integer optimum **8**. The actual *integer source-extension penalty* is **1 additional dictionary word**. The corresponding ordinary fractional optimum difference is **23/39** (full LP 16/3, restricted-five LP 185/39). Thus the full original L5 integer integrality ratio is **3/2**, and the original restricted-five L5 ratio is **273/185**. These are fixed-instance parameters requiring structural explanation; not general bounds or novelty claims.

## Fundamental proof targets

### T0 — The physical observation-cut weight bound (derive before experiments)

For finite hypothesis set \(S\) of size n and action-induced incremental binary sensor observations whose informative cuts have (after transporting through preceding physical permutations) sizes \(s_1,\ldots,s_q\), all hypotheses generate q-bit increment codes with total Hamming weight exactly \(\sum_j s_j\). If the n codes are pairwise distinct, the total must be at least \(W(n,q)\), the sum of the Hamming weights of the n lightest distinct q-bit strings, filling binomial layers \(\binom qr\) from small r upward. Hence the elementary **necessary** condition

\[
\sum_{j=1}^{q}s_j\ge W(n,q).
\]

In the tracked-edge instance, each flip-capable physical action yields an exactly four-slot cut, so \(q=4\) gives total 16 while \(W(12,4)=19\): full identification is impossible even with sixteen possible 4-bit signatures. This elementary inequality is a clean starting point, **not** a sufficient condition for physical identifiability and not automatically a novel mathematical result. **0.20's genuine challenge** is to strengthen it with *joint reachability/conjugacy constraints* to account for the specific nine-turn preset threshold.

### T1 — Collision-hypergraph and source-extension laws

For each realized word w, let \(B(w)\) be the graph of indistinguishable pairs of initial hypotheses. A fixed dictionary \(D\) fails exactly when there exists admitted \(A\in\mathcal R\) containing some edge of \(B(w)\) for **every** w in D. Equivalently, there exist selected collision edges \(e_w\in B(w)\) whose union lies inside an A in \(\mathcal R\). Characterize which source extensions \(\mathcal R\subsetneq\mathcal R'\) necessarily increase the **integer** minimum, and when fractional and integer extension costs diverge. The frozen L5 example with integer increment 1 and fractional increment 23/39 is a certified test instance, not a universal theorem.

### T2 — Proof-carrying quotient and symmetry theorem

Specify sufficient conditions under which (a) original-source support implication, (b) source-specific collision inclusion dominance, (c) source-incidence automorphisms, and (d) k-specific conditional integer dual cuts preserve satisfiability/UNSAT of the original experiment-selection problem. Crucial failure mode: **cross-rank dominance cannot be reused unchanged when a case split restricts the admissible ranks**. Deliver a small independent checker for each preservation step rather than relying on unverifiable long solver logs.

### T3 — Preset versus adaptive feedback and sensor access rights

Place the fixed-preset nine-action full-12-hypothesis threshold and locally exact adaptive minimax seven-action policy into the same finite-state observability formalism. Prove any claimed policy separation under **identical initial-state and sensor conventions**, explicitly distinguishing the resettable dictionary size M from single-word identification depth. Introduce bounded memory or missing observation histories as an explicit, independently falsifiable model change, not as a claim about human attention.

### T4 — Cross-transducer falsification and literature novelty court

Choose at least one distinct reversible finite transducer or a controlled alternative cube observation convention, preregister what changes and what is invariant, and test which candidate structural bounds survive. Maintain a rival-baseline table covering classical perfect/separating hash families, covering designs/arrays, adaptive and preset automata distinguishing sequences, and certified symmetry/dominance proof systems. The objective is a genuine theorem with hypotheses and counterexamples, not a renamed finite enumeration.

## Proposed phase labels and falsifiable gates

- **0.20-P0 — Theorem Contract & Prior-Art Rival Audit.** Freeze the transducer/source/sensor/cost ontology and literature countermodels. Reject any new term if classical theory already gives the claimed statement.
- **0.20-P1 — Action-Transported Cut Geometry & Finite Code-Weight Bound.** Prove necessary conditions, construct sharp physical counterexamples where mere bit counts fail, test on at least two systems.
- **0.20-P2 — Restricted Perfect-Hash Source-Extension Certificates.** Characterize when source extension forces a dictionary-cost jump, and separate fractionally visible from purely integer obstructions.
- **0.20-P3 — Proof-Carrying Physical-Quotient and Integer Branch Certification.** Machine-check original physical transitions, dominance/symmetry reweighting and every case-specific source rank.
- **0.20-P4 — Feedback, Memory & Counterexample Ecology.** Derive and adversarially test accessibility hierarchies and boundaries to human inference.

At P4 closure, demand at least **one theorem beyond the frozen twelve-edge model** or an explicitly negative result that shows the generalization fails. A second enormous brute-force census by itself does not qualify.

## Research integrity and activation gate

1. Do not promote new 0.20 claims from the 0.19 source-family benchmark alone.
2. Freeze the P13 eight-word physical witness, the original exact source SHA, independent per-t exclusion receipts, completeness of the t=0..7 partition and a reproducible end-to-end proof package.
3. Confirm actual independent GitHub CI/proof checker receipts for the exact frozen P13 claim before administrative closure of 0.19. Locally checked finite arithmetic is an important but distinct grade.
4. Explicitly decide/approve 0.20's formal name and P0 contract; **a proposed charter is not an activated version**.
5. FMC/YouTube/WCA human reconstructions remain optional auxiliary datasets and cannot certify the finite deterministic physical cube theorem.

## Key prior research (novelty baselines)

- Bogaerts, Gocht, McCreesh & Nordström, *Certified Dominance and Symmetry Breaking for Combinatorial Optimisation*, JAIR 77 (2023), DOI 10.1613/jair.1.14296.
- Shangguan & Ge, *Separating Hash Families: A Johnson-type bound and New Constructions*, SIAM J. Discrete Math. (2016), DOI 10.1137/15M103827X.
- Xin Wei, Xiande Zhang & Gennian Ge, *Separating Hash Families with Large Universe*, JCTA 216 (2025), DOI 10.1016/j.jcta.2025.106075.
- Proof logging / VeriPB references curated at https://veripb.org/publications.html.

**No claim of original authorship of perfect-hash families, standard automata distinction, LP duality, basic Hamming-weight bounds, symmetry groups or proof logging.** New 0.20 claims must be formulated as genuinely distinct physical or source-specific hypotheses and checked against competitors.