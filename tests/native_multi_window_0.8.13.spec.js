'use strict';
const {test,expect,chromium}=require('@playwright/test');
const {spawn}=require('child_process');
const fs=require('fs');
const path=require('path');
const zlib=require('zlib');
const crypto=require('crypto');

const PORT=8130;
const BASE=`http://127.0.0.1:${PORT}/participant-cognitive-mode-0.8.13.html?test_mode=1`;
let server;

async function waitServer(){
  const deadline=Date.now()+15000;
  while(Date.now()<deadline){try{const r=await fetch(`http://127.0.0.1:${PORT}/`);if(r.ok||r.status===404)return}catch(_){}await new Promise(r=>setTimeout(r,100))}
  throw new Error('STATIC_SERVER_TIMEOUT');
}
async function openPair(context){
  const [a,b]=await Promise.all([context.newPage(),context.newPage()]);
  await Promise.all([a.goto(BASE),b.goto(BASE)]);
  await Promise.all([a.click('#begin'),b.click('#begin')]);
  await Promise.all([a.waitForFunction(()=>!!window.CUBE_REV_0813_TEST_HOOKS),b.waitForFunction(()=>!!window.CUBE_REV_0813_TEST_HOOKS)]);
  await expect.poll(async()=>{
    const [x,y]=await Promise.all([a.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.getState()),b.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.getState())]);
    return `${x.session_id}|${x.cursor}|${y.session_id}|${y.cursor}`;
  }).toMatch(/^(.+)\|0\|\1\|0$/);
  return [a,b];
}
function opFrom(page,display,tag,latency=11){
  return page.evaluate(({display,tag,latency})=>{
    const h=CUBE_REV_0813_TEST_HOOKS,s=h.getState(),p=h.responseAt(display,latency);
    return {type:'RESPONSE',mutation_id:`CR0813-${tag}`,expected_revision:s.revision,expected_position:p.position,response:p.response};
  },{display,tag,latency});
}
function decodeCollectorPayload(fields){
  const text=fields.encoding==='gzip-base64'
    ?zlib.gunzipSync(Buffer.from(fields.payload||'','base64')).toString('utf8')
    :String(fields.payload||'');
  return {text,value:JSON.parse(text),sha256:crypto.createHash('sha256').update(text).digest('hex')};
}
function installCollectorEmulator(context,evidence){
  const receipts=new Map();
  return context.route(/https:\/\/script\.google\.com\/macros\/s\//,async route=>{
    const req=route.request(),url=new URL(req.url()),action=url.searchParams.get('action');
    if(req.method()==='GET'&&action==='health'){
      const cb=url.searchParams.get('callback')||'callback';
      return route.fulfill({status:200,contentType:'application/javascript',body:`${cb}(${JSON.stringify({ok:true,collector_id:'CUBE-REV-0712-MAIN',protocol_version:'receipt-v2',expected_version:'0.7.12',receipt_confirmation_available:true,deployment_id:'CR0813-LOCAL-DELAYED-EMULATOR'})});`});
    }
    if(req.method()==='POST'){
      const fields=Object.fromEntries(new URLSearchParams(req.postData()||''));
      const decoded=decodeCollectorPayload(fields),envelope=decoded.value,snapshot=envelope.cognitive_snapshot||{};
      const index=evidence.posts.length;
      const record={
        index,session_id:fields.session_id,nonce:fields.submission_nonce,checksum:fields.checksum_fnv1a32,
        received_at:new Date().toISOString(),payload_bytes:Buffer.byteLength(decoded.text),payload_sha256:decoded.sha256,
        envelope_session_id:envelope.session_id,scientific_session_id:snapshot.session_id,
        original_scientific_session_id:envelope.original_scientific_session_id,
        transport_session_policy:envelope.transport_session_policy,
        trial_count:Array.isArray(envelope.trials)?envelope.trials.length:null,
        response_count:Array.isArray(snapshot.responses)?snapshot.responses.length:null
      };
      evidence.posts.push(record);
      receipts.set(record.nonce,{...record,status:index===0?'stored':'duplicate',readyAt:Date.now()+(index===0?5000:250)});
      return route.fulfill({status:200,contentType:'text/html',body:'<!doctype html><title>accepted</title>'});
    }
    if(req.method()==='GET'&&action==='receipt'){
      const cb=url.searchParams.get('callback')||'callback',nonce=url.searchParams.get('submission_nonce'),rec=receipts.get(nonce);
      let payload;
      if(!rec||Date.now()<rec.readyAt)payload={ok:true,status:'pending',submission_nonce:nonce,session_id:url.searchParams.get('session_id')};
      else payload={ok:true,status:rec.status,submission_nonce:nonce,session_id:rec.session_id,checksum_fnv1a32:rec.checksum,receipt_code:`CR0813-LOCAL-${rec.index+1}`,file_name:`${rec.session_id}.json`,received_at:new Date().toISOString()};
      evidence.polls.push({nonce,status:payload.status,at:new Date().toISOString()});
      return route.fulfill({status:200,contentType:'application/javascript',body:`${cb}(${JSON.stringify(payload)});`});
    }
    return route.fulfill({status:404,body:'not found'});
  });
}

