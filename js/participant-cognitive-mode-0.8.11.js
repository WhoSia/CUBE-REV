(function(global){
'use strict';

const VERSION='CUBE-REV 0.8.11';
const SCHEMA='CR0811-RESUME-STATE-1';
const STORAGE_KEY='cube-rev-cognitive-mode-0811-v1';
const QUARANTINE_KEY='cube-rev-cognitive-mode-0811-quarantine-v1';
const DISPLAY_RE=/^[URFDLB](?:2|')?$/;
const CODE_RE=/^CR9C-[0-9a-f]{16}$/;
const INPUT_KEYS=new Set(['stimulus_id','choice_display','choice_code','latency_ms']);
const FORBIDDEN_RESPONSE_KEYS=new Set(['state_id','rotation_id','face_map','choice_canonical','canonical_move']);
const BINDING_KEYS=['manifest_sha256','public_bank_sha256','public_config_sha256','private_crosswalk_sha256'];

function fnv1a(s){let h=0x811c9dc5;for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,0x01000193)}return h>>>0}
function checksumText(s){return fnv1a(s).toString(16).padStart(8,'0')}
function checksum(x){return checksumText(JSON.stringify(x))}
function seal(x){const y={...x};delete y.integrity;return {...y,integrity:checksum({...y,integrity:undefined})}}
function token(storage,cryptoObj){
  let t=storage.getItem('cube-rev-anonymous-participant-v1');
  if(t)return t;
  const a=new Uint32Array(4);cryptoObj.getRandomValues(a);
  t='CRP-'+Array.from(a,x=>x.toString(16).padStart(8,'0')).join('');
  storage.setItem('cube-rev-anonymous-participant-v1',t);return t;
}
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
function snapshotValid(x){
  if(!x.submission_snapshot)return x.submission_snapshot_hash==null;
  return x.submission_snapshot.version===VERSION&&
    x.submission_snapshot.response_encoding==='OPAQUE_CHOICE_CODE_V1'&&
    x.submission_snapshot.upgrade_epoch===x.upgrade_epoch&&
    validBinding(x.submission_snapshot.asset_binding,x.asset_binding)&&
    checksum(x.submission_snapshot)===x.submission_snapshot_hash;
}
function valid(x,c,binding){
  return !!x&&x.schema_version===SCHEMA&&x.version===VERSION&&
    x.sequence_id===sequenceId(x.participant_token)&&
    Array.isArray(x.schedule)&&x.schedule.length===28&&
    x.schedule.join('|')===(c.schedules[x.sequence_id]||[]).join('|')&&
    Array.isArray(x.responses)&&x.responses.every(validResponse)&&
    x.responses.every((r,i)=>r.position===i+1&&r.stimulus_id===x.schedule[i])&&
    Array.isArray(x.telemetry)&&stateShapeValid(x)&&provenanceValid(x)&&
    validBinding(x.asset_binding,binding)&&snapshotValid(x)&&
    x.integrity===checksum({...x,integrity:undefined});
}
function persist(storage,x,now){const y=seal({...x,revision:(x.revision||0)+1,updated_at:now()});storage.setItem(STORAGE_KEY,JSON.stringify(y));return y}
function event(storage,x,type,data,now){return persist(storage,{...x,telemetry:[...x.telemetry,{type,at:now(),data:data||{}}]},now)}
function create(c,d){
  if(!validBinding(d.binding,d.binding))throw new Error('ASSET_BINDING_REQUIRED');
  const t=token(d.storage,d.cryptoObj),sid=sequenceId(t),n=d.now;
  let x=seal({
    schema_version:SCHEMA,version:VERSION,mode_id:'COG-MODE-001',participant_token:t,
    session_id:'CR0811-'+n().replace(/\D/g,'').slice(0,14)+'-'+fnv1a(t+n()).toString(16).padStart(8,'0'),
    sequence_id:sid,schedule:[...c.schedules[sid]],cursor:0,responses:[],telemetry:[],post_task:null,
    submission_snapshot:null,submission_snapshot_hash:null,snapshot_sealed_at:null,status:'IN_PROGRESS',
    created_at:n(),updated_at:n(),submitted_at:null,submission_receipt:null,revision:0,
    asset_binding:{...d.binding},upgrade_epoch:0,migration_provenance:null
  });
  return event(d.storage,x,'SESSION_CREATED',{asset_manifest:d.binding.manifest_sha256,atomic_initialization:true},n);
}
function loadExisting(c,d){
  const raw=d.storage.getItem(STORAGE_KEY);
  if(!raw)return {state:null,resumed:false,invalid:false};
  try{
    let x=JSON.parse(raw);
    if(valid(x,c,d.binding)){
      x=event(d.storage,x,'SESSION_RESUMED',{cursor:x.cursor,snapshot_sealed:!!x.submission_snapshot,upgrade_epoch:x.upgrade_epoch},d.now);
      return {state:x,resumed:true,invalid:false};
    }
  }catch(e){}
  d.storage.setItem(QUARANTINE_KEY,raw);d.storage.removeItem(STORAGE_KEY);
  return {state:null,resumed:false,invalid:true};
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
function record(storage,x,r,now){
  if(x.status!=='IN_PROGRESS')throw new Error('SESSION_NOT_ACTIVE');
  const clean=sanitizeInput(r);
  if(clean.stimulus_id!==x.schedule[x.cursor])throw new Error('TRIAL_ORDER_MISMATCH');
  const response={...clean,position:x.cursor+1,recorded_at:now()};
  let y=persist(storage,{...x,responses:[...x.responses,response],cursor:x.cursor+1,status:x.cursor+1===28?'POST_TASK':'IN_PROGRESS'},now);
  return event(storage,y,'RESPONSE_RECORDED',{position:y.cursor,stimulus_id:clean.stimulus_id},now);
}
function savePostTask(storage,x,p,now){
  if(x.status!=='POST_TASK')throw new Error('POST_TASK_NOT_READY');
  const clean={hypothesis_guess:String(p.hypothesis_guess||'').slice(0,2000),confidence:Math.max(0,Math.min(100,Number(p.confidence)||0)),deliberate_strategy_change:!!p.deliberate_strategy_change,technical_notes:String(p.technical_notes||'').slice(0,2000)};
  let y=persist(storage,{...x,post_task:clean,status:'READY_TO_SUBMIT'},now);
  return event(storage,y,'POST_TASK_SAVED',{confidence:clean.confidence,deliberate_strategy_change:clean.deliberate_strategy_change},now);
}
function scientificEnvelope(x){
  return {
    schema_version:'CR0811-COLLECTOR-PAYLOAD-1',version:VERSION,mode_id:x.mode_id,
    response_encoding:'OPAQUE_CHOICE_CODE_V1',session_id:x.session_id,participant_token:x.participant_token,
    sequence_id:x.sequence_id,responses:x.responses,telemetry:x.telemetry,post_task:x.post_task,
    started_at:x.created_at,scientific_completed_at:x.updated_at,asset_binding:x.asset_binding,
    upgrade_epoch:x.upgrade_epoch,migration_provenance:x.migration_provenance,
    participant_ui:{legacy_fixed_set_selector:false,diagnostic_identifiers_exposed:false,canonical_moves_exposed:false},
    submission_snapshot_policy:'IMMUTABLE_RETRY_STABLE_V1'
  };
}
function prepareSubmissionSnapshot(storage,x,now){
  if(x.submission_snapshot){if(!snapshotValid(x))throw new Error('SUBMISSION_SNAPSHOT_INVALID');return x}
  if(x.status!=='READY_TO_SUBMIT')throw new Error('SNAPSHOT_NOT_READY');
  let y=event(storage,x,'SUBMISSION_SNAPSHOT_SEALING',{},now);
  const snap=scientificEnvelope(y),hash=checksum(snap);
  return persist(storage,{...y,submission_snapshot:snap,submission_snapshot_hash:hash,snapshot_sealed_at:now()},now);
}
function exportSnapshot(x){if(!x.submission_snapshot||!snapshotValid(x))throw new Error('SUBMISSION_SNAPSHOT_INVALID');return x.submission_snapshot}
function saveExternalMutation(storage,x,now){return persist(storage,x,now)}
function markSubmitted(storage,x,receipt,now){
  if(x.status==='SUBMITTED')return x;
  if(x.status!=='READY_TO_SUBMIT')throw new Error('SESSION_NOT_COMPLETE');
  let y=persist(storage,{...x,status:'SUBMITTED',submitted_at:now(),submission_receipt:receipt||null},now);
  return event(storage,y,'SUBMISSION_CONFIRMED',{},now);
}
function fromMigration(c,d,m){
  if(!m||!Array.isArray(m.responses)||!Array.isArray(m.schedule))throw new Error('MIGRATION_MATERIAL_REQUIRED');
  if(!Number.isInteger(d.epoch)||d.epoch<1)throw new Error('MIGRATION_EPOCH_REQUIRED');
  if(m.sequence_id!==sequenceId(m.participant_token))throw new Error('MIGRATION_ASSIGNMENT_MISMATCH');
  if(m.schedule.join('|')!==(c.schedules[m.sequence_id]||[]).join('|'))throw new Error('MIGRATION_SCHEDULE_MISMATCH');
  if(m.cursor!==m.responses.length||!m.responses.every(validResponse))throw new Error('MIGRATION_RESPONSE_INVALID');
  const at=d.now();
  const provenance={
    source_version:m.source_version,source_schema:m.source_schema,source_storage_key:m.source_storage_key,
    source_session_id:m.session_id,source_integrity:m.source_integrity,source_revision:m.source_revision,
    migrated_at:at,migration_policy:'ATOMIC_LOCKED_SOURCE_PRESERVED_V2',migration_epoch:d.epoch,
    parent_provenance:m.previous_provenance||null
  };
  return seal({
    schema_version:SCHEMA,version:VERSION,mode_id:m.mode_id||'COG-MODE-001',participant_token:m.participant_token,
    session_id:m.session_id,sequence_id:m.sequence_id,schedule:[...m.schedule],cursor:m.cursor,
    responses:m.responses.map(x=>({...x})),telemetry:[...(m.telemetry||[]),{type:'ATOMIC_CROSS_VERSION_MIGRATION_COMPLETED',at,data:{source_version:m.source_version,cursor:m.cursor,migration_epoch:d.epoch}}],
    post_task:m.post_task||null,submission_snapshot:null,submission_snapshot_hash:null,snapshot_sealed_at:null,
    status:m.status,created_at:m.created_at,updated_at:at,submitted_at:null,submission_receipt:null,revision:0,
    asset_binding:{...d.binding},upgrade_epoch:d.epoch,migration_provenance:provenance
  });
}

const api={VERSION,SCHEMA,STORAGE_KEY,QUARANTINE_KEY,DISPLAY_RE,CODE_RE,BINDING_KEYS,fnv1a,checksum,seal,sequenceId,validBinding,validResponse,stateShapeValid,provenanceValid,snapshotValid,valid,persist,event,create,loadExisting,sanitizeInput,record,savePostTask,scientificEnvelope,prepareSubmissionSnapshot,exportSnapshot,saveExternalMutation,markSubmitted,fromMigration};
if(typeof module!=='undefined'&&module.exports)module.exports=api;
global.CUBE_REV_COGNITIVE_MODE_0811=api;
})(typeof window!=='undefined'?window:globalThis);
