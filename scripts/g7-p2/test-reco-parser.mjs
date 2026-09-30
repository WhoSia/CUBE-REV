import assert from "node:assert/strict";
import fs from "node:fs";
import { parseRecoIndexHtml, parseRecoSolveHtml } from "./parse-reco-html.mjs";

const solveHtml=fs.readFileSync("scripts/g7-p2/fixtures/reco-14134-minimal.html","utf8");
const r=parseRecoSolveHtml(solveHtml,"https://reco.nz/solve/14134");
assert.equal(r.source_record_id,"14134");
assert.equal(r.solver,"Yiheng Wang");
assert.equal(r.result_text,"3.84");
assert.equal(r.puzzle,"3x3");
assert.equal(r.solve_date,"2026-08-24");
assert.equal(r.competition,"Monkey League Season 6");
assert.equal(r.reconstructor,"Stewy");
assert.ok(r.scramble_raw.startsWith("U R L' F'"));
assert.ok(r.reconstruction_raw.includes("// xcross"));
assert.ok(r.reconstruction_raw.includes("// OLL"));
assert.equal(r.stats.Time.Total,"3.84");
assert.equal(r.stats.STM.Total,"55");
assert.equal(r.video_url,"https://www.youtube.com/embed/bl30ZOMTGL8");

assert.deepEqual(r.average_neighbor_ids,[14098,14133]);

const rendered=solveHtml
  .replace('<iframe src="https://www.youtube.com/embed/bl30ZOMTGL8"></iframe>',
           '<div src="https://www.youtube.com/embed/bl30ZOMTGL8" data-original-tag="iframe"></div>')
  .replace('href="14098"','href="https://reco.nz/solve/14098"')
  .replace('href="14133"','href="https://reco.nz/solve/14133"');
const rr=parseRecoSolveHtml(rendered,"https://reco.nz/solve/14134");
assert.equal(rr.video_url,"https://www.youtube.com/embed/bl30ZOMTGL8");
assert.deepEqual(rr.average_neighbor_ids,[14098,14133]);

const indexHtml=fs.readFileSync("scripts/g7-p2/fixtures/reco-index-minimal.html","utf8");
const idx=parseRecoIndexHtml(indexHtml);
assert.deepEqual(idx.solve_ids,[14133,14134,14147]);
assert.equal(idx.rows.length,3);
assert.equal(idx.rows[0].puzzle,"OH");
assert.equal(idx.rows[1].puzzle,"3x3");
assert.equal(idx.rows[1].method,"CFOP");
assert.equal(idx.rows[1].movecount,55);
assert.equal(idx.rows[1].tps,14.32);
assert.deepEqual(idx.referenced_pages,[2,42]);

console.log("G7_P2_RECO_HTML_PARSER_PASS");
console.log("SOLVE_FIXTURE_ID\t"+r.source_record_id);
console.log("INDEX_FIXTURE_IDS\t"+idx.solve_ids.length);