test.beforeAll(async()=>{
  server=spawn('python3',['-m','http.server',String(PORT),'--bind','127.0.0.1'],{cwd:path.resolve(__dirname,'..'),stdio:'ignore'});
  await waitServer();
});
test.afterAll(()=>{if(server&&!server.killed)server.kill('SIGTERM')});

test('native Chromium Web Locks serialize two pages without response loss',async()=>{
  const browser=await chromium.launch({headless:true});
  const context=await browser.newContext();
  const [a,b]=await openPair(context);
  const initial=await a.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.getState());
  expect(initial.version).toBe('CUBE-REV 0.8.13');
  expect(await a.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.valid())).toBe(true);
  expect(await b.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.valid())).toBe(true);

  const [opA,opB]=await Promise.all([opFrom(a,'U','NATIVE-A'),opFrom(b,'R','NATIVE-B')]);
  expect(opA.expected_revision).toBe(opB.expected_revision);
  const [rA,rB]=await Promise.all([a.evaluate(op=>CUBE_REV_0813_TEST_HOOKS.apply(op),opA),b.evaluate(op=>CUBE_REV_0813_TEST_HOOKS.apply(op),opB)]);
  expect([rA.action,rB.action].sort()).toEqual(['RESPONSE_APPLIED','RESPONSE_CONFLICT'].sort());
  const stored=await a.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.getStoredState());
  const conflicts=await a.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.getConflictJournal());
  expect(stored.cursor).toBe(1);expect(stored.responses).toHaveLength(1);expect(conflicts).toHaveLength(1);
  expect(conflicts[0].stored_response.choice_display).not.toBe(conflicts[0].attempted_response.choice_display);

  await expect.poll(async()=>{
    const [x,y]=await Promise.all([a.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.getState().revision),b.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.getState().revision)]);return `${x}:${y}`;
  }).toMatch(/^(\d+):\1$/);

  const responseOp=await opFrom(a,'F','RACE-RESPONSE',13);
  const telemetryOp=await b.evaluate(()=>{const h=CUBE_REV_0813_TEST_HOOKS,s=h.getState();return {type:'TELEMETRY',mutation_id:'CR0813-RACE-TELEMETRY',expected_revision:s.revision,event_id:'CR0813-RACE-EVENT',event_type:'VISIBILITY_HIDDEN',data:{source:'native-two-page-test'}}});
  let [rr,rt]=await Promise.all([a.evaluate(op=>CUBE_REV_0813_TEST_HOOKS.apply(op),responseOp),b.evaluate(op=>CUBE_REV_0813_TEST_HOOKS.apply(op),telemetryOp)]);
  if(rr.action==='STALE_REVISION'){
    responseOp.expected_revision=rr.state.revision;
    rr=await a.evaluate(op=>CUBE_REV_0813_TEST_HOOKS.apply(op),responseOp);
  }
  expect(rr.action).toBe('RESPONSE_APPLIED');
  expect(['TELEMETRY_APPLIED','TELEMETRY_MERGED_ON_LATEST']).toContain(rt.action);
  const afterRace=await a.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.getStoredState());
  expect(afterRace.cursor).toBe(2);expect(afterRace.responses).toHaveLength(2);expect(afterRace.telemetry.some(e=>e.event_id==='CR0813-RACE-EVENT')).toBe(true);

  const beforeHide=JSON.stringify(afterRace.responses);
  await b.evaluate(()=>dispatchEvent(new PageTransitionEvent('pagehide',{persisted:false})));
  await b.close();
  await a.waitForTimeout(300);
  const afterHide=await a.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.getStoredState());
  expect(JSON.stringify(afterHide.responses)).toBe(beforeHide);
  const pagehidePersisted=afterHide.telemetry.some(e=>e.type==='PAGEHIDE');

  fs.mkdirSync('artifacts/0.8.13',{recursive:true});
  fs.writeFileSync('artifacts/0.8.13/native_multi_window_evidence.json',JSON.stringify({schema_version:'CR0813-NATIVE-BROWSER-EVIDENCE-1',browser:'chromium-playwright',same_origin:true,native_web_locks:true,session_id:afterHide.session_id,response_conflict:{winner:afterHide.responses[0],conflict:conflicts[0]},response_telemetry_race:{cursor:afterHide.cursor,revision:afterHide.revision,event_present:true},pagehide:{event_persisted:pagehidePersisted,response_bytes_preserved:true},result:'PASS_NATIVE_SERIALIZATION_HOLD_PAGEHIDE_DURABILITY'},null,2));
  console.log(`CR0813_NATIVE_MULTI_WINDOW_PASS cursor=${afterHide.cursor} conflict_count=${conflicts.length} pagehide_persisted=${pagehidePersisted}`);
  await browser.close();
});

