# CUBE-REV 0.25 P0-R6H — Graded Prefix Refutation and Rational Normal-Form Languages: Canonical DFA Coverage, Action-Word Proof Algebra, Weighted Cylinders & Source-Complete Certificate Composition

**Research state:** mathematical Lean4 proof of the new generic bounded prefix-refutation equivalence completed GitHub Actions SUCCESS [#38524938289](https://github.com/WhoSia/CUBE-REV/actions/runs/38524938289), 13 build jobs. The newly extended all-depth transfer recurrence and low/high coefficient Lean source must receive its own next kernel confirmation. The completed original physical WCA cube B9/B6 certificate independently established **16≤d18(s)≤18** at [#38520307408](https://github.com/WhoSia/CUBE-REV/actions/runs/38520307408). A true source B10/B6 full intersection or no-intersection search of ALL canonical words has NOT completed. The one-high-class action D B10 physical pilot [#38524132916](https://github.com/WhoSia/CUBE-REV/actions/runs/38524132916) has COMPLETED SUCCESS and independent Go audit: one source-first-D cylinder, exactly 14,279,876,542 accounted calls, 80,144,176 visits, 14,199,732,366 safely skipped, full target hits zero; wall 561.99s, peak RSS 1,341,156 KiB. The global lower17 is NOT proven.

## 1. Mathematical question: how can finite computation become composable mathematical proof?

A bare set of 18 successful job logs does not constitute a global shortest-path proof unless the actual language of every possible legal original action word is exhausted without overlap gaps. Represent a search node not merely as a cubie configuration s, but as a pair (s,q), where q is the last-move/context state of the canonical normal-form DFA. Let S be the physical group action space, A be the actual original 18 HTM generator alphabet, delta:S×A→S the noncommutative original physical transition, Q the DFA state space, tau:Q×A→Q and Allowed(q,a) the locally legal canonical action language, and T⊆S the exact full cubie B6(solved) target.

Define F_k(s,q) to mean **every DFA-admissible ordered suffix word of length at most k from (s,q) misses T**. This has an exact, finite recursive interpretation:

    F_0(s,q) <=> s not-in T

    F_(k+1)(s,q) <=>
       (s not-in T) AND
       (for ALL a with Allowed(q,a):
            F_k(delta(s,a),tau(q,a))).

The second line is a **universal branching** law. It is independent of heuristic style or whether s has an easy corner/edge projection. An exact physically sound corner/edge language-exclusion theorem may discharge an entire subtree proof obligation at once, but doing so must establish the same universal absence condition. A missing branch, a wrong q, or a resource HOLD cannot close the proof.

A proof-producing DFS therefore returns not just a Boolean but a *typed witness* of a bounded negative language: an empty-word physical nonmembership receipt plus child absence certificates or separately kernel-validated sound subtree exclusions. An actual full-cubie intersection invalidates negative proof and must be reconstructed as a physical witness.

## 2. Lean formal theorem: exact proof-system soundness AND completeness

[PrefixRefutationCalculus.lean](../../formal/025/PrefixRefutationCalculus.lean) introduces:
- legalSuffix: the correct normal-form continuation language as a function of the DFA q, preserving noncommutative action order;
- PrefixRefutation: a graded inductive proof tree, whose base case is an exact current-state target exclusion and whose positive-depth case additionally requires proofs for **every grammar-admissible next action**;
- prefix_refutation_sound: such a complete tree excludes every legal action word of length ≤k;
- prefix_refutation_complete: every true bounded nonreachability property gives rise to such a tree (classically/unfolded as a proof object, not necessarily small);
- prefix_refutation_iff_bounded_absence: exact logical equivalence.

The [separate read-only Lean4 kernel workflow #38524938289](https://github.com/WhoSia/CUBE-REV/actions/runs/38524938289) actually completed SUCCESS, with **Build completed successfully (13 jobs)**. This is the precise mathematical bridge from a DFA-normalized exhaustive DFS to a graded no-reachability statement. It DOES NOT verify the real cube's C++ implementation, entire original B10 enumeration, or actual physical 54-sticker transition tables inside Lean.

The proof uses an actual normal-form DFA state q in addition to s and never asserts that independent corner-success and edge-success words may be replaced by the same word. In combination with [ProjectionWordLanguage.lean](../../formal/025/ProjectionWordLanguage.lean) and [BoundedResidualDominance.lean](../../formal/025/BoundedResidualDominance.lean), it separates (i) ordered projection language inclusion, (ii) valid bounded refutation composition, and (iii) proof-cache reuse by one-sided right-language simulation.

## 3. A compact rational generating function — exact beauty of the canonical grammar

The original 18HTM normal form has three powers per face and six faces in order U,R,F,D,L,B. Equal consecutive faces are prohibited, and commuting opposite faces are only retained in ascending face order. By symmetry of the three opposite axes, the six possible terminal faces collapse for COUNTING into two classes: lower indexed faces {U,R,F} and higher indexed faces {D,L,B}, with transfer

    [L_(n+1)]   [6 6] [L_n]
    [H_(n+1)] = [9 6] [H_n].

The characteristic polynomial is t²−12t−18, and hence any future-total counts from either class satisfy c_(n+2)=12 c_(n+1)+18 c_n. The just-added [CanonicalTransfer.lean](../../formal/025/CanonicalTransfer.lean) theorem all_depth_canonical_transfer_recurrence formalizes this for EVERY remaining depth and ANY initial state pair; its later actual Lean CI must be separately inspected.

Now define G_low(z) as the ordinary generating function for normal-form words starting with ONE PARTICULAR low-index original physical first action, and G_high(z) analogously for one fixed high-index first action, counting total word length from the root, so the first coefficient is z. Their initial coefficients and their shared characteristic recurrence yield EXACT closed rational series:

    D(z) = 1 − 12z − 18z²

    G_low(z)  = z(1 + 3z) / D(z)
    G_high(z) = z / D(z).

The whole legal canonical word language (including the empty word) has exactly nine of each first-generator type:

    C(z) = 1 + 9 G_low(z) + 9 G_high(z)
         = (1 + 6z + 9z²) / (1 − 12z − 18z²).

These are *word-count* generating functions, NOT generating functions for distinct physical Rubik group elements. The original source canonical iteratively deepened recursive-call budget through R is the weighted coefficient sum

    N_R = ∑_(n=0)^R (R−n+1) [z^n] C(z).

It can be verified independently by 18-letter DFA dynamic programming and the two-state transfer matrix. For R=10 the result is exactly 285,921,738,920 repeated recursive calls before mathematically proven pruning.

## 4. An elegant exact asymptotic: sqrt(3/2) class imbalance

D(z) has positive dominant growth root λ=6+3sqrt(6). The same simple positive pole controls both low/high first-action generating functions; therefore their coefficient ratio approaches

    lim_(n→∞) ([z^n]G_low / [z^n]G_high)
        = 1+3/λ
        = sqrt(3/2) ≈ 1.22474487139.

The same limit holds for cumulative iteratively repeated first-action shard-call counts, because both are dominated by the same exponentially growing mode. The direct exactly enumerated B10 first-action shard sizes already have ratio

    17,489,205,559 / 14,279,876,542 ≈ 1.224744871397.

This algebra explains why naive 18-equal-budget scheduling is imbalanced by about 22.47% in the **unpruned language-call population**. It does NOT predict the same ratio in wall/RSS for physical Rubik cube shards: actual projected prune rates and source-dependent full cubie geometry also matter. The asymptotic generating-function formula is established by standard rational-series algebra conditional on the already verified canonical transfer; the real-field asymptotic limit itself is not separately claimed as a Lean4 kernel theorem.

## 5. Source proof cuts as weighted language cylinders

For any prefix-free frontier P in the canonical action language, let Cyl(p)={p·w : p·w is canonical}. A source-complete proof requires EVERY relevant canonical word either to be shorter than its first encountered frontier cut or to belong to EXACTLY ONE cylinder for p∈P. The key source proof condition is an **exact weighted cylinder partition**, not merely that the number of jobs is large:

    total source DFA word-call population
      = short/frontier-internal calls
        + Σ_(p∈P) calls in the completed suffix language under p.

For the already physically verified first-letter frontier P=A, the internal contribution is R+1 repeated root calls and the 18 cylinders are disjoint because every nonempty word has a unique first generator. This yielded the exact independently Go/Lean verified B10 identity

    285,921,738,920
      = 11 + 9(17,489,205,559) + 9(14,279,876,542).

Variable-depth prefix code cutsets are a promising way to balance genuinely measured source-shard costs; a proposed cutset must itself carry a verified unique decomposition and exact DFA-count weight before accepted.

## 6. Actual original cube proof frontier and resource policy

R6G [real physical B6/B7 18-first-action regression #38523511353](https://github.com/WhoSia/CUBE-REV/actions/runs/38523511353) completed all shards with independent Go and 4,608 full-versus-packed physical turn cases: 120,213,368 unpruned complete source calls = 674,715 visited + 119,538,653 soundly skipped, zero actual full-cubie collisions. This establishes the first-letter *method* for the ORIGINAL cube to radius7; not yet the B10 proof.

The cost-gated one-high-class first-D-move [B10 pilot #38524132916](https://github.com/WhoSia/CUBE-REV/actions/runs/38524132916) passed its B3/B3 physical/Go preflight, but its one B10 source shard job had not yet completed at last query. A completed original one-shard receipt may certify only that action's exact source language; **global lower17 would require all 18 action shards, the checked root and an independently validated union with zero missing/gapped prefixes**. If a complete original physical B10 source word meets the complete B6 solved goal, preserve the witness and independently replay rather than incorrectly claiming disjointness.

**Cost policy:** do not initiate 17 further expensive B10 runs based on an unmeasured mathematical asymptotic. Use the actual one-shard hardware cost, observed safe pruning fraction and peak RSS to decide whether further sharding, stronger sound language-automata exclusion, or a different verified physical search architecture is needed.

**Governance:** full physical C++17, independent Go source accounting, Lean4 general TCS; WhoSia author+committer only, read-only Actions, no bot contributions, source privacy of 451 human reconstructions maintained.


## Final external verification of the all-depth transfer theorem

[Lean4 normal-form theorem Actions #38525117311](https://github.com/WhoSia/CUBE-REV/actions/runs/38525117311) completed SUCCESS and the actual job reported **Build completed successfully (13 jobs)**. The added all-depth canonical transfer recurrence theorem applies to ANY initial two-class pair and any finite remaining depth. The low-first (1,15,198) and high-first (1,12,162) initial coefficients are kernel-verified as well. Thus the coefficientwise rational identities derived from the transfer are uniquely fixed: G_low(z)=z(1+3z)/(1−12z−18z²), G_high(z)=z/(1−12z−18z²), and whole canonical language C(z)=(1+6z+9z²)/(1−12z−18z²). The analytic asymptotic low/high ratio sqrt(3/2) is derived mathematically from the simple dominant root; this real-limit argument is NOT claimed to be a separate Lean theorem.

[Second actual bounded B10 first-low U source pilot #38525480526](https://github.com/WhoSia/CUBE-REV/actions/runs/38525480526) has been submitted with independent Go per-shard receipt, cost cap, full 54-sticker physics, and strict NOT GLOBAL labels to calibrate the other canonical source class. At this update its entire physical B10 result is not yet verified. Neither a single low and a single high completed shard, nor a rational generating series, can prove the remaining 16 first-action B10 cylinders empty.
