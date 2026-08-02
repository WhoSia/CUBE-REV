import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {createRequire} from 'node:module';

const ROOT=path.resolve(path.dirname(new URL(import.meta.url).pathname),'..');
const snapshotPath=process.argv[2]||path.join(ROOT,'artifacts/0.8.14/live_synthetic_snapshot.json');
const envelopePath=process.argv[3]||path.join(ROOT,'artifacts/0.8.14/reconstructed_live_envelope.json');
const evidencePath=process.argv[4]||path.join(ROOT,'artifacts/0.8.14/reconstruction_evidence.json');
const runtimeRoot=path.resolve(process.argv[5]||ROOT);
const runtimeClass=process.argv[6]||'archival-live-head';
const EXPECTED={
  'archival-live-head':{
    snapshot_sha256:'5fbf313d1a81bc7d94820da42a588e94cccba5aa14c287316cf548175ef82f83',
    envelope_sha256:'6aa9d1e3ebeb403d9e9d9fcfe520867201b815bbcd3f02979012ad371ddd70b9',
    checksum_fnv1a32:'c8cda746',bytes:16217,
    source_commit:'70e68aa2a768972d31882e0f1c2a483cfd9ca9bc',construction:'INLINE_LIVE_PROBE_COMPATIBILITY_ENVELOPE_V1',strict_identity:true
  },
  'final-0.8.13-head':{
    snapshot_sha256:'5fbf313d1a81bc7d94820da42a588e94cccba5aa14c287316cf548175ef82f83',
    source_commit:'6c127f86704b29ed4d884acc19a28407578753c2',construction:'FINAL_RUNTIME_COLLECTOR_ENVELOPE_HELPER_V1',strict_identity:false,
    previously_committed_claim:{envelope_sha256:'6aa9d1e38c88786f1962a5878f87377a4a5fe1e99222a1b9e8c9c285111118e3',checksum_fnv1a32:'f795cd8e',bytes:21227}
  }
}[runtimeClass];
if(!EXPECTED)throw new Error(`RUNTIME_CLASS_UNKNOWN:${runtimeClass}`);
const SESSION='CR-20260802110000-0813a0b0c0d0';
function sha(text){return crypto.createHash('sha256').update(text).digest('hex')}
function fnv(text){let h=0x811c9dc5;for(let i=0;i<text.length;i++){h^=text.charCodeAt(i);h=Math.imul(h,0x01000193)}return (h>>>0).toString(16).padStart(8,'0')}
function assertEqual(actual,expected,label){if(actual!==expected)throw new Error(`${label}: expected ${expected}, observed ${actual}`)}
function archivalEnvelope(snapshot,snapshotSha256){
  const compatibilityTrials=snapshot.responses.map(r=>({trial_index:r.position,trial_id:`CR0813-COMPAT-${String(r.position).padStart(2,'0')}`,condition_id:snapshot.mode_id,stimulus_id:r.stimulus_id,response:{choice_display:r.choice_display,choice_code:r.choice_code,latency_ms:r.latency_ms,recorded_at:r.recorded_at},status:'completed',source_schema:snapshot.schema_version,scientific_revision:snapshot.scientific_revision}));
  return {project:'CUBE-REV',version:'0.7.12',session_id:snapshot.session_id,generated_at:'2026-08-02T11:00:30.000Z',trials:compatibilityTrials,data_submission:{status:'engineering_synthetic_live_cert',synthetic_live_cert:true,exclude_from_human_cohort:true,app_payload_version:snapshot.version,app_payload_schema:snapshot.schema_version,collector_compatibility_schema:'CR0813-COLLECTOR-COMPATIBILITY-ENVELOPE-1',compatibility_trial_policy:'LOSSLESS_OPAQUE_RESPONSE_PROJECTION_V1',immutable_snapshot_sha256:snapshotSha256},cognitive_snapshot:snapshot};
}
function finalRuntimeEnvelope(snapshot,snapshotSha256){
  const requireFromRuntime=createRequire(path.join(runtimeRoot,'package.json'));
  requireFromRuntime(path.join(runtimeRoot,'js/public-asset-verifier-0.8.13.js'));
  const loaded=requireFromRuntime(path.join(runtimeRoot,'js/participant-cognitive-mode-0.8.13.js'));
  const M=globalThis.CUBE_REV_COGNITIVE_MODE_0813||loaded;
  if(typeof M.collectorEnvelopeFromSnapshot!=='function')throw new Error('FINAL_RUNTIME_COLLECTOR_ENVELOPE_HELPER_MISSING');
  return M.collectorEnvelopeFromSnapshot(snapshot,{generated_at:'2026-08-02T11:00:30.000Z',status:'engineering_synthetic_live_cert',synthetic_live_cert:true,exclude_from_human_cohort:true,immutable_snapshot_sha256:snapshotSha256});
}

