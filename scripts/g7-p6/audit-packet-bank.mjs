import fs from "node:fs";
const bank=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));
const out=process.argv[3]; if(!out) throw new Error("output");
const fail=[];
const rec=bank.records;
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
if(rec.length!==256) fail.push("COUNT");
if(new Set(rec.map(x=>x.state_id)).size!==256) fail.push("STATE_ID");
if(new Set(rec.map(x=>JSON.stringify(x.cube))).size!==256) fail.push("EXACT_STATE_DUPLICATE");
const seeds=[...new Set(rec.map(x=>x.seed_id))].sort();
if(seeds.length!==8) fail.push("SEEDS");
const motifs=["H2_UNIQUE","ALL_HORIZON_DISAGREE","COMPONENT_UNIQUE","COMPONENT_VS_MAX_CONFLICT"];
const counts={};
const lbCounts={};
for(const x of rec){
  counts[x.motif]=(counts[x.motif]||0)+1;
  lbCounts[x.phase1_lb]=(lbCounts[x.phase1_lb]||0)+1;
  const h1=x.rivals.H1_MAX_PDB_GREEDY,h2=x.rivals.H2_MAX_PDB_LOOKAHEAD,h3=x.rivals.H3_MAX_PDB_LOOKAHEAD;
  const ts=x.rivals.H1_TWIST_SLICE_COMPONENT,fs=x.rivals.H1_FLIP_SLICE_COMPONENT;
  if(![h1,h2,h3,ts,fs].every(a=>a.length>0)) fail.push("EMPTY_RIVAL:"+x.state_id);
  if(x.motif==="H2_UNIQUE" && (eq(h2,h1)||eq(h2,h3))) fail.push("H2_UNIQUE:"+x.state_id);
  if(x.motif==="ALL_HORIZON_DISAGREE" && (eq(h1,h2)||eq(h1,h3)||eq(h2,h3))) fail.push("ALL_H:"+x.state_id);
  if(x.motif==="COMPONENT_UNIQUE"){
    const tsu=!eq(ts,h1)&&!eq(ts,h2)&&!eq(ts,h3)&&!eq(ts,fs);
    const fsu=!eq(fs,h1)&&!eq(fs,h2)&&!eq(fs,h3)&&!eq(fs,ts);
    if(!(tsu||fsu)) fail.push("COMP_UNIQUE:"+x.state_id);
  }
  if(x.motif==="COMPONENT_VS_MAX_CONFLICT" && (eq(ts,fs)||(eq(ts,h2)&&eq(fs,h2)))) fail.push("COMP_MAX:"+x.state_id);
}
for(const m of motifs) if(counts[m]!==64) fail.push("MOTIF_COUNT:"+m+":"+counts[m]);
for(const s of seeds) if(rec.filter(x=>x.seed_id===s).length!==32) fail.push("SEED_COUNT:"+s);
if(Object.keys(lbCounts).length<3) fail.push("LB_SUPPORT");
const report={schema_version:"g7-p6-packet-bank-audit-1",pass:fail.length===0,failures:fail,
 states:rec.length,seeds:seeds.length,motif_counts:counts,phase1_lb_counts:lbCounts,bank_sha256:bank.sha256};
fs.writeFileSync(out,JSON.stringify(report,null,2)+"\n");
if(fail.length){console.error(fail.join("\n"));process.exit(1);}
console.log("G7_P6_PACKET_BANK_AUDIT_PASS");
console.log("STATES\t"+report.states);
console.log("SEEDS\t"+report.seeds);
console.log("LB_LEVELS\t"+Object.keys(lbCounts).length);
