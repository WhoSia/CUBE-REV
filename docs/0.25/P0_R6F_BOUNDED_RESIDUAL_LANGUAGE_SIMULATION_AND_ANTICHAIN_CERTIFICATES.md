# CUBE-REV 0.25 P0-R6F — Depth-Bounded Residual-Language Simulation, Antichain Proof Reuse and Canonical Context

**Evidence state: source and mathematical theorem submitted; new Lean4 kernel SUCCESS must be separately read from the actual Actions log. Original WCA 3×3 distance 15<=d18(s)<=18 remains the last completed physical result (R6B #38518179172). Source B9 versus goal B6 original physical lower16 trial #38520307408 is still IN_PROGRESS at the most recent status check.**

## Pure TCS advance

Previous R6E Lean4 project proved common ordered-word projection language inclusion and exact residual-language equivalence for proof reuse. Exact equality is a stronger condition than needed to justify sharing a negative certificate. For a deterministic automaton state x (which must include its corner, edge and canonical-normal-form DFA context), let

    R_k(x) = {w in A* : |w|<=k and accept(delta*(x,w))}.

This is an accepted SUFFIX-WORD language for the SAME ordered generator alphabet in all projections. Define a depth-bounded simulation PREORDER x >=_k y iff R_k(y) is a subset of R_k(x). The direction is essential: if state x is certified to have NO accepted suffixes and all suffixes possibly accepted from y would also be accepted from x, y is also empty and safe to prune. Do not reverse the direction. This does not mean that fully empty languages constitute a larger set under inclusion than equality. Rather the required PROOF OBLIGATION can be one-sided and potentially cheaper than establishing equality of arbitrary residual languages in advance.

For any deterministic total action transition delta and acceptance predicate, a short exact characteristic theorem holds:

    x >=_(k+1) y  IFF
      (accept(y) => accept(x))
      AND (for all a in A, delta(x,a) >=_k delta(y,a)).

Proof: any possible accepted word of length <=k+1 is either empty or begins with one and the same actual first symbol a and continues with length <=k. Forward direction restricts to the empty word and words a::tail. Reverse direction reconstructs all words by exhaustive case division. No commutativity or exchange of unlike words is assumed. This is mathematically the exact recursive justification for checking/caching bounded simulation of product-automaton residual languages. Reflexivity, transitivity, downward budget monotonicity, common-next-action preservation and sound transfer of negative certificates follow.

The actual source normal form forbids adjacent same faces and one orientation of commuting opposite faces. The search state must therefore include its last-face/axis normal-form DFA context or an equivalent total dead-state transition. Comparing only two cubie projections while silently changing allowed continuation grammars would be unsound.

## Machine-checked versus unverified scope

[Lean4 bounded residual theorem](../../formal/025/BoundedResidualDominance.lean) provides six separate theorems covering preorder reflexivity, transitivity, negative certificate transfer, ordered-action successor congruence, depth-budget restriction and the exact recursive IFF. [Isolated read-only Lean4 workflow](../../.github/workflows/cuberev-025-P0-R6F-lean-residual-dominance.yml) is an independent fast kernel gate. The previous [P0-R6E Lean4 canonical matrix and projected language workflow #38520778258](https://github.com/WhoSia/CUBE-REV/actions/runs/38520778258) had completed SUCCESS and does NOT by itself certify this newly added R6F file.

The generic theorem is conditional on honest full-to-quotient homomorphisms and the canonical language defined by the product-state context. It neither proves the entire original 54-facelet physical transition tables in Lean nor produces a complete B9/source versus B6/goal no-intersection certificate. When applied to the Rubik original cube, an empty COMMON corner-edge accepted language is a necessary-condition exclusion, but one nonempty accepted word still requires full CP/CO/EP/EO equality to establish a true physical intersection.

## Research applications and falsifiable costs

A safe negative antichain cache record must carry a verified state scope (including canonical last face), remaining word budget, exact projected acceptance semantics, verified emptiness of its residual language, and a certified simulation or inclusion relation for any reused state. Merely sharing a heuristic number, a corner PDB distance or an edge PDB distance is not enough to establish inclusion. A longer certificate can refute a shorter budget only when the budget and relation direction are correct.

The two-class source-grammar recurrence from R6E has characteristic equation c_(n+2)=12c_(n+1)+18c_n and proves the unpruned source-normal-form word counts. That recurrence by itself does not imply that a guessed antichain saves CPU or RAM. It gives a finite proof-call population against which one could compare a new certified cache. The cost of relation computation and cache construction must be included in wall/RSS benchmarks. If simulation checks cost more than the eliminated physical successors, that is a valid research negative result.

R6E's real physical #38520307471 same-runner D/E comparison recorded 19.29 s versus 18.80 s, preserving exact source complete B7 call counts; a one-run 2.54% change is not a universal performance theorem. A newly developed cache must preserve EXACT source/goal physical soundness, identical original move semantics, no projected false negatives, and all source-normal-form recursive call ledgers.

**Proof frontier:** preserve source-specific 15<=d18(s)<=18 until an independently audited completed B9/B6 physical no-intersection (or a shorter true 15-move solution). No bot authors/committers; Actions contents:read, no writes; protect private 451 human cases.
