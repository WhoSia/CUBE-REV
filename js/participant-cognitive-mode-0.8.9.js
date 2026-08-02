(function(global){
'use strict';

const VERSION='CUBE-REV 0.8.9';
const SCHEMA='CR0809-RESUME-STATE-1';
const STORAGE_KEY='cube-rev-cognitive-mode-0809-v1';
const QUARANTINE_KEY='cube-rev-cognitive-mode-0809-quarantine-v1';
const DISPLAY_RE=/^[URFDLB](?:2|')?$/;
const CODE_RE=/^CR9C-[0-9a-f]{16}$/;
const INPUT_KEYS=new Set(['stimulus_id','choice_display','choice_code','latency_ms']);
const FORBIDDEN_RESPONSE_KEYS=new Set(['state_id','rotation_id','face_map','choice_canonical','canonical_move']);

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
function snapshotValid(x){
  if(!x.submission_snapshot)return x.submission_snapshot_hash==null;
  return x.submission_snapshot.version===VERSION&&
    x.submission_snapshot.response_encoding==='OPAQUE_CHOICE_CODE_V1'&&
    checksum(x.submission_snapshot)===x.submission_snapshot_hash;
}
function validResponse(r){
  if(!r||typeof r!=='object')return false;
  if(typeof r.stimulus_id!=='string'||!r.stimulus_id)return false;
  if(!DISPLAY_RE.test(r.choice_display)||!CODE_RE.test(r.choice_code))return false;
  if(!Number.isFinite(r.latency_ms)||r.latency_ms<0)return false;
  if(!Number.isInteger(r.position)||r.position<1||r.position>28)return false;
  if(typeof r.recorded_at!=='string'||!r.recorded_at)return false;
  return ![...FORBIDDEN_RESPONSE_KEYS].some(k=>Object.prototype.hasOwnProperty.call(r,k));
}
function valid(x,c){
  return !!x&&x.schema_version===SCHEMA&&x.version===VERSION&&
    x.sequence_id===sequenceId(x.participant_token)&&
    Array.isArray(x.schedule)&&x.schedule.length===28&&
    x.schedule.join('|')===(c.schedules[x.sequence_id]||[]).join('|')&&
    Array.isArray(x.responses)&&x.responses.every(validResponse)&&
    x.cursor===x.responses.length&&x.cursor>=0&&x.cursor<=28&&
    Array.isArray(x.telemetry)&&snapshotValid(x)&&
    x.integrity===checksum({...x,integrity:undefined});
}
function persist(storage,x,now){
  const y=seal({...x,revision:x.revision+1,updated_at:now()});
  storage.setItem(STORAGE_KEY,JSON.stringify(y));return y;
}
function event(storage,x,type,data,now){
  return persist(storage,{...x,telemetry:[...x.telemetry,{type,at:now(),data:data||{}}]},now);
}
function create(c,d){
  const t=token(d.storage,d.cryptoObj),sid=sequenceId(t),n=d.now;
  let x=seal({
    schema_version:SCHEMA,version:VERSION,mode_id:'COG-MODE-001',participant_token:t,
    session_id:'CR089-'+n().replace(/\D/g,'').slice(0,14)+'-'+fnv1a(t+n()).toString(16).padStart(8,'0'),
    sequence_id:sid,schedule:[...c.schedules[sid]],cursor:0,responses:[],telemetry:[],post_task:null,
    submission_snapshot:null,submission_snapshot_hash:null,snapshot_sealed_at:null,status:'IN_PROGRESS',
    created_at:n(),updated_at:n(),submitted_at:null,submission_receipt:null,revision:0
  });
  return event(d.storage,x,'SESSION_CREATED',{},n);
}
function loadOrCreate(c,d){
  const raw=d.storage.getItem(STORAGE_KEY);
  if(raw){
    try{
      let x=JSON.parse(raw);
      if(valid(x,c)){
        x=event(d.storage,x,'SESSION_RESUMED',{cursor:x.cursor,snapshot_sealed:!!x.submission_snapshot},d.now);
        return {state:x,resumed:true};
      }
    }catch(e){}
    d.storage.setItem(QUARANTINE_KEY,raw);d.storage.removeItem(STORAGE_KEY);
  }
  return {state:create(c,d),resumed:false};
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
  const clean={
    hypothesis_guess:String(p.hypothesis_guess||'').slice(0,2000),
    confidence:Math.max(0,Math.min(100,Number(p.confidence)||0)),
    deliberate_strategy_change:!!p.deliberate_strategy_change,
    technical_notes:String(p.technical_notes||'').slice(0,2000)
  };
  let y=persist(storage,{...x,post_task:clean,status:'READY_TO_SUBMIT'},now);
  return event(storage,y,'POST_TASK_SAVED',{confidence:clean.confidence,deliberate_strategy_change:clean.deliberate_strategy_change},now);
}
function scientificEnvelope(x){
  return {
    schema_version:'CR0809-COLLECTOR-PAYLOAD-1',version:VERSION,mode_id:x.mode_id,
    response_encoding:'OPAQUE_CHOICE_CODE_V1',session_id:x.session_id,participant_token:x.participant_token,
    sequence_id:x.sequence_id,responses:x.responses,telemetry:x.telemetry,post_task:x.post_task,
    started_at:x.created_at,scientific_completed_at:x.updated_at,
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

const api={VERSION,SCHEMA,STORAGE_KEY,QUARANTINE_KEY,DISPLAY_RE,CODE_RE,fnv1a,checksum,snapshotValid,validResponse,valid,loadOrCreate,persist,event,sanitizeInput,record,savePostTask,scientificEnvelope,prepareSubmissionSnapshot,exportSnapshot,saveExternalMutation,markSubmitted};
if(typeof module!=='undefined'&&module.exports)module.exports=api;
global.CUBE_REV_COGNITIVE_MODE_0809=api;
})(typeof window!=='undefined'?window:globalThis);
