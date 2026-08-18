"use strict";
const assert=require("node:assert/strict");

class Storage{
  constructor(){this.x={};}
  getItem(k){return Object.prototype.hasOwnProperty.call(this.x,k)?this.x[k]:null;}
  setItem(k,v){this.x[k]=String(v);}
  removeItem(k){delete this.x[k];}
}
const storage=new Storage();
const messageListeners=new Set();
let driveChecksum="";
let randomCounter=0;
const fakeWindow={
  localStorage:storage,
  addEventListener(type,fn){if(type==="message")messageListeners.add(fn);},
  removeEventListener(type,fn){if(type==="message")messageListeners.delete(fn);},
  open(){return {};}
};
function element(tag){
  return {
    tagName:String(tag).toUpperCase(),children:[],style:{},hidden:false,
    appendChild(c){this.children.push(c);return c;},setAttribute(){},remove(){},
    submit(){
      const f=Object.fromEntries(this.children.map(c=>[c.name,c.value]));
      const ack={type:"CUBE_REV_COLLECTOR_ACK",ok:true,status:"duplicate",submission_nonce:f.submission_nonce,session_id:f.session_id,checksum_fnv1a32:f.checksum_fnv1a32,receipt_code:"DUP-CACHED",confirmation_source:"doPost_store_complete"};
      queueMicrotask(()=>{for(const fn of messageListeners)fn({data:ack});});
    }
  };
}
global.window=fakeWindow;
global.document={
  createElement:element,
  body:{appendChild(){}},
  head:{appendChild(script){
    const u=new URL(script.src);const cb=u.searchParams.get("callback");
    const nonce=u.searchParams.get("submission_nonce");const sessionId=u.searchParams.get("session_id");
    queueMicrotask(()=>fakeWindow[cb]({type:"CUBE_REV_COLLECTOR_ACK",ok:true,status:"stored",submission_nonce:nonce,session_id:sessionId,checksum_fnv1a32:driveChecksum,receipt_code:"DRIVE-LOOKUP",confirmation_source:"drive_lookup",received_at:"2026-08-18T03:00:00.000Z"}));
  }}
};
require("../js/collector-client.js");
const Client=fakeWindow.CubeRevCollectorClient;
const hashString=text=>{let h=0x811c9dc5;for(const ch of text){h^=ch.charCodeAt(0);h=Math.imul(h,0x01000193)>>>0;}return h>>>0;};
const config=Client.normalizeConfig({enabled:true,endpoint:"https://script.google.com/macros/s/TEST/exec",collectorId:"CUBE-REV-0712-MAIN",protocolVersion:"receipt-v2",gzipWhenAvailable:false,timeoutMs:30000,receiptPollIntervalMs:700,healthCheckTimeoutMs:5000},"0.7.12");
const randomHex=()=>`r15${String(++randomCounter).padStart(21,"0")}`;
const mk=(session,extra={})=>new Client({config,version:"0.7.12",getSession:()=>session,exportSession:()=>session,logEvent:(t,x)=>{session.events=session.events||[];session.events.push({type:t,...x});},persist:()=>{},setStatus:()=>{},randomHex,hashString,translate:k=>k,snapshotStorage:storage,...extra});

