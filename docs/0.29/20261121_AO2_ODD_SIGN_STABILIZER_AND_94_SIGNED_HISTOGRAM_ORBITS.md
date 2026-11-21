# CUBE-REV 0.29 AO2 — Odd-sign histogram stabilizers: a mandatory gauge counterexample

**Date:** 2026-11-21. **Classification:** structural lemma with an independent finite orbit audit, not a global policy correctness theorem. **Motivation:** the source-level representative selector chooses one of several color symmetries that map an observed histogram to the canonical histogram. A proof that forgets the chosen symmetry can silently corrupt the edge-versus-corner parity label.

## 1. The parity character

Let (G=\operatorname{Aut}(K_{2,2,2})\cong(C_2)^3\rtimes S_3). For (g\in G), let (\tau_g) permute the three opposite-color pairs and put
[
\chi(g)=\operatorname{parity}(\tau_g)\in\mathbb Z/2\mathbb Z.
]
By the generator theorem AK4, this equals the parity of the induced permutation of all twelve edge types. Let (X) be the 1,362 Hall-feasible first-eleven color histograms. For a histogram (n\in X), let (G_n=\{g:g\cdot n=n\}).

An **odd-character stabilizer** is a (g\in G_n) with (\chi(g)=1). If such an element exists, two normalizing symmetries that send the same observed histogram to the *same canonical representative* may differ in their induced edge permutation sign.

## 2. Exact stabilizer classification

An independent direct enumeration of the 48 color maps, using only the three-pair parity character, yields:

| Stabilizer order `|G_n|` | Representative orbits without odd stabilizer | Representative orbits with odd stabilizer | Orbit size |
| ---: | ---: | ---: | ---: |
| 1 | 12 | 0 | 48 |
| 2 | 20 | 7 | 24 |
| 4 | 10 | 0 | 12 |
| 8 | 0 | 3 | 6 |
| **Total** | **42** | **10** | — |

Thus **10/52 canonical histogram orbits** (containing (7\cdot24+3\cdot6=186) of the 1,362 labeled histograms) admit a parity-odd stabilizer. The other 42 orbits (1,176 labeled histograms) have stabilizers contained in the kernel of the sign character. The groups of sizes 8 and 2 with odd characters are not interchangeable with the even-only stabilizers of size 4 or 2.

**Practical counterexample:** in the coordinate order (U,D,R,L,F,B), the histogram `(0,3,1,3,1,3)` is feasible and has a stabilizer of order 2 with one sign-odd member. The histogram `(1,2,2,2,2,2)` has a stabilizer of order 8 with four sign-odd members. In both cases two color automorphisms can preserve the histogram yet change the normalized twelve-edge piece-label permutation sign. These are not assertions that the full *physical cube* is invariant under the color map; the action here is the edge-color graph action.

**Consequent soundness gate:** a representation of the normalized game that stores only the unsigned histogram key is not enough to infer the correct physical corner parity in all cases. One must retain the exact color-map witness (g), and for ordered first-color transcripts also the stable-sort position map (\beta), or else prove stabilizer-equivariance of the full policy together with its terminal sign convention. Merely recomputing an unsigned representative after the fact loses information needed by the inverse transport.

## 3. Abstract signed-histogram orbit count: 94, not 52 or 104

Introduce the *formal product* (Y=X\times\mathbb Z/2\mathbb Z), with action
[
g\cdot(n,p)=(g\cdot n,\;p\oplus\chi(g)).
]
This is a well-defined finite group action on 2,724 labeled signed histogram pairs. It is **not yet the actual signed ordered eleven-color posterior game**, because that game has an additional position-sorting parity correction that depends on the full observed string.

For an ordinary histogram orbit with no sign-odd stabilizer, the two parity labels lie in *two different* (G)-orbits, while if the stabilizer contains an odd element, the two labels lie in *one*. Therefore
[
|Y/G|=2\cdot(52-10)+10=\boxed{94}.
]
The signed orbit-size distribution is (23\times12,\ 40\times24,\ 31\times48), summing to (2,724). The character-twisted Burnside check gives
[
\sum_{\chi(g)=0}|\operatorname{Fix}_X(g)|=2256,\quad
\sum_{\chi(g)=1}|\operatorname{Fix}_X(g)|=240,\quad
|Y/G|=\frac{2(2256)}{48}=94.
]

The two independent calculations—via the stabilizer-index formula and via character-filtered Burnside—agree. The executable also directly constructs the 2,724-pair signed action and obtains 94 exact orbits. These checks are intentionally limited to a 48-element group and a 1,362-histogram space, rather than full 12! cube permutations.

## 4. Reviewer-level interpretation and attack plan

**What is new here?** Not the existence of the parity character or Burnside's lemma, which are standard; rather the identification of ten specific *gauge-ambiguous* classes in the frozen Rubik upper-policy quotient. This suggests both a new regression family and a precise point where the parity correction must be kernel-checked.

**What is not proved?** These 94 abstract signed-histogram orbits are not 94 physically distinct optimal decision games, not proof that the existing 52-root certificate fails, and not a new 19-frame lower bound. The frozen interpreter already records a chosen color normalization and computes a sign correction; the issue is ensuring the future Lean implementation retains and proves the same correction for every actual ordered prefix.

**Next tests:**
1. For each of the 10 risky orbit representatives, select two color maps mapping it to the same representative but with opposite (\chi). Construct actual *ordered* first-color strings using a Hall matching, compute their stable-sort order and the **combined** sign correction, then check that both transports reconstruct the *same* original edge assignment.
2. Construct a regression mutation that deliberately discards the chosen (g) (or its parity) and verify that at least one such case fails. Do not use a trivial mutation that only alters a numeric receipt.
3. In Lean, generalize AL's finite character theorem to `sign(α∘π∘β)=sign(α)sign(π)sign(β)`, then check the exact `route_info` selector. Do not assume this equation follows from the unsigned Hall proof.

## Sources and reproducibility

Executable `scripts/cuberev-observation/audit_r029_hall_burnside_graph_quotient.py` contains the independent odd-stabilizer census, 94 signed orbits, size checks, and character-filtered Burnside sums. Formal finite theorem `formal/029/ColorGraphCharacter.lean` establishes the 12-edge/3-pair sign identity using the pinned six-color table. Original method books: [Cameron (1999), *Permutation Groups*](https://drive.google.com/file/d/14WWOUzTUy7PVuFcr5cnX0O2Fsfxqif/view), [Seress (2003), *Permutation Group Algorithms*](https://drive.google.com/file/d/1kUj3ajt6Fq_O8S9omgyUEHnbTAazItne/view), and [McKay–Piperno, *Practical Graph Isomorphism, II*](https://drive.google.com/file/d/1iQ38YgNK14g1lCazcHUS7Y6CvNujXbuf/view).
