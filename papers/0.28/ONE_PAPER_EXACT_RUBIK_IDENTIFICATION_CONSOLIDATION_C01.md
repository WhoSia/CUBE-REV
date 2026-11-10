# WORKING SINGLE PAPER — Exact State Identification in the Rubik Group Under Two Observation Regimes

**Version: C0.1 research consolidation, 2026-11-10.** **NOT SUBMISSION-READY.** This is an explicitly scoped *one-manuscript candidate* consolidating Paper A D0.5 and Paper B D0.8 without deleting or superseding either source manuscript, and does not assert a new unified optimization quantity or publication priority. All numerical cube results below are **inherited from separately maintained project certificates**, with verification duties listed in §7. The six-state general observation-model demo is independently executable and is deliberately not claimed as a Rubik theorem.

## Abstract

We investigate exact zero-error state identification of legal fixed-centre 3×3×3 Rubik configurations under two deliberately distinct observation regimes. First, for the radius-six ball in the symmetric 18-half-turn metric, a *tagged cubie sensor* reveals the complete position and orientation of a specified original corner or edge. Using finite physical short-word stabilizer certificates and independent 48-moving-facelet enumeration, the inherited classification establishes an optimum of sixteen tagged cubies and precisely 156 optimum sensor arrangements among 4,845 sixteen-sensor subsets. From this physically certified classification and legality constraints we derive a full inclusion-wise minimal-sensor spectrum of {16,17}: 156 minimal sixteen-sensor and 276 minimal seventeen-sensor arrangements, 432 total. Their exact proper-rotation structure and a rational analysis of three randomized removal policies distinguish minimum from merely minimal observation systems. Second, for the **entire legal cube group**, one paired observation of one spatial edge-facelet color and one spatial corner-facelet color is allowed per frame; reversible known legal turns between frames have zero charged cost. A separately inherited certificate establishes that fixed probing schedules require exactly 21 frames, whereas an explicitly constructed feedback policy identifies all legal states in at most 20; the unrestricted adaptive optimum remains between 18 and 20. Thus a strict preset-versus-feedback improvement is already established in this separate categorical observation regime. We explain both studies through the standard distinction between static hitting sets and adaptive decision trees, while keeping their state domains, sensor channels, physical meaning and resource units separate. The contribution is **two auditable cube-specific finite theorems within one observation-theoretic case study**, not a novel general group-base or adaptive-distinguishing-sequence theorem.

**Keywords:** Rubik group; exact identification; radius-restricted base; finite-word stabilizer; categorical facelet probe; adaptive decision tree; minimal sensor arrangements; certified finite computation.

## 1. Exact model and central question

Let \(G\) be the legal 3×3×3 fixed-centre Rubik group, \(T\) the usual symmetric 18 generators (quarter turn, inverse quarter turn and half turn of each face), and \(B_r=\{g\in G:\ell_T(g)\le r\}\). An experiment begins at one unknown original state \(x\) drawn from a specified state domain and must identify that exact state without error. We consider two **noninterchangeable** experiments.

**Regime A — spatially tracked original cubie tags.** The hidden domain is \(B_6\), not all \(G\). Choose \(S\subseteq\Omega\), where \(\Omega\) consists of twenty persistently labelled *original* cubies: eight corners and twelve edges. A sensor for \(u\in\Omega\) returns the exact current position AND orientation of original cubie \(u\). All sensors in \(S\) are read jointly, without dynamic query changes. Let \(\pi_S\) be the resulting output signature. Minimize \(b_6=\min\{|S|:\pi_S|_{B_6}\text{ injective}\}\).

**Regime B — spatially queried categorical facelet colors.** The hidden domain is the **entire** \(G\) (43,252,003,274,489,856,000 distinct legal states). One frame returns the ordered pair of six-category color observations from exactly one spatial edge facelet and one spatial corner facelet. A known legal sequence of face turns may reposition these read locations before the next frame, without using additional observation frames; known turns are **not charged**, and all 576 pairs of 24 edge and 24 corner spatial sticker read locations must be physically reachable. The observed colors do not tag individual original cubies. Minimize the number of paired frames of either (i) a preset independent-of-observations query schedule or (ii) an adaptive, history-dependent schedule. These frame costs cannot be compared numerically to \(|S|\) in Regime A.

**Central question:** How do exact legal-state structure, observation channel and decision rules constrain zero-error reconstruction? We answer two concrete, independently defined versions, not a universal theorem equating their resource measures.

