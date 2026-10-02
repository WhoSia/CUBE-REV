import fs from "node:fs";
import crypto from "node:crypto";

const input=process.argv[2], outDir=process.argv[3];
if(!input||!outDir) throw new Error("usage: select-packets bank.json outdir");
const bank=JSON.parse(fs.readFileSync(input,"utf8"));
const models=[
 "H1_MAX_PDB_GREEDY",
 "H2_MAX_PDB_LOOKAHEAD",
 "H3_MAX_PDB_LOOKAHEAD",
 "H1_TWIST_SLICE_COMPONENT",
 "H1_FLIP_SLICE_COMPONENT"
];
const set=x=>new Set(x);
function jaccard(a,b){
  const A=set(a),B=set(b);
  let inter=0; for(const x of A) if(B.has(x)) inter++;
  const union=new Set([...A,...B]).size;
  return union?inter/union:1;
}
function diversity(r){
  let sum=0,n=0,min=1;
  for(let i=0;i<models.length;i++) for(let j=i+1;j<models.length;j++){
    const d=1-jaccard(r.rivals[models[i]],r.rivals[models[j]]);
    sum+=d;n++;min=Math.min(min,d);
  }
  return {mean:sum/n,min,ties:models.reduce((s,m)=>s+r.rivals[m].length,0)};
}
const cells=new Map();
for(const r of bank.records){
  const k=r.seed_id+"|"+r.motif;
  if(!cells.has(k)) cells.set(k,[]);
  cells.get(k).push({...r,selection_geometry:diversity(r)});
}
if(cells.size!==32) throw new Error("CELL_COUNT:"+cells.size);
const dev=[],confirm=[],reserve=[];
for(const [cell,rows] of [...cells].sort()){
  rows.sort((a,b)=>
    b.selection_geometry.mean-a.selection_geometry.mean ||
    b.selection_geometry.min-a.selection_geometry.min ||
    a.selection_geometry.ties-b.selection_geometry.ties ||
    a.state_id.localeCompare(b.state_id)
  );
  if(rows.length!==8) throw new Error("CELL_SIZE:"+cell+":"+rows.length);
  dev.push({...rows[0],cell,within_cell_rank:1});
  confirm.push({...rows[1],cell,within_cell_rank:2});
  for(let i=2;i<rows.length;i++) reserve.push({...rows[i],cell,within_cell_rank:i+1});
}
const canonical=x=>JSON.stringify(x);
const hash=x=>crypto.createHash("sha256").update(canonical(x)).digest("hex");
const devCore={schema_version:"g7-p6-live-packet-1",role:"DEVELOPMENT",human_contact_authority:"CLOSED",records:dev};
const conCore={schema_version:"g7-p6-live-packet-1",role:"FRESH_CONFIRMATION",human_contact_authority:"CLOSED",records:confirm};
const resCore={schema_version:"g7-p6-live-packet-reserve-1",role:"RESERVE",human_contact_authority:"CLOSED",records:reserve};
fs.mkdirSync(outDir,{recursive:true});
fs.writeFileSync(outDir+"/development-packet.json",JSON.stringify({...devCore,sha256:hash(devCore)},null,2)+"\n");
fs.writeFileSync(outDir+"/confirmation-packet.json",JSON.stringify({...conCore,sha256:hash(conCore)},null,2)+"\n");
fs.writeFileSync(outDir+"/reserve-bank.json",JSON.stringify({...resCore,sha256:hash(resCore)},null,2)+"\n");
const receipt={
 schema_version:"g7-p6-packet-selection-1",
 source_bank_sha256:bank.sha256,
 selection_rule:"within each of 8 seed x 4 motif cells rank by mean pairwise five-rival Jaccard distance descending, minimum pairwise distance descending, total rival tie count ascending, state_id lexical",
 development_states:dev.length,
 confirmation_states:confirm.length,
 reserve_states:reserve.length,
 development_sha256:hash(devCore),
 confirmation_sha256:hash(conCore),
 reserve_sha256:hash(resCore),
 development_mean_diversity:dev.reduce((s,x)=>s+x.selection_geometry.mean,0)/dev.length,
 confirmation_mean_diversity:confirm.reduce((s,x)=>s+x.selection_geometry.mean,0)/confirm.length,
 exact_state_overlap_dev_confirm:dev.filter(x=>confirm.some(y=>canonical(x.cube)===canonical(y.cube))).length,
 state_id_overlap_dev_confirm:dev.filter(x=>confirm.some(y=>x.state_id===y.state_id)).length
};
fs.writeFileSync(outDir+"/selection-receipt.json",JSON.stringify(receipt,null,2)+"\n");
console.log("G7_P6_PACKET_SELECTION_PASS");
console.log("DEVELOPMENT\t"+dev.length);
console.log("CONFIRMATION\t"+confirm.length);
console.log("RESERVE\t"+reserve.length);
console.log("DEV_SHA256\t"+receipt.development_sha256);
console.log("CONFIRM_SHA256\t"+receipt.confirmation_sha256);
console.log("DEV_MEAN_DIVERSITY\t"+receipt.development_mean_diversity);
console.log("CONFIRM_MEAN_DIVERSITY\t"+receipt.confirmation_mean_diversity);
