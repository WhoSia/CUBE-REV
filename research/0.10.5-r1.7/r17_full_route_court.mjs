import fs from 'node:fs';
import crypto from 'node:crypto';
import { Alg } from 'cubing/alg';
import { cube3x3x3 } from 'cubing/puzzles';

const root=process.env.R17_FULL_ROOT||'/tmp/r17full';
const manifest=JSON.parse(fs.readFileSync(`${root}/FULL_ROUTE_SAMPLE_MANIFEST.json`,'utf8'));
const kp=await cube3x3x3.kpuzzle();
const OUT=`${root}/route`;
fs.mkdirSync(OUT,{recursive:true});

function stable(x){if(Array.isArray(x))return '['+x.map(stable).join(',')+']';if(x&&typeof x==='object')return '{'+Object.keys(x).sort().map(k=>JSON.stringify(k)+':'+stable(x[k])).join(',')+'}';return JSON.stringify(x)}
function thash(t){return crypto.createHash('sha256').update(stable(t.transformationData)).digest('hex')}
function physicalSolved(t){return kp.defaultPattern().applyTransformation(t).experimentalIsSolved({ignorePuzzleOrientation:true,ignoreCenterOrientation:true});}
const isRotation=m=>/^[xyz](?:2'?|')?$/.test(m);
const isOuterFace=m=>/^[URFDLB](?:2'?|')?$/.test(m);

const patterns={
 INSPECTION:[/\binspection\b/i],
 CROSS:[/\b(?:cross|xcross|xxcross|xxxcross)\b/i,/\bpseudo\s+cross\b/i,/\bmissed\s+cross\b/i],
 F2L:[/\bf2l\b/i,/\b(?:1st|2nd|3rd|4th|first|second|third|fourth)\s*(?:\/\s*)?pair/i,/\bpairs?\b/i,/\bzbls\b/i,/\bsvls\b/i],
 LL_ORIENT:[/\boll(?:\b|cp)/i,/\beoll\b/i,/\bcoll\b/i,/\bollcp\b/i],
 LL_PERMUTE:[/\bpll\b/i,/\bepll\b/i,/\bauf\b/i],
 LL_ONELOOK:[/\bzbll\b/i,/\b2gll\b/i,/\bell\b/i,/\bcll\b/i],
 ROUX_FB:[/\bfb\b/i,/\bfbdr\b/i,/\bpseudo\s+fb\b/i],
 ROUX_SB:[/\bsb\b/i,/\bss\b/i,/\bsp\b/i,/\bflipped\s+sp\b/i],
 ROUX_CMLL:[/\bcmll\b/i],
 ROUX_LSE:[/\blse\b/i,/\beolr\b/i,/\beolrb\b/i,/\bep\b/i],
};
function classify(method,comment){
 const c=String(comment||'').trim().toLowerCase();if(!c)return {phase:'UNKNOWN',hits:[]};
 let hits=[];for(const [phase,ps] of Object.entries(patterns))if(ps.some(p=>p.test(c)))hits.push(phase);
 if(method!=='Roux')hits=hits.filter(x=>!x.startsWith('ROUX_'));
 if(method==='Roux'&&hits.includes('LL_ONELOOK')&&/\bcll\b/i.test(c)&&!hits.includes('ROUX_CMLL')){hits=hits.filter(x=>x!=='LL_ONELOOK');hits.push('ROUX_CMLL');}
 hits=[...new Set(hits)];
 return {phase:hits.length===1?hits[0]:(hits.length?'AMBIGUOUS':'UNKNOWN'),hits};
}
function parseAnnotated(raw,method){
 const tokens=[],lines=[];let lineId=0;
 for(const rawLine of String(raw||'').split(/\r?\n/)){
   const idx=rawLine.indexOf('//'); const left=(idx>=0?rawLine.slice(0,idx):rawLine).trim(); const comment=(idx>=0?rawLine.slice(idx+2):'').trim();
   if(!left&&!comment)continue;
   const cls=classify(method,comment);let moves=[];
   if(left){const a=Alg.fromString(left).expand();moves=Array.from(a.experimentalLeafMoves()).map(m=>m.toString());}
   const start=tokens.length;for(const m of moves)tokens.push({move:m,phase:cls.phase,line_id:lineId,comment});
   lines.push({line_id:lineId,start,end:tokens.length,comment,phase:cls.phase,hits:cls.hits,moves});lineId++;
 }
 return {tokens,lines};
}

