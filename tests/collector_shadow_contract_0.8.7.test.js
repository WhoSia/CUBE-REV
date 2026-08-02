const assert=require('assert');
const C=require('../js/collector-submit-shadow-0.8.7.js');
function fnv1a(s){let h=0x811c9dc5;for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,0x01000193)}return h>>>0}
function make(policy){
 let session={session_id:'CR0807-S',version:'CUBE-REV 0.8.7',responses:[{x:1}]},persistCount=0,postCount=0,firstChecksum=null;
 const client=new C({config:{collectorId:'CUBE-REV-0712-MAIN',protocolVersion:'receipt-v2'},version:'0.7.12',getSession:()=>session,exportSession:()=>session,persist:()=>persistCount++,now:()=>`2026-08-02T14:00:0${Math.min(persistCount,9)}Z`,randomHex:()=>`nonce${postCount+1}`,hashString:fnv1a,isAutomaticConfigured:()=>true,checkHealth:async()=>policy.health||{collector_id:'CUBE-REV-0712-MAIN',protocol_version:'receipt-v2',expected_version:'0.7.12'},encodePayload:async s=>({payload:s,encoding:'json',original_bytes:s.length,transmitted_bytes:s.length}),postWithConfirmedReceipt:async f=>{postCount++;if(!firstChecksum)firstChecksum=f.checksum_fnv1a32;return policy.post(f,{postCount,firstChecksum});}});
 return {client,session,get:()=>({persistCount,postCount,firstChecksum})};
}
(async()=>{
 const results={};
 {const x=make({post:async f=>({ok:true,status:'stored',checksum_fnv1a32:f.checksum_fnv1a32})});await x.client.submit();assert.equal(x.session.data_submission.status,'received');results.stored_current_checksum='PASS';}
 {const x=make({post:async f=>({ok:true,status:'duplicate',checksum_fnv1a32:f.checksum_fnv1a32})});await x.client.submit();assert.equal(x.session.data_submission.collector_status,'duplicate');results.duplicate_current_checksum='PASS';}
 {const x=make({post:async f=>({ok:true,status:'stored',checksum_fnv1a32:'deadbeef'})});await assert.rejects(x.client.submit(),/CHECKSUM_MISMATCH/);assert.equal(x.session.data_submission.status,'failed');results.checksum_mismatch_rejected='PASS';}
 {const x=make({health:{collector_id:'WRONG',protocol_version:'receipt-v2',expected_version:'0.7.12'},post:async()=>{throw new Error('UNREACHED')}});await assert.rejects(x.client.submit(),/WRONG_COLLECTOR/);assert.equal(x.get().postCount,0);results.health_wrong_collector_prevents_post='PASS';}
 {const x=make({post:async(f,m)=>{if(m.postCount===1)throw new Error('RECEIPT_LOST_AFTER_STORE');return {ok:true,status:'duplicate',checksum_fnv1a32:f.checksum_fnv1a32}}});await assert.rejects(x.client.submit(),/RECEIPT_LOST/);const first=x.get().firstChecksum;await x.client.submit();assert.equal(x.session.data_submission.status,'received');assert.notEqual(first,x.session.data_submission.checksum_fnv1a32);results.receipt_loss_duplicate_current_checksum='PASS';}
 {const x=make({post:async(f,m)=>{if(m.postCount===1)throw new Error('RECEIPT_LOST_AFTER_STORE');return {ok:true,status:'duplicate',checksum_fnv1a32:m.firstChecksum}}});await assert.rejects(x.client.submit(),/RECEIPT_LOST/);await assert.rejects(x.client.submit(),/CHECKSUM_MISMATCH/);results.receipt_loss_duplicate_original_checksum='FAILS_BY_DESIGN_DEPENDENCY';}
 {let release,pending;const gate=new Promise(r=>{release=r});const x=make({post:async f=>{pending=f;return gate}});const a=x.client.submit(),b=x.client.submit();while(!pending)await new Promise(r=>setImmediate(r));release({ok:true,status:'stored',checksum_fnv1a32:pending.checksum_fnv1a32});const [ra,rb]=await Promise.all([a,b]);assert.equal(x.get().postCount,1);assert.deepEqual(ra,rb);results.inflight_single_post_two_callers='PASS';}
 console.log(JSON.stringify(results,null,2));
})().catch(e=>{console.error(e);process.exit(1)});
