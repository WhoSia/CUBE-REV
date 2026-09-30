(() => {
  "use strict";
  const MOVES=["U","U2","U'","R","R2","R'","F","F2","F'","D","D2","D'","L","L2","L'","B","B2","B'"];
  const $=id=>document.getElementById(id);
  const views={intro:$("intro"),trial:$("trial"),confidence:$("confidencePanel"),done:$("done")};
  let sessionId="", trials=[], cursor=0, shownAt=0, pending=null, log=[];

  function show(name){Object.values(views).forEach(v=>v.classList.add("hidden"));views[name].classList.remove("hidden")}
  function randInt(n){const a=new Uint32Array(1);crypto.getRandomValues(a);return a[0]%n}
  function shuffle(xs){const a=[...xs];for(let i=a.length-1;i>0;i--){const j=randInt(i+1);[a[i],a[j]]=[a[j],a[i]]}return a}
  function selectTrials(rows){
    const buckets=new Map([[1,[]],[2,[]],[3,[]]]);
    rows.forEach(r=>{if(buckets.has(r.d1))buckets.get(r.d1).push(r)});
    const chosen=[...shuffle(buckets.get(1)).slice(0,8),...shuffle(buckets.get(2)).slice(0,8),...shuffle(buckets.get(3)).slice(0,8)];
    const side=shuffle([...Array(12).fill("A"),...Array(12).fill("B")]);
    return shuffle(chosen).map((r,i)=>({...r,arm:side[i]}));
  }
  function renderFacelets(s){
    if(!/^[URFDLB]{54}$/.test(s))throw new Error("BAD_FACELETS");
    const net=$("cubeNet");net.textContent="";
    const pos={U:[3,0],L:[0,3],F:[3,3],R:[6,3],B:[9,3],D:[3,6]};
    const order=["U","R","F","D","L","B"];
    order.forEach((face,fi)=>{
      const div=document.createElement("div");div.className="face";div.style.gridColumn=(pos[face][0]+1)+"/span 3";div.style.gridRow=(pos[face][1]+1)+"/span 3";
      s.slice(fi*9,fi*9+9).split("").forEach(ch=>{const x=document.createElement("span");x.className="sticker "+ch;div.appendChild(x)});
      net.appendChild(div);
    });
  }
  function current(){return trials[cursor]}
  function showTrial(){
    if(cursor>=trials.length){show("done");return}
    const t=current(), arm=t.arm, state=arm==="A"?t.a:t.b;
    $("progress").textContent=`${cursor+1} / ${trials.length}`;
    $("session").textContent=sessionId.slice(0,8);
    renderFacelets(state.facelets);
    shownAt=performance.now();pending=null;show("trial");
  }
  function chooseMove(move){
    if(pending)return;
    const t=current(), now=performance.now(), state=t.arm==="A"?t.a:t.b;
    pending={sequence:cursor+1,family:t.family,arm:t.arm,dg:t.dg,d1:t.d1,q:t.q,solutions:t.solutions,firstMask:t.firstMask,prefix2:t.prefix2,scramble:state.scramble,slack:state.slack,move,latencyMs:Math.round((now-shownAt)*10)/10};
    show("confidence");
  }
  MOVES.forEach(m=>{const b=document.createElement("button");b.textContent=m;b.addEventListener("click",()=>chooseMove(m));$("moves").appendChild(b)});
  for(let n=1;n<=5;n++){const b=document.createElement("button");b.textContent=String(n);b.addEventListener("click",()=>{pending.confidence=n;log.push(pending);pending=null;cursor++;showTrial()});$("confidence").appendChild(b)}

  $("start").addEventListener("click",()=>{
    if(!Array.isArray(window.G7_STIMULI)||window.G7_STIMULI.length!==90)throw new Error("STIMULUS_MANIFEST_REFUSE");
    sessionId=crypto.randomUUID();
    trials=selectTrials(window.G7_STIMULI);cursor=0;log=[];
    log.meta={sessionId,startedAt:new Date().toISOString(),instrument:"G7-P1",manifestSha256:window.G7_MANIFEST_SHA256,expertise:{familiarity:$("familiarity").value,solveBand:$("solveBand").value,method:$("method").value,practice:$("practice").value,notation:$("notation").checked}};
    showTrial();
  });
  $("download").addEventListener("click",()=>{
    const payload={meta:log.meta,trials:[...log],completedAt:new Date().toISOString()};
    const blob=new Blob([JSON.stringify(payload,null,2)],{type:"application/json"});
    const url=URL.createObjectURL(blob),a=document.createElement("a");a.href=url;a.download=`cube-rev-g7-p1-${sessionId}.json`;a.click();URL.revokeObjectURL(url);
  });
  $("reset").addEventListener("click",()=>location.reload());
})();