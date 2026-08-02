'use strict';
const fs=require('fs');
const path=require('path');
const crypto=require('crypto');
const M=require('../js/participant-cognitive-mode-0.8.13.js');
const root=path.resolve(__dirname,'..');
const config=JSON.parse(fs.readFileSync(path.join(root,'cognitive/COGNITIVE_MODE_CONFIG_0.8.13.json'),'utf8'));
const bankDoc=JSON.parse(fs.readFileSync(path.join(root,'cognitive/PARTICIPANT_STIMULUS_BANK_0.8.13.json'),'utf8'));
const pins=require('../js/asset-pins-0.8.13.js');
const bank=Object.fromEntries(bankDoc.stimuli.map(x=>[x.stimulus_id,x]));
const participantToken='CR0813-LIVE-CERT-PARTICIPANT-DO-NOT-ANALYZE-0001';
const sessionId='CR-20260802110000-0813a0b0c0d0';
const sequenceId=M.sequenceId(participantToken),schedule=config.schedules[sequenceId];
const base=Date.parse('2026-08-02T11:00:00.000Z');
const responses=schedule.map((stimulusId,i)=>({stimulus_id:stimulusId,choice_display:'U',choice_code:bank[stimulusId].choice_codes.U,latency_ms:100+i,position:i+1,recorded_at:new Date(base+(i+1)*1000).toISOString()}));
const state=M.seal({
  schema_version:M.SCHEMA,version:M.VERSION,mode_id:config.mode_id,participant_token:participantToken,
  session_id:sessionId,sequence_id:sequenceId,schedule:[...schedule],cursor:28,responses,
  telemetry:[{event_id:'CR0813-LIVE-CERT-EVENT-1',type:'ENGINEERING_SYNTHETIC_SESSION',at:new Date(base).toISOString(),data:{synthetic_live_cert:true,exclude_from_human_analysis:true,exclude_from_human_cohort:true,certificate:'CUBE-REV-0.8.13'}}],
  post_task:{hypothesis_guess:'engineering synthetic collector and factory certification',confidence:100,deliberate_strategy_change:false,technical_notes:'SYNTHETIC LIVE CERTIFICATION — DO NOT INCLUDE IN HUMAN COHORT OR SCIENTIFIC ESTIMATION'},
  submission_snapshot:null,submission_snapshot_hash:null,snapshot_sealed_at:null,status:'READY_TO_SUBMIT',created_at:new Date(base).toISOString(),updated_at:new Date(base+29000).toISOString(),submitted_at:null,submission_receipt:null,
  revision:1,mutation_history:[{mutation_id:'CR0813-LIVE-CERT-FIXTURE',type:'SYNTHETIC_FIXTURE',from_revision:0,to_revision:1,at:new Date(base+29000).toISOString(),outcome:'APPLIED'}],
  conflict_count:0,submission_control:M.emptySubmissionControl(),asset_binding:{manifest_sha256:pins.manifest_sha256,public_bank_sha256:pins.public_bank_sha256,public_config_sha256:pins.public_config_sha256,private_crosswalk_sha256:pins.private_crosswalk_sha256},
  upgrade_epoch:0,migration_provenance:null,active_session_provenance:{source_version:'CUBE-REV 0.8.12',source_schema:'CR0812-RESUME-STATE-1',source_storage_key:'cube-rev-cognitive-mode-0812-v1',source_integrity:'synthetic-fixture-do-not-analyze',source_revision:1,migrated_at:new Date(base).toISOString(),policy:'SYNTHETIC_CERT_FIXTURE_EXCLUDE_FROM_HUMAN_COHORT_V1'}
});
if(!M.valid(state,config,state.asset_binding))throw new Error('SYNTHETIC_STATE_INVALID');
const snapshot=M.scientificEnvelope(state);
const out=process.argv[2]||path.join(root,'artifacts/0.8.13/live_synthetic_snapshot.json');
fs.mkdirSync(path.dirname(out),{recursive:true});
fs.writeFileSync(out,JSON.stringify(snapshot));
const hash=crypto.createHash('sha256').update(JSON.stringify(snapshot)).digest('hex');
console.log(`CR0813_SYNTHETIC_SNAPSHOT_PASS session=${snapshot.session_id} responses=${snapshot.responses.length} sha256=${hash} excluded_from_human_cohort=true`);
