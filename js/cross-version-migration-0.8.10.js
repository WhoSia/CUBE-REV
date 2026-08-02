(function(global){
'use strict';

const VERSION='CUBE-REV 0.8.10';
const JOURNAL_KEY='cube-rev-migration-0810-v1';
const MIGRATION_QUARANTINE_KEY='cube-rev-migration-0810-quarantine-v1';
const ARCHIVE_PREFIX='cube-rev-migrated-legacy-0810-';
const SOURCE_088='cube-rev-cognitive-mode-0808-v1';
const SOURCE_089='cube-rev-cognitive-mode-0809-v1';
const ELIGIBLE=new Set(['IN_PROGRESS','POST_TASK','READY_TO_SUBMIT']);

function parse(raw){try{return JSON.parse(raw)}catch(e){return null}}
function fingerprint(raw,m10){return m10.fnv1a(raw).toString(16).padStart(8,'0')}
function bankIndex(bank){return Object.fromEntries((bank.stimuli||[]).map(x=>[x.stimulus_id,x]))}
function legacyRoute(version){return version==='CUBE-REV 0.8.8'?'participant-cognitive-mode-0.8.8.html':'participant-cognitive-mode-0.8.9.html'}
function migrationId(source,raw,m10){return `CR0810-MIG-${source.version.replace(/\D/g,'')}-${fingerprint(raw,m10)}-${source.session_id}`}
function quarantine(storage,reason,entries,now){
  const value={schema_version:'CR0810-MIGRATION-QUARANTINE-1',version:VERSION,reason,at:now(),entries};
  storage.setItem(MIGRATION_QUARANTINE_KEY,JSON.stringify(value));
  return value;
}
function sealed(source){return !!source.submission_snapshot||source.status==='SUBMITTED'}
function stateShapeValid(source){
  if(!source||!Number.isInteger(source.cursor)||!Array.isArray(source.responses)||source.cursor!==source.responses.length)return false;
  const complete=source.cursor===28,hasPost=!!source.post_task,hasSnapshot=!!source.submission_snapshot;
  if(hasSnapshot)return complete&&hasPost&&['READY_TO_SUBMIT','SUBMITTED'].includes(source.status);
  if(source.status==='SUBMITTED')return false;
  if(source.status==='IN_PROGRESS')return source.cursor>=0&&source.cursor<28&&!hasPost;
  if(source.status==='POST_TASK')return complete&&!hasPost;
  if(source.status==='READY_TO_SUBMIT')return complete&&hasPost;
  return false;
}
function normalize088(source,bank,m10){
  const byId=bankIndex(bank);
  const responses=source.responses.map((r,i)=>{
    const stimulus=byId[r.stimulus_id];
    if(!stimulus)throw new Error(`MIGRATION_STIMULUS_UNKNOWN:${r.stimulus_id}`);
    const code=(stimulus.choice_codes||{})[r.choice_display];
    if(!code)throw new Error(`MIGRATION_DISPLAY_UNMAPPED:${r.stimulus_id}:${r.choice_display}`);
    if(r.position!==i+1||r.stimulus_id!==source.schedule[i])throw new Error(`MIGRATION_RESPONSE_ORDER:${i+1}`);
    return {stimulus_id:r.stimulus_id,choice_display:r.choice_display,choice_code:code,latency_ms:r.latency_ms,position:r.position,recorded_at:r.recorded_at};
  });
  if(!responses.every(m10.validResponse))throw new Error('MIGRATION_088_RESPONSE_INVALID');
  return responses;
}
function normalize089(source,m10){
  const responses=source.responses.map((r,i)=>({
    stimulus_id:r.stimulus_id,choice_display:r.choice_display,choice_code:r.choice_code,
    latency_ms:r.latency_ms,position:r.position,recorded_at:r.recorded_at
  }));
  if(responses.some((r,i)=>r.position!==i+1||r.stimulus_id!==source.schedule[i]||!m10.validResponse(r)))throw new Error('MIGRATION_089_RESPONSE_INVALID');
  return responses;
}
function material(source,raw,sourceKey,responses){
  return {
    source_version:source.version,source_schema:source.schema_version,source_storage_key:sourceKey,
    source_integrity:source.integrity,source_revision:source.revision||0,session_id:source.session_id,
    mode_id:source.mode_id,participant_token:source.participant_token,sequence_id:source.sequence_id,
    schedule:[...source.schedule],cursor:source.cursor,responses,telemetry:[...(source.telemetry||[])],
    post_task:source.post_task||null,status:source.status,created_at:source.created_at,source_raw:raw
  };
}
function writeJournal(storage,journal){storage.setItem(JOURNAL_KEY,JSON.stringify(journal));return journal}
function validateSource(raw,version,o){
  const source=parse(raw);
  if(!source)return {valid:false,source:null,failure:'PARSE'};
  const runtimeValid=version==='0.8.8'?o.m088.valid(source,o.config088):o.m089.valid(source,o.config089);
  if(!runtimeValid)return {valid:false,source,failure:'LEGACY_RUNTIME_CONTRACT'};
  if(!stateShapeValid(source))return {valid:false,source,failure:'STATE_MACHINE_SHAPE'};
  return {valid:true,source,failure:null};
}
function chooseSource(o){
  const raw088=o.storage.getItem(SOURCE_088),raw089=o.storage.getItem(SOURCE_089);
  const a=raw088?validateSource(raw088,'0.8.8',o):null;
  const b=raw089?validateSource(raw089,'0.8.9',o):null;
  const invalid=[];
  if(a&&!a.valid)invalid.push({source_storage_key:SOURCE_088,raw:raw088,failure:a.failure});
  if(b&&!b.valid)invalid.push({source_storage_key:SOURCE_089,raw:raw089,failure:b.failure});
  if(invalid.length)return {kind:'INVALID',invalid};
  const valid=[];
  if(a&&a.valid)valid.push({source:a.source,raw:raw088,key:SOURCE_088,version:'0.8.8'});
  if(b&&b.valid)valid.push({source:b.source,raw:raw089,key:SOURCE_089,version:'0.8.9'});
  if(valid.length>1)return {kind:'CONFLICT',valid};
  if(!valid.length)return {kind:'NONE'};
  return {kind:'ONE',...valid[0]};
}
function migrateOne(o,selected){
  const {storage,m10,config10,bank10,binding,now}=o;
  const source=selected.source,raw=selected.raw;
  if(sealed(source))return {action:'LEGACY_SEALED_RETRY',source_version:source.version,legacy_route:legacyRoute(source.version),source_unchanged:true};
  if(!ELIGIBLE.has(source.status))throw new Error(`MIGRATION_STATUS_UNSUPPORTED:${source.status}`);
  const responses=selected.version==='0.8.8'?normalize088(source,bank10,m10):normalize089(source,m10);
  const m=material(source,raw,selected.key,responses);
  const id=migrationId(source,raw,m10),preparedAt=now();
  writeJournal(storage,{schema_version:'CR0810-MIGRATION-JOURNAL-1',version:VERSION,migration_id:id,state:'PREPARED',prepared_at:preparedAt,source_version:source.version,source_storage_key:selected.key,source_fingerprint:fingerprint(raw,m10),source_integrity:source.integrity,target_storage_key:m10.STORAGE_KEY});
  let targetWritten=false;
  try{
    if(o.injectFailure==='AFTER_JOURNAL')throw new Error('INJECTED_AFTER_JOURNAL');
    const target=m10.fromMigration(config10,{binding,now},m);
    if(!m10.valid(target,config10,binding))throw new Error('MIGRATED_TARGET_INVALID_PREWRITE');
    storage.setItem(m10.STORAGE_KEY,JSON.stringify(target));targetWritten=true;
    if(o.injectFailure==='AFTER_TARGET_WRITE')throw new Error('INJECTED_AFTER_TARGET_WRITE');
    const reread=parse(storage.getItem(m10.STORAGE_KEY));
    if(!m10.valid(reread,config10,binding))throw new Error('MIGRATED_TARGET_INVALID_REREAD');
    if(reread.participant_token!==source.participant_token||reread.sequence_id!==source.sequence_id||reread.schedule.join('|')!==source.schedule.join('|')||reread.cursor!==source.cursor)throw new Error('ASSIGNMENT_CONTINUITY_FAILURE');
    if(storage.getItem(selected.key)!==raw)throw new Error('SOURCE_MUTATED');
    const archiveKey=`${ARCHIVE_PREFIX}${selected.version.replace(/\./g,'')}-${fingerprint(raw,m10)}`;
    storage.setItem(archiveKey,raw);
    writeJournal(storage,{schema_version:'CR0810-MIGRATION-JOURNAL-1',version:VERSION,migration_id:id,state:'COMMITTED',prepared_at:preparedAt,committed_at:now(),source_version:source.version,source_storage_key:selected.key,source_fingerprint:fingerprint(raw,m10),source_integrity:source.integrity,target_storage_key:m10.STORAGE_KEY,target_integrity:reread.integrity,archive_key:archiveKey,source_preserved:true});
    return {action:'MIGRATED',state:reread,resumed:true,source_version:source.version,journal_state:'COMMITTED',source_unchanged:true,archive_key:archiveKey};
  }catch(e){
    if(targetWritten)storage.removeItem(m10.STORAGE_KEY);
    writeJournal(storage,{schema_version:'CR0810-MIGRATION-JOURNAL-1',version:VERSION,migration_id:id,state:'ROLLED_BACK',prepared_at:preparedAt,rolled_back_at:now(),source_version:source.version,source_storage_key:selected.key,source_fingerprint:fingerprint(raw,m10),error:String(e.message||e),source_preserved:storage.getItem(selected.key)===raw});
    throw e;
  }
}
function loadOrMigrate(o){
  const existing=o.m10.loadExisting(o.config10,{storage:o.storage,binding:o.binding,now:o.now});
  if(existing.state)return {action:'TARGET_RESUMED',state:existing.state,resumed:true};
  const selected=chooseSource(o);
  if(selected.kind==='INVALID'){
    quarantine(o.storage,'INVALID_LEGACY_SOURCE',selected.invalid,o.now);
    return {action:'SOURCE_INVALID',resumed:false};
  }
  if(selected.kind==='CONFLICT'){
    quarantine(o.storage,'MULTIPLE_VALID_LEGACY_SOURCES',selected.valid.map(x=>({source_storage_key:x.key,version:x.source.version,session_id:x.source.session_id,integrity:x.source.integrity})),o.now);
    return {action:'SOURCE_CONFLICT',resumed:false};
  }
  if(selected.kind==='NONE')return {action:'NO_SOURCE',resumed:false};
  return migrateOne(o,selected);
}

const api={VERSION,JOURNAL_KEY,MIGRATION_QUARANTINE_KEY,ARCHIVE_PREFIX,SOURCE_088,SOURCE_089,parse,fingerprint,bankIndex,legacyRoute,migrationId,quarantine,sealed,stateShapeValid,normalize088,normalize089,material,validateSource,chooseSource,migrateOne,loadOrMigrate};
if(typeof module!=='undefined'&&module.exports)module.exports=api;
global.CUBE_REV_MIGRATION_0810=api;
})(typeof window!=='undefined'?window:globalThis);
