import fs from "node:fs";
import path from "node:path";
const args=process.argv.slice(2);
const val=(k,d=null)=>{const i=args.indexOf(k);return i>=0&&i+1<args.length?args[i+1]:d;};
const pre=JSON.parse(fs.readFileSync(val("--preseal","g7/p4/preseal.json"),"utf8"));
const pilot=JSON.parse(fs.readFileSync(val("--pilot-summary"),"utf8"));
const conf=JSON.parse(fs.readFileSync(val("--confirmatory-summary"),"utf8"));
const cross=JSON.parse(fs.readFileSync(val("--cross","g7/p4/cross-source-replication.json"),"utf8"));
const outDir=val("--out","g7/p4/build");
const failures=[];
const th=pre.closure_thresholds;
if(pilot.solve_count!==10) failures.push("PILOT_COUNT");
if(conf.solve_count!==10) failures.push("CONFIRMATORY_COUNT");
if(pilot.supported_fraction<th.descriptive_exact_replay_fraction_min) failures.push("PILOT_REPLAY_SUPPORT");
if(conf.supported_fraction<th.descriptive_exact_replay_fraction_min) failures.push("CONFIRMATORY_REPLAY_SUPPORT");
const annotationBearing=pilot.annotation_geometry.annotation_bearing_solves+conf.annotation_geometry.annotation_bearing_solves;
if(annotationBearing<th.annotation_bearing_solves_min) failures.push("ANNOTATION_SUPPORT");
if(cross.semantic_structure_replication!=="PASS_BOUNDED_SCHEMA") failures.push("CROSS_SOURCE_SCHEMA");

const searchEvents=(pilot.search_alignment.n||0)+(conf.search_alignment.n||0);
const searchMaterialized=searchEvents>0;
const reconstructorConditionedRobustness=false;
const independentMechanismReplication=cross.mechanism_replication==="PASS";
const mechanismEligible=
  failures.length===0 &&
  independentMechanismReplication &&
  reconstructorConditionedRobustness &&
  searchMaterialized;

let verdict;
if(failures.length) verdict="HOLD_MECHANISM_IDENTIFICATION_INSUFFICIENT";
else if(mechanismEligible) verdict="PASS_MECHANISM_SUPPORT_WITH_MEASUREMENT_BOUNDARY";
else verdict="PASS_DESCRIPTIVE_POLICY_GEOMETRY_ONLY";
if(!pre.terminal_verdicts.includes(verdict)) throw new Error("VERDICT_NOT_PRESEALED");

const report={
  schema_version:"g7-p4-closure-1",
  verdict,
  failures,
  evidence:{
    pilot_supported_fraction:pilot.supported_fraction,
    confirmatory_supported_fraction:conf.supported_fraction,
    annotation_bearing_solves:annotationBearing,
    pilot_moves_search_aligned:pilot.search_alignment.n||0,
    confirmatory_moves_search_aligned:conf.search_alignment.n||0,
    search_events:searchEvents,
    pilot_best_rival_tie_rate:pilot.search_alignment.best_rival_tie_rate??null,
    confirmatory_best_rival_tie_rate:conf.search_alignment.best_rival_tie_rate??null,
    pilot_mean_local_regret:pilot.search_alignment.mean_local_regret??null,
    confirmatory_mean_local_regret:conf.search_alignment.mean_local_regret??null,
    cross_source_semantic_replication:cross.semantic_structure_replication,
    cross_source_mechanism_replication:cross.mechanism_replication
  },
  mechanism_gate:{
    independent_mechanism_replication:independentMechanismReplication,
    reconstructor_conditioned_robustness:reconstructorConditionedRobustness,
    search_alignment_materialized:searchMaterialized
  },
  support_boundary:[
    "Exact replay validates mechanical trajectory consistency, not latent planning state.",
    "Source comments remain reconstruction annotations rather than direct cognitive measurements.",
    "Phase-1 PDB rival geometry is a frozen search representation, not a model of what the solver considered.",
    "Reconstructor concentration remains a non-ignorable measurement axis.",
    "Cross-source transport is semantic/schema replication only; body-level mechanism replication remains HOLD.",
    "No unrestricted solve-body mirror or raw-public-release authority is created by this phase."
  ],
  next_phase_permission:failures.length===0
};
fs.mkdirSync(outDir,{recursive:true});
fs.writeFileSync(path.join(outDir,"G7-P4-CLOSURE.json"),JSON.stringify(report,null,2)+"\n");
fs.writeFileSync(path.join(outDir,"G7-P4-CLOSURE.md"),[
  "# CUBE-REV Generation VII G7-P4 closure","",
  `**${verdict}**`,"",
  `- pilot exact replay support: ${(pilot.supported_fraction*100).toFixed(1)}%`,
  `- confirmatory exact replay support: ${(conf.supported_fraction*100).toFixed(1)}%`,
  `- annotation-bearing solves: ${annotationBearing}`,
  `- phase-1 single-HTM search events: ${searchEvents}`,
  `- cross-source schema transport: ${cross.semantic_structure_replication}`,
  `- mechanism replication: ${cross.mechanism_replication}`,"",
  "## Support boundary",
  ...report.support_boundary.map(x=>"- "+x)
].join("\n")+"\n");
console.log("G7_P4_CLOSURE_PASS");
console.log("VERDICT\t"+verdict);
console.log("NEXT_PHASE_PERMISSION\t"+(report.next_phase_permission?"YES":"NO"));
