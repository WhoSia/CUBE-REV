'use strict';

const assert=require('assert');
const Builder=require('../scripts/build_0_8_12_assets.js');
const Verify=require('../js/public-asset-verifier-0.8.12.js');
const M11=require('../js/participant-cognitive-mode-0.8.11.js');
const M12=require('../js/participant-cognitive-mode-0.8.12.js');
const CAS=require('../js/active-session-cas-0.8.12.js');
const bank11=require('../cognitive/PARTICIPANT_STIMULUS_BANK_0.8.11.json');
const config11=require('../cognitive/COGNITIVE_MODE_CONFIG_0.8.11.json');
const manifest11=require('../research/CUBE_REV_0.8.11_ASSET_MANIFEST.json');

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
const cryptoObj={getRandomValues(a){for(let i=0;i<a.length;i++)a[i]=0x300+i;return a}};
function clock(start=Date.UTC(2026,7,2,10,0,0)){let n=0,t=start;const f=()=>new Date(t+n++).toISOString();f.advance=ms=>{t+=ms};return f}
function idFactory(){let n=0;return p=>`TEST-${String(p||'M').toUpperCase()}-${++n}`}
function byId(bank){return Object.fromEntries(bank.stimuli.map(x=>[x.stimulus_id,x]))}
function create11(storage,out,now,count=0){
  let s=M11.create(config11,{storage,cryptoObj,now,binding:out.parentBinding});
  const bank=byId(out.publicBank);
  for(let i=0;i<count;i++){
    const id=s.schedule[s.cursor],d='U';
    s=M11.record(storage,s,{stimulus_id:id,choice_display:d,choice_code:bank[id].choice_codes[d],latency_ms:40+i},now);
  }
  return s;
}
function options(storage,out,bundle,locks,now=clock()){
  return {
    storage,lockManager:locks,config:out.publicConfig,binding:bundle.binding,
    parentConfig:config11,parentBinding:out.parentBinding,m11:M11,m12:M12,
    atomic11:{async loadOrInitializeAtomic(){const raw=storage.getItem(M11.STORAGE_KEY);return raw?{action:'TARGET_RESUMED',state:JSON.parse(raw)}:{action:'PARENT_STATE_MISSING',blocking:true}}},
    atomic11Deps:{},cryptoObj,now,idFactory:idFactory()
  };
}
async function boot(storage,out,bundle,locks,now=clock(),count=0){
  if(!storage.getItem(M11.STORAGE_KEY))create11(storage,out,now,count);
  const o=options(storage,out,bundle,locks,now);
  const r=await CAS.loadOrInitializeActive(o);
  return {o,r};
}
function responseFor(state,bank,display='U',latency=100){
  const id=state.schedule[state.cursor];
  return {stimulus_id:id,choice_display:display,choice_code:bank[id].choice_codes[display],latency_ms:latency};
}
async function op(o,state,type,extra={},id='op'){
  return CAS.applyOperation(o,{type,mutation_id:o.idFactory(id),session_id:state.session_id,expected_revision:state.revision,...extra});
}

