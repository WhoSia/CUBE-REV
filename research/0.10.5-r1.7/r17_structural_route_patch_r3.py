#!/usr/bin/env python3
from pathlib import Path
import json
src=Path('research/0.10.5-r1.7/r17_full_route_court.mjs').read_text(encoding='utf-8')
# Inherit the prospectively declared target-selection gate, exactly as R2.
assert src.count('ess_ge_400:ess>=400,')==1
src=src.replace('ess_ge_400:ess>=400,','ess_ge_200_inherited_from_target_selection:ess>=200,')
src=src.replace("schema_version:'CR0105R17-FULL-ROUTE-ADMISSION-GATE-1'","schema_version:'CR0105R17-STRUCTURAL-ROUTE-ADMISSION-GATE-1'")
# Define a stricter route-structure phenotype before any outcome calculation.
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

'''+anchor
assert src.count(anchor)==1
src=src.replace(anchor,insert)
old="const chosen=chooseIntervals(candidates);const faceTurns=moves.filter(isOuterFace).length,nonRot=moves.filter(m=>!isRotation(m)).length;"
new="const algebraicChosen=chooseIntervals(candidates);const structuralCandidates=candidates.filter(isStructuralCandidate);const chosen=chooseIntervals(structuralCandidates);const faceTurns=moves.filter(isOuterFace).length,nonRot=moves.filter(m=>!isRotation(m)).length;"
assert src.count(old)==1
src=src.replace(old,new)
old2="o.outcome={candidate_intervals:chosen.candidate_count,selected_nonoverlap_intervals:chosen.selected,total_saved_moves:chosen.total_saved,"
new2="o.outcome={all_algebraic_candidate_intervals:algebraicChosen.candidate_count,all_algebraic_selected_saved_moves:algebraicChosen.total_saved,any_algebraic_redundancy:algebraicChosen.total_saved>0,structural_candidate_intervals:chosen.candidate_count,selected_nonoverlap_intervals:chosen.selected,total_saved_moves:chosen.total_saved,"
assert src.count(old2)==1
src=src.replace(old2,new2)
# Rename the primary outcome everywhere so the R2 algebraic phenotype cannot be confused with R3 structural phenotype.
src=src.replace('any_state_verified_redundancy','any_multi_generator_state_verified_redundancy')
src=src.replace('any_redundancy','any_structural_redundancy')
src=src.replace('raw_any_structural_redundancy','raw_any_multi_generator_redundancy')
src=src.replace("'NO_STATE_VERIFIED_REDUNDANCY'","'NO_MULTI_GENERATOR_STATE_VERIFIED_REDUNDANCY'")
src=src.replace("'COMPOUND_STATE_VERIFIED_REDUNDANCY'","'COMPOUND_MULTI_GENERATOR_STATE_VERIFIED_REDUNDANCY'")
src=src.replace("'STATE_VERIFIED_EXACT_LOOP'","'MULTI_GENERATOR_STATE_VERIFIED_EXACT_LOOP'")
src=src.replace("'STATE_VERIFIED_LOCAL_SHORTENING'","'MULTI_GENERATOR_STATE_VERIFIED_LOCAL_SHORTENING'")
src=src.replace("schema_version:'CR0105R17-FULL-ROUTE-COURT-1'","schema_version:'CR0105R17-STRUCTURAL-ROUTE-COURT-1'")
# Add an explicit structural filter to the immutable phenotype definition.
src=src.replace("overlap_rule:'weighted interval scheduling maximizes saved non-overlapping move tokens; overlapping candidate windows are never summed'","structural_filter:'Primary R3 phenotype requires at least two distinct non-rotation move-generator families in the actual interval; single-generator algebraic compression/cancellation is excluded.',overlap_rule:'weighted interval scheduling is rerun after the structural filter and maximizes saved non-overlapping move tokens; overlapping candidate windows are never summed'")
# Preserve R2 algebraic prevalence as a comparison, but do not bootstrap/promote it as the R3 primary metric.
marker="const methodSummary={};"
insert2="const algebraicComparison={raw_any_algebraic_redundancy:rawMean(o=>o.outcome.any_algebraic_redundancy?1:0),standardized_any_algebraic_redundancy:estimate(o=>o.outcome.any_algebraic_redundancy?1:0),raw_algebraic_saved_moves:rawMean(o=>o.outcome.all_algebraic_selected_saved_moves),standardized_algebraic_saved_moves:estimate(o=>o.outcome.all_algebraic_selected_saved_moves)};\n"+marker
assert src.count(marker)==1
src=src.replace(marker,insert2)
src=src.replace("metrics,phenotype_counts:","metrics,algebraic_comparison:algebraicComparison,phenotype_counts:")
runtime=Path('research/0.10.5-r1.7/r17_structural_route_r3_runtime.mjs')
runtime.write_text(src,encoding='utf-8')
pre={
 'schema_version':'CR0105R17-STRUCTURAL-FILTER-PREOUTCOME-1','status':'PASS_PREOUTCOME_FILTER_FREEZE',
 'source_manifest_sha256':__import__('hashlib').sha256(Path('research/0.10.5-r1.7/evidence-full-route/FULL_ROUTE_SAMPLE_MANIFEST.json').read_bytes()).hexdigest(),
 'source_r2_court_sha256':__import__('hashlib').sha256(Path('research/0.10.5-r1.7/evidence-full-route-r2/FULL_ROUTE_COURT.json').read_bytes()).hexdigest(),
 'motivation_seen':'R2 algebraic phenotype was high; no individual R3 structural outcomes were computed before this filter was declared.',
 'primary_structural_filter':'At least two distinct non-rotation move-generator families in candidate actual interval.',
 'single_generator_policy':'Retain R2 as algebraic-compression sensitivity only; exclude from R3 primary structural phenotype.',
 'scheduling_policy':'Re-run weighted interval scheduling after filtering; do not merely delete chosen R2 intervals.',
 'human_observations':0
}
Path('/tmp/r17r3').mkdir(parents=True,exist_ok=True)
Path('/tmp/r17r3/STRUCTURAL_FILTER_PREOUTCOME.json').write_text(json.dumps(pre,indent=2)+'\n')
print(json.dumps(pre,indent=2))
