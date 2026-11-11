# CUBE-REV 0.28 R14-P8.29 — Historical P48 Transport of the B7 Two-State Collision

Date: 2026-11-11. Branch: research/current. Evidence status: **SOURCE CODE COMMITTED; EXECUTION/REMOTE CI NOT YET VERIFIED IN THIS SESSION**. Keep this separate from the preceding locally executed P8.24 and P8.28 evidence.

## Input claims and interfaces

- P8.24: physical 48-sticker engine constructs the 13-HTM word `L F R' F' L' U2 R U R U' R2 U2 R`, splitting into prefix of length six and suffix of length seven. The observed 16 original cubie tags comprise six corners and ten edges, hence 38 moving stickers.
- P8.28: historical six face-turn permutations of Zassenhaus (1982), and 288 explicit full 48-sticker bijections `phi` satisfying `phi ∘ H_i = R_{f(i)}^{eps_i} ∘ phi`. The 288 enumerate different generator assignments and residual representation gauges; they do not give 288 independent physical witnesses.
- A B6-positive layout's first B7 collision at radius seven still relies on the separately inherited B6 positive certificate. Here we check a B7 collision's invariance under presentation change, not its shortest word.

## Transport lemma and proof obligation

Let `phi : A -> P` be a bijection between historical labels and modern spatial sticker positions, equivariant for the respective face-turn generator assignments. For any physical action `g`, define `g_A = phi^-1 ∘ g ∘ phi`. Then:
1. `(gh)_A = g_A h_A` and `g_A^-1 = (g^-1)_A` by cancellation of `phi phi^-1`.
2. If physical states `x != y`, then `x_A != y_A`, because conjugation is injective.
3. For observed physical source sticker labels `K subset P`, `x|_K = y|_K` if and only if `x_A|_(phi^-1(K)) = y_A|_(phi^-1(K))`. This is just substitution `x_A(a)=phi^-1(x(phi(a)))`; no global search needed.
4. Replacing each physical face-turn in a word by the corresponding historical generator or its inverse gives an equal-length face-turn word under conjugation. Half-turns remain half-turns.

Thus an actual P8.24 collision `x,y in B7` transports to a historical collision between two historical words of lengths at most seven and six. The transported observed sticker set has **38 elements** representing the same 16 original physical cubie tags.

## Executable audit

`scripts/cuberev-observation/audit_r14_p829_historical_b7_collision_transport.py` dynamically loads the two separately authored historical and physical P48 checkers. It checks slot agreement, all 288 bijective conjugacy cases, 13-word historical transcription under each generator map/sign, suffix/prefix two-state identity, pulled-back states, and identical outcomes on all 38 transported observed sticker labels.

Expected JSON *only after execution*: status PASS; 288 historical conjugacies checked; physical word length 13; 16 observed original tags; 38 observed moving sticker labels. A failed check must halt CI. Do **not** fabricate the JSON before a successful actual run.

CI workflow `.github/workflows/cuberev-r14-p827-historical-p48-conjugacy.yml` was amended to run both P8.24 and P8.29 as read-only tests, without Git write credentials. Its former escaped inline-newline syntax in a Python heredoc was corrected. Previous workflow status must not be extrapolated.

## Limits and follow-up

- This comparison is not independent of both imported source scripts; it is a cross-presentation regression proof check, stronger than agreeing support counts but weaker than a completely independent original-source simulation.
- It does **not** establish `b_7=17` or `b_7=18`. Only one previously known 24-layout orbit is covered by the explicit B7 physical witness.
- It does **not** check all 156 B6-optimal layouts or independently re-execute the original 41 shortest-distance positive certificates.
- It does **not** resolve unrestricted 19-frame adaptive observation.
- Next: obtain actual remote CI job logs and JSON artifacts, then audit a second representative physical witness from another B6 optimal rotation orbit; run fresh 18-HTM distance verification before using any radius claim.

## Historical context and backlog

The 38th conversation's missing-original literature ledger still includes Harary–Melter 1976, Slater 1975, Hennie 1964, Vasilevskii 1973, Hopcroft 1971, Sokolovskii 1971, and the Furst–Hopcroft–Luks 1980 FOCS original. Candidate extras include Singmaster, Bandelow, Golomb, McKay–Piperno, and an as-yet unidentified Babai original. This session has **not** independently re-audited the full Drive holdings; the list is carried forward provisionally, not a newly proven absence census.

The original 2026-10-30 B5 ZIP and original positive-geodesic/Lean-kernel receipts remain distinct missing or unverified raw-data gates.
