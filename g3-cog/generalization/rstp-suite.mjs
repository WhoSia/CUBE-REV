import {execFileSync} from 'node:child_process';
const files=['torus-witness-v2.mjs','hypercube-witness.mjs','permutation-witness.mjs'];
const witnesses=[];
for(const f of files){const out=execFileSync(process.execPath,[`g3-cog/generalization/${f}`],{encoding:'utf8'});witnesses.push(JSON.parse(out));}
const pass=witnesses.every(w=>w.result==='PASS');
const receipt={schema:'CUBE-REV-RSTP-PORTABILITY-SUITE-v1',domains:witnesses.map(w=>({system:w.system,result:w.result,reversibility:w.reversibility,algebra:w.algebra??null,divergent:w.family?.divergent?.different_context,control:w.family?.control?.context_equal,common_suffix:w.family?.divergent?.common_suffix,action_surface:w.family?.divergent?.action_surface?.length})),claim_boundary:'Compiler portability across distinct reversible finite-state systems; no claim of universal human mechanism.',result:pass?'PASS':'FAIL'};
console.log(JSON.stringify(receipt,null,2));if(!pass)process.exit(1);
