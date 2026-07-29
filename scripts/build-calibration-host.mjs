import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const sourcePath = path.join(root, "index.html");
const outputDir = path.join(root, "calibration");
const outputPath = path.join(outputDir, "index.html");
const expectedBaseline = "ced1836b372e407b328d0863b0bc968cd7d89359d5edfa91da9313989444bb31";
const sourceText = fs.readFileSync(sourcePath, "utf8");
let html = sourceText.replace(/\r\n/g, "\n");
const sha256 = (value) => crypto.createHash("sha256").update(value).digest("hex");

if (sha256(html) !== expectedBaseline) {
  throw new Error("Baseline index.html does not match the verified 0.6.11 source.");
}
function once(search, replacement, label) {
  const first = html.indexOf(search);
  if (first < 0 || html.indexOf(search, first + search.length) >= 0) {
    throw new Error(`Expected exactly one ${label} build anchor.`);
  }
  html = html.replace(search, replacement);
}

once(
  "<title>CUBE-REV 0.6.11 Hidden-scramble State Recovery Pilot</title>",
  "<title>CUBE-REV 0.7.11 Calibration · verified 0.6.11 host</title>",
  "title"
);
once(
  "</style>",
  `.calibrationLock{position:fixed;z-index:1500;left:50%;top:8px;transform:translateX(-50%);display:flex;align-items:center;gap:9px;max-width:calc(100vw - 190px);padding:7px 12px;border:1px solid #755f2d;border-radius:12px;background:rgba(35,28,13,.94);box-shadow:0 10px 28px rgba(0,0,0,.28);color:#ffe4a1;font-size:.76rem;line-height:1.35;backdrop-filter:blur(8px)}.calibrationLock strong{white-space:nowrap}.calibrationLock code{color:#ffd56a}@media(max-width:720px){.calibrationLock{position:relative;left:auto;top:auto;transform:none;max-width:none;margin:7px 7px 0;font-size:.68rem}.languageDock{top:58px}}\n</style>`,
  "style terminator"
);
once(
  "<body>",
  `<body>\n<div class="calibrationLock" role="status" data-testid="calibration-lock"><strong>0.7.11 CALIBRATION</strong><span>Run-in only · collection locked · eligibility clock <code>NOT_STARTED</code></span></div>`,
  "body"
);

const collectorBlock = /window\.CUBE_REV_COLLECTOR_CONFIG = \{\r?\n  enabled: true,[\s\S]*?\r?\n\};\r?\n<\/script>/;
if (!collectorBlock.test(html)) throw new Error("Collector configuration anchor missing.");
html = html.replace(
  collectorBlock,
  `window.CUBE_REV_COLLECTOR_CONFIG = {
  enabled: false,
  endpoint: '',
  manualUploadUrl: '',
  studyId: 'CUBE-REV-0.6.11',
  collectorId: 'CUBE-REV-0711-CALIBRATION-LOCKED',
  protocolVersion: 'receipt-v2',
  autoSubmitOnComplete: false,
  gzipWhenAvailable: true,
  timeoutMs: 45000
};
</script>`
);

once(
  '<script src="./js/i18n-controller.js?v=0611-orbit-ui-1"></script>',
  `<script src="./calibration-config.js?v=0711-source-bound-1"></script>
<script src="./linkage.js?v=0711-source-bound-1"></script>
<script src="./probe-policy.js?v=0711-source-bound-1"></script>
<script src="./eligibility-clock.js?v=0711-source-bound-1"></script>
<script src="./export-decoration.js?v=0711-source-bound-1"></script>
<script src="./runtime.js?v=0711-source-bound-1"></script>
<script src="../js/i18n-controller.js?v=0611-orbit-ui-1"></script>`,
  "controller scripts"
);
html = html
  .replaceAll('src="./js/collector-client.js', 'src="../js/collector-client.js')
  .replaceAll('src="./js/cube-drag-controller.js', 'src="../js/cube-drag-controller.js')
  .replaceAll('src="./js/camera-zoom-controller.js', 'src="../js/camera-zoom-controller.js')
  .replaceAll('src="./js/responsive-layout-controller.js', 'src="../js/responsive-layout-controller.js');

once(
  "const BUILD_ID = '0.6.11-orbit-ui-1';",
  `const BUILD_ID = '0.7.11-source-bound-calibration-1';
const CALIBRATION_PROTOCOL_VERSION = '0.7.11';
const calibrationRuntime = new CubeRevCalibrationRuntime();`,
  "build id"
);

