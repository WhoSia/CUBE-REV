# Paper 1 frozen claim surface

## C1 — Replay authority
- Recovered ordered records: 1,890
- Center-relative terminal solved replay: 1,890/1,890
- Frozen Paper-1 CFOP denominator: 1,625
- Interpretation: exactness is conditional on recorded notation under the deterministic replay rules, not independent sensor ground truth.

## C2 — Reconstructed turnover
- Frontier segments: 5,466
- Q=0: 5,120
- Q>0: 346
- Q-positive solves: 327
- Solver identities represented among Q-positive segments: 39
- Reconstructors represented among Q-positive segments: 17
- Q-positive by starting frontier k=1/2/3: 46 / 72 / 228
- All observed Q-positive segments have Q=1; no impossibility or population claim is made about Q=2.

## C3 — Same-scalar / opposite-Q witnesses
- Distinct complete scalar signatures: 668
- Signatures observed with both Q=0 and Q>0: 12
- Segments in mixed complete-scalar signatures: 180 = 142 Q0 + 38 Q+
- Q+ rows with an opposite-Q same-scalar twin: same solver 17; same reconstructor 29; same solver + reconstructor 16.
- Frozen Figure-1 witness: recon 230 vs recon 2414, Yiheng Wang, reconstructor Ruimin Yan, k=3→4, D=4, scalar sequence `3,3,1,2,4`, Q=1 vs Q=0.

Pair paths for the Figure-1 witness:
- recon 230, Q=1: `BR|GO|GR → BO|GO|GR → GR → BR|GR → BO|BR|GO|GR`
- recon 2414, Q=0: `BR|GO|GR → BR|GO|GR → GO → BO|GO → BO|BR|GO|GR`

## C4 — Coarser observation ambiguity
- O_dwell=(k,k′,D): 110 observed signatures; 45 mixed; 339/346 Q+ segments fall in mixed cells.
- O_record=(k,k′): every Q+ segment, 346/346, falls in a cell that also contains Q0.
- These are archive witness-coverage counts, not theoretical ambiguity probabilities or population estimates.

## C5 — Structural noninjectivity
For a fixed cross, `π(S)=|S|` has pair-set preimage multiplicities:
- k=1: 4
- k=2: 6
- k=3: 4

Therefore scalar solved-pair count cannot generally identify pair identity or the underlying reconstructed pair-state path.

## Source concentration
Ruimin Yan accounts for 313/346 Q-positive reconstructed segments. Turnover also occurs outside this source, but source/reconstructor equivalence is not claimed.
