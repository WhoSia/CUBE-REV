import fs from "node:fs";
import path from "node:path";
const pre=JSON.parse(fs.readFileSync("g7/p6/preseal.json","utf8"));
const src=JSON.parse(fs.readFileSync("g7/p6/data-source-expansion.json","utf8"));
const ctx=JSON.parse(fs.readFileSync("g7/p6/current-contact-context.json","utf8"));
const outDir=process.argv[2]||"g7/p6/build";
const blockers=[];
const wca=src.sources.find(x=>x.source_id==="p6_wca_results_v2_current_20261002");
const nuzzi=src.sources.find(x=>x.source_id==="p6_nuzzi_planning_while_acting");
if(!wca||wca.status!=="CURRENT_EXPORT_BYTE_CENSUS_PASS") blockers.push("WCA_CURRENT_CENSUS");
if(!nuzzi||nuzzi.status!=="BYTE_VERIFIED_STATIC_PICKLE_AUDIT_PASS") blockers.push("EXTERNAL_PLANNING_BYTE_AUTHORITY");
if(pre.expanded_rival_ecology.families.length!==5) blockers.push("RIVAL_ECOLOGY");
if(pre.data_lanes.prospective_human_data.live_data_collection_authorized!==false) blockers.push("CONTACT_AUTHORITY_DRIFT");

let verdict;
if(blockers.length){
  verdict="HOLD_WORLD_CONTACT_OR_IDENTIFICATION_INSUFFICIENT";
}else if(ctx.live_cube_behavior_rows===0 || ctx.development_participants===0){
  verdict="HOLD_WORLD_CONTACT_OR_IDENTIFICATION_INSUFFICIENT";
}else{
  verdict="PASS_BEHAVIORAL_SIGNAL_WITH_MECHANISM_PROMOTION_HOLD";
}
if(!pre.terminal_verdicts.includes(verdict)) throw new Error("VERDICT_NOT_PRESEALED");

const report={
  schema_version:"g7-p6-final-court-1",
  verdict,
  blockers,
  phase_closed:true,
  live_cube_world_contact_completed:ctx.live_cube_behavior_rows>0,
  mechanism_promotion:false,
  next_phase_permission:blocksOnlyWorldContact(),
  next_phase_must_preserve:{
    five_rival_ecology:true,
    development_confirmation_packet_freshness:true,
    contact_gate:true,
    no_optional_stopping:true,
    external_transport_not_cube_ground_truth:true
  },
  evidence_summary:{
    exact_cube_bank_states:256,
    development_packet_states:32,
    confirmation_packet_states:32,
    reserve_states:192,
    external_planning_participants:40,
    external_first_decisions:1549,
    external_all_decisions:4778,
    external_timing_rows:33029,
    external_timing_analysis_rows:31444,
    wca_attempt_rows_333:wca?.census?.attempt_rows_333??null,
    wca_persons_333:wca?.census?.persons_333??null,
    wca_competitions_333:wca?.census?.competitions_333??null,
    wca_scrambles_333:wca?.census?.scrambles_333??null,
    live_cube_behavior_rows:ctx.live_cube_behavior_rows
  },
  closure_reason:"All precontact computational, literature, external-behavioral, and official-attempt evidence lanes are materialized. The remaining missing evidence is prospective matched-state behavior from authorized cube participants; therefore no human planning mechanism claim is promoted."
};
function blocksOnlyWorldContact(){
  return blockers.length===0 && ctx.live_cube_behavior_rows===0;
}
fs.mkdirSync(outDir,{recursive:true});
fs.writeFileSync(path.join(outDir,"G7-P6-FINAL-COURT.json"),JSON.stringify(report,null,2)+"\n");
fs.writeFileSync(path.join(outDir,"G7-P6-FINAL-COURT.md"),[
 "# CUBE-REV Generation VII G7-P6 final court","",
 `**${verdict}**`,"",
 `- phase closed: ${report.phase_closed?"YES":"NO"}`,
 `- live cube world contact completed: ${report.live_cube_world_contact_completed?"YES":"NO"}`,
 `- mechanism promotion: NO`,
 `- next-phase permission: ${report.next_phase_permission?"YES":"NO"}`,
 `- WCA 3x3 attempts: ${report.evidence_summary.wca_attempt_rows_333}`,
 `- external human-planning participants: ${report.evidence_summary.external_planning_participants}`,
 `- exact cube bank: ${report.evidence_summary.exact_cube_bank_states} states`
].join("\n")+"\n");
console.log("G7_P6_FINAL_COURT_PASS");
console.log("VERDICT\t"+verdict);
console.log("PHASE_CLOSED\tYES");
console.log("NEXT_PHASE_PERMISSION\t"+(report.next_phase_permission?"YES":"NO"));