(async()=>{
  // Court 1: the first pre-transport export is sealed and survives a failed receipt + page/client reconstruction.
  {
    const session={project:"CUBE-REV",version:"0.7.12",session_id:"CR-R15-SNAPSHOT",trials:[{choice:"U",latency_ms:123}],data_submission:{}};
    const posted=[];
    const c1=mk(session);
    c1.checkHealth=async()=>({expected_version:"0.7.12",receipt_confirmation_available:true,collector_id:"CUBE-REV-0712-MAIN",protocol_version:"receipt-v2"});
    c1.postWithConfirmedReceipt=async f=>{posted.push({...f});throw new Error("RECEIPT_LOST_AFTER_STORE");};
    await assert.rejects(c1.submit(),/RECEIPT_LOST_AFTER_STORE/);
    assert.ok(storage.getItem(c1.snapshotKey(session.session_id)),"failed submission must retain exact snapshot locally");
    const firstPayload=posted[0].payload, firstChecksum=posted[0].checksum_fnv1a32;

    // Deliberately mutate both scientific-looking state and transport telemetry after the failed attempt.
    session.trials[0].choice="R";session.runtime_note="MUTATED_AFTER_FIRST_POST";
    const c2=mk(session);
    c2.checkHealth=c1.checkHealth;
    c2.postWithConfirmedReceipt=async f=>{posted.push({...f});return {ok:true,status:"stored",checksum_fnv1a32:f.checksum_fnv1a32,receipt_code:"RECOVERED",received_at:"2026-08-18T03:00:01.000Z",checksum_verified:true};};
    const receipt=await c2.submit();
    assert.equal(posted[1].payload,firstPayload,"retry after reconstruction must reuse byte-identical sealed payload");
    assert.equal(posted[1].checksum_fnv1a32,firstChecksum,"retry checksum must be immutable");
    assert.equal(receipt.status,"stored");
    assert.equal(session.data_submission.submission_snapshot_source,"local_storage");
    assert.equal(storage.getItem(c2.snapshotKey(session.session_id)),null,"confirmed receipt may clear local retry snapshot");
  }

  // Court 2: an internally corrupted persisted snapshot is fail-closed, never silently regenerated.
  {
    const session={project:"CUBE-REV",version:"0.7.12",session_id:"CR-R15-CORRUPT",trials:[],data_submission:{}};
    const c=mk(session);
    storage.setItem(c.snapshotKey(session.session_id),JSON.stringify({schema:"CUBE_REV_SUBMISSION_SNAPSHOT_V1",version:"0.7.12",session_id:session.session_id,checksum_fnv1a32:"00000000",text:"{\"x\":1}"}));
    assert.throws(()=>c.sealSubmissionSnapshot(),/SUBMISSION_SNAPSHOT_STORAGE_CORRUPT/);
    storage.removeItem(c.snapshotKey(session.session_id));
  }

  // Court 3: R1.4 counterexample. Cached duplicate ACK matches retry B, but Drive contains A -> reject regardless of cache-first ordering.
  {
    const session={project:"CUBE-REV",version:"0.7.12",session_id:"CR-R15-RACE-MISMATCH",data_submission:{}};
    const c=mk(session);
    const retryChecksum="c8d53a2d";driveChecksum="b467dd85";
    await assert.rejects(c.postWithConfirmedReceipt({submission_nonce:"571b61d40a9093b2249ffe44",session_id:session.session_id,checksum_fnv1a32:retryChecksum,payload:"B",encoding:"json"}),/DUPLICATE_STORED_BYTE_CHECKSUM_MISMATCH/);
  }

  // Court 4: a legitimate same-byte duplicate is promoted only after a fresh-nonce Drive lookup proves stored-byte identity.
  {
    const session={project:"CUBE-REV",version:"0.7.12",session_id:"CR-R15-RACE-LEGIT",data_submission:{}};
    const c=mk(session);
    const checksum="b467dd85";driveChecksum=checksum;
    const r=await c.postWithConfirmedReceipt({submission_nonce:"samebytesnonce000000000001",session_id:session.session_id,checksum_fnv1a32:checksum,payload:"A",encoding:"json"});
    assert.equal(r.status,"duplicate");
    assert.equal(r.checksum_fnv1a32,checksum);
    assert.equal(r.checksum_verified,true);
    assert.equal(r.stored_byte_reverified,true);
    assert.equal(r.stored_confirmation_source,"drive_lookup");
    assert.match(r.transport,/fresh_drive_lookup/);
    assert.notEqual(r.stored_lookup_nonce,"samebytesnonce000000000001","reverification must use an independent nonce");
  }

  console.log("CR0105R15_RECEIPT_RACE_CLOSURE_PASS 4/4");
})().catch(e=>{console.error(e);process.exit(1);});
