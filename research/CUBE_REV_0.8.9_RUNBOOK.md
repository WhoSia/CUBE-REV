# CUBE-REV 0.8.9 Rerun Runbook

## Checkpoint A — branch stack

```text
base: cube-rev-0.8.8-immutable-submission-snapshot
head: cube-rev-0.8.9-public-bank-minimization
PR: #8
```

## Checkpoint B — materialize artifacts

From the repository root:

```bash
node scripts/build_0_8_9_public_bank.js
```

Required marker:

```text
CR0809_PUBLIC_BANK_BUILD_PASS stimuli=28 choices=504
```

Expected generated public files:

- `cognitive/PARTICIPANT_STIMULUS_BANK_0.8.9.json`
- `cognitive/COGNITIVE_MODE_CONFIG_0.8.9.json`
- `research/CUBE_REV_0.8.9_BUILD_MANIFEST.json`

Expected generated private file:

- `.cube-rev-private/PRIVATE_CROSSWALK_0.8.9.json`

The private file must exist locally for reconstruction tests but must be ignored and untracked.

## Checkpoint C — executable certification

```bash
node tests/public_bank_minimization_0.8.9.test.js
node tests/immutable_snapshot_contract_0.8.8.test.js
```

Required markers:

```text
CR0809_PUBLIC_BANK_CERT_PASS 8/8
CR0808_IMMUTABLE_SNAPSHOT_PASS 8/8
```

## Checkpoint D — syntax

```bash
node --check scripts/build_0_8_9_public_bank.js
node --check scripts/reconstruct_0_8_9_factory.js
node --check js/participant-cognitive-mode-0.8.9.js
node --check tests/public_bank_minimization_0.8.9.test.js
```

The inline script in `participant-cognitive-mode-0.8.9.html` must also be parsed in a browser smoke test or extracted and checked separately.

## Checkpoint E — public/private boundary

```bash
git check-ignore .cube-rev-private/PRIVATE_CROSSWALK_0.8.9.json
git ls-files | grep -E 'PRIVATE_CROSSWALK|\.cube-rev-private|research-private'
```

The first command must succeed. The second command must return no tracked private paths.

The public stimulus bank must contain none of:

```text
state_id rotation_id face_map choice_canonical canonical_move
pair_id member_id probe_name diagnostic_class branch_count
branch_level decision_class distance
```

## Checkpoint F — Factory reconstruction

Prepare a completed 0.8.9 payload, then run:

```bash
node scripts/reconstruct_0_8_9_factory.js \
  payload.json \
  .cube-rev-private/PRIVATE_CROSSWALK_0.8.9.json \
  reconstructed.json
```

Required marker for a 28-response session:

```text
CR0809_FACTORY_RECONSTRUCTION_PASS rows=28
```

Display/code disagreement or an unknown code must terminate with a nonzero exit.

## Checkpoint G — immutable manifest identities

Compare generated artifacts against `research/CUBE_REV_0.8.9_BUILD_MANIFEST.json`. A hash mismatch blocks promotion. The private crosswalk may be stored outside the repository, but its SHA-256 must match the manifest before Factory use.

## External stop gates

Automatic continuation stops for:

- live Factory ingestion with the protected crosswalk;
- live Collector POST from the participant route;
- owner mobile/desktop walkthrough;
- production default-entry change;
- final custody location and access policy for the private crosswalk.

## Promotion rule

Passing local/CI checkpoints certifies the artifact and reconstruction contracts, not production deployment. Production remains `NO_GO` until the external stop gates are explicitly completed and authorized.