// <=3-turn exact alternatives for ordinary outer face moves only.
const faceMoves=[];for(const f of ['U','R','F','D','L','B'])for(const s of ['', '2', "'"])faceMoves.push(f+s);
const shortest=new Map();
function faceOf(m){return m[0]}
function addShortest(seq){const t=seq.length?kp.algToTransformation(seq.join(' ')):kp.identityTransformation();const h=thash(t),p=shortest.get(h);if(!p||seq.length<p.length||(seq.length===p.length&&seq.join(' ')<p.join(' ')))shortest.set(h,[...seq]);}
addShortest([]);for(const a of faceMoves)addShortest([a]);for(const a of faceMoves)for(const b of faceMoves)if(faceOf(a)!==faceOf(b))addShortest([a,b]);for(const a of faceMoves)for(const b of faceMoves)for(const c of faceMoves)if(faceOf(a)!==faceOf(b)&&faceOf(b)!==faceOf(c))addShortest([a,b,c]);

function candidateKey(c){return `${c.start}:${c.end}`}
function chooseIntervals(cands){
  const ded=new Map();
  for(const c of cands){const k=candidateKey(c),p=ded.get(k);if(!p||c.saved_moves>p.saved_moves||(c.saved_moves===p.saved_moves&&c.kind==='EXACT_LOOP'&&p.kind!=='EXACT_LOOP'))ded.set(k,c);}
  const a=[...ded.values()].sort((x,y)=>x.end-y.end||x.start-y.start||y.saved_moves-x.saved_moves);
  const prev=a.map((c,i)=>{let j=i-1;while(j>=0&&a[j].end>c.start)j--;return j;});
  const dp=new Array(a.length+1).fill(0),cnt=new Array(a.length+1).fill(0),take=new Array(a.length).fill(false);
  for(let i=1;i<=a.length;i++){
    const c=a[i-1],j=prev[i-1]+1,yes=dp[j]+c.saved_moves,yesCnt=cnt[j]+1,no=dp[i-1],noCnt=cnt[i-1];
    if(yes>no||(yes===no&&yesCnt<noCnt)){dp[i]=yes;cnt[i]=yesCnt;take[i-1]=true;}else{dp[i]=no;cnt[i]=noCnt;}
  }
  const sel=[];let i=a.length-1;while(i>=0){const c=a[i],j=prev[i]+1;if(dp[i+1]===dp[j]+c.saved_moves&&cnt[i+1]===cnt[j]+1){sel.push(c);i=prev[i];}else i--;}
  sel.reverse();return {selected:sel,total_saved:dp[a.length],candidate_count:a.length};
}
function quantile(xs,q){if(!xs.length)return null;const a=[...xs].sort((x,y)=>x-y);return a[Math.min(a.length-1,Math.floor(q*(a.length-1)))];}

