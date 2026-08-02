(function(global){
'use strict';

const base=typeof module!=='undefined'&&module.exports?require('./atomic-migration-0.8.11.js'):global.CUBE_REV_ATOMIC_MIGRATION_0811;
if(!base)throw new Error('ATOMIC_MIGRATION_BASE_REQUIRED');
const original=base.loadOrInitializeAtomic;

function targetIdentityMatches(info,journal){
  if(!info||!info.valid||!journal)return false;
  const state=info.state,provenance=state.migration_provenance;
  return state.upgrade_epoch===journal.transaction_epoch&&
    !!provenance&&provenance.source_storage_key===journal.source_storage_key&&
    provenance.source_integrity===journal.source_integrity&&
    state.session_id===journal.source_session_id;
}
function resume(o,owner,state,type,data){base.assertOwner(o.storage,owner);return o.m11.event(o.storage,state,type,data,o.now)}
function committedUnderLock(o,owner,j){
  const target=base.targetInfo(o),sourceRaw=o.storage.getItem(j.source_storage_key),archiveRaw=o.storage.getItem(j.archive_key);
  const sourceMatches=sourceRaw===j.source_raw,archiveMatches=archiveRaw===j.source_raw;
  if(targetIdentityMatches(target,j)){
    if(!archiveMatches){
      base.quarantine(o,owner,'COMMITTED_ARCHIVE_INTEGRITY_HOLD',{journal:j,archive_raw:archiveRaw,target_raw:target.raw});
      return {action:'COMMITTED_ARCHIVE_INTEGRITY_HOLD',blocking:true,resumed:false};
    }
    if(!sourceMatches){
      base.quarantine(o,owner,'DOWNGRADE_SOURCE_MUTATION',{journal:j,mutated_source_raw:sourceRaw,current_target_integrity:target.state.integrity,initial_target_integrity:j.target_integrity});
      const state=resume(o,owner,target.state,'DOWNGRADE_SOURCE_MUTATION_QUARANTINED',{migration_epoch:j.transaction_epoch,source_storage_key:j.source_storage_key});
      return {action:'DOWNGRADE_MUTATION_QUARANTINED',state,resumed:true};
    }
    const state=resume(o,owner,target.state,'ATOMIC_TARGET_RESUMED',{migration_epoch:j.transaction_epoch,current_integrity:target.state.integrity});
    return {action:'TARGET_RESUMED',state,resumed:true};
  }
  if(sourceMatches&&archiveMatches){
    if(target.present)base.fencedRemove(o.storage,owner,o.m11.STORAGE_KEY);
    const next=base.writeJournal(o,owner,j,'ROLLED_BACK_TO_LEGACY',{rolled_back_at:o.now(),rollback_reason:'COMMITTED_TARGET_LOST_OR_IDENTITY_MISMATCH',source_preserved:true});
    base.writeFence(o,owner,next,'ROLLED_BACK_TO_LEGACY');
    return {action:'ROLLED_BACK_TO_LEGACY',legacy_route:base.legacyRoute(j.source_version),source_version:j.source_version,resumed:false};
  }
  base.quarantine(o,owner,'TARGET_LOSS_WITH_SOURCE_DIVERGENCE',{journal:j,current_source_raw:sourceRaw,archive_raw:archiveRaw,target_raw:target.raw});
  return {action:'TARGET_LOSS_WITH_SOURCE_DIVERGENCE',blocking:true,resumed:false};
}
async function loadOrInitializeAtomic(o){
  if(!o||!o.lockManager||typeof o.lockManager.request!=='function')return original(o);
  const observed=base.readJournal(o.storage);
  if(!observed||observed.phase!=='COMMITTED')return original(o);
  const result=await o.lockManager.request(base.LOCK_NAME,{mode:'exclusive'},async()=>{
    const owner=base.acquireOwner(o);
    try{
      const current=base.readJournal(o.storage);
      if(!current||current.phase!=='COMMITTED')return {delegate:true};
      return committedUnderLock(o,owner,current);
    }finally{base.releaseOwner(o,owner)}
  });
  return result&&result.delegate?original(o):result;
}

base.targetIdentityMatches=targetIdentityMatches;
base.committedUnderLock=committedUnderLock;
base.loadOrInitializeAtomic=loadOrInitializeAtomic;
if(typeof module!=='undefined'&&module.exports)module.exports=base;
global.CUBE_REV_ATOMIC_MIGRATION_0811=base;
})(typeof window!=='undefined'?window:globalThis);
