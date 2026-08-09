'use strict';
const {test,expect,chromium}=require('@playwright/test');
const {spawn}=require('child_process');
const fs=require('fs');
const path=require('path');
const zlib=require('zlib');
const crypto=require('crypto');

const PORT=8142;
const BASE=`http://127.0.0.1:${PORT}/participant-cognitive-mode-0.8.13.html?test_mode=1&lease_dynamic=0814`;
const ITERATIONS=4;
let server;

const sleep=ms=>new Promise(resolve=>setTimeout(resolve,ms));
async function waitServer(){
  const deadline=Date.now()+15000;
  while(Date.now()<deadline){
    try{const r=await fetch(`http://127.0.0.1:${PORT}/`);if(r.ok||r.status===404)return}catch(_){}
    await sleep(100);
  }
  throw new Error('STATIC_SERVER_TIMEOUT');
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
      return route.fulfill({status:200,contentType:'application/javascript',body:`${cb}(${JSON.stringify({ok:true,collector_id:'CUBE-REV-0712-MAIN',protocol_version:'receipt-v2',expected_version:'0.7.12',receipt_confirmation_available:true,deployment_id:'CR0814-DYNAMIC-LEASE-EMULATOR'})});`});
    }
    if(req.method()==='POST'){
      const fields=Object.fromEntries(new URLSearchParams(req.postData()||''));
      const decoded=decodeCollectorPayload(fields),envelope=decoded.value,snapshot=envelope.cognitive_snapshot||{};
      const index=evidence.posts.length;
      const record={
        index,
        observed_at_ms:Date.now(),
        observed_at:new Date().toISOString(),
        session_id:fields.session_id,
        nonce:fields.submission_nonce,
        checksum:fields.checksum_fnv1a32,
        payload_bytes:Buffer.byteLength(decoded.text),
        payload_sha256:decoded.sha256,
        envelope_session_id:envelope.session_id,
        scientific_session_id:snapshot.session_id,
        original_scientific_session_id:envelope.original_scientific_session_id,
        transport_session_policy:envelope.transport_session_policy,
        trial_count:Array.isArray(envelope.trials)?envelope.trials.length:null,
        response_count:Array.isArray(snapshot.responses)?snapshot.responses.length:null
      };
      evidence.posts.push(record);
      receipts.set(record.nonce,{...record,status:index===0?'stored':'duplicate',readyAt:Date.now()+(index===0?3000:150)});
      return route.fulfill({status:200,contentType:'text/html',body:'<!doctype html><title>accepted</title>'});
    }
    if(req.method()==='GET'&&action==='receipt'){
      const cb=url.searchParams.get('callback')||'callback',nonce=url.searchParams.get('submission_nonce'),rec=receipts.get(nonce);
      let payload;
      if(!rec||Date.now()<rec.readyAt)payload={ok:true,status:'pending',submission_nonce:nonce,session_id:url.searchParams.get('session_id')};
      else payload={ok:true,status:rec.status,submission_nonce:nonce,session_id:rec.session_id,checksum_fnv1a32:rec.checksum,receipt_code:`CR0814-DYNAMIC-${rec.index+1}`,file_name:`${rec.session_id}.json`,received_at:new Date().toISOString()};
      evidence.polls.push({nonce,status:payload.status,at_ms:Date.now(),at:new Date().toISOString()});
      return route.fulfill({status:200,contentType:'application/javascript',body:`${cb}(${JSON.stringify(payload)});`});
    }
    return route.fulfill({status:404,body:'not found'});
  });
}
async function openPage(context,label,errors){
  const page=await context.newPage();
  page.on('console',msg=>{if(msg.type()==='error')errors.push({label,type:'console',text:msg.text(),at:new Date().toISOString()})});
  page.on('pageerror',err=>errors.push({label,type:'pageerror',text:String(err&&err.message||err),at:new Date().toISOString()}));
  await page.goto(BASE,{waitUntil:'domcontentloaded'});
  await page.click('#begin');
  await page.waitForFunction(()=>!!window.CUBE_REV_0813_TEST_HOOKS);
  return page;
}
async function pollValue(fn,predicate,{timeout=10000,interval=50,label='POLL_TIMEOUT'}={}){
  const deadline=Date.now()+timeout;
  let value;
  while(Date.now()<deadline){
    value=await fn();
    if(predicate(value))return value;
    await sleep(interval);
  }
  throw new Error(`${label}:${JSON.stringify(value)}`);
}
async function waitPastPersistedExpiry(page,lease,evidence){
  const expiresMs=Date.parse(lease.lease_expires_at);
  if(!Number.isFinite(expiresMs))throw new Error(`LEASE_EXPIRY_INVALID:${lease.lease_expires_at}`);
  const targetMs=expiresMs+250;
  const before={node_now_ms:Date.now(),browser_now_ms:await page.evaluate(()=>Date.now()),target_ms:targetMs};
  while(Date.now()<targetMs)await sleep(Math.min(100,Math.max(10,targetMs-Date.now())));
  const after={node_now_ms:Date.now(),browser_now_ms:await page.evaluate(()=>Date.now()),target_ms:targetMs};
  evidence.expiry_wait={before,after,margin_after_expiry_ms:after.browser_now_ms-expiresMs};
  if(after.browser_now_ms<=expiresMs)throw new Error(`LEASE_NOT_EXPIRED:${JSON.stringify(evidence.expiry_wait)}`);
}

