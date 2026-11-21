# CUBE-REV 0.29 AS24 — Finite-statewise response quantifiers and exact-length terminal parity scheduling

**2026-11-21.** A scientific proof note for the nineteen-frame upper-bound compiler. This document distinguishes (i) a generic theorem about finite candidate sectors, (ii) its instantiation for the immutable 52 policy roots, and (iii) the timing of the last physical corner observation. Only (i) is formalized by the new modules at the time of writing; (ii) and (iii)'s complete cube-specific glue are still open.

## 1. Exact reduction from answer quantification to candidate quantification

Let (B) be a *list* of concrete oriented-edge candidate states, (O(s,q)) their categorical sticker observation, and (B_{q,r}=\{s\in B:O(s,q)=r\}\). A finite decision-tree checker needs to verify that the child indexed by (r\) has the correct posterior whenever (r\) can occur.

The original semantic specification in `SectorSemanticCompiler.lean` quantifies over every reply (r\in R\), requiring validation only when (B_{q,r}\ne\varnothing\). The new `SectorStatewiseValidity.lean` expresses the same premise as
[
 \forall s\in B,\quad
 \mathrm{Valid}(\mathrm{child}(O(s,q)), B_{q,O(s,q)},k-1).
\tag{1.1}
]

**Theorem AS.1.** For every finite candidate list, every well-typed policy instruction array, every integer budget and every observation function,
[
 \mathrm{SemanticallyValidSector}(G,O,\sigma,k,i,B)
\iff
 \mathrm{StatewiseSectorValid}(G,O,\sigma,k,i,B).
\tag{1.2}
]

*Proof.* Induct on the remaining read budget. Both specifications agree at an absent node, at a leaf (at most one candidate per parity) and at a padding node (recurse with an unchanged belief). At a read node, the forward implication in (1.2) takes (r=O(s,q)\) for each (s\in B\), which is feasible with witness (s\). Conversely, for any feasible reply (r\), choose the witness (s\in B\) that makes (O(s,q)=r\), then apply the statewise premise. The recursive child and filtered candidate list are literally the same, so the induction hypothesis transports validity in both directions. □

**Consequent soundness.** Composing (1.2) with `valid_sector_compilation_recovers_each_candidate` proves that a statewise-checked sector policy, when run on any of its initial candidates, produces a sign-indexed terminal decoder which returns that exact candidate when supplied the candidate's true sign. No uncontrolled response alphabet size remains in the checker: one may check *at most the feasible candidate-generated responses*, merging repeated replies under caching.

**Open instance:** neither (1.2) nor that soundness composition asserts `StatewiseSectorValid` for the actual frozen 52 roots. A verified executable checker or a proof relating the old `NineteenReadData.verifyNode` to `StatewiseSectorValid` must discharge this exact premise, using the original pinned JSON bytes and `NineteenReadData.sector` representative candidates.

## 2. Why “at most eight reads” does not supply the nineteenth corner color

In the frozen upper design, eleven initial paired frames read eleven first edge colors together with eleven scheduled corner stickers; the remaining eight frames contain the continuation edge reads together with **eight more scheduled corner probes**. The final necessary new corner sticker is at **frame 19**, and together with the other thirteen distinct corner colors it yields all 24 original corner colors by the separate parity/twist conservation argument.

The generic `FrozenPolicyInterpreter.lean` and `compileSectorDecoder` can legally stop early at a leaf, since `Fits 8` is only an *upper bound*. If we compose such an early-stop edge policy naïvely with the corner observation schedule, fewer than nineteen physical corner replies may be obtained. Passing the terminal corner sign in that situation would silently create an information oracle. **This timing error cannot be fixed by saying that the mathematical policy still “has a budget of eight”.**

## 3. Exact-length padding with genuine simultaneous observations

The module `ExactBudgetPadding.lean` defines an operation `Policy.padToExact fallback n` for a controller with a `Fits n` derivation:

- a nonterminal query remains the same, and its actual categorical reply selects the corresponding recursively padded branch;
- an early terminal is replaced with one **real** query to a known legal fallback address, whose reply is ignored, followed by further padding until the budget is exhausted;
- a terminal that is already at depth (n\) remains unchanged.

Theorem AS.2 proves the padding result still has `Fits n`. Theorem AS.3 proves its **output on every state is identical** to the original controller's output; the added answers carry no information to that controller. Theorem AS.4 proves the **ordered address/response transcript has length exactly (n\)**, not merely at most (n\), for every initial state.

This construction is mathematically separate from the corner schedule, but solves the missing physical time slots: after the first eleven paired frames, an eight-read padded edge policy can be paired with eight ordinary corner reads. The corner replies must still be collected and decoded by the actual physical compiler, and the sign chosen only **after** the nineteenth response. Padding therefore prevents *early termination* from skipping necessary corner observations without changing the upper edge policy's computed decoder.

## 4. Semantic-negative controls and strong boundaries

- **Fake success from a missing branch:** the typed parser uses an invalid node index for a missing reply. The semantic checker must reject a physically feasible branch sent there, though an infeasible reply need not have a valid child.
- **Fake parity oracle:** the terminal decoder is a function `Bool → Option Word`, not a tree that branches on an unobserved Bool. The Bool must be computed from physical corner observations before applying it.
- **Free padding:** a JSON `repeat` or an early leaf may not move the physical corner schedule forward without counting a simultaneous observation. The padding operation turns each unused frame into a genuine `Policy.read`.
- **Certificate-only accounting:** the old 52-tree receipt validates the frozen source structure and leaf counts, but full machine-checked upper correctness also requires a theorem connecting the same JSON to the new typed semantic checker and the corner/edge legal-state bridge.
- **Color-label symmetry versus physical rotation:** the 48 automorphisms of the six-color edge graph include maps not realizable as whole-cube rigid rotations; their signed coordinate maps are proof transformations, not free physical operations.

## 5. Research-director acceptance order

1. Complete pinned CI on `SectorStatewiseValidity` and `ExactBudgetPadding`. Their `#print axioms` must be inspected individually; earlier generic semantic modules compiled with only standard Lean logical axioms.
2. Define a *computable* statewise Boolean checker of the finite typed graphs and prove `checker = true ⇒ StatewiseSectorValid`. A small proof by induction on the read budget should suffice; it replaces large case-by-case Lean proof objects by one generic soundness theorem.
3. Evaluate this checker on exactly the pinned 52 representative JSON trees and candidate sectors, preferably with an independent native receipt and mutations; preserve and print the resulting `native_decide` trust dependency. Do not infer full policy correctness merely from candidate/leaf count totals.
4. Compose all ordered eleven-color normalization witnesses with the physical corner schedule, its nineteenth-frame sign release and the exact eight-read padded decoder, then discharge the final unconditional `Fits 19` theorem.

**Method reference custody:** [Knuth (1991), Combinatorica journal original](https://drive.google.com/file/d/1mIhQ-9tchQp-quRSkFyFF5AY0m1HTdaZ/view); [Furst–Hopcroft–Luks (1980), IEEE FOCS 36–41 original](https://drive.google.com/file/d/1AhZmbHGT_8RnIZ3D4OoSTdZK7aZLYvkF/view); [Babai (1981), Annals 113(3) original](https://drive.google.com/file/d/1PdBg2ByUtXQQ61k47DHHxPUQ4J0C1j4r/view). They motivate efficient group/certificate handling but do not themselves establish the paired-color Rubik upper theorem.
