import fs from 'node:fs';
import { buildR19Core, parseAnnotated, sha } from './r19_quotient_core.mjs';

const OUT=process.env.R19_GEOM_ROOT||'/tmp/r19geom';fs.mkdirSync(OUT,{recursive:true});
const core=await buildR19Core();
const {kp,defaultPattern,EDGE,CORNER,CENTER,ORIENT,faces,faceSupport,canonicalizeByCenters,detectCrossFace,detectRouxLastFace,buildPhaseSpec,maskDistance}=core;
function samePattern(a,b){return sha(a.patternData)===sha(b.patternData);}
const checks={};
checks.orientation_group_24=ORIENT.length===24;
checks.face_edge_support_4=faces.every(f=>faceSupport[f].edges.length===4);
checks.face_corner_support_4=faces.every(f=>faceSupport[f].corners.length===4);
checks.opposite_edge_support_disjoint=['UD','RL','FB'].every(x=>faceSupport[x[0]].edges.every(i=>!faceSupport[x[1]].edges.includes(i)));
checks.opposite_corner_support_disjoint=['UD','RL','FB'].every(x=>faceSupport[x[0]].corners.every(i=>!faceSupport[x[1]].corners.includes(i)));
const syn=defaultPattern.applyAlg("R U F2 L' D B U2");
const can=canonicalizeByCenters(syn),canRot=canonicalizeByCenters(syn.applyAlg('x y2 z'));
checks.center_canonical_unique_unrotated=can.ok&&can.count===1;
checks.center_canonical_unique_rotated=canRot.ok&&canRot.count===1;
checks.center_canonical_rotation_invariant=can.ok&&canRot.ok&&samePattern(can.pattern,canRot.pattern);
const crossTarget=defaultPattern.applyAlg('U');
const crossFrame=detectCrossFace(crossTarget);
checks.synthetic_cross_face_detected=crossFrame.ok;
checks.synthetic_cross_face_unique=crossFrame.ok&&crossFrame.tie_n===1;
checks.synthetic_cross_face_D=crossFrame.ok&&crossFrame.crossFace==='D';
const routeFrame={crossFace:'D',lastFace:'U'};
const crossSpec=buildPhaseSpec({method:'CFOP',phase:'CROSS',startRaw:defaultPattern.applyAlg("R U R'"),targetRaw:crossTarget,routeFrame,comment:'cross'});
checks.cross_spec_admitted=crossSpec.ok;
if(crossSpec.ok){
  const s=crossSpec.specs[0];
  const d0=maskDistance(crossTarget,crossTarget,s.masks,s.target_variants),dIgnored=maskDistance(crossTarget.applyMove('U'),crossTarget,s.masks,s.target_variants);
  checks.cross_endpoint_zero=d0.ok&&Math.abs(d0.distance)<1e-12;
  checks.cross_ignores_U_layer_permutation=dIgnored.ok&&Math.abs(dIgnored.distance)<1e-12;
}
const f2lTarget=defaultPattern.applyAlg('U'),f2lStart=f2lTarget.applyAlg("R U R'");
const f2lSpec=buildPhaseSpec({method:'CFOP',phase:'F2L',startRaw:f2lStart,targetRaw:f2lTarget,routeFrame,comment:'1st pair'});
checks.f2l_spec_admitted=f2lSpec.ok;
if(f2lSpec.ok){
  const s=f2lSpec.specs[0];
  const d0=maskDistance(f2lTarget,f2lTarget,s.masks,s.target_variants),dIgnored=maskDistance(f2lTarget.applyMove('U2'),f2lTarget,s.masks,s.target_variants);
  checks.f2l_endpoint_zero=d0.ok&&Math.abs(d0.distance)<1e-12;
  checks.f2l_quotients_last_layer_U_turn=dIgnored.ok&&Math.abs(dIgnored.distance)<1e-12;
}
const pllTarget=defaultPattern,pllStart=defaultPattern.applyAlg('U');
const pllSpec=buildPhaseSpec({method:'CFOP',phase:'LL_PERMUTE',startRaw:pllStart,targetRaw:pllTarget,routeFrame,comment:'PLL'});
checks.pll_spec_admitted=pllSpec.ok;
if(pllSpec.ok){
  const obj=pllSpec.specs.find(x=>x.channel_name==='objective');
  checks.pll_auf_equiv_U_zero=Math.abs(maskDistance(defaultPattern.applyMove('U'),pllTarget,obj.masks,obj.target_variants).distance)<1e-12;
  checks.pll_auf_equiv_U2_zero=Math.abs(maskDistance(defaultPattern.applyAlg('U2'),pllTarget,obj.masks,obj.target_variants).distance)<1e-12;
  checks.pll_auf_equiv_Uprime_zero=Math.abs(maskDistance(defaultPattern.applyAlg("U'"),pllTarget,obj.masks,obj.target_variants).distance)<1e-12;
}
const ollSpec=buildPhaseSpec({method:'CFOP',phase:'LL_ORIENT',startRaw:defaultPattern.applyAlg('R U'),targetRaw:defaultPattern,routeFrame,comment:'OLL'});
checks.oll_spec_admitted=ollSpec.ok;
if(ollSpec.ok){
  const obj=ollSpec.specs.find(x=>x.channel_name==='objective');
  checks.oll_piece_permutation_quotiented=maskDistance(defaultPattern.applyMove('U'),defaultPattern,obj.masks,obj.target_variants).distance===0;
}

