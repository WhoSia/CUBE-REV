# CUBE-REV 0.17 — return-maximality under inverse-closed reversible actions

**Evidence status:** small GENERAL MATHEMATICAL LEMMA with human proof and separately independently replayed finite examples; a transferable 0.17 mathematical step, but the PSD/Gram inequality and spectral graph facts are CLASSICAL. No novelty or Lean-kernel claim yet.

## Setup

Let X be a finite state space, A a finite *multiset* of admissible deterministic bijections X→X, and let B be the nonnegative INTEGER count matrix
`B[x,y]=#{a in A : T_a(x)=y}`. The t-th matrix power counts literal length-t action words ending y when started at x. Do not identify different action-token words merely because they induce the same map.

If A is **inverse-closed with equal multiplicities**, `B=Bᵀ`, since inverse tokens pair transitions x→y and y→x. A fixed action multigraph is **walk-regular at length t** if all diagonal entries of `B^t` are equal; a vertex-transitive automorphism group of B ensures this for every t. Note that state-transitivity of the abstract group action alone does NOT automatically assert that arbitrary fixed-generator count matrix B has an automorphism acting transitively: preservation of the action multiset is an additional condition.

## Theorem 0.17-A — two exact conditions for return-fiber maximality

Fix any positive integer t and assume B is real symmetric with nonnegative integer entries and has the same length-t diagonal walk count r_t at every state. If EITHER

1. t is even, OR
2. B is positive semidefinite,

then for all x,y in X, `(B^t)[x,y]≤(B^t)[x,x]=r_t`. In particular the maximum number of length-t literal histories with a common terminal state is exactly the same-state return count r_t, for ANY initial x.

**Proof.** If t=2k is even, symmetry gives `B^(2k)=(B^k)ᵀB^k`; hence it is positive semidefinite. If B is already positive semidefinite, every positive integer power B^t remains positive semidefinite by its spectral theorem. For any real PSD matrix Q there are Gram vectors v_x with Q[x,y]=〈v_x,v_y〉, so Cauchy–Schwarz yields `|Q[x,y]|≤sqrt(Q[x,x] Q[y,y])=r_t`. For Q=B^t, entries are nonnegative history counts; take Q=B^t and conclude `Q[x,y]≤r_t`. Equality at y=x gives maximality. QED.

**Spectral corollary.** If a finite symmetry group acts transitively by automorphisms of B, then `r_t=tr(B^t)/|X|=(Σ_λ m_λ λ^t)/|X|`. For even t this holds for inverse-closed action multisets whether or not their spectra contain negative eigenvalues. For ALL t it holds if B is additionally positive semidefinite. The 0.16 tracked-edge formula is an instance with `B=10I+CᵀC` and an explicitly transitive 24-vertex action multigraph.

## Counterexample: why odd horizons need an additional hypothesis

Let `X={0,1}`, A contain only one swap action, and `B=[[0,1],[1,0]]`. B is symmetric and vertex-transitive but has eigenvalue −1. At t=1 the number of one-action words returning to 0 is ZERO and the number ending in 1 is ONE; **return is not maximal**. At t=2 the unique two-action word returns to 0, in accord with the even-horizon theorem. This is a direct counterexample to the overbroad conjecture that symmetry and vertex transitivity alone imply return maximality at every t.

## Why it matters to 0.17, and what is not new

The statement shows the P8 maximally-colliding SAME endpoint phenomenon is structural, NOT dependent on Rubik cube geometry: it follows whenever inverse closure, appropriate symmetry/walk-regularity, and either even horizon or PSD hold. It is a classical matrix/graph inequality, not newly invented spectral graph theory. The **new research question** is whether **observable** history-fiber maxima and adaptive identification/reset lower bounds admit similarly tractable invariants for nontrivial observation partitions O:X→Y that do not respect endpoint state symmetry; an endpoint theorem alone does not settle that.

No human cognition or physical full-cube inference follows. Source inspection and Lean proof development must not upgrade this mathematical lemma to an independently peer-reviewed discovery.
