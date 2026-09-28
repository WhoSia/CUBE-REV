import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { canonicalStimulusBytes } from "../dist/kernel.js";

const packet = JSON.parse(readFileSync(new URL("../fixtures/r3-r3-f1-f10.json", import.meta.url)));
const report = [];
for (const fixture of packet.fixtures) {
  const { perm, ori, view, arm } = fixture.input;
  let ts; let rust;
  try { ts = canonicalStimulusBytes(perm, ori, view, arm); } catch (error) { ts = `REFUSE:${error.message}`; }
  try { rust = execFileSync("cargo", ["run", "--quiet", "-p", "cuberev-core", "--bin", "fixture_emit", "--", perm.join(","), ori.join(","), view, arm], { encoding: "utf8" }).trim(); }
  catch (error) { rust = `REFUSE:${String(error.stderr).trim()}`; }
  const tsPid = ts.startsWith("REFUSE:") ? null : createHash("sha256").update(ts, "utf8").digest("hex");
  const rustPid = rust.startsWith("REFUSE:") ? null : createHash("sha256").update(rust, "utf8").digest("hex");
  const pass = fixture.expected === "PASS" ? ts === rust && tsPid === rustPid : ts.startsWith("REFUSE:") && rust.startsWith("REFUSE:");
  report.push({ fixture_id: fixture.fixture_id, expected: fixture.expected, ts, rust, ts_pid_sha256: tsPid, rust_pid_sha256: rustPid, pass });
}
const failed = report.filter((row) => !row.pass);
console.log(JSON.stringify({ packet_id: packet.packet_id, total: report.length, passed: report.length - failed.length, failed: failed.length, rows: report }, null, 2));
if (failed.length) process.exit(1);
