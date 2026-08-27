import { buildR19Core } from '../0.10.5-r1.9/r19_quotient_core.mjs';

export async function buildRouxFrameCore(){
  const core=await buildR19Core();
  const {EDGE,CORNER,faces,opposite,faceSupport,canonicalizeByCenters,coordSolved}=core;
  const intersect=(a,b)=>{const s=new Set(b);return a.filter(x=>s.has(x));};
  function blockMask(bottom,side){
    const top=opposite[bottom];
    if(side===bottom||side===top)return null;
    return {
      bottom,side,top,
      edges:faceSupport[side].edges.filter(i=>!faceSupport[top].edges.includes(i)),
      corners:intersect(faceSupport[bottom].corners,faceSupport[side].corners),
    };
  }
  function solvedBlock(raw,mask){
    const c=canonicalizeByCenters(raw);if(!c.ok)return false;
    return mask.edges.every(i=>coordSolved(c.pattern,EDGE,i,'full'))&&mask.corners.every(i=>coordSolved(c.pattern,CORNER,i,'full'));
  }
  function bothBlocks(raw,frame){return solvedBlock(raw,frame.first)&&solvedBlock(raw,frame.second);}
  function cornersSolvedAUF(raw,top){
    let p=raw;
    for(let k=0;k<4;k++){
      const c=canonicalizeByCenters(p);
      if(c.ok){const n=c.pattern.patternData[CORNER].pieces.length;if([...Array(n).keys()].every(i=>coordSolved(c.pattern,CORNER,i,'full')))return true;}
      p=p.applyMove(top);
    }
    return false;
  }
  const frames=[];
  for(const bottom of faces)for(const side of faces){
    if(side===bottom||side===opposite[bottom])continue;
    frames.push({bottom,first_side:side,second_side:opposite[side],first:blockMask(bottom,side),second:blockMask(bottom,opposite[side]),axis_key:`${bottom}|${[side,opposite[side]].sort().join('-')}`});
  }
  return {...core,frames,blockMask,solvedBlock,bothBlocks,cornersSolvedAUF};
}