## 2. Established common mathematical language (not new prior art)

For finite state set \(X\), query family \(Q\), and deterministic observation \(O_q:X\to Y_q\), write the *pair-separating support* \(D_{xy}=\{q\in Q:O_q(x)\ne O_q(y)\}\) for distinct \(x,y\). A preset collection \(S\subseteq Q\) identifies every state **if and only if** it meets every \(D_{xy}\):

\[
  \forall x\ne y,\quad S\cap D_{xy}\ne\varnothing.
\]

This is the ordinary difference-support **hitting-set** formulation. For a belief \(B\subseteq X\), define the exact posterior \(B_{q,y}=\{x\in B:O_q(x)=y\}\). With no query cost asymmetry and with queries preserving the original-state observation semantics, the optimal adaptive decision-tree depth satisfies the usual AND–OR recursion

\[
 V(B)=0\text{ if }|B|\le1,\qquad
 V(B)=1+\min_{q\in Q}\max_{\substack{y\in Y_q\\B_{q,y}\ne\emptyset}}V(B_{q,y}),
\]

with \(V(B)=+\infty\) if every query fails to make progress. For any **single matched observation model**, optimal feedback depth cannot exceed the optimum preset sequence length; strict inequality is possible. However, applying this conclusion *across* Regimes A and B is invalid, since their \(X,Q,Y\), costs and intervention protocols are different.

**Tiny verified illustrative example (not Rubik).** Six states \(A_0,A_1,A_2,B_0,B_1,B_2\), three queries \(q_0,q_1,q_2\): \(q_0\) reports A/B, \(q_1\) discriminates only the three A states and is constant on the B states, \(q_2\) discriminates only the three B states and is constant on A. Any preset set of two queries fails but three queries work, whereas two adaptive queries suffice (ask \(q_0\), then \(q_1\) or \(q_2\) conditional on its output). [Self-contained exhaustive verifier](../../scripts/cuberev-observation/audit_r14_p817_common_observation_bridge.py) confirms all fifteen pair supports, the hitting-set condition and the exact Bellman optimum. The example illustrates why pairwise distinguishability and uniform global sensing are not equivalent; it is a known *generic* phenomenon, not a claimed novel theorem.

## 3. Main result I — finite-radius original-cubie identification

**Theorem A (inherited independently physically checked result).** In Regime A, \(b_6=16\). Exactly **156** of the \(\binom{20}{16}=4,845\) sixteen-tag designs identify every state of \(B_6\). The remaining 4,689 designs fail.

**Proof architecture.** The radius-doubling stabilizer lemma yields \(\pi_S|_{B_6}\) injective iff \(H_S\cap B_{12}=\{1\}\), where \(H_S\) fixes each selected original cubie in both position and orientation. Legality enforces matched corner/edge permutation parity, zero mod-three sum of corner twists, and zero mod-two sum of edge flips. A physically instantiated short-word support classification (including 872 irredundant support masks) proves negative claims, and 41 physically certified target-distance classes close the positive side by independent P48 exact bidirectional distance search. For all 16-tag designs, exactly 156 positives remain, equivalent to omitting two adjacent original corners \(\partial h\) and one of thirteen admissible original edge pairs associated with core edge \(h\). A separate lower certificate excludes all \(|S|\le15\). The full 48-facelet physical source/receipt provenance is maintained in the original Paper A proof package and **must be repackaged for an independent paper release**; the present condensation is not a new execution of those certificates.

**Corollary A1 (complete inclusion-wise minimal spectrum, conditional on Theorem A and historical short-support certificates).** Write \(\mathcal M(B_6)\) for the sizes of **inclusion-wise minimal** identifying tag sets. Then

\[
  \mathcal M(B_6)=\{16,17\}, \qquad
  N^\mathrm{minimal}_{16}=156,\quad
  N^\mathrm{minimal}_{17}=276,\quad
  N^\mathrm{minimal}_{\mathrm{total}}=432.
\]

A direct legal-cubie stabilizer argument and all 66 original edge-pair admissible-core incidences give the complete positive sensor counts 156,672,174,20,1 at sizes 16,17,18,19,20, respectively. Of the 276 minimal17 layouts, twelve omit an original core edge and its two endpoint corners, while 264 omit one corner and two edges (exactly 33 for each corner). No minimal identifying set uses 18 or more sensors. A geometry-only exhaustive verifier and separate finite incidence table are available; both depend on prior physical B12 sign certificates.

