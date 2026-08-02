'use strict';

const fs=require('fs');
const path=require('path');
const crypto=require('crypto');

const VERSION='CUBE-REV 0.8.9';
const PUBLIC_SCHEMA='CR0809-PUBLIC-STIMULUS-BANK-1';
const CONFIG_SCHEMA='CR0809-COGNITIVE-MODE-CONFIG-1';
const PRIVATE_SCHEMA='CR0809-PRIVATE-CROSSWALK-1';
const DISPLAY_MOVES=[...['U','R','F','D','L','B'].flatMap(face=>[face,face+'2',face+"'"])];
const FORBIDDEN_PUBLIC_FIELDS=new Set([
  'state_id','rotation_id','face_map','choice_canonical','canonical_move',
  'pair_id','member_id','probe_name','diagnostic_class','branch_count',
  'branch_level','decision_class','distance'
]);

function readJson(file){return JSON.parse(fs.readFileSync(file,'utf8'))}
function writeJson(file,value){fs.mkdirSync(path.dirname(file),{recursive:true});fs.writeFileSync(file,JSON.stringify(value)+'\n')}
function sha256(value){return crypto.createHash('sha256').update(typeof value==='string'?value:JSON.stringify(value)).digest('hex')}
function choiceCode(stimulusId,displayMove){return 'CR9C-'+sha256(`CUBE-REV-0.8.9|${stimulusId}|${displayMove}`).slice(0,16)}
function invertFaceMap(faceMap){
  const inverse={};
  for(const [canonical,display] of Object.entries(faceMap||{})){
    if(inverse[display])throw new Error(`NON_BIJECTIVE_FACE_MAP:${display}`);
    inverse[display]=canonical;
  }
  if(Object.keys(inverse).sort().join('')!=='BDFLRU')throw new Error('INCOMPLETE_FACE_MAP');
  return inverse;
}
function assertNoForbidden(value,trail='$'){
  if(Array.isArray(value)){value.forEach((v,i)=>assertNoForbidden(v,`${trail}[${i}]`));return}
  if(!value||typeof value!=='object')return;
  for(const [key,v] of Object.entries(value)){
    if(FORBIDDEN_PUBLIC_FIELDS.has(key))throw new Error(`FORBIDDEN_PUBLIC_FIELD:${trail}.${key}`);
    assertNoForbidden(v,`${trail}.${key}`);
  }
}
function assertSource(sourceBank,sourceConfig){
  if(!Array.isArray(sourceBank.stimuli)||sourceBank.stimuli.length!==28)throw new Error('SOURCE_STIMULUS_COUNT');
  if(!sourceConfig.schedules||Object.keys(sourceConfig.schedules).length!==24)throw new Error('SOURCE_SEQUENCE_COUNT');
  const ids=new Set(sourceBank.stimuli.map(x=>x.stimulus_id));
  if(ids.size!==28)throw new Error('SOURCE_STIMULUS_ID_DUPLICATE');
  for(const schedule of Object.values(sourceConfig.schedules)){
    if(!Array.isArray(schedule)||schedule.length!==28)throw new Error('SOURCE_SCHEDULE_LENGTH');
    if(new Set(schedule).size!==28||schedule.some(x=>!ids.has(x)))throw new Error('SOURCE_SCHEDULE_MEMBERSHIP');
  }
}
function build(sourceBank,sourceConfig){
  assertSource(sourceBank,sourceConfig);
  const globalCodes=new Set();
  const privateStimuli=[];
  const publicStimuli=sourceBank.stimuli.map(source=>{
    const inverse=invertFaceMap(source.face_map);
    const choiceCodes={};
    const choices={};
    for(const displayMove of DISPLAY_MOVES){
      const suffix=displayMove.slice(1);
      const canonicalMove=inverse[displayMove[0]]+suffix;
      const code=choiceCode(source.stimulus_id,displayMove);
      if(globalCodes.has(code))throw new Error(`CHOICE_CODE_COLLISION:${code}`);
      globalCodes.add(code);
      choiceCodes[displayMove]=code;
      choices[code]={choice_display:displayMove,choice_canonical:canonicalMove};
    }
    privateStimuli.push({
      stimulus_id:source.stimulus_id,
      state_id:source.state_id,
      rotation_id:source.rotation_id,
      face_map:source.face_map,
      choices
    });
    return {stimulus_id:source.stimulus_id,stickers:source.stickers,choice_codes:choiceCodes};
  });
  const publicBank={
    schema_version:PUBLIC_SCHEMA,
    version:VERSION,
    blinding:'OPAQUE_STIMULUS_AND_CHOICE_CODES',
    response_encoding:'OPAQUE_CHOICE_CODE_V1',
    forbidden_public_fields:[...FORBIDDEN_PUBLIC_FIELDS].sort(),
    stimuli:publicStimuli
  };
  assertNoForbidden(publicBank);
  const publicConfig={
    schema_version:CONFIG_SCHEMA,
    version:VERSION,
    mode_id:'COG-MODE-001',
    participant_route:'participant-cognitive-mode-0.8.9.html',
    assignment:{method:'stable_hash_mod_24',sequence_count:24,sequence_ids_hidden:true},
    resume:{
      storage_key:'cube-rev-cognitive-mode-0809-v1',
      quarantine_key:'cube-rev-cognitive-mode-0809-quarantine-v1',
      telemetry_persisted:true,
      immutable_submission_snapshot:true
    },
    collector:{files_modified:false,collector_contract_version:'0.7.12',app_payload_version:VERSION},
    participant_ui:{
      legacy_fixed_set_selector:'retired',sample_size_language:'forbidden',
      diagnostic_identifiers:'absent',canonical_moves:'absent',post_task_demand_check:true
    },
    schedules:sourceConfig.schedules
  };
  const privateCrosswalk={
    schema_version:PRIVATE_SCHEMA,
    version:VERSION,
    classification:'DO_NOT_DEPLOY_PARTICIPANT_SIDE',
    source_bank_schema:sourceBank.schema_version,
    stimuli:privateStimuli
  };
  const manifest={
    schema_version:'CR0809-BUILD-MANIFEST-1',version:VERSION,
    public_bank_sha256:sha256(publicBank),
    public_config_sha256:sha256(publicConfig),
    private_crosswalk_sha256:sha256(privateCrosswalk),
    stimulus_count:publicStimuli.length,
    sequence_count:Object.keys(publicConfig.schedules).length,
    choice_code_count:globalCodes.size,
    forbidden_public_fields:[...FORBIDDEN_PUBLIC_FIELDS].sort()
  };
  return {publicBank,publicConfig,privateCrosswalk,manifest};
}

