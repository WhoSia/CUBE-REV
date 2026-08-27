#!/usr/bin/env python3
from pathlib import Path
import json,hashlib
src=Path('research/0.10.5-r1.7/r17_full_route_court.mjs').read_text(encoding='utf-8')
assert src.count('ess_ge_400:ess>=400,')==1
src=src.replace('ess_ge_400:ess>=400,','ess_ge_200_inherited_from_target_selection:ess>=200,')
src=src.replace("schema_version:'CR0105R17-FULL-ROUTE-ADMISSION-GATE-1'","schema_version:'CR0105R17-IRREDUCIBLE-ROUTE-ADMISSION-GATE-1'")
anchor='// -------- Stage 1: route parsing and state certification only. No redundancy outcomes yet. --------'
insert=r'''function generatorFamily(m){
 const s=String(m||'');
 if(isRotation(s))return null;
 if(/^[URFDLB]/.test(s))return s[0];
 if(/^[urfdlb]/.test(s))return s[0].toUpperCase()+'w';
 if(/^[MES]/.test(s))return s[0];
 return s.replace(/(?:2'?|')$/,'');
}
function isStructuralCandidate(c){
 const fam=new Set(String(c.actual||'').trim().split(/\s+/).filter(Boolean).map(generatorFamily).filter(Boolean));
 return fam.size>=2;
}
function isProperSubinterval(d,c){return d.start>=c.start&&d.end<=c.end&&(d.start>c.start||d.end<c.end);}
function isMinimalIrreducible(c,allCandidates){
 if(!isStructuralCandidate(c))return false;
 // Adversarial R4: any proper algebraically reducible subinterval, even single-generator,
 // disqualifies the enclosing interval from the minimal/primitive phenotype.
 return !allCandidates.some(d=>d.saved_moves>0&&isProperSubinterval(d,c));
}

'''+anchor
assert src.count(anchor)==1
src=src.replace(anchor,insert)
old="const chosen=chooseIntervals(candidates);const faceTurns=moves.filter(isOuterFace).length,nonRot=moves.filter(m=>!isRotation(m)).length;"
new="const algebraicChosen=chooseIntervals(candidates);const structuralCandidates=candidates.filter(isStructuralCandidate);const structuralChosen=chooseIntervals(structuralCandidates);const irreducibleCandidates=structuralCandidates.filter(c=>isMinimalIrreducible(c,candidates));const chosen=chooseIntervals(irreducibleCandidates);const faceTurns=moves.filter(isOuterFace).length,nonRot=moves.filter(m=>!isRotation(m)).length;"
assert src.count(old)==1
src=src.replace(old,new)
old2="o.outcome={candidate_intervals:chosen.candidate_count,selected_nonoverlap_intervals:chosen.selected,total_saved_moves:chosen.total_saved,"
new2="o.outcome={all_algebraic_candidate_intervals:algebraicChosen.candidate_count,all_algebraic_selected_saved_moves:algebraicChosen.total_saved,any_algebraic_redundancy:algebraicChosen.total_saved>0,structural_candidate_intervals:structuralChosen.candidate_count,structural_selected_saved_moves:structuralChosen.total_saved,any_structural_redundancy:structuralChosen.total_saved>0,irreducible_candidate_intervals:chosen.candidate_count,selected_nonoverlap_intervals:chosen.selected,total_saved_moves:chosen.total_saved,"
assert src.count(old2)==1
src=src.replace(old2,new2)
src=src.replace('any_state_verified_redundancy','any_minimal_irreducible_state_verified_redundancy')
src=src.replace('any_redundancy','any_minimal_irreducible_redundancy')
src=src.replace('raw_any_minimal_irreducible_redundancy','raw_any_minimal_irreducible_redundancy')
src=src.replace("'NO_STATE_VERIFIED_REDUNDANCY'","'NO_MINIMAL_IRREDUCIBLE_STATE_VERIFIED_REDUNDANCY'")
src=src.replace("'COMPOUND_STATE_VERIFIED_REDUNDANCY'","'COMPOUND_MINIMAL_IRREDUCIBLE_STATE_VERIFIED_REDUNDANCY'")
src=src.replace("'STATE_VERIFIED_EXACT_LOOP'","'MINIMAL_IRREDUCIBLE_STATE_VERIFIED_EXACT_LOOP'")
src=src.replace("'STATE_VERIFIED_LOCAL_SHORTENING'","'MINIMAL_IRREDUCIBLE_STATE_VERIFIED_LOCAL_SHORTENING'")
src=src.replace("schema_version:'CR0105R17-FULL-ROUTE-COURT-1'","schema_version:'CR0105R17-IRREDUCIBLE-ROUTE-COURT-1'")
src=src.replace("overlap_rule:'weighted interval scheduling maximizes saved non-overlapping move tokens; overlapping candidate windows are never summed'","irreducibility_filter:'Candidate must be multi-generator and contain no proper contiguous subinterval that itself has any detected exact shortening/identity relation; this is an adversarial post-R3 sensitivity definition, not a preregistered primary phenotype.',overlap_rule:'weighted interval scheduling is rerun on minimal irreducible candidates and maximizes saved non-overlapping move tokens; overlapping windows are never summed'")
marker='const methodSummary={};'
insert2="const hierarchyComparison={raw_any_algebraic:rawMean(o=>o.outcome.any_algebraic_redundancy?1:0),standardized_any_algebraic:estimate(o=>o.outcome.any_algebraic_redundancy?1:0),raw_any_structural:rawMean(o=>o.outcome.any_structural_redundancy?1:0),standardized_any_structural:estimate(o=>o.outcome.any_structural_redundancy?1:0),raw_algebraic_saved:rawMean(o=>o.outcome.all_algebraic_selected_saved_moves),standardized_algebraic_saved:estimate(o=>o.outcome.all_algebraic_selected_saved_moves),raw_structural_saved:rawMean(o=>o.outcome.structural_selected_saved_moves),standardized_structural_saved:estimate(o=>o.outcome.structural_selected_saved_moves)};\n"+marker
assert src.count(marker)==1
src=src.replace(marker,insert2)
src=src.replace('metrics,phenotype_counts:','metrics,hierarchy_comparison:hierarchyComparison,phenotype_counts:')
runtime=Path('research/0.10.5-r1.7/r17_irreducible_route_r4_runtime.mjs');runtime.write_text(src,encoding='utf-8')
pre={'schema_version':'CR0105R17-IRREDUCIBLE-FILTER-POSTHOC-RAVEL-1','status':'PASS_ADVERSARIAL_SENSITIVITY_FREEZE','role':'POSTHOC_ADVERSARIAL_ROBUSTNESS_NOT_PRIMARY_PREREGISTRATION','source_sample_manifest_sha256':hashlib.sha256(Path('research/0.10.5-r1.7/evidence-full-route/FULL_ROUTE_SAMPLE_MANIFEST.json').read_bytes()).hexdigest(),'source_r3_sha256':hashlib.sha256(Path('research/0.10.5-r1.7/evidence-full-route-r3/FULL_ROUTE_COURT.json').read_bytes()).hexdigest(),'motivation':'R3 multi-generator shortening remained common; test whether enclosing windows are merely wrappers around smaller algebraic cancellations.','filter':'Multi-generator candidate with no proper contiguous subinterval that is itself any detected exact shortening or identity relation.','outcome_role':'Sensitivity boundary only. Do not retroactively call this preregistered primary.', 'human_observations':0}
Path('/tmp/r17r4').mkdir(parents=True,exist_ok=True);Path('/tmp/r17r4/IRREDUCIBLE_FILTER_FREEZE.json').write_text(json.dumps(pre,indent=2)+'\n');print(json.dumps(pre,indent=2))
