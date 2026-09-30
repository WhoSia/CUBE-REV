import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";

const root=fs.mkdtempSync(path.join(os.tmpdir(),"g7-p2-census-validator-"));
const raw=path.join(root,"raw","index");
const derived=path.join(root,"derived");
fs.mkdirSync(raw,{recursive:true});
fs.mkdirSync(derived,{recursive:true});

fs.writeFileSync(path.join(raw,"page-0001.html"),"<html>fixture</html>");
fs.writeFileSync(path.join(derived,"index-rows.jsonl"),JSON.stringify({id:3,index_page:1})+"\n");
fs.writeFileSync(path.join(derived,"execution.log"),[
  "G7_P2_RECO_INDEX_CENSUS_PASS",
  "PAGES\t1",
  "ROWS\t1",
  "UNIQUE_IDS\t1",
  "TERMINAL_REASON\tSHORT_PAGE",
  "SOLVE_BODY_REQUESTS\t0"
].join("\n")+"\n");

const census={
  schema_version:"g7-p2-reco-index-census-1",
  source_id:"reco_nz",
  scope:"INDEX_ONLY_NO_SOLVE_BODY_FETCH",
  robots_check:"ABSENT_404",
  terminal_reason:"SHORT_PAGE",
  pages_fetched:1,
  row_count:1,
  unique_id_count:1,
  duplicate_id_groups:[],
  duplicate_content_candidates:[],
  id_range:{min:3,max:3,missing_count:0,missing_ids:[]},
  date_range:{min:"2013-08-09",max:"2013-08-09"},
  puzzle_counts:{"3x3":1},
  method_counts:{"CFOP":1},
  solver_counts:{"Fixture Solver":1},
  reconstructor_counts:{"fixture":1},
  page_receipts:[{page:1,row_count:1}]
};
fs.writeFileSync(path.join(derived,"census.json"),JSON.stringify(census,null,2)+"\n");

const validator=path.resolve("scripts/g7-p2/validate-reco-index-census.mjs");
const pass=spawnSync(process.execPath,[validator,root],{encoding:"utf8"});
if(pass.status!==0) throw new Error("VALIDATOR_PASS_FIXTURE_FAILED\n"+pass.stdout+"\n"+pass.stderr);
if(!pass.stdout.includes("G7_P2_RECO_INDEX_CENSUS_ARTIFACT_PASS")) throw new Error("VALIDATOR_PASS_MARKER");

const broken={...census,scope:"INVALID_SCOPE"};
fs.writeFileSync(path.join(derived,"census.json"),JSON.stringify(broken,null,2)+"\n");
const fail=spawnSync(process.execPath,[validator,root],{encoding:"utf8"});
if(fail.status===0) throw new Error("VALIDATOR_NEGATIVE_FIXTURE_FALSE_PASS");

fs.rmSync(root,{recursive:true,force:true});
console.log("G7_P2_RECO_INDEX_CENSUS_VALIDATOR_TEST_PASS");
