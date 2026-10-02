import fs from "node:fs";
const packet=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));
const out=process.argv[3];
if(!out) throw new Error("output path required");
const failures=[];
const trials=packet.trials;
if(trials.length!==24) failures.push("TRIAL_COUNT");
const byPair=new Map();
for(const t of trials){if(!byPair.has(t.pair_id))byPair.set(t.pair_id,[]);byPair.get(t.pair_id).push(t);}
if(byPair.size!==12) failures.push("PAIR_COUNT");
const sideCondition={A:{NEUTRAL:0,DELIBERATE:0},B:{NEUTRAL:0,DELIBERATE:0}};
const lbs=new Map();
for(const [pair,ts] of byPair){
  if(ts.length!==2) failures.push("PAIR_SIZE:"+pair);
  const sides=new Set(ts.map(x=>x.trial_side));
  if(!(sides.has("A")&&sides.has("B"))) failures.push("PAIR_SIDES:"+pair);
  const l=new Set(ts.map(x=>x.phase1_lb));
  if(l.size!==1) failures.push("PAIR_LB:"+pair);
  const cond=new Set(ts.map(x=>x.condition.display_horizon_condition));
  if(!(cond.has("NEUTRAL")&&cond.has("DELIBERATE"))) failures.push("PAIR_CONDITION:"+pair);
  for(const t of ts){
    const a=t.predictions.H1_PDB_GREEDY.join(",");
    const b=t.predictions.H3_PDB_LOOKAHEAD.join(",");
    if(a===b) failures.push("NO_RIVAL_DISAGREEMENT:"+t.trial_id);
    if(!t.predictions.H1_PDB_GREEDY.length||!t.predictions.H3_PDB_LOOKAHEAD.length) failures.push("EMPTY_RIVAL:"+t.trial_id);
    sideCondition[t.trial_side][t.condition.display_horizon_condition]++;
    lbs.set(t.phase1_lb,(lbs.get(t.phase1_lb)||0)+1);
  }
}
if(sideCondition.A.NEUTRAL!==6||sideCondition.A.DELIBERATE!==6||sideCondition.B.NEUTRAL!==6||sideCondition.B.DELIBERATE!==6) failures.push("SIDE_CONDITION_IMBALANCE");
const states=trials.map(x=>x.state_id);
if(new Set(states).size!==states.length) failures.push("STATE_DUPLICATE");
const seeds=trials.map(x=>x.condition.choice_order_seed);
if(new Set(seeds).size!==seeds.length) failures.push("ORDER_SEED_DUPLICATE");
if(lbs.size<2) failures.push("LB_SUPPORT_TOO_NARROW");

const report={
  schema_version:"g7-p5-packet-audit-1",
  pass:failures.length===0,
  failures,
  trials:trials.length,
  pairs:byPair.size,
  distinct_phase1_lb:lbs.size,
  phase1_lb_counts:Object.fromEntries([...lbs].sort((a,b)=>a[0]-b[0])),
  side_condition_counts:sideCondition,
  unique_states:new Set(states).size,
  unique_choice_order_seeds:new Set(seeds).size,
  rival_disagreement_trials:trials.filter(t=>t.predictions.H1_PDB_GREEDY.join(",")!==t.predictions.H3_PDB_LOOKAHEAD.join(",")).length
};
fs.writeFileSync(out,JSON.stringify(report,null,2)+"\n");
if(failures.length){console.error(failures.join("\n"));process.exit(1);}
console.log("G7_P5_PACKET_AUDIT_PASS");
console.log("PAIRS\t"+report.pairs);
console.log("DISTINCT_LB\t"+report.distinct_phase1_lb);
console.log("SIDE_A_NEUTRAL\t"+sideCondition.A.NEUTRAL);
console.log("SIDE_A_DELIBERATE\t"+sideCondition.A.DELIBERATE);
