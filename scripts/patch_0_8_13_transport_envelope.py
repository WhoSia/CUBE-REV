from __future__ import annotations
import re
from pathlib import Path

path=Path('js/participant-cognitive-mode-0.8.13.js')
text=path.read_text(encoding='utf-8')
pattern=re.compile(r"function collectorEnvelopeFromSnapshot\(snapshot,options=\{\}\)\{.*?\n\}\nfunction exportSnapshot\(x\)\{.*?\n\}\n",re.S)
replacement=r'''function deepFreeze(value){
  if(!value||typeof value!=='object'||Object.isFrozen(value))return value;
  for(const child of Object.values(value))deepFreeze(child);
  return Object.freeze(value);
}
function collectorEnvelopeFromSnapshot(snapshot,options={}){
  const identity=transportSessionIdentity(snapshot),trials=compatibilityTrials(snapshot);
  const dataSubmission={
    status:String(options.status||'sealed_scientific_snapshot'),
    synthetic_live_cert:options.synthetic_live_cert===true,
    exclude_from_human_cohort:options.exclude_from_human_cohort===true,
    app_payload_version:snapshot.version,
    app_payload_schema:snapshot.schema_version,
    collector_compatibility_schema:'CR0813-COLLECTOR-COMPATIBILITY-ENVELOPE-1',
    compatibility_trial_policy:'LOSSLESS_OPAQUE_RESPONSE_PROJECTION_V1',
    original_scientific_session_id:identity.original_scientific_session_id,
    transport_session_id:identity.session_id,
    transport_session_policy:identity.transport_session_policy
  };
  if(typeof options.immutable_snapshot_sha256==='string')dataSubmission.immutable_snapshot_sha256=options.immutable_snapshot_sha256;
  if(typeof options.immutable_snapshot_integrity_fnv1a32==='string')dataSubmission.immutable_snapshot_integrity_fnv1a32=options.immutable_snapshot_integrity_fnv1a32;
  const envelope={
    project:'CUBE-REV',version:'0.7.12',session_id:identity.session_id,
    original_scientific_session_id:identity.original_scientific_session_id,
    transport_session_policy:identity.transport_session_policy,
    generated_at:String(options.generated_at||snapshot.scientific_completed_at||snapshot.started_at),
    trials,data_submission:dataSubmission,cognitive_snapshot:snapshot
  };
  if(envelope.session_id!==dataSubmission.transport_session_id)throw new Error('TRANSPORT_SESSION_INTERNAL_DIVERGENCE');
  if(envelope.original_scientific_session_id!==snapshot.session_id||dataSubmission.original_scientific_session_id!==snapshot.session_id)throw new Error('SCIENTIFIC_SESSION_INTERNAL_DIVERGENCE');
  if(envelope.transport_session_policy!==dataSubmission.transport_session_policy)throw new Error('TRANSPORT_POLICY_INTERNAL_DIVERGENCE');
  return deepFreeze(envelope);
}
function exportSnapshot(x){
  const snapshot=scientificSnapshot(x);
  return collectorEnvelopeFromSnapshot(snapshot,{immutable_snapshot_integrity_fnv1a32:x.submission_snapshot_hash});
}
'''
new,count=pattern.subn(replacement,text,count=1)
if count!=1:
    raise SystemExit(f'PATCH_TARGET_COUNT:{count}')
new=new.replace('transportSessionIdentity,collectorEnvelopeFromSnapshot,exportSnapshot,emptySubmissionControl','transportSessionIdentity,deepFreeze,collectorEnvelopeFromSnapshot,exportSnapshot,emptySubmissionControl')
if new==text:
    raise SystemExit('PATCH_NO_CHANGE')
path.write_text(new,encoding='utf-8')
print('CR0813_CANONICAL_ENVELOPE_PATCH_PASS')
