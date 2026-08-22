#!/usr/bin/env python3
from pathlib import Path
import json
src=Path('research/0.10.5-r1.8/r18_distance_null_calibration.mjs').read_text(encoding='utf-8')
repls={
  "sha(fs.readFileSync(MANIFEST_PATH))":"sha(fs.readFileSync(MANIFEST_PATH,'utf8'))",
  "sha(fs.readFileSync(NULL_FREEZE_PATH))":"sha(fs.readFileSync(NULL_FREEZE_PATH,'utf8'))",
  "let envelope=seg.actual_excursion;":"let envelope=seg.actual_candidate_reversal;",
  "const a=pathForMoves(seg.start,seg.target,z).excursion.max_excursion_amplitude;":"const a=pathForMoves(seg.start,seg.target,z).excursion.candidate_reversal_amplitude;",
  "const a=pathForMoves(seg.start,seg.target,altMoves).excursion.max_excursion_amplitude;":"const a=pathForMoves(seg.start,seg.target,altMoves).excursion.candidate_reversal_amplitude;",
  "null_aggregation:'one envelope observation per phase segment = max observed/accepted exact-transformation null realization',":"null_aggregation:'POSTHOC MATCHED-STATISTIC REMAND: one envelope observation per phase segment = max PRE-ENDPOINT CANDIDATE-REVERSAL amplitude across observed/accepted exact-transformation realizations',",
  "schema_version:'CR0105R18-ALGORITHM-NULL-CALIBRATION-1'":"schema_version:'CR0105R18-MATCHED-CANDIDATE-NULL-CALIBRATION-POSTHOC-1'",
  "schema_version:'CR0105R18-NULL-THRESHOLD-SEAL-1',status:'SEALED_BEFORE_HOLDOUT_SCORE'":"schema_version:'CR0105R18-MATCHED-CANDIDATE-NULL-THRESHOLD-POSTHOC-1',status:'POSTHOC_REMAND_AFTER_PROSPECTIVE_ZERO'",
  "holdout_outcomes_seen:false":"holdout_outcomes_seen:true",
}
for old,new in repls.items():
    c=src.count(old)
    if c!=1: raise RuntimeError(f'R18_MATCHED_NULL_PATCH_ANCHOR {c}: {old}')
    src=src.replace(old,new)
# Rewrite output names so prospective threshold evidence cannot be overwritten or confused.
src=src.replace("`${OUT}/ALGORITHM_NULL_CALIBRATION.json`","`${OUT}/MATCHED_CANDIDATE_NULL_CALIBRATION.json`")
src=src.replace("`${OUT}/NULL_THRESHOLD_SEAL.json`","`${OUT}/MATCHED_CANDIDATE_NULL_THRESHOLD.json`")
src=src.replace("`${OUT}/NULL_SEGMENT_LEDGER.json`","`${OUT}/MATCHED_CANDIDATE_NULL_SEGMENT_LEDGER.json`")
# The semantic name `null_envelope` is retained in rows, but it now means the matched candidate-reversal envelope by explicit schema/role.
out=Path('r18_matched_null_runtime.mjs');out.write_text(src,encoding='utf-8')
rec={
 'schema_version':'CR0105R18-MATCHED-NULL-REMAND-PATCH-1',
 'status':'PASS_POSTHOC_REMAND_PATCH',
 'role':'POSTHOC_MEASUREMENT-STATISTIC MATCHING DIAGNOSTIC; NOT THE R1.8 PROSPECTIVE PRIMARY',
 'prospective_zero_known_before_patch':True,
 'prospective_threshold_seal_changed':False,
 'changes':[
   'Calibration envelope statistic changed from maximum excursion amplitude to pre-endpoint candidate-reversal amplitude, matching the holdout scoring statistic.',
   'Representation and exact-transformation solver alternatives are scored with candidate-reversal amplitude rather than max excursion.',
   'The original threshold hierarchy and nearest-rank quantile rules are retained only as a diagnostic comparison.',
   'Outputs use distinct POSTHOC schema/file names and cannot supersede the frozen prospective threshold seal.'
 ],
 'human_observations':0
}
Path('/tmp/r18matched').mkdir(parents=True,exist_ok=True);Path('/tmp/r18matched/MATCHED_NULL_REMAND_PATCH.json').write_text(json.dumps(rec,indent=2)+'\n')
print(json.dumps(rec,indent=2))
