# CUBE-REV 0.28 — R14-P8.8: Comparative Horizon and Unrestricted Nineteen-Frame Proof Gate

**Date:** 2026-11-10. **Status:** scientific direction / pre-registered falsifiers and proof responsibilities; **NOT** a newly solved exact optimum, new CI result, general theorem, or publication-priority certificate.

## 0. Decision after P8.6/P8.7

The current proven working statement in the exact idealized model is

\[
h_{\mathrm{fixed}}=21,\qquad 18\le h_{\mathrm{adaptive}}\le20.
\]

The 20-frame constructive protocol is a real full 12-edge/8-corner color-observation upper bound, not the earlier oracle-conditioned edge game. Its corner channel identifies all corners by frame 14 and only then supplies their parity to the edge strategy. The independent 20-frame lower theorem is **restricted** to a fixed first twelve edge observations, one designated first facelet at each spatial edge position, **even if the parity is revealed free as early as frame 12**. It does not prohibit a mixed-first-reads 19-frame protocol. Historical P8.1–P8.3 files retaining 18–21 describe their own prior information state, not a current global interval.

**Primary verified source trails:** [P8.6 construction](20261109_R14_P86_CONSTRUCTIVE_20_FRAME_ADAPTIVE_UPPER.md), [P8.7 restricted lower](20261109_R14_P87_FIXED_FIRST_EDGE_SCAN_20_LOWER.md), [P8.3 actual belief aliases and three-edge obstructions](20261109_R14_P83_PHYSICAL_BELIEF_ALIASES_AND_THREE_EDGE_NO_GO.md), and the [Paper B D0.8 manuscript](../../papers/0.28/DUAL_COLOR_PROBE_ADAPTIVE_IDENTIFICATION_DRAFT_01.md). R14-P8.6 remote Actions PASS is not independently established by this note.

## 1. Three exact, different optimization problems

| Question | \(M^*(L)\) fixed physical experiment dictionary | \(b_r\) radius-limited full-cubie sensors | \(h_{\mathrm{adaptive}}\) full-group online color probing |
|---|---|---|---|
| Input domain | Frozen 1,192 admitted subsets of 12 possible initial locations of a tracked zero-flip UR edge | Entire distance ball \(B_r=\{x:d_{\mathrm{HTM}}(e,x)\le r\}\) | All 43,252,003,274,489,856,000 legal cube states |
| Observation | Five-or-\(L\)-turn **intrinsic edge-flip-bit transcript** from each preset real HTM word | **Original-tag full cubie position and orientation** of each selected cubie | One spatial **edge facelet six-color** and one spatial **corner facelet six-color** response per paired frame |
| Policy | Fixed set of separate prepared experiments with the source/reset semantics of that experiment model | Fixed subset of original cubie tags | Joint adaptive decision tree: each next paired spatial read may depend on previous colors |
| Cost | Number of prescribed \(L\)-turn experiments | Number of original cubie tags observed | Maximum number of paired-color frames, with all tracked legal turns uncharged |
| Frozen result | \(M^*(5)=8\) for the admitted family | \(b_5=b_6=16\) | Fixed 21, unrestricted adaptive in \([18,20]\) |
| Missing generalization | Extend source family / experiment length / observation alphabet / feedback | Expand radius and/or weaken the ideal tag sensor | Settle 19-frame existence, then 18 if needed; add charge/noise only under a *new* model |

**Do not compare 8, 16 and 20 as if they measure the same resource.** The \(M^*\) source is not the full cube; a \(b_r\) channel reads far more per chosen tag than one facelet color; \(h\) counts paired rounds, not number of stickers, robot turns, total experiment words, motor-time or sensors owned. The \(\lvert G\rvert\le36^h\) Shannon-style counting argument only gives \(h\ge13\); the archived \(h\ge18\) is a stronger separate combinatorial certificate.

The \(M^*(5)=8\) local exact finite proof has distinct authority from the externally checked \(M^*(4)=34\) DRUP record. The \(b_6=16\) proof uses the inherited \(b_5\ge16\), 156 positive size-16 original-cubie layouts, and the physical stabilizer condition \(H_S\cap B_{12}=\{e\}\), via 41 HTM-distance classes. These do not establish a new full-group categorical-color horizon.

