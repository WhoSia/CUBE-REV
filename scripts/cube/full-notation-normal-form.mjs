/**
 * CUBE-REV 0.11 — conservative full notation decomposition.
 * Operates under the EXACT wide/slice definitions of sticker-cube.mjs.
 * A chronological word becomes fixed-frame face turns followed by a 24-state
 * rigid orientation. Face reductions use ONLY elementary opposite-face and
 * same-face relations; this is NOT a full cube-group word-problem solver.
 */
import {simpleFaceWordNormalForm} from './simple-face-word-normal-form.mjs';
const FACES='URFDLB';
const vectors={U:[0,1,0],R:[1,0,0],F:[0,0,1],D:[0,-1,0],L:[-1,0,0],B:[0,0,-1]};
const inverse=Object.fromEntries(Object.entries(vectors).map(([f,v])=>[v.join(','),f]));
const definitions={r:['x','L'],l:["x'",'R'],u:['y','D'],d:["y'",'U'],f:['z','B'],b:["z'",'F'],M:["x'","L'",'R'],E:["y'","D'",'U'],S:["F'","B",'z']};
const rx=/^([URFDLB]w|[urfdlb]|[MESxyz]|[URFDLB])(2'?|'?)$/;
function turn(token){const m=rx.exec(token);if(!m)throw new Error('UNKNOWN_CUBE_MOVE:'+token);
return {base:m[1],power:m[2].startsWith('2')?2:m[2]==="'"?3:1};}
function rotate(v,axis){const [x,y,z]=v;if(axis==='x')return[x,z,-y];if(axis==='y')return[-z,y,x];return[y,-x,z];}
export function expandCubeMove(token){const {base,power}=turn(token);
if(base.length===1&&'URFDLBxyz'.includes(base))return Array(power).fill(base);
const replacement=definitions[base.endsWith('w')?base[0].toLowerCase():base];
if(!replacement)throw Error('NO_EXACT_MOVE_DEFINITION:'+base);
return Array.from({length:power},()=>replacement.flatMap(expandCubeMove)).flat();}
export function normalizeCubeWord(tokens){
if(!Array.isArray(tokens))throw new TypeError('tokens must be an array');
let orientation=FACES.split('').map(f=>vectors[f]);const body=[];
for(const t of tokens)for(const u of expandCubeMove(t)){
if('xyz'.includes(u))orientation=orientation.map(v=>rotate(v,u));
else{const idx=orientation.findIndex(v=>v.join(',')===vectors[u].join(','));
if(idx<0)throw Error('FRAME_INVERSION_FAILURE');body.push(FACES[idx]);}}
const frame=orientation.map(v=>inverse[v.join(',')]).join('');
return {body,frame,elementary_form:simpleFaceWordNormalForm(body)};
}
export function classifyCubeWordPair(a,b){
const x=normalizeCubeWord(a),y=normalizeCubeWord(b);
if(x.frame!==y.frame)return 'DIFFERENT_FINAL_FRAME';
return x.elementary_form===y.elementary_form?'ELEMENTARY_REWRITE_EQUIVALENT':'ADDITIONAL_CUBE_RELATION_REQUIRED';
}
