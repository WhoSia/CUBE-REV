(function(global){
'use strict';

const VERSION='CUBE-REV 0.8.13';
const SCHEMA='CR0813-RESUME-STATE-1';
const STORAGE_KEY='cube-rev-cognitive-mode-0813-v1';
const QUARANTINE_KEY='cube-rev-cognitive-mode-0813-quarantine-v1';
const DISPLAY_RE=/^[URFDLB](?:2|')?$/;
const CODE_RE=/^CR9C-[0-9a-f]{16}$/;
const COLLECTOR_SESSION_RE=/^CR-[0-9]{14}-[0-9a-f]{12}$/;
const INPUT_KEYS=new Set(['stimulus_id','choice_display','choice_code','latency_ms']);
const FORBIDDEN_RESPONSE_KEYS=new Set(['state_id','rotation_id','face_map','choice_canonical','canonical_move']);
const BINDING_KEYS=['manifest_sha256','public_bank_sha256','public_config_sha256','private_crosswalk_sha256'];

function fnv1a(s){let h=0x811c9dc5;for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,0x01000193)}return h>>>0}
function checksumText(s){return fnv1a(s).toString(16).padStart(8,'0')}
function checksum(x){return checksumText(JSON.stringify(x))}
function seal(x){const y={...x};delete y.integrity;return {...y,integrity:checksum({...y,integrity:undefined})}}
function sequenceId(t){return String((fnv1a(t)%24)+1)}
function validBinding(actual,expected){return !!actual&&!!expected&&BINDING_KEYS.every(k=>typeof actual[k]==='string'&&actual[k]===expected[k])}
function validResponse(r){
  if(!r||typeof r!=='object')return false;
  if(typeof r.stimulus_id!=='string'||!r.stimulus_id)return false;
  if(!DISPLAY_RE.test(r.choice_display)||!CODE_RE.test(r.choice_code))return false;
  if(!Number.isFinite(r.latency_ms)||r.latency_ms<0)return false;
  if(!Number.isInteger(r.position)||r.position<1||r.position>28)return false;
  if(typeof r.recorded_at!=='string'||!r.recorded_at)return false;
  return ![...FORBIDDEN_RESPONSE_KEYS].some(k=>Object.prototype.hasOwnProperty.call(r,k));
}
function sanitizeInput(r){
  if(!r||typeof r!=='object')throw new Error('RESPONSE_REQUIRED');
  for(const key of Object.keys(r)){
    if(FORBIDDEN_RESPONSE_KEYS.has(key))throw new Error(`FORBIDDEN_RESPONSE_FIELD:${key}`);
    if(!INPUT_KEYS.has(key))throw new Error(`UNKNOWN_RESPONSE_FIELD:${key}`);
  }
  if(typeof r.stimulus_id!=='string'||!r.stimulus_id)throw new Error('STIMULUS_ID_REQUIRED');
  if(!DISPLAY_RE.test(r.choice_display))throw new Error('DISPLAY_MOVE_INVALID');
  if(!CODE_RE.test(r.choice_code))throw new Error('OPAQUE_CHOICE_CODE_INVALID');
  const latency=Math.round(Number(r.latency_ms));
  if(!Number.isFinite(latency)||latency<0)throw new Error('LATENCY_INVALID');
  return {stimulus_id:r.stimulus_id,choice_display:r.choice_display,choice_code:r.choice_code,latency_ms:latency};
}
function sanitizePostTask(p){
  p=p||{};
  return {
    hypothesis_guess:String(p.hypothesis_guess||'').slice(0,2000),
    confidence:Math.max(0,Math.min(100,Number(p.confidence)||0)),
    deliberate_strategy_change:!!p.deliberate_strategy_change,
    technical_notes:String(p.technical_notes||'').slice(0,2000)
  };
}
function stateShapeValid(x){
  if(!x||!Number.isInteger(x.cursor)||!Array.isArray(x.responses)||x.cursor!==x.responses.length)return false;
  const complete=x.cursor===28,hasPost=!!x.post_task,hasSnapshot=!!x.submission_snapshot;
  if(hasSnapshot)return complete&&hasPost&&['READY_TO_SUBMIT','SUBMITTED'].includes(x.status);
  if(x.status==='SUBMITTED')return false;
  if(x.status==='IN_PROGRESS')return x.cursor>=0&&x.cursor<28&&!hasPost;
  if(x.status==='POST_TASK')return complete&&!hasPost;
  if(x.status==='READY_TO_SUBMIT')return complete&&hasPost;
  return false;
}
function provenanceValid(x){
  if(!Number.isInteger(x.upgrade_epoch)||x.upgrade_epoch<0)return false;
  if(!x.migration_provenance)return x.upgrade_epoch===0;
  return Number.isInteger(x.migration_provenance.migration_epoch)&&x.migration_provenance.migration_epoch===x.upgrade_epoch&&x.upgrade_epoch>0;
}
function mutationHistoryValid(x){
  if(!Number.isInteger(x.revision)||x.revision<1||!Array.isArray(x.mutation_history))return false;
  const ids=new Set();let last=0;
  for(const m of x.mutation_history){
    if(!m||typeof m.mutation_id!=='string'||!m.mutation_id||ids.has(m.mutation_id))return false;
    if(!Number.isInteger(m.from_revision)||!Number.isInteger(m.to_revision)||m.to_revision!==m.from_revision+1)return false;
    if(m.from_revision<last||m.to_revision>x.revision)return false;
    if(typeof m.type!=='string'||typeof m.at!=='string')return false;
    ids.add(m.mutation_id);last=m.to_revision;
  }
  return x.mutation_history.length===0||x.mutation_history[x.mutation_history.length-1].to_revision===x.revision;
}
function submissionControlValid(c){
  if(!c||typeof c!=='object')return false;
  if(!Number.isInteger(c.lease_generation)||c.lease_generation<0)return false;
  if(!Number.isInteger(c.attempt_count)||c.attempt_count<0)return false;
  if(c.retry_id!=null&&typeof c.retry_id!=='string')return false;
  if(c.lease_token==null)return c.lease_owner==null&&c.lease_expires_at==null;
  return typeof c.lease_token==='string'&&typeof c.lease_owner==='string'&&typeof c.lease_expires_at==='string';
}
function snapshotValid(x){
  if(!x.submission_snapshot)return x.submission_snapshot_hash==null&&x.snapshot_sealed_at==null;
  return x.submission_snapshot.version===VERSION&&
    x.submission_snapshot.schema_version==='CR0813-COLLECTOR-PAYLOAD-1'&&
    x.submission_snapshot.response_encoding==='OPAQUE_CHOICE_CODE_V1'&&
    Number.isInteger(x.submission_snapshot.scientific_revision)&&
    x.submission_snapshot.upgrade_epoch===x.upgrade_epoch&&
    validBinding(x.submission_snapshot.asset_binding,x.asset_binding)&&
    checksum(x.submission_snapshot)===x.submission_snapshot_hash&&
    typeof x.snapshot_sealed_at==='string';
}
function valid(x,c,binding){
  return !!x&&x.schema_version===SCHEMA&&x.version===VERSION&&
    x.sequence_id===sequenceId(x.participant_token)&&
    Array.isArray(x.schedule)&&x.schedule.length===28&&
    x.schedule.join('|')===(c.schedules[x.sequence_id]||[]).join('|')&&
    Array.isArray(x.responses)&&x.responses.every(validResponse)&&
    x.responses.every((r,i)=>r.position===i+1&&r.stimulus_id===x.schedule[i])&&
    Array.isArray(x.telemetry)&&stateShapeValid(x)&&provenanceValid(x)&&
    validBinding(x.asset_binding,binding)&&mutationHistoryValid(x)&&
    Number.isInteger(x.conflict_count)&&x.conflict_count>=0&&
    submissionControlValid(x.submission_control)&&snapshotValid(x)&&
    x.integrity===checksum({...x,integrity:undefined});
}
function scientificEnvelope(x){
  return {
    schema_version:'CR0813-COLLECTOR-PAYLOAD-1',version:VERSION,mode_id:x.mode_id,
    response_encoding:'OPAQUE_CHOICE_CODE_V1',session_id:x.session_id,participant_token:x.participant_token,
    sequence_id:x.sequence_id,responses:x.responses,telemetry:x.telemetry,post_task:x.post_task,
    started_at:x.created_at,scientific_completed_at:x.updated_at,scientific_revision:x.revision,
    asset_binding:x.asset_binding,upgrade_epoch:x.upgrade_epoch,migration_provenance:x.migration_provenance,
    active_session_provenance:x.active_session_provenance,
    participant_ui:{legacy_fixed_set_selector:false,diagnostic_identifiers_exposed:false,canonical_moves_exposed:false},
    submission_snapshot_policy:'IMMUTABLE_RETRY_STABLE_V3',
    factory_contract:{adapter:'CR0813_COGNITIVE_SNAPSHOT_FACTORY_ADAPTER_V1',raw_snapshot_immutable:true,response_order:'POSITION_1_TO_28'}
  };
}
function scientificSnapshot(x){
  if(!x.submission_snapshot||!snapshotValid(x))throw new Error('SUBMISSION_SNAPSHOT_INVALID');
  return x.submission_snapshot;
}
function compatibilityTrials(snapshot){
  if(!snapshot||snapshot.schema_version!=='CR0813-COLLECTOR-PAYLOAD-1'||snapshot.version!==VERSION)throw new Error('SNAPSHOT_IDENTITY');
  if(!Array.isArray(snapshot.responses)||snapshot.responses.length!==28)throw new Error('RESPONSE_CARDINALITY');
  return snapshot.responses.map(r=>({
    trial_index:r.position,
    trial_id:`CR0813-COMPAT-${String(r.position).padStart(2,'0')}`,
    condition_id:snapshot.mode_id,
    stimulus_id:r.stimulus_id,
    response:{choice_display:r.choice_display,choice_code:r.choice_code,latency_ms:r.latency_ms,recorded_at:r.recorded_at},
    status:'completed',source_schema:snapshot.schema_version,scientific_revision:snapshot.scientific_revision
  }));
}
function utcStamp14(value){
  const d=new Date(value);
  if(!Number.isFinite(d.getTime()))throw new Error('TRANSPORT_TIMESTAMP_INVALID');
  return [d.getUTCFullYear(),String(d.getUTCMonth()+1).padStart(2,'0'),String(d.getUTCDate()).padStart(2,'0'),String(d.getUTCHours()).padStart(2,'0'),String(d.getUTCMinutes()).padStart(2,'0'),String(d.getUTCSeconds()).padStart(2,'0')].join('');
}
function transportSessionIdentity(snapshot){
  if(!snapshot||typeof snapshot.session_id!=='string'||!snapshot.session_id)throw new Error('SCIENTIFIC_SESSION_IDENTITY');
  if(COLLECTOR_SESSION_RE.test(snapshot.session_id))return {session_id:snapshot.session_id,original_scientific_session_id:snapshot.session_id,transport_session_policy:'IDENTITY_SESSION_V1'};
  const stamp=utcStamp14(snapshot.started_at||snapshot.scientific_completed_at);
  const seed=`${snapshot.session_id}|${snapshot.participant_token||''}|${snapshot.sequence_id||''}`;
  const suffix=(checksumText(`${seed}|A`)+checksumText(`${seed}|B`)).slice(0,12);
  return {session_id:`CR-${stamp}-${suffix}`,original_scientific_session_id:snapshot.session_id,transport_session_policy:'DETERMINISTIC_LEGACY_SESSION_BRIDGE_V1'};
}
function deepFreeze(value){
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
function collectorWorkingCopy(x){
  const canonical=exportSnapshot(x);
  const copy=JSON.parse(JSON.stringify(canonical));
  const same=copy.session_id===canonical.session_id&&
    copy.original_scientific_session_id===canonical.original_scientific_session_id&&
    copy.transport_session_policy===canonical.transport_session_policy&&
    copy.data_submission&&canonical.data_submission&&
    copy.data_submission.transport_session_id===canonical.data_submission.transport_session_id&&
    copy.data_submission.original_scientific_session_id===canonical.data_submission.original_scientific_session_id&&
    copy.cognitive_snapshot&&canonical.cognitive_snapshot&&
    copy.cognitive_snapshot.session_id===canonical.cognitive_snapshot.session_id;
  if(!same)throw new Error('COLLECTOR_WORKING_COPY_IDENTITY');
  if(Object.isFrozen(copy))throw new Error('COLLECTOR_WORKING_COPY_FROZEN');
  return copy;
}
function emptySubmissionControl(){
  return {retry_id:null,lease_generation:0,lease_token:null,lease_owner:null,lease_expires_at:null,attempt_count:0,last_attempt_at:null,last_error:null,collector_meta:null,collector_events:[],receipt:null};
}
function from0812(c,d,x){
  if(!x||x.version!=='CUBE-REV 0.8.12'||x.schema_version!=='CR0812-RESUME-STATE-1')throw new Error('PARENT_STATE_IDENTITY');
  if(x.submission_snapshot||x.status==='SUBMITTED')throw new Error('SEALED_PARENT_RETRY_ONLY');
  if(!d.m12||!d.m12.valid(x,d.parentConfig,d.parentBinding))throw new Error('PARENT_STATE_INVALID');
  const at=d.now(),mutationId=`UPGRADE-${checksumText(x.integrity+at)}`;
  const initial={
    schema_version:SCHEMA,version:VERSION,mode_id:x.mode_id,participant_token:x.participant_token,
    session_id:x.session_id,sequence_id:x.sequence_id,schedule:[...x.schedule],cursor:x.cursor,
    responses:x.responses.map(r=>({...r})),
    telemetry:[...x.telemetry,{event_id:mutationId,type:'NATIVE_BROWSER_CERT_UPGRADE_COMPLETED',at,data:{source_version:x.version,source_revision:x.revision}}],
    post_task:x.post_task?{...x.post_task}:null,submission_snapshot:null,submission_snapshot_hash:null,snapshot_sealed_at:null,
    status:x.status,created_at:x.created_at,updated_at:at,submitted_at:null,submission_receipt:null,
    revision:1,mutation_history:[{mutation_id:mutationId,type:'ACTIVE_SESSION_UPGRADE',from_revision:0,to_revision:1,at,outcome:'APPLIED'}],
    conflict_count:0,submission_control:emptySubmissionControl(),asset_binding:{...d.binding},
    upgrade_epoch:x.upgrade_epoch,migration_provenance:x.migration_provenance,
    active_session_provenance:{source_version:x.version,source_schema:x.schema_version,source_storage_key:d.parentStorageKey,source_integrity:x.integrity,source_revision:x.revision,migrated_at:at,policy:'SOURCE_PRESERVED_NATIVE_BROWSER_CERT_V1'}
  };
  const y=seal(initial);
  if(!valid(y,c,d.binding))throw new Error('TARGET_STATE_INVALID');
  return y;
}

const api={VERSION,SCHEMA,STORAGE_KEY,QUARANTINE_KEY,DISPLAY_RE,CODE_RE,COLLECTOR_SESSION_RE,BINDING_KEYS,fnv1a,checksumText,checksum,seal,sequenceId,validBinding,validResponse,sanitizeInput,sanitizePostTask,stateShapeValid,provenanceValid,mutationHistoryValid,submissionControlValid,snapshotValid,valid,scientificEnvelope,scientificSnapshot,compatibilityTrials,utcStamp14,transportSessionIdentity,deepFreeze,collectorEnvelopeFromSnapshot,exportSnapshot,collectorWorkingCopy,emptySubmissionControl,from0812};
if(typeof module!=='undefined'&&module.exports)module.exports=api;
global.CUBE_REV_COGNITIVE_MODE_0813=api;
})(typeof window!=='undefined'?window:globalThis);