// -------- Stage 1: route parsing and state certification only. No redundancy outcomes yet. --------
const admission=[];const cellCert=new Map();let sourceN=0,parseN=0,certN=0;
const targetCell=new Map(manifest.target_cells.filter(c=>c.supported).map(c=>[`${c.speed}|${c.era}`,c]));
for(const r of manifest.records){
 const o={reco_id:r.reco_id,result_id:r.result_id,attempt_number:r.attempt_number,attempt_value:r.attempt_value,comp_year:r.comp_year,speed:r.speed,era:r.era,cell:r.cell,method:r.method,route_source_status:r.route_source_status};
 if(r.route_source_status!=='RAW_ALG_CUBING_LINK'){o.admission='NO_ROUTE_SOURCE';admission.push(o);continue;}sourceN++;
 try{
   const parsed=parseAnnotated(r.raw_alg,r.method);const moveString=parsed.tokens.map(x=>x.move).join(' ');
   const rawT=kp.algToTransformation(r.raw_alg),expandedT=kp.algToTransformation(moveString),setupT=kp.algToTransformation(r.raw_setup),endT=setupT.applyTransformation(rawT);
   o.raw_expanded_transform_equal=rawT.isIdentical(expandedT);o.expanded_move_count=parsed.tokens.length;o.phase_lines=parsed.lines.length;o.state_solved=physicalSolved(endT);o.parse_ok=true;parseN++;
   if(!o.raw_expanded_transform_equal){o.admission='EXPANSION_TRANSFORM_MISMATCH';admission.push(o);continue;}
   if(!o.state_solved){o.admission='STATE_UNCERTIFIED';admission.push(o);continue;}
   o.admission='STATE_CERTIFIED';o._parsed=parsed;o._setupT=setupT;o._endT=endT;o._record=r;certN++;
   cellCert.set(r.cell,(cellCert.get(r.cell)||0)+1);admission.push(o);
 }catch(e){o.admission='PARSE_ERROR';o.error=String(e?.stack||e).slice(0,800);admission.push(o);}
}
const coveredCells=[...targetCell.entries()].filter(([k])=>(cellCert.get(k)||0)>0);const coveredPop=coveredCells.reduce((s,[,c])=>s+c.population_n,0);const targetTotal=manifest.target_population_under10;
const rawWeights=[];for(const [k,c] of coveredCells){const n=cellCert.get(k);for(let i=0;i<n;i++)rawWeights.push(c.population_n/n);}
const meanW=rawWeights.reduce((a,b)=>a+b,0)/Math.max(1,rawWeights.length);const stab=rawWeights.map(w=>w/meanW);const sumW=stab.reduce((a,b)=>a+b,0),sumW2=stab.reduce((a,b)=>a+b*b,0);const ess=sumW*sumW/Math.max(1e-12,sumW2);
const sortedW=[...stab].sort((a,b)=>a-b);
const routeSourceRate=sourceN/manifest.sample_n,parseRate=parseN/Math.max(1,sourceN),certRate=certN/Math.max(1,parseN),coverage=coveredPop/targetTotal;
const gateChecks={
 sample_n_exact:manifest.sample_n===900,
 route_source_rate_ge_0_95:routeSourceRate>=0.95,
 parse_rate_ge_0_95:parseRate>=0.95,
 state_certification_rate_ge_0_85:certRate>=0.85,
 state_certified_n_ge_650:certN>=650,
 target_population_coverage_ge_0_95:coverage>=0.95,
 ess_ge_400:ess>=400,
 stabilized_p99_le_10:(quantile(sortedW,.99)??Infinity)<=10,
 stabilized_max_le_20:(sortedW.at(-1)??Infinity)<=20,
};
const gate={schema_version:'CR0105R17-FULL-ROUTE-ADMISSION-GATE-1',status:Object.values(gateChecks).every(Boolean)?'PASS':'HOLD',declared_before_route_outcome_materialization:true,
 target_definition:manifest.target_definition,sample_n:manifest.sample_n,route_source_n:sourceN,route_source_rate:routeSourceRate,parse_n:parseN,parse_rate:parseRate,state_certified_n:certN,state_certification_rate:certRate,
 target_population_n:targetTotal,target_population_covered_n:coveredPop,target_population_coverage:coverage,weight_ess:ess,weight_ess_fraction:ess/Math.max(1,certN),stabilized_weight:{p50:quantile(sortedW,.5),p90:quantile(sortedW,.9),p95:quantile(sortedW,.95),p99:quantile(sortedW,.99),max:sortedW.at(-1)??null},checks:gateChecks,
 cell_certification:[...targetCell.entries()].map(([k,c])=>({cell:k,population_n:c.population_n,linked_n:c.linked_n,sample_n:c.sample_n||0,certified_n:cellCert.get(k)||0})),
 admission_records:admission.map(({_parsed,_setupT,_endT,_record,...rest})=>rest),human_observations:0,
 interpretation:'This gate depends only on route-source availability, parse/state certification, target-cell coverage and weights. Redundancy outcomes are not materialized unless it passes.'};
