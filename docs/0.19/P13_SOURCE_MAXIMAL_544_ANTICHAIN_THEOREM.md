# CUBE-REV 0.19–0.20 Bridge — Canonical Maximal-Source Antichain, 480+64=544

**Proof status:** Exact source-family inclusion geometry theorem; requires NO physical move enumeration, LP, MIP, SAT, symmetry reduction, or temporal sensor assumptions beyond hereditary injectivity. Independent original-source verifier PASS.

## General finite-set theorem (elementary, prior art of finite posets)

Given any finite set of candidate initial hypotheses S and finite family \(\mathcal R\subseteq2^S\), define the unique inclusion-maximal antichain

\[\operatorname{Max}(\mathcal R)=\{A\in\mathcal R:\nexists B\in\mathcal R\text{ with } A\subsetneq B\}.\]

Suppose each experiment w separates a source A whenever its observed trace \(h_w|_A\) is injective. Then for **any** executable experiment family and any cost on selected experiments (including cardinality),

\[\boxed{\mathcal D\text{ covers }\mathcal R\iff\mathcal D\text{ covers }\operatorname{Max}(\mathcal R).}\]

**Proof:** The forward direction is immediate because Max(R) ⊆R. For the reverse, every A∈R is contained in a maximal B∈R (finite ascent). Since some w∈D is injective on B, the same w is injective on A. The maximal members form a uniquely determined antichain. No cube-specific transition assumption was needed. Therefore the minimum experiment cost is unchanged for all observation horizons L, and for both SAT and fractional set-cover decisions.

This statement is elementary combinatorics; CUBE-REV does NOT claim to have invented antichain reductions, finite-poset maximality or hereditary injectivity. Its relevance is locating the physical problem's exact **source ontology kernel** prior to any solver-specific row or column reduction.

## Frozen original cube source family

For the original 1,192 admitted source sets, consisting of 220 triples, 492 quartets and 480 quintuples, the inclusion-maximal source antichain has **exactly 544 sets: all 480 admissible quintuples and 64 additional quartets**.

Write F={1,5,8,9} and B={3,7,10,11} for the original front and back edge-position quartets. Then the 64 maximal 4-source requirements have the *exact* geometric form

\[\mathcal H_4=\{T\cup\{x\}:T\in\binom F3\cup\binom B3,\quad x\in S\setminus G(T)\},\]

where G(T)=F or B according to which face supplies T. Counting gives 2 faces ×4 choices of face-triple ×8 off-face positions = **64**. The condition is source-family geometry, not an emergent property of a SAT optimizer.

The requirements **not contained in any one of the original 480 five-element source sets** are exactly **72**: the 64 primitive quartets above, plus the eight face-homogeneous triples \(\binom F3\cup\binom B3\). Each of these eight triples is contained in exactly eight primitive quartets, so all eight are themselves redundant once the 64 primitive quartets are required.

Thus the original 1,192→544 row reduction has a **canonical, physics-independent source-antichain explanation**. The previously reported additional original-L4 quotient to 398 rows can use stronger *candidate-family-dependent* row-support implication; that later reduction is not claimed to follow from source inclusion alone.

## Structural consequence for source-family extension

Let R5 denote the original 480 five-position requirements; then exactly 1,120 of all original 1,192 requirements lie in its downward shadow. The full family's *only logically new generators* relative to R5 are these **64 face-triple-plus-off-face quartets**. The eight extra face-homogeneous triple requirements add no independent constraint once the 64 quartets are included.

CUBE-REV's locally exact five-turn results are \(M^*(R5,5)=7\) and \(M^*(R_{\rm full},5)=8\). Therefore the exact integer source-extension penalty of **one** can be attributed to adding 64 explicit, geometrically characterized source generators—not to all 712 newly listed smaller sources as if they were independent demands. The exact fractional LP penalty for the same extension is **23/39**.

**Important:** This identifies which source constraints are *logically new*, but by itself does not prove a one-word cost jump. The jump requires the independent physical finite optimum certificates for R5 and the full source family.

## Independent verification

Run `verify_original_source_antichain_544.py --physical original_physical.json --output receipt.json`. It checks source SHA256, original 220/492/480 family sizes, full inclusion maximality, the exact 64 face/off-face quartets, exactly eight primitive triples, and full hereditary implication of every original source into one of the 544 maximal generators. It asserts `CUBE_REV_019_ORIGINAL_SOURCE_MAXIMAL_544_480PLUS64_ANTICHAIN_EXACT_GEOMETRY_PASS`.

**Scientific handoff:** The 0.20 restricted perfect-hash programme should treat the maximal-source antichain as its natural source-family representation. Then investigate genuinely new and falsifiable *physical-action* conditions for additional reductions, nontrivial extension penalties, and integer gaps beyond elementary poset theory.