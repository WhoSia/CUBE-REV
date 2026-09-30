import assert from "node:assert/strict";
import fs from "node:fs";
import { spawnSync } from "node:child_process";

const policy=JSON.parse(fs.readFileSync("g7/p2/reco-acquisition-policy.json","utf8"));
assert.equal(policy.bulk_authorized,false);
assert.equal(policy.max_solves_per_run,10);
assert.ok(policy.min_delay_ms>=2000);
assert.equal(policy.preserve_raw_html,true);

const dry=spawnSync(process.execPath,[
  "scripts/g7-p2/acquire-reco.mjs",
  "--pages","1","--max-solves","5"
],{encoding:"utf8"});
assert.equal(dry.status,0,dry.stderr);
assert.match(dry.stdout,/G7_P2_RECO_ACQUISITION_DRY_RUN/);
assert.match(dry.stdout,/EXECUTION\tREFUSED_WITHOUT_--execute/);

const tooMany=spawnSync(process.execPath,[
  "scripts/g7-p2/acquire-reco.mjs",
  "--pages","1","--max-solves","11"
],{encoding:"utf8"});
assert.notEqual(tooMany.status,0);
assert.match(tooMany.stderr,/RECO_SOLVE_LIMIT/);

const tooFast=spawnSync(process.execPath,[
  "scripts/g7-p2/acquire-reco.mjs",
  "--pages","1","--max-solves","1","--delay-ms","100"
],{encoding:"utf8"});
assert.notEqual(tooFast.status,0);
assert.match(tooFast.stderr,/RECO_DELAY_TOO_LOW/);

console.log("G7_P2_RECO_ACQUISITION_POLICY_PASS");
