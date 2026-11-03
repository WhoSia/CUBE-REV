# B6 positive bases: 41 physically grounded HTM-distance obligations

Date: 2026-11-03. Status: finite exact reduction plus upper certificates.
The **new independent HTM >=13 lower-bound certificate is still OPEN**.

## Source contract and provenance

This work uses the existing 3x3 fixed-center Rubik cube group, the 18
quarter/inverse/half face-turn HTM generators, 20 original tagged cubies,
and full position+orientation sensor readout. It does NOT introduce
an alternative observation protocol or a new NP-hardness conjecture.

Primary archived physical source:
CUBE_REV_20261030_EXACT_B1_B5_SENSOR_CERTIFICATES.zip,
SHA256 002887a198bac812ad360ba536309f2522899d5c28d12fb73bb92062ae889c94.
The script dynamically reads archived independent_b4.py, whose 54-facelet
state action is distinct from its generated 20-factor coordinate view.

Historical B6 results: 156 previously verified 16-tag positive layouts,
8 proper-24 rotation orbits, 6 full-48 spatial symmetry orbits, and
8,240,087 distinct B6 states from the older independent positive census.
Historical geometrical rules are in verify_b6_geometric_rule.py. We do
not re-label these source results as new.

## Exact abstract reduction

For radius ball B_r and original oriented-cubie pointwise stabilizer H_S:

    sensor(S) is injective on B_r  <=>  H_S cap B_(2r) = {1}.

With exactly two omitted corner tags and two omitted edge tags, standard
cube legality gives |H_S|=2*3*2=12. The group is abstractly S3 x C2:
a complementary corner twist of order 3, a simultaneous corner+edge
transposition of order 2 which inverts the twist, and a central paired
edge flip of order 2. Thus 11 nonidentity elements need distance >=13
for B6 injectivity. This is an elementary group-structure derivation,
not a new general mathematical theorem.

The existing positive layouts have 8 proper-24 orbits. Choose the
following representatives with the omitted corner pair at the two
ends of original edge DL:

    omitted edges     proper orbit size
    BL, DF            12
    DB, DF            24
    DB, FL            12
    DR, UL            12
    FR, UF            24
    UB, UF            24
    UB, UR            24
    UF, UR            24

build_b6_stabilizer_goals.py constructs all 11 nonidentity standard
cubie-coordinate states for each representative, maps them to actual
54-byte facelet configurations, verifies selected original-tag readouts,
and optionally writes deterministic JSON containing all 88 goal
facelet hex strings and SHA256 hashes.

Physical convention validation:
- 1000 deterministic pseudorandom archived 54-facelet move states have
  perfect encode/decode round trips;
- all 18 x 18 consecutive face-turn pairs obey the cubie composition law;
- the existing 13-HTM UR/UF flip word equals a generated subgroup
  target **byte for byte**;
- 88 target entries contain only 74 distinct physical states since
  the same two pure corner-twist states recur in all eight layouts;
- inverse word lengths agree, reducing the 74 to 65 inverse classes.

A second independent verifier, audit_b6_full48_target_orbits.py,
implements all 48 signed coordinate permutation symmetries, checks all
48 x 18 = 864 face-turn covariance equations on the archived physical
facelets (including turn-direction inversion under reflection), and
quotients the targets by symmetry and inverses. This yields exactly
**41** distance-equivalence classes (sizes: 17 singleton, 19 double,
1 triple, 4 quadruple). It also regenerates 6 extended layout orbits
of sizes 12,24,24,24,24,48.

Canonical SHA256 of the concatenation of sorted lexicographically
smallest 54-byte facelet encodings of all 41 classes:

    c3dbf41177e16d8d0cb0cd76b433304e14f9cdac4a14f205d6231dc9dd8abc1e

This **41-class digest is a goal identity/consistency seal**, NOT a
cryptographic proof of non-reachability at length <=12.

## Constructive 13-HTM upper bound for 48 of the 156 B6-positive layouts

A previously documented 13-HTM word (prior art, not new algorithm):

    L F R' F' L' U2 R U R U' R2 U2 R

replays on the original 54-facelet model to flip precisely original
edge tags UR and UF and leave all other original tags unchanged.
All three historical 13-HTM variants give the **same physical state**.

Its 24 proper rigid cube rotations are 24 length-13 word certificates
for all adjacent unordered pairs of original edges. Each B6-successful
layout in the F-h* class omits one such adjacent pair; 12 core h choices
times 4 far spokes yield **48 layouts**, forming two proper-24 orbits
and one full-48 orbit.

The physical verifier verify_b6_13_edge_orbit.py checks all 24 conjugate
words and their exact original-tag support. Crucially it also constructs
physical *radius-7* state pairs by splitting each 13-turn word into a
7-move initial chronological segment and inverse of the remaining
6 moves, verifying both states have <=7 actions and their original-tag
difference support is exactly the predicted edge pair. Therefore every
one of these 48 layouts fails at B7, with an executable 6+7 witness.

For those 48 layouts, the existing B6-positive census proves no
nonidentity stabilizer state has length <=12, and the 13-move word gives
one at length <=13. Hence their least stabilizer length is **exactly 13**.
The >=13 part still inherits the previous full B6 census and does
NOT constitute a new independent geometric lower-bound proof.

## Research next gate: avoid the 8.24-million-state re-enumeration

Replace the inherited positive census, if feasible, by a genuinely
independent checker certifying none of these **41 word-metric classes**
has an HTM representative of length <=12. A physically checked
shortest-path lower-bound proof should include:
- full goal identification using the 54-byte target representation;
- a demonstrably admissible cubie-coordinate heuristic or verified
  bidirectional search / formal proof trace;
- independent factor-orientation and inverse-conjugacy regression;
- a bound on work and verifiable PASS output.

Neither the 41 targets nor the 13-HTM upper witnesses imply those 41
negative results. No new NP-hardness or generalized automata protocol
claim is made.

## Reproduce locally

    cd scripts/cuberev-observation
    python verify_b6_13_edge_orbit.py HISTORICAL_B1_B5_ARCHIVE.zip
    python build_b6_stabilizer_goals.py HISTORICAL_B1_B5_ARCHIVE.zip /tmp/b6_goal_manifest.json
    python audit_b6_full48_target_orbits.py HISTORICAL_B1_B5_ARCHIVE.zip

Archive is supplied separately; it is NOT uploaded to the GitHub repo.
All three commands were tested against the SHA256-matched archived
source locally in this research session. Remote GitHub Actions result
is separate and should not be inferred from commit creation.
