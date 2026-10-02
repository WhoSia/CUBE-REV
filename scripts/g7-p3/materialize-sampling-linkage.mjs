import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const args=process.argv.slice(2);
const val=(k,d=null)=>{const i=args.indexOf(k);return i>=0&&i+1<args.length?args[i+1]:d;};
const input=val('--input'), presealPath=val('--preseal'), ontologyPath=val('--ontology'), configPath=val('--config'), outDir=val('--out','g7/p3/build');
if(!input||!presealPath||!ontologyPath||!configPath) throw new Error('USAGE_REQUIRED');
const rows=fs.readFileSync(input,'utf8').trim().split(/\r?\n/).filter(Boolean).map(JSON.parse);
const preseal=JSON.parse(fs.readFileSync(presealPath,'utf8'));
const ontology=JSON.parse(fs.readFileSync(ontologyPath,'utf8'));
const config=JSON.parse(fs.readFileSync(configPath,'utf8'));

const hash=(seed,x)=>crypto.createHash('sha256').update(seed+'|'+x).digest('hex');
const count=(xs,key)=>{const m=new Map();for(const x of xs){const k=key(x);m.set(k,(m.get(k)||0)+1);}return m;};
const solverCounts=count(rows,r=>String(r.solver??'').trim());
const reconCounts=count(rows,r=>String(r.reconstructor??'').trim());
function band(n){
  for(const [id,[lo,hi]] of Object.entries(preseal.frequency_bands)) if(n>=lo&&(hi===null||n<=hi)) return id;
  throw new Error('NO_BAND:'+n);
}
function era(date){
  const y=Number(String(date??'').slice(0,4));
  return preseal.temporal_eras.find(e=>y>=e.start_year&&y<=e.end_year)?.id??'OUTSIDE_PRESEALED_ERAS';
}
function family(method){return (ontology.raw_label_map[method]??ontology.fallback).family;}
function summary(xs){
  const c=(key)=>Object.fromEntries([...count(xs,key)].sort((a,b)=>b[1]-a[1]||String(a[0]).localeCompare(String(b[0]))));
  return {
    n:xs.length,
    raw_method_counts:c(r=>r.method),
    method_family_counts:c(r=>family(r.method)),
    temporal_era_counts:c(r=>era(r.date)),
    solver_frequency_band_counts:c(r=>band(solverCounts.get(String(r.solver??'').trim()))),
    reconstructor_frequency_band_counts:c(r=>band(reconCounts.get(String(r.reconstructor??'').trim())))
  };
}

const eligible=rows.filter(r=>r.puzzle===config.eligible_puzzle);
if(eligible.length<config.population_estimation.n||eligible.length<config.coverage_analysis.n) throw new Error('INSUFFICIENT_ELIGIBLE');

const pop=[...eligible].sort((a,b)=>hash(config.population_estimation.seed,a.id).localeCompare(hash(config.population_estimation.seed,b.id))||a.id-b.id).slice(0,config.population_estimation.n);

const strata=new Map();
for(const r of eligible){
  const key=[family(r.method),era(r.date),band(solverCounts.get(String(r.solver??'').trim())),band(reconCounts.get(String(r.reconstructor??'').trim()))].join('\u241f');
  if(!strata.has(key)) strata.set(key,[]);
  strata.get(key).push(r);
}
for(const [k,v] of strata) v.sort((a,b)=>hash(config.coverage_analysis.seed,a.id).localeCompare(hash(config.coverage_analysis.seed,b.id))||a.id-b.id);
const ordered=[...strata.entries()].sort((a,b)=>a[1].length-b[1].length||hash(config.coverage_analysis.seed,a[0]).localeCompare(hash(config.coverage_analysis.seed,b[0]))||a[0].localeCompare(b[0]));
const coverage=ordered.slice(0,config.coverage_analysis.n).map(([key,v])=>({record:v[0],stratum:key,stratum_size:v.length}));