function loadRecords(){
  const r17=JSON.parse(fs.readFileSync('research/0.10.5-r1.7/evidence-full-route/FULL_ROUTE_SAMPLE_MANIFEST.json','utf8')).records.map(r=>({...r,source:'R17'}));
  const r18=JSON.parse(fs.readFileSync('research/0.10.5-r1.8/evidence-holdout-a/HOLDOUT_A_ROUTE_MANIFEST.json','utf8')).records.map(r=>({...r,source:'R18'}));
  return [...r17,...r18];
}
const records=loadRecords(),hist={total:records.length,route_source:0,parse_ok:0,state_certified:0,cfop_zb:0,cfop_zb_cross_line:0,cfop_zb_frame_ok:0,cfop_zb_frame_tie:0,roux:0,roux_cmll_line:0,roux_last_face_ok:0,errors:0};
const crossFaces={},crossFail={},rouxFail={};
for(const r of records){
  if(r.route_source_status!=='RAW_ALG_CUBING_LINK'){continue;}hist.route_source++;
  try{
    const parsed=parseAnnotated(r.raw_alg,r.method),moves=parsed.tokens.map(x=>x.move),rawT=kp.algToTransformation(r.raw_alg),expandedT=kp.algToTransformation(moves.join(' '));if(!rawT.isIdentical(expandedT))throw new Error('EXPANSION_MISMATCH');hist.parse_ok++;
    let p=defaultPattern.applyAlg(r.raw_setup),states=[p];for(const m of moves){p=p.applyMove(m);states.push(p);}if(!p.experimentalIsSolved({ignorePuzzleOrientation:true,ignoreCenterOrientation:true}))continue;hist.state_certified++;
    if(r.method==='CFOP'||r.method==='ZB'){
      hist.cfop_zb++;const line=parsed.lines.find(x=>x.phase==='CROSS'&&x.end>x.start);if(!line){crossFail.NO_CROSS_LINE=(crossFail.NO_CROSS_LINE||0)+1;continue;}hist.cfop_zb_cross_line++;
      const f=detectCrossFace(states[line.end]);if(f.ok){hist.cfop_zb_frame_ok++;crossFaces[f.crossFace]=(crossFaces[f.crossFace]||0)+1;if(f.tie_n>1)hist.cfop_zb_frame_tie++;}else crossFail[f.reason]=(crossFail[f.reason]||0)+1;
    } else if(r.method==='Roux'){
      hist.roux++;const line=parsed.lines.find(x=>x.phase==='ROUX_CMLL'&&x.end>x.start);if(!line){rouxFail.NO_CMLL_LINE=(rouxFail.NO_CMLL_LINE||0)+1;continue;}hist.roux_cmll_line++;const f=detectRouxLastFace(states[line.start],states[line.end]);if(f.ok)hist.roux_last_face_ok++;else rouxFail[f.reason]=(rouxFail[f.reason]||0)+1;
    }
  }catch(e){hist.errors++;}
}
checks.historical_manifest_total_1800=hist.total===1800;
checks.historical_route_source_ge_1750=hist.route_source>=1750;
checks.historical_state_certified_ge_1700=hist.state_certified>=1700;
checks.cfop_zb_cross_frame_rate_ge_0_95=hist.cfop_zb_cross_line>0&&hist.cfop_zb_frame_ok/hist.cfop_zb_cross_line>=.95;
const result={schema_version:'CR0105R19-QUOTIENT-GEOMETRY-PROBE-1',status:Object.values(checks).every(Boolean)?'PASS':'HOLD',cubing_version:'0.63.3',cubing_source_commit:'c223a53ba37e0941fe8242571aef1cccb978bb24',orbits:{EDGE,CORNER,CENTER},face_support:faceSupport,checks,historical_frame_probe:hist,cross_face_counts:crossFaces,cross_failures:crossFail,roux_failures:rouxFail,human_observations:0};
fs.writeFileSync(`${OUT}/QUOTIENT_GEOMETRY_PROBE.json`,JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));
if(result.status!=='PASS')process.exit(20);
