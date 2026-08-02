'use strict';

const assert=require('assert');
const Builder=require('../scripts/build_0_8_10_assets.js');
const Verify=require('../js/public-asset-verifier-0.8.10.js');
const M088=require('../js/participant-cognitive-mode-0.8.8.js');
const M089=require('../js/participant-cognitive-mode-0.8.9.js');
const M10=require('../js/participant-cognitive-mode-0.8.10.js');
const Mig=require('../js/cross-version-migration-0.8.10.js');
const bank088=require('../cognitive/PARTICIPANT_STIMULUS_BANK_0.8.8.json');
const config088=require('../cognitive/COGNITIVE_MODE_CONFIG_0.8.8.json');
const bank089=require('../cognitive/PARTICIPANT_STIMULUS_BANK_0.8.9.json');
const config089=require('../cognitive/COGNITIVE_MODE_CONFIG_0.8.9.json');
const manifest089=require('../research/CUBE_REV_0.8.9_BUILD_MANIFEST.json');

class Storage{
  constructor(){this.x={}}
  getItem(k){return Object.prototype.hasOwnProperty.call(this.x,k)?this.x[k]:null}
  setItem(k,v){this.x[k]=String(v)}
  removeItem(k){delete this.x[k]}
}
const cryptoObj={getRandomValues(a){for(let i=0;i<a.length;i++)a[i]=0x100+i;return a}};
function clock(prefix='2026-08-02T09:00:'){
  let n=0;return()=>`${prefix}${String(n++).padStart(2,'0')}.000Z`;
}
function index(bank){return Object.fromEntries(bank.stimuli.map(x=>[x.stimulus_id,x]))}
function dep(storage,out,now,extra={}){
  return {storage,bank10:out.publicBank,config10:out.publicConfig,config088,config089,binding:extra.binding,m088:M088,m089:M089,m10:M10,now,...extra};
}
function create088(storage,out,count,{ready=false,sealed=false}={}){
  const now=clock('2026-08-02T10:00:');
  let s=M088.loadOrCreate(config088,{storage,cryptoObj,now}).state;
  const by=index(out.publicBank);
  const n=ready?28:count;
  for(let i=0;i<n;i++){
    const id=s.schedule[s.cursor],display='U';
    s=M088.record(storage,s,{stimulus_id:id,state_id:999,rotation_id:7,choice_display:display,choice_canonical:'D',latency_ms:40+i},now);
    assert.ok(by[id].choice_codes[display]);
  }
  if(ready){
    s=M088.savePostTask(storage,s,{hypothesis_guess:'x',confidence:71,deliberate_strategy_change:false,technical_notes:'legacy'},now);
    if(sealed)s=M088.prepareSubmissionSnapshot(storage,s,now);
  }
  return {state:s,now};
}
function create089(storage,out,count,{ready=false,sealed=false}={}){
  const now=clock('2026-08-02T11:00:');
  let s=M089.loadOrCreate(config089,{storage,cryptoObj,now}).state;
  const by=index(out.publicBank),n=ready?28:count;
  for(let i=0;i<n;i++){
    const id=s.schedule[s.cursor],display='R2';
    s=M089.record(storage,s,{stimulus_id:id,choice_display:display,choice_code:by[id].choice_codes[display],latency_ms:60+i},now);
  }
  if(ready){
    s=M089.savePostTask(storage,s,{hypothesis_guess:'y',confidence:52,deliberate_strategy_change:true,technical_notes:'opaque'},now);
    if(sealed)s=M089.prepareSubmissionSnapshot(storage,s,now);
  }
  return {state:s,now};
}

