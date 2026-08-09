'use strict';

const assert=require('assert');
const Builder=require('../scripts/build_0_8_11_assets.js');
const Verify=require('../js/public-asset-verifier-0.8.11.js');
const M088=require('../js/participant-cognitive-mode-0.8.8.js');
const M089=require('../js/participant-cognitive-mode-0.8.9.js');
const M10=require('../js/participant-cognitive-mode-0.8.10.js');
const M11=require('../js/participant-cognitive-mode-0.8.11.js');
const Atomic=require('../js/atomic-migration-0.8.11.js');
const bank10=require('../cognitive/PARTICIPANT_STIMULUS_BANK_0.8.10.json');
const config088=require('../cognitive/COGNITIVE_MODE_CONFIG_0.8.8.json');
const config089=require('../cognitive/COGNITIVE_MODE_CONFIG_0.8.9.json');
const config10=require('../cognitive/COGNITIVE_MODE_CONFIG_0.8.10.json');
const manifest10=require('../research/CUBE_REV_0.8.10_ASSET_MANIFEST.json');

class Storage{
  constructor(){this.x={}}
  getItem(k){return Object.prototype.hasOwnProperty.call(this.x,k)?this.x[k]:null}
  setItem(k,v){this.x[k]=String(v)}
  removeItem(k){delete this.x[k]}
  snapshot(){return JSON.stringify(this.x)}
}
class SerialLockManager{
  constructor(){this.tail=Promise.resolve();this.active=0;this.maxActive=0;this.entries=0}
  request(name,options,callback){
    const run=this.tail.then(async()=>{this.active++;this.entries++;this.maxActive=Math.max(this.maxActive,this.active);try{return await callback({name,mode:options.mode})}finally{this.active--}});
    this.tail=run.catch(()=>{});return run;
  }
}
const cryptoObj={getRandomValues(a){for(let i=0;i<a.length;i++)a[i]=0x200+i;return a}};
function clock(){let n=0,t=Date.UTC(2026,7,2,9,0,0);return()=>new Date(t+n++).toISOString()}
function ownerFactory(){let n=0;return()=>`OWNER-${++n}`}
function byId(bank){return Object.fromEntries(bank.stimuli.map(x=>[x.stimulus_id,x]))}
function dependencies(storage,out,bundle,lockManager,extra={}){
  return {storage,lockManager,bank11:out.publicBank,config11:out.publicConfig,config088,config089,config10,parent0810Binding:out.parentBinding,binding:bundle.binding,m088:M088,m089:M089,m10:M10,m11:M11,cryptoObj,now:extra.now||clock(),ownerIdFactory:extra.ownerIdFactory||ownerFactory(),...extra};
}
function create088(storage,out,count,{ready=false,sealed=false}={}){
  const now=clock();let s=M088.loadOrCreate(config088,{storage,cryptoObj,now}).state;const bank=byId(out.publicBank),n=ready?28:count;
  for(let i=0;i<n;i++){const id=s.schedule[s.cursor],d='U';s=M088.record(storage,s,{stimulus_id:id,state_id:7,rotation_id:3,choice_display:d,choice_canonical:'D',latency_ms:30+i},now);assert.ok(bank[id].choice_codes[d])}
  if(ready){s=M088.savePostTask(storage,s,{hypothesis_guess:'legacy',confidence:60,deliberate_strategy_change:false,technical_notes:''},now);if(sealed)s=M088.prepareSubmissionSnapshot(storage,s,now)}
  return s;
}
function create089(storage,out,count,{ready=false,sealed=false}={}){
  const now=clock();let s=M089.loadOrCreate(config089,{storage,cryptoObj,now}).state;const bank=byId(out.publicBank),n=ready?28:count;
  for(let i=0;i<n;i++){const id=s.schedule[s.cursor],d='R2';s=M089.record(storage,s,{stimulus_id:id,choice_display:d,choice_code:bank[id].choice_codes[d],latency_ms:50+i},now)}
  if(ready){s=M089.savePostTask(storage,s,{hypothesis_guess:'opaque',confidence:75,deliberate_strategy_change:true,technical_notes:''},now);if(sealed)s=M089.prepareSubmissionSnapshot(storage,s,now)}
  return s;
}
function create0810(storage,out,count,{ready=false,sealed=false}={}){
  const now=clock();let s=M10.loadOrCreate(config10,{storage,cryptoObj,now,binding:out.parentBinding}).state;const bank=byId(out.publicBank),n=ready?28:count;
  for(let i=0;i<n;i++){const id=s.schedule[s.cursor],d="F'";s=M10.record(storage,s,{stimulus_id:id,choice_display:d,choice_code:bank[id].choice_codes[d],latency_ms:70+i},now)}
  if(ready){s=M10.savePostTask(storage,s,{hypothesis_guess:'parent',confidence:80,deliberate_strategy_change:false,technical_notes:''},now);if(sealed)s=M10.prepareSubmissionSnapshot(storage,s,now)}
  return s;
}
function create0810DescendantOf088(storage,out,count){
  const source=create088(storage,out,count),raw=storage.getItem(Atomic.SOURCE_088),bank=byId(out.publicBank),now=clock();
  const responses=source.responses.map(r=>({stimulus_id:r.stimulus_id,choice_display:r.choice_display,choice_code:bank[r.stimulus_id].choice_codes[r.choice_display],latency_ms:r.latency_ms,position:r.position,recorded_at:r.recorded_at}));
  const material={source_version:source.version,source_schema:source.schema_version,source_storage_key:Atomic.SOURCE_088,source_integrity:source.integrity,source_revision:source.revision||0,session_id:source.session_id,mode_id:source.mode_id,participant_token:source.participant_token,sequence_id:source.sequence_id,schedule:[...source.schedule],cursor:source.cursor,responses,telemetry:[...source.telemetry],post_task:source.post_task,status:source.status,created_at:source.created_at};
  const target=M10.fromMigration(config10,{binding:out.parentBinding,now},material);assert.ok(M10.valid(target,config10,out.parentBinding));storage.setItem(M10.STORAGE_KEY,JSON.stringify(target));return {source,target,raw};
}
function mutateLegacy(storage,key,module,fn){const x=JSON.parse(storage.getItem(key));fn(x);x.integrity=module.checksum({...x,integrity:undefined});storage.setItem(key,JSON.stringify(x));return x}