(async()=>{
  let passed=0;
  const out=Builder.build(bank11,config11,manifest11);
  const bundle=await Verify.verifyBundle({manifestText:JSON.stringify(out.manifest),bankText:JSON.stringify(out.publicBank),configText:JSON.stringify(out.publicConfig),pins:out.pins});
  const bank=byId(out.publicBank);

  assert.equal(bundle.manifest.choice_code_count,504);
  assert.equal(bundle.config.resume.active_write_lock_required,true);
  assert.equal(bundle.config.active_session.revision_policy,'STRICT_MONOTONIC_INCREMENT_BY_ONE_V1');passed++;

  {const bad=JSON.parse(JSON.stringify(out.publicConfig));bad.active_session.revision_policy='BEST_EFFORT';await assert.rejects(()=>Verify.verifyBundle({manifestText:JSON.stringify(out.manifest),bankText:JSON.stringify(out.publicBank),configText:JSON.stringify(bad),pins:out.pins}),/PUBLIC_CONFIG_PIN_MISMATCH/);passed++}

  {const storage=new Storage();create11(storage,out,clock(),0);const before=storage.snapshot(),o=options(storage,out,bundle,null);const r=await CAS.loadOrInitializeActive(o);assert.equal(r.action,'LOCK_UNAVAILABLE');assert.equal(storage.snapshot(),before);passed++}

  {const storage=new Storage(),locks=new SerialLockManager(),now=clock();create11(storage,out,now,3);const raw=storage.getItem(M11.STORAGE_KEY),{r}=await boot(storage,out,bundle,locks,now);assert.equal(r.action,'UPGRADED_FROM_0811');assert.equal(r.state.cursor,3);assert.equal(storage.getItem(M11.STORAGE_KEY),raw);assert.ok(M12.valid(r.state,out.publicConfig,bundle.binding));passed++}

  {const storage=new Storage(),locks=new SerialLockManager(),now=clock();create11(storage,out,now,2);const a=options(storage,out,bundle,locks,now),b=options(storage,out,bundle,locks,now);const [x,y]=await Promise.all([CAS.loadOrInitializeActive(a),CAS.loadOrInitializeActive(b)]);assert.deepEqual(new Set([x.action,y.action]),new Set(['UPGRADED_FROM_0811','TARGET_RESUMED']));assert.equal(x.state.session_id,y.state.session_id);assert.equal(locks.maxActive,1);passed++}

  const storage=new Storage(),locks=new SerialLockManager(),now=clock();
  const z=await boot(storage,out,bundle,locks,now,0);const o=z.o;let s=z.r.state;

  {const r=await op(o,s,'RESPONSE',{expected_position:s.cursor,response:responseFor(s,bank)},'response');assert.equal(r.action,'RESPONSE_APPLIED');assert.equal(r.state.cursor,1);assert.equal(r.state.revision,s.revision+1);s=r.state;passed++}

  {const mid=o.idFactory('idem'),payload={type:'TELEMETRY',mutation_id:mid,session_id:s.session_id,expected_revision:s.revision,event_id:'EV-IDEM',event_type:'TEST',data:{a:1}};const a=await CAS.applyOperation(o,payload),rev=a.state.revision,b=await CAS.applyOperation(o,payload);assert.equal(b.action,'IDEMPOTENT_REPLAY');assert.equal(b.state.revision,rev);s=b.state;passed++}

  {const base=s,ra=responseFor(base,bank,'R',111),rb=responseFor(base,bank,'F',222);const [a,b]=await Promise.all([
    CAS.applyOperation(o,{type:'RESPONSE',mutation_id:'CONCURRENT-A',session_id:base.session_id,expected_revision:base.revision,expected_position:base.cursor,response:ra}),
    CAS.applyOperation(o,{type:'RESPONSE',mutation_id:'CONCURRENT-B',session_id:base.session_id,expected_revision:base.revision,expected_position:base.cursor,response:rb})
  ]);assert.deepEqual(new Set([a.action,b.action]),new Set(['RESPONSE_APPLIED','RESPONSE_CONFLICT']));s=JSON.parse(storage.getItem(M12.STORAGE_KEY));assert.equal(s.cursor,2);assert.equal(JSON.parse(storage.getItem(CAS.CONFLICT_KEY)).length,1);passed++}

  {const stale=s.revision-1,r=await CAS.applyOperation(o,{type:'RESPONSE',mutation_id:'STALE-FUTURE',session_id:s.session_id,expected_revision:stale,expected_position:s.cursor,response:responseFor(s,bank,'L',130)});assert.equal(r.action,'STALE_REVISION');assert.equal(r.state.cursor,s.cursor);passed++}

  {const old=s.revision-1,r=await CAS.applyOperation(o,{type:'TELEMETRY',mutation_id:'TM-STALE',session_id:s.session_id,expected_revision:old,event_id:'EV-STALE',event_type:'VISIBILITY_HIDDEN',data:{}});assert.equal(r.action,'TELEMETRY_MERGED_ON_LATEST');assert.equal(r.state.cursor,s.cursor);assert.ok(r.state.telemetry.some(e=>e.event_id==='EV-STALE'));s=r.state;passed++}

  {const before=s.revision,r=await CAS.applyOperation(o,{type:'TELEMETRY',mutation_id:'TM-DUP-OTHER',session_id:s.session_id,expected_revision:s.revision,event_id:'EV-STALE',event_type:'VISIBILITY_HIDDEN',data:{}});assert.equal(r.action,'TELEMETRY_ALREADY_MERGED');assert.equal(r.state.revision,before);passed++}

  {const base=s;await Promise.all([
    CAS.applyOperation(o,{type:'TELEMETRY',mutation_id:'TM-A',session_id:s.session_id,expected_revision:base.revision,event_id:'EV-A',event_type:'A',data:{}}),
    CAS.applyOperation(o,{type:'TELEMETRY',mutation_id:'TM-B',session_id:s.session_id,expected_revision:base.revision,event_id:'EV-B',event_type:'B',data:{}})
  ]);s=JSON.parse(storage.getItem(M12.STORAGE_KEY));assert.ok(s.telemetry.some(e=>e.event_id==='EV-A'));assert.ok(s.telemetry.some(e=>e.event_id==='EV-B'));assert.equal(s.revision,base.revision+2);passed++}

  while(s.cursor<28){const r=await op(o,s,'RESPONSE',{expected_position:s.cursor,response:responseFor(s,bank,'U',100+s.cursor)},`fill-${s.cursor}`);assert.equal(r.action,'RESPONSE_APPLIED');s=r.state}
  assert.equal(s.status,'POST_TASK');passed++;

  {const r=await CAS.applyOperation(o,{type:'POST_TASK',mutation_id:'POST-STALE',session_id:s.session_id,expected_revision:s.revision-1,post_task:{hypothesis_guess:'x',confidence:50}});assert.equal(r.action,'STALE_REVISION');assert.equal(r.state.status,'POST_TASK');passed++}

  {const r=await op(o,s,'POST_TASK',{post_task:{hypothesis_guess:'구조 비교',confidence:77,deliberate_strategy_change:false,technical_notes:''}},'post');assert.equal(r.action,'POST_TASK_APPLIED');assert.equal(r.state.status,'READY_TO_SUBMIT');s=r.state;passed++}

  {const r=await op(o,s,'SEAL_SNAPSHOT',{},'seal');assert.equal(r.action,'SNAPSHOT_SEALED');assert.ok(M12.snapshotValid(r.state));assert.ok(r.state.submission_control.retry_id);s=r.state;passed++}

  {const hash=s.submission_snapshot_hash,r=await CAS.applyOperation(o,{type:'TELEMETRY',mutation_id:'AFTER-SEAL',session_id:s.session_id,expected_revision:s.revision-1,event_id:'EV-AFTER-SEAL',event_type:'PAGEHIDE',data:{}});assert.equal(r.action,'TELEMETRY_MERGED_ON_LATEST');assert.equal(r.state.submission_snapshot_hash,hash);assert.ok(M12.snapshotValid(r.state));s=r.state;passed++}

  {const r=await CAS.applyOperation(o,{type:'RESPONSE',mutation_id:'RESP-AFTER-SEAL',session_id:s.session_id,expected_revision:s.revision,expected_position:27,response:{...s.responses[27]}});assert.equal(r.action,'SNAPSHOT_ALREADY_SEALED');passed++}

  {const before=s.revision,r=await CAS.applyOperation(o,{type:'SEAL_SNAPSHOT',mutation_id:'SEAL-AGAIN',session_id:s.session_id,expected_revision:s.revision});assert.equal(r.action,'SNAPSHOT_ALREADY_SEALED');assert.equal(r.state.revision,before);passed++}

  {const base=s;const [a,b]=await Promise.all([
    CAS.applyOperation(o,{type:'CLAIM_SUBMISSION',mutation_id:'CLAIM-A',session_id:s.session_id,expected_revision:base.revision,lease_token:'LEASE-A',lease_owner:'TAB-A'}),
    CAS.applyOperation(o,{type:'CLAIM_SUBMISSION',mutation_id:'CLAIM-B',session_id:s.session_id,expected_revision:base.revision,lease_token:'LEASE-B',lease_owner:'TAB-B'})
  ]);assert.deepEqual(new Set([a.action,b.action]),new Set(['SUBMISSION_LEASE_CLAIMED','SUBMISSION_IN_FLIGHT']));s=JSON.parse(storage.getItem(M12.STORAGE_KEY));assert.equal(s.submission_control.lease_token,'LEASE-A');passed++}

  {const before=s.revision,r=await CAS.applyOperation(o,{type:'SUBMISSION_META',mutation_id:'META-WRONG',session_id:s.session_id,lease_token:'WRONG',collector_meta:{status:'uploading'}});assert.equal(r.action,'STALE_SUBMISSION_LEASE');assert.equal(r.state.revision,before);passed++}

  {const r=await CAS.applyOperation(o,{type:'SUBMISSION_META',mutation_id:'META-A',session_id:s.session_id,lease_token:'LEASE-A',collector_meta:{status:'uploading',attempt_count:1},collector_events:[{type:'attempt'}]});assert.equal(r.action,'SUBMISSION_META_MERGED');assert.equal(r.state.submission_control.collector_meta.status,'uploading');s=r.state;passed++}

  {const hash=s.submission_snapshot_hash,r=await CAS.applyOperation(o,{type:'RELEASE_SUBMISSION',mutation_id:'RELEASE-A',session_id:s.session_id,lease_token:'LEASE-A',error:'network'});assert.equal(r.action,'SUBMISSION_LEASE_RELEASED');assert.equal(r.state.submission_snapshot_hash,hash);assert.equal(r.state.submission_control.lease_token,null);s=r.state;passed++}

  {const r=await CAS.applyOperation(o,{type:'CLAIM_SUBMISSION',mutation_id:'CLAIM-C',session_id:s.session_id,expected_revision:s.revision,lease_token:'LEASE-C',lease_owner:'TAB-C'});assert.equal(r.action,'SUBMISSION_LEASE_CLAIMED');s=r.state;passed++}

  {const receipt={status:'stored',receipt_code:'R-1',checksum_verified:true},r=await CAS.applyOperation(o,{type:'CONFIRM_SUBMISSION',mutation_id:'CONFIRM-C',session_id:s.session_id,lease_token:'LEASE-C',receipt});assert.equal(r.action,'SUBMISSION_CONFIRMED');assert.equal(r.state.status,'SUBMITTED');assert.deepEqual(M12.exportSnapshot(r.state),r.state.submission_snapshot);s=r.state;passed++}

  {const before=s.revision,r=await CAS.applyOperation(o,{type:'CONFIRM_SUBMISSION',mutation_id:'CONFIRM-AGAIN',session_id:s.session_id,lease_token:'LEASE-C',receipt:{status:'duplicate'}});assert.equal(r.action,'ALREADY_SUBMITTED');assert.equal(r.state.revision,before);passed++}

  {const storage2=new Storage(),locks2=new SerialLockManager(),now2=clock();create11(storage2,out,now2,0);const q=await boot(storage2,out,bundle,locks2,now2);const bad=JSON.parse(storage2.getItem(M12.STORAGE_KEY));bad.cursor=9;storage2.setItem(M12.STORAGE_KEY,JSON.stringify(bad));const r=await CAS.loadOrInitializeActive(q.o);assert.equal(r.action,'INVALID_ACTIVE_STATE');assert.equal(storage2.getItem(M12.STORAGE_KEY),null);assert.ok(storage2.getItem(M12.QUARANTINE_KEY));passed++}

  {const storage3=new Storage(),locks3=new SerialLockManager(),now3=clock();create11(storage3,out,now3,0);const q=await boot(storage3,out,bundle,locks3,now3);let x=q.r.state;
    while(x.cursor<28){x=(await op(q.o,x,'RESPONSE',{expected_position:x.cursor,response:responseFor(x,bank)},`e-fill-${x.cursor}`)).state}
    x=(await op(q.o,x,'POST_TASK',{post_task:{}},'e-post')).state;x=(await op(q.o,x,'SEAL_SNAPSHOT',{},'e-seal')).state;
    x=(await CAS.applyOperation(q.o,{type:'CLAIM_SUBMISSION',mutation_id:'E-CLAIM-1',session_id:x.session_id,expected_revision:x.revision,lease_token:'E-LEASE-1',lease_owner:'TAB-1'})).state;
    now3.advance(121000);
    const r=await CAS.applyOperation(q.o,{type:'CLAIM_SUBMISSION',mutation_id:'E-CLAIM-2',session_id:x.session_id,expected_revision:x.revision,lease_token:'E-LEASE-2',lease_owner:'TAB-2'});
    assert.equal(r.action,'SUBMISSION_LEASE_CLAIMED');assert.equal(r.state.submission_control.lease_token,'E-LEASE-2');assert.equal(r.state.submission_control.lease_generation,2);passed++}

  assert.equal(passed,26);
  console.log(`CR0812_ACTIVE_SESSION_CAS_PASS ${passed}/26`);
})().catch(e=>{console.error(e);process.exit(1)});
