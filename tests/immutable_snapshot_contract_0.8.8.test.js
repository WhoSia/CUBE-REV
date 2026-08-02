const assert=require('assert');
const M=require('../js/participant-cognitive-mode-0.8.8.js');
const C=require('../cognitive/COGNITIVE_MODE_CONFIG_0.8.8.json');
const Shadow=require('../js/collector-submit-shadow-0.8.7.js');
class S{constructor(){this.x={}}getItem(k){return this.x[k]??null}setItem(k,v){this.x[k]=String(v)}removeItem(k){delete this.x[k]}}
const cryptoObj={getRandomValues(a){a.set([9,10,11,12]);return a}};let tick=0;const now=()=>`2026-08-02T15:00:${String(tick++).padStart(2,'0')}.000Z`;
(async()=>{
 const storage=new S();let state=M.loadOrCreate(C,{storage,cryptoObj,now}).state;
 for(let i=0;i<28;i++)state=M.record(storage,state,{stimulus_id:state.schedule[state.cursor],choice_display:'U',choice_canonical:'U',latency_ms:50},now);
 state=M.savePostTask(storage,state,{hypothesis_guess:'',confidence:0,deliberate_strategy_change:false,technical_notes:''},now);
 state=M.prepareSubmissionSnapshot(storage,state,now);const snapText=JSON.stringify(M.exportSnapshot(state)),snapHash=state.submission_snapshot_hash;
 state=M.event(storage,state,'SUBMISSION_ATTEMPT',{attempt:1},now);assert.equal(JSON.stringify(M.exportSnapshot(state)),snapText);assert.equal(state.submission_snapshot_hash,snapHash);
 let postCount=0,firstChecksum=null;
 const client=new Shadow({config:{collectorId:'CUBE-REV-0712-MAIN',protocolVersion:'receipt-v2'},version:'0.7.12',getSession:()=>state,exportSession:()=>M.exportSnapshot(state),persist:()=>{state=M.saveExternalMutation(storage,state,now)},now,randomHex:()=>`n${postCount}`,hashString:M.fnv1a,isAutomaticConfigured:()=>true,checkHealth:async()=>({collector_id:'CUBE-REV-0712-MAIN',protocol_version:'receipt-v2',expected_version:'0.7.12'}),encodePayload:async s=>({payload:s,encoding:'json',original_bytes:s.length,transmitted_bytes:s.length}),postWithConfirmedReceipt:async f=>{postCount++;if(postCount===1){firstChecksum=f.checksum_fnv1a32;throw new Error('RECEIPT_LOST_AFTER_STORE')}return {ok:true,status:'duplicate',checksum_fnv1a32:firstChecksum}}});
 await assert.rejects(client.submit(),/RECEIPT_LOST/);state=M.event(storage,state,'SUBMISSION_FAILED',{attempt:1},now);assert.equal(JSON.stringify(M.exportSnapshot(state)),snapText);await client.submit();assert.equal(state.data_submission.status,'received');assert.equal(state.data_submission.checksum_fnv1a32,firstChecksum);assert.equal(postCount,2);
 const raw=JSON.parse(storage.getItem(M.STORAGE_KEY));raw.submission_snapshot.responses[0].choice_display='R';raw.integrity=M.checksum({...raw,integrity:undefined});storage.setItem(M.STORAGE_KEY,JSON.stringify(raw));const recovered=M.loadOrCreate(C,{storage,cryptoObj,now});assert.equal(recovered.resumed,false);assert.ok(storage.getItem(M.QUARANTINE_KEY));
 console.log('CR0808_IMMUTABLE_SNAPSHOT_PASS');
})().catch(e=>{console.error(e);process.exit(1)});
