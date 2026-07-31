import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const sourcePath = path.join(root, "index.html");
const outputPath = path.join(root, "calibration", "index.html");
const EXPECTED_SOURCE_SHA256 = "bd8e6d68bf7b50dda2297a849b39e8cb5ba2b484d37d64bf81e94b491c982a1c";
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
  "const BUILD_ID = '0.7.12-neutral-probe-hotfix-1';"
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
