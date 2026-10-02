import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
const dir=fs.mkdtempSync(path.join(os.tmpdir(),'g7-p3-test-'));
const rows=[
 {id:1,puzzle:'3x3',result:'5.00',solver:'A',method:'CFOP',date:'2024-01-01',competition:'X',tags:'',movecount:50,tps:10,reconstructor:'R1',index_page:1},
 {id:2,puzzle:'3x3',result:'5.10',solver:'A',method:'CFOP',date:'2024-01-02',competition:'X',tags:'',movecount:51,tps:10,reconstructor:'R1',index_page:1},
 {id:3,puzzle:'OH',result:'9.00',solver:'B',method:'Roux',date:'2025-01-03',competition:'Y',tags:'',movecount:55,tps:6,reconstructor:'R2',index_page:1},
 {id:4,puzzle:'3x3',result:'6.00',solver:'C',method:'CFOP',date:'2025-02-01',competition:'Z',tags:'',movecount:60,tps:8,reconstructor:'R1',index_page:1},
 {id:5,puzzle:'3x3',result:'6.00',solver:'C',method:'CFOP',date:'2025-02-01',competition:'Z',tags:'',movecount:60,tps:8,reconstructor:'R1',index_page:2}
];
const input=path.join(dir,'rows.jsonl'); fs.writeFileSync(input,rows.map(JSON.stringify).join('\n')+'\n');
const out=path.join(dir,'out');
const p=spawnSync(process.execPath,['scripts/g7-p3/analyze-population.mjs','--input',input,'--preseal','g7/p3/preseal.json','--ontology','g7/p3/method-ontology.json','--out',out],{encoding:'utf8'});
if(p.status!==0) throw new Error(p.stderr||p.stdout);
const r=JSON.parse(fs.readFileSync(path.join(out,'population-geometry.json'),'utf8'));
if(r.row_count!==5) throw new Error('ROW_COUNT');
if(r.solver_concentration.distinct!==3) throw new Error('SOLVER_DISTINCT');
if(r.reconstructor_concentration.distinct!==2) throw new Error('RECON_DISTINCT');
if(r.solver_reconstructor_graph.unique_pairs!==3) throw new Error('PAIR_COUNT');
if(r.duplicate_identity_court.candidate_groups!==1) throw new Error('DUP_CANDIDATE');
if(r.ontology_unknown_rows!==0) throw new Error('ONTOLOGY_COVERAGE');
if(r.authority.bulk_solve_body_mirror!=='HOLD') throw new Error('AUTHORITY_DRIFT');
console.log('G7_P3_POPULATION_GEOMETRY_TEST_PASS');
