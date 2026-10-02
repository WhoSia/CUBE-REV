import fs from "node:fs";
import path from "node:path";

const args=process.argv.slice(2);
const val=(k,d=null)=>{const i=args.indexOf(k);return i>=0&&i+1<args.length?args[i+1]:d;};
const instrument=JSON.parse(fs.readFileSync(val("--instrument"),"utf8"));
const fresh=JSON.parse(fs.readFileSync(val("--fresh"),"utf8"));
const court=JSON.parse(fs.readFileSync(val("--court","g7/p5/rival-ecology-court.json"),"utf8"));
const contact=JSON.parse(fs.readFileSync(val("--contact","g7/p5/contact-constitution.json"),"utf8"));
const ecoLines=fs.readFileSync(val("--ecology"),"utf8").trim().split(/\r?\n/).filter(Boolean);
const metrics={};
const lb=[];
for(const line of ecoLines){
  const p=line.split("\t");
  if(p[0]==="LB"){lb.push({lb:Number(p[1]),states:Number(p[2]),h1_h3_disagree_rate:Number(p[3]),h2_unique_rate:Number(p[4]),component_unique_rate:Number(p[5])});}
  else if(p.length===2 && p[0]!=="G7_P5_RIVAL_ECOLOGY_PASS") metrics[p[0]]=Number(p[1]);
}
const blockers=[];
if(instrument.verdict!=="PASS_INSTRUMENT_VALIDATED_HUMAN_CONTACT_NOT_YET_OPEN") blockers.push("INSTRUMENT_CLOSURE");
if(instrument.human_contact_open!==false) blockers.push("CONTACT_ALREADY_OPEN");
if(fresh.conclusion!=="PASS_TWO_SEED_PACKET_CONSTITUTION_REPLICATION") blockers.push("FRESH_PACKET");
if(metrics.STATES<(court.support_population.minimum_states??3000)) blockers.push("ECOLOGY_SUPPORT");
if(contact.status!=="DESIGN_ONLY_HUMAN_CONTACT_CLOSED") blockers.push("CONTACT_CONSTITUTION");

const h2Threshold=court.promotion_rules.h2_counts_as_independent_rival_if_unique_rate_gte;
const compThreshold=court.promotion_rules.component_family_counts_as_independent_rival_if_unique_rate_gte;
const h2Promoted=(metrics.H2_UNIQUE_RATE??0)>=h2Threshold;
const componentPromoted=(metrics.COMPONENT_UNIQUE_RATE??0)>=compThreshold;
const expanded=h2Promoted||componentPromoted;

const verdict=blockers.length
  ? "HOLD_INSTRUMENT_OR_IDENTIFICATION_INSUFFICIENT"
  : "PASS_INSTRUMENT_VALIDATED_HUMAN_CONTACT_NOT_YET_OPEN";

const report={
  schema_version:"g7-p5-final-precontact-1",
  verdict,
  blockers,
  p5_close_recommended:blockers.length===0,
  human_contact_executed:false,
  human_contact_open:false,
  next_phase_permission:blockers.length===0,
  expanded_rival_ecology_required_next_phase:expanded,
  promoted_rivals:{
    H2_PDB_LOOKAHEAD:h2Promoted,
    PHASE1_COMPONENT_FAMILY:componentPromoted
  },
  ecology:{
    states:metrics.STATES,
    h1_h3_disagree_rate:metrics.H1_H3_DISAGREE_RATE,
    h1_h2_disagree_rate:metrics.H1_H2_DISAGREE_RATE,
    h2_h3_disagree_rate:metrics.H2_H3_DISAGREE_RATE,
    h2_unique_rate:metrics.H2_UNIQUE_RATE,
    twist_slice_vs_flip_slice_disagree_rate:metrics.TS_FS_DISAGREE_RATE,
    component_unique_rate:metrics.COMPONENT_UNIQUE_RATE,
    jaccard_h1_h3:metrics.JACCARD_H1_H3,
    by_lower_bound:lb
  },
  phase_boundary:{
    p5_scope_closed_as:"prospective instrument constitution and validation",
    deferred_to_next_phase:[
      "live prospective participant execution",
      ...(expanded?["expanded rival-representation ecology beyond the validated H1-vs-H3 packet"]:[]),
      "fresh-participant or fresh-packet behavioral replication",
      "mechanism-promotion court on actual prospective behavior"
    ],
    reason:"Changing the validated P5 packet after the outcome-blind rival-ecology census would mix instrument constitution with the next empirical challenge."
  }
};
const outDir=val("--out","g7/p5/build");
fs.mkdirSync(outDir,{recursive:true});
fs.writeFileSync(path.join(outDir,"G7-P5-FINAL-PRECONTACT.json"),JSON.stringify(report,null,2)+"\n");
fs.writeFileSync(path.join(outDir,"G7-P5-FINAL-PRECONTACT.md"),[
  "# CUBE-REV Generation VII G7-P5 final precontact court","",
  `**${verdict}**`,"",
  `- ecology states: ${report.ecology.states}`,
  `- H2 independent rival promoted: ${h2Promoted?"YES":"NO"}`,
  `- component family promoted: ${componentPromoted?"YES":"NO"}`,
  `- expanded ecology required next phase: ${expanded?"YES":"NO"}`,
  `- human contact executed: NO`,
  `- P5 close recommended: ${report.p5_close_recommended?"YES":"NO"}`
].join("\n")+"\n");
console.log("G7_P5_FINAL_PRECONTACT_COURT_PASS");
console.log("VERDICT\t"+verdict);
console.log("H2_PROMOTED\t"+(h2Promoted?"YES":"NO"));
console.log("COMPONENT_PROMOTED\t"+(componentPromoted?"YES":"NO"));
console.log("EXPANDED_ECOLOGY_NEXT_PHASE\t"+(expanded?"YES":"NO"));
console.log("P5_CLOSE_RECOMMENDED\t"+(report.p5_close_recommended?"YES":"NO"));
