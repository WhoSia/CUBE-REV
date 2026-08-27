import crypto from 'node:crypto';
import { Alg } from 'cubing/alg';
import { cube3x3x3 } from 'cubing/puzzles';
import { experimentalSolve3x3x3IgnoringCenters } from 'cubing/search';

export const CUBING_VERSION='0.63.3';
export const CUBING_SOURCE_COMMIT='c223a53ba37e0941fe8242571aef1cccb978bb24';

function stable(x){
  if(Array.isArray(x)) return '['+x.map(stable).join(',')+']';
  if(x&&typeof x==='object') return '{'+Object.keys(x).sort().map(k=>JSON.stringify(k)+':'+stable(x[k])).join(',')+'}';
  return JSON.stringify(x);
}
export function sha(x){return crypto.createHash('sha256').update(typeof x==='string'?x:stable(x)).digest('hex');}
export function upperQuantile(xs,q){if(!xs.length)return null;const a=[...xs].sort((x,y)=>x-y);return a[Math.min(a.length-1,Math.max(0,Math.ceil(q*a.length)-1))];}
export function mean(xs){return xs.length?xs.reduce((a,b)=>a+b,0)/xs.length:null;}

const phasePatterns={
  INSPECTION:[/\binspection\b/i],
  CROSS:[/\b(?:cross|xcross|xxcross|xxxcross)\b/i,/\bpseudo\s+cross\b/i,/\bmissed\s+cross\b/i],
  F2L:[/\bf2l\b/i,/\b(?:1st|2nd|3rd|4th|first|second|third|fourth)\s*(?:\/\s*)?pair/i,/\bpairs?\b/i,/\bzbls\b/i,/\bsvls\b/i,/\bwvls\b/i,/\beols\b/i],
  LL_ORIENT:[/\boll(?:\b|cp)/i,/\beoll\b/i,/\bcoll\b/i,/\bollcp\b/i],
  LL_PERMUTE:[/\bpll\b/i,/\bepll\b/i,/\bauf\b/i],
  LL_ONELOOK:[/\bzbll\b/i,/\b2gll\b/i,/\bell\b/i,/\bcll\b/i],
  ROUX_FB:[/\bfb\b/i,/\bfbdr\b/i,/\bpseudo\s+fb\b/i],
  ROUX_SB:[/\bsb\b/i,/\bss\b/i,/\bsp\b/i,/\bflipped\s+sp\b/i],
  ROUX_CMLL:[/\bcmll\b/i],
  ROUX_LSE:[/\blse\b/i,/\beolr\b/i,/\beolrb\b/i,/\bep\b/i],
};
export function classifyPhase(method,comment){
  const c=String(comment||'').trim().toLowerCase(); if(!c)return {phase:'UNKNOWN',hits:[]};
  let hits=[]; for(const [phase,ps] of Object.entries(phasePatterns)) if(ps.some(p=>p.test(c))) hits.push(phase);
  if(method!=='Roux') hits=hits.filter(x=>!x.startsWith('ROUX_'));
  if(method==='Roux'&&hits.includes('LL_ONELOOK')&&/\bcll\b/i.test(c)&&!hits.includes('ROUX_CMLL')){hits=hits.filter(x=>x!=='LL_ONELOOK');hits.push('ROUX_CMLL');}
  hits=[...new Set(hits)]; return {phase:hits.length===1?hits[0]:(hits.length?'AMBIGUOUS':'UNKNOWN'),hits};
}
export function parseAnnotated(raw,method){
  const tokens=[],lines=[];let lineId=0;
  for(const rawLine of String(raw||'').split(/\r?\n/)){
    const idx=rawLine.indexOf('//'); const left=(idx>=0?rawLine.slice(0,idx):rawLine).trim(); const comment=(idx>=0?rawLine.slice(idx+2):'').trim();
    if(!left&&!comment)continue;
    const cls=classifyPhase(method,comment); let moves=[];
    if(left) moves=Array.from(Alg.fromString(left).expand().experimentalLeafMoves()).map(m=>m.toString());
    const start=tokens.length; for(const move of moves)tokens.push({move,phase:cls.phase,line_id:lineId,comment});
    lines.push({line_id:lineId,start,end:tokens.length,comment,phase:cls.phase,hits:cls.hits,moves}); lineId++;
  }
  return {tokens,lines};
}

