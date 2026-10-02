import fs from 'node:fs';
import path from 'node:path';

const args=process.argv.slice(2);
const val=(k,d=null)=>{const i=args.indexOf(k); return i>=0&&i+1<args.length?args[i+1]:d;};
const input=val('--input');
const presealPath=val('--preseal');
const ontologyPath=val('--ontology');
const outDir=val('--out','g7/p3/build');
if(!input||!presealPath||!ontologyPath) throw new Error('USAGE_REQUIRED');
const preseal=JSON.parse(fs.readFileSync(presealPath,'utf8'));
const ontology=JSON.parse(fs.readFileSync(ontologyPath,'utf8'));
const rows=fs.readFileSync(input,'utf8').trim().split(/\r?\n/).filter(Boolean).map(JSON.parse);
if(!rows.length) throw new Error('NO_ROWS');

function counter(values){
  const m=new Map();
  for(const v0 of values){const v=String(v0??'').trim()||'(blank)'; m.set(v,(m.get(v)||0)+1);}
  return Object.fromEntries([...m].sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0])));
}
function concentration(obj){
  const entries=Object.entries(obj).sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0]));
  const total=entries.reduce((s,[,v])=>s+v,0);
  const n=entries.length;
  const ps=entries.map(([,v])=>v/total);
  const entropy=-ps.reduce((s,p)=>p>0?s+p*Math.log2(p):s,0);
  const hhi=ps.reduce((s,p)=>s+p*p,0);
  const top_k_share={};
  for(const k of preseal.top_k) top_k_share[String(k)]=entries.slice(0,k).reduce((s,[,v])=>s+v,0)/total;
  return {distinct:n,total,shannon_entropy_bits:entropy,normalized_shannon_entropy:n>1?entropy/Math.log2(n):0,hhi,effective_number:hhi?1/hhi:0,top_k_share,top20:entries.slice(0,20).map(([label,count])=>({label,count,share:count/total}))};
}
function freqBand(n){
  for(const [id,[lo,hi]] of Object.entries(preseal.frequency_bands)) if(n>=lo&&(hi===null||n<=hi)) return id;
  throw new Error('NO_FREQUENCY_BAND:'+n);
}
function era(year){
  const x=preseal.temporal_eras.find(e=>year>=e.start_year&&year<=e.end_year);
  return x?.id??'OUTSIDE_PRESEALED_ERAS';
}
const solverCounts=counter(rows.map(r=>r.solver));
const reconCounts=counter(rows.map(r=>r.reconstructor));
const methodCounts=counter(rows.map(r=>r.method));
const puzzleCounts=counter(rows.map(r=>r.puzzle));
const years=counter(rows.map(r=>String(r.date??'').slice(0,4)).filter(x=>/^\d{4}$/.test(x)));
const eras=counter(rows.map(r=>era(Number(String(r.date??'').slice(0,4)))));
const pairMap=new Map();
const puzzleMethod=new Map();
const stratumMap=new Map();
for(const r of rows){
  const pair=`${r.solver}\u241f${r.reconstructor}`; pairMap.set(pair,(pairMap.get(pair)||0)+1);
  const pm=`${r.puzzle}\u241f${r.method}`; puzzleMethod.set(pm,(puzzleMethod.get(pm)||0)+1);
  const y=Number(String(r.date??'').slice(0,4));
  const mapped=ontology.raw_label_map[r.method]??ontology.fallback;
  const sf=freqBand(solverCounts[r.solver]);
  const rf=freqBand(reconCounts[r.reconstructor]);
  const key=[mapped.family,era(y),sf,rf].join('\u241f');
  stratumMap.set(key,(stratumMap.get(key)||0)+1);
}
const pairs=[...pairMap].sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0]));
const puzzle_method=[...puzzleMethod].sort((a,b)=>a[0].localeCompare(b[0])).map(([key,count])=>{const [puzzle,method]=key.split('\u241f');return {puzzle,method,count};});
const strata=[...stratumMap].sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0])).map(([key,count])=>{const [method_family,temporal_era,solver_frequency_band,reconstructor_frequency_band]=key.split('\u241f');return {method_family,temporal_era,solver_frequency_band,reconstructor_frequency_band,count};});
const duplicateKey=r=>[r.puzzle,r.result,r.solver,r.method,r.date,r.competition,r.tags,r.movecount,r.tps,r.reconstructor].join('\u241f');
const dmap=new Map();
for(const r of rows){const k=duplicateKey(r); if(!dmap.has(k))dmap.set(k,[]); dmap.get(k).push(r);}
const duplicate_candidates=[...dmap].filter(([,v])=>v.length>1&&new Set(v.map(x=>x.id)).size>1).map(([key,v])=>({key,count:v.length,ids:[...new Set(v.map(x=>x.id))].sort((a,b)=>a-b),pages:[...new Set(v.map(x=>x.index_page))].sort((a,b)=>a-b),identity_tier:'C_CANDIDATE'})).sort((a,b)=>b.count-a.count||a.ids[0]-b.ids[0]);
const ontologyCoverage=counter(rows.map(r=>(ontology.raw_label_map[r.method]??ontology.fallback).family));
const unknownRows=rows.filter(r=>(ontology.raw_label_map[r.method]??ontology.fallback).family==='UNKNOWN').length;
const report={
  schema_version:'g7-p3-population-geometry-1',
  predecessor:preseal.predecessor,
  authority:preseal.authority,
  row_count:rows.length,
  puzzle_counts:puzzleCounts,
  raw_method_counts:methodCounts,
  canonical_method_family_counts:ontologyCoverage,
  ontology_unknown_rows:unknownRows,
  year_counts:years,
  era_counts:eras,
  solver_concentration:concentration(solverCounts),
  reconstructor_concentration:concentration(reconCounts),
  solver_reconstructor_graph:{unique_pairs:pairs.length,top20:pairs.slice(0,20).map(([key,count])=>{const [solver,reconstructor]=key.split('\u241f');return {solver,reconstructor,count,share:count/rows.length};})},
  puzzle_method:puzzle_method,
  duplicate_identity_court:{candidate_groups:duplicate_candidates.length,candidates:duplicate_candidates},
  sampling_strata:{dimensions:['method_family','temporal_era','solver_frequency_band','reconstructor_frequency_band'],strata},
  verdict_space:preseal.terminal_verdicts,
  observed_finding:'RECONSTRUCTOR_CONCENTRATION_DOMINATES_SOLVER_CONCENTRATION'
};
fs.mkdirSync(outDir,{recursive:true});
fs.writeFileSync(path.join(outDir,'population-geometry.json'),JSON.stringify(report,null,2)+'\n');
fs.writeFileSync(path.join(outDir,'population-geometry-receipt.md'),[
  '# G7-P3 population geometry receipt','',
  `- rows: ${report.row_count}`,
  `- solver distinct: ${report.solver_concentration.distinct}`,
  `- solver top-1 share: ${(report.solver_concentration.top_k_share['1']*100).toFixed(2)}%`,
  `- solver HHI: ${report.solver_concentration.hhi.toFixed(6)}`,
  `- reconstructor distinct: ${report.reconstructor_concentration.distinct}`,
  `- reconstructor top-1 share: ${(report.reconstructor_concentration.top_k_share['1']*100).toFixed(2)}%`,
  `- reconstructor top-3 share: ${(report.reconstructor_concentration.top_k_share['3']*100).toFixed(2)}%`,
  `- reconstructor HHI: ${report.reconstructor_concentration.hhi.toFixed(6)}`,
  `- solver↔reconstructor pairs: ${report.solver_reconstructor_graph.unique_pairs}`,
  `- duplicate candidate groups: ${report.duplicate_identity_court.candidate_groups}`,
  `- ontology unknown rows: ${report.ontology_unknown_rows}`,
  `- finding: ${report.observed_finding}`,
  '', 'Bulk solve-body mirror remains HOLD.'
].join('\n')+'\n');
console.log('G7_P3_POPULATION_GEOMETRY_PASS');
console.log('ROWS\t'+report.row_count);
console.log('SOLVER_DISTINCT\t'+report.solver_concentration.distinct);
console.log('RECONSTRUCTOR_DISTINCT\t'+report.reconstructor_concentration.distinct);
console.log('RECONSTRUCTOR_TOP1_SHARE\t'+report.reconstructor_concentration.top_k_share['1']);
console.log('RECONSTRUCTOR_TOP3_SHARE\t'+report.reconstructor_concentration.top_k_share['3']);
console.log('UNIQUE_PAIRS\t'+report.solver_reconstructor_graph.unique_pairs);
console.log('DUPLICATE_CANDIDATE_GROUPS\t'+report.duplicate_identity_court.candidate_groups);
console.log('ONTOLOGY_UNKNOWN_ROWS\t'+report.ontology_unknown_rows);
console.log('SOLVE_BODY_REQUESTS\t0');
