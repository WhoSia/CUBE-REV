# CUBE-REV 0.19 — P13 Final: Exact Physical Five-Turn Dictionary Minimum Eight

**Evidence status: locally independently re-executed exact finite computer-assisted proof. External GitHub Actions success/Lean/VeriPB checking NOT YET ESTABLISHED.**

## Theorem, with exact quantifiers

On the original frozen 1,192 admitted 3-, 4-, and 5-element source subsets of twelve possible initially zero-flip positions of one tracked UR edge, each fixed nonadaptive experiment is a **legal five-HTM Rubik's Cube word** with an intrinsic edge-flip bit observed after each move. A word separates a source subset iff the five-bit transcripts of its members are pairwise distinct. Dictionary cost counts the **number of fixed experiments**. In this precise model:

\[\boxed{M^*(5)=8.}\]

### Positive bound: eight real five-move words

```text
F' B' L F B
F' B' R F B
F' B' D F B
F L2 B' D2 F
F U2 B R2 F
F' B' U F B
F B L F B
F B R F B
```

Independent replay from the frozen 18×24 sticker-derived physical edge transition maps finds partition rank 7 for every listed word, respective original-source coverage counts **553, 553, 553, 465, 465, 553, 553, 553**, and union of all eight covers **1,192/1,192** original admitted source sets. This is a constructive \(M^*(5)\le8\) certificate; it is *not* a sequence to solve the cube or distinguish all full-cube states.

### Negative bound: no seven experiments

1. **Five-source gate (P12):** Independently checked \(M^*_{\mathcal R_5}(5)=7\) for the original 480 admitted five-element sources. Hence any original-family <=7-word cover would consist of seven physically realized words with observation rank at least five; rank<=4 cannot separate any five-element source. Every selected word must have at least one private admitted five-source witness, because no six-word R5 cover exists.
2. **Rank-seven case split:** For a hypothetical seven-word full-family dictionary, let \(t\in\{0,\ldots,7\}\) be the number of words whose complete five-bit transcript induces exactly seven different output classes over the twelve initial edge slots. Original physical census contains exactly **2,295** distinct full-source coverage types of rank 5, **1,144** of rank 6 and **32** of rank 7. All rank-conditional checks retain the **raw original** rank5/rank6 physical coverage families, not the globally cross-rank-dominated reduced columns.
3. **\(t=0\):** A dictionary using only rank5/rank6 words needs a rank6 word (seven rank5 words cannot identify 480 five-state sources). Original physical source-incidence symmetry group of order 16 yields **74** first-rank6 word orbits. **65** are ruled out by positive original-row integer conditional duals satisfying \(W>6B\) for remaining source demand. The remaining **9** orbits are ruled out by complete exact integer bitset case branching, **5,082 nodes total**, after only valid dual-derived necessary candidate exclusions. The independently re-executed verifier checks all 74 representatives and all original word masks.
4. **\(t=1,2,3\):** Physical rank7 tuples form **3, 44, 327** symmetry orbits. For all **374** representatives, independent original-source nonnegative integer row weights certify residual demand \(W>(7-t)B\), where B is the largest residual weighted coverage attained by any actually physically realizable rank5/rank6 word. All 374 certificates were rechecked with integer arithmetic against **all 3,439 original rank5/rank6** physical cover types.
5. **\(t=4\):** Enumerate all \(\binom{32}{4}=35,960\) rank7 sets; the fully checked 16-element physical incidence group yields **2,361** distinct tuple orbits. For each representative, check whether any **three** real rank5/rank6 experiments can cover the *remaining original 1,192-source rows*. The independently re-executed, duplicate-safe exhaustive checker covers all 2,361 representatives in 14 contiguous slices, **359,004** first-low-word trials in total; no three-word completion exists. Every slice's source SHA, exact orbit interval and negative conclusion was freshly checked.
6. **\(t=5\):** All \(\binom{32}{5}=201,376\) combinations reduce to **12,717** physical symmetry representatives; every possible actual two-word lower-rank completion is ruled out by original-source support intersections.
7. **\(t=6\):** All \(\binom{32}{6}=906,192\) combinations are rejected after checking all actual one-word lower-rank completions on original 1,192 source sets; only 16 pairs of rank7-six combinations even permit completion of the restricted five-source family, and none permits all 1,192.
8. **\(t=7\):** All \(\binom{32}{7}=3,365,856\) physical rank7 word tuples fail even to distinguish all original 480 five-element sources (best 476).

