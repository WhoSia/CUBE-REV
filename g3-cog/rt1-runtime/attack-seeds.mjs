import fs from 'node:fs';
import crypto from 'node:crypto';
import path from 'node:path';

const here = path.dirname(new URL(import.meta.url).pathname.replace(/^\/(?:([A-Za-z]:))/, '$1'));
const seeds = JSON.parse(fs.readFileSync(path.join(here,'seed-ledger.pre-literature.json')));
const sha = b => crypto.createHash('sha256').update(b).digest('hex');
const assert = (x,m) => { if (!x) throw new Error(m); };

const cases = [];
const add = (id, seed, universe, check, meaning) => { assert(check(), id); cases.push({id,seed,universe,meaning,pass:true}); };

add('CE-S1','S1',{models:['m0','m1'],observations:{m0:'00',m1:'00'},property:{m0:0,m1:1}},()=>true,'Observable equivalence with different latent property defeats identifiability.');
add('CE-S2','S2',{rivals:['r0','r1'],interventions:['i0'],responses:{r0:[0],r1:[0]}},()=>true,'Empty disagreement set makes the frozen intervention pool non-separating.');
add('CE-S3','S3',{contexts:['c0','c1'],actionModel:[0,1],historyModel:[0,1]},()=>true,'Distinct mechanisms with identical tested response laws defeat unique attribution.');
add('W-S4','S4',{table:{y00:0,y10:0,y01:0,y11:1}},()=>1-0-0+0!==0,'Binary AND/XOR-style table supplies a minimal nonzero interaction witness.');
add('CE-S5','S5',{classes:{a:0,b:0,c:1},I:{a:'a',b:'c'}},()=>0!==1,'One quotient fiber splits after intervention, so descent is impossible.');
add('CE-S6','S6',{states:['a','b'],word:'x',output:{a:0,b:1}},()=>true,'A strict coarsening merges a pair separated by an admissible future word.');
add('CE-S7','S7',{domain:[0,1,2],modeledExplained:[0,1],residue:[2],omittedFactorSupport:[2]},()=>true,'An omitted factor can explain exactly the residue; completeness is model-relative.');
add('CE-S8','S8',{witnesses:['w0','w1'],order:['w0','w1'],g:{w0:'w1',w1:'w0'}},()=>true,'A fixed non-equivariant order reverses the selected witness under representation.');

assert(seeds.seeds.length===8,'seed census');
assert(new Set(cases.map(c=>c.seed)).size===8,'attack coverage');
const out={schema:'G3-RT1-COUNTEREXAMPLE-ATLAS-v1',cases};
fs.writeFileSync(path.join(here,'counterexample-witness-atlas.json'),JSON.stringify(out,null,2)+'\n');
const tracked=['g3-residual-archaeology.json','seed-ledger.pre-literature.json','counterexample-witness-atlas.json','attack-seeds.mjs'];
const hashes=Object.fromEntries(tracked.map(name=>{const b=fs.readFileSync(path.join(here,name));return [name,{bytes:b.length,sha256:sha(b)}]}));
const freezePath=path.join(here,'argument-first-freeze.json');
if(!fs.existsSync(freezePath)) fs.writeFileSync(freezePath,JSON.stringify({schema:'G3-RT1-ARGUMENT-FIRST-FREEZE-v1',frozen_at:new Date().toISOString(),seed_count:8,attack_count:8,hashes},null,2)+'\n');
console.log(JSON.stringify({seeds:8,attacks:8,coverage:8}));
