# CUBE-REV 0.28 R14-P6 — Exact Mixed-Color Belief Factorization and Successor Branch Court

**Date:** 2026-11-06. **Status:** symbolic factorization PROVED; independent small-model full-state enumeration and full-P48 parity-matching count verification LOCAL PASS. **Not** a full canonical quotient, a global 20-frame strategy, or a universal 21-frame adversary.

## 1. Original observation and legal-state model

Let `G` be the legal fixed-centre cube group, with 12 edge types, 8 corner types, exactly one six-color sticker result from a spatial edge facelet and one from a spatial corner facelet per frame. Legal rotations are known, arbitrary physical routing is permitted at no cost in the objective. All spatial queries are translated back to initial-spatial slot IDs; this translation requires known legal turns and is independent of hidden configuration.

For a partial transcript H, write `R_E(H)` and `R_C(H)` for the *literal* observed slot/color constraints in the two sectors. A constraint is `slot: six-color`. Duplicate observations of the same color are idempotent; contradictory observations have no compatible state.

Define `E_p(H)` as the complete set of oriented bijections of edge cubie labels onto 12 initial-spatial edge positions that satisfy **all** edge-color constraints, have total edge flip zero modulo two, and have permutation sign p. Define `C_p(H)` for eight corners with twist sum zero modulo three and permutation sign p.

## 2. Exact coupled-parity factorization lemma

The fundamental legality constraints imply

    B(H) = (E_0(H) × C_0(H)) ⊔ (E_1(H) × C_1(H)).

The union is disjoint. Every pair drawn from the matching sign class is a legal complete Rubik configuration (fundamental theorem of cubology); mismatched signs are illegal. No other cross-sector coupling exists in this idealized model. Thus

    |B(H)| = Σ_{p∈{0,1}} |E_p(H)| |C_p(H)|.

For any future paired spatial query q=(i,j) and ordered color output y=(a,b), the posterior is *exactly*

    B(H;q,y) = ⊔_{p=0,1} E_p(H∪{i↦a}) × C_p(H∪{j↦b}),

and

    |B(H;q,y)|=Σ_p |E_p(H∪{i↦a})| |C_p(H∪{j↦b})|.

Because each complete cube state yields precisely one color pair, the entire 36-outcome branch partition satisfies the exact conservation law

    Σ_{a,b∈F} |B(H;q,(a,b))|=|B(H)|.

This expression is **not merely a population approximation**: it gives a symbolic representation of each full successor belief as a union of explicitly defined parity-conditioned exact-matching constraint sets. However, a solver wishing to **merge two different** transcript descriptions still needs a mathematically valid history-preserving bijection (or proof they specify identical state sets), not equality of their cardinalities or branch-cardinality multisets.

## 3. Exact parity-matching dynamic programming

For a sector with n types of cyclic orientation arity r, each spatial cubie position i has allowed `(type label,orientation)` pairs consistent with all literal slot/color requirements. A DP state `(used_mask, permutation_sign, total_orientation_residue)` recursively assigns a distinct type to the next spatial position. Inserting label j after earlier labels contributes inversion parity equal to the number of *already assigned* labels larger than j; adding rotation t updates the orientation residue modulo r. At the terminal state count only zero total residue, separately by final permutation parity.

This DP evaluates the exact finite sets E_p(H), C_p(H) **without enumerating** the 43,252,003,274,489,856,000 full cube states. The query-response update simply adds a literal facelet-color requirement and calls the sector DPs. No assumption of independent edge/corner permutation sign is made; the two sign sectors are multiplied only on matching p.

## 4. Independent full-enumeration micro-court (648 states)

The new stdlib-only script implements its own 3-edge/3-corner complete legal-state enumerator: 3!×2² oriented edge sector states, 3!×3² oriented corner sector states; matching permutation signs yield `648` legal coupled states. It samples 464 distinct realized prefix constraint sets (up to three queries) generated from true states and compares exact parity-matching posterior counts with **actual full-state filtering**, then validates all **36 next color outcomes** under a next sampled query in the same way. All comparisons PASS.

### Negative control: population aliasing is demonstrably unsound

Two reachable beliefs in the micro-model each have exactly **108** candidates:

- Constraints A: edge local facelet 0 has color U, corner local facelet 0 has color U.
- Constraints B: edge local facelet 0 has color U, corner local facelet 4 has color U.

For the **same** next paired query of local facelets `(0,0)`, A produces the *single* next posterior of size `[108]`, whereas B produces nonempty child sizes `[12,12,24,24,36]`. The count 108 is identical yet the entire next-query color outcome partition differs. **This fixed-query counterexample rejects cardinality-only equivalence.** It does NOT by itself rule out a different query permutation connecting the two beliefs; that requires its own all-query isomorphism test. The negative control is therefore carefully scoped.

## 5. Full physical P48 cross-check

The script loads the existing **P5.1 physical 48-facelet geometric module** (declared dependency, *not* an independent second P48 geometry generation). It independently constructs its oriented edge/corner source-color words and evaluates all 12 second-query location orbit representatives after root `(q0,(U,U))` using its own matching DP. It reproduces

- Initial posterior after canonical root color pair: `1,201,444,535,402,496,000` states;
- All 12 initial stabilizer-orbit representatives' complete 36-color branch sums;
- Best one-step worst-surviving population: `41,608,468,758,528,000` states, for reading a new edge position and new corner position.

This independently corroborates the previous R14-P5.2 arithmetic, but the two computations share P5.1 geometry and hence are **not independent physical implementations**.

## 6. The actual new search interface and next proof gate

A correct exact zero-error belief search now has an explicit symbolic core:

    win(H,k) = (|B(H)|==1) OR
               (k>0 AND ∃ paired spatial query q:
                ∀ nonempty output y, win(H∪{q↦y},k-1)).

The recursion is mathematically complete but **not yet computationally feasible** at full 20-frame depth. Next, construct an exact canonical constraint signature under the verified left legal spatial and right source-color transformations; include the inverse action and inverse color map to replay the representative query on a real history. Use the subgroup stabilizer orbits (P5.4/P5.5) only when every previously queried slot is pointwise fixed. Test an exact micro-model AND/OR solver exhaustively and reject every false quotient that joins beliefs with different reachable future decision trees. In P48, integrate safe necessary lower bounds from the total matching count and high-difficulty restricted edge residual games. Keep identical-color but different spatial slot constraints distinct unless an explicit certified bijection transports both their **entire** future query-response structure.

## 7. Research OS, scope, and originality

This factorization follows classical legal cube parity constraints and standard finite constraint programming. The contribution is an *audited exact branch-aware interface*, not an invented generic theorem. The 648-state independent micro-court and full-P48 12-orbit second branch regression are the current evidence level. **The original unresolved adaptive horizon remains 18≤h_adaptive≤21.** A failure to search through horizon 20 is not a mathematical lower bound.

- Source: `scripts/cuberev-observation/audit_r14_p6_symbolic_belief_branch_court.py`.
- First execution: `R14_P6_EXACT_SYMBOLIC_BELIEF_BRANCH_COURT_PASS`.
- Source and execution receipt originals: Google Drive immutable raw file URLs recorded separately after upload; SHA-256 must be verified by Drive raw-byte readback.
- Related: `docs/0.28/20261106_R14_P54_MIXED_PREFIX_STABILIZER_ORBITS.md` and `docs/0.28/20261106_R14_P55_PARITY_COUPLED_FAMILY_ORBIT_THEOREM.md`.
