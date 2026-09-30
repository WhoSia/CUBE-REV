import fs from "node:fs";
import crypto from "node:crypto";
import path from "node:path";

const source=process.argv[2]??"g7/p1/build/g7-p1-radius4-match-search.tsv";
const out=process.argv[3]??"g7/p1/build/instrument";
const raw=fs.readFileSync(source,"utf8").trimEnd();
const lines=raw.split(/\r?\n/);
const hi=lines.findIndex(x=>x.startsWith("family\tdg\td1\tq\t"));
if(hi<0)throw new Error("HEADER_NOT_FOUND");
const header=lines[hi].split("\t");
const required=["family","dg","d1","q","solutions","first_mask","prefix2","A","A_facelets","A_slack","B","B_facelets","B_slack"];
if(required.some((x,i)=>header[i]!==x))throw new Error("SCHEMA_MISMATCH");
const rows=lines.slice(hi+1).filter(Boolean).map(line=>{
  const v=line.split("\t");if(v.length!==header.length)throw new Error("ROW_WIDTH");
  const o=Object.fromEntries(header.map((k,i)=>[k,v[i]]));
  for(const key of ["A_facelets","B_facelets"]){
    if(!/^[URFDLB]{54}$/.test(o[key]))throw new Error("FACELET_FORMAT");
    for(const ch of "URFDLB")if([...o[key]].filter(x=>x===ch).length!==9)throw new Error("FACELET_COUNT");
  }
  return {family:Number(o.family),dg:Number(o.dg),d1:Number(o.d1),q:o.q,solutions:Number(o.solutions),firstMask:Number(o.first_mask),prefix2:Number(o.prefix2),
    a:{scramble:o.A,facelets:o.A_facelets,slack:o.A_slack},b:{scramble:o.B,facelets:o.B_facelets,slack:o.B_slack}};
});
if(rows.length!==90)throw new Error("FAMILY_COUNT");
if(new Set(rows.map(r=>r.family)).size!==90)throw new Error("DUPLICATE_FAMILY");
fs.mkdirSync(out,{recursive:true});
for(const name of ["index.html","app.js","styles.css"])fs.copyFileSync(path.join("g7/p1/web",name),path.join(out,name));
const payload=JSON.stringify(rows);
const digest=crypto.createHash("sha256").update(payload).digest("hex");
fs.writeFileSync(path.join(out,"stimuli.js"),`window.G7_MANIFEST_SHA256="${digest}";window.G7_STIMULI=${payload};\n`);
fs.writeFileSync(path.join(out,"manifest.sha256"),digest+"\n");
for(const file of ["index.html","app.js","styles.css"]){
  const text=fs.readFileSync(path.join(out,file),"utf8");
  if(/https?:\/\//i.test(text)||/fetch\s*\(|XMLHttpRequest|WebSocket|sendBeacon/i.test(text))throw new Error("NETWORK_SURFACE_REFUSE:"+file);
}
console.log("G7_P1_INSTRUMENT_BUILD_PASS");
console.log("FAMILIES\t"+rows.length);
console.log("MANIFEST_SHA256\t"+digest);
console.log("NETWORK_SURFACE\tNONE");
