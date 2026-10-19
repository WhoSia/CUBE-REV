# CUBE-REV 0.27 — P13 Rewind: One Radius-17 Court and One-Sided Goal-Superset Certificates

**Date:** 2026-10-19. **One original physical radius-10 negative certificate ACTUALLY verified. Original radius-17 negative certificate NOT YET computed.** We have a third-party solver-backed 18HTM result, but do not upgrade it to unconditional independent no17 on the strength of this small prototype.

## Rewind theorem — replace separate ≤16 and ≤17 courts with one
Let `B_r(x)` be the full physical HTM ball of radius r. For a true original source `s` and solved `e` in the unit-cost undirected Rubik move graph,
```
d(s,e) <= 17   IFF   B_10(s) ∩ B_7(e) != ∅.
```
Splitting and concatenating actual legal paths proves this for **all shorter lengths as well**. A single independently checked no-intersection certificate plus the existing physically replayed 18-turn solution proves `d(s,e)=18`; unlike the historical phased research, no separate ≤16 search is logically necessary for this self-contained replacement.

## Core simplification: negative membership needs ONLY one-sided goal coverage
Fix any deterministic state fingerprint H (it need not be collision-free, secret, or cryptographic). An **untrusted** sorted fingerprint set F is sufficient if a small verifier establishes:
1. For every full physical state g in the complete exact solved B6 and for each of 18 moves a, `H(g)` and `H(g*a)` belong to F. This proves `H(B7)⊆F`.
2. For every original source state x reachable in ≤10 HTM moves, `H(x)∉F`.

Then `B10(s)∩B7(e)=∅` **deterministically, with no collision-resistance hypothesis**. Collisions or deliberately inserted spurious fingerprints can produce only **false positives**, which must be resolved or cause certification HOLD. They can never induce false negatives *after exhaustive coverage verification*. There is no need to trust the filter builder or a giant external phase1x24 PDB. Source-side pruning, if any, must still carry independent one-sided admissibility certificates; a full physical source enumeration avoids that assumption but may be expensive.

## Real complete local rehearsal on original WCA instance: B5(s) versus B5(e)
Actual independent C++17 executables `build_goal_b5_filter.cpp` and `verify_rewind_one_sided_b5.cpp` use the authentic original P11 `P[18][54]` geometry and 54 original distinct sticker labels. The original 20HTM WCA scramble and genuine 18HTM completing word are replayed and checked on all 54 labels in BOTH programs. Actual *exact-equality* BFS deduplicates physical 54-byte states (hash collisions cannot delete BFS states).

- Builder separately enumerated exact solved B5 shell census 1,18,243,3240,43239,574908 = **621649** full physical states. Output **621649 sorted unsigned 64-bit FNV fingerprints, 4,973,192 bytes** (all unique in this experiment).
- Separate verifier reads that untrusted file, independently enumerates solved exact B4 = **46,741** physical states, and checks **46,741×19=888,079** goal containment obligations (each B4 and its 18 neighbors). PASS. This establishes coverage of true solved B5 independently of the builder.
- Separate verifier independently enumerates exact original source B5 = **621,649** physical states and checks all fingerprints **absent**. Actual **0 positive hits**, PASS. Concludes the genuine limited theorem `d18(original_WCA_scramble) > 10`, not >17. This is a complete, independent *one-stage* physical proof-of-concept, with no third-party RubikOptimal and no normal-form DFA trust.
- Real native wall time builder **0.62s** peak **104,812KiB**, verifier **1.07s** peak **112,264KiB**. Timings are local-run observations, not promised for full 17.
- Mutation tests: delete one required goal fingerprint => **REJECT** `MISSING_GOAL_B4_NEIGHBOR_FROM_FILTER`; corrupt sort order => **REJECT**; insert an extra unneeded fingerprint not in source visited states => **PASS**, demonstrating permitted one-sided false-positive superset semantics.

The local 14-file source+filter+logs+sha portable ZIP **4,724,630 bytes SHA256 `5ae352798c887c9278676a05272787a4bff7f45acdf4e6793345d021a7947cec`**. The exact raw bytes were uploaded to existing Drive `10_CANONICAL_PROOF_COURTS`, file ID `1QRzzrnweM51cpsZRVYNIUl91Szdj418n`, [verified Drive artifact](https://drive.google.com/file/d/1QRzzrnweM51cpsZRVYNIUl91Szdj418n/view), then authenticated-downloaded and compared to original **BYTE-FOR-BYTE and SHA256 PASS**. This is P13 T2 BYTE_VERIFIED only for the little B5+B5 rehearsal, NOT for a global 17 certificate.

## Exact full-radius target and resource reality
Published exact physical HTM ball cardinality to depth 7 is **109,043,123** states (OEIS A080601), giving **872,344,984 bytes ≈ 831.93 MiB** at one sorted uint64 fingerprint per physical state. The independently pinned full solved B6 already contains 8,240,087 exact states. One-sided goal-coverage verification requires **8,240,087×19=156,561,653** hash containments, not full independent enumeration of a B7 BFS. Reaching B7 from B6 takes at most 8,240,087×18 physical successor constructions; dedup+sort produces the filter. Source B10 has **264,501,924,112 canonical sequences of lengths ≤10** before any pruning (standard HTM canonical grammar; not number of distinct states). This search is still substantial and may suffer weaker early C8 pruning when the goal radius increases from 6 to7. **No speedup or feasible overall wall time is claimed without a measured physical pilot.**

Other possible radii include B9(s)+B8(e), trading a much larger >11GB goal fingerprint table against shallower source exploration. Actual measured throughput, sound pruning, memory, collision-triggered inconclusive leaves, indexing, and independent all-root coverage must decide. One can use any deterministic filter with stronger indexing, but all actual source positives must remain explicit HOLD or undergo exact physical disambiguation. Old C++/Go ≤16 soundly pruned branches cannot simply be reused for ≤17: old C8 cutoffs were narrower and unsafe for a longer target.

## Scientific positioning
This is a promising *proof-carrier engineering pattern*, not invention of bidirectional Rubik solving or Bloom/fingerprint filters. Cf. [Rokicki Nxopt double-ended search description](https://github.com/rokicki/cube20src/blob/master/nxopt.md), [Korf optimal Rubik PDB](https://www.aaai.org/Papers/AAAI/1997/AAAI97-109.pdf), and standard HTM layer counts [OEIS A080601](https://oeis.org/A080601). Novelty, if any, must be demonstrated by a complete source-fixed 17 rejection, public independent checker, transparent trust boundaries, and real certificate/CPU comparison.

**P13 next:** build a resumable true physical B7 64-bit fingerprint producer from independent B6, an independent 156.56-million-check goal coverage verifier, and a **small selected source-depth10 court pilot** to measure lookup throughput and candidate positives before full proof expansion. Continue separate upstream heuristic certification only if needed for performance; keep solver-backed optimum18 distinct from independently proof-carrying exact18.