fs.writeFileSync(`${OUT}/ROUTE_ADMISSION_GATE.json`,JSON.stringify(gate,null,2)+'\n');
console.log(JSON.stringify({...gate,admission_records:undefined,cell_certification:gate.cell_certification},null,2));
if(gate.status!=='PASS')process.exit(20);

// -------- Stage 2: state-verified, phase-contained counterfactual redundancy. --------
const certified=admission.filter(x=>x.admission==='STATE_CERTIFIED');
for(const o of certified){
 const {tokens,lines}=o._parsed;const moves=tokens.map(x=>x.move),r=o._record;const candidates=[];
 // Only within a single annotation line and an unambiguous post-inspection phase.
 for(const line of lines){
   if(['INSPECTION','UNKNOWN','AMBIGUOUS'].includes(line.phase)||line.end-line.start<2)continue;
   const maxEnd=Math.min(line.end,line.start+200);
   for(let i=line.start;i<maxEnd;i++){
     for(let len=2;len<=24&&i+len<=line.end;len++){
       const seg=moves.slice(i,i+len),T=kp.algToTransformation(seg.join(' '));
       if(T.isIdentityTransformation()){
         const saved=seg.filter(m=>!isRotation(m)).length;if(saved>0)candidates.push({kind:'EXACT_LOOP',phase:line.phase,line_id:line.line_id,start:i,end:i+len,actual_length:len,saved_moves:saved,actual:seg.join(' '),replacement:''});
       }
       if(len<=8&&seg.every(isOuterFace)){
         const alt=shortest.get(thash(T));
         if(alt&&alt.length<len){
           const cf=[...moves.slice(0,i),...alt,...moves.slice(i+len)];const cfEnd=o._setupT.applyAlg(cf.join(' '));
           if(!cfEnd.isIdentical(o._endT))throw new Error(`R17_ENDPOINT_MISMATCH_${o.reco_id}_${i}_${len}`);
           candidates.push({kind:'SHORTER_EXACT_REWRITE',phase:line.phase,line_id:line.line_id,start:i,end:i+len,actual_length:len,replacement_length:alt.length,saved_moves:len-alt.length,actual:seg.join(' '),replacement:alt.join(' ')});
         }
       }
     }
   }
 }
 const chosen=chooseIntervals(candidates);const faceTurns=moves.filter(isOuterFace).length,nonRot=moves.filter(m=>!isRotation(m)).length;const phases=[...new Set(chosen.selected.map(c=>c.phase))];const kinds=[...new Set(chosen.selected.map(c=>c.kind))];
 o.outcome={candidate_intervals:chosen.candidate_count,selected_nonoverlap_intervals:chosen.selected,total_saved_moves:chosen.total_saved,
  any_redundancy:chosen.total_saved>0,any_exact_loop:kinds.includes('EXACT_LOOP'),any_shorter_rewrite:kinds.includes('SHORTER_EXACT_REWRITE'),selected_phases:phases,
  outer_face_move_tokens:faceTurns,nonrotation_move_tokens:nonRot,face_turn_token_redundancy_fraction:faceTurns?chosen.total_saved/faceTurns:null,
  phenotype:chosen.total_saved===0?'NO_STATE_VERIFIED_REDUNDANCY':(kinds.length>1?'COMPOUND_STATE_VERIFIED_REDUNDANCY':(kinds[0]==='EXACT_LOOP'?'STATE_VERIFIED_EXACT_LOOP':'STATE_VERIFIED_LOCAL_SHORTENING'))};
}