**Corollary A2 (geometry and selection).** The 156 size16 minimum layouts form eight orbits under the 24 proper cube rotations. The 276 minimal17 layouts form twelve rotation orbits: one size12 and eleven size24. When starting with all twenty sensors and repeatedly removing a **uniformly selected currently removable** sensor, exact rational finite-DAG enumeration yields

\[
  \Pr(\text{minimum16})=\frac{1166}{1995},\qquad
  \Pr(\text{minimal17})=\frac{829}{1995}.
\]

If removal of currently removable corners is prioritized over edges, \(\Pr(\text{minimum16})=11/12\); if edges are prioritized, the probability drops to \(1/2\). These are **three clearly defined conditional random algorithms**, not a general greedy approximation result or a measurement of a robot's actual operation. The corner-first probability has a short proof: after removing adjacent corners, the unique edge joining them is the only one of twelve possible first omitted edges that cannot be extended to a positive 16-sensor omitted-edge pair. The edge-first probability is the exact ratio \(264/528\) of extendable one-corner/two-edge omission triples.

**Interpretation.** The finite-state observation closure of the B6 identifying family has both minimum16 and strictly larger minimal17 generating sets. Thus the corresponding closure is not matroidal; this does not contradict results on *global group-action* irredundant bases, primitive IBIS actions, or known graph determining-set phenomena, because Regime A is a radius-restricted difference-support system.

## 4. Main result II — full-group paired color observations

**Theorem B (inherited finite certificate and feedback construction).** In Regime B, the exact optimum for preset schedules is \(h_{\mathrm{fixed}}=21\). A physically routable, exactly decoded adaptive schedule identifies **every** legal original cube configuration in at most twenty paired frames. The separate inherited lower certificate currently establishes \(18\le h_{\mathrm{adaptive}}\), so

\[
  18\le h_{\mathrm{adaptive}}\le20,\qquad
  1\le h_{\mathrm{fixed}}-h_{\mathrm{adaptive}}\le3.
\]

**Constructive outline.** The first twelve frames read the first color facelet of all twelve edge cubies and simultaneously use corner readings to complete the two ordered color measurements needed at six corners. The next two frames obtain adaptive edge mate colors while completing a seventh corner; legal corner permutation/twist constraints then determine all corners by frame fourteen. Physical parity information obtained from corners is only used **after** it becomes observable. The remaining frames adaptively read edge mates. The proof's exact finite conditional-edge controller covers 867 possible edge first-color count vectors, 39 color-orbit representatives and 609,376 conditional edge assignments. An exceptional pattern is resolved by using the legally obtained corner parity after two necessary edge-mate reads; all cases finish within eight additional edge reads. The complete-policy certificate includes a source-independent physically routed 48-facelet checker, 576 accessible paired locations and known legal generated/hard-case full-cube decodings. The earlier exact finite lower bound of 20 frames **only** concerns the restricted twelve-first-edge-facelet family, even with favorable parity-oracle help; it does not rule out unrestricted mixed-prefix 19 or 18.

**Scope of novelty.** Adaptive distinguishing sequences and splitting-tree construction are classical automata theory; a generic claim that feedback reduces experimental length is not new. The claim here is the particular full legal Rubik group, six-color joint edge-and-corner observation protocol, exact preset minimum of 21, genuinely physically routable adaptive upper of 20 and independently auditable certificates. The source verification and bibliography must be checked against model-equivalent cube-scanning literature before submission.

## 5. Synthesis — why one manuscript might be preferable

The two results share **exact hidden-state reconstruction, a legal puzzle group, physically specified observations, and a proof-carrying finite decision problem**, but intentionally have **different hidden domains, types of measurement, actions and costs**. Presenting them together can expose how hard legal-state constraints turn naive counts into rigorous constructions, while demonstrating two orthogonal design questions: "which permanent rich sensors are needed on a bounded ball?" and "how many low-bandwidth adaptive frames identify any legal state?"

The **unifying contribution is a model-specific comparative case study**, not a theorem equating 16 sensors to 20 frames, nor a proof that Theorem B follows from Theorem A. A critical editor could reasonably prefer splitting these into two papers if the combined study obscures the central theorem, if independently checkable supplements become unwieldy, or if audiences for short-radius computational group theory and active FSM learning differ sharply. This version therefore keeps both archived full manuscripts intact while running a **single-paper C0.1 candidate** through a referee-style decision gate.

