/** CUBE-REV 0.13 — Pre-action, tie-preserving Cross target inference.
 * Exact PDB distances only. Does not accept stage annotations or future turns.
 * Returns set-valued candidates; single-face tie-break is descriptive only.
 */
import {FACE_EDGE_IDS,indexOfFourEdges} from './cross4-pdb.mjs';
export const CROSS_FACE_ORDER=Object.freeze(['U','D','R','L','F','B']);
export function crossFaceDistances(cubie,tables){
  if(!cubie||!Array.isArray(cubie.ep)||!Array.isArray(cubie.eo))throw Error('CUBIE_REQUIRED');
  const output={};
  for(const face of CROSS_FACE_ORDER){
    const table=tables[face];
    if(!table||table.length!==190080)throw Error('PDB_REQUIRED_'+face);
    output[face]=table[indexOfFourEdges(cubie.ep,cubie.eo,FACE_EDGE_IDS[face])];
    if(output[face]===255)throw Error('UNREACHABLE_CROSS');
  }
  return output;
}
export function inferCrossGoalSet(firstTwoTurns,goalDistance){
  if(!Array.isArray(firstTwoTurns)||firstTwoTurns.length!==2)throw Error('TWO_OBSERVED_TURNS_REQUIRED');
  if(typeof goalDistance!=='function')throw Error('DISTANCE_FUNCTION_REQUIRED');
  const gains=Object.fromEntries(CROSS_FACE_ORDER.map(f=>[f,0]));
  for(const turn of firstTwoTurns){
    if(!turn||!turn.before||!turn.after||turn.kind!=='FACE_TURN')throw Error('TURN_CONTRACT_VIOLATION');
    for(const face of CROSS_FACE_ORDER){
      const a=goalDistance(face,turn.before),b=goalDistance(face,turn.after);
      if(!Number.isInteger(a)||!Number.isInteger(b)||a<0||b<0)throw Error('INVALID_GOAL_DISTANCE');
      gains[face]+=a-b;
    }
  }
  const maximum=Math.max(...Object.values(gains));
  const candidateFaces=CROSS_FACE_ORDER.filter(f=>gains[f]===maximum);
  return {candidateFaces,unique:candidateFaces.length===1,diagnosticTieBrokenFace:candidateFaces[0],gains};
}