// Target-standardized estimates: each speed×era cell gets frozen WCA population mass.
const recs=certified.map(o=>({o,cell:o.cell,N:targetCell.get(o.cell).population_n,n:cellCert.get(o.cell)}));
function estimate(getter){let num=0,den=0;for(const z of recs){const w=z.N/z.n,v=getter(z.o);if(v===null||v===undefined||Number.isNaN(v))continue;num+=w*Number(v);den+=w;}return den?num/den:null;}
function rawMean(getter){const vs=certified.map(getter).filter(v=>v!==null&&v!==undefined&&!Number.isNaN(v)).map(Number);return vs.length?vs.reduce((a,b)=>a+b,0)/vs.length:null;}
const phases=['CROSS','F2L','LL_ORIENT','LL_ONELOOK','LL_PERMUTE','ROUX_FB','ROUX_SB','ROUX_CMLL','ROUX_LSE'];
const metrics={
 any_state_verified_redundancy:{raw:rawMean(o=>o.outcome.any_redundancy?1:0),standardized:estimate(o=>o.outcome.any_redundancy?1:0)},
 any_exact_loop:{raw:rawMean(o=>o.outcome.any_exact_loop?1:0),standardized:estimate(o=>o.outcome.any_exact_loop?1:0)},
 any_shorter_exact_rewrite:{raw:rawMean(o=>o.outcome.any_shorter_rewrite?1:0),standardized:estimate(o=>o.outcome.any_shorter_rewrite?1:0)},
 max_nonoverlap_saved_moves:{raw:rawMean(o=>o.outcome.total_saved_moves),standardized:estimate(o=>o.outcome.total_saved_moves)},
 face_turn_token_redundancy_fraction:{raw:rawMean(o=>o.outcome.face_turn_token_redundancy_fraction),standardized:estimate(o=>o.outcome.face_turn_token_redundancy_fraction)},
};
for(const p of phases)metrics[`phase_${p}_any_selected_redundancy`]={raw:rawMean(o=>o.outcome.selected_phases.includes(p)?1:0),standardized:estimate(o=>o.outcome.selected_phases.includes(p)?1:0)};

// Deterministic stratified bootstrap of descriptive sampling uncertainty.
let seed=0x17c0ffee;function rnd(){seed=(1664525*seed+1013904223)>>>0;return seed/4294967296;}
const byCell=new Map();for(const o of certified){if(!byCell.has(o.cell))byCell.set(o.cell,[]);byCell.get(o.cell).push(o);}
function bootMetric(getter,B=1200){const vals=[];for(let b=0;b<B;b++){let num=0,den=0;for(const [cell,arr] of byCell){const N=targetCell.get(cell).population_n;let s=0,c=0;for(let i=0;i<arr.length;i++){const o=arr[Math.floor(rnd()*arr.length)],v=getter(o);if(v!==null&&v!==undefined&&!Number.isNaN(v)){s+=Number(v);c++;}}if(c){num+=N*(s/c);den+=N;}}vals.push(den?num/den:NaN);}const a=vals.filter(Number.isFinite).sort((x,y)=>x-y);return {lo:quantile(a,.025),hi:quantile(a,.975),replicates:a.length};}
for(const [name,m] of Object.entries(metrics)){
 const getter=name==='any_state_verified_redundancy'?(o=>o.outcome.any_redundancy?1:0):name==='any_exact_loop'?(o=>o.outcome.any_exact_loop?1:0):name==='any_shorter_exact_rewrite'?(o=>o.outcome.any_shorter_rewrite?1:0):name==='max_nonoverlap_saved_moves'?(o=>o.outcome.total_saved_moves):name==='face_turn_token_redundancy_fraction'?(o=>o.outcome.face_turn_token_redundancy_fraction):((p)=>o=>o.outcome.selected_phases.includes(p)?1:0)(name.replace('phase_','').replace('_any_selected_redundancy',''));
 m.bootstrap_95=bootMetric(getter);
}

