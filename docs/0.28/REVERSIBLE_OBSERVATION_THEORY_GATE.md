# Reversible observation: first external-theory audit (2026-11-02)

## Problem contract
Finite set X of n explicit states; nonempty alphabet A acting by permutations
delta_a:X->X; fixed Moore output q:X->Y. An action word acts on both candidate
states by the SAME symbols. Observation is taken at the empty prefix and
after every action. A pair {x,y} is distinguishable if there exists a word w
such that q(delta_w(x)) != q(delta_w(y)) (equivalently the two observation
traces differ on at least one prefix).

## Elementary pair-graph criterion (existing standard automata technique)
Form graph on unordered pairs {x,y}, x!=y; label-a edge to
{delta_a(x),delta_a(y)}. Mark any pair with q(x)!=q(y).
A pair is distinguishable iff it can reach a marked vertex. Proof:
a path labeled w corresponds exactly to applying w simultaneously to
both states, and marked terminal output differs. Converse by prefixes.

The shortest such word has length <= C(n,2)-1 whenever it exists:
a shortest path to the marked set never revisits an unmarked pair,
and there are <= C(n,2) pair vertices in total. For n<2 no pairs.
This is a straightforward finite-graph bound, NOT claimed as new.

## Physical 4-state countermodel
X=Z/4Z, action a(x)=x+1 mod 4.
q_singleton(x)=1 iff x=0: states 1,2,3 share the same initial observation,
but prefix outputs at actions 0,1,2 distinguish all four.
q_parity(x)=x mod 2: states 0 and 2, and 1 and 3, remain indistinguishable
under every action because q(a^t(x+2))=q(a^t(x)).
Thus reversibility alone does not imply observability.
Run: python scripts/cuberev-observation/reversible_pair_audit.py

## Research gate
These are established elementary Moore-machine observations and an
illustrative model, NOT a novel result of CUBE-REV. Next benchmark task:
enumerate all small reversible action/output systems to locate the smallest
nontrivial gap between a *characterizing family of words* and a *single
preset distinguishing word*, holding the same q, X, action alphabet, and
cost convention. Before claiming novelty, review Lee–Yannakakis (1994),
Rivest–Schapire (1993), and the modern FSM-testing literature.
Static multi-coordinate cubie sensors b_r and 0.18's fixed-length move-word
experiment dictionary Mstar remain DIFFERENT tasks; never compare numerical
optima without common model.

Primary classical complexity source: Garey–Johnson (1979), Theorem 3.9
MINIMUM TEST COLLECTION, appendix SP6 MINIMUM TEST SET, final-printing
correction asserting NP-completeness even for tests of size at most 2.
This does not establish hardness of Rubik-legal restricted tests.


## R6 Origin Re-entry: full physical state does not identify a mental history mechanism (2026-11-05)

The founding CUBE-REV 1.md (2026-07-24) and the Grand Doctrine make human cube reconstruction the central explanandum. Exact physical search and observation theory are instruments, not convenient substitute aims.

**Retrospective feasibility warning.** The earlier 0.21 P4 naturalistic source-pair ladder contains 1,442 pairs at coarse FC3, 88 after exact full-cubie-state matching, 10 after recorded rotation-frame proxy, one after recorded stage, and **zero** after matching previous action. This is missing comparison support, NOT evidence that cognition is memoryless. Paper 1 M1.2 separately reports 346 turnover-positive frontier segments, 313 from the dominant reconstructor. Neither set permits an independent, reconstructor-invariant history-as-cause inference without further controls.

**New physical countermodel.** The actual P48 cube engine confirms `U U' F` and `R R' F` are different three-HTM histories ending in the identical non-solved full state `F`, with an identical final action. Let H distinguish histories and Y distinguish a later choice. Two competing mechanisms are observationally indistinguishable:
- history-policy: H is uniform and Y=H;
- latent-goal policy: Z is uniform, H=Z, and Y=Z.

Both yield P(H=h,Y=y)=1/2 for h=y, zero otherwise, conditional on the same complete physical end state. However, under an experimentally assigned history H=0, the first model predicts P(Y=0)=1, the second 1/2. This is a textbook causal confounding construction, NOT a new generic causal theorem. It is an exact physically matched Rubik example. Test: `scripts/cuberev-observation/test_reversible_pair_audit.py`, `R6HistoryConfoundingPhysicalCourt`.

**Falsifiable next comparison.** Predict future actions using C=coarse progress, X=full state, and H=recorded action history, with explicit viewpoint, task, method and provenance. Compare prospective out-of-group log scores; `I(Y;H|C,X)` is a predictive information target, not causal evidence. A controlled physically matched-endpoint randomized history manipulation could distinguish the two mechanisms, but execution/motor priming and unmeasured goals still require controls and participant ethics. The inherited naturalistic data have inadequate strict matched overlap for that causal conclusion. Do not claim a human cognition result.

Full-group adaptive exact six-color identification remains open at 16 to 21 frames; fixed nonadaptive minimum is 21. The R6 physical causal-control example is a separate scientific problem, not an improvement of that horizon.