**Recommended ordering:** A (main theorem, 156 layouts, 432 minimal) → compact A robustness/greedy structure → B (strict whole-group feedback separation) → shared methodological discussion of exact finite evidence. The A/B comparison belongs in one sharply delimited paragraph in the introduction and conclusion, not an unsupported numerical transfer.

## 6. Prior mathematics and related models

- Original group bases, stabilizer chains and matroid conditions: Bailey and Cameron (2011), *Base size, metric dimension and other invariants of groups and graphs*; Cameron and Fon-Der-Flaass (1995), *Bases for Permutation Groups and Matroids*; Dalla Volta, Mastrogiacomo and Spiga (2024), *On the Cardinality of Irredundant and Minimal Bases of Finite Permutation Groups*. These study related **different** mathematical settings.
- Classic preset and adaptive FSM experiments: Moore (1956), *Gedanken-Experiments on Sequential Machines*; Lee and Yannakakis (1994), *Testing Finite-State Machines: State Identification and Verification*.
- Construction algorithms and partial beliefs: Türker, Ünlüyurt and Yenigün (2016), *Effective Algorithms for Constructing Minimum Cost Adaptive Distinguishing Sequences*, doi:10.1016/j.infsof.2016.02.001; Soucha and Bogdanov (2020), *State Identification Sequences from the Splitting Tree*, doi:10.1016/j.infsof.2020.106297; Hierons and Türker (2015), *Incomplete Distinguishing Sequences for Finite State Machines*, doi:10.1093/comjnl/bxv041.
- Distributed observation is not this jointly controlled model: Hierons and Türker (2016), *Distinguishing Sequences for Distributed Testing: Adaptive Distinguishing Sequences*, doi:10.1093/comjnl/bxw004.
- Metric dimension means distance-based graph outputs, not full tagged-cubie states. Color camera robot scanning, noisy RGB readings, human cognitive mechanisms and actual HTM path optimization are NOT covered by the exact categorical model here.
- **Original source custody:** Existing Google Drive original PDFs are retained at their established file IDs; no new paper PDF bytes were produced by this draft.

## 7. Proof-release gate and what would refute this consolidation

1. **Independent physical check of Theorem A:** Produce the exact 41 stabilizer distance classes and all 4,845 design verdicts from the original 48-facelet engine and preserved raw data; then reproduce 156 positive and 4,689 negative. Preserve source SHA/inputs, human committer provenance and a second independent implementation, not only a success summary.
2. **Independent feedback check of Theorem B:** Recover the full conditional edge policy, all exceptional residual states and physical routing proofs, then rerun with a second implementation against the entire mathematically specified finite conditional family. The reported 2,001 generated cubes and 2,592 exceptional cubes are useful smoke tests but are NOT exhaustive over all 43.25 quintillion original states. Conditional exhaustive state-class reasoning must carry the universal theorem.
3. **Exact read-only CI and Lean:** Link published source blob identifiers and complete logs for relevant certificates; keep generic Lean P8.9/P8.10 as SOURCE_PENDING_KERNEL until completed proofs are observed. Any later Lean proof of geometry must discharge physical parity/covariance hypotheses, not postulate the numerical theorem.
4. **Novelty/prior-art review:** Check equivalence of prior Rubik original-tag observation and two categorical probes, not just nearby words. Existing source searches suggest relevant classical ADS and base theory but do not establish global originality.
5. **Compact-paper editorial gate:** Ask an external mathematics/algorithms reviewer whether A and B genuinely form a single intellectual claim. If not, retain one concise **Paper A** with the proven spectrum as its submission focus and keep B as a separate technical note until stronger unrestricted adaptive results emerge. One paper is a choice, not a substitute for coherence.
6. **Submission readiness:** The present C0.1 is a newly authored research draft, NOT peer-reviewed, and the formal hypotheses are explicit. No fabricated publication outcome, robotics experiment, user study or completed 19-frame exact minimum.

**Source manuscripts preserved:** [Paper A D0.5](RADIUS_RESTRICTED_CUBIE_OBSERVATION_DRAFT_01.md) and [Paper B D0.8](DUAL_COLOR_PROBE_ADAPTIVE_IDENTIFICATION_DRAFT_01.md). This merged draft is a **third editorial work product**, not an erasure of research genealogy.
