const assert=require('assert');
const M=require('../js/participant-cognitive-mode-0.8.8.js');
const C=require('../cognitive/COGNITIVE_MODE_CONFIG_0.8.8.json');
const Shadow=require('../js/collector-submit-shadow-0.8.7.js');

class S{
  constructor(){this.x={}}
  getItem(k){return this.x[k]??null}
  setItem(k,v){this.x[k]=String(v)}
  removeItem(k){delete this.x[k]}
}

function fixture(){
  const storage=new S();
  const cryptoObj={getRandomValues(a){a.set([9,10,11,12]);return a}};
  let tick=0;
  const now=()=>`2026-08-02T15:${String(Math.floor(tick/60)).padStart(2,'0')}:${String(tick++%60).padStart(2,'0')}.000Z`;
  let state=M.loadOrCreate(C,{storage,cryptoObj,now}).state;
  return {storage,cryptoObj,now,get state(){return state},set state(v){state=v}};
}

function complete(f){
  for(let i=0;i<28;i++){
    f.state=M.record(f.storage,f.state,{
      stimulus_id:f.state.schedule[f.state.cursor],
      choice_display:'U',
      choice_canonical:'U',
      latency_ms:50
    },f.now);
  }
  f.state=M.savePostTask(f.storage,f.state,{
    hypothesis_guess:'',confidence:0,deliberate_strategy_change:false,technical_notes:''
  },f.now);
  f.state=M.prepareSubmissionSnapshot(f.storage,f.state,f.now);
  return {
    text:JSON.stringify(M.exportSnapshot(f.state)),
    hash:f.state.submission_snapshot_hash
  };
}

function clientFor(f,postWithConfirmedReceipt){
  return new Shadow({
    config:{collectorId:'CUBE-REV-0712-MAIN',protocolVersion:'receipt-v2'},
    version:'0.7.12',
    getSession:()=>f.state,
    exportSession:()=>M.exportSnapshot(f.state),
    persist:()=>{f.state=M.saveExternalMutation(f.storage,f.state,f.now)},
    now:f.now,
    randomHex:()=>`n${f.state.revision}`,
    hashString:M.fnv1a,
    isAutomaticConfigured:()=>true,
    checkHealth:async()=>({
      collector_id:'CUBE-REV-0712-MAIN',
      protocol_version:'receipt-v2',
      expected_version:'0.7.12'
    }),
    encodePayload:async s=>({payload:s,encoding:'json',original_bytes:s.length,transmitted_bytes:s.length}),
    postWithConfirmedReceipt
  });
}

