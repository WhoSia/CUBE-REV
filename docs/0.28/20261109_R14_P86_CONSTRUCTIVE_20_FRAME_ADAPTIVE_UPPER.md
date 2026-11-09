# CUBE-REV 0.28 · R14-P8.6 — A constructive 20-frame adaptive upper bound

**Date:** 2026-11-09 · **Model:** exact, categorical six-color, one edge and one corner spatial facelet per frame; arbitrary *known* legal face-turn sequences between frames are free; centers fixed; all 43,252,003,274,489,856,000 physical legal cube states are allowed. **Status:** executable finite computational proof + explicit structural reductions, independently replayed on physical sample states and the entire exceptional conditional class. **No publication-priority or global-optimum claim.**

## 1. Main theorem

**Theorem P8.6 (constructive upper).** Under the stated model, a deterministic adaptive observation-and-decoding policy uniquely reconstructs the entire original physical 48-facelet state in **at most twenty paired observation frames**. Thus

\[
 h_{\mathrm{adaptive}} \le 20.
\]

Combined with the *previously archived* lower bound of 18 frames (not re-proved here), this narrows the working interval from **18–21 to 18–20**. No theorem presented here excludes a different 18- or 19-frame policy.

**Important scope:** The number **20** refers to observation frames, not Rubik moves. Known moves can be performed and undone between reads without being counted. This does not claim a 20-move solution to the cube or tolerance to noisy RGB labels.

## 2. Explicit policy

1. **Frames 1–12:** Observe a fixed indexed first facelet from *each* of the twelve spatial edge positions. In parallel, read the first two **ordered** spatial facelets from each of six chosen corner positions (twelve corner observations total).
2. **Frames 13–14:** Read the second indexed facelet (mate) of two additional edge positions selected according to previously returned edge colors. In parallel, read the first two spatial facelets of the **seventh** corner position. These 14 corner readings determine the complete corner arrangement and its permutation parity by the injective 24-word corner codebook and the twist-sum condition.
3. **Frames 15–20:** Select remaining edge-mate reads adaptively using prior edge colors. In the one exceptional first-color orbit, pass the newly *observed* corner permutation parity to the edge policy **only after frame 14**. In all other orbits the edge policy does not require this information. Once all edge cubies are uniquely decoded, combine with the completely reconstructed corners to recover all 48 original moving-sticker colors. Redundant corner reads are allowed after the first 14 frames.

The above is a constructive **finite decision procedure**, not an existence claim based on an information bound. The executable implementation provides a reproducible policy choice at every reachable belief and the inverse map from its normalized query coordinates to the genuine original spatial facelet indices.

## 3. Exhaustive edge observation court

Every legal edge configuration has an even total flip. Recording the first indexed facelet at each of twelve edge spatial positions yields a word \(a\in\{U,D,R,L,F,B\}^{12}\). A canonical representative for its color-count vector is the lexically grouped first-color word; source-color relabelings preserving all three opposite-face pairs act on these vectors.

The checked court reports:

| Quantity | Full finite verification |
|---|---:|
| Realizable first-color count vectors | **867** |
| Opposite-pair-preserving edge-color automorphisms | **48** |
| Count-vector orbits | **39** |
| Conditional full edge assignments across the **867 canonical first-color words** | **609,376** |
| Exhaustive deterministic complete decoder replays of those assignments | **609,376** |
| Extra mate reads required without parity, by count-vector classes | 6: **72**, 7: **636**, 8: **156**, 9: **3** |
| Number of exceptional hard color-count orbits | **1** |

**No misinterpretation of the 609,376 total:** these are conditional edge assignments summed **once per canonical first-color count vector**, **not** a brute-force enumeration of all 12!·2¹¹ full edge configurations. The explicit observed-position permutation transports the result to *every actual first-color sequence* having a given count vector.

The 39 root representatives are solved by exact AND–OR bitmask recursion, with all possible next-facelet colors tested and exact full-belief branch updates. For every representative, the program verifies its computed extra-read depth and constructs a correct decoding policy. The **867-member source-color transfer** is checked as a bijection of every conditional edge candidate set, not merely equality of candidate populations. The transformed permutation parity is tracked by the signs of the source-label permutation and the observed spatial reordering; source orientation reversals preserve even total flip in the 48 permitted relabelings.

All but three count vectors are decoded in at most eight mate reads without any parity oracle. The remaining three form one color-count orbit. Its representative first-color word is `RRRFFFLLLBBB`, with exactly **2,592** compatible even-flip edge assignments. An exact coupled decision game proves a policy exists that reads **two** edge mates, then receives the common parity at frame 14 and finishes using at most **six further mate reads**. There is no premature parity access.

The canonical bitset decision game explicitly checks 2,592/2,592 representative target decodings, with 2,336 targets requiring seven mates and 256 requiring eight mates (corresponding to frames 19 and 20).

## 4. Physical realizability and the second independent geometry audit

