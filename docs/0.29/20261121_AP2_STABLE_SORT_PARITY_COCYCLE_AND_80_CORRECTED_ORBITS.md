# CUBE-REV 0.29 AP2 — Stable-sort parity cocycle and the eighty corrected signed orbits

**21 November 2026 · Mathematical argument + independent finite verification.** Supersedes the *scope of interpretation* (not the validity) of AO2's 94-orbit character-only count. Actual frozen policy transport uses both a six-color relabeling **and** an order-sorting position permutation; both change edge permutation parity.

## 1. The causal normalization datum

Let (X) denote the 1,362 Hall-feasible color histograms (n=(n_c)_{c\in V}), with (\sum n_c=11), and let (G=\operatorname{Aut}(K_{2,2,2})) be the 48-element color group. For each histogram (n), define (w_n) to be the canonical length-eleven word of colors in the exact order `COLORS="URFDLB"` repeated according to (n).

For (g\in G), its color relabeling of (w_n) must be *stably sorted*. Define (\beta_{g,n}\in S_{11}) as the unique permutation sending the stably sorted positions to their original pre-sort positions. In the actual frozen Python policy, it is the array
```python
order = tuple(sorted(range(11), key=lambda i: COLORS.index(g[word[i]])))
```
with the final unread twelfth edge slot fixed. Let (\chi(g)=\operatorname{parity}(\tau_g)), the sign character of the induced three-opposite-pair permutation. By AK4–AL, this equals the sign of the induced permutation of the twelve edge cubies.

Define the **complete normalization correction**
[
\varepsilon(g,n)
  =\chi(g)\oplus\operatorname{parity}(\beta_{g,n})\in\mathbb Z/2.
]
Unlike the character-only (\chi), the correction (\varepsilon) depends on the observed color multiplicities. It is nevertheless determined **entirely by already observed first colors** and the chosen color map (g), not by future answers.

## 2. A closed inversion formula

Suppose the canonical color ranking is (c_0<\cdots<c_5). Since (w_n) is sorted into blocks (c_i^{n_i}), applying (g) changes the order of two whole blocks precisely when (\operatorname{rank}(g(c_i))>\operatorname{rank}(g(c_j))). That block transposition crosses (n_i n_j) distinct sticker positions, so
[
\operatorname{parity}(\beta_{g,n}) =
\sum_{0\le i<j<6}
n_i n_j
[\operatorname{rank}(g(c_i))>\operatorname{rank}(g(c_j))]
\pmod2.
]
There are only fifteen unordered *color-block pairs*, as against up to fifty-five pairs of observed positions, and no edge-permutation brute force. If either block cardinality is even, its crossing contributes zero. This yields a low-cost exact sign correction from six counts and the three-pair sign character.

**Proof.** Stable sorting preserves the relative order within each block. Every inversion is therefore between two distinct original color blocks whose transformed rank order is reversed. There are precisely (n_i n_j) ordered pairs of positions from the respective blocks. Sum those contributions modulo two. □

## 3. Cocycle identity, not merely a lookup table

Let (g,h\in G), and write (g\cdot n) for the transformed histogram. Stable sorting of a color-bijective word by (g), then by (h), gives the same final relative position order as a single stable sort by (h\circ g). Equal colors stay in their original order throughout because both maps are bijective. Permutation parity adds under composition; the edge-label character (\chi) is a homomorphism. Consequently,
[
\boxed{
\varepsilon(h\circ g,n)
 =\varepsilon(g,n)\oplus\varepsilon(h,g\cdot n).
}
]
This is the **1-cocycle identity** for the group action on histogram space. It guarantees that the augmented action
[
g\cdot(n,p)=(g\cdot n,\ p\oplus\varepsilon(g,n))
]
is associative and thus a genuine (G)-action on the abstract signed histogram pairs (X\times\mathbb Z/2).

The frozen Python transport's parity correction can therefore be modeled as a group-action cocycle rather than an ad hoc leaf-time XOR. **This is the exact replacement for AO2's simplified character-only action** if one wants to model the stable-sort step.

## 4. Complete stabilizer audit and corrected orbit census

For each representative (n\in X/G), let (G_n) be its 48-group stabilizer. The sign of the gauge difference between two valid normalizations is determined by (\varepsilon(h,n)) for some (h\in G_n). The independent audit yields:

| Stabilizer order | Gauge-safe representatives (all (\varepsilon=0)) | Gauge-unsafe representatives (some (\varepsilon=1)) |
|---:|---:|---:|
| 1 | 12 | 0 |
| 2 | 14 | 13 |
| 4 | 2 | 8 |
| 8 | 0 | 3 |
| **Total** | **28** | **24** |

