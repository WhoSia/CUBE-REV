# CUBE-REV 0.28 — R14-P8.23/P8.24: Full-Group Base 18, B10 Saturation, and an Explicit B7 Counterexample

Date: 2026-11-11. Status: independently executed finite **legal cubie stabilizer parity/orientation enumeration** and genuinely independently executed **48 moving-sticker B7 two-state collision**. The B6 exact 16-sensor/156-layout positive certificate and published Rubik 18-HTM diameter 20 are **external premises**, not computations redone in the current experiment. No Lean kernel result or original 41 B12 classes claimed in this unit.

## A. Source and actual scholarly reading

New originals are already present in canonical central Research OS 10_PAPERS (read text and verify exact Drive IDs, name, size and existing parent; do not move/rename again): Blaha (1992), Journal of Algorithms 13:297–306, 1Z-Oe_mOkUrZAQhgsmpZvHuAwN8JtEGKL; Jerrum (1986), Journal of Algorithms 7:60–78, 1iB2SnrHoIlxFlaz3IQGXRuT5cIHyNUvH; Sims (1970), 1M4WTjnpXCjcGoXaVD1UZpGss79409eK8; Sims (1971), 12ESPckYd--MAe0_V6-E5wsqsTXiAOd4A; Bshouty, Goldman, Hancock & Matar (1996), 1DcEyQhPZfYErZaTra9sSqvOo_Kl4W8p4; Bisht, Bshouty & Khoury (2008 issue / 2007 online), 1wU_xQt0rwHbaI0y2eXa23zZJJfpSJHxB; Rivest (1987), 16OTCF7mxJO4ypYvBanEBoN-PkPsH1J8t (re-read already-normalized target 10_PAPERS parent). **Bshouty1995.pdf** id 1br-s2_yYtMhoIw_r-CZ4OBTNDuLtA2Pa remains **00_INTAKE TEXT_EXTRACTION / IDENTITY HOLD**; no evidence yet it is identical to the November 1995 publisher version of Bshouty, Exact Learning Boolean Functions via the Monotone Theory. An official ECCC report https://eccc.weizmann.ac.il/report/1995/008/ and journal DOI 10.1006/inco.1995.1164 identify the published original, but file name is not an originality/edition test.

Specific scholarly critique: Blaha (1992, §2.2) selects an additional **point in a largest orbit of the current pointwise stabilizer**, to shrink group order at each step. The earlier CUBE-REV P8.15 algorithm deletes **an already selected sensor chosen from currently removable tags**, subject to radius-six injectivity. These are NOT the same greedy heuristic and neither Blaha's NP-completeness result nor his approximation bound can be transferred without model and algorithm matching. Sims (1971) defines base and stabilizer chains and derives group order as product of basic orbit sizes. Jerrum (1986) improves representation costs and coset enumeration. Bshouty et al. (1996) optimize equivalence-query counterexamples in membership/equivalence learning, whereas Bisht et al. study erroneous answers in a model with an adversarial teacher. Their costs/feedback differ from the six-color two-spatial-probe Rubik game.

## B. Full original-cubie tag sensing on the entire legal group

Let Ω comprise eight persistent original corner tags C and twelve edge tags E. Each sensor outputs the exact location and orientation of a particular original cubie. The legal fixed-center Rubik group G has corner orientation sum 0 mod 3, edge flip sum 0 mod 2, and matching parity of corner/edge permutations.

For omitted original tags U, define H(U) to be the legal whole-group pointwise stabilizer of all observed tags Ω\U, where each observed ORIGINAL cubie must retain its exact initial position and orientation.

**Elementary complete theorem:** H(U) is trivial iff |U∩C|≤1 AND |U∩E|≤1. Proof: with at most one omitted cubie of each type, permutations of omitted corners/edges are forced identity and corner/edge orientation sums force zero. Conversely, if U contains two omitted corners, their opposite nonzero twists preserve all observed original tags; if U contains two omitted edges, their joint flip preserves all observed tags. Any larger U contains one of these two witnesses.

Hence the full-group identifying sensor family is precisely all S that omit at most one corner and at most one edge; minimum count |S|=18, with exactly 8×12=**96 labelled optimum designs**. Full-group identifying counts for 18,19,20 sensors are 96,20,1, respectively. These results are immediate exact legal-group consequences, NOT a newly invented general permutation-group base theorem.

The 48 physical state structure gives |G|=8!·3^7·12!·2^11 / 2 =43,252,003,274,489,856,000.

An independent Python checker enumerated all legal pointwise stabilizer permutation/orientation pairs for every omission shape of sizes 0..3 and obtained:
- 20 observed: one design, stabilizer order 1.
- 19 observed: 20 designs, order 1.
- 18 observed: 96 designs order1; 66 designs order2 (two unobserved edges); 28 designs order3 (two unobserved corners).
- 17 observed: 528 designs order2 (one omitted corner, two edges), 336 designs order3 (two omitted corners, one edge), 220 designs order12 (three omitted edges), 56 designs order27 (three omitted corners).
- 16 observed with 2C+2E omitted (the entire previously certified B6 minimum class): stabilizer order **12**, rather than 1.

The 17-observed sector figure **336** is an ALL-layout whole-group stabilizer count, not B6-positive 144; the two statements have different quantifiers. In the previously certified B6 positive subset, the 17 positive layouts split as 528 order2 and 144 order3, 18 positive as 96 order1, 66 order2, 12 order3; all true global 18-tag bases are included among B6 positives.

## C. Radius saturation using the already published 18-HTM diameter D=20