test('lease expiry allows a second owner while receipt-v2 converges two deliveries to one snapshot',async()=>{
  const evidence={posts:[],polls:[]};
  const browser=await chromium.launch({headless:true});
  const context=await browser.newContext();
  await installCollectorEmulator(context,evidence);
  const [a,b]=await openPair(context);
  const browserErrors=[];
  for(const [label,page] of [['a',a],['b',b]]){
    page.on('console',msg=>{if(msg.type()==='error')browserErrors.push({label,type:'console',text:msg.text()})});
    page.on('pageerror',err=>browserErrors.push({label,type:'pageerror',text:String(err&&err.message||err)}));
  }
  await Promise.all([a.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.setLeaseTimeoutForTest(1000)),b.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.setLeaseTimeoutForTest(1000))]);
  await a.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.completeResponses('U'));
  await expect.poll(()=>a.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.getStoredState().cursor)).toBe(28);
  await a.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.savePostTask('lease-expiry-network-ambiguity'));
  await expect.poll(()=>b.evaluate(()=>{const s=CUBE_REV_0813_TEST_HOOKS.getState();return `${s.status}|${s.cursor}`}),{timeout:10000}).toBe('READY_TO_SUBMIT|28');
  await b.evaluate(()=>{CUBE_REV_0813_TEST_HOOKS.send();return true});
  try{
    await expect.poll(()=>evidence.posts.length,{timeout:10000}).toBe(1);
  }catch(error){
    const [aState,bState,stored,aUi,bUi]=await Promise.all([
      a.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.getState()),
      b.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.getState()),
      a.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.getStoredState()),
      a.evaluate(()=>({done:document.querySelector('#doneText')?.textContent||'',retryHidden:document.querySelector('#retry')?.classList.contains('hidden'),doneHidden:document.querySelector('#done')?.classList.contains('hidden')})),
      b.evaluate(()=>({done:document.querySelector('#doneText')?.textContent||'',retryHidden:document.querySelector('#retry')?.classList.contains('hidden'),doneHidden:document.querySelector('#done')?.classList.contains('hidden')}))
    ]);
    const diagnostic={schema_version:'CR0813-NATIVE-SUBMISSION-DIAGNOSTIC-1',posts:evidence.posts,polls:evidence.polls,browser_errors:browserErrors,a_state:{status:aState.status,revision:aState.revision,cursor:aState.cursor,submission_control:aState.submission_control,snapshot_sealed:!!aState.submission_snapshot},b_state:{status:bState.status,revision:bState.revision,cursor:bState.cursor,submission_control:bState.submission_control,snapshot_sealed:!!bState.submission_snapshot},stored_state:{status:stored&&stored.status,revision:stored&&stored.revision,cursor:stored&&stored.cursor,submission_control:stored&&stored.submission_control,snapshot_sealed:!!(stored&&stored.submission_snapshot)},a_ui:aUi,b_ui:bUi};
    fs.mkdirSync('artifacts/0.8.13',{recursive:true});
    fs.writeFileSync('artifacts/0.8.13/native_submission_failure.json',JSON.stringify(diagnostic,null,2));
    throw new Error(`NATIVE_SUBMISSION_NO_POST:${JSON.stringify(diagnostic)}`,{cause:error});
  }
  const sealed1=await a.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.getStoredState());
  expect(sealed1.submission_snapshot).toBeTruthy();
  const identity=await a.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.transportIdentity());
  expect(identity.transport_session_id).toMatch(/^CR-[0-9]{14}-[0-9a-f]{12}$/);
  expect(identity.scientific_session_id).toBe(sealed1.submission_snapshot.session_id);
  if(identity.transport_session_id!==identity.scientific_session_id)expect(identity.transport_session_policy).toBe('DETERMINISTIC_LEGACY_SESSION_BRIDGE_V1');
  const copyIsolation=await a.evaluate(()=>{
    const h=CUBE_REV_0813_TEST_HOOKS,canonical=h.exportSnapshot(),working=h.collectorWorkingCopy();
    const before=canonical.session_id;
    working.session_id='CR-20000101000000-000000000000';
    return {canonical_frozen:Object.isFrozen(canonical),working_frozen:Object.isFrozen(working),canonical_session_id:canonical.session_id,before};
  });
  expect(copyIsolation.canonical_frozen).toBe(true);
  expect(copyIsolation.working_frozen).toBe(false);
  expect(copyIsolation.canonical_session_id).toBe(copyIsolation.before);
  const snapshotHash=sealed1.submission_snapshot_hash,retryId=sealed1.submission_control.retry_id;
  await a.waitForTimeout(1400);
  await a.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.send());
  await expect.poll(()=>evidence.posts.length,{timeout:10000}).toBe(2);
  await expect.poll(()=>a.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.getStoredState().status),{timeout:15000}).toBe('SUBMITTED');
  await a.waitForTimeout(5500);
  const finalState=await a.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.getStoredState());
  expect(finalState.submission_snapshot_hash).toBe(snapshotHash);
  expect(finalState.submission_control.retry_id).toBe(retryId);
  expect(finalState.submission_control.lease_generation).toBe(2);
  expect(finalState.responses).toHaveLength(28);
  expect(evidence.posts[0].session_id).toBe(identity.transport_session_id);
  expect(evidence.posts[0].session_id).toBe(evidence.posts[1].session_id);
  expect(evidence.posts[0].envelope_session_id).toBe(identity.transport_session_id);
  expect(evidence.posts[0].scientific_session_id).toBe(identity.scientific_session_id);
  expect(evidence.posts[0].original_scientific_session_id).toBe(identity.scientific_session_id);
  expect(evidence.posts[0].transport_session_policy).toBe(identity.transport_session_policy);
  expect(evidence.posts[0].trial_count).toBe(28);expect(evidence.posts[0].response_count).toBe(28);
  expect(evidence.posts[0].checksum).toBe(evidence.posts[1].checksum);
  expect(evidence.posts[0].payload_sha256).toBe(evidence.posts[1].payload_sha256);
  expect(evidence.posts[0].nonce).not.toBe(evidence.posts[1].nonce);
  const terminalStatuses=new Set(evidence.polls.filter(x=>x.status!=='pending').map(x=>x.status));
  expect(terminalStatuses.has('duplicate')).toBe(true);
  const envelope=await a.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.exportSnapshot());
  fs.mkdirSync('artifacts/0.8.13',{recursive:true});
  fs.writeFileSync('artifacts/0.8.13/native_snapshot.json',JSON.stringify(envelope));
  fs.writeFileSync('artifacts/0.8.13/delayed_receipt_evidence.json',JSON.stringify({schema_version:'CR0813-DELAYED-RECEIPT-EVIDENCE-2',lease_timeout_ms:1000,post_count:evidence.posts.length,posts:evidence.posts,polls:evidence.polls,session_bridge:identity,final:{status:finalState.status,lease_generation:finalState.submission_control.lease_generation,snapshot_hash:snapshotHash,retry_id:retryId,response_count:finalState.responses.length},result:'PASS_TWO_DELIVERIES_ONE_SNAPSHOT_TRANSPORT_BRIDGE_LOCAL_RECEIPT_V2'},null,2));
  console.log(`CR0813_LEASE_EXPIRY_AMBIGUITY_PASS posts=${evidence.posts.length} generation=${finalState.submission_control.lease_generation} status=${finalState.status} bridge=${identity.transport_session_policy}`);
  await browser.close();
});