(async()=>{
  // Gate 1: a snapshot cannot be sealed before scientific completion.
  {
    const f=fixture();
    assert.throws(()=>M.prepareSubmissionSnapshot(f.storage,f.state,f.now),/SNAPSHOT_NOT_READY/);
  }

  // Gate 2: sealing is idempotent and post-seal telemetry cannot change the payload.
  {
    const f=fixture();
    const sealed=complete(f);
    const again=M.prepareSubmissionSnapshot(f.storage,f.state,f.now);
    assert.equal(JSON.stringify(M.exportSnapshot(again)),sealed.text);
    assert.equal(again.submission_snapshot_hash,sealed.hash);
    f.state=M.event(f.storage,again,'SUBMISSION_ATTEMPT',{attempt:1},f.now);
    f.state=M.event(f.storage,f.state,'SUBMISSION_FAILED',{attempt:1},f.now);
    assert.equal(JSON.stringify(M.exportSnapshot(f.state)),sealed.text);
    assert.equal(f.state.submission_snapshot_hash,sealed.hash);
  }

  // Gate 3: receipt loss followed by duplicate recovery uses an identical checksum.
  {
    const f=fixture();
    const sealed=complete(f);
    let postCount=0,firstChecksum=null,secondChecksum=null;
    const client=clientFor(f,async req=>{
      postCount++;
      if(postCount===1){
        firstChecksum=req.checksum_fnv1a32;
        throw new Error('RECEIPT_LOST_AFTER_STORE');
      }
      secondChecksum=req.checksum_fnv1a32;
      return {ok:true,status:'duplicate',checksum_fnv1a32:firstChecksum};
    });
    await assert.rejects(client.submit(),/RECEIPT_LOST/);
    f.state=M.event(f.storage,f.state,'SUBMISSION_FAILED',{attempt:1},f.now);
    assert.equal(JSON.stringify(M.exportSnapshot(f.state)),sealed.text);
    await client.submit();
    assert.equal(firstChecksum,secondChecksum);
    assert.equal(f.state.data_submission.status,'received');
    assert.equal(f.state.data_submission.checksum_fnv1a32,firstChecksum);
    assert.equal(postCount,2);
  }

  // Gate 4: concurrent calls through one client collapse to one in-flight POST.
  {
    const f=fixture();
    complete(f);
    let posts=0;
    const client=clientFor(f,async req=>{
      posts++;
      await new Promise(r=>setTimeout(r,5));
      return {ok:true,status:'stored',checksum_fnv1a32:req.checksum_fnv1a32};
    });
    const [a,b]=await Promise.all([client.submit(),client.submit()]);
    assert.equal(posts,1);
    assert.equal(a.status,'stored');
    assert.equal(b.status,'stored');
  }

  // Gate 5: a collector checksum mismatch is never promoted to received.
  {
    const f=fixture();
    complete(f);
    const client=clientFor(f,async()=>({ok:true,status:'stored',checksum_fnv1a32:'00000000'}));
    await assert.rejects(client.submit(),/CHECKSUM_MISMATCH/);
    assert.equal(f.state.data_submission.status,'failed');
    assert.equal(f.state.data_submission.receipt_confirmed,false);
  }

  // Gate 6: top-level corruption is quarantined even without snapshot mutation.
  {
    const f=fixture();
    complete(f);
    const raw=JSON.parse(f.storage.getItem(M.STORAGE_KEY));
    raw.cursor=3;
    f.storage.setItem(M.STORAGE_KEY,JSON.stringify(raw));
    const recovered=M.loadOrCreate(C,{storage:f.storage,cryptoObj:f.cryptoObj,now:f.now});
    assert.equal(recovered.resumed,false);
    assert.ok(f.storage.getItem(M.QUARANTINE_KEY));
  }

  // Gate 7: snapshot mutation is quarantined even if the outer integrity field is recomputed.
  {
    const f=fixture();
    complete(f);
    const raw=JSON.parse(f.storage.getItem(M.STORAGE_KEY));
    raw.submission_snapshot.responses[0].choice_display='R';
    raw.integrity=M.checksum({...raw,integrity:undefined});
    f.storage.setItem(M.STORAGE_KEY,JSON.stringify(raw));
    const recovered=M.loadOrCreate(C,{storage:f.storage,cryptoObj:f.cryptoObj,now:f.now});
    assert.equal(recovered.resumed,false);
    assert.ok(f.storage.getItem(M.QUARANTINE_KEY));
  }

  // Gate 8: sequence/schedule drift is quarantined rather than silently reassigned.
  {
    const f=fixture();
    const raw=JSON.parse(f.storage.getItem(M.STORAGE_KEY));
    raw.sequence_id=raw.sequence_id==='24'?'1':String(Number(raw.sequence_id)+1);
    raw.integrity=M.checksum({...raw,integrity:undefined});
    f.storage.setItem(M.STORAGE_KEY,JSON.stringify(raw));
    const recovered=M.loadOrCreate(C,{storage:f.storage,cryptoObj:f.cryptoObj,now:f.now});
    assert.equal(recovered.resumed,false);
    assert.ok(f.storage.getItem(M.QUARANTINE_KEY));
  }

  console.log('CR0808_IMMUTABLE_SNAPSHOT_PASS 8/8');
})().catch(e=>{console.error(e);process.exit(1)});