async function runIteration(browser,iteration){
  const context=await browser.newContext();
  const evidence={iteration,posts:[],polls:[],browser_errors:[]};
  await installCollectorEmulator(context,evidence);
  try{
    const first=await openPage(context,`first-${iteration}`,evidence.browser_errors);
    await first.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.setLeaseTimeoutForTest(1000));
    await first.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.completeResponses('U'));
    await pollValue(
      ()=>first.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.getStoredState().cursor),
      value=>value===28,
      {label:'RESPONSES_NOT_COMPLETE'}
    );
    await first.evaluate(label=>CUBE_REV_0813_TEST_HOOKS.savePostTask(label),`dynamic-lease-${iteration}`);
    await first.evaluate(()=>{CUBE_REV_0813_TEST_HOOKS.send();return true});
    await pollValue(()=>Promise.resolve(evidence.posts.length),value=>value===1,{label:'FIRST_POST_NOT_OBSERVED'});

    const lease=await pollValue(
      ()=>first.evaluate(()=>{
        const s=CUBE_REV_0813_TEST_HOOKS.getStoredState();
        return s&&s.submission_control?{
          revision:s.revision,
          status:s.status,
          lease_token:s.submission_control.lease_token,
          lease_owner:s.submission_control.lease_owner,
          lease_generation:s.submission_control.lease_generation,
          lease_expires_at:s.submission_control.lease_expires_at,
          last_attempt_at:s.submission_control.last_attempt_at,
          snapshot_hash:s.submission_snapshot_hash,
          retry_id:s.submission_control.retry_id,
          response_count:s.responses.length
        }:null;
      }),
      value=>!!(value&&value.lease_token&&value.lease_expires_at&&value.lease_generation===1),
      {label:'PERSISTED_FIRST_LEASE_MISSING'}
    );
    evidence.first_lease=lease;
    expect(lease.status).toBe('READY_TO_SUBMIT');
    expect(lease.response_count).toBe(28);
    await waitPastPersistedExpiry(first,lease,evidence);

    const second=await openPage(context,`second-${iteration}`,evidence.browser_errors);
    await second.evaluate(()=>{CUBE_REV_0813_TEST_HOOKS.send();return true});
    await pollValue(()=>Promise.resolve(evidence.posts.length),value=>value===2,{timeout:10000,label:'SECOND_POST_NOT_OBSERVED_AFTER_PERSISTED_EXPIRY'});
    await pollValue(
      ()=>second.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.getStoredState().status),
      value=>value==='SUBMITTED',
      {timeout:10000,label:'SECOND_OWNER_DID_NOT_CONFIRM'}
    );
    await sleep(3400);

    const finalState=await second.evaluate(()=>CUBE_REV_0813_TEST_HOOKS.getStoredState());
    evidence.final={
      status:finalState.status,
      revision:finalState.revision,
      lease_generation:finalState.submission_control.lease_generation,
      lease_token:finalState.submission_control.lease_token,
      snapshot_hash:finalState.submission_snapshot_hash,
      retry_id:finalState.submission_control.retry_id,
      response_count:finalState.responses.length,
      receipt:finalState.submission_receipt
    };
    expect(evidence.posts).toHaveLength(2);
    expect(evidence.posts[0].payload_sha256).toBe(evidence.posts[1].payload_sha256);
    expect(evidence.posts[0].checksum).toBe(evidence.posts[1].checksum);
    expect(evidence.posts[0].payload_bytes).toBe(evidence.posts[1].payload_bytes);
    expect(evidence.posts[0].session_id).toBe(evidence.posts[1].session_id);
    expect(evidence.posts[0].nonce).not.toBe(evidence.posts[1].nonce);
    expect(evidence.posts[0].trial_count).toBe(28);
    expect(evidence.posts[0].response_count).toBe(28);
    expect(evidence.final.status).toBe('SUBMITTED');
    expect(evidence.final.lease_generation).toBe(2);
    expect(evidence.final.lease_token).toBeNull();
    expect(evidence.final.snapshot_hash).toBe(lease.snapshot_hash);
    expect(evidence.final.retry_id).toBe(lease.retry_id);
    expect(evidence.final.response_count).toBe(28);
    const terminal=new Set(evidence.polls.filter(x=>x.status!=='pending').map(x=>x.status));
    expect(terminal.has('duplicate')).toBe(true);
    expect(terminal.has('stored')).toBe(true);
    evidence.result='PASS_DYNAMIC_PERSISTED_EXPIRY_TAKEOVER';
    return evidence;
  }finally{
    await context.close().catch(()=>{});
  }
}

