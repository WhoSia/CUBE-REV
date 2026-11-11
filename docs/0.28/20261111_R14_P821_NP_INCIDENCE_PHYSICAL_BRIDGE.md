# CUBE-REV R14-P8.21 — Exact N–P Collision Timing from 3D Incidence and P48 Witnesses

Date 2026-11-11. Status: independently executed 3D seed-orbit geometry PASS; new source-independent 48-moving-sticker P48 full-physical replay script and read-only workflow WRITTEN but remote job result not observed. No new full B12 41-goal distance replay.

## 1. Explicit N–P first-failure law

For each original cube edge h, N(h) has four edges incident to an endpoint of h, while P(h) has two side-parallel edges distinct from h and its opposite. Given n in N(h) and p in P(h), let their endpoint sets be ∂n, ∂p.

NEW LOCAL GEOMETRIC LAW within this N–P SECTOR ONLY: the omitted-original-tag 16-sensor layout omitting ∂h and n,p ALREADY FAILS on B5 if ∂n∩∂p is empty; when ∂n∩∂p is nonempty it SURVIVES B5 but fails B6. For each h, four old and four new failures; across 12 native core edges 48+48=96. The law is not asserted beyond N–P or before P48 source-level receipt is inspected.

Concrete h=DL: near edges BL,DB,DF,FL and side-parallel DR,UL. Already B5-failing nonmeeting pairs: BL-DR, DB-UL, DF-UL, FL-DR. Newly B6-failing meeting pairs: BL-UL, DB-DR, DF-DR, FL-UL.

## 2. Independent calculation already EXECUTED

A separate local Python checker built the six face-normal 3D cube graph from scratch, represented all 12 original edges by spatial midpoints and endpoints, independently generated all 24 orientation-preserving signed coordinate rotations, and rotated all nine original P48 B5 5+5-HTM word-pair support labels recorded in verify_b6_complete_4845_p48.py. It recovered exactly 216 unique B5 support labels and checked all 12 cores x 8 N–P choices. Every one obeyed B5-invalid ⇔ ∂n and ∂p are disjoint, with 48 old and 48 new. PASS. The local geometry code does not independently reconstruct the 48 moving-sticker word endpoints: that is a distinct remaining verification gate.

## 3. Existing P48 physical seeds remove the former B5 ZIP blocker

Important correction to P8.20: the missing original historical B5 54-facelet ZIP is NOT necessary to compute actual 5+5 physical B5 N–P witnesses. Nine explicit P48-derived B5 seed word pairs were already committed in scripts/cuberev-observation/verify_b6_complete_4845_p48.py. Nineteen separate P48 B6 seed pairs are in scripts/cuberev-observation/verify_b6_negative_19_pairs_p48.py.

NEW scripts/cuberev-observation/audit_r14_p821_np_explicit_p48.py calls the actual 48-moving-sticker physical replay functions adjacent_b5_obstructions() and adjacent_b6_obstructions(); each performs all proper-rotation physical word transports and returns respectively 216 old and 420 new actual four-tag supports. The new script tests all 96 individual N–P pairs against these independently replayed outcomes FIRST, and checks the shared-endpoint geometric criterion SECOND, yielding a per-core explicit JSON witness ledger plus SHA256 of exact source seed text. It does not falsely mark old historical B5 ZIP as a prerequisite.

New read-only workflow .github/workflows/cuberev-r14-p821-np-physical-bridge.yml runs the P48 replay and uploads JSON. Remote CI PASS remains UNOBSERVED. No new original 41-class B12 positive proof or completely independent original physical source engine is claimed.

## 4. Prior work versus genuine research novelty

Pre-existing in repository since November 4: b5=b6=16; 576 B5-positive versus 156 B6-positive selected 16-tag designs; 420 newly invalid; original physical 216 B5 and 420 B6 2C2E witness supports; coarse N–P split 4 old/4 new.

New this research turn: specific N–P PAIR IDENTITIES and an exact concise shared-endpoint geometric discriminator, independently tested on 24 rotational coordinates, plus a fully specified P48 original-witness replay workflow that can proceed even without the inaccessible historical ZIP. This is a local structural lemma and does not independently justify another article.

## 5. Open next theorem gate

Develop a complete first-failure radius rule rcrit(S) for all 66 2C2E omitted-edge candidate pairs at a fixed core h, beyond the four shared N–P examples. This requires actual P48 physical witnesses and 41-class positive checks, not simply a category table. Compare minimum-versus-inclusionwise-minimal sensor spectra of B5 and B6 only after B5 full classification. Full-color 19-frame unrestricted adaptive question remains separate and OPEN.

## 6. Raw archive custody

Still unresolved: original CUBE_REV_20261030_EXACT_B1_B5_SENSOR_CERTIFICATES.zip historical SHA256 002887a198bac812ad360ba536309f2522899d5c28d12fb73bb92062ae889c94 (targeted Drive search negative); archive is now needed for original historical byte/source audit, NOT for independent P48 N–P collision membership. Other physical-certificate release gates remain 41 target B12 MITM raw receipts, 872 support witness provenance, and entire Paper B conditional 609376-family replay.

No new PDF intake or moves. All source written on research/current as WhoSia human GitHub commits; CI read-only.
