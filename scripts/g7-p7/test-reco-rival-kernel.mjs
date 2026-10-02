import {spawnSync} from "node:child_process";
const solved="0,1,2,3,4,5,6,7\t0,0,0,0,0,0,0,0\t0,1,2,3,4,5,6,7,8,9,10,11\t0,0,0,0,0,0,0,0,0,0,0,0";
const input="1\t0\t0\t0\t"+solved+"\n";
const p=spawnSync("cargo",["run","-q","-p","search-geometry-core","--bin","g7_p7_reco_rivals"],{input,encoding:"utf8"});
if(p.status!==0) throw new Error(p.stderr||p.stdout);
const lines=p.stdout.trim().split(/\r?\n/);
if(lines.length!==2) throw new Error("LINES:"+lines.length);
const h=lines[0].split("\t"),v=lines[1].split("\t");
const x=Object.fromEntries(h.map((k,i)=>[k,v[i]]));
if(x.phase1_lb!=="0"||x.is_g1!=="1") throw new Error("SOLVED_GEOMETRY");
const sets=["h1_best","h2_best","h3_best","ts_best","fs_best"];
for(const k of sets){
  const vals=x[k].split(",").filter(Boolean).map(Number);
  if(!vals.length||vals.some(v=>!Number.isInteger(v)||v<0||v>17)) throw new Error("RIVAL_SET:"+k);
}
const u=Number(x.rival_unique_sets);
if(!(u>=1&&u<=5)) throw new Error("RIVAL_UNIQUENESS_RANGE");
const d=Number(x.mean_pairwise_jaccard_distance);
if(!(d>=0&&d<=1)) throw new Error("DIVERSITY_RANGE");
for(const [setKey,matchKey] of [["h1_best","observed_match_h1"],["h2_best","observed_match_h2"],["h3_best","observed_match_h3"],["ts_best","observed_match_ts"],["fs_best","observed_match_fs"]]){
  const expected=x[setKey].split(",").map(Number).includes(0)?1:0;
  if(Number(x[matchKey])!==expected) throw new Error("OBSERVED_MATCH:"+setKey);
}
console.log("G7_P7_RECO_RIVAL_KERNEL_TEST_PASS");
