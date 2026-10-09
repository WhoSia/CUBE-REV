# CUBE-REV 0.16 — Internal pure-mathematics P8: exact history multiplicity and reversible control

## Frozen model and existing result
A *single tracked edge* has 24 possible current coordinates (12 physical edge slots × intrinsic orientation bit). Legal primitive actions are 18 reversible HTM face turns. A read of the bit is obtained after every action (no free initial read in active-diagnosis problems). Historical-word counting assumes exactly `t` actions, known initial tracked-edge coordinate, known final tracked-edge coordinate, **no additional observation record**, and distinct literal action-token strings count as distinct histories, including canceling consecutive moves. This is neither a complete 3×3 cube endpoint nor a human memory capacity measurement.

## Theorem A. Universal feedback diagnosis/restoration sandwich
Let `X` be a finite state set, `A` a collection of bijections on `X`, `o:X→{0,...,q-1}` a perfect sensor, `S⊆X` a nonempty initial source support, and `z∈X` the desired physical target. After each chosen action, one sensor symbol is reported and the controller may stop at a branch. Define `D(S)` to be the smallest worst-case depth of a feedback policy that uniquely identifies the **initial** state, and `R_z(S)` the smallest worst-case depth of a feedback policy that sends every source in S to the **same exact** z. Assume all states reachable from source states can be steered to z by a known-state word of length at most `d_z` (a finite worst-case correction radius).

Then, whenever these numbers are finite,

`D(S) ≤ R_z(S) ≤ D(S)+d_z`.

**Proof.** Suppose reset policy succeeds. If distinct original states x,y generated exactly the same entire reported symbol string, deterministic feedback entails the same chosen action word and stop decision. The action word acts bijectively and cannot send x,y to the same z. Hence source-state→output-string is injective, so that reset policy also identifies the original state from its symbol string; this yields D≤R. Conversely run any depth-D diagnosing policy. Its reported transcript determines the original source state, and because every chosen action is publicly known and bijective, also the exact current state. A known-state correction word to z of length ≤d_z completes the reset, giving R≤D+d_z. ■

**Prefix/Kraft refinement.** Because stopping is a deterministic function of observed history, terminal observation strings are prefix-free. If there are |S| different states all successfully reset, the q-ary Kraft bound says Σ_{x∈S}q^{-ℓ(x)}≤1. Thus `max ℓ(x)≥ceil(log_q|S|)` and for source prior π the expected number of observations satisfies `Eπ ℓ(X)≥H_q(π)` (under exactly this prefix-tree and no side messages). Group invertibility itself does not imply equality in these inequalities.

## Theorem B. Historical word multiplicities are matrix powers
For a finite action multiset A of size m and fixed state set X, let `B_xy` be the number of actions a with a(x)=y (including parallel edges and loops). With known original x, there are exactly `(B^t)_{xy}` literal length-t action strings ending at y. Consequently, given *only* the pair of known initial/final states, the minimum worst-case additional **fixed-length** binary message needed to reconstruct the exact action word is

`b_t(x)=ceil(log₂(max_y (B^t)_{xy}))`.

With W_t sampled uniformly from A^t and Y_t its endpoint, `H(W_t|Y_t)=t log₂(m)−H(Y_t)` by determinism of endpoint conditioned on W. These assertions hold without reversibility, assuming all action words distinguishable as literal historical records.

## Theorem C. Exact 24-state cube endpoint fiber closed form
Let the six cube face labels be U,R,F,D,L,B with opposite pairs (U,D), (R,L), (F,B). The cube's 12 physical edge slots are unordered adjacent (nonopposite) face pairs. Intrinsic orientation assigns one of two **orders** to that pair. Thus each tracked-edge state is an ordered pair `(a,b)` of adjacent faces, 6×4=24 possibilities.

A face action with face a changes the **other** coordinate of `(a,b)` (if a is first), keeping a fixed, and analogously for second-coordinate face b. All three nontrivial rotations of the respective face send b to three other adjacent faces c. A face not incident to the current edge slot leaves `(a,b)` unchanged. Therefore the 24×24 action-count matrix `B` has 12 loops per vertex and exactly one off-diagonal edge per shared first or shared second coordinate.

