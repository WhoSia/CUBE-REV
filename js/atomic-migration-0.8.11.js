(function(global){
'use strict';

const VERSION='CUBE-REV 0.8.11';
const LOCK_NAME='cube-rev-migration-0811-exclusive-v1';
const JOURNAL_KEY='cube-rev-migration-0811-journal-v1';
const EPOCH_KEY='cube-rev-migration-0811-epoch-v1';
const OWNER_KEY='cube-rev-migration-0811-owner-v1';
const FENCE_KEY='cube-rev-migration-0811-fence-v1';
const QUARANTINE_KEY='cube-rev-migration-0811-quarantine-v1';
const ARCHIVE_PREFIX='cube-rev-migrated-legacy-0811-';
const SOURCE_088='cube-rev-cognitive-mode-0808-v1';
const SOURCE_089='cube-rev-cognitive-mode-0809-v1';
const SOURCE_0810='cube-rev-cognitive-mode-0810-v1';
const ELIGIBLE=new Set(['IN_PROGRESS','POST_TASK','READY_TO_SUBMIT']);
const PHASES=new Set(['PREPARED','TARGET_WRITTEN','ARCHIVE_WRITTEN','FENCE_WRITTEN','COMMITTED','ROLLED_BACK','ROLLED_BACK_TO_LEGACY']);

function parse(raw){try{return JSON.parse(raw)}catch(e){return null}}
function fingerprint(raw,m11){return m11.fnv1a(String(raw)).toString(16).padStart(8,'0')}
function bankIndex(bank){return Object.fromEntries((bank.stimuli||[]).map(x=>[x.stimulus_id,x]))}
function legacyRoute(version){
  if(version==='CUBE-REV 0.8.8')return 'participant-cognitive-mode-0.8.8.html';
  if(version==='CUBE-REV 0.8.9')return 'participant-cognitive-mode-0.8.9.html';
  return 'participant-cognitive-mode-0.8.10.html';
}
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
function sealed(source){return !!source.submission_snapshot||source.status==='SUBMITTED'}
function randomOwner(o){
  if(typeof o.ownerIdFactory==='function')return String(o.ownerIdFactory());
  const c=o.cryptoObj||global.crypto;
  if(c&&typeof c.getRandomValues==='function'){
    const a=new Uint32Array(3);c.getRandomValues(a);return 'CR0811-OWNER-'+Array.from(a,x=>x.toString(16).padStart(8,'0')).join('');
  }
  return 'CR0811-OWNER-'+String(o.now()).replace(/\D/g,'')+'-'+Math.random().toString(16).slice(2);
}
function currentEpoch(storage){const n=Number(storage.getItem(EPOCH_KEY)||0);return Number.isSafeInteger(n)&&n>=0?n:0}
function acquireOwner(o){
  const epoch=currentEpoch(o.storage)+1,owner={schema_version:'CR0811-MIGRATION-OWNER-1',version:VERSION,epoch,owner_id:randomOwner(o),status:'ACTIVE',acquired_at:o.now()};
  o.storage.setItem(EPOCH_KEY,String(epoch));o.storage.setItem(OWNER_KEY,JSON.stringify(owner));
  const reread=parse(o.storage.getItem(OWNER_KEY));
  if(!reread||reread.epoch!==epoch||reread.owner_id!==owner.owner_id||reread.status!=='ACTIVE')throw new Error('OWNER_ACQUIRE_FAILED');
  return owner;
}
function assertOwner(storage,owner){
  const x=parse(storage.getItem(OWNER_KEY));
  if(!x||x.status!=='ACTIVE'||x.epoch!==owner.epoch||x.owner_id!==owner.owner_id)throw new Error('STALE_MIGRATION_OWNER');
  return true;
}
function releaseOwner(o,owner){
  const x=parse(o.storage.getItem(OWNER_KEY));
  if(x&&x.status==='ACTIVE'&&x.epoch===owner.epoch&&x.owner_id===owner.owner_id){
    o.storage.setItem(OWNER_KEY,JSON.stringify({...x,status:'RELEASED',released_at:o.now()}));
  }
}
function fencedSet(storage,owner,key,value){assertOwner(storage,owner);storage.setItem(key,String(value));assertOwner(storage,owner)}
function fencedRemove(storage,owner,key){assertOwner(storage,owner);storage.removeItem(key);assertOwner(storage,owner)}
function readJournal(storage){const x=parse(storage.getItem(JOURNAL_KEY));return x&&x.schema_version==='CR0811-ATOMIC-MIGRATION-JOURNAL-1'&&PHASES.has(x.phase)?x:null}
function writeJournal(o,owner,base,phase,patch={}){
  if(!PHASES.has(phase))throw new Error(`JOURNAL_PHASE_INVALID:${phase}`);
  assertOwner(o.storage,owner);
  const x={...base,...patch,schema_version:'CR0811-ATOMIC-MIGRATION-JOURNAL-1',version:VERSION,phase,last_writer_epoch:owner.epoch,last_writer_owner:owner.owner_id,updated_at:o.now()};
  fencedSet(o.storage,owner,JOURNAL_KEY,JSON.stringify(x));return x;
}
function writeFence(o,owner,journal,status='ACTIVE_TARGET_AUTHORITY'){
  const x={schema_version:'CR0811-DOWNGRADE-FENCE-1',version:VERSION,status,transaction_id:journal.transaction_id,migration_epoch:journal.transaction_epoch,source_version:journal.source_version,source_storage_key:journal.source_storage_key,source_fingerprint:journal.source_fingerprint,target_storage_key:journal.target_storage_key,target_integrity:journal.target_integrity,archive_key:journal.archive_key,written_at:o.now(),last_writer_epoch:owner.epoch};
  fencedSet(o.storage,owner,FENCE_KEY,JSON.stringify(x));return x;
}
function quarantine(o,owner,reason,evidence){
  assertOwner(o.storage,owner);
  const previous=parse(o.storage.getItem(QUARANTINE_KEY));
  const entries=previous&&Array.isArray(previous.entries)?previous.entries:[];
  const item={reason,at:o.now(),owner_epoch:owner.epoch,evidence};
  fencedSet(o.storage,owner,QUARANTINE_KEY,JSON.stringify({schema_version:'CR0811-MIGRATION-QUARANTINE-1',version:VERSION,entries:[...entries,item].slice(-20)}));
  return item;
}
function migrationId(source,raw,owner,m11){return `CR0811-MIG-${source.version.replace(/\D/g,'')}-${fingerprint(raw,m11)}-${owner.epoch}-${source.session_id}`}
function archiveKey(version,raw,m11){return `${ARCHIVE_PREFIX}${version.replace(/\D/g,'')}-${fingerprint(raw,m11)}`}
function simulatedCrash(phase){const e=new Error(`SIMULATED_CRASH:${phase}`);e.simulatedCrash=true;return e}
function maybeCrash(o,phase){if(o.injectCrash===phase)throw simulatedCrash(phase)}

function normalize088(source,bank,m11){
  const by=bankIndex(bank);
  const responses=source.responses.map((r,i)=>{
    const stimulus=by[r.stimulus_id],code=stimulus&&stimulus.choice_codes&&stimulus.choice_codes[r.choice_display];
    if(!stimulus)throw new Error(`MIGRATION_STIMULUS_UNKNOWN:${r.stimulus_id}`);
    if(!code)throw new Error(`MIGRATION_DISPLAY_UNMAPPED:${r.stimulus_id}:${r.choice_display}`);
    if(r.position!==i+1||r.stimulus_id!==source.schedule[i])throw new Error(`MIGRATION_RESPONSE_ORDER:${i+1}`);
    return {stimulus_id:r.stimulus_id,choice_display:r.choice_display,choice_code:code,latency_ms:r.latency_ms,position:r.position,recorded_at:r.recorded_at};
  });
  if(!responses.every(m11.validResponse))throw new Error('MIGRATION_088_RESPONSE_INVALID');
  return responses;
}
function normalizeOpaque(source,m11,label){
  const responses=source.responses.map((r,i)=>({stimulus_id:r.stimulus_id,choice_display:r.choice_display,choice_code:r.choice_code,latency_ms:r.latency_ms,position:r.position,recorded_at:r.recorded_at}));
  if(responses.some((r,i)=>r.position!==i+1||r.stimulus_id!==source.schedule[i]||!m11.validResponse(r)))throw new Error(`MIGRATION_${label}_RESPONSE_INVALID`);
  return responses;
}
function material(selected,responses){
  const s=selected.source;
  return {source_version:s.version,source_schema:s.schema_version,source_storage_key:selected.key,source_integrity:s.integrity,source_revision:s.revision||0,session_id:s.session_id,mode_id:s.mode_id,participant_token:s.participant_token,sequence_id:s.sequence_id,schedule:[...s.schedule],cursor:s.cursor,responses,telemetry:[...(s.telemetry||[])],post_task:s.post_task||null,status:s.status,created_at:s.created_at,previous_provenance:s.migration_provenance||null};
}
function commonResponseEqual(a,b){return a&&b&&['stimulus_id','choice_display','latency_ms','position','recorded_at'].every(k=>a[k]===b[k])}
function compatibleAncestor(lower,higher){
  const a=lower.source,b=higher.source,p=b.migration_provenance;
  if(!p||p.source_storage_key!==lower.key||p.source_integrity!==a.integrity)return false;
  if(a.participant_token!==b.participant_token||a.session_id!==b.session_id||a.sequence_id!==b.sequence_id)return false;
  if((a.schedule||[]).join('|')!==(b.schedule||[]).join('|')||a.cursor>b.cursor)return false;
  for(let i=0;i<a.responses.length;i++)if(!commonResponseEqual(a.responses[i],b.responses[i]))return false;
  return true;
}
function validateSource(raw,desc,o){
  const source=parse(raw);if(!source)return {valid:false,source:null,failure:'PARSE'};
  let runtimeValid=false;
  if(desc.version==='0.8.8')runtimeValid=o.m088.valid(source,o.config088);
  else if(desc.version==='0.8.9')runtimeValid=o.m089.valid(source,o.config089);
  else runtimeValid=o.m10.valid(source,o.config10,o.parent0810Binding);
  if(!runtimeValid)return {valid:false,source,failure:'RUNTIME_CONTRACT'};
  if(!stateShapeValid(source))return {valid:false,source,failure:'STATE_MACHINE_SHAPE'};
  return {valid:true,source,failure:null};
}
function inspectSources(o){
  const descs=[{version:'0.8.8',key:SOURCE_088},{version:'0.8.9',key:SOURCE_089},{version:'0.8.10',key:SOURCE_0810}];
  return descs.map(d=>{const raw=o.storage.getItem(d.key);if(raw==null)return {...d,present:false};const v=validateSource(raw,d,o);return {...d,present:true,raw,...v}});
}
function selectSource(o){
  const all=inspectSources(o),v10=all.find(x=>x.version==='0.8.10'),v9=all.find(x=>x.version==='0.8.9'),v8=all.find(x=>x.version==='0.8.8');
  if(v10&&v10.present&&!v10.valid)return {kind:'INVALID_HIGHER_SOURCE',entries:[v10]};
  if(v10&&v10.valid){
    const lowers=[v8,v9].filter(x=>x&&x.present);
    const incompatible=lowers.filter(x=>!x.valid||!compatibleAncestor(x,v10));
    if(incompatible.length)return {kind:'ANCESTRY_CONFLICT',selected:v10,entries:incompatible};
    return {kind:'ONE',selected:v10};
  }
  const invalid=[v8,v9].filter(x=>x&&x.present&&!x.valid);
  if(invalid.length)return {kind:'INVALID_SOURCE',entries:invalid};
  if(v8&&v8.valid&&v9&&v9.valid)return {kind:'SOURCE_CONFLICT',entries:[v8,v9]};
  const one=[v8,v9].find(x=>x&&x.valid);return one?{kind:'ONE',selected:one}:{kind:'NONE'};
}
function targetInfo(o){
  const raw=o.storage.getItem(o.m11.STORAGE_KEY);if(raw==null)return {raw:null,state:null,valid:false,present:false};
  const state=parse(raw);return {raw,state,valid:!!state&&o.m11.valid(state,o.config11,o.binding),present:true};
}
function targetMatchesJournal(info,j){
  if(!info.valid)return false;
  const s=info.state,p=s.migration_provenance;
  return s.integrity===j.target_integrity&&s.upgrade_epoch===j.transaction_epoch&&p&&p.source_storage_key===j.source_storage_key&&p.source_integrity===j.source_integrity&&s.session_id===j.source_session_id;
}
function resumeState(o,owner,state,type,data){assertOwner(o.storage,owner);return o.m11.event(o.storage,state,type,data,o.now)}

function rollbackPreAuthority(o,owner,j,reason){
  const t=targetInfo(o);if(t.present)fencedRemove(o.storage,owner,o.m11.STORAGE_KEY);
  const next=writeJournal(o,owner,j,'ROLLED_BACK',{rolled_back_at:o.now(),rollback_reason:reason,source_preserved:o.storage.getItem(j.source_storage_key)===j.source_raw});
  return {action:'RECOVERED_ROLLBACK',journal:next,continue_selection:true};
}
function divergenceHold(o,owner,j,reason){
  const t=targetInfo(o);quarantine(o,owner,reason,{journal:j,current_source_raw:o.storage.getItem(j.source_storage_key),target_raw:t.raw});
  if(t.present)fencedRemove(o.storage,owner,o.m11.STORAGE_KEY);
  writeJournal(o,owner,j,'ROLLED_BACK',{rolled_back_at:o.now(),rollback_reason:reason,source_preserved:false});
  return {action:reason,resumed:false,blocking:true};
}
function reconcileCommitted(o,owner,j){
  const t=targetInfo(o),sourceRaw=o.storage.getItem(j.source_storage_key),archiveRaw=o.storage.getItem(j.archive_key),sourceMatches=sourceRaw===j.source_raw,archiveMatches=archiveRaw===j.source_raw;
  if(t.valid&&targetMatchesJournal(t,j)){
    if(!archiveMatches){quarantine(o,owner,'COMMITTED_ARCHIVE_INTEGRITY_HOLD',{journal:j,archive_raw:archiveRaw,target_raw:t.raw});return {action:'COMMITTED_ARCHIVE_INTEGRITY_HOLD',blocking:true}}
    if(!sourceMatches){
      quarantine(o,owner,'DOWNGRADE_SOURCE_MUTATION',{journal:j,mutated_source_raw:sourceRaw,target_integrity:t.state.integrity});
      const state=resumeState(o,owner,t.state,'DOWNGRADE_SOURCE_MUTATION_QUARANTINED',{migration_epoch:j.transaction_epoch,source_storage_key:j.source_storage_key});
      return {action:'DOWNGRADE_MUTATION_QUARANTINED',state,resumed:true};
    }
    const state=resumeState(o,owner,t.state,'ATOMIC_TARGET_RESUMED',{migration_epoch:j.transaction_epoch});
    return {action:'TARGET_RESUMED',state,resumed:true};
  }
  if(sourceMatches&&archiveMatches){
    if(t.present)fencedRemove(o.storage,owner,o.m11.STORAGE_KEY);
    const next=writeJournal(o,owner,j,'ROLLED_BACK_TO_LEGACY',{rolled_back_at:o.now(),rollback_reason:'COMMITTED_TARGET_LOST',source_preserved:true});
    writeFence(o,owner,next,'ROLLED_BACK_TO_LEGACY');
    return {action:'ROLLED_BACK_TO_LEGACY',legacy_route:legacyRoute(j.source_version),source_version:j.source_version,resumed:false};
  }
  quarantine(o,owner,'TARGET_LOSS_WITH_SOURCE_DIVERGENCE',{journal:j,current_source_raw:sourceRaw,archive_raw:archiveRaw,target_raw:t.raw});
  return {action:'TARGET_LOSS_WITH_SOURCE_DIVERGENCE',blocking:true,resumed:false};
}
function reconcile(o,owner){
  let j=readJournal(o.storage);const fence=parse(o.storage.getItem(FENCE_KEY));
  if(!j){
    if(fence){quarantine(o,owner,'ORPHAN_FENCE_WITHOUT_JOURNAL',{fence});return {action:'ORPHAN_FENCE_WITHOUT_JOURNAL',blocking:true}}
    return {action:'NO_JOURNAL',continue_selection:true};
  }
  if(j.phase==='ROLLED_BACK')return {action:'PRIOR_ROLLBACK',continue_selection:true,journal:j};
  if(j.phase==='ROLLED_BACK_TO_LEGACY')return {action:'ROLLED_BACK_TO_LEGACY',legacy_route:legacyRoute(j.source_version),source_version:j.source_version};
  if(j.phase==='COMMITTED')return reconcileCommitted(o,owner,j);

  let t=targetInfo(o),sourceRaw=o.storage.getItem(j.source_storage_key),sourceMatches=sourceRaw===j.source_raw;
  if(j.phase==='PREPARED'){
    if(!t.present)return sourceMatches?rollbackPreAuthority(o,owner,j,'CRASH_AFTER_PREPARED'):divergenceHold(o,owner,j,'PREPARED_SOURCE_DIVERGENCE');
    if(!t.valid)return sourceMatches?rollbackPreAuthority(o,owner,j,'INVALID_ORPHAN_TARGET'):divergenceHold(o,owner,j,'INVALID_TARGET_SOURCE_DIVERGENCE');
    j=writeJournal(o,owner,j,'TARGET_WRITTEN',{target_integrity:t.state.integrity,target_written_at:o.now(),recovered_from:'PREPARED'});
  }
  t=targetInfo(o);sourceRaw=o.storage.getItem(j.source_storage_key);sourceMatches=sourceRaw===j.source_raw;
  if(j.phase==='TARGET_WRITTEN'){
    if(!targetMatchesJournal(t,j))return sourceMatches?rollbackPreAuthority(o,owner,j,'TARGET_VALIDATION_FAILURE'):divergenceHold(o,owner,j,'TARGET_SOURCE_DIVERGENCE');
    if(!sourceMatches)return divergenceHold(o,owner,j,'PRE_FENCE_SOURCE_DIVERGENCE');
    const archiveRaw=o.storage.getItem(j.archive_key);
    if(archiveRaw!=null&&archiveRaw!==j.source_raw){quarantine(o,owner,'ARCHIVE_COLLISION',{journal:j,archive_raw:archiveRaw});return {action:'ARCHIVE_COLLISION',blocking:true}}
    if(archiveRaw==null)fencedSet(o.storage,owner,j.archive_key,j.source_raw);
    j=writeJournal(o,owner,j,'ARCHIVE_WRITTEN',{archive_written_at:o.now()});
  }
  t=targetInfo(o);sourceMatches=o.storage.getItem(j.source_storage_key)===j.source_raw;
  if(j.phase==='ARCHIVE_WRITTEN'){
    if(!targetMatchesJournal(t,j)||o.storage.getItem(j.archive_key)!==j.source_raw)return rollbackPreAuthority(o,owner,j,'ARCHIVE_OR_TARGET_VALIDATION_FAILURE');
    if(!sourceMatches)return divergenceHold(o,owner,j,'PRE_FENCE_SOURCE_DIVERGENCE');
    writeFence(o,owner,j,'ACTIVE_TARGET_AUTHORITY');
    j=writeJournal(o,owner,j,'FENCE_WRITTEN',{fence_written_at:o.now()});
  }
  if(j.phase==='FENCE_WRITTEN'){
    t=targetInfo(o);
    if(!targetMatchesJournal(t,j)||o.storage.getItem(j.archive_key)!==j.source_raw){quarantine(o,owner,'POST_FENCE_TARGET_OR_ARCHIVE_FAILURE',{journal:j,target_raw:t.raw,archive_raw:o.storage.getItem(j.archive_key)});return {action:'POST_FENCE_TARGET_OR_ARCHIVE_FAILURE',blocking:true}}
    const diverged=o.storage.getItem(j.source_storage_key)!==j.source_raw;
    if(diverged)quarantine(o,owner,'DOWNGRADE_SOURCE_MUTATION_BEFORE_COMMIT',{journal:j,mutated_source_raw:o.storage.getItem(j.source_storage_key)});
    j=writeJournal(o,owner,j,'COMMITTED',{committed_at:o.now(),downgrade_mutation_detected:diverged});
    writeFence(o,owner,j,'COMMITTED_TARGET_AUTHORITY');
    const state=resumeState(o,owner,t.state,diverged?'DOWNGRADE_SOURCE_MUTATION_QUARANTINED':'ATOMIC_MIGRATION_RECOVERED',{migration_epoch:j.transaction_epoch,recovered:true});
    return {action:diverged?'DOWNGRADE_MUTATION_QUARANTINED':'RECOVERED_COMMIT',state,resumed:true};
  }
  return {action:'JOURNAL_PHASE_UNHANDLED',blocking:true};
}

function migrateSelected(o,owner,selected,previousJournal){
  const source=selected.source,raw=selected.raw;
  if(sealed(source))return {action:'LEGACY_SEALED_RETRY',source_version:source.version,legacy_route:legacyRoute(source.version),source_unchanged:true};
  if(!ELIGIBLE.has(source.status))throw new Error(`MIGRATION_STATUS_UNSUPPORTED:${source.status}`);
  let responses;
  if(selected.version==='0.8.8')responses=normalize088(source,o.bank11,o.m11);
  else if(selected.version==='0.8.9')responses=normalizeOpaque(source,o.m11,'089');
  else responses=normalizeOpaque(source,o.m11,'0810');
  const m=material(selected,responses),aKey=archiveKey(source.version,raw,o.m11),id=migrationId(source,raw,owner,o.m11);
  let j=writeJournal(o,owner,{
    transaction_id:id,transaction_epoch:owner.epoch,source_version:source.version,source_schema:source.schema_version,
    source_storage_key:selected.key,source_session_id:source.session_id,source_integrity:source.integrity,
    source_fingerprint:fingerprint(raw,o.m11),source_raw:raw,target_storage_key:o.m11.STORAGE_KEY,archive_key:aKey,
    prepared_at:o.now(),previous_terminal_phase:previousJournal&&previousJournal.phase||null
  },'PREPARED');
  try{
    maybeCrash(o,'PREPARED');
    const target=o.m11.fromMigration(o.config11,{binding:o.binding,epoch:owner.epoch,now:o.now},m);
    if(!o.m11.valid(target,o.config11,o.binding))throw new Error('MIGRATED_TARGET_INVALID_PREWRITE');
    fencedSet(o.storage,owner,o.m11.STORAGE_KEY,JSON.stringify(target));
    j=writeJournal(o,owner,j,'TARGET_WRITTEN',{target_integrity:target.integrity,target_written_at:o.now()});
    maybeCrash(o,'TARGET_WRITTEN');
    if(o.storage.getItem(selected.key)!==raw)throw new Error('PRE_FENCE_SOURCE_DIVERGENCE');
    const oldArchive=o.storage.getItem(aKey);if(oldArchive!=null&&oldArchive!==raw)throw new Error('ARCHIVE_COLLISION');
    if(oldArchive==null)fencedSet(o.storage,owner,aKey,raw);
    j=writeJournal(o,owner,j,'ARCHIVE_WRITTEN',{archive_written_at:o.now()});
    maybeCrash(o,'ARCHIVE_WRITTEN');
    if(o.storage.getItem(selected.key)!==raw)throw new Error('PRE_FENCE_SOURCE_DIVERGENCE');
    writeFence(o,owner,j,'ACTIVE_TARGET_AUTHORITY');
    j=writeJournal(o,owner,j,'FENCE_WRITTEN',{fence_written_at:o.now()});
    maybeCrash(o,'FENCE_WRITTEN');
    const diverged=o.storage.getItem(selected.key)!==raw;
    if(diverged)quarantine(o,owner,'DOWNGRADE_SOURCE_MUTATION_BEFORE_COMMIT',{journal:j,mutated_source_raw:o.storage.getItem(selected.key)});
    j=writeJournal(o,owner,j,'COMMITTED',{committed_at:o.now(),downgrade_mutation_detected:diverged});
    writeFence(o,owner,j,'COMMITTED_TARGET_AUTHORITY');
    maybeCrash(o,'COMMITTED');
    const reread=targetInfo(o);
    if(!targetMatchesJournal(reread,j))throw new Error('COMMITTED_TARGET_INVALID');
    return {action:diverged?'MIGRATED_WITH_DOWNGRADE_QUARANTINE':'MIGRATED',state:reread.state,resumed:true,source_version:source.version,journal_state:'COMMITTED',migration_epoch:owner.epoch,archive_key:aKey};
  }catch(e){
    if(e.simulatedCrash)throw e;
    const current=readJournal(o.storage)||j;
    if(current.phase==='FENCE_WRITTEN'||current.phase==='COMMITTED')throw e;
    if(o.storage.getItem(o.m11.STORAGE_KEY)!=null)fencedRemove(o.storage,owner,o.m11.STORAGE_KEY);
    writeJournal(o,owner,current,'ROLLED_BACK',{rolled_back_at:o.now(),rollback_reason:String(e.message||e),source_preserved:o.storage.getItem(selected.key)===raw});
    throw e;
  }
}

async function loadOrInitializeAtomic(o){
  if(!o||!o.lockManager||typeof o.lockManager.request!=='function')return {action:'LOCK_UNAVAILABLE',blocking:true,resumed:false};
  return o.lockManager.request(LOCK_NAME,{mode:'exclusive'},async()=>{
    const owner=acquireOwner(o);
    try{
      const recovery=reconcile(o,owner);
      if(recovery.blocking||recovery.state||recovery.action==='ROLLED_BACK_TO_LEGACY')return recovery;
      const target=targetInfo(o);
      if(target.present){
        if(!target.valid){quarantine(o,owner,'UNJOURNALED_TARGET_INVALID',{target_raw:target.raw});return {action:'UNJOURNALED_TARGET_INVALID',blocking:true}}
        const state=resumeState(o,owner,target.state,'ATOMIC_TARGET_RESUMED',{owner_epoch:owner.epoch,unjournaled_fresh_session:true});
        return {action:'TARGET_RESUMED',state,resumed:true};
      }
      const selection=selectSource(o);
      if(selection.kind==='INVALID_HIGHER_SOURCE'||selection.kind==='INVALID_SOURCE'||selection.kind==='SOURCE_CONFLICT'||selection.kind==='ANCESTRY_CONFLICT'){
        quarantine(o,owner,selection.kind,{entries:selection.entries&&selection.entries.map(x=>({version:x.version,key:x.key,failure:x.failure,raw:x.raw})),selected:selection.selected&&{version:selection.selected.version,key:selection.selected.key}});
        return {action:selection.kind,blocking:true,resumed:false};
      }
      if(selection.kind==='NONE'){
        const state=o.m11.create(o.config11,{storage:o.storage,cryptoObj:o.cryptoObj,now:o.now,binding:o.binding});
        return {action:'FRESH_SESSION_CREATED',state,resumed:false,owner_epoch:owner.epoch};
      }
      return migrateSelected(o,owner,selection.selected,recovery.journal||null);
    }finally{releaseOwner(o,owner)}
  });
}

const api={VERSION,LOCK_NAME,JOURNAL_KEY,EPOCH_KEY,OWNER_KEY,FENCE_KEY,QUARANTINE_KEY,ARCHIVE_PREFIX,SOURCE_088,SOURCE_089,SOURCE_0810,PHASES,parse,fingerprint,bankIndex,legacyRoute,stateShapeValid,sealed,randomOwner,currentEpoch,acquireOwner,assertOwner,releaseOwner,fencedSet,fencedRemove,readJournal,writeJournal,writeFence,quarantine,migrationId,archiveKey,simulatedCrash,maybeCrash,normalize088,normalizeOpaque,material,commonResponseEqual,compatibleAncestor,validateSource,inspectSources,selectSource,targetInfo,targetMatchesJournal,rollbackPreAuthority,divergenceHold,reconcileCommitted,reconcile,migrateSelected,loadOrInitializeAtomic};
if(typeof module!=='undefined'&&module.exports)module.exports=api;
global.CUBE_REV_ATOMIC_MIGRATION_0811=api;
})(typeof window!=='undefined'?window:globalThis);
