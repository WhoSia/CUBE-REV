const assert=require('assert');
const fs=require('fs');
const os=require('os');
const path=require('path');
const Builder=require('../scripts/build_0_8_9_public_bank.js');
const Factory=require('../scripts/reconstruct_0_8_9_factory.js');
const Runtime=require('../js/participant-cognitive-mode-0.8.9.js');

class Storage{
  constructor(){this.x={}}
  getItem(k){return this.x[k]??null}
  setItem(k,v){this.x[k]=String(v)}
  removeItem(k){delete this.x[k]}
}

function recursiveKeys(value,out=[]){
  if(Array.isArray(value)){value.forEach(x=>recursiveKeys(x,out));return out}
  if(!value||typeof value!=='object')return out;
  for(const [k,v] of Object.entries(value)){out.push(k);recursiveKeys(v,out)}
  return out;
}

(function(){
  const root=path.resolve(__dirname,'..');
  const sourceBank=JSON.parse(fs.readFileSync(path.join(root,'cognitive/PARTICIPANT_STIMULUS_BANK_0.8.8.json'),'utf8'));
  const sourceConfig=JSON.parse(fs.readFileSync(path.join(root,'cognitive/COGNITIVE_MODE_CONFIG_0.8.8.json'),'utf8'));
  const built=Builder.build(sourceBank,sourceConfig);

  // Gate 1: exact source cardinalities and globally unique opaque response codes.
  assert.equal(built.publicBank.stimuli.length,28);
  assert.equal(Object.keys(built.publicConfig.schedules).length,24);
  assert.equal(built.manifest.choice_code_count,28*18);
  const allCodes=built.publicBank.stimuli.flatMap(s=>Object.values(s.choice_codes));
  assert.equal(new Set(allCodes).size,28*18);
  assert.ok(allCodes.every(x=>/^CR9C-[0-9a-f]{16}$/.test(x)));

  // Gate 2: participant files contain no internal state/rotation/canonical metadata.
  const publicKeys=new Set(recursiveKeys(built.publicBank));
  for(const key of Builder.FORBIDDEN_PUBLIC_FIELDS)assert.equal(publicKeys.has(key),false,`leaked ${key}`);
  assert.equal(built.publicBank.version,'CUBE-REV 0.8.9');
  assert.equal(built.publicConfig.version,'CUBE-REV 0.8.9');
  assert.equal(built.publicConfig.participant_ui.canonical_moves,'absent');

  // Gate 3: the private crosswalk retains exact reconstruction information.
  assert.equal(built.privateCrosswalk.classification,'DO_NOT_DEPLOY_PARTICIPANT_SIDE');
  assert.equal(built.privateCrosswalk.stimuli.length,28);
  const sourceById=Object.fromEntries(sourceBank.stimuli.map(s=>[s.stimulus_id,s]));
  for(const privateStimulus of built.privateCrosswalk.stimuli){
    const source=sourceById[privateStimulus.stimulus_id];
    assert.equal(privateStimulus.state_id,source.state_id);
    assert.equal(privateStimulus.rotation_id,source.rotation_id);
    assert.deepEqual(privateStimulus.face_map,source.face_map);
  }

  // Gate 4: public config preserves every counterbalanced schedule exactly.
  assert.deepEqual(built.publicConfig.schedules,sourceConfig.schedules);

  // Gate 5: runtime rejects internal fields and records only opaque responses.
  const storage=new Storage();
  const cryptoObj={getRandomValues(a){a.set([1,2,3,4]);return a}};
  let tick=0;const now=()=>`2026-08-02T18:00:${String(tick++%60).padStart(2,'0')}.000Z`;
  let state=Runtime.loadOrCreate(built.publicConfig,{storage,cryptoObj,now}).state;
  const first=built.publicBank.stimuli.find(s=>s.stimulus_id===state.schedule[0]);
  assert.throws(()=>Runtime.record(storage,state,{stimulus_id:first.stimulus_id,choice_display:'U',choice_code:first.choice_codes.U,choice_canonical:'U',latency_ms:1},now),/FORBIDDEN_RESPONSE_FIELD/);
  for(let i=0;i<28;i++){
    const stimulus=built.publicBank.stimuli.find(s=>s.stimulus_id===state.schedule[state.cursor]);
    state=Runtime.record(storage,state,{stimulus_id:stimulus.stimulus_id,choice_display:'U',choice_code:stimulus.choice_codes.U,latency_ms:10+i},now);
  }
  state=Runtime.savePostTask(storage,state,{hypothesis_guess:'',confidence:0,deliberate_strategy_change:false,technical_notes:''},now);
  state=Runtime.prepareSubmissionSnapshot(storage,state,now);
  const payload=Runtime.exportSnapshot(state);
  assert.equal(payload.response_encoding,'OPAQUE_CHOICE_CODE_V1');
  assert.ok(payload.responses.every(r=>r.choice_code&&!('choice_canonical' in r)&&!('state_id' in r)&&!('rotation_id' in r)));

  // Gate 6: Factory/private-crosswalk reconstruction restores every canonical row.
  const reconstructed=Factory.reconstruct(payload,built.privateCrosswalk);
  assert.equal(reconstructed.row_count,28);
  for(const row of reconstructed.rows){
    assert.ok(row.state_id!=null);
    assert.ok(row.rotation_id!=null);
    assert.ok(/^[URFDLB](?:2|')?$/.test(row.choice_canonical));
  }

  // Gate 7: mismatched display/code pairs are rejected during reconstruction.
  const bad=JSON.parse(JSON.stringify(payload));
  bad.responses[0].choice_display=bad.responses[0].choice_display==='U'?'R':'U';
  assert.throws(()=>Factory.reconstruct(bad,built.privateCrosswalk),/DISPLAY_CODE_DISAGREEMENT/);

  // Gate 8: generated private output is covered by the repository ignore policy.
  const ignore=fs.readFileSync(path.join(root,'.gitignore'),'utf8');
  assert.ok(ignore.includes('.cube-rev-private/'));
  assert.ok(ignore.includes('*PRIVATE_CROSSWALK*.json'));

  // Materialize an isolated build to verify writer paths without touching the repository.
  const temp=fs.mkdtempSync(path.join(os.tmpdir(),'cr0809-'));
  const pubBank=path.join(temp,'PARTICIPANT_STIMULUS_BANK_0.8.9.json');
  const pubConfig=path.join(temp,'COGNITIVE_MODE_CONFIG_0.8.9.json');
  const privateFile=path.join(temp,'PRIVATE_CROSSWALK_0.8.9.json');
  const manifest=path.join(temp,'CUBE_REV_0.8.9_BUILD_MANIFEST.json');
  fs.writeFileSync(pubBank,JSON.stringify(built.publicBank));
  fs.writeFileSync(pubConfig,JSON.stringify(built.publicConfig));
  fs.writeFileSync(privateFile,JSON.stringify(built.privateCrosswalk));
  fs.writeFileSync(manifest,JSON.stringify(built.manifest));
  for(const file of [pubBank,pubConfig,privateFile,manifest])assert.ok(fs.statSync(file).size>0);

  console.log('CR0809_PUBLIC_BANK_CERT_PASS 8/8');
})();
