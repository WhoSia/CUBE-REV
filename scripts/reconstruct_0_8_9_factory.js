'use strict';

const fs=require('fs');

function indexCrosswalk(crosswalk){
  if(!crosswalk||crosswalk.classification!=='DO_NOT_DEPLOY_PARTICIPANT_SIDE')throw new Error('PRIVATE_CROSSWALK_REQUIRED');
  const index=new Map();
  for(const stimulus of crosswalk.stimuli||[]){
    for(const [choiceCode,choice] of Object.entries(stimulus.choices||{})){
      const key=`${stimulus.stimulus_id}|${choiceCode}`;
      if(index.has(key))throw new Error(`DUPLICATE_CROSSWALK_KEY:${key}`);
      index.set(key,{
        stimulus_id:stimulus.stimulus_id,
        state_id:stimulus.state_id,
        rotation_id:stimulus.rotation_id,
        choice_display:choice.choice_display,
        choice_canonical:choice.choice_canonical
      });
    }
  }
  return index;
}

function reconstruct(payload,crosswalk){
  if(!payload||payload.version!=='CUBE-REV 0.8.9')throw new Error('PAYLOAD_VERSION_MISMATCH');
  if(payload.response_encoding!=='OPAQUE_CHOICE_CODE_V1')throw new Error('RESPONSE_ENCODING_MISMATCH');
  const index=indexCrosswalk(crosswalk);
  const rows=(payload.responses||[]).map((response,position)=>{
    const key=`${response.stimulus_id}|${response.choice_code}`;
    const resolved=index.get(key);
    if(!resolved)throw new Error(`UNRESOLVED_OPAQUE_CHOICE:${key}`);
    if(resolved.choice_display!==response.choice_display)throw new Error(`DISPLAY_CODE_DISAGREEMENT:${key}`);
    return {
      session_id:payload.session_id,
      participant_token:payload.participant_token,
      sequence_id:payload.sequence_id,
      position:response.position??position+1,
      stimulus_id:response.stimulus_id,
      state_id:resolved.state_id,
      rotation_id:resolved.rotation_id,
      choice_display:response.choice_display,
      choice_canonical:resolved.choice_canonical,
      choice_code:response.choice_code,
      latency_ms:response.latency_ms,
      recorded_at:response.recorded_at
    };
  });
  return {
    schema_version:'CR0809-FACTORY-RECONSTRUCTION-1',
    source_payload_version:payload.version,
    source_session_id:payload.session_id,
    row_count:rows.length,
    rows
  };
}

function main(argv=process.argv.slice(2)){
  if(argv.length<3){
    console.error('usage: node reconstruct_0_8_9_factory.js <payload.json> <private-crosswalk.json> <output.json>');
    process.exit(2);
  }
  const payload=JSON.parse(fs.readFileSync(argv[0],'utf8'));
  const crosswalk=JSON.parse(fs.readFileSync(argv[1],'utf8'));
  const out=reconstruct(payload,crosswalk);
  fs.writeFileSync(argv[2],JSON.stringify(out)+'\n');
  console.log(`CR0809_FACTORY_RECONSTRUCTION_PASS rows=${out.row_count}`);
}

if(require.main===module)main();
module.exports={indexCrosswalk,reconstruct};