The first physical checker reconstructs genuine 3D source-to-spatial sticker permutations from legal 18-HTM move prefixes and verifies **2,001** full legal cube states, including actual readouts at requested spatial positions, reconstruction of the corner sign, and exact final 48-color recovery. It checks that every one of the **576** paired spatial edge/corner sticker targets is reachable from the fixed two-sensor pair by a legal turn word and validates 38,080 actual planned paired accesses. Of these 2,001 tests none encountered the exceptional hard color-count orbit; the next check addresses that omission.

The hard-case checker independently constructs **all 2,592 genuine legal physical 48-sticker states** realizing first-color word `RRRFFFLLLBBB` (one lawful corner completion for each edge assignment), checks physical legality, replays the adaptive policy, checks the corner sign is not consumed before frame 14, and verifies the complete edge/corner state reconstruction in **19–20** frames (2,336 at 19; 256 at 20).

**A new independent checker added in this release does not import P5.1, P8.2, or P8.6.** It rebuilds the 48 facelets from signed unit normals, reconstructs 18 genuine face turns by an alternative Rodrigues/cross-product quarter-turn formula, checks all moves preserve legal permutation parity and orientation totals, and establishes all 576 spatial paired-slot targets are reachable by turn and undo (maximum routing word length **6** turns). The actual sensor readings before and after tracked routing agree on 273 independent physical tests. It independently establishes that all **8×3=24** ordered adjacent corner-color pairs are distinct; hence reading two indexed stickers on seven corners uniquely determines those seven labels and twists, and the eighth label/twist follows from source uniqueness and total corner twist modulo 3. All 1,000 additional rotated corner assignments pass. The **proof of general corner reconstruction** is the injective codebook together with the cubie and twist constraints, rather than extrapolation from those samples.

These checks prove the mathematical observation protocol under the explicitly idealized hardware/turn-cost model. An implementation with limited rotations per frame, noisy labels, untracked moves or corner-side miscalibration is a different research problem.

## 5. Exact, but restricted, lower bound P8.7

A **separate** independently written exact `frozenset` Bellman solver enumerates the 2,592 edge completions under first-color transcript `RRRFFFLLLBBB`, split into 1,296 of each permutation parity. Even if an oracle reveals the correct common parity **for free immediately after the first twelve reads** (strictly more information than the proposed protocol), **seven more edge-mate reads are insufficient** in either parity stratum, while eight are sufficient. The solver supplies a bad legal response branch for every one of the twelve possible first extra query positions.

Therefore **20 frames are optimal within the family of protocols whose first twelve edge measurements read exactly the indexed first facelet of each of the twelve spatial edge cubies**. This does **not** establish \(h_{\mathrm{adaptive}}\ge20\) for *arbitrary* adaptive initial schedules. A different choice of the initial twelve spatial edge facelets, their order, repetitions, or interleaving of mates may permit a shorter universal policy.

## 6. What remains unproved / next scientific cycle

- **Global 18 or 19 impossibility:** The current restricted lower does not address a fully unrestricted two-probe initial query policy. To show exact \(h=20\), find a legal-state adaptive adversary that survives nineteen paired observations for every possible policy, not merely the fixed twelve-first-facelets schedule.
- **Independent prior-art audit:** Classical cubology, corner chirality, group actions, active diagnosis, and earlier two-sensor cube robot work predate this project. This document makes **no** claim that the specific twenty-frame theorem has not appeared before. Compare the exact sensor alphabet, query access, and charged cost definition before asserting originality.
- **Release completeness:** Pin source hashes, upload raw code and test receipts to long-term Drive, register `WhoSia`-authored GitHub commits, and independently inspect remote CI output before saying CI passed. Purely local pass is not remote CI success.
- **Potential research sequel P8.8:** Replace reliance on one fixed first-facelet per edge by an arbitrary reachable mixed-facelet belief state; attempt a sound lower bound of twenty via a small exact adversarial core or find a nineteen-frame counter-policy.

**Scientific priority:** This is a consequential *upper-bound improvement on the actual full coupled problem*. Further tool engineering is justified only if it supplies a missing proof ingredient, a nontrivial falsification test, or an independent numerical certificate.

## 7. Reproduce (Python 3.11, standard library)

Run from the repository's `scripts/cuberev-observation` directory after the five new files have been committed. The standalone corner/route independent checker does not import other CUBE-REV scripts.

```bash
python audit_r14_p86_constructive_full_20_frame.py
python verify_r14_p86_physical_20frame_routing.py
python verify_r14_p86_hard_physical_states.py
python verify_r14_p86_independent_corner_route_axioms.py
python verify_r14_p87_12_first_family_lower20.py
```

The physical runner and hard-case runner import the same policy source and P5.1 physical geometry. The new independent corner/route checker and the independent P8.7 hard-case solver do **not** import those modules. Each script emits a JSON receipt into its own directory and asserts all claimed properties before writing `PASS`.