test.beforeAll(async()=>{
  server=spawn('python3',['-m','http.server',String(PORT),'--bind','127.0.0.1'],{cwd:path.resolve(__dirname,'..'),stdio:'ignore'});
  await waitServer();
});
test.afterAll(()=>{if(server&&!server.killed)server.kill('SIGTERM')});

test('persisted lease expiry deterministically permits a second page owner',async()=>{
  const browser=await chromium.launch({headless:true});
  const iterations=[];
  try{
    for(let i=0;i<ITERATIONS;i++){
      const result=await runIteration(browser,i);
      iterations.push(result);
      console.log(`CR0814_DYNAMIC_LEASE_ITERATION_PASS iteration=${i+1}/${ITERATIONS} posts=${result.posts.length} generation=${result.final.lease_generation} margin_ms=${result.expiry_wait.margin_after_expiry_ms}`);
    }
  }finally{
    await browser.close();
  }
  const report={
    schema_version:'CR0814-DYNAMIC-LEASE-EXPIRY-EVIDENCE-1',
    route:'participant-cognitive-mode-0.8.13.html',
    timing_policy:'READ_PERSISTED_LEASE_EXPIRES_AT_THEN_OPEN_SECOND_PAGE_AFTER_250MS_MARGIN',
    fixed_sleep_used:false,
    iteration_count:iterations.length,
    passed_iterations:iterations.filter(x=>x.result==='PASS_DYNAMIC_PERSISTED_EXPIRY_TAKEOVER').length,
    total_posts:iterations.reduce((n,x)=>n+x.posts.length,0),
    all_payload_pairs_identical:iterations.every(x=>x.posts[0].payload_sha256===x.posts[1].payload_sha256&&x.posts[0].checksum===x.posts[1].checksum),
    all_final_generations_two:iterations.every(x=>x.final.lease_generation===2),
    iterations,
    result:'PASS_DYNAMIC_PERSISTED_LEASE_EXPIRY_REPEATED'
  };
  fs.mkdirSync('artifacts/0.8.14',{recursive:true});
  fs.writeFileSync('artifacts/0.8.14/dynamic_lease_expiry_evidence.json',JSON.stringify(report,null,2));
  expect(report.passed_iterations).toBe(ITERATIONS);
  expect(report.total_posts).toBe(ITERATIONS*2);
  expect(report.all_payload_pairs_identical).toBe(true);
  expect(report.all_final_generations_two).toBe(true);
  console.log(`CR0814_DYNAMIC_LEASE_EXPIRY_PASS iterations=${ITERATIONS}/${ITERATIONS} posts=${report.total_posts} fixed_sleep=false`);
});
