# CUBE-REV Paper 1 M1.1 — Public Byte Verification Receipt

Zenodo record: https://zenodo.org/records/22164926
DOI: 10.5281/zenodo.22164926
Verified downloaded filename: `CUBE_REV_PAPER1_M1.1_FULL_REPRO_PACKAGE (1).zip`
Expected pre-upload SHA-256: `34b5bd932dae99635f0f82caa50234c96c994fc4d36d24cc7d50206fb33254a2`
Observed post-download SHA-256: `34b5bd932dae99635f0f82caa50234c96c994fc4d36d24cc7d50206fb33254a2`
Byte identity: PASS
ZIP integrity test: PASS
Internal `SHA256SUMS`: 23/23 PASS
Standalone reproduction command: `python code/reproduce_paper1.py`
Observed stdout: `CUBE_REV_PAPER1_M1_1_REPRO_PASS`
Return code: 0
Public reproduction authority: PASS

Notes:
- The M1.1 ZIP was frozen before the DOI itself existed, so the internal release manifest retains a pre-mint `PENDING_M1_1_RELEASE` field. The immutable public Zenodo record and this post-release receipt bind the frozen byte package to DOI `10.5281/zenodo.22164926` without rewriting historical package bytes.
- Raw third-party CubeRoot source bytes are not redistributed. The public package contains the frozen derived analysis surface, deterministic verifier, figure inputs/figures, provenance and source-rights documentation.
- No new empirical claim was added during M1.1 release verification.
