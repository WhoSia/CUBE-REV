# CUBE-REV 0.29 AN2 — A four-family Hall criterion, with irredundancy

**Date:** 21 November 2026. **Research goal:** remove unnecessary subproblem enumeration from the first eleven edge-color observations using the exact (K_{2,2,2}) graph. This note is a mathematical reduction and an independently checked finite receipt, not a new proof that the full cube is identifiable in nineteen frames.

## Theorem — necessary and sufficient inequalities

Let the six face colors form three opposite pairs `P1={U,D}`, `P2={R,L}`, `P3={F,B}`. Each edge type is an unordered two-color pair with its endpoints in two different `P_i`. For a nonnegative vector `n` with total `Σ n_v=11`, the eleven-color transcript is realizable by eleven distinct original edge types **if and only if** all of the following hold:

1. **Singleton:** `n_x ≤ 4` for every color `x`.
2. **Nonopposite pair:** `n_x+n_y ≤ 7` for each pair `x,y` from different opposite pairs.
3. **Full pair plus a third color:** `n_a+n_b+n_c ≤ 10` whenever `{a,b}` is one whole opposite pair and `c` lies in another pair.
4. **One from each of the three pairs:** `n_a+n_b+n_c ≤ 9` whenever `a∈P1`, `b∈P2`, `c∈P3`.

**Proof.** Hall's theorem in AK2 says `Σ_{x∈S}n_x ≤ 12 - |E(H[V\S])|` for every subset `S` of six colors. The automorphism group `(C2)^3⋊S3` partitions all **64 subsets** into ten orbits classified by the sorted triple `(|S∩P1|,|S∩P2|,|S∩P3|)` with components 0, 1 or 2. For each orbit choose a representative; its Hall capacity is a function only of these three occupancy numbers:

| Occupancies | Number of subsets | Hall upper bound |
| --- | ---: | ---: |
| (0,0,0) | 1 | 0 |
| (0,0,1) | 6 | 4 |
| (0,0,2) | 3 | 8 |
| (0,1,1) | 12 | 7 |
| (0,1,2) | 12 | 10 |
| (1,1,1) | 8 | 9 |
| (0,2,2) | 3 | 12 |
| (1,1,2) | 12 | 11 |
| (1,2,2) | 6 | 12 |
| (2,2,2) | 1 | 12 |
| **Total** | **64** | — |

The empty-set cut is automatic. Since the vector sum is eleven, every cut with upper bound eleven or twelve is automatic. The `(0,0,2)` cut `n_a+n_b≤8` follows from the two singleton cuts `n_a≤4`, `n_b≤4`. The only remaining conditions are exactly the four stated families. Thus those four families are simultaneously necessary and sufficient. Combined with the complete-cube parity completion in AK2, they characterize the actual *legal cube* first-color histogram support. □

## Irredundancy and mutation controls

For every one of the 4,368 vectors of six nonnegative entries summing to eleven, the complete 64-subset Hall test and the reduced four-family test return exactly the same verdict, accepting 1,362 vectors. Moreover, all four families are independent as systems of inequalities. Dropping each family while retaining the other three introduces the following number of false positives:

| Removed family | Invalid histograms newly admitted |
| --- | ---: |
| Singleton | 468 |
| Nonopposite pair | 120 |
| Full opposite pair plus third color | 12 |
| One from each pair | 72 |

The counts come from the independent pure-Python audit `scripts/cuberev-observation/audit_r029_hall_burnside_graph_quotient.py`. The source uses an exhaustive finite check *only as a negative-control validation of the structural theorem*, not as the theorem's proof. The four irredudancy witness classes are potentially useful for mutation tests of a future Lean `decide` implementation.

## Why this matters in the formal proof

The previous first-color orbit receipt used an `11×12` edge-assignment generator and counted 1,362 histograms. In a fully formal construction, the four inequalities give a compact feasibility predicate that no longer requires enumerating oriented 12-piece arrangements to decide *root support*. This is a larger conceptual gain than optimizing a brute-force loop by a constant factor, because a proof of Hall and the occupancy classification generalizes to similar multipartite sensor-design problems.

The **remaining danger** is informational: the normalized continuation policy depends on the *order* of eleven first-color replies, the chosen color-map witness and the ordered endpoint labels, not only the count vector. Thus even a perfect root-support predicate cannot certify the entire adaptive tree; the group-covariant posterior proof and stable-sort sign character must still be discharged.

## Methods references (owned originals)

- [Diestel (2017), *Graph Theory*, 5th ed., §2.1](https://drive.google.com/file/d/1T2pB-wAv7RXLsXTVJ7I5EkllVdIKxBWd/view).
- [Schrijver (2003), *Combinatorial Optimization*, §§22.1–22.1a](https://drive.google.com/file/d/1Y7TMSTkLxvmhpQEkyiPhPm9WiLJb3MaD/view).
- [Chekuri (2022), *Combinatorial Optimization*, Theorem 5.11](https://drive.google.com/file/d/1_NdMZy6A0w_owAK5BtasY9c-6LPqJe5g/view).
- [Cameron (1999), *Permutation Groups*, group action and orbit counting](https://drive.google.com/file/d/14WWOUzTUy7PVuFcr5cnX0O2Fsfxqif/view).

The matching theorem and orbit–stabilizer machinery are classical. The source-specific technical contribution is the exact reduction of the cube's categorical-prefix feasibility constraints and the executable verification controls.
