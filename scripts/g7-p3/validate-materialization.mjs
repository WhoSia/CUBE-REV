import fs from 'node:fs';
const args=process.argv.slice(2);
const val=(k,d=null)=>{const i=args.indexOf(k); return i>=0&&i+1<args.length?args[i+1]:d;};
const report=JSON.parse(fs.readFileSync(val('--report'),'utf8'));
const anchor=JSON.parse(fs.readFileSync(val('--anchor','g7/p3/p2-anchor.json'),'utf8'));
const e=anchor.expected;
const checks=[
  ['ROW_COUNT',report.row_count,e.row_count],
  ['SOLVER_DISTINCT',report.solver_concentration?.distinct,e.solver_distinct],
  ['RECONSTRUCTOR_DISTINCT',report.reconstructor_concentration?.distinct,e.reconstructor_distinct],
  ['UNIQUE_PAIRS',report.solver_reconstructor_graph?.unique_pairs,e.unique_pairs],
  ['DUPLICATE_CANDIDATES',report.duplicate_identity_court?.candidate_groups,e.duplicate_candidate_groups],
  ['ONTOLOGY_UNKNOWN',report.ontology_unknown_rows,e.ontology_unknown_rows],
  ['WORKFLOW_RUN',report.predecessor?.workflow_run,anchor.workflow_run],
  ['ARTIFACT_ID',report.predecessor?.artifact_id,anchor.artifact_id],
  ['BULK_MIRROR',report.authority?.bulk_solve_body_mirror,'HOLD']
];
for(const [name,actual,expected] of checks) if(actual!==expected) throw new Error(`${name}:${actual}!=${expected}`);
if(report.observed_finding!=='RECONSTRUCTOR_CONCENTRATION_DOMINATES_SOLVER_CONCENTRATION') throw new Error('FINDING_TOKEN');
console.log('G7_P3_MATERIALIZATION_ANCHOR_PASS');
