import fs from "node:fs";
import path from "node:path";
const args=process.argv.slice(2);
const val=(k,d=null)=>{const i=args.indexOf(k);return i>=0&&i+1<args.length?args[i+1]:d;};
const pre=JSON.parse(fs.readFileSync(val("--preseal","g7/p5/preseal.json"),"utf8"));
const contact=JSON.parse(fs.readFileSync(val("--contact","g7/p5/contact-constitution.json"),"utf8"));
const audit=JSON.parse(fs.readFileSync(val("--audit"),"utf8"));
const analysis=JSON.parse(fs.readFileSync(val("--analysis"),"utf8"));
const sensitivity=JSON.parse(fs.readFileSync(val("--sensitivity"),"utf8"));
const outDir=val("--out","g7/p5/build");
const blockers=[];
if(!audit.pass) blockers.push("PACKET_AUDIT");
if(audit.trials!==24||audit.pairs!==12) blockers.push("PACKET_SIZE");
if(analysis.authority!=="SYNTHETIC_VALIDATION_ONLY") blockers.push("NON_SYNTHETIC_ANALYSIS");
if(analysis.sessions!==8||analysis.valid_choice_rows!==192) blockers.push("SYNTHETIC_E2E");
if(!(analysis.primary.h3_agreement_rate>analysis.primary.h1_agreement_rate)) blockers.push("POSITIVE_CONTROL_NOT_RECOVERED");
if(sensitivity.authority!=="DESIGN_CALIBRATION_ONLY"||sensitivity.frozen_complete_session_target!==24) blockers.push("SENSITIVITY_NOT_FROZEN");
if(contact.status!=="DESIGN_ONLY_HUMAN_CONTACT_CLOSED") blockers.push("CONTACT_STATUS");
if(pre.human_contact.live_data_collection_authorized_by_this_phase!==false) blockers.push("LIVE_AUTHORITY_DRIFT");
let verdict=blockers.length?"HOLD_INSTRUMENT_OR_IDENTIFICATION_INSUFFICIENT":"PASS_INSTRUMENT_VALIDATED_HUMAN_CONTACT_NOT_YET_OPEN";
if(!pre.terminal_verdicts.includes(verdict)) throw new Error("VERDICT_NOT_PRESEALED");
const report={
 schema_version:"g7-p5-instrument-closure-1",verdict,blockers,
 human_contact_open:false,
 next_substage_permission:!blockers.length,
 evidence:{
   packet_sha256:analysis.packet_sha256,
   packet_trials:audit.trials,
   packet_pairs:audit.pairs,
   distinct_phase1_lb:audit.distinct_phase1_lb,
   side_condition_counts:audit.side_condition_counts,
   synthetic_sessions:analysis.sessions,
   synthetic_choices:analysis.valid_choice_rows,
   synthetic_h1_agreement:analysis.primary.h1_agreement_rate,
   synthetic_h3_agreement:analysis.primary.h3_agreement_rate,
   synthetic_permutation_p:analysis.primary.state_level_label_swap_permutation_p,
   fixed_complete_session_target:sensitivity.frozen_complete_session_target,
   reference_delta_010_sensitivity:sensitivity.reference_cell.estimated_sensitivity
 },
 support_boundary:[
   "Synthetic positive-control recovery validates the pipeline, not a claim about people.",
   "Human contact remains closed until a separate operational authorization is satisfied.",
   "The fixed-N rule is design calibration rather than an empirical effect-size prior.",
   "Representation agreement does not establish literal internal representation."
 ]
};
fs.mkdirSync(outDir,{recursive:true});
fs.writeFileSync(path.join(outDir,"G7-P5-INSTRUMENT-CLOSURE.json"),JSON.stringify(report,null,2)+"\n");
fs.writeFileSync(path.join(outDir,"G7-P5-INSTRUMENT-CLOSURE.md"),[
 "# CUBE-REV G7-P5 instrument-validation closure","",`**${verdict}**`,"",
 `- packet: ${audit.pairs} pairs / ${audit.trials} trials`,
 `- distinct phase-1 LB: ${audit.distinct_phase1_lb}`,
 `- synthetic sessions / choices: ${analysis.sessions} / ${analysis.valid_choice_rows}`,
 `- H1 / H3 positive-control agreement: ${analysis.primary.h1_agreement_rate} / ${analysis.primary.h3_agreement_rate}`,
 `- fixed complete-session target: ${sensitivity.frozen_complete_session_target}`,
 "- human contact open: NO"
].join("\n")+"\n");
console.log("G7_P5_INSTRUMENT_CLOSURE_PASS");
console.log("VERDICT\t"+verdict);
console.log("HUMAN_CONTACT_OPEN\tNO");
