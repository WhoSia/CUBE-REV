# CUBE-REV 0.28-R14-P6.1 — A Complete 648-State Adaptive Paired-Color Decision Tree

**Date:** 2026-11-06. **Verdict:** Exact full-model finite case (3 edges + 3 corners), both lower and upper certificates re-executable. **Not** the full 3×3×3 legal cube 20-frame problem; its unresolved bound remains `18<=h_adaptive<=21`.

## 1. Explicit miniature model, not a heuristic sample

There are 3 edge source labels (`UR`,`UF`,`UL`) with 2 cyclic orientations and 3 corner labels (`URF`,`UFL`,`ULB`) with 3 cyclic orientations. Each sector contains all permutations of its three cubie types, restricted to orientation sum 0. Two complete sector assignments may be paired iff their permutation parities match. The legal coupled state count is

    (3! * 2^2)*(3! * 3^2)/2 = 648.

A query is any `(i,j)` with `i∈{0,…,5}` one spatial edge facelet and `j∈{0,…,8}` one spatial corner facelet. There are exactly `6*9=54` allowed queries. It returns the two literal six-color sticker values, without revealing original cubie identity or orientation directly. Every observation query is free to choose from the spatial slots, with no routing cost in this abstract miniature problem. Corner labels are cyclic abstract words rather than independently lifted P48 chirality; the model is declared exactly and is not silently equated with the full physical cube.

## 2. Exact zero-error minimax and witness replay

For a belief bitmask B of the 648 explicitly enumerated legal states and integer budget k, use the exact AND–OR formula

    Win(B,k) = (|B|=1) or
               (k>0 and exists one of all 54 paired queries q such that
                  every nonempty 2-color observation child B_(q,y)
                  satisfies Win(B_(q,y),k-1)).

The program constructs all 54 query-output bitsets **directly from all 648 complete states**, memoizes the recurrence without heuristic equivalence merging, and evaluates at the full prior.

    Win(full,2)=False;
    Win(full,3)=False;
    Win(full,4)=True.

Thus the **exact worst-case zero-error adaptive horizon of this particular miniature model is 4**.

For the positive witness it recursively materializes a complete query/6-color-branch decision tree and **replays the tree on every one of the 648 legal complete states**. All 648 executions terminate in the leaf containing exactly the correct original state, within four observations. The distribution of realized depths in the exhibited policy is 24 states at depth 3 and 624 states at depth 4. The evidence receipt contains the complete executable policy tree, including every query index and every observed-color transition, not just total counts. The tree has 963 nodes including leaves; those counts are *certificate sizes*, not a claim of mathematical originality.

For the negative witness, the script checks all 54 possible first query choices. For **each one**, it records at least one nonempty literal color response child whose exact remaining two-query minimax value is false. The receipt preserves 54 root obstruction entries. These are witnesses to the universal quantification over the first move, supported by an exact memoized enumeration of all future query choices—not a mere failure of a single heuristic solver. The complete mathematical proof is finite exhaustive search over 648 legal states; the Python script is the replayable proof certificate.

## 3. Link to P6 and why it matters

R14-P6 had already established exact parity-factored symbolic successor counting and tested 464 partial histories against full-state enumeration. **P6.1 integrates the same observation model into an end-to-end Bellman/AND–OR optimizer** without assuming that equal posterior sizes imply policy equivalence. This supplies a reference solver to test future full-P48 matching-constraint canonicalization; any accelerated solver should be compared to P6.1 on every reachable small belief, preserving both its exact Win(B,k) values and a reconstructed query policy.

The miniature provides a concrete positive and negative certificate in one complete finite case. Its 4-frame optimum has no immediate implication for the full 12-edge/8-corner Rubik group. In particular, a constant-factor extrapolation from 3+3 to 12+8 would be invalid.

## 4. Next promotion gate

1. Use this solver as an independent **oracle** for testing canonicalization of actual symbolic partial-color matching constraints (not just query-location stabilizer orbits).
2. Verify that each canonical equivalence transports the **full** color-result partition and that inverse transformations reproduce the originally indexed query policy.
3. Reject unsafe merges that merely share population size or sorted branch-size profile. Include the 108-candidate alias discovered in P6 as a negative test.
4. Transfer the exact same interface (not the 648 bitmask implementation) to full 12-edge/8-corner parity-constrained matching DP; use safe lower bounds and P5.4 stabilizer action orbits to reduce choices, but do not announce a full depth-20 conclusion until an independently replayable universal witness or universal adversarial obstruction is constructed.

## 5. Evidence and custody

- Executable **standalone** pure-Python proof: `scripts/cuberev-observation/audit_r14_p61_micro_exact_minimax_decision_tree.py`.
- Exact JSON certificate: `R14_P61_EXACT_648_STATE_MINIMAX_4_AND_NO3_PASS`, including 54 root query obstruction branches and the full 963-node positive policy tree.
- GitHub commit identifiers / raw Drive links / hashes recorded after upload.
- Source-independent physical P48 coordinates are not tested by this program; the point here is an exhaustive finite Bellman optimizer and decoder replay on a different, fully declared model.
- Remote CI PASS is a separate gate, never inferred from local execution.
