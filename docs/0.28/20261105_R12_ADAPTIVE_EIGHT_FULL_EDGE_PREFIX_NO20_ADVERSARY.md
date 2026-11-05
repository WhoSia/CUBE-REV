# CUBE-REV 0.28 — R12: A Universal Adversary Against Eight-Fully-Observed-Edges-First Policies

**Date:** 2026-11-05. **Status:** mathematical restricted-class impossibility proof + reproducible physical P48 adversarial completions. Remote GitHub Actions still QUEUED at time of writing, so do not invent remote PASS. The full two-probe adaptive horizon remains 18–21; this is NOT a proof that 20-frame identification is impossible for all policies.

## Why we need a sharper negative result

R11 constructs a fully joint, no-corner-oracle, legal-turn adaptive 21-frame full-cube identifier by using the first 16 edge color frames to read eight complete spatial edge positions and, in parallel, the first 14 corner color frames to reconstruct all eight corners. It then runs the R9 exact residual four-edge decision tree, requiring three, four, or five further observations depending on the four remaining edge-color types. R8/R9 identified 54 bad four-edge label sets (six K1,4 stars and 48 triangle-with-pendant graphs) requiring five reads even if the entire corner state is known and any remaining edge facelet can be read for free.

An apparent 20-frame workaround is to choose WHICH eight edge positions to read in the first sixteen frames *adaptively*, in hope of arranging that the remaining four source edge labels never belong to those 54 bad sets. R12 eliminates this entire workaround, without claiming a complete global impossibility.

## Restricted policy class

Let a full-cube two-probe deterministic policy make at most 20 observation frames, with known legal 18-HTM actions, full history-dependent feedback, any information gathered by the simultaneous corner sensor, and unlimited computational memory. Suppose its **first 16 edge-sensor readings are precisely two distinct facelet slots at each of eight distinct initial spatial edge positions**, with no edge-sensor readings at the remaining four positions. The order of querying individual facelets and the chosen eight positions may adapt to previous sensor results; in particular, the policy need not choose all eight positions before seeing any colors.

The true initial corner configuration can be revealed for free as an additional oracle; this only strengthens the policy. The extra oracle does not affect the lower bound.

## Theorem (structural prefix obstruction)

**No such eight-complete-edges-first policy can guarantee zero-error identification of all legal 3×3×3 Rubik states within 20 edge/corner color observation frames.** In fact, for at least one physically legal state and corresponding first-16 response history, its remaining edge belief cannot be separated in four further single-color edge readings, even if the complete corner state is known and the physical edge sensor has arbitrary free access to any remaining facelet.

### Proof

1. Choose any of the 54 obstructing four-original-edge-type sets \(L\). Write \(C\) for the eight other original edge types. Fix a complete legal corner configuration in advance; take solved corners for convenience. Because a known legal action transports the stationary edge probe to a known **initial spatial** facelet slot, the choice of that slot may be determined from previous colors without reference to the unknown edge permutation.
2. Answer the policy online as follows: when it first probes an as-yet-unvisited initial spatial edge position, assign one previously unused type from \(C\) to that position, with a chosen physically admissible flip (e.g. zero), and return the corresponding actual sticker color. Its second probe at that position is answered consistently. The next spatial position may depend arbitrarily on the previous edge/corner symbols. The adversary always has enough unused types from \(C\): the policy visits exactly eight distinct positions and \(|C|=8\).
3. At the end of the first sixteen readings, the eight observed positions contain exactly the eight types from \(C\), and the four unread positions must contain exactly the four types from \(L\). Because none of the four remaining spatial positions has been read, **every remaining assignment and flip configuration** compatible with the already fixed corner permutation parity and edge-flip sum has the same first-16 color history. There are \(4!/2\times2^3=96\) such legal completions. One can always choose a remaining assignment of the required parity, and choose the remaining four edge flips with even total parity. These are legal Rubik states; the true corner state is common to all of them. Thus no corner color readout or known turn can separate these candidate edge states for free.
4. For all 54 selected \(L\), the exact R8/R9 minimax decision-tree certificate shows that five more single edge-facelet six-color results are needed in the worst case to separate these 96 completions **even allowing free access to arbitrary initial edge slots**. The physical two-probe action policy is weaker than this relaxed oracle.
5. Therefore at least one of the 96 completions forces \(16+5=21\) total frames. This contradicts a uniform 20-frame guarantee for the restricted prefix policy class.