(async()=>{
  let passed=0;
  const out=Builder.build(bank10,config10,manifest10);
  const bundle=await Verify.verifyBundle({manifestText:JSON.stringify(out.manifest),bankText:JSON.stringify(out.publicBank),configText:JSON.stringify(out.publicConfig),pins:out.pins});
  assert.equal(bundle.manifest.choice_code_count,504);assert.equal(bundle.config.resume.web_locks_required,true);passed++;

  {const bad=JSON.parse(JSON.stringify(out.publicConfig));bad.resume.web_locks_required=false;await assert.rejects(()=>Verify.verifyBundle({manifestText:JSON.stringify(out.manifest),bankText:JSON.stringify(out.publicBank),configText:JSON.stringify(bad),pins:out.pins}),/PUBLIC_CONFIG_PIN_MISMATCH/);passed++}

  {const storage=new Storage(),before=storage.snapshot();const r=await Atomic.loadOrInitializeAtomic(dependencies(storage,out,bundle,null));assert.equal(r.action,'LOCK_UNAVAILABLE');assert.equal(storage.snapshot(),before);passed++}

  {const storage=new Storage(),locks=new SerialLockManager(),o=dependencies(storage,out,bundle,locks);const r=await Atomic.loadOrInitializeAtomic(o);assert.equal(r.action,'FRESH_SESSION_CREATED');assert.ok(M11.valid(r.state,out.publicConfig,bundle.binding));assert.equal(locks.maxActive,1);passed++}

  {const storage=new Storage(),locks=new SerialLockManager(),now=clock(),owners=ownerFactory();const o=dependencies(storage,out,bundle,locks,{now,ownerIdFactory:owners});const [a,b]=await Promise.all([Atomic.loadOrInitializeAtomic(o),Atomic.loadOrInitializeAtomic(o)]);assert.deepEqual(new Set([a.action,b.action]),new Set(['FRESH_SESSION_CREATED','TARGET_RESUMED']));assert.equal(a.state.session_id,b.state.session_id);assert.equal(locks.maxActive,1);passed++}

  {const storage=new Storage(),locks=new SerialLockManager(),legacy=create088(storage,out,5),raw=storage.getItem(Atomic.SOURCE_088);const r=await Atomic.loadOrInitializeAtomic(dependencies(storage,out,bundle,locks));assert.equal(r.action,'MIGRATED');assert.equal(r.state.cursor,5);assert.equal(r.state.session_id,legacy.session_id);assert.equal(storage.getItem(Atomic.SOURCE_088),raw);assert.equal(JSON.parse(storage.getItem(Atomic.JOURNAL_KEY)).phase,'COMMITTED');passed++}

  {const storage=new Storage(),locks=new SerialLockManager(),legacy=create089(storage,out,4);const r=await Atomic.loadOrInitializeAtomic(dependencies(storage,out,bundle,locks));assert.equal(r.action,'MIGRATED');assert.equal(r.state.session_id,legacy.session_id);assert.deepEqual(r.state.responses,legacy.responses);passed++}

  {const storage=new Storage(),locks=new SerialLockManager(),legacy=create0810(storage,out,3);const r=await Atomic.loadOrInitializeAtomic(dependencies(storage,out,bundle,locks));assert.equal(r.action,'MIGRATED');assert.equal(r.source_version,'CUBE-REV 0.8.10');assert.equal(r.state.session_id,legacy.session_id);passed++}

  {const storage=new Storage(),locks=new SerialLockManager(),chain=create0810DescendantOf088(storage,out,3);const r=await Atomic.loadOrInitializeAtomic(dependencies(storage,out,bundle,locks));assert.equal(r.action,'MIGRATED');assert.equal(r.source_version,'CUBE-REV 0.8.10');assert.equal(r.state.session_id,chain.target.session_id);passed++}

  {const storage=new Storage(),locks=new SerialLockManager();create088(storage,out,2);create0810(storage,out,2);const r=await Atomic.loadOrInitializeAtomic(dependencies(storage,out,bundle,locks));assert.equal(r.action,'ANCESTRY_CONFLICT');assert.equal(storage.getItem(M11.STORAGE_KEY),null);passed++}

  {const storage=new Storage(),locks=new SerialLockManager();create0810(storage,out,0,{ready:true,sealed:true});const raw=storage.getItem(Atomic.SOURCE_0810);const r=await Atomic.loadOrInitializeAtomic(dependencies(storage,out,bundle,locks));assert.equal(r.action,'LEGACY_SEALED_RETRY');assert.equal(r.legacy_route,'participant-cognitive-mode-0.8.10.html');assert.equal(storage.getItem(Atomic.SOURCE_0810),raw);passed++}

  {const storage=new Storage(),o=dependencies(storage,out,bundle,new SerialLockManager()),owner1=Atomic.acquireOwner(o);Atomic.releaseOwner(o,owner1);const owner2=Atomic.acquireOwner(o);assert.throws(()=>Atomic.writeJournal(o,owner1,{transaction_id:'x'},'PREPARED'),/STALE_MIGRATION_OWNER/);Atomic.releaseOwner(o,owner2);passed++}

  async function crashRecovery(phase,expected){const storage=new Storage(),locks=new SerialLockManager();create088(storage,out,3);const o1=dependencies(storage,out,bundle,locks,{injectCrash:phase});await assert.rejects(()=>Atomic.loadOrInitializeAtomic(o1),new RegExp(`SIMULATED_CRASH:${phase}`));const o2=dependencies(storage,out,bundle,locks);const r=await Atomic.loadOrInitializeAtomic(o2);assert.equal(r.action,expected);assert.ok(M11.valid(r.state,out.publicConfig,bundle.binding));assert.equal(JSON.parse(storage.getItem(Atomic.JOURNAL_KEY)).phase,'COMMITTED');return {storage,locks,r}}
  await crashRecovery('PREPARED','MIGRATED');passed++;
  await crashRecovery('TARGET_WRITTEN','RECOVERED_COMMIT');passed++;
  await crashRecovery('ARCHIVE_WRITTEN','RECOVERED_COMMIT');passed++;
  await crashRecovery('FENCE_WRITTEN','RECOVERED_COMMIT');passed++;
  {const z=await crashRecovery('COMMITTED','TARGET_RESUMED');const again=await Atomic.loadOrInitializeAtomic(dependencies(z.storage,out,bundle,z.locks));assert.equal(again.action,'TARGET_RESUMED');assert.equal(again.state.session_id,z.r.state.session_id);passed++}

  {const storage=new Storage(),locks=new SerialLockManager();create088(storage,out,3);await assert.rejects(()=>Atomic.loadOrInitializeAtomic(dependencies(storage,out,bundle,locks,{injectCrash:'TARGET_WRITTEN'})),/SIMULATED_CRASH/);const bad=JSON.parse(storage.getItem(M11.STORAGE_KEY));bad.responses[0].choice_code='CR9C-0000000000000000';bad.integrity=M11.checksum({...bad,integrity:undefined});storage.setItem(M11.STORAGE_KEY,JSON.stringify(bad));const r=await Atomic.loadOrInitializeAtomic(dependencies(storage,out,bundle,locks));assert.equal(r.action,'MIGRATED');assert.equal(JSON.parse(storage.getItem(Atomic.JOURNAL_KEY)).previous_terminal_phase,'ROLLED_BACK');passed++}

  {const storage=new Storage(),locks=new SerialLockManager();create088(storage,out,2);await Atomic.loadOrInitializeAtomic(dependencies(storage,out,bundle,locks));storage.removeItem(M11.STORAGE_KEY);const r=await Atomic.loadOrInitializeAtomic(dependencies(storage,out,bundle,locks));assert.equal(r.action,'ROLLED_BACK_TO_LEGACY');assert.equal(r.legacy_route,'participant-cognitive-mode-0.8.8.html');assert.equal(JSON.parse(storage.getItem(Atomic.JOURNAL_KEY)).phase,'ROLLED_BACK_TO_LEGACY');passed++}

  {const storage=new Storage(),locks=new SerialLockManager();create088(storage,out,2);const first=await Atomic.loadOrInitializeAtomic(dependencies(storage,out,bundle,locks));mutateLegacy(storage,Atomic.SOURCE_088,M088,x=>{x.telemetry.push({type:'STALE_DOWNGRADE_WRITE',at:clock()(),data:{}})});const r=await Atomic.loadOrInitializeAtomic(dependencies(storage,out,bundle,locks));assert.equal(r.action,'DOWNGRADE_MUTATION_QUARANTINED');assert.equal(r.state.session_id,first.state.session_id);assert.ok(storage.getItem(Atomic.QUARANTINE_KEY));passed++}

  {const storage=new Storage(),locks=new SerialLockManager();create088(storage,out,2);await Atomic.loadOrInitializeAtomic(dependencies(storage,out,bundle,locks));mutateLegacy(storage,Atomic.SOURCE_088,M088,x=>{x.telemetry.push({type:'STALE_DOWNGRADE_WRITE',at:clock()(),data:{}})});storage.removeItem(M11.STORAGE_KEY);const r=await Atomic.loadOrInitializeAtomic(dependencies(storage,out,bundle,locks));assert.equal(r.action,'TARGET_LOSS_WITH_SOURCE_DIVERGENCE');assert.equal(r.blocking,true);passed++}

  {const storage=new Storage(),locks=new SerialLockManager();create088(storage,out,2);await assert.rejects(()=>Atomic.loadOrInitializeAtomic(dependencies(storage,out,bundle,locks,{injectCrash:'TARGET_WRITTEN'})),/SIMULATED_CRASH/);mutateLegacy(storage,Atomic.SOURCE_088,M088,x=>{x.telemetry.push({type:'CONCURRENT_LEGACY_PROGRESS',at:clock()(),data:{}})});const r=await Atomic.loadOrInitializeAtomic(dependencies(storage,out,bundle,locks));assert.equal(r.action,'PRE_FENCE_SOURCE_DIVERGENCE');assert.equal(storage.getItem(M11.STORAGE_KEY),null);passed++}

  {const storage=new Storage(),locks=new SerialLockManager(),now=clock(),owners=ownerFactory();create088(storage,out,4);const o=dependencies(storage,out,bundle,locks,{now,ownerIdFactory:owners});const [a,b]=await Promise.all([Atomic.loadOrInitializeAtomic(o),Atomic.loadOrInitializeAtomic(o)]);assert.deepEqual(new Set([a.action,b.action]),new Set(['MIGRATED','TARGET_RESUMED']));assert.equal(a.state.session_id,b.state.session_id);assert.equal(JSON.parse(storage.getItem(Atomic.JOURNAL_KEY)).transaction_epoch,a.state.upgrade_epoch);assert.equal(locks.maxActive,1);passed++}

  assert.equal(passed,23);
  console.log(`CR0811_ATOMIC_MIGRATION_PASS ${passed}/23`);
})().catch(e=>{console.error(e);process.exit(1)});