In any finite group with symmetric generators and geodesic ball B_r, the elementary radius-doubling identity is B_r^{-1}B_r=B_{2r} (split a geodesic of length ≤2r into two pieces of length ≤r). A static set of original cubie tags distinguishes the entire B_r iff its whole-group pointwise stabilizer H(S) intersects B_{2r} only at identity.

Rokicki et al. (2013), The Diameter of the Rubik's Cube Group Is Twenty, provides the independently established **HTM diameter D=20**. Thus B_{20}=G, and more sharply B_{10}^{-1}B_{10}=G. Therefore B10-tag injectivity is equivalent to full-group injectivity:

  b_10 = b_G = 18, and the 96 full-group 18-tag bases are exactly the B10 minimum bases.

For every r≥10 the full B_r identification family coincides with full-group bases (because full-group bases are sufficient and B10 already detects every nontrivial stabilizer). Combine the separately certified b5=b6=16 with monotonicity to obtain:

  b_5=b_6=16, b_10=b_11=...=18; the exact first one- or two-unit jumps occur only among r=7,8,9,10.

No assertion that b7=17/18 is justified yet. More generally, this saturation lemma is standard and the cube-specific 18 derives from elementary parity constraints; it may be a useful bridge in a wider physically verified radius transition study, not a stand-alone publication claim.

## D. Explicit B7 collision for at least 24 B6-optimal sensor layouts

A previously recorded physical 13-move word is:

    L F R' F' L' U2 R U R U' R2 U2 R

The word is a legal 13-HTM sequence that, in the **independently reconstructed 48-sticker physical model**, fixes all sticker positions of all original cubies except that it flips the two original edges UF and UR (four stickers move). The omitted four-tag set of the sensor arrangement S is the two original endpoint corners of native edge DL PLUS original edges UF and UR. This is an actual physically certified **B6-positive** size16 layout in the inherited 156-layout family. (Its corners are omitted by design but not affected by this particular witness.)

Let w be the length-13 word, p its first 6 turns, and s its final 7 turns. With the physical permutation composition convention state(w)=state(s)∘state(p), let

  x=state(s)^{-1}, y=state(p).

Then x and y are two **distinct** legal configurations, both in B7 (word lengths respectively 7 and 6), and state(w)=x^{-1}∘y. As the 13-word transformation fixes all observed original sticker identifiers, the 16 original cubie tag observation vectors agree exactly in x and y. A genuinely separate locally executed Python 48-sticker generator checked all:
- 48 moving facelet slot coordinates and 20 oriented original cubies;
- exact 13-word physical permutation equals the two-original-edge flip target;
- two full distinct legal B7 states, y from six prefix turns and x from inverse seven suffix turns;
- every one of 16 observed cubies has identical full sticker destinations in x and y;
- the four omitted original pieces and the physical difference support (two edges only) are explicitly checked.

All 24 proper cube rotations generate **24 distinct omitted-four-tag sensor layouts** in the same B6-minimum family, with rotated physical 13-word witnesses (rotate move faces, preserving HTM length). Hence for each of those 24 labelled B6-positive layouts,

  rcrit(S) = 7.

The **lower** rcrit(S)>6 premise uses the inherited physically sealed B6 41-positive-target certificate. The **upper** rcrit(S)≤7 is directly constructed by fresh separate physical P48 execution. This verifies the existence of concrete first-failure-at-seven layouts, but DOES NOT show every one of the 156 B6-optimal layouts fails at B7; b7 itself remains unknown.

Source script: scripts/cuberev-observation/audit_r14_p824_independent_48_sticker_b7_collision.py. Source script for the independent exact legal stabilizer census: scripts/cuberev-observation/audit_r14_p823_full_group_radius10_bridge.py.

## E. Next mathematically serious experiment

1. **Classify the 8 proper-rotation orbits of the 156 B6 optimum 16-sensor layouts by earliest physical collision radius**. We now have a verified-orbit 24-member class of rcrit=7 and general upper rcrit≤10. The exact metric on the 11 nontrivial stabilizer elements per layout, and 41 global symmetry-reduced target classes, are the right bridge. It may be possible to label all eight orbits without redoing global 4,845 classification.
2. Repeat for the 276 B6-minimal 17-tag layouts: stabilizer order2 or3 and critical radii in {7,8,9,10}, again with verified P48 target distances. Their first-failure radius may correlate with the 12 proper-rotation minimal17 orbits.
3. Physically replay all 41 B12-positive distance certificates and audit target-file hashes, then build a source-first finite Lean 24-action/66-pair bridge instead of generic static-identifier tautologies.
4. Keep Paper B whole cube h_adaptive=18..20 and its 19-frame open question separate from original-cubie tag costs. Avoid manuscript inflation before this classification becomes a strong theorem.

## F. Physical and bibliographic provenance

Published diameter reference already owned in Research OS 10_PAPERS: Rokicki et al. (2013), The Diameter of the Rubik's Cube Group Is Twenty, Drive ID 1cPtmb_5Npbnd8bghe4JNh734otHybnOV. The SIAM Review 2014 republication is separately owned, not to be confused as first appearance.

All new original scholarly items are source text/metadata verified, already present in central 10_PAPERS. The Bshouty (1995?) filename only is unverified in 00_INTAKE. Raw PDF byte SHA seals are NOT newly performed. GitHub read-only CI and Notion records remain distinct from actual kernel/physical proof verification. Neither exact P48 new B7 source nor P8.23 algebra code is independently confirmed by remote Actions until workflow results are observed.