const tuple=r=>[r.solver,r.date,r.competition,r.result,r.puzzle].map(x=>String(x??'').trim()).join('\u241f');
const tupleCounts=count(rows,tuple);
let A=0,B=0,C=0,U=0;
const linkageRows=[];
for(const r of rows){
  const required=[r.solver,r.date,r.result,r.puzzle].every(x=>String(x??'').trim());
  const comp=String(r.competition??'').trim();
  let tier;
  if(required&&comp&&tupleCounts.get(tuple(r))===1){tier='B_STRONG_SUPPORT';B++;}
  else if(required&&comp){tier='C_CANDIDATE';C++;}
  else {tier='U_UNRESOLVED';U++;}
  linkageRows.push({source_id:r.id,tier,solver:r.solver,date:r.date,competition:r.competition,result:r.result,puzzle:r.puzzle});
}
if(A!==0) throw new Error('INDEX_METADATA_MUST_NOT_GRANT_EXACT');

const manifest={
  schema_version:'g7-p3-sampling-manifest-1',
  predecessor:preseal.predecessor,
  authority:{...preseal.authority,...config.body_contact},
  eligible_population:{puzzle:config.eligible_puzzle,n:eligible.length,nonempty_strata:strata.size},
  population_estimation:{
    design:config.population_estimation,
    inclusion_probability:config.population_estimation.n/eligible.length,
    selected:pop.map(r=>({source_id:r.id,index_page:r.index_page,solver:r.solver,reconstructor:r.reconstructor,date:r.date,method:r.method,method_family:family(r.method),temporal_era:era(r.date),solver_frequency_band:band(solverCounts.get(String(r.solver??'').trim())),reconstructor_frequency_band:band(reconCounts.get(String(r.reconstructor??'').trim()))})),
    support:summary(pop)
  },
  coverage_analysis:{
    design:config.coverage_analysis,
    selected:coverage.map(({record:r,stratum,stratum_size})=>({source_id:r.id,index_page:r.index_page,solver:r.solver,reconstructor:r.reconstructor,date:r.date,method:r.method,method_family:family(r.method),temporal_era:era(r.date),solver_frequency_band:band(solverCounts.get(String(r.solver??'').trim())),reconstructor_frequency_band:band(reconCounts.get(String(r.reconstructor??'').trim())),stratum,stratum_size})),
    support:summary(coverage.map(x=>x.record))
  },
  linkage_support:{
    definitions:config.linkage_support,
    counts:{A_EXACT:A,B_STRONG_SUPPORT:B,C_CANDIDATE:C,U_UNRESOLVED:U},
    reco_side_unique_supported_fraction:B/rows.length,
    competition_present_fraction:(B+C)/rows.length,
    claim:'LINKAGE_SUPPORT_ONLY_NOT_EXTERNAL_ATTEMPT_IDENTITY'
  }
};
fs.mkdirSync(outDir,{recursive:true});
fs.writeFileSync(path.join(outDir,'sampling-manifest.json'),JSON.stringify(manifest,null,2)+'\n');
fs.writeFileSync(path.join(outDir,'linkage-support.jsonl'),linkageRows.map(JSON.stringify).join('\n')+'\n');
fs.writeFileSync(path.join(outDir,'sampling-linkage-receipt.md'),[
  '# G7-P3 sampling/linkage receipt','',
  `- eligible 3x3 records: ${eligible.length}`,
  `- nonempty presealed strata: ${strata.size}`,
  `- population-estimation sample: ${pop.length}`,
  `- population-estimation inclusion probability: ${(config.population_estimation.n/eligible.length).toPrecision(8)}`,
  `- coverage-analysis sample: ${coverage.length}`,
  `- linkage A_EXACT: ${A}`,
  `- linkage B_STRONG_SUPPORT: ${B}`,
  `- linkage C_CANDIDATE: ${C}`,
  `- linkage U_UNRESOLVED: ${U}`,
  '- external official-attempt identity claimed: NO',
  '- solve-body requests: 0',
  '- bulk mirror: HOLD'
].join('\n')+'\n');
console.log('G7_P3_SAMPLING_LINKAGE_PASS');
console.log('ELIGIBLE_3X3\t'+eligible.length);
console.log('NONEMPTY_STRATA\t'+strata.size);
console.log('POP_SAMPLE\t'+pop.length);
console.log('COVERAGE_SAMPLE\t'+coverage.length);
console.log('LINK_A_EXACT\t'+A);
console.log('LINK_B_STRONG_SUPPORT\t'+B);
console.log('LINK_C_CANDIDATE\t'+C);
console.log('LINK_U_UNRESOLVED\t'+U);
console.log('SOLVE_BODY_REQUESTS\t0');
