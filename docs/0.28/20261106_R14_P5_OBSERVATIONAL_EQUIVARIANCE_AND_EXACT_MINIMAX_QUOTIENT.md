# CUBE-REV 0.28 — R14-P5: Parity-Paired Observational Equivariance and a Sound Belief Quotient

**Status (2026-11-06):** mathematical **conditional exact** finite sensing-game equivariance theorem + independently executed 5-edge/3-corner algebraic court. **NOT** an independent P48 geometry court, full color-Rubik 20-frame construction, or a global 21-frame impossibility theorem.

## I. Research target and known obstruction

R14-P3 identified a fatal shortcut: four parity-class posterior **counts** can coincide while the same next paired color query has different outcome partitions ([20,20,20,12] versus [48,24]). R14-P4 counts parity-constrained legal completions exactly, but cannot infer an optimal adaptive policy merely from completion counts.

The correct object for the minimax decision tree is a **belief set** B with an observation map O_q: B -> six-color x six-color, for every allowed query q=(edge_facelet,corner_facelet). Define B_(q,y)={s in B:O_q(s)=y}. The zero-error horizon recursion is

    D(B) = 0 if |B|=1;
    D(B) = 1 + min_{q in Q} max_{y:B_(q,y) != ∅} D(B_(q,y)) otherwise.

In this **free-spatial-slot readout** game Q contains all paired spatial facelet choices. The R11 P48 joint probe orbit shows 576 edge/corner slot pairs can be reached by known legal turns when turn **cost** is not bounded; this statement needs independent P48 lift verification when transferring an algebraic coordinate transform to actual facelet geometry.

## II. Exact minimax-equivariance lemma

Let T:X->X be a bijection on the *legal* hidden-state space, and let rho:Q->Q be a bijection on allowed query pairs, satisfying

    O_{rho(q)}(T(s)) = O_q(s)   for all legal s and allowed q.

Then for any B subseteq X, any q and output y,

    T(B_(q,y)) = (T(B))_(rho(q),y).

The singleton terminal predicate is invariant under T. Hence by well-founded induction on remaining query budget, the existence of a zero-error depth-k policy is invariant:

    Win(B,k) <=> Win(T(B),k) for every k >= 0,

so the exact minimax values coincide: D(B)=D(T(B)). This is not an entropy approximation, equal-cardinality heuristic, or assertion based on sampled policy performance. The theorem is immediate from bijection and outcome covariance; the *substantive domain-specific work* is constructing and physically validating a nontrivial group of legal, observable covariances.

**Important:** T need not be implementable by an actual legal cube move; it is a symmetry of the **state-observation decision problem**, not necessarily a permitted physical action. If the objective also minimizes HTM turn cost, rho must additionally preserve routing costs/pose and the statement above does **not** by itself hold.

## III. Concrete parity-coupled symmetry in the R14-P5 finite court

The finite court has five distinct edge labels, three corner labels, flip parity zero and corner twist residue zero, and **matched** edge/corner permutation parity. It uses physical-looking six-color labels but cyclic abstract corner facelet ordering (no independent P48 construction).

Its legal state space is

    X = (E_0 x C_0) union (E_1 x C_1)

with |E_p|=960, |C_p|=27, |X|=51,840. For each state s=(edge_word,corner_word), the edge word contains ten ordered single-facelet colors and the corner word nine. A query (i,j) returns exactly the two colors at those positions.

Construct three generators on initial-spatial facelet **coordinates**, with corresponding bijective transformations of the color words:

1. P: interchange the two complete spatial edge positions 0 and 1, **and simultaneously** the two complete spatial corner positions 0 and 1. Each sector's permutation parity toggles; the shared parity constraint remains valid. The edge-only odd swap alone sends **every** legal coupled state to a cross-parity illegal state.
2. F: exchange the two ordered facelet slots at edge positions 0 and 1 simultaneously. Their orientation residues each toggle, so global edge-flip parity remains even.
3. T: rotate the three ordered corner facelet slots at corner position 0 by +1 and position 1 by -1 modulo three. Global twist residue remains zero.

The generated group has **12 elements**. Abstractly it has the presentation of D_3 x C_2: P^2=F^2=T^3=1, PTP=T^(-1), and F commutes with P,T. It is a *small verified subgroup* of possible coordinate automorphisms, not necessarily the maximal quotient group. Each element g acts on state words and on paired facelet indices, with exactly conserved observed **color symbols**.