Hence **24/52 representative orbits** and **426/1,362 feasible labeled histograms** admit two normalizations of the same histogram whose combined parity corrections differ. The original character-only test found ten unsafe orbits; that count is mathematically valid for the simplified action but underestimates *actual policy correction* risk.

Under the corrected cocycle action on 2,724 abstract signed histogram pairs, there are
[
2\cdot 28+24=\boxed{80}
]
orbits. The corrected orbit-size distribution is
[
7\cdot12+36\cdot24+37\cdot48=2,724.
]
The cocycle-twisted Burnside computation independently gives
[
\sum_{g\in G}\#\{n\in X:g\cdot n=n,\ \varepsilon(g,n)=0\}=1,920,
]
[
\sum_{g\in G}\#\{n\in X:g\cdot n=n,\ \varepsilon(g,n)=1\}=576,
qquad
\frac{2\cdot1,920}{48}=80.
]

## 5. Replication controls

The standalone audit `scripts/cuberev-observation/audit_r029_hall_burnside_graph_quotient.py` now preserves **both** separately labelled numerical experiments:
- 94 orbits: simplified parity-character action (p\mapsto p\oplus\chi(g)), no sorting;
- **80 orbits:** complete policy-style correction (p\mapsto p\oplus\varepsilon(g,n)), including stable sorting.

It checks the exact cocycle identity for all 1,362 possible histograms, all 48 group maps, and five Cayley generators: (1,362\times48\times5=326,880) composition identities. The same five generator types cover the group by the separately kernel-compiled `ColorGraphCharacter.lean` finite theorem. In addition it validates the 24 unsafe stabilizer classes, 426 affected labeled vectors, corrected signed orbit-size distribution, and the independent Burnside fixed-point totals (1,920+576=2,496).

This calculation is **not** a complete kernel proof of the cocycle formula. An exact Lean proof is now a prioritized next formal task, using the standard sign homomorphism on finite permutations plus the block-inversion formula above. The exhaustive small-group audit is a regression and independent numerical check, not a substitute for that proof.

## 6. Reviewer-critical limitations

- The 80 orbits classify *histograms with a formal sign bit*, not all ordered first-eleven-color posterior states or optimal adaptive decision trees. The actual parity of a legal cube is coupled to its corners, and the same (g) is not necessarily a physical whole-cube rotation.
- The gauge correction can be checked using only the past observed colors; a normalization algorithm may choose among stabilizer elements but must choose deterministically and retain its witness.
- This does not imply the frozen 52-representative policy is wrong. Its existing executable `route_info` retains the map and sorting permutation and computes `permutation_parity(order+(11,)) ^ relabel_sign(g)`.
- The next conclusive negative control should deliberately change or discard the *chosen normalization witness*, and demonstrate a wrong original edge reconstruction for an explicitly feasible ordered prefix. This requires testing the full already-existing independent certificate and not merely the abstract histogram orbit.
- Full upper-bound closure still requires interpreting every representative's 8-read tree in Lean and proving physical nineteen-frame recovery. The strong eighteen-frame obstruction remains independently certified.

