# Portable release layout

Target: a research package that can be deposited on Zenodo and mirrored to Kaggle when licensing permits.

```text
CUBE_REV_DATA_RELEASE_<version>/
├── README.md
├── CITATION.cff
├── LICENSE_CODE
├── DATA_USE_NOTICE.md
├── manifest.json
├── checksums.sha256
├── source_registry.csv
├── data_dictionary/
│   ├── tables.md
│   └── variables.csv
├── acquisition/
│   ├── fetch_<source>.py
│   └── SOURCE_RECEIPTS/
├── schemas/
├── derived/
│   ├── parquet/
│   └── csv_small/
├── analyses/
├── figures/
└── tests/
```

## Raw-data rule

Raw source bytes are included only when source terms explicitly permit redistribution and privacy risk is acceptable. Otherwise the release contains immutable source metadata, version/date, URL/DOI, hashes when obtainable, acquisition code, and independently reproducible derived outputs that are lawful to share.

## Format rule

- Parquet = primary large derived tables.
- CSV = compact human-readable extracts only.
- JSON/YAML = manifests and schema contracts.
- UTF-8 everywhere.
- Stable opaque row IDs for derived records; do not propagate unnecessary source identifiers.

## Provenance minimum

Every derived table records:
- source corpus + source version/date;
- raw snapshot hash or source receipt;
- compiler commit SHA;
- schema version;
- deterministic transformation command;
- row/column counts;
- exclusions and missingness rules;
- license/republication class.

## Repository rule

GitHub stores code and small metadata, never bulk raw data. Google Drive is the working byte store. Public repository deposits are generated from a frozen release candidate, never directly from mutable working folders.
