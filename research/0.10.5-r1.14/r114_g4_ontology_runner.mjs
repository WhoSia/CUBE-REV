import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import crypto from 'node:crypto';

const here=path.dirname(fileURLToPath(import.meta.url));
const srcPath=path.join(here,'r114_g4_ontology_geometry.mjs');
const runtimePath=path.join(here,'r114_g4_ontology_geometry.runtime.mjs');
const original=fs.readFileSync(srcPath,'utf8');
const needle='lines[i].end>x.start';
const replacement='lines[i].end>lines[i].start';
const occurrences=original.split(needle).length-1;
if(occurrences!==1) throw new Error(`R114_PREEXEC_REPAIR_OCCURRENCE_${occurrences}`);
const repaired=original.replace(needle,replacement);
if(repaired.includes(needle)) throw new Error('R114_PREEXEC_REPAIR_INCOMPLETE');
fs.writeFileSync(runtimePath,repaired,'utf8');
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const receipt={
  schema_version:'CR0105R114-PREEXEC-IMPLEMENTATION-REPAIR-1',
  status:'PASS_SINGLE_LITERAL_REPAIR_BEFORE_ANY_G4_ROUTE_OUTCOME',
  source_path:path.relative(process.cwd(),srcPath),
  runtime_path:path.relative(process.cwd(),runtimePath),
  source_sha256:sha(original),
  runtime_sha256:sha(repaired),
  replacement_count:occurrences,
  old_literal:needle,
  new_literal:replacement,
  scientific_definition_changed:false,
  gate_changed:false,
  baseline_membership_changed:false,
  route_outcomes_seen_before_repair:false,
  human_observations:0
};
const out=process.env.R114_ROOT||'/tmp/r114';fs.mkdirSync(out,{recursive:true});
fs.writeFileSync(path.join(out,'PREEXEC_IMPLEMENTATION_REPAIR_RECEIPT.json'),JSON.stringify(receipt,null,2)+'\n');
console.log('CR0105R114_PREEXEC_IMPLEMENTATION_REPAIR_PASS',receipt.runtime_sha256);
await import(pathToFileURL(runtimePath).href+`?sha=${receipt.runtime_sha256}`);