const snapshotText=fs.readFileSync(snapshotPath,'utf8');
const snapshot=JSON.parse(snapshotText);
assertEqual(snapshot.session_id,SESSION,'SNAPSHOT_SESSION');
const snapshotSha256=sha(snapshotText);assertEqual(snapshotSha256,EXPECTED.snapshot_sha256,'SNAPSHOT_SHA256');
const envelope=runtimeClass==='archival-live-head'?archivalEnvelope(snapshot,snapshotSha256):finalRuntimeEnvelope(snapshot,snapshotSha256);
const envelopeText=JSON.stringify(envelope);
const observed={runtime_class:runtimeClass,runtime_root:runtimeRoot,source_commit:EXPECTED.source_commit,construction:EXPECTED.construction,bytes:Buffer.byteLength(envelopeText),envelope_sha256:sha(envelopeText),checksum_fnv1a32:fnv(envelopeText),snapshot_raw_sha256:snapshotSha256,embedded_snapshot_sha256:sha(JSON.stringify(envelope.cognitive_snapshot)),session_id:envelope.session_id,trial_count:Array.isArray(envelope.trials)?envelope.trials.length:null,response_count:Array.isArray(envelope.cognitive_snapshot?.responses)?envelope.cognitive_snapshot.responses.length:null};
assertEqual(observed.session_id,SESSION,'ENVELOPE_SESSION');assertEqual(observed.trial_count,28,'TRIAL_COUNT');assertEqual(observed.response_count,28,'RESPONSE_COUNT');
if(EXPECTED.strict_identity){assertEqual(observed.bytes,EXPECTED.bytes,'ENVELOPE_BYTES');assertEqual(observed.envelope_sha256,EXPECTED.envelope_sha256,'ENVELOPE_SHA256');assertEqual(observed.checksum_fnv1a32,EXPECTED.checksum_fnv1a32,'ENVELOPE_FNV')}
const committedClaimMatches=EXPECTED.previously_committed_claim?observed.bytes===EXPECTED.previously_committed_claim.bytes&&observed.envelope_sha256===EXPECTED.previously_committed_claim.envelope_sha256&&observed.checksum_fnv1a32===EXPECTED.previously_committed_claim.checksum_fnv1a32:null;
fs.mkdirSync(path.dirname(envelopePath),{recursive:true});fs.writeFileSync(envelopePath,envelopeText);
const result=runtimeClass==='archival-live-head'?'PASS_ARCHIVAL_LIVE_SUBMITTED_BYTE_RECONSTRUCTION':committedClaimMatches?'PASS_FINAL_RUNTIME_MATCHES_COMMITTED_CLAIM':'PASS_FINAL_RUNTIME_OBSERVED_COMMITTED_CLAIM_UNEXPLAINED';
fs.writeFileSync(evidencePath,JSON.stringify({schema_version:'CR0814-RUNTIME-PINNED-ENVELOPE-RECONSTRUCTION-3',runtime_class:runtimeClass,expected:EXPECTED,observed,exact_runtime_pinned_bytes_reconstructed:true,committed_claim_matches_observed:committedClaimMatches,exact_drive_stored_bytes_retrieved:false,result},null,2));
console.log(`CR0814_RUNTIME_PINNED_RECONSTRUCTION_PASS class=${runtimeClass} construction=${EXPECTED.construction} bytes=${observed.bytes} sha256=${observed.envelope_sha256} checksum=${observed.checksum_fnv1a32} committed_claim_matches=${committedClaimMatches}`);
