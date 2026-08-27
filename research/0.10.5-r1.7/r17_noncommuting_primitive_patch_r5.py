#!/usr/bin/env python3
from pathlib import Path
import json,hashlib
src=Path('research/0.10.5-r1.7/r17_full_route_court.mjs').read_text(encoding='utf-8')
assert src.count('ess_ge_400:ess>=400,')==1
src=src.replace('ess_ge_400:ess>=400,','ess_ge_200_inherited_from_target_selection:ess>=200,')
src=src.replace("schema_version:'CR0105R17-FULL-ROUTE-ADMISSION-GATE-1'","schema_version:'CR0105R17-NONCOMMUTING-PRIMITIVE-ADMISSION-GATE-1'")
anchor='// -------- Stage 1: route parsing and state certification only. No redundancy outcomes yet. --------'
insert=r'''function outerFaceFamily(m){
 const s=String(m||'');
 return /^[URFDLB](?:2'?|')?$/.test(s)?s[0]:null;
}
const oppositeFace={U:'D',D:'U',R:'L',L:'R',F:'B',B:'F'};
function hasNoncommutingOuterFacePair(c){
 const ms=String(c.actual||'').trim().split(/\s+/).filter(Boolean);
 if(!ms.length||!ms.every(m=>outerFaceFamily(m)!==null))return false;
 const fs=[...new Set(ms.map(outerFaceFamily))];
 if(fs.length<2)return false;
 for(let i=0;i<fs.length;i++)for(let j=i+1;j<fs.length;j++){
   if(oppositeFace[fs[i]]!==fs[j])return true;
 }
 return false;
}
function isProperSubinterval(d,c){return d.start>=c.start&&d.end<=c.end&&(d.start>c.start||d.end<c.end);}
function isMinimalIrreducible(c,allCandidates){
 return !allCandidates.some(d=>d.saved_moves>0&&isProperSubinterval(d,c));
}
function isNoncommutingPrimitive(c,allCandidates){
 return hasNoncommutingOuterFacePair(c)&&isMinimalIrreducible(c,allCandidates);
}

'''+anchor
assert src.count(anchor)==1
src=src.replace(anchor,insert)
old="const chosen=chooseIntervals(candidates);const faceTurns=moves.filter(isOuterFace).length,nonRot=moves.filter(m=>!isRotation(m)).length;"
new="const algebraicChosen=chooseIntervals(candidates);const primitiveCandidates=candidates.filter(c=>isNoncommutingPrimitive(c,candidates));const chosen=chooseIntervals(primitiveCandidates);const faceTurns=moves.filter(isOuterFace).length,nonRot=moves.filter(m=>!isRotation(m)).length;"
assert src.count(old)==1
src=src.replace(old,new)
old2="o.outcome={candidate_intervals:chosen.candidate_count,selected_nonoverlap_intervals:chosen.selected,total_saved_moves:chosen.total_saved,"
new2="o.outcome={all_algebraic_candidate_intervals:algebraicChosen.candidate_count,all_algebraic_selected_saved_moves:algebraicChosen.total_saved,any_algebraic_redundancy:algebraicChosen.total_saved>0,noncommuting_primitive_candidate_intervals:chosen.candidate_count,selected_nonoverlap_intervals:chosen.selected,total_saved_moves:chosen.total_saved,"
assert src.count(old2)==1
src=src.replace(old2,new2)
src=src.replace('any_state_verified_redundancy','any_noncommuting_primitive_state_verified_redundancy')
src=src.replace('any_redundancy','any_noncommuting_primitive_redundancy')
src=src.replace("'NO_STATE_VERIFIED_REDUNDANCY'","'NO_NONCOMMUTING_PRIMITIVE_STATE_VERIFIED_REDUNDANCY'")
src=src.replace("'COMPOUND_STATE_VERIFIED_REDUNDANCY'","'COMPOUND_NONCOMMUTING_PRIMITIVE_STATE_VERIFIED_REDUNDANCY'")
src=src.replace("'STATE_VERIFIED_EXACT_LOOP'","'NONCOMMUTING_PRIMITIVE_STATE_VERIFIED_EXACT_LOOP'")
src=src.replace("'STATE_VERIFIED_LOCAL_SHORTENING'","'NONCOMMUTING_PRIMITIVE_STATE_VERIFIED_LOCAL_SHORTENING'")
src=src.replace("schema_version:'CR0105R17-FULL-ROUTE-COURT-1'","schema_version:'CR0105R17-NONCOMMUTING-PRIMITIVE-ROUTE-COURT-1'")
src=src.replace("overlap_rule:'weighted interval scheduling maximizes saved non-overlapping move tokens; overlapping candidate windows are never summed'","primitive_filter:'Posthoc adversarial R5: candidate must use ordinary outer-face turns only, contain at least one pair of non-opposite generator families (hence noncommuting on the 3x3), and contain no proper contiguous subinterval with any detected exact shortening/identity relation.',overlap_rule:'weighted interval scheduling is rerun after the noncommuting-primitive filter; overlapping candidate windows are never summed'")
marker='const methodSummary={};'
insert2="const algebraicComparison={raw_any_algebraic:rawMean(o=>o.outcome.any_algebraic_redundancy?1:0),standardized_any_algebraic:estimate(o=>o.outcome.any_algebraic_redundancy?1:0),raw_algebraic_saved:rawMean(o=>o.outcome.all_algebraic_selected_saved_moves),standardized_algebraic_saved:estimate(o=>o.outcome.all_algebraic_selected_saved_moves)};\n"+marker
assert src.count(marker)==1
src=src.replace(marker,insert2)
src=src.replace('metrics,phenotype_counts:','metrics,algebraic_comparison:algebraicComparison,phenotype_counts:')
runtime=Path('research/0.10.5-r1.7/r17_noncommuting_primitive_r5_runtime.mjs');runtime.write_text(src,encoding='utf-8')
pre={'schema_version':'CR0105R17-NONCOMMUTING-PRIMITIVE-FILTER-POSTHOC-1','status':'PASS_ADVERSARIAL_SENSITIVITY_FREEZE','role':'POSTHOC_ADVERSARIAL_ROBUSTNESS_NOT_PRIMARY_PREREGISTRATION','source_sample_manifest_sha256':hashlib.sha256(Path('research/0.10.5-r1.7/evidence-full-route/FULL_ROUTE_SAMPLE_MANIFEST.json').read_bytes()).hexdigest(),'source_r4_candidate_audit_sha256':hashlib.sha256(Path('research/0.10.5-r1.7/evidence-irred-audit/IRREDUCIBLE_CANDIDATE_AUDIT.json').read_bytes()).hexdigest(),'motivation':'R4 surviving intervals were dominated by opposite-face commutation normalizations and rotation/slice representation identities.','filter':'Ordinary outer-face turns only; at least one pair of distinct non-opposite face families; no proper contiguous subinterval with any detected exact shortening or identity relation.','excluded_examples':['U\' D\' U\' -> D\' U2 (U/D commute)','L\' R L -> R (L/R commute)','M\' r\' R -> identity (slice/wide representation)','d\' y\' U -> identity (rotation/wide representation)'],'outcome_role':'Adversarial sensitivity only. A zero or near-zero result is evidence that R4 did not isolate noncommuting primitive detours; it is not proof that human recovery never occurs.','human_observations':0}
Path('/tmp/r17r5').mkdir(parents=True,exist_ok=True);Path('/tmp/r17r5/NONCOMMUTING_PRIMITIVE_FILTER_FREEZE.json').write_text(json.dumps(pre,indent=2)+'\n');print(json.dumps(pre,indent=2))
