'use strict';
const fs=require('fs');
const path=require('path');
const crypto=require('crypto');

const VERSION='CUBE-REV 0.8.13';
const ROOT=path.resolve(__dirname,'..');
const read=p=>JSON.parse(fs.readFileSync(path.join(ROOT,p),'utf8'));
const canonical=x=>JSON.stringify(x);
const sha=x=>crypto.createHash('sha256').update(typeof x==='string'?x:canonical(x)).digest('hex');
const write=(p,x)=>{const full=path.join(ROOT,p);fs.mkdirSync(path.dirname(full),{recursive:true});fs.writeFileSync(full,typeof x==='string'?x:canonical(x));};

const parentBank=read('cognitive/PARTICIPANT_STIMULUS_BANK_0.8.12.json');
const parentConfig=read('cognitive/COGNITIVE_MODE_CONFIG_0.8.12.json');
const parentManifest=read('research/CUBE_REV_0.8.12_ASSET_MANIFEST.json');
const parentManifestHash=sha(parentManifest);
const parentBankHash=sha(parentBank);
const parentConfigHash=sha(parentConfig);
const privateCrosswalk=parentManifest.private_crosswalk_sha256;

if(parentManifestHash!=='c9abbf5c1057bb0e02795fc0d3ab1095c9ce115943b1f89cb825ac8a9ed35af6')throw new Error('PARENT_0812_MANIFEST_IDENTITY');
if(parentBankHash!=='fc76841350cd8937e576c701995ff64bcfbc02f6f7b50977b8946f8299a712a8')throw new Error('PARENT_0812_BANK_IDENTITY');
if(parentConfigHash!=='1d04467c3ad2390f2e9784973bd026c1b77b8a72919fedd09070ff048b6d0701')throw new Error('PARENT_0812_CONFIG_IDENTITY');

const bank={
  ...parentBank,
  schema_version:'CR0813-PUBLIC-STIMULUS-BANK-1',
  version:VERSION,
  source_bundle:{
    version:'CUBE-REV 0.8.12',
    manifest_sha256:parentManifestHash,
    public_bank_sha256:parentBankHash,
    public_config_sha256:parentConfigHash,
    opaque_choice_code_count:504
  }
};

const config=JSON.parse(JSON.stringify(parentConfig));
config.schema_version='CR0813-COGNITIVE-MODE-CONFIG-1';
config.version=VERSION;
config.participant_route='participant-cognitive-mode-0.8.13.html';
config.resume={
  ...config.resume,
  storage_key:'cube-rev-cognitive-mode-0813-v1',
  quarantine_key:'cube-rev-cognitive-mode-0813-quarantine-v1',
  active_write_lock_name:'cube-rev-session-write-0813-exclusive-v1',
  active_write_journal_key:'cube-rev-session-write-0813-journal-v1',
  active_write_conflict_key:'cube-rev-session-write-0813-conflicts-v1',
  native_browser_evidence_key:'cube-rev-native-browser-0813-evidence-v1'
};
config.collector={...config.collector,files_modified:false,collector_contract_version:'0.7.12',app_payload_version:VERSION};
config.active_session={
  parent_version:'CUBE-REV 0.8.12',
  parent_storage_key:'cube-rev-cognitive-mode-0812-v1',
  parent_asset_binding:{
    manifest_sha256:parentManifestHash,
    public_bank_sha256:parentBankHash,
    public_config_sha256:parentConfigHash,
    private_crosswalk_sha256:privateCrosswalk
  },
  operation_dispatcher:'REVISION_CAS_OPERATION_DISPATCHER_V2_NATIVE_BROWSER',
  revision_policy:'STRICT_MONOTONIC_INCREMENT_BY_ONE_V1',
  scientific_write_policy:'EXPECTED_REVISION_REQUIRED_V1',
  stale_write_policy:'REJECT_WITHOUT_STATE_MUTATION_V1',
  response_conflict_policy:'ONE_WINNER_QUARANTINE_LOSER_EVIDENCE_V1',
  telemetry_policy:'LOCKED_APPEND_MERGE_ON_LATEST_REVISION_V1',
  snapshot_policy:'IMMUTABLE_SCIENTIFIC_ENVELOPE_RETRY_STABLE_V3',
  submission_policy:'LEASE_TOKEN_SINGLE_NETWORK_OWNER_V1',
  collector_metadata_policy:'LEASE_AUTHORIZED_AUXILIARY_MERGE_V1',
  lease_timeout_ms:120000,
  mutation_history_limit:256,
  conflict_history_limit:64,
  source_state_preserved:true,
  sealed_parent_policy:'PARENT_VERSION_RETRY_ONLY',
  native_browser_contract:'TWO_PAGE_SAME_ORIGIN_WEB_LOCKS_STORAGE_EVENT_V1',
  delayed_network_contract:'TWO_NONCE_SAME_SNAPSHOT_RECEIPT_DEDUP_V1',
  factory_adapter_contract:'CR0813_COGNITIVE_SNAPSHOT_FACTORY_ADAPTER_V1'
};
config.factory={
  raw_snapshot_immutable:true,
  adapter:'CR0813_COGNITIVE_SNAPSHOT_FACTORY_ADAPTER_V1',
  expected_payload_schema:'CR0813-COLLECTOR-PAYLOAD-1',
  expected_response_count:28,
  output_tables:['session_table.csv','trial_table.csv','telemetry_table.csv','qc_report.csv'],
  manifest_required:true
};

