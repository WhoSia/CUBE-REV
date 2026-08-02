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
    source_commit:'70e68aa2a768972d31882e0f1c2a483cfd9ca9bc'
  },
  'final-0.8.13-head':{
    snapshot_sha256:'5fbf313d1a81bc7d94820da42a588e94cccba5aa14c287316cf548175ef82f83',
    envelope_sha256:'6aa9d1e38c88786f1962a5878f87377a4a5fe1e99222a1b9e8c9c285111118e3',
    checksum_fnv1a32:'f795cd8e',bytes:21227,
    source_commit:'6c127f86704b29ed4d884acc19a28407578753c2'
  }
}[runtimeClass];
if(!EXPECTED)throw new Error(`RUNTIME_CLASS_UNKNOWN:${runtimeClass}`);
const requireFromRuntime=createRequire(path.join(runtimeRoot,'package.json'));
requireFromRuntime(path.join(runtimeRoot,'js/public-asset-verifier-0.8.13.js'));
const M=requireFromRuntime(path.join(runtimeRoot,'js/participant-cognitive-mode-0.8.13.js'));
const SESSION='CR-20260802110000-0813a0b0c0d0';
function sha(text){return crypto.createHash('sha256').update(text).digest('hex')}
function fnv(text){let h=0x811c9dc5;for(let i=0;i<text.length;i++){h^=text.charCodeAt(i);h=Math.imul(h,0x01000193)}return (h>>>0).toString(16).padStart(8,'0')}
function assertEqual(actual,expected,label){if(actual!==expected)throw new Error(`${label}: expected ${expected}, observed ${actual}`)}

const snapshotText=fs.readFileSync(snapshotPath,'utf8');
const snapshot=JSON.parse(snapshotText);
assertEqual(snapshot.session_id,SESSION,'SNAPSHOT_SESSION');
assertEqual(sha(snapshotText),EXPECTED.snapshot_sha256,'SNAPSHOT_SHA256');
const envelope=M.collectorEnvelopeFromSnapshot(snapshot,{
  generated_at:'2026-08-02T11:00:30.000Z',
  status:'engineering_synthetic_live_cert',
  synthetic_live_cert:true,
  exclude_from_human_cohort:true,
  immutable_snapshot_sha256:EXPECTED.snapshot_sha256
});
const envelopeText=JSON.stringify(envelope);
const observed={runtime_class:runtimeClass,runtime_root:runtimeRoot,source_commit:EXPECTED.source_commit,bytes:Buffer.byteLength(envelopeText),envelope_sha256:sha(envelopeText),checksum_fnv1a32:fnv(envelopeText),snapshot_raw_sha256:sha(snapshotText),embedded_snapshot_sha256:sha(JSON.stringify(envelope.cognitive_snapshot)),session_id:envelope.session_id,trial_count:Array.isArray(envelope.trials)?envelope.trials.length:null,response_count:Array.isArray(envelope.cognitive_snapshot?.responses)?envelope.cognitive_snapshot.responses.length:null};
assertEqual(observed.bytes,EXPECTED.bytes,'ENVELOPE_BYTES');
assertEqual(observed.envelope_sha256,EXPECTED.envelope_sha256,'ENVELOPE_SHA256');
assertEqual(observed.checksum_fnv1a32,EXPECTED.checksum_fnv1a32,'ENVELOPE_FNV');
assertEqual(observed.session_id,SESSION,'ENVELOPE_SESSION');
assertEqual(observed.trial_count,28,'TRIAL_COUNT');
assertEqual(observed.response_count,28,'RESPONSE_COUNT');
fs.mkdirSync(path.dirname(envelopePath),{recursive:true});
fs.writeFileSync(envelopePath,envelopeText);
fs.writeFileSync(evidencePath,JSON.stringify({schema_version:'CR0814-RUNTIME-PINNED-ENVELOPE-RECONSTRUCTION-1',runtime_class:runtimeClass,expected:EXPECTED,observed,exact_runtime_pinned_bytes_reconstructed:true,exact_drive_stored_bytes_retrieved:false,result:runtimeClass==='archival-live-head'?'PASS_ARCHIVAL_LIVE_SUBMITTED_BYTE_RECONSTRUCTION':'PASS_FINAL_RUNTIME_COUNTERFACTUAL_RECONSTRUCTION'},null,2));
console.log(`CR0814_RUNTIME_PINNED_RECONSTRUCTION_PASS class=${runtimeClass} bytes=${observed.bytes} sha256=${observed.envelope_sha256} checksum=${observed.checksum_fnv1a32} embedded_snapshot_sha256=${observed.embedded_snapshot_sha256}`);
