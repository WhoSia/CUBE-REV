# CUBE-REV Secondary-Data Frontier

Canonical operating rule from G3-P14: **existing human behavioral telemetry is the default world-contact surface; bespoke human collection is reserve only.**

## Storage roles

- **GitHub (`research/data-spine`)**: schemas, manifests, acquisition recipes, hashes, data dictionaries, derived-table builders, analysis code, release metadata. No large raw datasets.
- **Google Drive (`CUBE-REV/20_SECONDARY_DATA_FRONTIER`)**: immutable raw snapshots, large intermediate tables, license/source receipts, release candidates.
- **Zenodo/Kaggle later**: release packages only after license review and scientific freeze. Prefer portable CSV/Parquet + README + data dictionary + provenance manifest + code DOI. Never re-host raw data when source terms do not permit it.

## Drive layout

- `00_REGISTRY_AND_LICENSES/`
- `10_RAW_SNAPSHOTS/`
- `20_DERIVED_TABLES/`
- `30_RELEASE_CANDIDATES/`

## Admission rule

A corpus must expose a falsifiable estimand, not merely large N. Score question fit, temporal/action granularity, repeated-measure depth, natural contrasts, scale, selection/censoring auditability, license/provenance stability, source independence, and incremental information.

## Authority ladder

- T0 population geometry
- T1 within-person dynamics
- T2 natural/quasi-experimental contrasts
- T3 cross-corpus convergence
- T4 cognitive/physiological bridge

No claim may be promoted merely because a dataset is large or biomedical.

## Active acquisition order

1. **WCA Results Export v2** — primary population-performance spine.
2. **Existing CUBE reconstruction/BLE corpora** — primary move-level mechanism spine.
3. **Aalto 136M Keystrokes** — large external motor-control comparator.
4. **EdNet** — large sequential learning/control comparator.
5. **Duolingo learning traces** — spaced-repetition/history comparator.
6. **How We Type** — deep multimodal mechanism bridge.
7. **OpenNeuro / PhysioNet** — question-first neural/physiological bridge only.
8. **StarData / other game telemetry** — reserve comparator; not a default expansion lane.

Bulk download is forbidden until the corresponding row in `registry.yaml` is promoted to `ACQUIRE` with a named estimand and license/release plan.