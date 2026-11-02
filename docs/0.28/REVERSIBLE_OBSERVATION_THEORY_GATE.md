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