const methodSummary={};for(const method of [...new Set(certified.map(o=>o.method))]){const arr=certified.filter(o=>o.method===method);methodSummary[method]={n:arr.length,raw_any_redundancy:arr.filter(o=>o.outcome.any_redundancy).length/arr.length,raw_mean_saved_moves:arr.reduce((s,o)=>s+o.outcome.total_saved_moves,0)/arr.length,claim_scope:'RECONSTRUCTION_FRAME_DESCRIPTIVE_ONLY; WCA has no solving-method field for population calibration.'};}
const phaseChosen=new Map();for(const o of certified)for(const c of o.outcome.selected_nonoverlap_intervals)phaseChosen.set(c.phase,(phaseChosen.get(c.phase)||0)+1);
const result={schema_version:'CR0105R17-FULL-ROUTE-COURT-1',status:'PASS',stage:'CUBE-REV 0.10.5-R1.7 — Counterfactual Route Alignment, Phase-aware Redundancy Phenotyping & Selection-corrected Reconstruction Analysis',
 parent_wca_export_sha256:'35ce0975798b3c4f648c2421f35b94784ed0811fec8df12f70e8ae574f2d20ad',parent_db_sha256:manifest.parent_db_sha256,
 target_definition:manifest.target_definition,sample_design:manifest.sample_design,admission_gate_summary:{state_certified_n:certN,state_certification_rate:certRate,target_population_coverage:coverage,weight_ess:ess,stabilized_weight:gate.stabilized_weight},
 phenotype_definition:{unit:'distinct WCA-linked official attempt with one SHA-canonical reconstruction',route_source:'raw alg.cubing.net setup + reconstruction alg',state_certification:'cubing.js KPattern experimentalIsSolved, ignoring puzzle and center orientation',phase_rule:'candidate interval must be wholly inside one non-inspection, non-unknown, non-ambiguous annotation line',counterfactual_rule:'exact fixed-frame KTransformation identity loop or <=8 ordinary-face-turn window exactly replaceable by <=3 ordinary face turns; replacement rechecked against full route endpoint',overlap_rule:'weighted interval scheduling maximizes saved non-overlapping move tokens; overlapping candidate windows are never summed'},
 metrics,phenotype_counts:Object.fromEntries([...new Set(certified.map(o=>o.outcome.phenotype))].map(p=>[p,certified.filter(o=>o.outcome.phenotype===p).length])),selected_interval_phase_counts:Object.fromEntries(phaseChosen),method_reconstruction_frame:methodSummary,
 certification_attrition:gate.admission_records.reduce((a,r)=>(a[r.admission]=(a[r.admission]||0)+1,a),{}),
 claim_scope:{allowed:['speed x era standardized descriptive route-redundancy phenotype for the supported <10s linked-reconstruction target','raw reconstruction-frame method summaries','phase attribution only for annotation-certified lines'],prohibited:['full-WCA prevalence','causal cognitive error or recovery mechanism','claiming speed x era standardization removes unobserved reconstruction selection','claiming WCA export identifies competitor attempt scramble','population calibration by solving method']},
 human_observations:0,human_recruitment:'DEFERRED_BY_RESEARCH_DESIGN',
 records:certified.map(({_parsed,_setupT,_endT,_record,...rest})=>rest)};
fs.writeFileSync(`${OUT}/FULL_ROUTE_COURT.json`,JSON.stringify(result,null,2)+'\n');
const compact={...result,records:undefined,metrics:result.metrics};console.log(JSON.stringify(compact,null,2));
