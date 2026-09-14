const q=new URLSearchParams(location.search);
const speed=Math.max(0,Number(q.get('speed')??250));
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const mod=n=>(n%5+5)%5;
const stable=v=>Array.isArray(v)?`[${v.map(stable).join(',')}]`:v&&typeof v==='object'?`{${Object.keys(v).sort().map(k=>`${JSON.stringify(k)}:${stable(v[k])}`).join(',')}}`:JSON.stringify(v);
async function sha256(text){const b=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(text));return[...new Uint8Array(b)].map(x=>x.toString(16).padStart(2,'0')).join('');}
function apply([x,y],a){if(a==='E')x++;else if(a==='W')x--;else if(a==='N')y++;else if(a==='S')y--;else throw new Error(`unsupported action ${a}`);return[mod(x),mod(y)];}
function same(a,b){return a[0]===b[0]&&a[1]===b[1];}
function optimalFirstMoves(state,goal){const dist=(p,g)=>{const d=Math.abs(p-g);return Math.min(d,5-d)};const score=a=>{const s=apply(state,a);return dist(s[0],goal[0])+dist(s[1],goal[1]);};const actions=['N','E','S','W'],scores=Object.fromEntries(actions.map(a=>[a,score(a)])),m=Math.min(...Object.values(scores));return actions.filter(a=>scores[a]===m);}

const packet=await fetch('packet.json',{cache:'no-store'}).then(r=>{if(!r.ok)throw new Error(`packet HTTP ${r.status}`);return r.json();});
const candidate=await fetch('candidate.json',{cache:'no-store'}).then(r=>{if(!r.ok)throw new Error(`candidate HTTP ${r.status}`);return r.json();});
const cellId=q.get('cell')||packet.cells[0].id;
const cell=packet.cells.find(c=>c.id===cellId);
if(!cell)throw new Error(`unknown cell ${cellId}`);
const perm=(q.get('perm')||'ABCD').toUpperCase();
if(!/^[ABCD]{4}$/.test(perm)||new Set(perm).size!==4)throw new Error(`bad permutation ${perm}`);
const history=packet.histories[cell.history];

const runtime={phase:'LOAD',state:[...packet.start],context:'A',trace:[],locked:null,receipt:[],manifest:null,manifest_hash:null,optimal_first_moves:null};
window.RSTPNav={snapshot:()=>JSON.parse(JSON.stringify(runtime)),apply,optimalFirstMoves};
const el=id=>document.getElementById(id);
const grid=el('grid'),phaseEl=el('phase'),cellEl=el('cell'),moveEl=el('move-index'),debug=el('debug');
const buttons=[...document.querySelectorAll('[data-action]')];
function record(type,extra={}){runtime.receipt.push({type,t:performance.now(),...extra});}
function setPhase(p){runtime.phase=p;phaseEl.textContent=p;record('PHASE',{phase:p});}
function updateContext(after){if(runtime.context==='I'||same(after,packet.context_trigger))runtime.context='I';}
function draw(){
  grid.textContent='';
  const labelByKey=new Map(packet.landmarks.map((p,i)=>[p.join(','),perm[i]]));
  for(let y=4;y>=0;y--)for(let x=0;x<5;x++){
    const d=document.createElement('div');d.className='cell';d.dataset.x=String(x);d.dataset.y=String(y);
    if(same([x,y],packet.goal))d.classList.add('goalCell');
    if(same([x,y],runtime.state))d.classList.add('agentCell');
    if(cell.R===1&&labelByKey.has(`${x},${y}`)){const m=document.createElement('span');m.className='marker';m.dataset.landmark=`${x},${y}`;m.textContent=labelByKey.get(`${x},${y}`);d.appendChild(m);}
    grid.appendChild(d);
  }
  el('support-legend').classList.toggle('hidden',cell.R!==1);
  debug.textContent=`state=${runtime.state.join(',')} context=${runtime.context} perm=${perm}`;
}
function fail(reason){setPhase('FAIL_CLOSED');runtime.fail_reason=reason;buttons.forEach(b=>b.disabled=true);record('FAIL',{reason});throw new Error(reason);}
buttons.forEach(b=>b.addEventListener('click',async()=>{
  if(runtime.phase!=='RESPONSE_ARM'||runtime.locked)return;
  const action=b.dataset.action;
  runtime.locked={action,t:performance.now(),manifest_hash:runtime.manifest_hash};
  buttons.forEach(x=>x.disabled=true);record('RESPONSE',{action,manifest_hash:runtime.manifest_hash});setPhase('END');
}));

async function run(){
  try{
    cellEl.textContent=cell.id;
    draw();record('LOAD',{cell:cell.id});
    const manifest={schema:'CUBE-REV-G3-P11-NAV-SESSION-MANIFEST-v1',candidate_id:candidate.candidate_id,packet_schema:packet.schema,cell_id:cell.id,O:cell.O,R:cell.R,permutation:perm,history_id:cell.history,estimand:packet.scientific_contract.primary_estimand,human_collection:false};
    runtime.manifest=manifest;runtime.manifest_hash=await sha256(stable(manifest));
    setPhase('HISTORY');
    for(let i=0;i<history.length;i++){
      const before=[...runtime.state],a=history[i];runtime.state=apply(runtime.state,a);updateContext(runtime.state);
      runtime.trace.push({i:i+1,before,action:a,after:[...runtime.state],context:runtime.context});moveEl.textContent=`${i+1}/${history.length}`;draw();record('MOVE',{i:i+1,action:a,state:runtime.state.join(','),context:runtime.context});
      if(speed)await sleep(speed);
    }
    if(!same(runtime.state,packet.probe))fail(`probe mismatch ${runtime.state} != ${packet.probe}`);
    if(runtime.context!==cell.K)fail(`context mismatch ${runtime.context} != ${cell.K}`);
    runtime.optimal_first_moves=optimalFirstMoves(runtime.state,packet.goal);
    if(runtime.optimal_first_moves.length<2)fail('degenerate probe action surface');
    setPhase('RESPONSE_ARM');buttons.forEach(b=>b.disabled=false);draw();record('ARM',{state:runtime.state.join(','),context:runtime.context,optimal_first_moves:runtime.optimal_first_moves});
  }catch(e){if(runtime.phase!=='FAIL_CLOSED'){runtime.fail_reason=String(e?.message||e);runtime.phase='FAIL_CLOSED';phaseEl.textContent='FAIL_CLOSED';buttons.forEach(b=>b.disabled=true);record('FAIL',{reason:runtime.fail_reason});}console.error(e);}
}
run();
