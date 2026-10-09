/** CUBE-REV 0.15 P3B: exact five-edge slot/orientation coordinate.
 * Four D-cross edges (4,5,6,7) plus fixed UR (0).
 * The 16-to-1 projection preserves every labelled outer-turn successor.
 * Source contains no archived human solve data.
 */
import {indexOfFourEdges} from '../cuberev-013/cross4-pdb.mjs';
export const FIVE_EDGE_TARGETS=Object.freeze([4,5,6,7,0]);
export const FIVE_EDGE_STATES=3041280;
export function fiveEdgeRank(positions){
 if(!Array.isArray(positions)||positions.length!==5)throw Error('FIVE_POSITIONS_REQUIRED');
 const pool=Array.from({length:12},(_,i)=>i);let rank=0;
 for(let k=0;k<5;k++){
  const i=pool.indexOf(positions[k]);if(i<0)throw Error('DUPLICATE_OR_INVALID_SLOT');
  rank=rank*(12-k)+i;pool.splice(i,1);
 }
 return rank;
}
export function fiveEdgeCoordinate(ep,eo){
 if(!Array.isArray(ep)||!Array.isArray(eo)||ep.length!==12||eo.length!==12)
  throw Error('FULL_EDGE_COORDINATE_REQUIRED');
 const p=FIVE_EDGE_TARGETS.map(id=>ep.indexOf(id));
 if(p.some(i=>i<0)||p.some(i=>eo[i]!==0&&eo[i]!==1))throw Error('MISSING_EDGE_OR_ORIENTATION');
 return fiveEdgeRank(p)*32+p.reduce((bits,slot,i)=>bits+(eo[slot]<<i),0);
}
export function fourEdgeProjection(ep,eo){
 return indexOfFourEdges(ep,eo,[4,5,6,7]);
}
/** Mathematical fiber of the fifth edge over any fixed 4-edge state. */
export function sixteenLiftsOfFour(positions4,bits4){
 if(!Array.isArray(positions4)||positions4.length!==4||new Set(positions4).size!==4||
    positions4.some(x=>!Number.isInteger(x)||x<0||x>=12)||
    !Number.isInteger(bits4)||bits4<0||bits4>15)throw Error('BAD_FOUR_EDGE_FIBER');
 const available=Array.from({length:12},(_,i)=>i).filter(i=>!positions4.includes(i));
 const out=[];
 for(const p of available)for(const bit of [0,1])
  out.push(fiveEdgeRank([...positions4,p])*32+bits4+(bit<<4));
 if(out.length!==16||new Set(out).size!==16)throw Error('FIBER_COUNT_INVARIANT');
 return out;
}
