# CUBE-REV 0.29 — AX archival preseal and Lean-first active tree (2026-11-22)

## Verifiable custody

- Source commit (before retirement): `5fe57052c427be35a3e749a52ae0a57d4f7cb55a`.
- GitHub Actions read-only source-custody run: https://github.com/WhoSia/CUBE-REV/actions/runs/44926929951
- Actions artifact ID: `14715702188`; outer ZIP SHA-256: `sha256:7c0ba12222a370263b77e60c46732bcbea91189d251fe2c00c2dcaf079d668cc`.
- Google Drive canonical retirement ZIP: https://drive.google.com/file/d/1KNVij3D3DQDicKoJ_rNSBl5aKJMuPMVQ/view
- Target folder: https://drive.google.com/drive/folders/1xpUKiXclYvGGPMpE9dVDhp2lOc_YJzRS
- The ZIP contains `MANIFEST.json` (10 historical file paths, original Git blob IDs, byte counts and individual SHA-256 digests) and `exact-historical-source.tar.gz` with the unchanged original bytes. All 10 extracted files were checked against manifest hashes; Drive raw-file round trip reproduced exactly the 39,493-byte ZIP and its SHA-256.

## Exact limited cut

The active `research/current` branch retired only 10 historic README/version manuscripts under `archive/readme/**` and `archive/versions/**`, plus the one-shot archival workflow after it completed. Those files are not Lean modules, Python evidence auditors or current execution dependencies. They remain recoverable from the Drive ZIP and the immutable pre-retirement commit. No current `formal/029` file, 0.29 source, 0.29 certificate or executable workflow was removed.

The strict P7 `allowed_paths` inventory is reconciled in the same atomic tree update. The archive workflow was read-only and created no bot-authored Git commit; its artifact is preserved in Drive beyond the GitHub retention window.

## Lean-first migration boundary

Do not delete historical Python experiments solely because the suffix is `.py`. For each candidate, check whether the current CI imports/calls it, whether it produces irreplaceable raw evidence, and whether its theorem-relevant outputs have already been reflected in the pinned Lean package. The priority is Lean kernel theorems + tiny immutable replay inputs, with Python retained for independent external cross-checks, adversarial mutation and certificate packaging. A Python implementation cannot be called replaced by Lean until the new Lean theorem, explicit axiom audit and read-only CI complete.
