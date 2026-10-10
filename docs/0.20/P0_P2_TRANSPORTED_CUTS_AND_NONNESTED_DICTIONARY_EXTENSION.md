# CUBE-REV 0.20 — P0–P2: Physical Cut Transport and Non-Nested Dictionary Extension

**Formal programme:** CUBE-REV 0.20 — Structural Laws of Physical Identifiability: Action-Transported Observation Codes, Restricted Perfect Hash Families & Proof-Carrying Covering Complexity.

**State:** RESEARCH OPEN / P0 EVIDENCE AUDITED LOCALLY / EXTERNAL P13 CI GATE PENDING. This is a mathematical research note, not an external formal proof or a manuscript novelty claim.

## P0 — Frozen ontology and audit

- Physical source SHA-256: `9f2119738f92f56485897c1894d2cb721a3d6b0498c5aa14832c71f18b20e2f1`.
- Original admitted source family: 1,192 distinct subsets of 12 initial tracked UR-edge positions, initial intrinsic edge-flip zero; 220 triples, 492 quartets, 480 quintuples.
- Experiment: one legal word of exactly five actions from 18 HTM moves, cumulative flip bit after each turn, perfect reset, no feedback within a word; cost = number of distinct experiment words.
- `M*(R5,5)=7`; `M*(Rfull,5)=8`; maximal source antichain = 480 five-source generators plus 64 extra face-triple/off-face quartets. Exact fractional covering optima `185/39` and `16/3`.
- Original 37-entry ZIP `CUBE_REV_019_P13_EXACT_FULL_MSTAR5_EIGHT_FINITE_PROOF.zip`: SHA-256 `c84e020b47348e3f8c60ca9b180c365789bf89f2e937b20c5c44145a6a93929d`. Independent 2026-10-10 local check: outer ZIP hash matched; all 36 listed internal SHA-256/length pairs matched; original physical source hash matched; existing P13 receipt compiler re-run returned PASS and its JSON equals frozen receipt; independent 8-word replay separated all 1,192 rows.
- External status: source-locked GitHub Actions full P13 proof success **not established**. At inspection, P7 active-set audit failed with 75 unexpected tracked paths and zero missing allowlisted paths. This is an active-set governance failure, not a proof that P13's mathematics is wrong. CI activation gate remains separate.

## P1 — Exact transported-cut refinement theorem

Let `S` be a finite set of initial positions, initial bit `b_0=0`, and every legal action `a` act by
`T_a(p,b)=(sigma_a(p), b XOR 1_{C_a}(p))`, with a permutation `sigma_a` and cut `C_a subset S` (possibly empty). Let `P_i=sigma_{a_i} o ... o sigma_{a_1}` with `P_0=id`, and let `E_i=P_{i-1}^{-1}(C_{a_i})`.

**Proposition P1-A (exact Boolean signature and rank gain).** For every word `w=a_1...a_L` and initial positions `s,t`, their entire cumulative binary observation histories agree iff the membership vectors `(1_{E_i}(s))_i` and `(1_{E_i}(t))_i` agree. Let `Pi_i` be the partition of `S` by the first `i` membership bits. Then

`|Pi_i|-|Pi_{i-1}| = #{B in Pi_{i-1} : 0 < |B intersect E_i| < |B|}.`

**Proof.** The i-th observed bit is the XOR of the first i increment bits, and adjacent observed bits recover the increments by XOR, so the two transcripts define the same partition. Adding cut `E_i` divides each old cell B into at most the two parts `B intersect E_i` and `B minus E_i`. Precisely one new cell appears for each nontrivially split B. QED.

**Corollary P1-B (physically constrained reachability).** The achievable maximum rank at length L equals the maximum number of distinct atoms of the cut arrangements `(P_{i-1}^{-1}C_{a_i})_{i=1}^L` over executable words, and can be strictly below `2^q` even when q informative actions exist. Cut support sizes alone do not determine that maximum: the allowed prefix permutations constrain which intersections are realizable. If all transported cuts are unions of blocks of one invariant partition with m cells, rank is <=m for every L.