function main(argv=process.argv.slice(2)){
  const root=path.resolve(__dirname,'..');
  const sourceBankPath=path.resolve(argv[0]||path.join(root,'cognitive/PARTICIPANT_STIMULUS_BANK_0.8.8.json'));
  const sourceConfigPath=path.resolve(argv[1]||path.join(root,'cognitive/COGNITIVE_MODE_CONFIG_0.8.8.json'));
  const publicBankPath=path.resolve(argv[2]||path.join(root,'cognitive/PARTICIPANT_STIMULUS_BANK_0.8.9.json'));
  const publicConfigPath=path.resolve(argv[3]||path.join(root,'cognitive/COGNITIVE_MODE_CONFIG_0.8.9.json'));
  const privatePath=path.resolve(argv[4]||path.join(root,'.cube-rev-private/PRIVATE_CROSSWALK_0.8.9.json'));
  const manifestPath=path.resolve(argv[5]||path.join(root,'research/CUBE_REV_0.8.9_BUILD_MANIFEST.json'));
  const out=build(readJson(sourceBankPath),readJson(sourceConfigPath));
  writeJson(publicBankPath,out.publicBank);
  writeJson(publicConfigPath,out.publicConfig);
  writeJson(privatePath,out.privateCrosswalk);
  writeJson(manifestPath,out.manifest);
  console.log(`CR0809_PUBLIC_BANK_BUILD_PASS stimuli=${out.manifest.stimulus_count} choices=${out.manifest.choice_code_count}`);
}

if(require.main===module)main();
module.exports={VERSION,DISPLAY_MOVES,FORBIDDEN_PUBLIC_FIELDS,choiceCode,invertFaceMap,assertNoForbidden,build};
