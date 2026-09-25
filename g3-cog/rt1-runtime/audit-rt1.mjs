import fs from 'node:fs';
import crypto from 'node:crypto';
import path from 'node:path';

const here=path.dirname(new URL(import.meta.url).pathname.replace(/^\/(?:([A-Za-z]:))/, '$1'));
const root=path.resolve(here,'..','..');
const read=name=>fs.readFileSync(path.join(here,name));
const json=name=>JSON.parse(read(name));
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const assert=(x,m)=>{if(!x)throw new Error(m)};

const archaeology=json('g3-residual-archaeology.json');
const pre=json('seed-ledger.pre-literature.json');
const atlas=json('counterexample-witness-atlas.json');
const complement=json('prior-art-complement-ledger.json');
const custody=json('source-custody-ledger.json');
const rivals=json('strongest-rival-matrix.json');
const adj=json('seed-adjudication.json');
const gate=json('p39-gate.json');

assert(archaeology.entries.length>=8,'archaeology census');
assert(pre.seeds.length===8,'seed census');
assert(atlas.cases.length===8 && new Set(atlas.cases.map(x=>x.seed)).size===8,'attack coverage');
assert(complement.seeds.length===8,'complement census');
assert(rivals.rivals.length>=6,'rival census');
assert(adj.distinctive_survivor_count===0 && !adj.external_falsifier_changed,'promotion violation');
assert(gate.decision==='P39_REAUTHORIZATION_DENIED' && !gate.p39_opened && gate.world_contact==='NOT_EXECUTED','gate violation');
assert(custody.canonical_drive.filter(x=>x.status?.startsWith('PRESENT')).length>=7,'custody census');

const inherited={
  terminal:'g3-cog/p38-r2-runtime/terminal-receipt.json',
  a:'g3-cog/p38-r2-runtime/external-falsification-preseal-a.json',
  b:'g3-cog/p38-r2-runtime/external-falsification-preseal-b.json'
};
const got=Object.fromEntries(Object.entries(inherited).map(([k,p])=>[k,sha(fs.readFileSync(path.join(root,p)))]));
assert(got.terminal===gate.p38_custody.terminal_receipt_sha256,'P38 receipt drift');
assert(got.a===gate.p38_custody.preseal_a_sha256,'preseal A drift');
assert(got.b===gate.p38_custody.preseal_b_sha256,'preseal B drift');

const files=fs.readdirSync(here).filter(n=>!['verification.json','terminal-receipt.json'].includes(n)).sort();
const hashes=Object.fromEntries(files.map(name=>[name,{bytes:read(name).length,sha256:sha(read(name))}]));
const verification={schema:'G3-RT1-VERIFICATION-v1',generated_at:new Date().toISOString(),checks:{archaeology_entries:archaeology.entries.length,seeds:8,attacks:8,prior_art_complements:8,strong_rivals:rivals.rivals.length,distinctive_survivors:0,external_falsifier_changed:false,p38_bytes_unchanged:true,world_contact_executed:false,p39_opened:false},inherited_hashes:got,hashes};
fs.writeFileSync(path.join(here,'verification.json'),JSON.stringify(verification,null,2)+'\n');
console.log(JSON.stringify(verification.checks));
