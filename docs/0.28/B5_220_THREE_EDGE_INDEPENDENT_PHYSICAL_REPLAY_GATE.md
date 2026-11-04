# CUBE-REV 0.28 — Physical re-certification gate for the B5 220 original-edge triples

**2026-11-04. Status: independent B3 12/220 partial example replayed in CI; B5 220/220 independent replay NOT YET claimed.**

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

The historical original B5 archive contains the nine B5-new physical pairs and original B4 seeds, but an extracted all-orbit representative manifest has **not** been loaded and replayed by this new source yet. This script does not pretend to have those original moves.

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

### Verified partial baseline

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
3. **New B5 independent 220/220 physical witness replay**: **OPEN**. Only the B3 seed orbit 12/220 has been independently replayed by the new strict manifest contract. This is a transparent reproducibility improvement, not an announcement that the 220 physical certificates were recovered or independently rechecked.

This gate supplies a source-independent test interface that can take the already archived original B5 seeds, without enumerating all 621,649 B5 states or silently treating an abstract list of 220 triples as physical evidence.
