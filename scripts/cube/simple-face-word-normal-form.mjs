/**
 * CUBE-REV 0.11: conservative rewrite normal form for outer-face words.
 *
 * This is NOT a normal form for the whole Rubik cube group.
 * Relations permitted: F^4=1 for each face F, and opposite face turns
 * commute: [U,D]=[R,L]=[F,B]=1. This is the free product of the three
 * Z4 x Z4 subgroups. Wide, slice, and whole-cube moves are excluded.
 *
 * Equal results imply an exact algebraic rewrite using ONLY those relations;
 * unequal results imply the selected short rewrite system cannot connect
 * the words (NOT that the paths have different full cube-state endpoints).
 */
const pairs = Object.freeze({U:'UD',D:'UD',R:'RL',L:'RL',F:'FB',B:'FB'});
const token = /^([URFDLB])(2'?|'?)$/;
function parse(t) {
  const m=token.exec(t);
  if(!m) return null;
  return {face:m[1], exponent:m[2].startsWith('2')?2:m[2]==="'"?3:1};
}
export function simpleFaceWordNormalForm(moves) {
  if(!Array.isArray(moves)) throw new TypeError('moves must be an array');
  const stack=[];
  for(const t of moves){
    const parsed=parse(t);
    if(!parsed)return null; // not a face-only word: classify separately
    const {face,exponent}=parsed;
    const family=pairs[face];
    if(stack.length && stack.at(-1).family===family){
      const top=stack.at(-1);
      top.values[face]=(top.values[face]+exponent)%4;
      if(Object.values(top.values).every(v=>v===0))stack.pop();
    } else {
      const values=Object.fromEntries([...family].map(f=>[f,0]));
      values[face]=exponent;
      stack.push({family,values});
    }
  }
  return stack.map(({family,values})=>family+':'+[...family].map(f=>values[f]).join(',')).join('|');
}
export function classifySimpleFaceWordPair(a,b){
  const left=simpleFaceWordNormalForm(a);
  const right=simpleFaceWordNormalForm(b);
  if(left===null||right===null)return 'EXTENDED_GRAMMAR_UNCLASSIFIED';
  return left===right?'SIMPLE_REWRITE_EQUIVALENT':'REQUIRES_ADDITIONAL_CUBE_RELATION';
}
