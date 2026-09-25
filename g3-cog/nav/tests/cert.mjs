import {chromium} from 'playwright';
import {readFileSync,mkdirSync,writeFileSync} from 'node:fs';
const BASE=process.env.RSTP_NAV_URL||'http://127.0.0.1:4174';
const packet=JSON.parse(readFileSync('g3-cog/nav/packet.json','utf8'));
const candidate=JSON.parse(readFileSync('g3-cog/nav/candidate.json','utf8'));
const mod=n=>(n%5+5)%5;
const apply=([x,y],a)=>{if(a==='E')x++;else if(a==='W')x--;else if(a==='N')y++;else if(a==='S')y--;else throw Error(a);return[mod(x),mod(y)]};
const same=(a,b)=>a[0]===b[0]&&a[1]===b[1];
const hist=h=>Object.fromEntries([...new Set(h)].sort().map(a=>[a,h.filter(x=>x===a).length]));
const run=h=>{let s=[...packet.start],k='A',trace=[s.join(',')];for(const a of h){s=apply(s,a);if(k==='I'||same(s,packet.context_trigger))k='I';trace.push(s.join(','));}return{s,k,trace}};
const suffix=packet.common_suffix;
const pre=h=>run(h.slice(0,-suffix.length)).s;
const perms=xs=>xs.length<2?xs:[...xs].flatMap((x,i)=>perms(xs.slice(0,i).concat(xs.slice(i+1))).map(p=>x+p));
const permutations=perms([... 'ABCD']);
const pairs=[['AVOID1','AVOID2','equal'],['HIT','AVOID1','divergent']];
const matchedR=[['N2X9F6RT','N5H7Q2WB'],['N8C1V4JL','N3D6K9SP']];
const formal=[];
for(const [a,b,kind] of pairs){const A=run(packet.histories[a]),B=run(packet.histories[b]);formal.push({pair:`${a}/${b}`,kind,same_terminal:same(A.s,B.s)&&same(A.s,packet.probe),same_pre_suffix:same(pre(packet.histories[a]),pre(packet.histories[b])),suffix:A.trace.length===B.trace.length&&packet.histories[a].slice(-2).join(',')===suffix.join(',')&&packet.histories[b].slice(-2).join(',')===suffix.join(','),histogram:JSON.stringify(hist(packet.histories[a]))===JSON.stringify(hist(packet.histories[b])),context:kind==='equal'?A.k===B.k:A.k!==B.k});}
const dist=(p,g)=>{const d=Math.abs(p-g);return Math.min(d,5-d)};const score=a=>{const s=apply(packet.probe,a);return dist(s[0],packet.goal[0])+dist(s[1],packet.goal[1])};const scores=Object.fromEntries(packet.actions.map(a=>[a,score(a)])),m=Math.min(...Object.values(scores)),optimal=packet.actions.filter(a=>scores[a]===m);
const receipt={schema:'CUBE-REV-G3-P11-NAV-CERT-v4',candidate_id:candidate.candidate_id,base_url:BASE,browser:null,formal_contract:{pass:0,total:formal.length+1,details:formal,optimal_first_moves:optimal},browser_cells:{pass:0,total:packet.cells.length*permutations.length},manifest_uniqueness:{pass:0,total:packet.cells.length},representation_labels:{pass:0,total:packet.cells.filter(c=>c.R===1).length*permutations.length},physical_render_invariance:{pass:0,total:packet.cells.length*permutations.length},matched_r0_r1_physical_surface:{pass:0,total:matchedR.length},response_lock:{pass:0,total:packet.cells.length*packet.actions.length},cross_task_preseal:{estimand:packet.scientific_contract.primary_estimand,normalized_divergence:'JSD / ln(2)',contrasts:['Delta_K = D(divergent,R0)-D(control,R0)','Delta_R = D(divergent,R0)-D(divergent,R1)']},result:'PENDING',diagnostics:[]};
let browser=null;
try{
  for(const d of formal)if(Object.entries(d).filter(([k])=>!['pair','kind'].includes(k)).every(([,v])=>v===true))receipt.formal_contract.pass++;
  if(optimal.length===2&&optimal.includes('N')&&optimal.includes('E'))receipt.formal_contract.pass++;
  if(receipt.formal_contract.pass!==receipt.formal_contract.total)throw Error('formal RSTP contract failed');
  browser=await chromium.launch({headless:true});receipt.browser=await browser.version();const page=await browser.newPage({viewport:{width:900,height:900},deviceScaleFactor:1});
  page.on('pageerror',e=>receipt.diagnostics.push({type:'pageerror',text:String(e)}));
  page.on('console',m=>{if(['error','warning'].includes(m.type()))receipt.diagnostics.push({type:`console_${m.type()}`,text:m.text().slice(0,1000)});});
  const wait=async label=>{await page.waitForFunction(()=>window.RSTPNav&&['RESPONSE_ARM','FAIL_CLOSED'].includes(window.RSTPNav.snapshot().phase),null,{timeout:10000});const s=await page.evaluate(()=>window.RSTPNav.snapshot());if(s.phase!=='RESPONSE_ARM')throw Error(`${label}: runtime ${s.phase}: ${s.fail_reason}`);return s};
  const physicalSignature=async()=>JSON.stringify(await page.locator('#grid .cell').evaluateAll(ns=>ns.map(n=>{const r=n.getBoundingClientRect(),s=getComputedStyle(n);return{x:n.dataset.x,y:n.dataset.y,classes:[...n.classList].filter(c=>c!=='marker').sort(),rect:[r.x,r.y,r.width,r.height].map(v=>Math.round(v*1000)/1000),background:s.backgroundColor,borderColor:s.borderColor,outline:s.outline,boxShadow:s.boxShadow};})));
  for(const cell of packet.cells){let baseline=null;const manifests=new Set();for(const perm of permutations){await page.goto(`${BASE}/?cell=${cell.id}&perm=${perm}&speed=0`,{waitUntil:'domcontentloaded',timeout:15000});const s=await wait(`${cell.id}/${perm}`);if(s.state.join(',')!==packet.probe.join(',')||s.context!==cell.K||s.trace.length!==6||s.manifest?.candidate_id!==candidate.candidate_id||s.manifest_hash?.length!==64)throw Error(`${cell.id}/${perm} semantic drift`);receipt.browser_cells.pass++;manifests.add(s.manifest_hash);
      if(cell.R===1){const markerMap=await page.locator('.marker').evaluateAll(ns=>Object.fromEntries(ns.map(n=>[n.dataset.landmark,n.textContent])));const mappingOK=Object.keys(markerMap).length===packet.landmarks.length&&packet.landmarks.every((p,i)=>markerMap[p.join(',')]===perm[i]);if(!mappingOK)throw Error(`${cell.id}/${perm} landmark-label mapping`);receipt.representation_labels.pass++;}
      const sig=await physicalSignature();if(baseline===null)baseline=sig;else if(sig!==baseline)throw Error(`${cell.id}/${perm} physical render changed`);receipt.physical_render_invariance.pass++;
    }if(manifests.size===permutations.length)receipt.manifest_uniqueness.pass++;else throw Error(`${cell.id} manifest permutation collision`);}
  for(const [r0,r1] of matchedR){const sigs=[],states=[];for(const id of [r0,r1]){await page.goto(`${BASE}/?cell=${id}&perm=ABCD&speed=0`,{waitUntil:'domcontentloaded',timeout:15000});const s=await wait(`${r0}/${r1}/${id}`);sigs.push(await physicalSignature());states.push(s.state.join(','));}if(sigs[0]!==sigs[1]||states[0]!==states[1])throw Error(`${r0}/${r1} R-layer changed physical surface`);receipt.matched_r0_r1_physical_surface.pass++;}
  for(const cell of packet.cells)for(const a of packet.actions){await page.goto(`${BASE}/?cell=${cell.id}&perm=ABCD&speed=0`,{waitUntil:'domcontentloaded',timeout:15000});const preSnap=await wait(`${cell.id}/${a}`);await page.locator(`[data-action="${a}"]`).click();const post=await page.evaluate(()=>window.RSTPNav.snapshot());if(post.phase!=='END'||post.locked?.action!==a||post.locked?.manifest_hash!==preSnap.manifest_hash)throw Error(`${cell.id}/${a} response lock`);receipt.response_lock.pass++;}
  for(const k of ['browser_cells','manifest_uniqueness','representation_labels','physical_render_invariance','matched_r0_r1_physical_surface','response_lock'])if(receipt[k].pass!==receipt[k].total)throw Error(`${k} incomplete`);
  receipt.result='PASS_RSTP_G3_INSTRUMENT_PORTABILITY_PREFLIGHT';
}catch(e){receipt.result='FAIL';receipt.error=String(e?.stack||e);process.exitCode=1;
}finally{
  if(browser){try{await browser.close();}catch(e){receipt.diagnostics.push({type:'browser_close',text:String(e)});}}
  mkdirSync('g3-cog/nav/certification',{recursive:true});writeFileSync('g3-cog/nav/certification/p11-receipt.json',JSON.stringify(receipt,null,2)+'\n');console.log(JSON.stringify(receipt,null,2));
}
