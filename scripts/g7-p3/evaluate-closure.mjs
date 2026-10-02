import fs from 'node:fs';
import path from 'node:path';
const args=process.argv.slice(2);
const val=(k,d=null)=>{const i=args.indexOf(k);return i>=0&&i+1<args.length?args[i+1]:d;};
const geometry=JSON.parse(fs.readFileSync(val('--geometry'),'utf8'));
const sampling=JSON.parse(fs.readFileSync(val('--sampling'),'utf8'));
const transport=JSON.parse(fs.readFileSync(val('--transport','g7/p3/cross-source-transport.json'),'utf8'));
const preseal=JSON.parse(fs.readFileSync(val('--preseal','g7/p3/preseal.json'),'utf8'));
const outDir=val('--out','g7/p3/build');
const reasons=[];
if(geometry.row_count!==12941) reasons.push('POPULATION_ROW_AUTHORITY_FAILED');
if(geometry.duplicate_identity_court?.candidate_groups!==48) reasons.push('DUPLICATE_COURT_FAILED');
if(geometry.ontology_unknown_rows!==0) reasons.push('ONTOLOGY_COVERAGE_FAILED');
if(sampling.eligible_population?.n!==10591) reasons.push('3X3_SUPPORT_FAILED');
if(sampling.population_estimation?.selected?.length!==64) reasons.push('POPULATION_SAMPLE_FAILED');
if(sampling.coverage_analysis?.selected?.length!==96) reasons.push('COVERAGE_SAMPLE_FAILED');
if(sampling.linkage_support?.counts?.A_EXACT!==0) reasons.push('UNAUTHORIZED_EXACT_LINKAGE');
if(sampling.authority?.bulk_mirror!=='HOLD' && sampling.authority?.bulk_solve_body_mirror!=='HOLD') reasons.push('BULK_AUTHORITY_DRIFT');
if(transport.transport_verdict!=='PASS_PARTIAL_WITH_EXPLICIT_BOUNDARY') reasons.push('TRANSPORT_BOUNDARY_FAILED');

const fullResearchGrade =
  transport.sources?.wca_v2?.exact_identity_linkage==='PASS' &&
  transport.sources?.cubesolves_historical?.body_transport==='PASS' &&
  sampling.linkage_support?.counts?.U_UNRESOLVED===0;

let verdict;
if(reasons.length) verdict='HOLD_POPULATION_SUPPORT_INSUFFICIENT';
else if(fullResearchGrade) verdict='PASS_RESEARCH_GRADE_CORPUS_CONSTITUTED';
else verdict='PASS_CONDITIONAL_CORPUS_WITH_EXPLICIT_SUPPORT_BOUNDARY';

if(!preseal.terminal_verdicts.includes(verdict)) throw new Error('VERDICT_NOT_PRESEALED');
const report={
  schema_version:'g7-p3-closure-1',
  verdict,
  reasons,
  evidence:{
    population_rows:geometry.row_count,
    solver_distinct:geometry.solver_concentration.distinct,
    reconstructor_distinct:geometry.reconstructor_concentration.distinct,
    reconstructor_top1_share:geometry.reconstructor_concentration.top_k_share['1'],
    duplicate_candidates:geometry.duplicate_identity_court.candidate_groups,
    ontology_unknown_rows:geometry.ontology_unknown_rows,
    eligible_3x3:sampling.eligible_population.n,
    population_sample_n:sampling.population_estimation.selected.length,
    coverage_sample_n:sampling.coverage_analysis.selected.length,
    linkage_support_counts:sampling.linkage_support.counts,
    transport_verdict:transport.transport_verdict
  },
  support_boundary:[
    'Corpus authority is the observed reconstruction population, not all human or WCA solves.',
    'Reconstructor identity and time are non-ignorable descriptive dimensions.',
    'Metadata duplicate candidates are not collapsed without stronger identity evidence.',
    'Reco-to-WCA exact attempt identity is not claimed.',
    'Population-estimation and coverage-analysis samples have different inferential roles.',
    'Bulk solve-body mirroring and raw public release remain HOLD.',
    'Cross-source transport is semantic/provenance bounded, not frequency-equivalence authority.'
  ],
  next_generation_permission: verdict!=='HOLD_POPULATION_SUPPORT_INSUFFICIENT'
};
fs.mkdirSync(outDir,{recursive:true});
fs.writeFileSync(path.join(outDir,'G7-P3-CLOSURE.json'),JSON.stringify(report,null,2)+'\n');
fs.writeFileSync(path.join(outDir,'G7-P3-CLOSURE.md'),[
  '# CUBE-REV Generation VII G7-P3 closure','',
  `**${verdict}**`,'',
  `- population rows: ${report.evidence.population_rows}`,
  `- eligible 3x3: ${report.evidence.eligible_3x3}`,
  `- solver/reconstructor: ${report.evidence.solver_distinct} / ${report.evidence.reconstructor_distinct}`,
  `- reconstructor top-1 share: ${(report.evidence.reconstructor_top1_share*100).toFixed(2)}%`,
  `- duplicate candidates retained: ${report.evidence.duplicate_candidates}`,
  `- linkage exact claims: ${report.evidence.linkage_support_counts.A_EXACT}`,
  `- transport: ${report.evidence.transport_verdict}`,'',
  '## Support boundary',
  ...report.support_boundary.map(x=>'- '+x)
].join('\n')+'\n');
console.log('G7_P3_CLOSURE_PASS');
console.log('VERDICT\t'+verdict);
console.log('NEXT_GENERATION_PERMISSION\t'+(report.next_generation_permission?'YES':'NO'));