The proof is an online adversary induction for *every deterministic adaptive prefix policy* meeting the structural condition. It is not a finite random simulation presented as a universal lower theorem.

The proof extends to zero-error randomized policies under a strict worst-case guarantee over their random choices, but we make no probabilistic or expected-depth claim.

## Executable physical sanity check

[R12 P48 adversarial completion source](../../scripts/cuberev-observation/audit_r12_eight_full_edge_prefix_adversary.py) constructs 96 distinct physically legal example states across two distinct obstructing graph shapes, three different prefix position selectors and sixteen deterministic selectors' salts. For each, it assigns observed edge labels online from the complement, completes the four unread labels with the correct legal corner/edge permutation parity, checks P48 physical sticker colors, confirms even edge-flip sum and all-corner solved constraints, and invokes R8's exact five-read residual minimax result. This program is an executable **witness sanity check**, while the quantified theorem is established by the online adversary reasoning above. Source was added to the P7 active-set allowlist and read-only CI; remote CI is not called passed until the run actually completes.

## R12 consequence for R13 research design

A universal 20-frame full-cube identifying policy, IF one exists, cannot use the natural 16-complete-edge prefix no matter how adaptively those eight positions are chosen. Within 16 edge readings it must either:
- query more than eight distinct edge positions, leaving at least one only partially observed; or
- use some other non-eight-complete pattern including repeated/inefficient choices (which cannot trivially improve information capacity and would require separate justification).

This is a necessary condition on candidate full-group 20-frame policies, not a sufficiency claim. It points to **interleaved partial-color strategies across nine or more edge positions** as the next hard research frontier, together with actual corner parity knowledge by frame 14 via R11.

A meaningful next theorem must certify a full 20-frame policy with both physical color sensors and no free corner oracle, OR exhibit a policy-wise adaptive indistinguishable-pair obstruction for all 20-frame strategies. Do not retreat into easy smaller B2 optimization just because a proof is hard.

## Human-origin boundaries

The cube color oracle does not record gaze, internal working-memory state, response time or motor decision costs. Exact two-probe mathematical ambiguity is a benchmark, not an observed human cognitive effect. The earlier CUBE-REV 0.21 strict matched-state/history naturalistic sample had zero comparable matched previous-action pairs. This non-overlap limitation survives every mathematical proof in R11/R12.

**Custody:** WhoSia-authored source and notes, P7 exact active-set checked separately, Actions read-only, Notion scientific decision record, Drive for irreplaceable source records. Mark CI QUEUED/FAIL/PASS truthfully; no GitHub Actions bot source commits.


## R14 extension — seven-complete-edge prefix by frame 14 (2026-11-05)

**Stronger, still restricted impossibility theorem.** For the same
zero-error full legal cube, edge/corner two-color probe and known legal-turn
actions as above, consider any deterministic feedback policy whose first
**14 edge-facelet readings cover exactly seven spatial edge positions,
both distinct facelets at each position**. The seven positions, their
read order, and all choices may depend on preceding edge and corner
outputs. Such a policy **cannot** guarantee identification within
20 frames. This is strictly broader than a fixed preselected seven-edge
prefix, and it also cuts off this prefix class *before* the existing
R12 16-read/eight-complete gate.

**Adversary/proof.** The policy is allowed the complete true corner state
for free, and each remaining initial spatial edge facelet may subsequently
be queried at zero turn cost. Fix solved corners and fix the five-edge
type set