**Adversarial toy, reversible and deterministic.** On `S={0,1,2,3}`, set F to flip on `{0,1}` and swap positions 0 and 1, and let P swap positions 1 and 2 with no flip. Word FFF gives rank 2 (all transported cuts equal `{0,1}`); word FPF gives rank 4 (cuts `{0,1}` and `{1,2}`, all four membership atoms nonempty). Thus inserting a zero-immediate-information transport action increases identifiability. This is a toy demonstration of an established partition-refinement principle, **not** a novelty claim by itself.

## P2 — Non-nested optimal dictionary extension (physically certified instance)

For a finite source-family inclusion `R subset R'=R union H`, let `Cov(w)` be the requirements separated by one executable word and let `D` be a chosen optimum cover of `R`. Define `U_H(D)={A in H: A not in union_w-in-D Cov(w)}` and the exact extension/repair number

`rho_H(D)=min{|E|: E subset W, U_H(D) subset union_w-in-E Cov(w)}.`

**Proposition P2-A (repair obstruction).** A selected old-optimal dictionary D extends to R' by at most one extra word iff there exists an executable word covering all of `U_H(D)`. A necessary certificate for impossibility is `max_w |Cov(w) intersect U_H(D)| < |U_H(D)|`. This is exact set-cover logic, with physical relevance only when the maximum ranges over genuinely executable words.

**Cube instance with a strict non-nesting witness.** P10 has an actually executable seven-word R5 dictionary `D7`, hence optimal by the independent exact R5 lower bound. Independent replay against the original source masks finds it covers 1,120 of 1,192 original requirements: precisely 72 are left, all 64 new maximal quartets and eight face-homogeneous triples. Independently scanning all 14,938 actual physical L5 observation partitions finds `max_w |Cov(w) intersect U_H(D7)| = 36 < 72`. Consequently `rho_H(D7) >= 2`. Since an eight-word full dictionary exists, **the specific old-optimal seven-word D7 cannot be a subset of any full-optimal eight-word dictionary**; at least one old selection must be replaced.

The eight-word P13 positive witness is *itself irredundant on R5*: deleting each of its eight words in order leaves only `476,476,464,472,472,468,476,476` of the 480 R5 requirements covered, respectively. This was independently recomputed from the frozen 18x24 physical action maps and 1,192 source masks. Thus an inclusion-minimal eight-word R5 cover coexists with a strictly smaller seven-word R5 optimum. Do not confuse irredundancy with minimum cardinality.

**P2-B — Novelty guard.** The abstract obstruction and Boolean-cut identities follow from known finite set-cover and separating-system/automata theory. The exact physically executable non-nesting and numerical repair obstruction are instance-specific mathematical facts. A new general law would require additional structural assumptions on the action-generated cut language and independent countermodels that discriminate it from ordinary set-cover non-nesting.

## Prior-art boundaries and next falsification

- Perfect hash families: Stinson, *Perfect Hash Families: Probabilistic Methods and Explicit Constructions*, JCTA (2000), DOI 10.1006/jcta.1999.3050.
- Finite-state distinguishing-sequence complexity: Lee and Yannakakis, *Testing finite-state machines: state identification and verification*, IEEE TC (1994), DOI 10.1109/12.272431.
- Separation of adaptive versus preset observability: *A survey on observability of Boolean control networks*, Control Theory and Technology (2022), https://link.springer.com/article/10.1007/s11768-022-00122-x .
- Proof-log competitor: VeriPB, https://veripb.org/ . Verify source-locked external artifacts before upgrading evidence grade.

**Next experiment:** quantify the reconfiguration distance between a given old-optimal D and full-optimal dictionaries; test for a structural bound in terms of reachable transported cuts and find the smallest reversible-transducer counterexample. Do not announce an original theorem until classical CSP/set-cover reductions and stronger adversarial families are examined.

## Custody and authorship

Preserve all 0.19 proofs, previous charter title as history, no deletion or rewriting of obsolete status logs. The source repository is `WhoSia/CUBE-REV`; publication and commit attribution must remain solely `WhoSia`, with no bot coauthor or coauthor trailers.
