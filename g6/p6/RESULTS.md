# CUBE-REV Generation VI G6-P6 — Results

## Exact executable authority

- science HEAD: `2a58f8abb8154310493107486a5461d176938884`
- GitHub Actions run: `36658377775` — SUCCESS
- artifact: `11072663871`
- artifact digest: `sha256:9ed65afd496e2762e0b9fb5128759e7f3987a701268b8be65aeba47595d2de48`
- same-head gates: rustfmt, workspace check/tests, G6-P1, G6-P2, G6-P6, G5-P5-R3, G5-P6 — all PASS

## Frozen local domain

The exact P6 court is the full-cube slice:

- `dG=3`
- phase-1 `d1=2`
- `960` full states
- exact phase-2 BFS authority through radius `6`

The executable receipt reports:

- shortest entry-cost profile classes: **3**
- one-slack frontier profile classes: **4**
- regret-positive states: **928 / 960**
- hard shortest-entry states: **32 / 960**
- distinct phase-1 q coordinates in the slice: **50**
- same-q coordinates that split into multiple shortest-entry regret classes: **2**
- maximum same-q regret strata: **2**

## Cost-sufficient fiber result

The shortest endpoint-cost fiber compresses literal endpoint identity while preserving the local shortest-entry cost claim.

The three exact shortest-entry profiles are:

1. 864 states: two endpoints with `d2=(1,2)`
2. 64 states: four endpoints with `d2=(1,2,2,3)`
3. 32 states: four endpoints, all certified `d2>6`

Thus literal G1 endpoint identity is stronger than needed for the scalar local cost question, but phase-1 q alone is too weak.

## Same-q regret stratification

Deterministic witness:

- `U R L`
- `R L U2`

Both have

`q=(twist=1906, flip=0, slice=21)`

and `d1=2`, but their shortest-entry cost fibers differ:

- `U R L`: `(1,2,2,3)`
- `R L U2`: four endpoints all `d2>6`

So exact phase-1 state sufficiency does not imply two-phase cost sufficiency.

## Slack-frontier result

The shortest-entry target and the +1-slack target are distinct representation contracts.

For the hard class, the executable non-vacuous witness is:

`R' L U2`

- shortest first-hit total: `>=9`
- +1 phase-1 slack, excluding solved endpoint: total `4`

Hence one additional phase-1 move can improve the bounded non-vacuous total by at least five moves.

Solved-during-phase-1 remains a separate vacuity control.

## C4 symmetry compression

On the frozen 960-state slice:

- C4 orbits: **248**
- compression ratio: **3.870968**
- orbit-size 2: **16**
- orbit-size 4: **232**
- cost-signature conflicts under C4: **0**

The executable C4 result is a positive-control subgroup of the broader D4h transport argument. No full 16-element D4h implementation census is claimed.

## Generation-VI synthesis

The tested 3×3 representation ladder is:

`weak projected PDB -> exact q/d1 -> shortest endpoint-cost fiber -> slack frontier -> full state`

Each level preserves a different Cube-search claim.

The scientific consequence is Cube-specific and directly reusable for cognition:

- phase coordinates expose boundary reachability;
- endpoint-cost fibers expose handoff quality;
- slack frontiers expose planning horizon allocation;
- symmetry orbits remove redundant search structure;
- same-q / different-fiber states provide matched candidates for future human planning experiments.

No machine representation is identified with a human cognitive representation.

## Authority ceiling

No claim is made about:

- global frequency over all legal 3×3 states;
- globally minimal cost-sufficient representation;
- exact d2 beyond the radius-6 authority;
- full D4h implementation census;
- human behavioral equivalence.

P4-R4 viewpoint/mixed-radix remains BLOCKED.
G4-R2 provenance remains HOLD.
Human world contact remains CLOSED.