`L = {UR, UF, UL, UB, FR}`.

Let `C` be its seven-edge-type complement. For every first encounter
with a new spatial edge position during the 14-query prefix, choose an
unused label from `C` and a legal orientation, and report the actual
color. The policy may revisit previously seen positions in any adaptive
order. Because the first 14 queries eventually cover precisely seven
fully read positions and **no other** edge positions, this process
assigns every label of `C` consistently. All other five spatial edge
positions are unobserved and have exactly label set `L`. The
already assigned edge labels and known true corner permutation fix
the residual permutation parity; the total edge-flip constraint fixes
the residual flip parity. For each of the four possible parity pairs
the whole residual belief contains

`(5!/2) * 2^4 = 960`

distinct legal assignments, all compatible with the identical first-14
edge/corner transcript. No earlier corner observation can distinguish
them, since every completion uses the identical solved corner state.

The existing R11 exact ten-facelet adaptive minimax court for `L`
proves six further free-position edge-color readings insufficient, and
seven sufficient, for **all four** residual parity combinations.
Consequently some physically legal cube defeats any depth-20
policy from this prefix family, because `14 + 7 = 21`.

**Scientific novelty ledger.** The precise 960-state, six-read negative
and seven-read positive result already appears in the prior R11
fixed-prefix five-edge court; it is **not** new in R14. The genuine
new deduction here is extending the obstruction to **all adaptively
chosen/ordered seven-complete-position first-14 prefixes** using an
online remaining-label adversary. This is not a global depth-20
impossibility proof. A successful 20-frame joint policy, if one exists,
must therefore avoid completing seven entire edge positions within its
first 14 edge queries. It must spread observations partially or use
another policy class.

**Reproduction and custody.** The existing active-set R12 source
`scripts/cuberev-observation/audit_r12_eight_full_edge_prefix_adversary.py`
contains `audit_r14_seven_complete_prefix_gate()` to check all four
parity cases using the current R11 solver. A separate, **repository-
independent**, Python stdlib 960-state minimax and seven-query replay is
preserved on Drive in the lab's canonical proof-court folder:

- [Independent R14 source (.py)](https://drive.google.com/file/d/1faz1MgjNJqLv9I4nm0ay1esUP4QxcCRt/view)
- [Independent R14 output receipt](https://drive.google.com/file/d/1Lnr5l1hqVBMoxkuR9mNKg25fkaHvIba6/view)

The independent source is a *color-label parity model*, not an
independent P48 physical coordinate implementation. The P48-derived
edge type labeling and its physical realization are inherited from
R11/R12; global physical zero-error claims need those audited links.
The independent local run passed. The two R14 seven-prefix files
were independently downloaded as RAW bytes from Drive; exact SHA-256
comparisons against original source succeeded:
- Independent Python: `a07b416cb6a2b479083f3dcf5134cac78fa235f0874399d3833cb9b5646fb18e` (4,651 bytes).
- Residual minimax receipt: `9ff354c6984d3e18380f83a26188005adb8f689b666d83d86d6862ad8a95f17e` (2,272 bytes).
The earlier two R14 color-orbit artifacts were likewise raw-byte SHA-verified.
Thus Drive status is **BYTE_VERIFIED** for all four. The remote GitHub
Actions result for this **new** R14 entry remains UNCONFIRMED; raw Drive
custody does not substitute for remote code execution certification.


## R14-P2 extension — six-complete-edge prefix by frame 12 (2026-11-05)

**New restricted finite computational theorem (local independent PASS, remote
CI not yet certified).** Any deterministic zero-error full-cube two-probe
policy whose first **twelve** edge-sensor readouts consist of the two
distinct facelets at each of precisely **six** spatial initial edge
positions cannot guarantee completion in at most twenty frames. Both
the six visited positions and the order of the first twelve reads may
depend on earlier edge/corner sensor outcomes. This is an independent
earlier-prefix gate, not a proof against all mixed observation policies.

**Online adversary.** Fix the entire true corner state (give it to the
policy for free). Let the six hard unseen original edge color types be

`L={UR,UF,UL,UB,FR,FL}`.

As the first twelve readouts encounter six previously unseen spatial
edge positions, assign unused edge types from the six-element complement

`C={DR,DF,DL,DB,BL,BR}`,

with fixed consistent orientations and actual sticker outputs. This is
consistent with any deterministic adaptive choice/order in the
restricted class. All five hundred? **No**: the unobserved region
comprises six spatial edge positions and exactly six original edge
types. Conditioned on the already observed type placements, fixed
corner permutation parity and total edge-flip parity, the number of
legal distinct completions is

`(6!/2) * 2^5 = 11,520`.

All these legal states have exactly the same first-twelve observation
history and the identical true corner state. Known physical actions
do not change this adversarial ambiguity: every fixed-probe reading
at a known turn prefix is a reading of a known initial spatial
facelet, so we may grant free access to **all** twelve remaining edge
facelet slots to strengthen the prospective observer.

**Exact residual finite court.** For each of 720 relative edge-piece
permutations of six labels and 64 flip choices, retain only the required
permutation and flip parity, yielding 11,520 complete 12-character
six-color readout words per parity pair. A fully explicit memoized
minimax decision-tree recurrence considers every next facelet query
q in 0..11 and branches on each physically realizable six-color value.
For a belief mask `B`, define `Win(B,d)` by
- true for a singleton;
- false for non-singletons when `d=0`;
- otherwise true iff some facelet q makes all nonempty outcome
  belief subsets `Win(B[q=c],d-1)`.
The `|B|>6^d` bound is used only as a sound **necessary condition**
for success, never as a positive proof.

Independent Python stdlib exact evaluation for L reports
`Win(B_full,8)=False` with **225,886 cached states** in the
(perm-parity=0, flip-parity=0) case, while a specific **fixed**
nine-query sequence `(0,1,2,3,4,5,6,7,8)` has exactly 11,520
distinct readout traces. Explicit facelet-coordinate permutations
interchanging the first two unknown edge positions and exchanging
the two facelet slots of the first position induce bijections among
all four parity-conditioned 11,520-state games. Hence all four parity
conditions have the same exact minimax value **nine**.

Thus every policy in the designated first-twelve/six-complete class
has a fully legal state forcing at least `12+9=21` frames even under
the stronger free-corner/free-facelet-read oracle.

**Limit and novelty control.** This does not assert that the full
mixed/adaptive two-probe game requires 21. To achieve <=20,
a policy must avoid completely reading six distinct spatial edges in
its first twelve edge queries and must also avoid completely reading
seven in its first fourteen, as independently shown by R14-P1.
The resulting residual 11,520-state six-edge computational lower
bound is **new to the present R14 court**, while the conditional
five-edge/960-state seven-read result used for P1 was preexisting R11
work. Further source-independent physical P48 equivalence and remote
CI verification are required before submission-level proof promotion.

**Canonical byte-preserved proof sources:**
- [Drive Python source](https://drive.google.com/file/d/1uMXpAtsFNkwKGOWiQ9sDY3ltyYijcJ2A/view) —
  4,148 raw bytes, SHA-256
  `2ef9b5f5f58640762192464428a3813c211d8976de71b5a81f6da73ee4f6b393`.
- [Drive exact receipt](https://drive.google.com/file/d/1im0UeRllW8eDruTaBS_9N6pFs0U7utFo/view) —
  938 raw bytes, SHA-256
  `e7858ad0bc7c6bf2354330ef523f2ba6d957ee92a000e804ec6db5442f5f54d5`.

Both files were independently downloaded again as raw Drive bytes and
matched these original SHA values. The source was also committed to
`scripts/cuberev-observation/audit_r14_six_complete_prefix.py`
with P7 exact active-set registration. No GitHub remote CI success is
claimed based on the local Python run or Drive readback.