Sources: [original finite \(M^*(5)\) instance and exact proof](../0.19/P13_FINAL_EXACT_PHYSICAL_MSTAR5_EIGHT.md); [\(b_6\) physical 16-sensor certificate](B6_EXACT_16_TWO_CERTIFICATE_CLOSURE.md). The continuity question is how *source restrictions, observation channels, adaptive choices, and charged resources* transform state-identification limits, not a narrative that one scalar subsumes the others.

## 2. Exact global P8.8 question

Let \(G\) be the original legal cube group and \(\mathcal Q\) all \(24\times24=576\) pairs of initial spatial edge/corner facelet slots. For a legal nonempty belief \(B\subseteq G\) and \(q\in\mathcal Q\), let \(B_{q,y}=\{x\in B:O_q(x)=y\}\) for a pair \(y\) of categorical six-color outputs. All tracked legal routing is represented exactly by the corresponding spatial query (no orientation/position reset and no free unknown state information).

\[
\operatorname{Win}(B,k)\ \Longleftrightarrow\
(|B|=1)\ \lor\
\left(k>0\ \land\ \exists q\in\mathcal Q\
\forall y\;(B_{q,y}\ne\varnothing\Rightarrow\operatorname{Win}(B_{q,y},k-1))\right).
\]

Use \(|B|\le1\) only if a generic implementation intentionally admits an empty belief; physical histories are nonempty. The two genuine resolution targets are:
- **CONSTRUCTIVE** \(\operatorname{Win}(G,19)=\mathrm{true}\), with one deterministic complete online decision tree and all feasible legal initial states replayed or represented by sound complete proof-carrying quotient transport;
- **UNIVERSAL NEGATIVE** \(\operatorname{Win}(G,19)=\mathrm{false}\), with every possible root query excluded under all later adaptive actions and a checkable adversarial certificate. Combined with P8.6 this would establish \(h_{\mathrm{adaptive}}=20\).

Root and color symmetries in Paper B §5 suggest reducing the first query/response to one canonical posterior and then reducing its next queries to twelve exact stabilizer orbits. That reduction is valid **only for exact action/observation-covariant bijections**; it is not permission to treat all equal-size or equal-parity-vector beliefs as equivalent.

**Do not import invalid shortcuts.** The P8.3 physical six-state pair has identical \((E_0,E_1,C_0,C_1)=(1,1,3,3)\), but different multisets of all 576 next-query color partitions. Yet both happen to have residual Bellman depth one. Thus matching counts is not a sound query-partition quotient; different partitions alone do *not* prove distinct future optimal depth. P7 oracle-conditioned edge residual tables are not unconditional full-group Bellman values.

## 3. Two deliberately rival P8.8 experimental directions

### A. Find a real 19-frame constructive policy (the falsifier of conjectured optimality 20)