**Original mathematical context:** [Cameron (1999), *Permutation Groups*](https://drive.google.com/file/d/14WWOUzTUy7PVuFcrvr5cnX0O2Fsfxqif/view) and [Seress (2003), *Permutation Group Algorithms*](https://drive.google.com/file/d/1kUj3ajt6Fq_O8S9omgyUEHnbTAazItne/view), alongside the present CUBE-REV AL sign-character theorem. Standard cocycle/homomorphism facts are not claimed as new discoveries; the exact sensor-specific 24-orbit gauge hazard is the new audit finding.

## 7. AV extension: 9,984 real ordered-gauge covariance checks

The previous one-witness gauge-forgetting negative control has been extended
**without changing the frozen 52-root policy or certificate bytes**.
`scripts/cuberev-observation/audit_r029_gauge_counterexample.py` now builds
one legal oriented 12-edge array for each of the 52 canonical feasible
first-color histograms, applies four distinct fixed permutations of its eleven
initial edge positions, then applies each of the 48 allowed opposite-color-pair
relabelings. For each of the `52 × 4 × 48 = 9,984` cases, it independently
checks complete piece uniqueness, even total edge flips, and the exact
combined position-sort/color-relabeling sign identity. An incorrect retained
gauge still produces the existing concrete false-sign negative control.

The check is intentionally **not** exhaustive over every original legal edge
permutation or every possible ordered eleven-color string. It provides
independent regression coverage of four first-eleven orderings per
representative, with 48 gauge maps each; extending this to all permutations
or proving it universally in Lean is a separate obligation. Edge arrays
are physically compatible with some legal cube corner permutation of the
corresponding parity, but the script does not construct and replay that
complete corner arrangement.

- [Source audit commit](https://github.com/WhoSia/CUBE-REV/commit/5a9f006658c11515f8626168b6a3d9b90e036f8c)
- [Read-only CI integration](https://github.com/WhoSia/CUBE-REV/commit/2774976cba343f3a82680f470c07389025c6e163)
- [Run #44912274902](https://github.com/WhoSia/CUBE-REV/actions/runs/44912274902): the dedicated 9,984-case audit step passed. Overall workflow completion must be read independently; step success alone is not a claim of overall success.

**Next exact proof task:** derive the sign relation for *arbitrary* `EdgeSlotOrder` and 48-color automorphism (rather than only four concrete orders), then connect that retained witness to the actual eleven-color prefix routing and sign-dependent terminal decoder. An unconditional `Fits 19` physical theorem remains open.

## 8. Clean-clone certificate loader regression (2026-11-21)

The 9,984-case gauge audit completed successfully inside the independent
observation workflow, but the **overall** workflow
[#44912274902](https://github.com/WhoSia/CUBE-REV/actions/runs/44912274902)
failed during standard-library test discovery: the legacy
`test_19_policy_certificate_negative.py` attempted to open
`scripts/cuberev-observation/upper-policy-certificate.json`, a plaintext
file deliberately omitted from the active Git checkout. This is an
**input-path failure**, not a counterexample to the 19-frame certificate or
to the gauge-covariance identity.

The corrected negative test reads the committed immutable
`formal/029/certificate_blobs/upper-policy-certificate.json.gz.b64` in
memory; validates SHA-256 of both the compressed and decompressed content
against the pinned digests; and then executes the same four independent
malformed-tree mutations. No certificate regeneration, network download,
untracked plaintext file, or modification to `verify_one` is necessary.
[Exact fix](https://github.com/WhoSia/CUBE-REV/commit/ce802b57930ac151c84bcb1d466fa57e2c689672).
This repairs the clean-checkout test path only; it is **not** a new
mathematical proof. The updated workflow's completed outcome must be
checked separately before claiming the whole test suite passed.

## 9. AV universal adjacent-swap and collision-free relabeling lemmas (2026-11-21)

To reduce the gap between finite 48-color audits and a reusable theorem over
arbitrary ordered observation histories, `formal/029/EdgeSorting.lean` now
carries the following mathematically distinct statements:

1. `adjTrace_relative_parity_invariant` (previously compiled):
   a shared valid adjacent-swap trace changes parity identically on two
   equally long distinct-label lists; their relative parity is unchanged.
2. `adjTrace_relabel_parity_shift_invariant` ([source commit](https://github.com/WhoSia/CUBE-REV/commit/61ceed548760b3c32dd747454a7c3e273cdf8686)):
   for **any** `f : Nat → Nat` and distinct list `xs` whose image under
   `f` also remains distinct, applying a valid positional adjacent-swap
   trace does not change the parity difference between the original and
   relabeled list. This is a general relabeling lemma, not a color-specific
   finite enumeration.
3. `adjTrace_equal_outputs_force_same_swap_parity` ([source commit](https://github.com/WhoSia/CUBE-REV/commit/3e16ad07ea924eaade9e6e4a50b28a5a146cb458)):
   two valid adjacent-swap traces on a distinct input list that produce
   exactly the same final ordering must have equal swap-count parity.
   Hence the parity contribution depends on the resulting position
   permutation, not on its chosen adjacent-transposition decomposition.

The additional hypotheses are essential: the lists must have no repeated
labels, and for (2) the relabeling must not merge two labels that occur in
`xs`. The actual first-eleven *colors* do have repeats, so this lemma
must be instantiated on **position IDs or edge-piece IDs**, not blindly on
the repeated color string. The 48 legal color maps themselves are
permutations of six color IDs, but the stable-sort position witness acts
on eleven distinct positions.

**Exact remaining proof gap:** provide a total deterministic stable-sort
permutation witness for every feasible *ordered* eleven-color prefix,
prove that its effect on the twelve edge labels is the correction used by
the frozen `route_info`, then compose it with
`induced_edge_sign_is_three_pair_sign` and the certified 52-root
decision-policy transport. No unconditional `Fits 19` policy is claimed
here. The latest Lean CI result must be verified on the exact commit;
source commits alone do not certify that these new lemmas compile.