Form a bipartite graph G with left vertices L_a and right vertices R_b for the six faces and one edge L_a—R_b precisely when a,b are adjacent cube faces. Its 24 edges index the directed pairs. Let C be the unsigned 12×24 vertex–edge incidence matrix of G. Its line graph joins exactly those directed pairs with equal first or equal second face label. Then

`B = 10 I₂₄ + Cᵀ C`.

Indeed `CᵀC` has diagonal entries 2 and off-diagonal 1 precisely at shared endpoints, hence B has diagonal12 and exactly the legal six incident turns as its neighbors.

The six-face adjacency matrix of the octahedral graph is `O=J₆−I₆−P`, where P swaps each opposite-face pair. Its spectrum is `{4¹,0³,(-2)²}`. As G is its bipartite double cover,

`C Cᵀ = 4 I₁₂ + [[0,O],[O,0]]`,

and its eigenvalues are `{8¹,6²,4⁶,2²,0¹}`. The 24×24 `CᵀC` has these eleven nonzero eigenvalues and thirteen zero eigenvalues. Therefore **exactly**

`spec(B)={18¹,16²,14⁶,12²,10¹³}`.

Automorphisms of the octahedral graph act transitively on all 24 directed adjacent face pairs and induce automorphisms of B, hence each diagonal entry of B^t is equal to `tr(B^t)/24`. For any natural t≥0,

`R_t=(B^t)_{xx} = (18^t + 2·16^t + 6·14^t + 2·12^t + 13·10^t)/24`, for **all** x.

All eigenvalues of B are positive, so B^t is a positive semidefinite symmetric matrix for any t. By Cauchy–Schwarz in its Gram factorization,

`(B^t)_{xy}² ≤ (B^t)_{xx}(B^t)_{yy}=R_t²`.

All entries count action words and are nonnegative, so **the largest length-t endpoint fiber equals the return-to-source fiber R_t** for every t and every source. We obtain an exact formula for the minimum worst-case fixed auxiliary action-history log:

`b_t = ceil(log₂ R_t)`;  `b_0=0, b_1=4, b_2=8, b_3=11, b_4=15, b_5=19, b_8=31`.

This explains the prior `R_4=26584` from structural algebra rather than one-time enumeration. A separate 24-state physical move simulation verified `B=10I+CᵀC` on ALL 24×18 moves and tested equality to the spectral formula for t0..12, without using numerical eigensolvers to prove the identity.

## Theorem D. Exact spectral rate of historical-information loss
Put `P=B/18`. P is symmetric, row-stochastic, irreducible (octahedron double-cover line graph is connected) and aperiodic (12 self-loops at each state). Thus for any source state x, the endpoint distribution converges to uniform on 24 coordinates. Its nontrivial eigenvalues are `8/9` twice, `7/9` six times, `2/3` twice and `5/9` thirteen times.

By vertex transitivity and symmetry, its exact chi-squared divergence from the 24-uniform law after t steps is

`χ²(p_t||u)= 2(8/9)^(2t)+6(7/9)^(2t)+2(2/3)^(2t)+13(5/9)^(2t)`.

The order-2 Rényi relative entropy bound implies

`0 ≤ log₂24−H(Y_t) ≤ log₂(1+χ²(p_t||u))`.

Together with Theorem B,

`H(W_t|Y_t)=t log₂18 − log₂24 + Δ_t`, where `0 ≤ Δ_t ≤ log₂(1+χ²(p_t||u))`.

Thus the *rate* of lost historical-word information is asymptotically `log₂18` bits per action, with a finite-endpoint observation offset tending to only `log₂24`. This is information for **uniform independent HTM action tokens and only the final single-edge coordinate**; not a bound on humans, on a complete cube state, on a remembered word or on other observation channels.

## Exact source contract and paper novelty
Theorems A–B and spectral mixing inequalities are standard general mathematical mechanisms; the new cube-specific contribution is the explicit identification of its orientation-state action multigraph with the line graph of the octahedral bipartite double-cover and the closed **all-length** action-word multiplicity and information-rate formulas. The earlier P7 results `diagnosis=8`, `physical reset=10`, 25≤M*≤34 stay separate complete finite-search results. The user’s original cognitive intuition remains unproved as an empirical statement.