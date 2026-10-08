/** CUBE-REV 0.11: Group-certified substitution of a recorded move word.
 * This is a mathematical counterfactual, NOT evidence that a human made this choice.
 */
import {operatorSignature} from './operator-permutation.mjs';
export function transferObservedWord(prefixes,start,expected,replacement){
 if(!Array.isArray(prefixes)||!Array.isArray(expected)||!Array.isArray(replacement))throw Error('BAD_INPUT');
 if(expected.length!==replacement.length||!expected.length)throw Error('LENGTH_MISMATCH');
 if(!Number.isInteger(start)||start<0||start+expected.length>prefixes.length)throw Error('BOUNDS');
 const tokens=prefixes.map(p=>typeof p==='string'?p:p.raw);
 const normalize=t=>String(t).replace(/2'$/,'2');
 if(tokens.slice(start,start+expected.length).map(normalize).join(' ')!==expected.map(normalize).join(' '))throw Error('OBSERVED_WORD_MISMATCH');
 for(let i=start;i<start+expected.length-1;i++){
  const p=prefixes[i];
  if(typeof p!=='string'&&(p.annotation_after||p.boundary_after))throw Error('STAGE_BOUNDARY_CROSSED');
 }
 if(operatorSignature(expected.map(normalize))!==operatorSignature(replacement.map(normalize)))throw Error('OPERATOR_NOT_EQUIVALENT');
 const out=[...tokens];out.splice(start,expected.length,...replacement);
 return out;
}