Warning: odd position permutation of only one sensor's cubie sector is **not** a legal state bijection; an implementation silently permitting that would produce a false quotient. More elaborate color relabelings and full P48 slot/chirality conventions are deliberately excluded from this P5 court.

## IV. Independent exact finite verification results

The standalone stdlib-only Python script constructs every legal state, every realized adaptive three-frame transcript, all twelve group elements, and a memoized complete minimax decision tree for a selected nontrivial remaining belief.

- Full legal finite test universe: **51,840** states.
- Adaptive three-pair free-slot readouts induce **2,464** distinct realized transcripts.
- For **each of the 2,464 transcripts** and each of the **three generators**, the exact transformed posterior matches the candidate set defined by the transformed transcript: 7,392 generator/history exact posterior checks using bitset-indexed all-state filtering.
- For the selected **40-state** reachable posterior, all 12 transformed beliefs are distinct and reproduce the **same exact minimax depth 3**, with complete policy replay on every state of each transformed belief.
- All 12 transformations and all 90 possible paired facelet queries of the selected belief satisfy exact outcome-partition covariance: 12 x 90 = **1,080** paired query comparisons.
- For all 2,464 histories each generator is tested on a rotating query (7,392 additional query partition comparisons); the general full-query identity follows from the proven coordinate mapping, not this finite subset.
- The invalidity of an unpaired odd edge-position swap is checked against all 51,840 states.

The observation histories used to construct the 40-state posterior are obtained with a deterministic feedback-dependent query schedule. Its 12 symmetry-transformed histories are valid observational constraints but **need not** coincide with the original deterministic schedule's choice at those histories; this is correct for a minimax game that can freely choose queries.

These exact checks establish a **sound orbit quotient for this finite algebraic sensing game**; they do not prove compression of all full 48-sticker P48 physical states, nor the existence of an optimal global 20-frame policy. The 12-to-1 reduction is demonstrated on one orbit of 12 distinct information states and applies to other states in the same model under the same group action.

## V. High-priority promotion gates

**P5.1 — independent P48 lift.** Obtain P48's physically ordered edge/corner sticker facelets and legal oriented cubie coordinates; prove each abstract generator maps actual legal P48 states to legal P48 states, including color response covariance and matched permutation parity. If naive order swapping breaks chirality/orientation conventions, construct the correct conjugated action or reject the claimed physical lift. Test every generator on many legal P48 samples and perform a structural proof beyond sampling.

**P5.2 — orbit canonicalization and witness reconstruction.** Implement a canonical representative of arbitrary partial observation constraints under this proven symmetry and track the inverse query transformation for replaying the representative policy against the original cube. Show exact matching-DP counts and all color branches agree on every canonicalization.

**P5.3 — stronger symmetry / bisimulation.** Find a larger, computationally viable subgroup (possibly combining color graph automorphisms with physical cubie-coordinate transformations), or a separate exact matching constraint equivalence, without merging beliefs merely by cardinality. Prove branch-preserving canonicalization by exhaustive comparison on meaningful mixed-prefix families, then apply to 12 edge + 8 corner full state.

**P5.4 — main 20-frame gate.** Use this exact quotient, parity matching DP and prefix-obstruction certificates to either construct a universally verified <=20 adaptive paired color policy or establish a universal >20 adversary. Initial 12/14/16 fully-read prefix obstructions do not cover genuinely mixed partial prefixes. Do **not** chase a paper headline based only on one 12-fold little toy symmetry.

## VI. Research OS and evidence custody

- Active source: `scripts/cuberev-observation/audit_r14_p5_observational_equivariance.py`.
- Exact local receipt: 40-candidate/12-orbit depth-three check, 2,464 histories, all three generator transformations.
- Canonical original Python in Drive: https://drive.google.com/file/d/1mgk7kdckRwEyb8lOQH4ubmemZahCeKCu/view
- Canonical output JSON in Drive: https://drive.google.com/file/d/1S8SFjv29UVEGsab3sLFTk0Lz_SqBRJX_/view
- Original Python SHA256 `c0f0ed57be25ac0373f82a8b6317768a96698e0454565a0a0e99354936ff6375` (10,414 bytes).
- Original JSON SHA256 `c3309d6abe89031d99858fd0f9f71ee1ef01b8ffcdefec1111b43569894e8236`.
- Local script run: PASS.
- Drive remote raw-byte SHA verification: PENDING until independently downloaded and compared.
- GitHub Actions CI: PENDING until actual result is observed.
- Notion: canonical research verdict and dependency record.