These eight mutually exclusive cases cover every possible 7-word real physical dictionary. Thus \(M^*(5)\ge8\). Combined with the eight actual words yields the exact theorem. A <=6 dictionary is already impossible from the P12 R5=7 theorem.

## Source identity and verifier receipt

- Frozen physical source SHA-256: `9f2119738f92f56485897c1894d2cb721a3d6b0498c5aa14832c71f18b20e2f1`.
- Exactly `18^5=1,889,568` five-turn physical words induce `14,938` distinct original observation partitions. Every rank-conditioned verifier works from this exact physical corpus.
- Complete original rank split certificate for t0: 65 dual + nine branches, 74 first-rank6 orbits.
- Original-source t1-3 integer certificate: 374 verified integer row-weight inequalities.
- t4: **14 independently re-executed contiguous orbit slices**, 2,361 orbit representatives, 359,004 first-low trials; composite receipt.
- t5-7: 12,717 / 906,192 / 3,365,856 separate exact branches.
- One final no-SAT receipt compiler independently replays the eight HTM words against the original 1,192 source rows, checks all required P12/P13 stage receipts and source SHA, and emits `CUBE_REV_019_P13_ORIGINAL_FULL_1192_PHYSICAL_MSTAR5_EXACT_EIGHT_LOCAL_FINITE_PROOF_PASS`.

## Full observation-horizon classification for this *fixed* physical model

| Length L | Exact M*(L) | Evidence grade |
|---|---:|---|
| 0–3 | not feasible | local analytic four-slot and sensor action confinement |
| 4 | 34 | **externally verified DRUP** from CUBE-REV 0.18 |
| 5 | **8** | **P13 fresh local finite proof**; external new CI pending |
| 6 | 4 | P7 original physical finite proof; external new CI pending |
| 7 | 3 | P5 original physical finite proof; external new CI pending |
| 8 | 2 | P5 original physical finite proof; external new CI pending |
| >=9 | 1 | P5 original physical nine-word full-identification witness |

**Fractional-vs-integer gap** at L5 (same original-source model): ordinary real set-cover LP optimum exactly \(16/3\), integer minimum **8**, ratio **3/2**. For R5-only 480 sources the exact LP optimum is \(185/39\), integer **7**, ratio \(273/185\). Enlarging R5 to the full 1192 admitted source family costs **exactly one additional integer experiment**, while the ordinary fractional optimum rises by exactly **23/39**. These are properties of this fixed instance, not universal bounds for all perfect hash families or general 3×3 cube solving.

## Certificate integrity and claim boundaries

- This is a computer-assisted finite proof with separately auditable fixed-physical-input verifiers and integer certificate inequalities. The original 0.19 L5 result is NOT described as externally validated by GitHub Actions, a formal theorem prover, DRUP or VeriPB until actual independent successful receipts are checked.
- The 16 signed-coordinate transformations are **source-incidence automorphisms**, not claimed to be sixteen executable cube actions. Every orbit reduction is contingent on separately checked preservation of all original source rows and raw physical cover types.
- The original source ontology, initial intrinsic flip-zero convention, five-observation transcript, action alphabet, reset privileges and dictionary-unit cost are fixed. No claims are made about full 3×3 cube state identification, human cognitive limits, WCA optimal solving, or arbitrary source families.
- Proposed 0.20 generalization and novelty require comparison with existing perfect/separating hash family, automata distinguishing sequence and certified combinatorial optimization literature.

## 0.20 handoff

The exact 0.19 horizon profile is now a **frozen benchmark**. The next meaningful research target is not to enumerate still larger families blindly, but to derive **general structural theorems** explaining physical observation-cut transport, restricted-perfect-hash source extensions, discrete-vs-fractional covering gaps, and feedback-versus-preset trade-offs, supported by proof-carrying reductions and falsifiable transfer to at least one distinct finite physical transducer. The formal name is proposed in `docs/0.20/PREPARATORY_CHARTER_NOT_ACTIVATED.md`. Do not claim 0.20 has proved these laws merely by opening a plan.