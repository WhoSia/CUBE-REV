(function(global){
'use strict';

const LOCK_NAME='cube-rev-session-write-0813-exclusive-v1';
const JOURNAL_KEY='cube-rev-session-write-0813-journal-v1';
const CONFLICT_KEY='cube-rev-session-write-0813-conflicts-v1';
const SOURCE_0812='cube-rev-cognitive-mode-0812-v1';
const LEGACY_ROUTE='participant-cognitive-mode-0.8.12.html';

function clone(x){return JSON.parse(JSON.stringify(x))}
function parse(raw){try{return JSON.parse(raw)}catch(_){return null}}
function isoMs(s){const n=Date.parse(s||'');return Number.isFinite(n)?n:0}
function hasLockManager(x){return !!x&&typeof x.request==='function'}
function mutationSeen(x,id){return x.mutation_history.some(m=>m.mutation_id===id)}
function telemetrySeen(x,id){return x.telemetry.some(e=>e&&e.event_id===id)}
function writeJournal(o,entry){o.storage.setItem(JOURNAL_KEY,JSON.stringify(entry))}
function readConflicts(o){const x=parse(o.storage.getItem(CONFLICT_KEY));return Array.isArray(x)?x:[]}
function writeConflict(o,e){
  const limit=(o.config.active_session&&o.config.active_session.conflict_history_limit)||64;
  const a=readConflicts(o);a.push(e);while(a.length>limit)a.shift();
  o.storage.setItem(CONFLICT_KEY,JSON.stringify(a));
}
function readState(o){
  const raw=o.storage.getItem(o.m13.STORAGE_KEY);
  if(!raw)return {state:null,raw:null,invalid:false};
  const x=parse(raw);
  return {state:x,raw,invalid:!x||!o.m13.valid(x,o.config,o.binding)};
}
function verifyStored(o,expected){
  const r=readState(o);
  if(r.invalid||!r.state||r.state.revision!==expected.revision||r.state.integrity!==expected.integrity)throw new Error('CAS_POST_WRITE_VERIFY_FAILED');
  return r.state;
}
function commit(o,current,op,type,mutate,outcome='APPLIED'){
  if(!op||typeof op.mutation_id!=='string'||!op.mutation_id)throw new Error('MUTATION_ID_REQUIRED');
  if(mutationSeen(current,op.mutation_id))return {ok:true,action:'IDEMPOTENT_REPLAY',state:current,mutated:false};
  const at=o.now(),nextRevision=current.revision+1;
  const body=mutate(clone(current));
  body.revision=nextRevision;body.updated_at=at;
  body.mutation_history=[...current.mutation_history,{mutation_id:op.mutation_id,type,from_revision:current.revision,to_revision:nextRevision,at,outcome}];
  const limit=(o.config.active_session&&o.config.active_session.mutation_history_limit)||256;
  if(body.mutation_history.length>limit)body.mutation_history=body.mutation_history.slice(-limit);
  const next=o.m13.seal(body);
  if(!o.m13.valid(next,o.config,o.binding))throw new Error(`CAS_CANDIDATE_INVALID:${type}`);
  o.storage.setItem(o.m13.STORAGE_KEY,JSON.stringify(next));
  const verified=verifyStored(o,next);
  writeJournal(o,{schema_version:'CR0813-ACTIVE-WRITE-JOURNAL-1',session_id:verified.session_id,mutation_id:op.mutation_id,type,from_revision:current.revision,to_revision:verified.revision,outcome,committed_at:at,integrity:verified.integrity});
  return {ok:true,action:outcome,state:verified,mutated:true};
}
function reject(action,state,extra={}){return {ok:false,action,state,mutated:false,...extra}}
function expectedMatch(current,op){return Number.isInteger(op.expected_revision)&&op.expected_revision===current.revision}
function responseEquivalent(a,b){return !!a&&a.stimulus_id===b.stimulus_id&&a.choice_display===b.choice_display&&a.choice_code===b.choice_code&&a.latency_ms===b.latency_ms}
function conflictEvidence(o,current,op,clean,kind){
  const e={schema_version:'CR0813-WRITE-CONFLICT-1',kind,detected_at:o.now(),session_id:current.session_id,current_revision:current.revision,expected_revision:op.expected_revision,expected_position:op.expected_position,mutation_id:op.mutation_id,attempted_response:clean,stored_response:Number.isInteger(op.expected_position)?current.responses[op.expected_position]||null:null};
  writeConflict(o,e);return e;
}
function assertSession(current,op){if(op.session_id&&op.session_id!==current.session_id)throw new Error('SESSION_ID_MISMATCH')}
function sanitizeMeta(patch){
  const allowed=['status','receipt_confirmed','attempt_count','last_attempt_at','manual','collector_health','encoding','original_bytes','transmitted_bytes','checksum_fnv1a32','submission_nonce','confirmation_protocol','collector_status','received_at','receipt_code','file_name','last_error','transport','response_verification','checksum_verified'];
  const out={};for(const k of allowed)if(Object.prototype.hasOwnProperty.call(patch||{},k))out[k]=clone(patch[k]);
  return out;
}
function leaseActive(c,now){return !!c.lease_token&&isoMs(c.lease_expires_at)>isoMs(now)}
function plusMs(iso,ms){return new Date(isoMs(iso)+ms).toISOString()}

function applyLocked(o,op){
  const r=readState(o);
  if(!r.state)return reject('STATE_MISSING',null,{blocking:true});
  if(r.invalid)return reject('STATE_INVALID',null,{blocking:true});
  const current=r.state;assertSession(current,op);
  if(op.mutation_id&&mutationSeen(current,op.mutation_id))return {ok:true,action:'IDEMPOTENT_REPLAY',state:current,mutated:false};

  switch(op.type){
    case 'RESPONSE':{
      if(current.submission_snapshot)return reject('SNAPSHOT_ALREADY_SEALED',current);
      const clean=o.m13.sanitizeInput(op.response);
      if(!Number.isInteger(op.expected_position)||op.expected_position<0)return reject('EXPECTED_POSITION_REQUIRED',current);
      if(!expectedMatch(current,op)){
        if(op.expected_position<current.cursor){
          const stored=current.responses[op.expected_position];
          if(responseEquivalent(stored,clean))return {ok:true,action:'RESPONSE_ALREADY_APPLIED',state:current,mutated:false};
          const evidence=conflictEvidence(o,current,op,clean,'RESPONSE_CONFLICT');
          return reject('RESPONSE_CONFLICT',current,{conflict:evidence});
        }
        return reject('STALE_REVISION',current,{current_revision:current.revision});
      }
      if(current.status!=='IN_PROGRESS')return reject('SESSION_NOT_ACTIVE',current);
      if(op.expected_position!==current.cursor)return reject('TRIAL_POSITION_MISMATCH',current);
      if(clean.stimulus_id!==current.schedule[current.cursor])return reject('TRIAL_ORDER_MISMATCH',current);
      const recordedAt=op.recorded_at||o.now();
      return commit(o,current,op,'RESPONSE',x=>{
        const response={...clean,position:x.cursor+1,recorded_at:recordedAt};
        x.responses=[...x.responses,response];x.cursor+=1;x.status=x.cursor===28?'POST_TASK':'IN_PROGRESS';
        x.telemetry=[...x.telemetry,{event_id:`${op.mutation_id}:telemetry`,type:'RESPONSE_RECORDED',at:recordedAt,data:{position:x.cursor,stimulus_id:clean.stimulus_id}}];
        return x;
      },'RESPONSE_APPLIED');
    }
    case 'TELEMETRY':{
      if(typeof op.event_id!=='string'||!op.event_id)return reject('EVENT_ID_REQUIRED',current);
      if(telemetrySeen(current,op.event_id))return {ok:true,action:'TELEMETRY_ALREADY_MERGED',state:current,mutated:false};
      const merged=!expectedMatch(current,op);
      return commit(o,current,op,'TELEMETRY',x=>{x.telemetry=[...x.telemetry,{event_id:op.event_id,type:String(op.event_type||'EVENT').slice(0,100),at:op.at||o.now(),data:clone(op.data||{})}];return x},merged?'TELEMETRY_MERGED_ON_LATEST':'TELEMETRY_APPLIED');
    }
    case 'POST_TASK':{
      if(current.submission_snapshot)return reject('SNAPSHOT_ALREADY_SEALED',current);
      const clean=o.m13.sanitizePostTask(op.post_task);
      if(!expectedMatch(current,op)){
        if(current.post_task&&JSON.stringify(current.post_task)===JSON.stringify(clean))return {ok:true,action:'POST_TASK_ALREADY_APPLIED',state:current,mutated:false};
        return reject('STALE_REVISION',current,{current_revision:current.revision});
      }
      if(current.status!=='POST_TASK')return reject('POST_TASK_NOT_READY',current);
      return commit(o,current,op,'POST_TASK',x=>{
        x.post_task=clean;x.status='READY_TO_SUBMIT';
        x.telemetry=[...x.telemetry,{event_id:`${op.mutation_id}:telemetry`,type:'POST_TASK_SAVED',at:o.now(),data:{confidence:clean.confidence,deliberate_strategy_change:clean.deliberate_strategy_change}}];return x;
      },'POST_TASK_APPLIED');
    }
    case 'SEAL_SNAPSHOT':{
      if(current.submission_snapshot){
        if(!o.m13.snapshotValid(current))return reject('SUBMISSION_SNAPSHOT_INVALID',current,{blocking:true});
        return {ok:true,action:'SNAPSHOT_ALREADY_SEALED',state:current,mutated:false};
      }
      if(!expectedMatch(current,op))return reject('STALE_REVISION',current,{current_revision:current.revision});
      if(current.status!=='READY_TO_SUBMIT')return reject('SNAPSHOT_NOT_READY',current);
      return commit(o,current,op,'SEAL_SNAPSHOT',x=>{
        const sealingAt=o.now();
        x.telemetry=[...x.telemetry,{event_id:`${op.mutation_id}:telemetry`,type:'SUBMISSION_SNAPSHOT_SEALED',at:sealingAt,data:{scientific_revision:current.revision}}];
        const snap=o.m13.scientificEnvelope(x),hash=o.m13.checksum(snap);
        x.submission_snapshot=snap;x.submission_snapshot_hash=hash;x.snapshot_sealed_at=sealingAt;
        x.submission_control={...x.submission_control,retry_id:`CR0813-RETRY-${o.m13.checksumText(x.session_id+hash)}`};return x;
      },'SNAPSHOT_SEALED');
    }
    case 'CLAIM_SUBMISSION':{
      if(current.status==='SUBMITTED')return {ok:true,action:'ALREADY_SUBMITTED',state:current,mutated:false};
      if(!current.submission_snapshot||!o.m13.snapshotValid(current))return reject('SNAPSHOT_NOT_READY',current);
      const now=o.now(),c=current.submission_control;
      if(leaseActive(c,now))return reject('SUBMISSION_IN_FLIGHT',current,{lease_owner:c.lease_owner,lease_expires_at:c.lease_expires_at});
      if(typeof op.lease_token!=='string'||!op.lease_token||typeof op.lease_owner!=='string'||!op.lease_owner)return reject('LEASE_IDENTITY_REQUIRED',current);
      return commit(o,current,op,'CLAIM_SUBMISSION',x=>{
        const generation=x.submission_control.lease_generation+1;
        x.submission_control={...x.submission_control,lease_generation:generation,lease_token:op.lease_token,lease_owner:op.lease_owner,lease_expires_at:plusMs(now,(o.config.active_session&&o.config.active_session.lease_timeout_ms)||120000),attempt_count:x.submission_control.attempt_count+1,last_attempt_at:now,last_error:null};
        x.telemetry=[...x.telemetry,{event_id:`${op.mutation_id}:telemetry`,type:'SUBMISSION_LEASE_CLAIMED',at:now,data:{lease_generation:generation,retry_id:x.submission_control.retry_id}}];return x;
      },'SUBMISSION_LEASE_CLAIMED');
    }
    case 'SUBMISSION_META':{
      if(current.submission_control.lease_token!==op.lease_token)return reject('STALE_SUBMISSION_LEASE',current);
      const meta=sanitizeMeta(op.collector_meta||{});
      return commit(o,current,op,'SUBMISSION_META',x=>{x.submission_control={...x.submission_control,collector_meta:{...(x.submission_control.collector_meta||{}),...meta},collector_events:Array.isArray(op.collector_events)?clone(op.collector_events).slice(-64):x.submission_control.collector_events};return x},'SUBMISSION_META_MERGED');
    }
    case 'RELEASE_SUBMISSION':{
      if(current.status==='SUBMITTED')return {ok:true,action:'ALREADY_SUBMITTED',state:current,mutated:false};
      if(current.submission_control.lease_token!==op.lease_token)return reject('STALE_SUBMISSION_LEASE',current);
      return commit(o,current,op,'RELEASE_SUBMISSION',x=>{const at=o.now();x.submission_control={...x.submission_control,lease_token:null,lease_owner:null,lease_expires_at:null,last_error:String(op.error||'').slice(0,500)};x.telemetry=[...x.telemetry,{event_id:`${op.mutation_id}:telemetry`,type:'SUBMISSION_LEASE_RELEASED',at,data:{failed:!!op.error}}];return x},'SUBMISSION_LEASE_RELEASED');
    }
    case 'CONFIRM_SUBMISSION':{
      if(current.status==='SUBMITTED')return {ok:true,action:'ALREADY_SUBMITTED',state:current,mutated:false};
      if(current.submission_control.lease_token!==op.lease_token)return reject('STALE_SUBMISSION_LEASE',current);
      return commit(o,current,op,'CONFIRM_SUBMISSION',x=>{const at=o.now();x.status='SUBMITTED';x.submitted_at=at;x.submission_receipt=clone(op.receipt||null);x.submission_control={...x.submission_control,lease_token:null,lease_owner:null,lease_expires_at:null,receipt:clone(op.receipt||null),last_error:null};x.telemetry=[...x.telemetry,{event_id:`${op.mutation_id}:telemetry`,type:'SUBMISSION_CONFIRMED',at,data:{retry_id:x.submission_control.retry_id}}];return x},'SUBMISSION_CONFIRMED');
    }
    case 'REFRESH':return {ok:true,action:'REFRESHED',state:current,mutated:false};
    default:return reject('UNKNOWN_OPERATION',current);
  }
}

async function applyOperation(o,op){
  if(!hasLockManager(o.lockManager))return reject('LOCK_UNAVAILABLE',null,{blocking:true});
  return o.lockManager.request(LOCK_NAME,{mode:'exclusive'},()=>applyLocked(o,op));
}
function quarantineInvalid(o,raw){o.storage.setItem(o.m13.QUARANTINE_KEY,raw);o.storage.removeItem(o.m13.STORAGE_KEY)}
function resumeLocked(o,action='TARGET_RESUMED'){
  const r=readState(o);
  if(!r.state)return {action:'ABSENT',state:null};
  if(r.invalid){quarantineInvalid(o,r.raw);return {action:'INVALID_ACTIVE_STATE',state:null,blocking:true}}
  const op={type:'TELEMETRY',mutation_id:o.idFactory('resume'),event_id:o.idFactory('resume-event'),expected_revision:r.state.revision,event_type:'SESSION_RESUMED',data:{cursor:r.state.cursor,snapshot_sealed:!!r.state.submission_snapshot}};
  const z=applyLocked(o,op);return {action,state:z.state,resumed:true};
}
async function loadOrInitializeActive(o){
  if(!hasLockManager(o.lockManager))return {action:'LOCK_UNAVAILABLE',state:null,blocking:true};
  const pre=await o.lockManager.request(LOCK_NAME,{mode:'exclusive'},()=>resumeLocked(o));
  if(pre.action!=='ABSENT')return pre;
  const parent=await o.active12.loadOrInitializeActive(o.active12Deps);
  if(parent.blocking||parent.action==='LOCK_UNAVAILABLE')return parent;
  if(parent.action==='LEGACY_SEALED_RETRY'||parent.action==='ROLLED_BACK_TO_LEGACY')return parent;
  if(!parent.state)return {action:'PARENT_STATE_MISSING',state:null,blocking:true};
  return o.lockManager.request(LOCK_NAME,{mode:'exclusive'},()=>{
    const second=readState(o);
    if(second.state&&!second.invalid)return resumeLocked(o,'TARGET_RESUMED');
    if(second.invalid){quarantineInvalid(o,second.raw);return {action:'INVALID_ACTIVE_STATE',state:null,blocking:true}}
    const raw=o.storage.getItem(SOURCE_0812),x=parse(raw);
    if(!x||!o.m12.valid(x,o.parentConfig,o.parentBinding))return {action:'PARENT_STATE_INVALID',state:null,blocking:true};
    if(x.submission_snapshot||x.status==='SUBMITTED')return {action:'LEGACY_SEALED_RETRY',state:null,legacy_route:LEGACY_ROUTE};
    const target=o.m13.from0812(o.config,{binding:o.binding,parentConfig:o.parentConfig,parentBinding:o.parentBinding,parentStorageKey:SOURCE_0812,m12:o.m12,now:o.now},x);
    o.storage.setItem(o.m13.STORAGE_KEY,JSON.stringify(target));
    const verified=verifyStored(o,target);
    writeJournal(o,{schema_version:'CR0813-ACTIVE-WRITE-JOURNAL-1',session_id:verified.session_id,mutation_id:verified.mutation_history[0].mutation_id,type:'ACTIVE_SESSION_UPGRADE',from_revision:0,to_revision:1,outcome:'UPGRADED_FROM_0812',committed_at:verified.updated_at,integrity:verified.integrity});
    return {action:'UPGRADED_FROM_0812',state:verified,resumed:false};
  });
}
function makeIdFactory(cryptoObj){return prefix=>{const a=new Uint32Array(2);cryptoObj.getRandomValues(a);return `CR0813-${String(prefix||'M').toUpperCase()}-${Array.from(a,x=>x.toString(16).padStart(8,'0')).join('')}`}}

const api={LOCK_NAME,JOURNAL_KEY,CONFLICT_KEY,SOURCE_0812,LEGACY_ROUTE,clone,parse,hasLockManager,mutationSeen,telemetrySeen,readState,writeConflict,applyLocked,applyOperation,loadOrInitializeActive,makeIdFactory};
if(typeof module!=='undefined'&&module.exports)module.exports=api;
global.CUBE_REV_ACTIVE_SESSION_CAS_0813=api;
})(typeof window!=='undefined'?window:globalThis);