export async function buildR19Core(){
  const kp=await cube3x3x3.kpuzzle(); const defaultPattern=kp.defaultPattern();
  const orbitNames=Object.keys(defaultPattern.patternData);
  const EDGE=orbitNames.find(k=>/edge/i.test(k)); const CORNER=orbitNames.find(k=>/corner/i.test(k)); const CENTER=orbitNames.find(k=>/center/i.test(k));
  if(!EDGE||!CORNER||!CENTER) throw new Error(`R19_ORBIT_DISCOVERY_FAIL ${orbitNames.join(',')}`);
  function thash(t){return sha(t.transformationData);}
  function orientationGroup(){
    const gens=['x','y','z'].map(m=>kp.moveToTransformation(m)); const id=kp.identityTransformation();
    const seen=new Map([[thash(id),id]]),q=[id];
    while(q.length){const a=q.shift();for(const g of gens){const b=a.applyTransformation(g),h=thash(b);if(!seen.has(h)){seen.set(h,b);q.push(b);}}}
    return [...seen.values()];
  }
  const ORIENT=orientationGroup();
  const faces=['U','D','R','L','F','B']; const opposite={U:'D',D:'U',R:'L',L:'R',F:'B',B:'F'};
  function movedPositions(face,orbit){
    const d=kp.moveToTransformation(face).transformationData[orbit]; const out=[];
    for(let i=0;i<d.permutation.length;i++) if(d.permutation[i]!==i) out.push(i);
    return out;
  }
  const faceSupport={}; for(const f of faces) faceSupport[f]={edges:movedPositions(f,EDGE),corners:movedPositions(f,CORNER)};
  const defaultCenters=defaultPattern.patternData[CENTER].pieces;
  function sameArray(a,b){return a.length===b.length&&a.every((x,i)=>x===b[i]);}
  function canonicalizeByCenters(p){
    const candidates=[];
    for(let i=0;i<ORIENT.length;i++){
      const q=p.applyTransformation(ORIENT[i]);
      if(sameArray(q.patternData[CENTER].pieces,defaultCenters)) candidates.push({index:i,pattern:q,orientation:ORIENT[i]});
    }
    if(candidates.length!==1) return {ok:false,count:candidates.length,candidates};
    return {ok:true,count:1,...candidates[0]};
  }
  function coordSolved(p,orbit,i,channel='full'){
    const a=p.patternData[orbit],b=defaultPattern.patternData[orbit];
    if(channel==='piece') return a.pieces[i]===b.pieces[i];
    if(channel==='orientation') return a.orientation[i]===b.orientation[i];
    return a.pieces[i]===b.pieces[i]&&a.orientation[i]===b.orientation[i];
  }
  function solvedPositions(p,orbit,positions=null,channel='full'){
    const ps=positions??p.patternData[orbit].pieces.map((_,i)=>i); return ps.filter(i=>coordSolved(p,orbit,i,channel));
  }
  function f2lDomain(crossFace){
    const last=opposite[crossFace]; const le=new Set(faceSupport[last].edges),lc=new Set(faceSupport[last].corners);
    return {
      edges:defaultPattern.patternData[EDGE].pieces.map((_,i)=>i).filter(i=>!le.has(i)),
      corners:defaultPattern.patternData[CORNER].pieces.map((_,i)=>i).filter(i=>!lc.has(i)),
      lastFace:last,
    };
  }
  function fullSolvedCountInDomain(p,domain){return solvedPositions(p,EDGE,domain.edges).length+solvedPositions(p,CORNER,domain.corners).length;}
  function detectCrossFace(targetRaw){
    const cc=canonicalizeByCenters(targetRaw); if(!cc.ok)return {ok:false,reason:'CENTER_CANONICALIZATION',center_candidates:cc.count}; const target=cc.pattern;
    const candidates=[];
    for(const f of faces){
      const es=faceSupport[f].edges; if(es.length!==4)continue;
      if(es.every(i=>coordSolved(target,EDGE,i,'full'))){const domain=f2lDomain(f);candidates.push({face:f,f2l_solved:fullSolvedCountInDomain(target,domain)});}
    }
    if(!candidates.length)return {ok:false,reason:'NO_EXACT_SOLVED_FACE_STAR'};
    candidates.sort((a,b)=>b.f2l_solved-a.f2l_solved||faces.indexOf(a.face)-faces.indexOf(b.face));
    return {ok:true,crossFace:candidates[0].face,lastFace:opposite[candidates[0].face],tie_n:candidates.filter(x=>x.f2l_solved===candidates[0].f2l_solved).length,candidates,canonical_target:target};
  }
  function detectRouxLastFace(startRaw,targetRaw){
    const cs=canonicalizeByCenters(startRaw),ct=canonicalizeByCenters(targetRaw); if(!cs.ok||!ct.ok)return {ok:false,reason:'CENTER_CANONICALIZATION'};
    const candidates=[];
    for(const f of faces){const ps=faceSupport[f].corners;if(ps.length!==4)continue;const targetSolved=ps.filter(i=>coordSolved(ct.pattern,CORNER,i,'full')).length;const newly=ps.filter(i=>!coordSolved(cs.pattern,CORNER,i,'full')&&coordSolved(ct.pattern,CORNER,i,'full')).length;if(targetSolved===4)candidates.push({face:f,newly});}
    if(!candidates.length)return {ok:false,reason:'NO_FOUR_SOLVED_CORNER_FACE'};
    candidates.sort((a,b)=>b.newly-a.newly||faces.indexOf(a.face)-faces.indexOf(b.face));
    return {ok:true,lastFace:candidates[0].face,tie_n:candidates.filter(x=>x.newly===candidates[0].newly).length,candidates};
  }
  function maskDistance(pRaw,targetRaw,masks,targetVariantsRaw=null){
    const cp=canonicalizeByCenters(pRaw); if(!cp.ok)return {ok:false,reason:'CENTER_CANONICALIZATION_STATE'};
    const targets=(targetVariantsRaw??[targetRaw]).map(t=>canonicalizeByCenters(t)).filter(x=>x.ok).map(x=>x.pattern); if(!targets.length)return {ok:false,reason:'CENTER_CANONICALIZATION_TARGET'};
    function one(target){
      let bad=0,total=0;
      for(const m of masks){
        const a=cp.pattern.patternData[m.orbit],b=target.patternData[m.orbit];
        for(const i of m.positions){
          if(m.channel==='piece'||m.channel==='full'){total++;if(a.pieces[i]!==b.pieces[i])bad++;}
          if(m.channel==='orientation'||m.channel==='full'){total++;if(a.orientation[i]!==b.orientation[i])bad++;}
        }
      }
      return total?{distance:bad/total,bad,total}:null;
    }
    const vals=targets.map(one).filter(Boolean); if(!vals.length)return {ok:false,reason:'EMPTY_MASK'}; vals.sort((a,b)=>a.distance-b.distance||a.bad-b.bad); return {ok:true,...vals[0]};
  }
  function lastFaceVariants(target,lastFace){
    if(!lastFace)return [target]; const out=[target]; let p=target; for(let k=1;k<4;k++){p=p.applyMove(lastFace);out.push(p);} return out;
  }
  function exactSolvedPositions(target,domain){return {edges:solvedPositions(target,EDGE,domain.edges,'full'),corners:solvedPositions(target,CORNER,domain.corners,'full')};}
  function buildPhaseSpec({method,phase,startRaw,targetRaw,routeFrame,comment=''}){
    const cs=canonicalizeByCenters(startRaw),ct=canonicalizeByCenters(targetRaw); if(!cs.ok||!ct.ok)return {ok:false,reason:'CENTER_CANONICALIZATION'}; const start=cs.pattern,target=ct.pattern;
    const specs=[];
    if(phase==='CROSS'){
      if(!routeFrame?.crossFace)return {ok:false,reason:'NO_CROSS_FRAME'}; const pos=faceSupport[routeFrame.crossFace].edges;
      if(!pos.every(i=>coordSolved(target,EDGE,i,'full')))return {ok:false,reason:'CROSS_ENDPOINT_NOT_EXACT'};
      specs.push({channel_name:'objective',kind:'objective_backtrack',masks:[{orbit:EDGE,positions:pos,channel:'full'}],target_variants:[targetRaw]});
    } else if(phase==='F2L'){
      if(!routeFrame?.crossFace)return {ok:false,reason:'NO_CROSS_FRAME'}; const d=f2lDomain(routeFrame.crossFace),sol=exactSolvedPositions(target,d);
      const newE=sol.edges.filter(i=>!coordSolved(start,EDGE,i,'full')),newC=sol.corners.filter(i=>!coordSolved(start,CORNER,i,'full'));
      if(newE.length<1||newC.length<1)return {ok:false,reason:'F2L_NO_EDGE_CORNER_ACQUISITION',new_edges:newE.length,new_corners:newC.length};
      const cross=faceSupport[routeFrame.crossFace].edges;if(!cross.every(i=>coordSolved(target,EDGE,i,'full')))return {ok:false,reason:'F2L_CROSS_NOT_PRESERVED'};
      specs.push({channel_name:'objective',kind:'objective_backtrack',masks:[{orbit:EDGE,positions:sol.edges,channel:'full'},{orbit:CORNER,positions:sol.corners,channel:'full'}],target_variants:[targetRaw]});
    } else if(['LL_ORIENT','LL_PERMUTE','LL_ONELOOK'].includes(phase)){
      if(!routeFrame?.lastFace||!routeFrame?.crossFace)return {ok:false,reason:'NO_LL_FRAME'}; const ll=faceSupport[routeFrame.lastFace],d=f2lDomain(routeFrame.crossFace),anchors=exactSolvedPositions(target,d);
      const mode=phase==='LL_ORIENT'?'orientation':phase==='LL_PERMUTE'?'piece':'full'; const tv=phase==='LL_ORIENT'?[targetRaw]:lastFaceVariants(targetRaw,routeFrame.lastFace);
      specs.push({channel_name:'objective',kind:'objective_backtrack',masks:[{orbit:EDGE,positions:ll.edges,channel:mode},{orbit:CORNER,positions:ll.corners,channel:mode}],target_variants:tv});
      if(anchors.edges.length+anchors.corners.length>0) specs.push({channel_name:'anchor',kind:'anchor_break_peak',masks:[{orbit:EDGE,positions:anchors.edges,channel:'full'},{orbit:CORNER,positions:anchors.corners,channel:'full'}],target_variants:[targetRaw]});
    } else if(phase==='ROUX_FB'||phase==='ROUX_SB'){
      const allE=target.patternData[EDGE].pieces.map((_,i)=>i),allC=target.patternData[CORNER].pieces.map((_,i)=>i); const se=solvedPositions(target,EDGE,allE,'full'),sc=solvedPositions(target,CORNER,allC,'full'); const newly=se.filter(i=>!coordSolved(start,EDGE,i,'full')).length+sc.filter(i=>!coordSolved(start,CORNER,i,'full')).length; const minNew=phase==='ROUX_FB'?3:2;
      if(newly<minNew)return {ok:false,reason:'ROUX_SOLVED_SUPPORT_GROWTH_LOW',newly,minNew}; specs.push({channel_name:'objective',kind:'objective_backtrack',masks:[{orbit:EDGE,positions:se,channel:'full'},{orbit:CORNER,positions:sc,channel:'full'}],target_variants:[targetRaw]});
    } else if(phase==='ROUX_CMLL'){
      const allC=target.patternData[CORNER].pieces.map((_,i)=>i),last=routeFrame?.rouxLastFace; specs.push({channel_name:'objective',kind:'objective_backtrack',masks:[{orbit:CORNER,positions:allC,channel:'full'}],target_variants:last?lastFaceVariants(targetRaw,last):[targetRaw]});
      const se=solvedPositions(target,EDGE,null,'full');if(se.length)specs.push({channel_name:'anchor',kind:'anchor_break_peak',masks:[{orbit:EDGE,positions:se,channel:'full'}],target_variants:[targetRaw]});
    } else if(phase==='ROUX_LSE'){
      const allE=target.patternData[EDGE].pieces.map((_,i)=>i),last=routeFrame?.rouxLastFace; specs.push({channel_name:'objective',kind:'objective_backtrack',masks:[{orbit:EDGE,positions:allE,channel:'full'}],target_variants:last?lastFaceVariants(targetRaw,last):[targetRaw]});
      const sc=solvedPositions(target,CORNER,null,'full');if(sc.length)specs.push({channel_name:'anchor',kind:'anchor_break_peak',masks:[{orbit:CORNER,positions:sc,channel:'full'}],target_variants:[targetRaw]});
    } else return {ok:false,reason:'PHASE_UNSUPPORTED'};
    for(const s of specs){const end=maskDistance(targetRaw,targetRaw,s.masks,s.target_variants);if(!end.ok||end.distance>1e-12)return {ok:false,reason:'ENDPOINT_OBJECTIVE_NONZERO',channel:s.channel_name,end};}
    return {ok:true,specs,canonical_start:start,canonical_target:target,comment};
  }
  function objectiveBacktrack(ds){
    if(ds.length<3)return {amplitude:0,candidate:null}; let frontier=ds[0],best=0,candidate=null;
    for(let t=1;t<ds.length;t++){
      const pre=frontier,amp=ds[t]-pre;
      if(amp>best+1e-12){for(let k=t+1;k<=ds.length-2;k++){if(ds[k]<=pre+1e-12){best=amp;candidate={peak_index:t,return_index:k,pre_frontier:pre,peak:ds[t],return:ds[k],amplitude:amp};break;}}}
      if(ds[t]<frontier)frontier=ds[t];
    }
    return {amplitude:best,candidate};
  }
  function featureForMoves(startRaw,targetRaw,moves,spec){
    let p=startRaw; const ds=[]; const d0=maskDistance(p,targetRaw,spec.masks,spec.target_variants);if(!d0.ok)return {ok:false,reason:d0.reason};ds.push(d0.distance);
    for(const m of moves){p=p.applyMove(m);const d=maskDistance(p,targetRaw,spec.masks,spec.target_variants);if(!d.ok)return {ok:false,reason:d.reason};ds.push(d.distance);}
    if(spec.kind==='objective_backtrack'){const x=objectiveBacktrack(ds);return {ok:true,kind:spec.kind,amplitude:x.amplitude,path:ds,candidate:x.candidate,endpoint:ds.at(-1)};}
    if(spec.kind==='anchor_break_peak'){const amp=Math.max(...ds.slice(1,-1),0);return {ok:true,kind:spec.kind,amplitude:amp,path:ds,endpoint:ds.at(-1)};}
    return {ok:false,reason:'UNKNOWN_FEATURE_KIND'};
  }
  const outer=/^([URFDLB])(?:2'?|')?$/,oppPairs=new Set(['UD','DU','RL','LR','FB','BF']);
  function faceFamily(m){const x=String(m).match(outer);return x?x[1]:null;}
  function representationVariants(moves){
    const out=[],seen=new Set([moves.join(' ')]);
    for(let i=0;i<moves.length-1;i++){const a=faceFamily(moves[i]),b=faceFamily(moves[i+1]);if(a&&b&&oppPairs.has(a+b)){const z=[...moves];[z[i],z[i+1]]=[z[i+1],z[i]];const s=z.join(' ');if(!seen.has(s)){seen.add(s);out.push(z);}}}
    const order={U:0,D:1,R:2,L:3,F:4,B:5};let z=[...moves],changed=true,passes=0;
    while(changed&&passes++<moves.length*moves.length){changed=false;for(let i=0;i<z.length-1;i++){const a=faceFamily(z[i]),b=faceFamily(z[i+1]);if(a&&b&&oppPairs.has(a+b)&&order[a]>order[b]){[z[i],z[i+1]]=[z[i+1],z[i]];changed=true;}}}
    const s=z.join(' ');if(!seen.has(s)){seen.add(s);out.push(z);}return out.slice(0,16);
  }
  async function exactNullRealizations(startRaw,targetRaw,moves,spec){
    const originalT=kp.algToTransformation(moves.join(' ')); const rows=[]; const obs=featureForMoves(startRaw,targetRaw,moves,spec);if(obs.ok)rows.push({source:'OBSERVED',moves,feature:obs,exact:true});
    for(const z of representationVariants(moves)){try{const t=kp.algToTransformation(z.join(' '));if(!t.isIdentical(originalT))continue;const f=featureForMoves(startRaw,targetRaw,z,spec);if(f.ok)rows.push({source:'REPRESENTATION',moves:z,feature:f,exact:true});}catch{}}
    let solver={attempted:false,exact:false,physical_only:false,error:null};
    try{
      solver.attempted=true; const rel=defaultPattern.applyTransformation(originalT); const solve=await experimentalSolve3x3x3IgnoringCenters(rel); const alt=Array.from(solve.invert().expand().experimentalLeafMoves()).map(m=>m.toString()); const altT=kp.algToTransformation(alt.join(' ')); solver.exact=altT.isIdentical(originalT);
      const altEnd=startRaw.applyTransformation(altT),canonAlt=canonicalizeByCenters(altEnd),canonTarget=canonicalizeByCenters(targetRaw);solver.physical_only=canonAlt.ok&&canonTarget.ok&&canonAlt.pattern.experimentalIsSolved({ignorePuzzleOrientation:true,ignoreCenterOrientation:true})===canonTarget.pattern.experimentalIsSolved({ignorePuzzleOrientation:true,ignoreCenterOrientation:true});
      if(solver.exact){const f=featureForMoves(startRaw,targetRaw,alt,spec);if(f.ok)rows.push({source:'SOLVER',moves:alt,feature:f,exact:true});}
    }catch(e){solver.error=String(e?.message||e).slice(0,240);}
    return {rows,solver};
  }
  return {kp,defaultPattern,EDGE,CORNER,CENTER,ORIENT,faces,opposite,faceSupport,canonicalizeByCenters,coordSolved,solvedPositions,f2lDomain,detectCrossFace,detectRouxLastFace,maskDistance,lastFaceVariants,buildPhaseSpec,featureForMoves,exactNullRealizations,representationVariants};
}
