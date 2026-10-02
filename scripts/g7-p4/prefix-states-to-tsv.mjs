import fs from "node:fs";
const input=process.argv[2];
if(!input) throw new Error("input");
for(const line of fs.readFileSync(input,"utf8").trim().split(/\r?\n/).filter(Boolean)){
  const x=JSON.parse(line), c=x.cubie;
  console.log([
    x.source_id,x.prefix_index,x.observed_next_action_index??-1,x.boundary_after?1:0,
    c.cp.join(","),c.co.join(","),c.ep.join(","),c.eo.join(",")
  ].join("\t"));
}