const normalizedCollectorEndpoint =
  /  enabled:true,\n  endpoint:'[^']+',\n  manualUploadUrl:'[^']+',/;
if (!normalizedCollectorEndpoint.test(html)) {
  throw new Error("Normalized collector endpoint anchor missing.");
}
html = html.replace(
  normalizedCollectorEndpoint,
  "  enabled:false,\n  endpoint:'',\n  manualUploadUrl:'',"
);
html = html.replace(
  "  collectorId:'CUBE-REV-0611-MAIN',",
  "  collectorId:'CUBE-REV-0711-CALIBRATION-LOCKED',"
);
html = html.replace(
  "  autoSubmitOnComplete:true",
  "  autoSubmitOnComplete:false"
);

once(
  "  t.scramble_tokens=String(t.scramble).split(/\\s+/).filter(Boolean);return t;",
  "  t.scramble_tokens=String(t.scramble).split(/\\s+/).filter(Boolean);return calibrationRuntime.resolveTrial(t,participant);",
  "trial resolver"
);
once(
  "trials:[],events:[],self_test:window.__CUBEREV_SELFTEST__};",
  "trials:[],events:[],self_test:window.__CUBEREV_SELFTEST__};calibrationRuntime.decorateSession(session);",
  "session decoration"
);
once(
  "function sanitizeSessionForExport(){const {_rng,_plan,_index,_active_started_perf,_hidden_started_perf,...publicSession}=session;const out=structuredClone(publicSession);out.project=PROJECT;out.version=VERSION;out.build_id=BUILD_ID;out.trial_manifest_version=TRIAL_MANIFEST.version;return out;}",
  "function sanitizeSessionForExport(){const {_rng,_plan,_index,_active_started_perf,_hidden_started_perf,...publicSession}=session;const out=structuredClone(publicSession);out.project=PROJECT;out.version=VERSION;out.build_id=BUILD_ID;out.trial_manifest_version=TRIAL_MANIFEST.version;return calibrationRuntime.decorateExport(out);}",
  "export decoration"
);
once(
  "function scheduleAutomaticSubmission(){",
  "function scheduleAutomaticSubmission(){if(!calibrationRuntime.collectionAllowed()){setUploadStatus('0.7.11 run-in: collection is governance-locked. Save JSON locally only.','info');return;}",
  "submission lock"
);
once(
  "  session.trials.push(currentTrialRecord);trialStartPerf=performance.now();",
  "  calibrationRuntime.decorateTrial(currentTrialRecord,trial);session.trials.push(currentTrialRecord);trialStartPerf=performance.now();",
  "trial decoration"
);
once(
  "  document.getElementById('scrambleText').textContent=tr('state.private');updateHUD();\n  logicalState=applyAlg(solvedState(),trial.scramble_tokens);",
  `  document.getElementById('scrambleText').textContent=tr('state.private');updateHUD();
  await calibrationRuntime.presentAssignedHistory(currentTrialRecord,trial,{setText:(text)=>{document.getElementById('scrambleText').textContent=text;},privateLabel:()=>tr('state.private'),setView:(context)=>{camera=context==='reoriented'?{...DEFAULT_CAMERA,yaw:DEFAULT_CAMERA.yaw+Math.PI/2,pitch:DEFAULT_CAMERA.pitch+Math.PI/6}:{...DEFAULT_CAMERA};scheduleDraw();},sleep,log:logSessionEvent});
  logicalState=applyAlg(solvedState(),trial.scramble_tokens);`,
  "history presentation"
);
once(
  "function collectProbe(){\n  return new Promise(resolve=>{",
  "function collectProbe(){\n  calibrationRuntime.prepareProbe(currentTrialRecord);\n  return new Promise(resolve=>{",
  "probe preparation"
);
html = html.replace(
  "const replayLabel=document.querySelector('[data-strategy=\"replay\"]');\n    replayLabel.classList.toggle('hidden',currentTrialRecord.condition==='state_only');",
  "const replayLabel=document.querySelector('[data-strategy=\"direct_inverse\"]');\n    replayLabel?.classList.toggle('hidden',currentTrialRecord.replay_inference_allowed!==true);"
);

html = html.replace(
  "const releaseScripts=[...document.querySelectorAll('script[src^=\"./js/\"]')]",
  "const releaseScripts=[...document.querySelectorAll('script[src^=\"../js/\"]')]"
);
html = html.replace(
  "VERSION==='0.6.11'&&TRIAL_MANIFEST.version===VERSION&&COLLECTOR_CONFIG.studyId===`CUBE-REV-${VERSION}`&&BUILD_ID.startsWith(VERSION+'-')",
  "VERSION==='0.6.11'&&CALIBRATION_PROTOCOL_VERSION==='0.7.11'&&TRIAL_MANIFEST.version===VERSION&&COLLECTOR_CONFIG.studyId===`CUBE-REV-${VERSION}`&&BUILD_ID.startsWith(CALIBRATION_PROTOCOL_VERSION+'-')"
);
html = html.replace(
  "check('collector endpoint embedded',collectorConfigured()&&COLLECTOR_CONFIG.endpoint.includes('/macros/s/')&&COLLECTOR_CONFIG.endpoint.endsWith('/exec'));",
  "check('collector governance lock',!collectorConfigured()&&!COLLECTOR_CONFIG.enabled&&!COLLECTOR_CONFIG.endpoint&&calibrationRuntime.collectionAllowed()===false);check('eligibility clock not started',calibrationRuntime.eligibility.state==='NOT_STARTED'&&!calibrationRuntime.eligibility.activated);"
);

fs.mkdirSync(outputDir, { recursive: true });
fs.writeFileSync(outputPath, html, "utf8");
console.log(JSON.stringify({
  source: path.relative(root, sourcePath),
  output: path.relative(root, outputPath),
  baseline_sha256: expectedBaseline,
  output_sha256: sha256(html)
}, null, 2));
