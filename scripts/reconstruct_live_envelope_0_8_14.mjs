import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {createRequire} from 'node:module';

const ROOT=path.resolve(path.dirname(new URL(import.meta.url).pathname),'..');
const require=createRequire(import.meta.url);
require('../js/public-asset-verifier-0.8.13.js');
const M=require('../js/participant-cognitive-mode-0.8.13.js');

const snapshotPath=process.argv[2]||path.join(ROOT,'artifacts/0.8.14/live_synthetic_snapshot.json');
const envelopePath=process.argv[3]||path.join(ROOT,'artifacts/0.8.14/reconstructed_live_envelope.json');
const evidencePath=process.argv[4]||path.join(ROOT,'artifacts/0.8.14/reconstruction_evidence.json');
const EXPECTED={
  snapshot_sha256:'446ab20ec570140f810bcbe91660b089585f1416db5b29852f7bf6946881e2ba',
  envelope_sha256:'6aa9d1e38c88786f1962a5878f87377a4a5fe1e99222a1b9e8c9c285111118e3',
  checksum_fnv1a32:'f795cd8e',
  bytes:21227,
  session_id:'CR-20260802110000-0813a0b0c0d0'
};
function sha(text){return crypto.createHash('sha256').update(text).digest('hex')}
function fnv(text){let h=0x811c9dc5;for(let i=0;i<text.length;i++){h^=text.charCodeAt(i);h=Math.imul(h,0x01000193)}return (h>>>0).toString(16).padStart(8,'0')}
function assertEqual(actual,expected,label){if(actual!==expected)throw new Error(`${label}: expected ${expected}, observed ${actual}`)}

const snapshotText=fs.readFileSync(snapshotPath,'utf8');
const snapshot=JSON.parse(snapshotText);
assertEqual(snapshot.session_id,EXPECTED.session_id,'SNAPSHOT_SESSION');
assertEqual(sha(snapshotText),EXPECTED.snapshot_sha256,'SNAPSHOT_SHA256');
const envelope=M.collectorEnvelopeFromSnapshot(snapshot,{
  generated_at:'2026-08-02T11:00:30.000Z',
  status:'engineering_synthetic_live_cert',
  synthetic_live_cert:true,
  exclude_from_human_cohort:true,
  immutable_snapshot_sha256:EXPECTED.snapshot_sha256
});
const envelopeText=JSON.stringify(envelope);
const observed={
  bytes:Buffer.byteLength(envelopeText),
  envelope_sha256:sha(envelopeText),
  checksum_fnv1a32:fnv(envelopeText),
  session_id:envelope.session_id,
  trial_count:Array.isArray(envelope.trials)?envelope.trials.length:null,
  response_count:Array.isArray(envelope.cognitive_snapshot?.responses)?envelope.cognitive_snapshot.responses.length:null
};
assertEqual(observed.bytes,EXPECTED.bytes,'ENVELOPE_BYTES');
assertEqual(observed.envelope_sha256,EXPECTED.envelope_sha256,'ENVELOPE_SHA256');
assertEqual(observed.checksum_fnv1a32,EXPECTED.checksum_fnv1a32,'ENVELOPE_FNV');
assertEqual(observed.session_id,EXPECTED.session_id,'ENVELOPE_SESSION');
assertEqual(observed.trial_count,28,'TRIAL_COUNT');
assertEqual(observed.response_count,28,'RESPONSE_COUNT');
fs.mkdirSync(path.dirname(envelopePath),{recursive:true});
fs.writeFileSync(envelopePath,envelopeText);
fs.writeFileSync(evidencePath,JSON.stringify({
  schema_version:'CR0814-SUBMITTED-BYTE-RECONSTRUCTION-1',
  source:'deterministic_reconstruction_from_0.8.13_fixed_snapshot_and_runtime',
  expected_live_evidence:EXPECTED,
  observed,
  exact_submitted_bytes_reconstructed:true,
  exact_drive_stored_bytes_retrieved:false,
  custody_class:'T2_SUBMITTED_BYTE_IDENTITY_WITH_COLLECTOR_RECEIPT_NO_DIRECT_DRIVE_READ',
  result:'PASS_SUBMITTED_BYTE_RECONSTRUCTION_HOLD_STORED_RAW_CUSTODY'
},null,2));
console.log(`CR0814_SUBMITTED_BYTE_RECONSTRUCTION_PASS bytes=${observed.bytes} sha256=${observed.envelope_sha256} checksum=${observed.checksum_fnv1a32}`);