Test mixed-edge first prefixes with 9–11 unique edge positions encountered early, allowing second-facelet ("mate") reads before all twelve first facelets. Jointly schedule the real corner channel and its parity-availability time. Prioritize policies that **do not force** the hard transcript \`RRRFFFLLLBBB\` after exactly twelve first edge reads, but do not mistake avoiding that string for universal success. Use exact physical P48 colors, state consistency, and 576 reachable paired slots.

A valid positive output is a policy that *universally* recovers an unknown full state at or before frame 19; success on 2,001 move samples, on 2,592 hard-condition states, or on a conditional 648-state suffix alone is insufficient. A prospective 19-frame policy should be independently implemented and replayed, with first-color history canonicalization and parity timing audited.

### B. Prove a true unrestricted 19-frame obstruction (the falsifier of the 19-policy hope)

Starting from the canonical root posterior, seek a **sound adversarial response game** or small collision core that survives all adaptive paired queries for the remaining budget. A fixed bad query schedule or a bad greedy-policy branch proves nothing against other choices. Each proposed pruning rule must be certified against the exact \(\exists q\,\forall y\) order. Priority: extend actual P8.7 1,296-state hard-suffix certificates and P8.3 star/triangle negative branches to prefix classes involving partial edge/color and physically observed corner parity. The known hard three-edge theorem excludes **a particular late schedule**, not all 19-frame policies.

A negative certificate must either enumerate a sound symmetry-complete set of all possible root-conditioned policies or provide a transferable universal adversary. A time-out, missing witness, weak cardinality lower bound, or MIP/SAT UNKNOWN is not FALSE.

**Stop/revise trigger:** If a policy-search code extension cannot discriminate A versus B by a new exact candidate, sound lower pruning, failed transport witness or independently replayable counterexample, defer it. Work on the scientific question first, not on new code names or commit counts.

## 4. Manuscript significance and external-priority gate

**Paper candidate already exists:** A self-contained computational mathematics paper can plausibly center on (i) exact idealized dual-color-probe model, (ii) explicit 20-frame *entire-group* adaptive construction, (iii) 21-frame preset minimum, (iv) restricted exact 20-frame converse, and (v) parity-timing and physical routing/decision-tree audit. Exact equality \(h_{\mathrm{adaptive}}=20\) would make a substantially stronger main theorem, but a sharp upper-bound advance can be publishable *without* the global optimum if it is novel, significant and independently checkable.

**Unresolved publication gates:**
1. Establish proper bibliographic priority against classic preset/adaptive FSM distinguishing sequences, active diagnosis, decision-tree complexity, and practical limited-color cube scanners. The notions of ADS, Bellman recurrences, group action transport and last-corner inference are prior art; a new application-specific constant is not automatically a novel general theory.
2. Include a clean standalone statement/proof of the *global 18 lower* and fixed 21 optimum, with precise input model and certificates, or downgrade claims to correctly cited dependency statements.
3. Require source snapshots, concrete SHA provenance, raw proof receipts and **independent** physical-geometry + decision-tree validators; distinguish local tests from actual remote Actions SUCCESS.
4. Do not market this as human cognitive evidence, a physical noisy RGB guarantee, a 20-HTM cube solving algorithm, a robotic movement-time optimum or an unqualified first discovery.
5. The strongest CUBE-REV research arc will eventually compare \(M^*\), \(b_r\), and \(h\) under a common finite-reversible-system **family** that systematically varies the observation channel, reset privileges, feedback and costs. That extension is a hypothesis and program, not a theorem already achieved.

Literature candidates for exact model-by-model comparison:
- *Effective algorithms for constructing minimum cost adaptive distinguishing sequences*, Information and Software Technology 74 (2016), 69–85, DOI 10.1016/j.infsof.2016.02.001.
- Hierons & Türker, *Distinguishing Sequences for Distributed Testing: Adaptive Distinguishing Sequences*, The Computer Journal 59(8) (2016), 1186–1206, DOI 10.1093/comjnl/bxw004.
- *State identification sequences from the splitting tree*, Information and Software Technology 123 (2020), 106297, DOI 10.1016/j.infsof.2020.106297.
These demonstrate deep existing ADS methodology. **2026-11-10 custody update:** All three papers' original PDFs are now confirmed in the central Research OS Literature Commons: [Türker, Ünlüyurt & Yenigün 2016](https://drive.google.com/file/d/10N6hZKeeKT6zMp0udLza4Si1yIaYEKUm/view), [Hierons & Türker 2016](https://drive.google.com/file/d/17NsR-UoqDikvTH_5vmG1uweOSNsPQ7On/view), and [Soucha & Bogdanov 2020](https://drive.google.com/file/d/1F7RmxBZjYh4lpOqInF3G-hvytObsF17k/view). In addition, Moore (1956), Buhrman & de Wolf (2002), and Hierons & Türker (2017 preset) were read and admitted to central custody. [R14-P8.9/P8.10 literature and formal proof audit](20261110_R14_P89_P810_LITERATURE_FORMAL_PROOF_BRIDGE.md). This ownership confirmation **does not establish** that no prior paper proves this exact twenty-frame cube instance; model-specific priority remains open.

## 5. Custody and authority of this unit

This document is a **T1 research-direction / comparative statement and prospective falsification contract**. It adds no new raw T2 experimental result and therefore does not call its GitHub text a Drive-byte scientific seal. Commit to **existing \`research/current\` only**, with human-authenticated \`WhoSia\` author **and committer**, preserving \`main\`; verify actual commit metadata after creation. The full independent scientific interpretation belongs on the CUBE-REV 0.28 Notion record; any newly generated scientific T2 raw evidence in future must be separately preserved in the Lab's Drive and verified by byte readback. The repository and Research OS custody/doctrine documents govern cleanup. No AI/bot identity should be a repository contributor.

**Closure at writing time:** Working bounds inherited from P8.6/P8.7; exact value OPEN; A and B not executed or solved by this direction note; remote CI unverified; literature completeness OPEN; empirical human-cognition claims unchanged.
