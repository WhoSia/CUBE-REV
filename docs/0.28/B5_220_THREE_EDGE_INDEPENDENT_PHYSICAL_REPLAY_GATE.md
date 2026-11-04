# CUBE-REV 0.28 — Physical re-certification gate for the B5 220 original-edge triples

**2026-11-04 AUTHORITATIVE SUPERSESSION: B5 220/220 independently generated and physically replayed — CI PASS.** The older 12/220 partial stage is retained below strictly as provenance, not the current scientific status. Fresh source-independent C++ 48-sticker radius-five BFS generated 621,649 distinct actual states and thirteen explicit two-sided <=5-HTM representative pairs. The separate Python 48-sticker engine replays **both original words and all 24 physically rotated variants** for each pair; exact original cubie support covers all **220/220** triple-edge omissions. A cross-language bridge additionally parses the **fresh C++ stdout**, independently checks the claimed triple and orbit sizes, compares actual words to the pinned manifest, and requires the physical coverage again. Success CI: [41756861110](https://github.com/WhoSia/CUBE-REV/actions/runs/41756861110). Scientific scope: complete B5 pure-three-original-edge-support existence, not an independent B6 41-target geodesic proof.


## 2026-11-04 closure — a physically replayed 13-seed, 220-support certificate

**Source:** `scripts/cuberev-observation/b5_independent_48sticker_seed_search.cpp`, a newly authored complete BFS to radius five of an independently implemented 48-labelled-sticker cube model. It certifies `1,18,243,3240,43239,574908` depth shell counts and `621649` distinct full 48-sticker states. Each of the thirteen geometric original-edge-triple orbits is searched for a *real pair* of distinct radius-five states with identical positions+orientations on all original physical cubies **other than** the three specified edge cubies. Both left and right sequences are at most five legal 18-HTM turns.

**Portable physical word pairs:** `data/0.28/B5_13_ORBIT_INDEPENDENT_WORD_PAIR_WITNESSES_20261104.json` contains all thirteen C++-discovered representative two-sided words, names the expected original-edge triple, and retains the exact move notation. Importantly, the first candidate run exposed incorrect face-turn sign conventions in C++: independent Python replay failed. The source was corrected to the Python physical oracle's `U-,R-,F-,D+,L+,B+` relative coordinate-axis convention, the entire BFS was rerun, and the regenerated **actual physical** words—not the wrong intermediate words—were stored.

**Independent check:** `verify_b5_three_edge_physical_manifest.py` applies each pair to the independent Python 48-sticker model, validates precisely three differing original labelled oriented edges, and *physically replays both move sequences transformed under all 24 proper spatial rotations*. Each rotated original-tag support must coincide with the geometrically transformed one. Every one of the 13 orbits passes; **220 distinct supports**, **zero missing**.

**Binding the two independent implementations:** `verify_b5_independent_cpp_receipt.py` parses the actual fresh C++ stdout, requires 13 consecutively indexed FOUND records, independently physically replays each C++-reported pair (not just the separately pinned JSON), validates the purported original edge names and proper-24 orbit size, performs 220/220 physical replayer verification, and demands exact equality of the output words with the committed manifest. The GitHub Actions read-only workflow actually compiles C++17, runs the fresh BFS, invokes both Python verifiers, and demands `B5_FRESH_CPP_TO_PYTHON_220_PHYSICAL_PASS` and `B5_220_INDEPENDENT_PHYSICAL_PASS`. This closes the potential loophole where a generator prints 13 arbitrary FOUND entries while Python verifies an unrelated manifest.

**Proven fact:** For every triple `E` of the twelve original edge cubies, there exist two distinct states `x_E,y_E∈B5` whose complete original-cubie position-and-orientation observations differ exactly on `E`. Equivalently, the 220 three-edge supports all belong to the radius-five physical collision support family. The proof is *finite and executable*, not a new generic graph sensor or group-base theorem.

**Still open:** (i) independent second-facelet-physical-engine reproduction of the 41 B6 HTM `>=13` stabilizer distance queries; (ii) more conceptual non-enumerative derivation of B6's 13 positive omission pairs per missing-corner edge; (iii) external novelty/peer review. These open items do not negate the new **physical B5 lower-bound** certificate.

## Why this gate exists

The exact B6 one-original-cubie-erasure threshold theorem `b6^(1)=19` has a physical **lower-bound dependency**: for *every* 3-subset of the 12 original oriented edge cubies, there must be two distinct real 3×3 cube states reachable in <=5 outer-face HTM turns each, with **all 8 original corner factors equal** and **only the specified three original edge factors different**. The historical B5 source has a sealed 54-facelet replay:

`CUBE_REV_20261030_EXACT_B1_B5_SENSOR_CERTIFICATES.zip`
SHA256 `002887a198bac812ad360ba536309f2522899d5c28d12fb73bb92062ae889c94`.

The *current* `verify_b6_one_erasure_exact19.py` helper named `inherited_all_B5_three_edge_supports()` constructs all 220 combinatorial triples with `itertools.combinations`. That is an **explicit statement of the inherited physical premise**, NOT an independent test that those physical witnesses exist. This difference is proof-critical and must never be hidden by a test that merely asserts the number 220.

## New fail-closed, differently implemented physical verifier

`scripts/cuberev-observation/verify_b5_three_edge_physical_manifest.py` accepts an explicit UTF-8 JSON object containing pairs of real length-≤5 sequences:

```json
{
  "schema_version": 1,
  "witnesses": [
    {"left": "U R2 U'", "right": "D B2 D'"}
  ]
}
```

Each pair must satisfy **all**:
- Both words are legal symmetric original 18-HTM sequences, each of at most five turns.
- The two resulting physical 48-movable-sticker configurations, through the existing **separately coded 48-sticker transition engine**, differ on **precisely three original labeled oriented edges**, and no other original cubies.
- Each of the 24 proper spatial rotations is applied **to both original move words**, then independently physically replayed. The measured three-edge factor support after every rotated replay must agree with the geometrically rotated original-edge set. Merely rotating an abstract mask without replay is **not** accepted.
- Duplicate supports are removed; the final physically realized family must equal all `C(12,3)=220` possible three-edge supports. If not, the default command exits nonzero with **INCOMPLETE** and exact coverage counts.

The historical original B5 archive contains the nine B5-new physical pairs and original B4 seeds. Their original seed words have **not** been imported. Instead the fresh 621,649-state C++ physical search recovered a NEW complete set of thirteen physical pairs, all independently replayed by the Python source; the new certificate no longer needs the historical seed-word manifest.

## Independent geometric census — exactly 13 original-edge-triple orbits

Without using the inherited B5 positive/negative masks or any physical witness words, the verifier independently constructs all `C(12,3)=220` original three-edge support sets and partitions them by the 24 orientation-preserving cube rotations. Exactly **13 orbits** result, of sizes

```
4, 4, 8, 12, 12, 12, 24, 24, 24, 24, 24, 24, 24.
```

One explicit representative for each is listed below; original edge names are the actual cubie stickers/positions, not abstract Cayley graph vertices:

| Geometric orbit representative (three omitted/original edge labels) | Orbit size | Physical B5 replay status |
| --- | ---: | --- |
| BL, DF, UR | 4 | Original witness manifest not yet imported |
| DB, FL, UR | 4 | Original witness manifest not yet imported |
| FR, UF, UR | 8 | Original witness manifest not yet imported |
| BR, UF, UR | 12 | Original witness manifest not yet imported |
| DR, UL, UR | 12 | Original witness manifest not yet imported |
| FL, UF, UR | 12 | Original witness manifest not yet imported |
| BL, UF, UR | 24 | Original witness manifest not yet imported |
| DB, UF, UR | 24 | Original witness manifest not yet imported |
| DF, UF, UR | 24 | Original witness manifest not yet imported |
| DF, UL, UR | 24 | Original witness manifest not yet imported |
| DL, UF, UR | 24 | Original witness manifest not yet imported |
| DR, UF, UR | 24 | Original witness manifest not yet imported |
| UF, UL, UR | 24 | Original witness manifest not yet imported |

The compact **source-independent geometric partition** sums to `4+4+8+3*12+7*24=220`; it also agrees with the historical 2026-10-30 description that B3+B4 supplied 4 orbits of sizes `12+24+24+24=84`, and B5 supplied 9 further orbits of sizes `4+4+8+12+12+24+24+24+24=136`. These subgroup-size facts do NOT determine which representatives have shortest witness radius B3/B4/B5 or prove their physical existence.

**Minimality under a restricted certificate format:** a single physical pair and all its spatial rotations can cover at most ONE of the thirteen disjoint orbits. Any orbit-saturated physical witness scheme must therefore contain **at least thirteen seed pairs** with support representatives in different orbits. One actual verified word pair in each orbit suffices; this yields a human-sized 13-seed verification target rather than 220 unrelated word pairs. The standalone fail-closed verifier now calculates the number of physically covered orbits from its supplied manifest and still requires `220/220` actual supports to claim completion.

### Historical partial baseline (superseded by current 220/220 replay)

The historical radius-three pair is:

```
A = U R2 U'
B = D B2 D'
```

The 48-sticker physical checker verifies both length-three words, exactly three originally different oriented edge factors, no changed corners, and **12** distinct triple-edge support sets from 24 word-rotation/replay executions. It prints **208 missing supports** and `full_220_certificate=false`. This is deliberately partial, *not* a B5 result.

Run:

```bash
python scripts/cuberev-observation/verify_b5_three_edge_physical_manifest.py --demo-b3
python -m unittest discover -s scripts/cuberev-observation -p 'test_b5_three_edge_physical_manifest.py' -v
python scripts/cuberev-observation/verify_b5_three_edge_physical_manifest.py /path/to/B5_all_seed_words.json
```

The final command must only print `COMPLETE_B5_220_PHYSICAL_REPLAY` once independent physical 220/220 replay actually succeeds.

## Distinguish scientific status

1. **Exact b6^(1)=19 proof conditional on historical B5 220-triple physical certification**: already documented in `B6_SINGLE_ERASURE_ROBUSTNESS_19_TAG_THEOREM.md`; the 18-tag impossibility is not deduced from invalid 16-core converse.
2. **New standalone physical corner-pair midpoint replay**: already performed on both 12-HTM words using 48 stickers; 16 two-corner pairs by rotation.
3. **New B5 independent 220/220 physical witness replay**: **CLOSED via newly discovered independent 13-seed source**, 220/220 physically replayed; the older 12/220 demonstration remains a negative control. This is a transparent reproducibility improvement, not an announcement that the 220 physical certificates were recovered or independently rechecked.

This gate supplies a source-independent test interface that can take the already archived original B5 seeds, without enumerating all 621,649 B5 states or silently treating an abstract list of 220 triples as physical evidence.
