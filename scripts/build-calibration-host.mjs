import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const sourcePath = path.join(root, "index.html");
const outputPath = path.join(root, "calibration", "index.html");
const EXPECTED_SOURCE_SHA256 = "e6e66bb489fc0c814a431c7d24c3d067363162393317e773abdec1377877d7cf";
const sha256 = value => crypto.createHash("sha256").update(value).digest("hex");

const source = fs.readFileSync(sourcePath, "utf8").replace(/\r\n/g, "\n");
const actual = sha256(source);
if (actual !== EXPECTED_SOURCE_SHA256) {
  throw new Error(`Source-bound 0.7.12 host mismatch: expected ${EXPECTED_SOURCE_SHA256}, received ${actual}`);
}

let host = source;
const requiredAnchors = [
  '<script src="./calibration/calibration-config.js',
  '<script src="./calibration/randomization.js',
  '<script src="./calibration/history-presentation.js',
  '<script src="./calibration/neutral-probe.js',
  '<script src="./collector-config.js',
  '<script src="./js/camera-orbit.js',
  "const VERSION = '0.7.12';",
  "const BUILD_ID = '0.7.12-camera-neutral-bypass-hotfix-1';"
];
for (const anchor of requiredAnchors) {
  if (!host.includes(anchor)) throw new Error(`Source-bound anchor missing: ${anchor}`);
}

host = host
  .replaceAll('src="./collector-config.js', 'src="../collector-config.js')
  .replaceAll('src="./calibration/', 'src="./')
  .replaceAll('src="./js/', 'src="../js/');

fs.writeFileSync(outputPath, host, "utf8");
console.log(JSON.stringify({
  source: path.relative(root, sourcePath),
  output: path.relative(root, outputPath),
  source_sha256: actual,
  output_sha256: sha256(host)
}, null, 2));
