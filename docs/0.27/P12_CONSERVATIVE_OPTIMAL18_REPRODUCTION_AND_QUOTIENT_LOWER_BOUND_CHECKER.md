# CUBE-REV 0.27 — P12: Conservative Independent Solver Replay and Verified Lower-Bound Checker Kernel

**Date 2026-10-19. Evidence grade:** externally reproduced optimal-18 under THREE remaining projected phase1x24 PDB soundness hypotheses; genuine third-party equal-axis heuristic eliminated. Standalone original 54-sticker 18-witness independently checked. **Independent global proof-carrying no17 is NOT YET CLOSED**. Every claim below distinguishes real runs and unexecuted proof obligations.

## Real completed external conservative recomputation

Real GitHub Actions [run #39196884761](https://github.com/WhoSia/CUBE-REV/actions/runs/39196884761) `completed/success`, existing branch `research/current`, commit `534fbbb1f9c3f114f7f120d1ac14152569242ef0`. The original independent P11 corner audit job succeeded; the guard-free full PyPy solver job succeeded. Wheel `RubikOptimal-1.1.0-py3-none-any.whl` **SHA256 c569e511dd9f9d2714030e0907186f4aec1849021793a539cf3c339c6feee61b**. Installed `optimal.solver` SHA256 `a6f6d67ca3f3cd3bbc93004e3db62abef4dc3d1996470f016048201ff80d4246`; original Python `search` SHA256 `af2659f5c53960196ec247fec6b21ea0afeb7fbd1d6114b18c5d4e6c9627e6b1`; conservative patched `search` SHA256 `190ecf64c5d09973bfeb33cca44930c836b2b4fde10cd6b62b72df6afdfe214b`.

The exact **previously unjustified equal-triaxial strengthened prune** was removed and verified absent by fail-closed patch contract; basic corner and three independent axis `distance >= remaining` cutoffs were retained. Before solving, the independently physical 40,320-corner exact distance table **and all 725,760** physical corner transitions were matched to the actual imported PyPI solver table; PASS. The original WCA source was pinned to the same 54-facelet string `LLRUURDDURDFLRLRBLLBFBFBBFDLDBUDRBLFBFFFLUURDDFUDBRUUR`.

| External conservative iterative depth | Actually generated |
|---:|---:|
| 14 | 290,658 |
| 15 | 3,789,156 |
| 16 | 49,449,246 |
| 17 | **645,445,908** (complete inside remaining PDB assumptions, no 17 witness) |
| 18 | 1,248,212,144 (terminates on a valid solution) |
| All depths | **1,947,210,938** |

Solver time **640.57 s** excluding table construction, which is a separate ≈15-minute cost. Independently replayed original 54-sticker 18HTM witness exactly:
`U' D' R2 F' D2 B' R F2 B U2 L2 U F U L U' F2 B2`.
This is a REAL fresh optimal-18 reported result without equal-triaxial enhancement, NOT a theorem independent of remaining huge PDB values and projection semantics.

## Authentic raw original-byte evidence seal

GitHub original Actions artifact ID **12163330636**, 1,873 bytes, SHA256 `64b912f4c9a23f9d041fe283532f0f80966df4800023562f3d40814d02355392`. Raw members `P11_GUARD_FREE_RAW.log` 4,852 bytes SHA256 `171c47a024c7203f20ff72d825de3f90f59c942367f118cdc1a1585e6f2f3a7b`; `P11_WHEEL_SHA256.txt` 124 bytes SHA256 `9fd4effe5a2d8729e01bae2a113abb669ee5dda074df104b1e2b097e079ead1a`. Original downloaded ZIP uploaded to Drive existing `10_CANONICAL_PROOF_COURTS` folder [file ID `171-GG5IOFnoJGU099N99vI1vhO7xj9ga`](https://drive.google.com/file/d/171-GG5IOFnoJGU099N99vI1vhO7xj9ga/view) and provider raw-byte re-downloaded; **exact original 1,873 byte equality and SHA verified**.

## Sufficient admissible-PDB certificate — finite graph theorem

Let G be the 18HTM full original cube transition graph, Q any finite quotient with goal q0 and a state projection π. For all legal whole-cube states x and every move a, certify **π(x·a)=T_a(π(x))**. Given a nonnegative integer certificate `h:Q→Z>=0` satisfying `h(q0)=0` and for every quotient vertex q and every 18HTM action a:

`h(q) <= 1 + h(T_a(q))`

then for every length k real cube solution, telescoping gives `h(π(x)) <= k`; h is a sound admissible HTM lower bound. This is a **sufficient** proof contract for the actual solver PDB pruning. Exactness of the table is not required. If each of h_UD, h_RL, h_FB and independently certified corner h_C is admissible, their maximum is admissible; this **does NOT** allow reinstating the stronger equal-distance tri-axial shortcut.

A fully checked distance table can additionally require (i) only the genuine goal at distance zero and (ii) an actual decrement by 1 from every non-goal. Distinguish weak safe admissibility from exact distance: a function identically zero is *admissible* and must PASS the weak check, but is not an exact-distance certificate and MUST fail the stronger check. Uniqueness of the goal and descent plus the one-sided Lipschitz bound prove exact distance on finite connected graphs.

**Critical warning:** an internally Lipschitz label array on a wrong quotient is NOT a real-cube proof. The quotient coordinate and all 18 transitions must be independently shown to commute with every physical cube move. The giant PDB only stores distance residues modulo3; the full positive integer labels and residue encoding itself still need certification.

## New ACTUALLY TESTED lower-bound certificate kernel

A separate producer-independent C++17 source `p12_quotient_lipschitz_checker.cpp` uses a read-only memory-mapped byte-array certificate, an independent `next(state,move)` callback, a goal index, a complete state count and move count. It checks every one-sided inequality, optionally exactness and a descending neighbor. Original authentic P11 C++ 54-sticker geometry supplies the independent **real corner quotient callback**, not the BFS producer. **Actual on-current-host PASS** on 40,320 corner states and 725,760 cube move transitions in EXACT mode, and on a deliberately weaker label table in ADMISSIBLE-ONLY mode. Negative controls: altered goal value REJECTED; inflated non-goal distance REJECTED; allzero admissible-safe passes weak mode but rejected in exact mode.

The independent `p12_mod3_residue_format_audit.py` validates all 40,320 original correct corner values in RubikOptimal's **16 residues / little-endian 32-bit word** layout, creating a **10,080 byte** test table; all residue roundtrips PASS, the 191 integer-case neighbor-distance reconstruction premise remains explicit, and injection of reserved residue3 REJECTED. Serialized test-vector SHA256 `566c3f1983e4a78912e2a8399e9b6cc487f9d7588410d6d6bde5c0359cc02e47`.

## Scale and **explicitly OPEN** genuine three-axis phase1x24 quotient audit

Upstream `N_FLIPSLICESORTED_CLASS=1,523,864`, `N_TWIST=2,187`, hence **3,332,690,568 projected states per axis** and **59,988,430,224** directed 18-move transitions. A u8 full-label certificate is **3.104 GiB** per axis; packed 2-bit residues are ≈0.776 GiB. This demands a separately audited D4h quotient and symmetry-transition generator, a real self-consistent numeric label reconstruction or exact BFS, a read-only streaming all-edges checker without storing ≈240GB edge files, and signed raw evidence hashes and independent projection commutation proof. **This complete giant quotient has not yet been verified**. The present P12 C++ callback only realizes the 40,320-state true original corner quotient. Never represent P12 as a full verified phase1x24 table. The failure-mode and trust boundary are explicit.

## Durable reproducibility and research priority

Full **10-member** P12 local ZIP `P12_CONSERVATIVE_CI_AND_GENERIC_PDB_CHECKER.zip` 32,912 bytes SHA256 **`fe059ee0e70c42f6de692ae84c647f22d80309d869625d2d8d68279e53a45945`**, containing C++ checker, Python 2bit decoder, original physical P11 header, original 40,320-byte corner labels, compressed test vector, standalone real execution logs, original GH raw artifact, all-member SHA manifest, research report. T2 Drive `10_CANONICAL_PROOF_COURTS` file [`1VV54-PM4R8G_U2BsnnDehDGUiBLnU0ya`](https://drive.google.com/file/d/1VV54-PM4R8G_U2BsnnDehDGUiBLnU0ya/view). **Actually re-downloaded original stored ZIP and verified all 32,912 bytes exactly match the original, SHA and ZIP CRC PASS**.

**Next P13**: freeze D4h projection and orbit conventions and construct an independent, executable `full cube → quotient` action-commutation checker; define a chunked 33.33e8-row distance certificate interface; begin exact PDB labels/residue reconstruction; only then attempt full ≈60b-edge certification. Seek a second independent no17 computation when affordable. Keep conditional external lower17, two verified distinct 18HTM upper witnesses and no-equal-axis third-party optimum18 separate. Do not claim full independent optimality until true PDB and search coverage both certified.