const bankHash=sha(bank);
const configHash=sha(config);
const manifest={
  schema_version:'CR0813-ASSET-MANIFEST-1',
  version:VERSION,
  canonicalization:'JSON_STRINGIFY_PARSED_OBJECT_V1',
  hash_algorithm:'SHA-256',
  public_bank_path:'cognitive/PARTICIPANT_STIMULUS_BANK_0.8.13.json',
  public_config_path:'cognitive/COGNITIVE_MODE_CONFIG_0.8.13.json',
  public_bank_sha256:bankHash,
  public_config_sha256:configHash,
  parent_manifest_sha256:parentManifestHash,
  parent_public_bank_sha256:parentBankHash,
  parent_public_config_sha256:parentConfigHash,
  private_crosswalk_sha256:privateCrosswalk,
  response_encoding:'OPAQUE_CHOICE_CODE_V1',
  stimulus_count:28,
  sequence_count:24,
  choice_code_count:504,
  active_session_serialization:'NATIVE_WEB_LOCKS_EXCLUSIVE_REVISION_CAS_V2',
  response_conflict_control:'ONE_WINNER_STALE_WRITE_REJECT_V1',
  submission_serialization:'LEASE_TOKEN_SINGLE_NETWORK_OWNER_V1',
  native_browser_evidence:'PLAYWRIGHT_CHROMIUM_TWO_PAGE_SAME_CONTEXT_V1',
  delayed_network_evidence:'CONTROLLED_RECEIPT_V2_TWO_NONCE_V1',
  factory_reconstruction:'CR0813_COGNITIVE_SNAPSHOT_FACTORY_ADAPTER_V1'
};
const manifestHash=sha(manifest);
const pins={
  schema_version:'CR0813-ASSET-PINS-1',version:VERSION,
  manifest_sha256:manifestHash,public_bank_sha256:bankHash,public_config_sha256:configHash,
  parent_manifest_sha256:parentManifestHash,private_crosswalk_sha256:privateCrosswalk
};
const pinModule=`(function(g){'use strict';const p=${canonical(pins)};if(typeof module!=='undefined'&&module.exports)module.exports=p;g.CUBE_REV_ASSET_PINS_0813=p;})(typeof window!=='undefined'?window:globalThis);\n`;

write('cognitive/PARTICIPANT_STIMULUS_BANK_0.8.13.json',bank);
write('cognitive/COGNITIVE_MODE_CONFIG_0.8.13.json',config);
write('research/CUBE_REV_0.8.13_ASSET_MANIFEST.json',manifest);
write('js/asset-pins-0.8.13.js',pinModule);
console.log(`CR0813_ASSET_BUILD_PASS stimuli=${bank.stimuli.length} choices=${bank.stimuli.reduce((n,s)=>n+Object.keys(s.choice_codes||{}).length,0)} manifest=${manifestHash}`);