(async()=>{
  let passed=0;
  const out=Builder.build(bank089,config089,manifest089);
  const bundle=await Verify.verifyBundle({
    manifestText:JSON.stringify(out.manifest),bankText:JSON.stringify(out.publicBank),configText:JSON.stringify(out.publicConfig),pins:out.pins
  });
  assert.equal(bundle.manifest.choice_code_count,504);assert.equal(bundle.bank.stimuli.length,28);passed++;

  const badBank=JSON.parse(JSON.stringify(out.publicBank));badBank.stimuli[0].stickers.U[0][0]='R';
  await assert.rejects(()=>Verify.verifyBundle({manifestText:JSON.stringify(out.manifest),bankText:JSON.stringify(badBank),configText:JSON.stringify(out.publicConfig),pins:out.pins}),/PUBLIC_BANK_PIN_MISMATCH/);passed++;

  {
    const storage=new Storage(),now=clock('2026-08-02T12:00:');
    const a=M10.loadOrCreate(out.publicConfig,{storage,cryptoObj,now,binding:bundle.binding});
    const token=a.state.participant_token,sid=a.state.sequence_id,schedule=a.state.schedule.join('|');
    const b=M10.loadOrCreate(out.publicConfig,{storage,cryptoObj,now,binding:bundle.binding});
    assert.equal(b.resumed,true);assert.equal(b.state.participant_token,token);assert.equal(b.state.sequence_id,sid);assert.equal(b.state.schedule.join('|'),schedule);passed++;
  }

  {
    const storage=new Storage();const legacy=create088(storage,out,5).state;const raw=storage.getItem(Mig.SOURCE_088);const now=clock('2026-08-02T13:00:');
    const r=Mig.loadOrMigrate(dep(storage,out,now,{binding:bundle.binding}));
    assert.equal(r.action,'MIGRATED');assert.equal(r.state.cursor,5);assert.equal(r.state.participant_token,legacy.participant_token);assert.equal(r.state.sequence_id,legacy.sequence_id);assert.equal(r.state.schedule.join('|'),legacy.schedule.join('|'));
    assert.ok(r.state.responses.every(x=>x.choice_code&&x.choice_canonical===undefined&&x.state_id===undefined));assert.equal(storage.getItem(Mig.SOURCE_088),raw);assert.equal(storage.getItem(r.archive_key),raw);
    const again=Mig.loadOrMigrate(dep(storage,out,now,{binding:bundle.binding}));assert.equal(again.action,'TARGET_RESUMED');passed++;
  }

  {
    const storage=new Storage();const legacy=create088(storage,out,0,{ready:true,sealed:false}).state;const now=clock('2026-08-02T14:00:');
    const r=Mig.loadOrMigrate(dep(storage,out,now,{binding:bundle.binding}));
    assert.equal(r.action,'MIGRATED');assert.equal(r.state.status,'READY_TO_SUBMIT');assert.deepEqual(r.state.post_task,legacy.post_task);assert.equal(r.state.cursor,28);
    const sealed=M10.prepareSubmissionSnapshot(storage,r.state,now);assert.equal(sealed.submission_snapshot.asset_binding.manifest_sha256,bundle.binding.manifest_sha256);assert.ok(M10.snapshotValid(sealed));passed++;
  }

  {
    const storage=new Storage();const legacy=create089(storage,out,4).state;const raw=storage.getItem(Mig.SOURCE_089);const now=clock('2026-08-02T15:00:');
    const r=Mig.loadOrMigrate(dep(storage,out,now,{binding:bundle.binding}));
    assert.equal(r.action,'MIGRATED');assert.equal(r.source_version,'CUBE-REV 0.8.9');assert.deepEqual(r.state.responses,legacy.responses);assert.equal(storage.getItem(Mig.SOURCE_089),raw);passed++;
  }

  {
    const storage=new Storage();const legacy=create088(storage,out,0,{ready:true,sealed:true}).state;const raw=storage.getItem(Mig.SOURCE_088);const now=clock('2026-08-02T16:00:');
    const r=Mig.loadOrMigrate(dep(storage,out,now,{binding:bundle.binding}));
    assert.equal(r.action,'LEGACY_SEALED_RETRY');assert.equal(r.legacy_route,'participant-cognitive-mode-0.8.8.html');assert.equal(storage.getItem(Mig.SOURCE_088),raw);assert.equal(storage.getItem(M10.STORAGE_KEY),null);assert.ok(legacy.submission_snapshot);passed++;
  }

  {
    const storage=new Storage();create089(storage,out,0,{ready:true,sealed:true});const raw=storage.getItem(Mig.SOURCE_089);const now=clock('2026-08-02T17:00:');
    const r=Mig.loadOrMigrate(dep(storage,out,now,{binding:bundle.binding}));
    assert.equal(r.action,'LEGACY_SEALED_RETRY');assert.equal(r.legacy_route,'participant-cognitive-mode-0.8.9.html');assert.equal(storage.getItem(Mig.SOURCE_089),raw);assert.equal(storage.getItem(M10.STORAGE_KEY),null);passed++;
  }

  {
    const storage=new Storage();create088(storage,out,3);const raw=storage.getItem(Mig.SOURCE_088);const now=clock('2026-08-02T18:00:');
    assert.throws(()=>Mig.loadOrMigrate(dep(storage,out,now,{binding:bundle.binding,injectFailure:'AFTER_TARGET_WRITE'})),/INJECTED_AFTER_TARGET_WRITE/);
    assert.equal(storage.getItem(M10.STORAGE_KEY),null);assert.equal(storage.getItem(Mig.SOURCE_088),raw);assert.equal(JSON.parse(storage.getItem(Mig.JOURNAL_KEY)).state,'ROLLED_BACK');passed++;
  }

  {
    const storage=new Storage();create088(storage,out,2);const x=JSON.parse(storage.getItem(Mig.SOURCE_088));x.sequence_id=x.sequence_id==='1'?'2':'1';storage.setItem(Mig.SOURCE_088,JSON.stringify(x));const now=clock('2026-08-02T19:00:');
    const r=Mig.loadOrMigrate(dep(storage,out,now,{binding:bundle.binding}));assert.equal(r.action,'SOURCE_INVALID');assert.ok(storage.getItem(Mig.MIGRATION_QUARANTINE_KEY));assert.equal(storage.getItem(M10.STORAGE_KEY),null);passed++;
  }

  {
    const storage=new Storage();create088(storage,out,1);create089(storage,out,1);const now=clock('2026-08-02T20:00:');
    const r=Mig.loadOrMigrate(dep(storage,out,now,{binding:bundle.binding}));assert.equal(r.action,'SOURCE_CONFLICT');assert.ok(storage.getItem(Mig.MIGRATION_QUARANTINE_KEY));assert.equal(storage.getItem(M10.STORAGE_KEY),null);passed++;
  }

  {
    const storage=new Storage();const now=clock('2026-08-02T21:00:');let s=M10.loadOrCreate(out.publicConfig,{storage,cryptoObj,now,binding:bundle.binding}).state;
    const forged={...bundle.binding,public_bank_sha256:'0'.repeat(64)};assert.equal(M10.valid(s,out.publicConfig,forged),false);
    const raw=JSON.parse(storage.getItem(M10.STORAGE_KEY));raw.asset_binding.public_bank_sha256='0'.repeat(64);raw.integrity=M10.checksum({...raw,integrity:undefined});storage.setItem(M10.STORAGE_KEY,JSON.stringify(raw));
    const recovered=M10.loadExisting(out.publicConfig,{storage,now,binding:bundle.binding});assert.equal(recovered.state,null);assert.equal(recovered.invalid,true);assert.ok(storage.getItem(M10.QUARANTINE_KEY));passed++;
  }

  assert.equal(passed,12);
  console.log(`CR0810_MIGRATION_HASH_PIN_PASS ${passed}/12`);
})().catch(e=>{console.error(e);process.exit(1)});
