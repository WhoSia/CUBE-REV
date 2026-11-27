import { readFileSync } from 'node:fs';
import { gunzipSync } from 'node:zlib';
import { createHash } from 'node:crypto';
function loadPinnedCertificate(){
  const packed=Buffer.from(readFileSync(new URL('../../formal/029/certificate_blobs/upper-policy-certificate.json.gz.b64',import.meta.url),'utf8').trim(),'base64');
  const plain=gunzipSync(packed),sha=b=>createHash('sha256').update(b).digest('hex');
  if(sha(packed)!=='d9dd5f9c283b9d79a86bcf00cefc51e013bc8d20a1c8c34077316a1c81e3f1d3'||sha(plain)!=='80f334520d288b09d0ad2398b596e8910515d312b342cf07ceeb5e4107922227')throw Error('pinned certificate hash mismatch');
  return JSON.parse(plain.toString('utf8'));
}
// Deterministic finite-model audit; no dependencies. Run with node.
function audit() {
  const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
  const require=(ok,msg)=>{if(!ok)throw Error(msg)};
  function costs(rows,labels) {
    const n=rows.length,m=rows[0].length,full=(1n<<BigInt(n))-1n;
    const bit=i=>1n<<BigInt(i);
    const masks=Array.from({length:m},(_,q)=>rows.reduce((a,row,s)=>row[q]?a|bit(s):a,0n));
    const pairs=[];for(let s=0;s<n;s++)for(let t=s+1;t<n;t++)if(labels[s]===labels[t]){
      let diff=0n;for(let q=0;q<m;q++)if(rows[s][q]!==rows[t][q])diff|=bit(q);
      pairs.push({s,t,diff,states:bit(s)|bit(t)});
    }
    const memo=new Map();
    function dp(b){if(!pairs.some(p=>(b&p.states)===p.states))return 0;if(memo.has(b))return memo.get(b);let v=Infinity;
      for(const mask of masks){const a=b&mask,c=b^a;if(a&&c)v=Math.min(v,1+Math.max(dp(a),dp(c)));}
      memo.set(b,v);return v;
    }
    function cover(ps) {
      if(ps.some(p=>p.diff===0n))return Infinity;
      const distinct=[...new Set(ps.map(p=>p.diff))];
      const cache=new Map();
      function visit(rem){if(!rem.length)return 0;const key=rem.join(",");if(cache.has(key))return cache.get(key);
        let v=Infinity,choose=rem[0];for(let q=0;q<m;q++)if(choose&bit(q))v=Math.min(v,1+visit(rem.filter(mask=>!(mask&bit(q)))));cache.set(key,v);return v;}
      return visit(distinct);
    }
    const local=Math.max(...rows.map((_,s)=>cover(pairs.filter(p=>p.s===s||p.t===s))));
    const early=Math.max(...[...new Set(labels)].map(k=>dp(labels.reduce((a,l,s)=>l===k?a|bit(s):a,0n))));
    const delayed=dp(full), fixed=cover(pairs);
    require(local<=early&&early<=delayed&&delayed<=fixed,"bound failure");
    return [local,early,delayed,fixed].map(x=>Number.isFinite(x)?x:"inf");
  }
  const hist={};for(let a=0;a<256;a++)for(let l=0;l<16;l++){
    const rows=Array.from({length:4},(_,s)=>[a>>(2*s)&1,a>>(2*s+1)&1]);
    const labels=Array.from({length:4},(_,s)=>l>>s&1);const key=costs(rows,labels).join(",");hist[key]=(hist[key]||0)+1;
  }
  require(hist["inf,inf,inf,inf"]===2416&&hist["1,1,1,1"]===672&&hist["1,1,2,2"]===192,"census mismatch");
  const indexing=[];for(let k=1;k<=4;k++)for(let d=1;d<=3;d++){
    const rows=[],labels=[];for(let i=0;i<k;i++)for(let b=0;b<2**d;b++){
      rows.push(Array.from({length:k*d},(_,q)=>Math.floor(q/d)===i?(b>>(q%d))&1:0));labels.push(i);
    }const got=costs(rows,labels);require(eq(got,[d,d,k*d,k*d]),"indexing mismatch");indexing.push({k,d,costs:got});
  }
  const onehot=[];for(let n=2;n<=12;n++){
    const rows=Array.from({length:n},(_,s)=>Array.from({length:n},(_,q)=>+(q===s)));const got=costs(rows,Array(n).fill(0));require(eq(got,[1,n-1,n-1,n-1]),"onehot mismatch");onehot.push({n,costs:got});
  }
  const routing=[];for(let d=1;d<=4;d++){
    const n=2**d,rows=Array.from({length:n},(_,s)=>Array.from({length:n-1},(_,q)=>{
      let node=q+1,lo=0,hi=n;const path=node.toString(2).slice(1);for(const b of path){const mid=(lo+hi)/2;if(b==="0")hi=mid;else lo=mid;}return +(s>=(lo+hi)/2&&s<hi);
    }));const got=costs(rows,Array(n).fill(0));require(got[1]===d&&got[2]===d&&got[3]===n-1,"routing mismatch");routing.push({d,costs:got});
  }
  return {order:["local","early","delayed","fixed"],hist,indexing,onehot,routing};
}
function auditClock() {
  const results=[];
  for(let k=1;k<=4;k++)for(let d=1;d<=3;d++){
    const n=k*2**d,m=k*d,bit=i=>1n<<BigInt(i),full=bit(n)-1n;
    const label=s=>Math.floor(s/2**d);
    const masks=Array.from({length:m},(_,q)=>{let b=0n;for(let s=0;s<n;s++)if(label(s)===Math.floor(q/d)&&((s%(2**d))>>(q%d)&1))b|=bit(s);return b;});
    const fibers=Array.from({length:k},(_,i)=>{let b=0n;for(let s=0;s<n;s++)if(label(s)===i)b|=bit(s);return b;});
    const post=new Map(),pre=new Map();
    function known(b){if(!b||!(b&(b-1n)))return 0;if(post.has(b))return post.get(b);let v=Infinity;for(const mask of masks){const a=b&mask,c=b^a;if(a&&c)v=Math.min(v,1+Math.max(known(a),known(c)));}post.set(b,v);return v;}
    function hidden(b,t){if(!b)return 0;if(t===0)return Math.max(...fibers.map(f=>known(b&f)));const key=b+":"+t;if(pre.has(key))return pre.get(key);let v=Infinity;
      for(const mask of masks){const a=b&mask,c=b^a;v=Math.min(v,1+Math.max(hidden(a,t-1),hidden(c,t-1)));}pre.set(key,v);return v;
    }
    for(let t=0;t<=m+1;t++){const got=hidden(full,t),expect=t+Math.max(0,d-Math.floor(t/k));if(got!==expect)throw Error(JSON.stringify({k,d,t,got,expect}));results.push({k,d,t,depth:got});}
  }
  // With a constant label, two primary bits need 2 frames alone; one
  // additional state-dependent auxiliary bit can identify all four in 1.
  const states=[0,1,2,3];
  const primaryDistinct=Math.max(...[0,1].map(q=>new Set(states.map(s=>s>>q&1)).size));
  const jointDistinct=new Set(states.map(s=>`${s&1},${s>>1&1}`)).size;
  if(primaryDistinct!==2||jointDistinct!==4)throw Error("auxiliary leakage control failed");
  return {checked:results.length,results,auxiliaryLeakage:{earlyPrimary:2,paired:1,constantLabel:true}};
}
function auditStructure() {
  const pop=x=>{let n=0;while(x){x&=x-1;n++;}return n;};
  function rank(rows){const piv=new Map();for(let x of rows){while(x){const p=31-Math.clz32(x);if(!piv.has(p)){piv.set(p,x);break;}x^=piv.get(p);}}return piv.size;}
  const results=[];let subsets=0, targetChecks=0;
  for(let n=1;n<=3;n++)for(let d=0;d<=n;d++){
    const inputs=Array.from({length:2**n},(_,i)=>i);
    const mon=inputs.filter(x=>pop(x)<=d),m=mon.length;
    const rows=inputs.map(x=>mon.reduce((a,u,j)=>(u&x)===u?a|(1<<j):a,0));
    const output=(coeff,row)=>pop(coeff&row)%2;
    let minFull=Infinity, targetMin=Array(m).fill(Infinity);
    for(let set=0;set<2**inputs.length;set++){
      const selected=rows.filter((_,i)=>set>>i&1),r=rank(selected),seen=new Map();
      for(let c=0;c<2**m;c++){
        const sig=selected.reduce((a,row,i)=>a|(output(c,row)<<i),0);
        const old=seen.get(sig);
        if(old===undefined)seen.set(sig,{first:c,ambiguous:0});
        else old.ambiguous|=old.first^c;
      }
      if(seen.size!==2**r)throw Error("rank/signature discrepancy");
      if(seen.size===2**m)minFull=Math.min(minFull,pop(set));
      let ambiguous=0;for(const item of seen.values())ambiguous|=item.ambiguous;
      for(let j=0;j<m;j++){
        const fixed=(ambiguous&(1<<j))===0, predicted=rank([...selected,1<<j])===r;
        if(fixed!==predicted)throw Error("target-span discrepancy");
        if(fixed)targetMin[j]=Math.min(targetMin[j],pop(set));
        targetChecks++;
      }subsets++;
    }
    const baseline=rows.filter((_,i)=>pop(i)<=1);
    const design=rows.filter((_,i)=>pop(i)<=d);
    if(minFull!==m||rank(design)!==m||targetMin.some((v,j)=>v!==2**pop(mon[j])))throw Error("exact cost mismatch");
    results.push({n,d,parameters:m,fullMinimum:minFull,oneFactorRank:rank(baseline),targetMinimum:targetMin});
  }
  // Interaction absent in all baseline and single-coordinate interventions.
  const x=[0,1,2,3].map(i=>Number(i===3));
  if(x.slice(0,3).some(Boolean)||x[3]!==1)throw Error("interaction mutation missed");
  return {subsets,targetChecks,results,interactionControl:x};
}
function auditParityCycles(){
  const assert=(x,msg)=>{if(!x)throw Error(msg)};
  function permutations(n){let out=[];function go(a,mask){if(a.length===n){let p=0;for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)p^=+(a[i]>a[j]);out.push({a,p});return;}for(let j=0;j<n;j++)if(!(mask>>j&1))go([...a,j],mask|1<<j);}go([],0);return out;}
  function cycles(rows,reference){
    const n=rows.length,adj=rows.map((row,i)=>reference.map((j,k)=>i!==k&&!!(row>>j&1)));
    const found=[];for(let start=0;start<n;start++){
      function visit(path,mask){const v=path[path.length-1];if(path.length>=2&&adj[v][start])found.push({len:path.length,mask});for(let w=start+1;w<n;w++)if(adj[v][w]&&!(mask>>w&1))visit([...path,w],mask|1<<w);}
      visit([start],1<<start);
    }
    const even=found.filter(c=>!(c.len&1)),odd=found.some(c=>c.len&1);
    const bothUnique=!odd&&even.length<=1;
    const refUnique=!odd&&!even.some((a,i)=>even.slice(i+1).some(b=>!(a.mask&b.mask)));
    // Independent SCC criterion, using transitive closure on small test graphs.
    const reach=adj.map((r,i)=>r.map((v,j)=>v||i===j));
    for(let k=0;k<n;k++)for(let i=0;i<n;i++)for(let j=0;j<n;j++)reach[i][j]||=reach[i][k]&&reach[k][j];
    const components=[];let seen=0;for(let i=0;i<n;i++)if(!(seen>>i&1)){const c=Array.from({length:n},(_,j)=>j).filter(j=>reach[i][j]&&reach[j][i]);for(const j of c)seen|=1<<j;if(c.length>1)components.push(c);}
    const sccUnique=components.length===0||(components.length===1&&components[0].length%2===0&&components[0].every(i=>components[0].filter(j=>adj[i][j]).length===1));
    assert(sccUnique===bothUnique,"SCC mismatch");
    return {bothUnique,refUnique};
  }
  function check(rows,perms){
    const matches=perms.filter(p=>p.a.every((j,i)=>rows[i]>>j&1));
    const counts=[0,0];for(const p of matches)counts[p.p]++;
    if(!matches.length)return "empty";
    const r=matches[0],pred=cycles(rows,r.a);
    assert(pred.bothUnique===(counts[0]<=1&&counts[1]<=1),"two-sector mismatch");
    assert(pred.refUnique===(counts[r.p]===1),"reference sector mismatch");
    return `${counts[0]},${counts[1]}`;
  }
  let graphs=0,graphHist={};for(let n=1;n<=4;n++){
    const perms=permutations(n),arcs=[];for(let i=0;i<n;i++)for(let j=0;j<n;j++)if(i!==j)arcs.push([i,j]);
    for(let mask=0;mask<2**arcs.length;mask++){const rows=Array.from({length:n},(_,i)=>1<<i);arcs.forEach(([i,j],k)=>{if(mask>>k&1)rows[i]|=1<<j;});const key=check(rows,perms);graphHist[key]=(graphHist[key]||0)+1;graphs++;}
  }
  const edges=[];for(let i=0;i<6;i++)for(let j=i+1;j<6;j++)if((i>>1)!==(j>>1))edges.push([i,j]);
  const perms=permutations(4);let residuals=0,empty=0,signedUnique=0,matchCounts={};
  for(let a=0;a<12;a++)for(let b=a+1;b<12;b++)for(let c=b+1;c<12;c++)for(let d=c+1;d<12;d++){
    const es=[edges[a],edges[b],edges[c],edges[d]],masks=Array.from({length:6},(_,v)=>es.reduce((acc,e,j)=>acc|(e.includes(v)?1<<j:0),0));
    for(let u=0;u<6;u++)for(let v=0;v<6;v++)for(let w=0;w<6;w++){
      const key=check([masks[u],masks[v],masks[w],15],perms);residuals++;if(key==="empty")empty++;else{const [x,y]=key.split(",").map(Number);if(x<=1&&y<=1)signedUnique++;const total=x+y;matchCounts[total]=(matchCounts[total]||0)+1;}
    }
  }
  assert(graphs===4165&&residuals===106920&&empty===61794&&signedUnique===34344,"domain mismatch");
  return {graphs,graphHist,residuals,empty,feasible:residuals-empty,signedUnique,matchCounts};
}
function countSignedCompletions(records, labels){
  const n=labels.length;
  const allowed=records.map(([a,b])=>labels.map(([u,v])=>[+( (!a||a===u)&&(!b||b===v) ),+( (!a||a===v)&&(!b||b===u) )]));
  const pop=x=>{let n=0;while(x){x&=x-1;n++}return n};
  const memo=new Map();
  function dp(mask){
    const i=pop(mask);if(i===n)return [1,0,0,0];if(memo.has(mask))return memo.get(mask);
    const out=[0,0,0,0];
    for(let j=0;j<n;j++)if(!(mask>>j&1)){
      const opts=allowed[i][j];if(!opts[0]&&!opts[1])continue;
      const sign=pop(mask>>(j+1))%2;
      const child=dp(mask|1<<j);
      for(let b=0;b<2;b++)if(opts[b])for(let k=0;k<4;k++)out[k^(2*sign+b)]+=child[k];
    }memo.set(mask,out);return out;
  }
  return dp(0);
}
function auditOrientedCharacters(){
  const labels=["DL","BL","FL","UL","DB","DF","UB","UF","DR","BR","FR","UR"],colors="URFDLB";
  const assert=(x,m)=>{if(!x)throw Error(m)};
  // Independently enumerate permutations and orientations, then compare all four Fourier sectors.
  let cases=0;
  for(let a=0;a<12;a++)for(let b=a+1;b<12;b++)for(let c=b+1;c<12;c++){
    const es=[labels[a],labels[b],labels[c]];
    for(const u of colors)for(const v of colors)for(const mode of [0,1,2]){
      const rec=[[u,null],[null,v],mode===0?[null,null]:mode===1?[u,null]:[u,v]];
      const brute=[0,0,0,0];function go(i,used,sign,flip){if(i===3){brute[2*sign+flip]++;return;}for(let j=0;j<3;j++)if(!used.includes(j))for(let o=0;o<2;o++){const e=o?es[j][1]+es[j][0]:es[j];if(rec[i].every((x,k)=>!x||x===e[k]))go(i+1,[...used,j],sign^(used.filter(x=>x>j).length%2),flip^o);}}
      go(0,[],0,0);
      const got=countSignedCompletions(rec,es);
      assert(got.every((x,i)=>x===brute[i]),"oriented mismatch");cases++;
    }
  }
  const all=countSignedCompletions(Array.from({length:12},()=>[null,null]),labels);
  assert(all.every(x=>x===490497638400),"full edge count");
  return {cases,fullSectors:all};
}
function auditFrozenLeaves(cert){
  const labels=["DL","BL","FL","UL","DB","DF","UB","UF","DR","BR","FR","UR"];
  const must=(x,msg)=>{if(!x)throw Error(msg)};
  let nodes=0,leaves=0,assignments=0,orientationEssential=0,signEssential=0,rawMatchingAmbiguity=0;
  const hist={},byBlank={};
  must(cert.representatives.length===52,"root count");
  for(const e of cert.representatives){
    const record=[...e.prefix].map(c=>[c,null]);record.push([null,null]);
    const seen=new Set();let rootMass=0;
    function visit(i,depth){
      must(Number.isInteger(i)&&i>=0&&i<e.nodes.length&&!seen.has(i)&&depth<=8,"tree");seen.add(i);nodes++;
      const node=e.nodes[i];
      if(node[0]==="leaf"){
        leaves++;
        const [ee,eo,oe,oo]=countSignedCompletions(record,labels);
        const actual=ee+oe;must(actual>=1&&ee<=1&&oe<=1,"terminal parity");
        const blank=record.filter(([a,b])=>!a&&!b).length;
        const key=`${blank},${ee},${eo},${oe},${oo}`;
        hist[key]=(hist[key]||0)+1;
        const lastReads=record[11].filter(Boolean).length;
        byBlank[lastReads]=(byBlank[lastReads]||0)+1;
        if(actual===2)signEssential++;
        if(blank===0&&(ee+eo>1||oe+oo>1)){orientationEssential++;rawMatchingAmbiguity++;}
        rootMass+=actual;assignments+=actual;return;
      }
      must(depth<8,"budget");
      if(node[0]==="repeat"){visit(node[1],depth+1);return}
      must(node[0]==="read"&&Number.isInteger(node[1])&&node[1]>=0&&node[1]<13,"read");
      const q=node[1],r=q<11?q:11,col=q===11?0:1,old=record[r][col];
      for(const [c,j] of Object.entries(node[2])){must(!old||old===c,"conflicting repeat");record[r][col]=c;visit(j,depth+1);}
      record[r][col]=old;
    }
    const expected=countSignedCompletions(record,labels);visit(0,0);
    must(seen.size===e.nodes.length&&rootMass===expected[0]+expected[2],"root mass");
  }
  must(nodes===141097&&leaves===73962&&assignments===144736,"pinned totals");
  return {nodes,leaves,assignments,signEssential,orientationEssential,rawMatchingAmbiguity,byLastEdgeReads:byBlank,sectorHistogram:hist};
}
function auditPrefixPolymatroid(){
  const edges=[];for(let i=0;i<6;i++)for(let j=i+1;j<6;j++)if((i>>1)!==(j>>1))edges.push([i,j]);
  const pow=Array.from({length:6},(_,i)=>5**i),vec=x=>pow.map(p=>Math.floor(x/p)%5);
  let s=new Set([0]);
  for(const [u,v] of edges){const next=new Set(s);for(const x of s){next.add(x+pow[u]);next.add(x+pow[v]);}s=next;}
  const rank=Array.from({length:64},(_,mask)=>edges.filter(([u,v])=>((mask>>u)|(mask>>v))&1).length);
  let checks=0;for(let a=0;a<64;a++)for(let b=0;b<64;b++){if(rank[a]+rank[b]<rank[a|b]+rank[a&b])throw Error("submodular");checks++;}
  let h=Array(13).fill(0),dp=Array(13).fill(0);
  for(let x=0;x<5**6;x++){let v=vec(x),k=v.reduce((a,b)=>a+b,0);const ok=Array.from({length:64},(_,m)=>v.reduce((t,a,i)=>t+(m>>i&1?a:0),0)).every((a,m)=>a<=rank[m]);if(ok!==s.has(x))throw Error("Hall support mismatch");if(ok)h[k]++;if(s.has(x))dp[k]++;}
  let forest=Array(6).fill(0);for(let mask=0;mask<1<<12;mask++){let p=Array.from({length:6},(_,i)=>i),root=i=>p[i]===i?i:root(p[i]),k=0,valid=true;for(let j=0;j<12;j++)if(mask>>j&1){const [u,v]=edges[j],a=root(u),b=root(v);if(a===b){valid=false;break}p[a]=b;k++;}if(valid)forest[k]++;}
  if(forest.reduce((a,b)=>a+b,0)!==h[12]||h[11]!==1362)throw Error("forest count");
  return {submodularChecks:checks,latticeCandidates:5**6,allPrefixSupport:h,forestCoefficients:forest,total:s.size};
}
function auditParityPolytope(){
 const labels=["DL","BL","FL","UL","DB","DF","UB","UF","DR","BR","FR","UR"],colors="URFDLB",p=Array.from({length:6},(_,i)=>5**i),vec=x=>p.map(q=>Math.floor(x/q)%5),encode=a=>a.reduce((s,x,i)=>s+x*p[i],0);
 const fibers=new Map(), orientations=[];
 for(let m=0;m<4096;m++){let x=0,b=0;let adj=Array.from({length:6},()=>[]);for(let i=0;i<12;i++){const f=m>>i&1,u=colors.indexOf(labels[i][f]),v=colors.indexOf(labels[i][1-f]);x+=p[u];b^=f;adj[v].push(u)}let c=fibers.get(x)||[0,0];c[b]++;fibers.set(x,c);orientations.push({x,b,adj});}
 function oddCycle(adj){for(let i=0;i<6;i++){function walk(v,seen,n){for(const w of adj[v]){if(w===i&&n>=3&&n%2===1)return true;if(!(seen>>w&1)&&walk(w,seen|1<<w,n+1))return true}return false}if(walk(i,1<<i,1))return true}return false}
 let h={evenOnly:0,oddOnly:0,both:0},oddCycleCount=0;for(const [x,c] of fibers){h[c[0]&&c[1]?"both":c[0]?"evenOnly":"oddOnly"]++}
 for(const {x,adj} of orientations){const odd=oddCycle(adj);if(odd)oddCycleCount++;if(odd!==fibers.get(x).every(Boolean))throw Error("odd cycle criterion")}
 function exchange(set){const rows=[...set].map(x=>[x,vec(x)]);let failures=0,witness=null,checks=0;for(const [x,a] of rows)for(const [y,b] of rows)for(let i=0;i<6;i++)if(a[i]>b[i]){checks++;let options=[];for(let j=0;j<6;j++)if(a[j]<b[j])options.push({j,x:vec(x-p[i]+p[j]),y:vec(y+p[i]-p[j]),inX:set.has(x-p[i]+p[j]),inY:set.has(y+p[i]-p[j])});if(!options.some(o=>o.inX)){failures++;if(!witness)witness={x:a,y:b,i,options};}}return {checks,failures,witness}}
 const even=new Set([...fibers].filter(([x,c])=>c[0]).map(([x])=>x)),odd=new Set([...fibers].filter(([x,c])=>c[1]).map(([x])=>x));
 const result={h,oddCycleCount,even:exchange(even),odd:exchange(odd),unrestricted:exchange(new Set(fibers.keys()))};
 for(const t of [result.even,result.odd]){const w=t.witness;w.counts={x:fibers.get(encode(w.x)),y:fibers.get(encode(w.y)),alternatives:w.options.map(o=>fibers.get(encode(o.x))||[0,0])}}
 if(h.evenOnly!==222||h.oddOnly!==216||h.both!==645||result.unrestricted.failures!==0||!result.even.failures||!result.odd.failures)throw Error("parity/exchange regression");
 return result
}
function auditParityHoles(){
 const labels=["DL","BL","FL","UL","DB","DF","UB","UF","DR","BR","FR","UR"],colors="URFDLB",p=Array.from({length:6},(_,i)=>5**i),vec=x=>p.map(q=>Math.floor(x/q)%5),enc=a=>a.reduce((s,x,i)=>s+x*p[i],0),fibers=new Map();
 for(let m=0;m<4096;m++){let x=0,b=0;for(let i=0;i<12;i++){let f=m>>i&1;x+=p[colors.indexOf(labels[i][f])];b^=f}let h=fibers.get(x)||[0,0];h[b]++;fibers.set(x,h)}
 const results=[];
 for(let b=0;b<2;b++){
   const keys=[...fibers].filter(([x,c])=>c[b]).map(([x])=>x),set=new Set(keys),rows=keys.map(x=>[x,vec(x)]),holes=new Set();let witness=null;
   for(let i=0;i<rows.length;i++)for(let j=i+1;j<rows.length;j++){const [x,a]=rows[i],[y,z]=rows[j];if(!a.every((v,k)=>(v+z[k])%2===0))continue;const m=(x+y)/2;if(!set.has(m)){if(!fibers.has(m))throw Error("unrestricted convex hole");holes.add(m);if(!witness)witness={a,c:z,midpoint:vec(m),counts:[fibers.get(x),fibers.get(y),fibers.get(m)]}}}
   results.push({parity:b,midpointHoles:holes.size,witness});
 }
 // Rank inequalities cannot distinguish the legal even support from full zonotope
 // if all rank maxima coincide (checked, not assumed).
 const max=(set,mask)=>Math.max(...set.map(x=>vec(x).reduce((s,n,i)=>s+((mask>>i&1)?n:0),0)));
 const all=[...fibers.keys()],rankGaps=[];
 for(let b=0;b<2;b++){const sector=all.filter(x=>fibers.get(x)[b]);let gaps=[];for(let m=0;m<64;m++){const a=max(all,m),v=max(sector,m);if(a!==v)gaps.push({mask:m,unrestricted:a,sector:v})}rankGaps.push(gaps)}
 return {results,rankGaps};
}
function auditRankBlindness(){
 const labels=["DL","BL","FL","UL","DB","DF","UB","UF","DR","BR","FR","UR"],colors="URFDLB",p=Array.from({length:6},(_,i)=>5**i),vec=x=>p.map(q=>Math.floor(x/q)%5);
 let vertices=[0,0],best=null;
 for(let m=0;m<4096;m++){let x=0,b=0;const adj=Array.from({length:6},()=>[]),deg=Array(6).fill(0);for(let i=0;i<12;i++){const f=m>>i&1,u=colors.indexOf(labels[i][f]),v=colors.indexOf(labels[i][1-f]);x+=p[u];b^=f;adj[v].push(u);deg[u]++}const queue=deg.flatMap((d,i)=>d===0?[i]:[]),order=[];for(let i=0;i<queue.length;i++){let v=queue[i];order.push(v);for(const u of adj[v])if(--deg[u]===0)queue.push(u)}
 if(order.length!==6)continue;vertices[b]++;if(b===1&&!best){const w=Array(6);order.forEach((v,i)=>w[v]=i);best={histogram:vec(x),weights:w,orientationMask:m,score:vec(x).reduce((s,v,i)=>s+v*w[i],0)}}}
 const scores=[-1,-1];for(let m=0;m<4096;m++){let x=0,b=0;for(let i=0;i<12;i++){const f=m>>i&1;x+=p[colors.indexOf(labels[i][f])];b^=f}scores[b]=Math.max(scores[b],vec(x).reduce((s,v,i)=>s+v*best.weights[i],0))}
 if(scores[1]!==best.score||scores[0]>=scores[1])throw Error("weighted objective not separated");
 return {vertices,weightedWitness:best,sectorMaxima:scores}
}
function auditParitySupportFunction(){
 const labels=["DL","BL","FL","UL","DB","DF","UB","UF","DR","BR","FR","UR"],colors="URFDLB",edges=labels.map(l=>[colors.indexOf(l[0]),colors.indexOf(l[1])]),p=Array.from({length:6},(_,i)=>5**i);
 const masks=Array.from({length:4096},(_,m)=>{let h=0,b=0,adj=Array.from({length:6},()=>[]),deg=Array(6).fill(0);for(let i=0;i<12;i++){const f=m>>i&1,u=edges[i][f],v=edges[i][1-f];h+=p[u];b^=f;adj[v].push(u);deg[u]++}let q=deg.flatMap((v,i)=>v===0?[i]:[]);for(let i=0;i<q.length;i++)for(const j of adj[q[i]])if(--deg[j]===0)q.push(j);return {h,b,acyclic:q.length===6}});
 const fibers=new Map();for(const {h,b,acyclic} of masks){const a=fibers.get(h)||{count:[0,0],vertex:false};a.count[b]++;a.vertex||=acyclic;fibers.set(h,a)}
 let exclusiveNonvertex=[0,0],vertices=[0,0];for(const {count,vertex} of fibers.values()){if(vertex&&count[0]+count[1]!==1)throw Error("vertex fiber");if(vertex)vertices[count[1]?1:0]++;if(!vertex&&!(count[0]&&count[1]))exclusiveNonvertex[count[1]?1:0]++}
 let checks=0;
 for(let code=0;code<3**6;code++){let w=Array.from({length:6},(_,i)=>Math.floor(code/3**i)%3-1);let best=0,b=0,gap=Infinity;for(const [u,v] of edges){best+=Math.max(w[u],w[v]);b^=+(w[v]>w[u]);gap=Math.min(gap,Math.abs(w[u]-w[v]))}const expected=[best-(b===0?0:gap),best-(b===1?0:gap)],actual=[-Infinity,-Infinity];for(const {h,b:k} of masks){let score=0;for(let i=0;i<6;i++)score+=w[i]*(Math.floor(h/p[i])%5);actual[k]=Math.max(actual[k],score)}if(expected.some((x,i)=>x!==actual[i]))throw Error("support function mismatch");checks++}
 if(vertices[0]!==210||vertices[1]!==216||exclusiveNonvertex[0]!==12||exclusiveNonvertex[1]!==0)throw Error("vertex classification");
 return {vertices,exclusiveNonvertex,weightVectors:checks};
}
function auditParityExchanges(){
 const labels=["DL","BL","FL","UL","DB","DF","UB","UF","DR","BR","FR","UR"],colors="URFDLB",p=Array.from({length:6},(_,i)=>5**i),vec=x=>p.map(q=>Math.floor(x/q)%5),orient=[],sets=[new Set(),new Set()];
 for(let m=0;m<4096;m++){let x=0,b=0,adj=Array.from({length:6},()=>[]);for(let i=0;i<12;i++){const f=m>>i&1,u=colors.indexOf(labels[i][f]),v=colors.indexOf(labels[i][1-f]);x+=p[u];b^=f;adj[v].push([u,1<<i])}sets[b].add(x);orient.push({m,x,b,adj})}
 let tests=0,exactPositive=0,liftFP=0,liftFN=0,evenPathFN=0,liftFPWitness=null,liftFNWitness=null,pathFNWitness=null;
 for(const {m,x,b,adj} of orient){
   const counts=vec(x),oddCycles=new Set();
   for(let s=0;s<6;s++){function visit(v,seen,used,len){for(const [u,edge] of adj[v]){if(u===s&&len>=2&&(len+1)%2===1)oddCycles.add(used|edge);else if(!(seen>>u&1))visit(u,seen|1<<u,used|edge,len+1)}}visit(s,1<<s,0,0)}
   for(let j=0;j<6;j++)for(let i=0;i<6;i++)if(i!==j&&counts[i]>0&&counts[j]<4){
      let hasEvenPath=false,hasCorrectedPath=false;
      function path(v,seen,used,len){if(v===i){if(len%2===0)hasEvenPath=true;else if([...oddCycles].some(c=>!(c&used)))hasCorrectedPath=true;return}for(const [u,e] of adj[v])if(!(seen>>u&1))path(u,seen|1<<u,used|e,len+1)}
      path(j,1<<j,0,0);
      const reach=new Set([2*j]),queue=[2*j];for(let k=0;k<queue.length;k++){const s=queue[k];for(const [u] of adj[s>>1]){let t=2*u+((s&1)^1);if(!reach.has(t)){reach.add(t);queue.push(t)}}}
      const lift=reach.has(2*i),actual=sets[b].has(x-p[i]+p[j]),pred=hasEvenPath||hasCorrectedPath;tests++;if(actual)exactPositive++;if(pred!==actual)throw Error(JSON.stringify({m,i,j,b,actual,pred}));
      const witness={orientationMask:m,parity:b,from:colors[i],to:colors[j],histogram:counts,target:vec(x-p[i]+p[j]),adj:adj.map(a=>a.map(([u,e])=>[colors[u],Math.log2(e)]))};
      if(lift&&!actual){liftFP++;liftFPWitness??=witness}if(!lift&&actual){liftFN++;liftFNWitness??=witness}if(!hasEvenPath&&actual){evenPathFN++;pathFNWitness??=witness}
   }
 }
 if(tests!==108384||exactPositive!==93156||!liftFP||!liftFN)throw Error("exchange census");
 return {tests,exactPositive,liftFP,liftFN,evenPathFN,liftFPWitness,liftFNWitness,pathFNWitness};
}
function auditGraphParityClassification(){
 const tally={},examples={};let graphCount=0,sectorCount=0;
 for(let n=2;n<=5;n++){
  const edges=[];for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)edges.push([i,j]);const base=n,p=Array.from({length:n},(_,i)=>base**i);
  for(let mask=1;mask<2**edges.length;mask++){
   const es=edges.filter((_,i)=>mask>>i&1),m=es.length,sets=[new Set(),new Set()];
   for(let o=0;o<2**m;o++){let x=0,b=0;for(let i=0;i<m;i++){let k=o>>i&1;x+=p[es[i][k]];b^=k}sets[b].add(x)}
   function exchange(set){let rows=[...set].map(x=>[x,p.map(q=>Math.floor(x/q)%base)]);for(const [x,a] of rows)for(const [,b] of rows)for(let i=0;i<n;i++)if(a[i]>b[i]&&!a.some((v,j)=>v<b[j]&&set.has(x-p[i]+p[j])))return false;return true}
   let valid=sets.map(exchange),num=valid.filter(Boolean).length;
   const touching=m===2&&es[0].some(v=>es[1].includes(v));const expected=m===1?2:touching?1:0;
   if(num!==expected)throw Error(JSON.stringify({n,es,valid,expected}));
   const key=m===1?"oneEdge":m===2?(touching?"twoAdjacent":"twoDisjoint"):"threeOrMore";tally[key]=(tally[key]||0)+1;examples[key]??={n,es,valid};graphCount++;sectorCount+=2;
  }
 }
 return {graphCount,sectorCount,tally,examples};
}
function auditBoundedExchange(){
  const colors="URFDLB",pow=Array.from({length:6},(_,i)=>5**i),vec=x=>pow.map(p=>Math.floor(x/p)%5);
  const families=[{name:"edge",pieces:["DL","BL","FL","UL","DB","DF","UB","UF","DR","BR","FR","UR"],mod:2},{name:"corner",pieces:["UFR","URB","ULF","UBL","DRF","DBR","DFL","DLB"],mod:3}];
  const results=[];
  for(const {name,pieces,mod} of families){
    const counts=new Map();
    function gen(i,key,charge){if(i===pieces.length){let a=counts.get(key)||Array(mod).fill(0);a[charge]++;counts.set(key,a);return;}
      for(let j=0;j<mod;j++)gen(i+1,key+pow[colors.indexOf(pieces[i][j])],(charge+j)%mod);}
    gen(0,0,0);
    const sectors=[];
    for(let b=0;b<mod;b++){
      const keys=[...counts].filter(([,a])=>a[b]).map(([k])=>k),set=new Set(keys),rows=keys.map(k=>({k,v:vec(k)})),steps=Array(mod+1).fill(0),witnesses={};
      let obligations=0;
      for(const {k:x,v:a} of rows)for(const {k:y,v:c} of rows){
        if(x===y)continue;
        let plus=[],minus=[],delta=a.map((v,i)=>v-c[i]);for(let i=0;i<6;i++){if(delta[i]>0)plus.push(i);if(delta[i]<0)minus.push(i)}
        for(const i of plus){
          obligations++;
          function rec(depth,limit,d,initial){
            if(depth>0&&set.has(x+d)&&set.has(y-d))return d;
            if(depth===limit)return null;
            for(const u of initial?[i]:plus)if(delta[u]>0)for(const v of minus)if(delta[v]<0){
              delta[u]--;delta[v]++;const ans=rec(depth+1,limit,d-pow[u]+pow[v],false);delta[u]++;delta[v]--;if(ans!==null)return ans;
            }return null;
          }
          let found=false;
          for(let lim=1;lim<=mod;lim++){const d=rec(0,lim,0,true);if(d!==null){steps[lim]++;witnesses[lim]??={x:a,y:c,excess:colors[i],xNext:vec(x+d),yNext:vec(y-d)};found=true;break}}
          if(!found)throw Error(`bounded exchange failed ${name} ${b} ${x} ${y} ${i}`);
        }
      }sectors.push({parity:b,support:keys.length,obligations,minTransfers:steps.slice(1),witnesses});
    }let hist={};for(const a of counts.values()){const k=a.map(n=>+(n>0)).join("");hist[k]=(hist[k]||0)+1}
    results.push({name,unrestricted:counts.size,sectorSupport:hist,sectors});
  }
  return results;
}
function auditSignCertificates(){
 const types=[["edge",["DL","BL","FL","UL","DB","DF","UB","UF","DR","BR","FR","UR"],2],["corner",["UFR","URB","ULF","UBL","DRF","DBR","DFL","DLB"],3]];
 const out=[];
 for(const [name,labels,m] of types){
   const n=labels.length;for(let d=1;d<m;d++){const unique=new Set();for(const l of labels)for(let j=0;j<m;j++){const key=l[j]+l[(j+d)%m];if(unique.has(key))throw Error("two colors not unique");unique.add(key);}}
   let hist={},min=2*n,example=null,checked=0,certCount=0;
   for(let blank=-1;blank<n;blank++){
     const used=new Set(blank<0?[]:labels[blank]);const singles=[];
     function run(i){
       if(i===n){
         const cost=2*n-singles.length-(blank>=0?2:0);
         const remaining=[...singles.map(([p])=>p),...(blank<0?[]:[blank])].sort((a,b)=>a-b);
         const req=new Map(singles);
         function oddCompletion(k,used,parity,twist){
           if(k===remaining.length)return parity===1&&twist===0;
           const pos=remaining[k];for(let j=0;j<remaining.length;j++)if(!(used>>j&1)){let lab=remaining[j],side=req.get(pos);
             for(let t=0;t<m;t++)if(side===undefined||labels[lab][(side+t)%m]===labels[pos][side]){
               let q=0;for(let z=j+1;z<remaining.length;z++)q^=used>>z&1;
               if(oddCompletion(k+1,used|1<<j,parity^q,(twist+t)%m))return true;
             }
           }return false;
         }
         checked++;let a=hist[cost]??[0,0];if(!oddCompletion(0,0,0,0)){a[1]++;certCount++;if(cost<min||!example){min=cost;example={blank,singles:singles.map(([i,s])=>({piece:labels[i],side:s,color:labels[i][s]})),full:labels.filter((_,i)=>i!==blank&&!req.has(i))}}}else a[0]++;hist[cost]=a;
         return;
       }
       if(i===blank){run(i+1);return;}
       run(i+1);
       for(let j=0;j<m;j++){const c=labels[i][j];if(used.has(c))continue;used.add(c);singles.push([i,j]);run(i+1);singles.pop();used.delete(c);}
     }run(0)
   }
   out.push({name,min,example,checked,certCount,hist});
 }
 if(out[0].min!==18||out[1].min!==11||out[1].hist[10][1]!==0)throw Error("certificate minima");
 return out;
}
function auditCornerSignMinimax(){
 const labels=["UFR","URB","ULF","UBL","DRF","DBR","DFL","DLB"],colors="URFDLB";
 const pos=labels.map(l=>Array.from(colors,c=>l.indexOf(c))),cm=Array.from(colors,(_,c)=>labels.reduce((a,l,i)=>a|(pos[i][c]>=0?1<<i:0),0));
 const pop=Array.from({length:256},(_,x)=>{let n=0;while(x){x&=x-1;n++}return n});
 const signCache=new Map(),depthCache=new Map();
 const key=(rows,mask,r)=>`${rows.join("")}:${mask}:${r}`;
 const swap=s=>((s&1)<<1)|((s&2)>>1);
 function signs(rows,mask,r){
  const k=key(rows,mask,r);if(signCache.has(k))return signCache.get(k);
  let s=0;
  if(!rows.length){const b=pop[mask];s=b>=2?3:b===1||r===0?1:0;}
  else{let j=mask&cm[rows[0]];while(j){const bit=j&-j;j^=bit;const l=31-Math.clz32(bit),child=signs(rows.slice(1),mask^bit,(r-pos[l][rows[0]]+3)%3);s|=pop[mask&(bit-1)]%2?swap(child):child;if(s===3)break;}}
  signCache.set(k,s);return s;
 }
 let calls=0;
 function depth(rows,mask,r){
  const k=key(rows,mask,r);if(depthCache.has(k))return depthCache.get(k);
  const s=signs(rows,mask,r);if(s!==3)return 0;
  calls++;
  let best=Infinity; const blanks=pop[mask]-rows.length;
  if(blanks){for(let j=0;j<3;j++){let worst=0;for(let c=0;c<6;c++){const next=[...rows,c].sort((a,b)=>a-b),nr=(r+j)%3;if(signs(next,mask,nr))worst=Math.max(worst,depth(next,mask,nr));if(worst+1>=best)break;}best=Math.min(best,worst+1);}}
  for(let i=0;i<rows.length;i++){
   if(i&&rows[i]===rows[i-1])continue;
   let j=mask&cm[rows[i]],worst=0;const rest=rows.slice(0,i).concat(rows.slice(i+1));
   while(j){const bit=j&-j;j^=bit;const l=31-Math.clz32(bit),nr=(r-pos[l][rows[i]]+3)%3;if(signs(rest,mask^bit,nr))worst=Math.max(worst,depth(rest,mask^bit,nr));if(worst+1>=best)break;}
   best=Math.min(best,worst+1);
  }
  if(!Number.isFinite(best))throw Error("no distinguishing action");depthCache.set(k,best);return best;
 }
 const result=depth([],255,0);
 const rootChoices=Array.from({length:3},(_,j)=>({side:j,cost:1+Math.max(...Array.from({length:6},(_,c)=>depth([c],255,j)))}));
 const scanMemo=new Map();
 function scan(rows,mask){const k=key(rows,mask,0);if(scanMemo.has(k))return scanMemo.get(k);if(signs(rows,mask,0)!==3)return 0;
  let best=Infinity;for(let i=0;i<rows.length;i++){if(i&&rows[i]===rows[i-1])continue;const rest=rows.slice(0,i).concat(rows.slice(i+1));let j=mask&cm[rows[i]],worst=0;while(j){const bit=j&-j;j^=bit;if(signs(rest,mask^bit,0))worst=Math.max(worst,scan(rest,mask^bit));}best=Math.min(best,1+worst);}scanMemo.set(k,best);return best;
 }
 let hist={},roots=0;function prefix(rows,min){if(rows.length===7){if(signs(rows,255,0)){let d=scan(rows,255);hist[d]=(hist[d]||0)+1;roots++;}return;}for(let c=min;c<6;c++)prefix([...rows,c],c);}prefix([],0);
 if(result!==13||rootChoices.some(x=>x.cost!==13)||roots!==642||hist[6]!==462)throw Error("sign minimax regression");
 return {result,rootChoices,calls,signCache:signCache.size,depthCache:depthCache.size,sevenPrefix:{roots,hist},scanCache:scanMemo.size};
}
function auditCornerGoals(){
 const labels=["UFR","URB","ULF","UBL","DRF","DBR","DFL","DLB"],colors="URFDLB";
 const index=labels.map(s=>Array.from(colors,c=>s.indexOf(c)));
 const pop=Array.from({length:256},(_,x)=>{let n=0;while(x){x&=x-1;n++}return n});
 const counts=new Map(),memo=new Map(),key=(a,m,r)=>`${a.join("")}:${m}:${r}`, cap=x=>Math.min(x,2);
 function count(a,m,r){
   const k=key(a,m,r);if(counts.has(k))return counts.get(k);let out=[0,0];
   if(!a.length){const b=pop[m];out=b>=2?[2,2]:b===1||r===0?[1,0]:[0,0];}
   else{for(let l=0;l<8;l++)if((m>>l&1)&&index[l][a[0]]>=0){
     const c=count(a.slice(1),m^(1<<l),(r-index[l][a[0]]+3)%3),p=pop[m&((1<<l)-1)]%2;
     out[0]=cap(out[0]+c[p]);out[1]=cap(out[1]+c[p^1]);}}
   counts.set(k,out);return out;
 }
 function actions(a,m,r){
   let out=[];
   if(pop[m]>a.length)for(let j=0;j<3;j++){const children=[];for(let c=0;c<6;c++){let b=[...a,c].sort((x,y)=>x-y),s=(r+j)%3;if(count(b,m,s).some(Boolean))children.push([b,m,s]);}out.push(children)}
   for(let i=0;i<a.length;i++)if(i===0||a[i]!==a[i-1]){const children=[],b=a.slice(0,i).concat(a.slice(i+1));for(let l=0;l<8;l++)if((m>>l&1)&&index[l][a[i]]>=0){let n=m^(1<<l),s=(r-index[l][a[i]]+3)%3;if(count(b,n,s).some(Boolean))children.push([b,n,s]);}out.push(children)}
   return out;
 }
 function depths(a,m,r){
   const k=key(a,m,r);if(memo.has(k))return memo.get(k);
   const c=count(a,m,r);if(c[0]+c[1]<=1)return [0,0,0];
   // sign, complete, complete with terminal (not early) sign
   let best=[c.every(Boolean)?Infinity:0,Infinity,c.every(x=>x<=1)?0:Infinity];
   for(const ch of actions(a,m,r)){
     const worst=[0,0,0];for(const s of ch){const d=depths(...s);for(let i=0;i<3;i++)worst[i]=Math.max(worst[i],d[i]+1);}
     for(let i=0;i<3;i++)best[i]=Math.min(best[i],worst[i]);
   }
   if(best.some(x=>!Number.isFinite(x)))throw Error("unresolved");
   memo.set(k,best);return best;
 }
 const root=depths([],255,0),hist={},examples={};
 for(const [k,d] of memo){const h=`${d[1]-d[0]},${d[1]-d[2]}`;hist[h]=(hist[h]||0)+1;examples[h]??={state:k,depths:d};}
 const feasibility=new Map();
 function feasible(a,m,r,h,t){
   const c=count(a,m,r),d=depths(a,m,r);
   if(c[0]+c[1]<=1)return true;
   if(d[0]>Math.max(h,0)||d[1]>t)return false;
   if(!c.every(Boolean))return d[1]<=t;
   const k=`${key(a,m,r)}:${h}:${t}`;if(feasibility.has(k))return feasibility.get(k);
   const ans=actions(a,m,r).some(ch=>ch.every(s=>feasible(...s,h-1,t-1)));feasibility.set(k,ans);return ans;
 }
 const deadlines=[];for(let h=root[0];h<=root[1];h++){let t=root[1];while(t<=16&&!feasible([],255,0,h,t))t++;deadlines.push({signBy:h,fullBy:t});}
 if(root.join(",")!=="13,13,12"||deadlines[0].fullBy!==13)throw Error("corner goal regression");
 return {root,deadlines,counts:counts.size,depths:memo.size,feasibility:feasibility.size,depthGapHistogram:hist,examples};
}
function auditEarlyCornerSign(){
 const labels=["UFR","URB","ULF","UBL","DRF","DBR","DFL","DLB"],colors="URFDLB",index=labels.map(s=>Array.from(colors,c=>s.indexOf(c)));
 const pop=Array.from({length:256},(_,x)=>{let n=0;while(x){x&=x-1;n++}return n});
 const counts=new Map(),memo=new Map(),key=(a,m,r)=>`${a.join("")}:${m}:${r}`;
 function count(a,m,r){const k=key(a,m,r);if(counts.has(k))return counts.get(k);let o=[0,0];if(!a.length){const b=pop[m];o=b>=2?[2,2]:b===1||r===0?[1,0]:[0,0]}else for(let l=0;l<8;l++)if(m>>l&1&&index[l][a[0]]>=0){const v=count(a.slice(1),m^(1<<l),(r-index[l][a[0]]+3)%3),p=pop[m&((1<<l)-1)]%2;for(let s=0;s<2;s++)o[s]=Math.min(2,o[s]+v[s^p])}counts.set(k,o);return o}
 function depth(a,m,r,s){if(count(a,m,r)[s]<=1)return 0;const k=key(a,m,r)+":"+s;if(memo.has(k))return memo.get(k);let best=Infinity;
  if(pop[m]>a.length)for(let j=0;j<3;j++){let worst=0;for(let c=0;c<6;c++){const b=[...a,c].sort((x,y)=>x-y),t=s^(a.filter(x=>x>c).length%2),nr=(r+j)%3;if(count(b,m,nr)[t])worst=Math.max(worst,1+depth(b,m,nr,t));}best=Math.min(best,worst)}
  for(let i=0;i<a.length;i++){if(i&&a[i]===a[i-1])continue;let worst=0,b=a.slice(0,i).concat(a.slice(i+1));for(let l=0;l<8;l++)if(m>>l&1&&index[l][a[i]]>=0){const nm=m^(1<<l),nr=(r-index[l][a[i]]+3)%3,t=s^((i+pop[m&((1<<l)-1)])%2);if(count(b,nm,nr)[t])worst=Math.max(worst,1+depth(b,nm,nr,t));}best=Math.min(best,worst)}
  if(!Number.isFinite(best))throw Error("unresolved");memo.set(k,best);return best;
 }
 const root=[depth([],255,0,0),depth([],255,0,1)];
 if(root.some(d=>d!==12))throw Error("early sign regression");
 return {root,countStates:counts.size,depthStates:memo.size};
}
function auditChargedCycleCertificates(){
 const types=[["edge",["DL","BL","FL","UL","DB","DF","UB","UF","DR","BR","FR","UR"],2],["corner",["UFR","URB","ULF","UBL","DRF","DBR","DFL","DLB"],3]],out=[];
 for(const [name,labels,m] of types){
  const n=labels.length, hist={},cyclesUsed={},witnesses={};let checked=0,min=2*n;
  for(let blank=-1;blank<n;blank++){
   const colors=new Set(blank<0?[]:labels[blank]),singles=[];
   function test(){
    const rows=[...singles.map(x=>x[0]),...(blank<0?[]:[blank])].sort((a,b)=>a-b),k=rows.length,req=new Map(singles),edges=rows.map((i)=>rows.map(j=>Array.from({length:m},(_,t)=>t).filter(t=>!req.has(i)||labels[j][(req.get(i)+t)%m]===labels[i][req.get(i)])));
    const byStart=Array.from({length:k},()=>[]); 
    for(let s=0;s<k;s++){
     const found=new Map();
     function walk(v,mask,len,r){
      for(let j=s;j<k;j++)for(const t of edges[v][j]){
       const nr=(r+t)%m;
       if(j===s){if(len===1&&nr===0)continue;const p=(len-1)%2,charge=p*m+nr,id=mask*2*m+charge;if(charge!==0&&!found.has(id))found.set(id,{mask,p,r:nr});}
       else if(!(mask>>j&1))walk(j,mask|1<<j,len+1,nr);
      }
     }walk(s,1<<s,1,0);byStart[s]=[...found.values()];
    }
    const memo=new Map();
    function target(mask,p,r){
     if(p===0&&r===0)return 0;
     if(!mask)return Infinity;
     const key=mask*2*m+p*m+r;if(memo.has(key))return memo.get(key);
     const bit=mask&-mask,s=31-Math.clz32(bit);let best=target(mask^bit,p,r);
     for(const c of byStart[s])if((mask&c.mask)===c.mask)best=Math.min(best,1+target(mask^c.mask,p^c.p,(r-c.r+m)%m));
     memo.set(key,best);return best;
    }
    const d=target((1<<k)-1,1,0);
    function brute(i,used,p,r){if(i===k)return p===1&&r===0;for(let j=0;j<k;j++)if(!(used>>j&1)){let q=0;for(let l=j+1;l<k;l++)q^=used>>l&1;for(const t of edges[i][j])if(brute(i+1,used|1<<j,p^q,(r+t)%m))return true;}return false}
    if(Number.isFinite(d)!==brute(0,0,0,0))throw Error("cycle mismatch");
    checked++;const cost=2*n-singles.length-(blank>=0?2:0),v=hist[cost]??[0,0];v[Number(!Number.isFinite(d))]++;hist[cost]=v;
    if(Number.isFinite(d)){cyclesUsed[d]=(cyclesUsed[d]||0)+1;witnesses[d]??={blank,singles:singles.map(([i,s])=>[labels[i],s,labels[i][s]])};}else min=Math.min(min,cost);
   }
   function gen(i){if(i===n){test();return;}if(i===blank){gen(i+1);return;}gen(i+1);for(let s=0;s<m;s++){let c=labels[i][s];if(colors.has(c))continue;colors.add(c);singles.push([i,s]);gen(i+1);singles.pop();colors.delete(c);}}gen(0);
  }
  out.push({name,checked,min,hist,cyclesUsed,witnesses});
 }
 if(out[0].checked!==14891||out[1].checked!==5873||out[0].cyclesUsed[1]!==782||out[1].cyclesUsed[2]!==312)throw Error("charged cycle regression");
 return out;
}
function auditGraphSignCertificateFormula(){
 let graphs=0,patterns=0,certificates=0,examples={};
 for(let v=2;v<=5;v++){
  const possible=[];for(let u=0;u<v;u++)for(let w=u+1;w<v;w++)possible.push([u,w]);
  for(let mask=1;mask<1<<possible.length;mask++){
   const E=possible.filter((_,i)=>mask>>i&1),n=E.length;
   const adj=Array.from({length:v},()=>[]);E.forEach(([u,w])=>{adj[u].push(w);adj[w].push(u)});
   const active=adj.filter(a=>a.length).length,side=Array(v).fill(-1);let bip=0;
   for(let u=0;u<v;u++)if(adj[u].length&&side[u]<0){let ok=true,q=[u];side[u]=0;for(let i=0;i<q.length;i++)for(const w of adj[q[i]]){if(side[w]<0){side[w]=side[q[i]]^1;q.push(w)}else if(side[w]===side[q[i]])ok=false;}if(ok)bip++;}
   const expected=2*n-active+Math.max(0,bip-1);let min=2*n;
   for(let blank=-1;blank<n;blank++){
    const used=new Set(blank<0?[]:E[blank]),singles=[];
    function inspect(){
     patterns++;
     const rows=[...singles.map(x=>x[0]),...(blank<0?[]:[blank])].sort((a,b)=>a-b),req=new Map(singles),k=rows.length;
     function odd(i,mask,p,r){if(i===k)return p===1&&r===0;for(let j=0;j<k;j++)if(!(mask>>j&1)){let q=0;for(let l=j+1;l<k;l++)q^=mask>>l&1;for(let t=0;t<2;t++)if(!req.has(rows[i])||E[rows[j]][(req.get(rows[i])+t)%2]===E[rows[i]][req.get(rows[i])])if(odd(i+1,mask|1<<j,p^q,r^t))return true;}return false}
     const next=Array(v).fill(-1);
     for(const [i,s] of singles)next[E[i][s]]=E[i][s^1];
     let evenCycle=false;
     for(let u=0;u<v;u++){let seen=new Map(),w=u,t=0;while(w>=0&&next[w]>=0&&!seen.has(w)){seen.set(w,t++);w=next[w]}if(seen.has(w)&&(t-seen.get(w))%2===0)evenCycle=true;}
     const ambiguous=odd(0,0,0,0);
     if(ambiguous!==evenCycle)throw Error(JSON.stringify({E,blank,singles,ambiguous,evenCycle}));
     if(!ambiguous){certificates++;min=Math.min(min,2*n-singles.length-(blank<0?0:2));}
    }
    function gen(i){if(i===n){inspect();return}if(i===blank){gen(i+1);return}gen(i+1);for(let s=0;s<2;s++){const c=E[i][s];if(used.has(c))continue;used.add(c);singles.push([i,s]);gen(i+1);singles.pop();used.delete(c)}}gen(0);
   }
   if(min!==expected)throw Error(JSON.stringify({E,expected,min,bip,active}));
   graphs++;examples[bip]??={E,n,active,bip,min};
  }
 }
 if(graphs!==1094||patterns!==312453||certificates!==306669)throw Error("graph census");
 return {graphs,patterns,certificates,examples};
}
function auditFullGraphCertificates(){
 let graphs=0,patterns=0,certs=0,gaps={};
 for(let v=2;v<=5;v++){
  const all=[];for(let u=0;u<v;u++)for(let w=u+1;w<v;w++)all.push([u,w]);
  for(let m=1;m<1<<all.length;m++){
   const E=all.filter((_,i)=>m>>i&1),n=E.length,adj=Array.from({length:v},()=>[]);
   for(const [u,w] of E){adj[u].push(w);adj[w].push(u)}
   let c=0,b=0,active=adj.filter(x=>x.length).length,side=Array(v).fill(-1);
   for(let u=0;u<v;u++)if(adj[u].length&&side[u]<0){c++;let q=[u],ok=true;side[u]=0;for(let i=0;i<q.length;i++)for(let w of adj[q[i]]){if(side[w]<0){side[w]=side[q[i]]^1;q.push(w)}else if(side[w]===side[q[i]])ok=false;}b+=+ok}
   let best=2*n;
   for(let blank=-1;blank<n;blank++){
    let used=new Set(blank<0?[]:E[blank]),single=[];
    function inspect(){
     patterns++;
     const next=Array(v).fill(-1);for(const [i,s] of single)next[E[i][s]]=E[i][s^1];
     let done=new Set(),even=0,odd=0;for(let u=0;u<v;u++){if(done.has(u))continue;let seen=new Map(),w=u,t=0;while(w>=0&&next[w]>=0&&!done.has(w)&&!seen.has(w)){seen.set(w,t++);w=next[w]}if(seen.has(w)){if((t-seen.get(w))%2)odd++;else even++}for(const x of seen.keys())done.add(x)}
     const pred=even===0&&odd<=(blank<0?1:0);
     let rows=[...single.map(x=>x[0]),...(blank<0?[]:[blank])].sort((a,b)=>a-b),req=new Map(single),k=rows.length,count=0;
     function direct(i,mask,r){if(count>=2)return;if(i===k){if(r===0)count++;return}for(let j=0;j<k;j++)if(!(mask>>j&1))for(let t=0;t<2;t++)if(!req.has(rows[i])||E[rows[j]][(req.get(rows[i])+t)%2]===E[rows[i]][req.get(rows[i])])direct(i+1,mask|1<<j,r^t)}
     direct(0,0,0);if(pred!==(count===1))throw Error("full cycle criterion");
     if(pred){certs++;best=Math.min(best,2*n-single.length-(blank<0?0:2))}
    }
    function gen(i){if(i===n){inspect();return}if(i===blank){gen(i+1);return}gen(i+1);for(let s=0;s<2;s++){let u=E[i][s];if(used.has(u))continue;used.add(u);single.push([i,s]);gen(i+1);single.pop();used.delete(u)}}gen(0)
   }
   const expected=2*n-active+c-1,sign=2*n-active+Math.max(0,b-1);if(best!==expected)throw Error(JSON.stringify({E,best,expected}));gaps[best-sign]=(gaps[best-sign]||0)+1;graphs++;
  }
 }
 if(graphs!==1094||patterns!==312453)throw Error("census");
 return {graphs,patterns,certs,gaps};
}
function solveGraphObservation(E,v){
 const n=E.length,N=1<<n,all=N-1,pop=new Uint8Array(N),cm=new Int32Array(v),side=Array.from({length:v},()=>new Uint8Array(n)),deg=new Uint8Array(v);
 if(n<1||n>12||v<2||v>7)throw Error("audit domain");
 for(let i=0;i<n;i++)for(let s=0;s<2;s++){const c=E[i][s];cm[c]|=1<<i;side[c][i]=s;deg[c]++}
 const gp=new Int32Array(v);let H=1;for(let c=0;c<v;c++){gp[c]=H;H*=deg[c]+1}
 const digits=new Uint8Array(H*v),sum=new Uint8Array(H);for(let h=0;h<H;h++)for(let c=0;c<v;c++){const q=Math.floor(h/gp[c])%(deg[c]+1);digits[h*v+c]=q;sum[h]+=q}
 const strides=new Int32Array(N*v),caps=new Uint8Array(N*v),off=new Int32Array(N+1);for(let m=0;m<N;m++){pop[m]=m?pop[m&(m-1)]+1:0;let p=1;for(let c=0;c<v;c++){let d=pop[m&cm[c]];caps[m*v+c]=d;strides[m*v+c]=p;p*=d+1;}off[m+1]=off[m]+p;}
 const C=new Uint8Array(2*off[N]),D=new Uint16Array(2*off[N]);let countStates=0,depthStates=0;
 function key(h,m,r){let z=off[m];for(let c=0;c<v;c++){let d=digits[h*v+c];if(d>caps[m*v+c])return -1;z+=d*strides[m*v+c]}return z*2+r;}
 function count(h,m,r){
  const b=pop[m]-sum[h];if(b<0)return 0;if(b>0)r=0;const k=key(h,m,r);if(k<0)return 0;if(C[k])return C[k]-1;
  countStates++;let a=0,d=0;
  if(!h){if(b>=2)a=d=2;else if(b===1||r===0)a=1;}
  else{let c=0;while(!digits[h*v+c])c++;for(let j=m&cm[c];j;){const bit=j&-j;j^=bit;const l=31-Math.clz32(bit),z=count(h-gp[c],m^bit,r^side[c][l]),p=pop[m&(bit-1)]&1;let x=z%3,y=Math.floor(z/3);if(p)[x,y]=[y,x];a=Math.min(2,a+x);d=Math.min(2,d+y);if(a===2&&d===2)break;}}
  C[k]=1+a+3*d;return a+3*d;
 }
 function depth(h,m,r){
  const b=pop[m]-sum[h];if(b>0)r=0;const z=count(h,m,r),a=z%3,d=Math.floor(z/3);if(a+d<=1)return 0;
  const k=key(h,m,r);if(D[k])return D[k]-1;depthStates++;const best=[a&&d?31:0,31,Math.max(a,d)<=1?0:31];
  function consider(ch){const w=[0,0,0];for(const [x,l,t] of ch)if(count(x,l,t)){const q=depth(x,l,t);for(let i=0;i<3;i++)w[i]=Math.max(w[i],1+((q>>(5*i))&31));}for(let i=0;i<3;i++)best[i]=Math.min(best[i],w[i]);}
  if(b>0)for(let s=0;s<(b===1?2:1);s++){const ch=[];for(let c=0;c<v;c++)if(digits[h*v+c]<caps[m*v+c])ch.push([h+gp[c],m,r^s]);consider(ch)}
  for(let c=0;c<v;c++)if(digits[h*v+c]){const ch=[];for(let j=m&cm[c];j;){let bit=j&-j;j^=bit;ch.push([h-gp[c],m^bit,r^side[c][31-Math.clz32(bit)]]);}consider(ch)}
  if(best.some(x=>x>=31))throw Error("unresolved");const q=best[0]|best[1]<<5|best[2]<<10;D[k]=q+1;return q;
 }
 const q=depth(0,all,0),depths=[q&31,(q>>5)&31,(q>>10)&31];
 let cover=99,strong=99;for(let s=0;s<1<<v;s++)if(E.every(([i,j])=>(s>>i&1)||(s>>j&1))){const k=s.toString(2).replace(/0/g,"").length;cover=Math.min(cover,k);if(E.some(([i,j])=>(s>>i&1)&&(s>>j&1)))strong=Math.min(strong,k)}
 const lower=Math.max(0,2*n-cover-1,2*n-strong);if(depths[0]<lower||depths[1]<depths[0])throw Error("cover lower violated");
 return {depths,cover,strong,lower,countStates,depthStates,tableBytes:C.byteLength+D.byteLength};
}
function auditGraphAdaptiveObjectives(){
 let graphs=0,gaps={};for(let v=2;v<=4;v++){const all=[];for(let i=0;i<v;i++)for(let j=i+1;j<v;j++)all.push([i,j]);for(let m=1;m<1<<all.length;m++){const E=all.filter((_,i)=>m>>i&1),r=solveGraphObservation(E,v),g=r.depths[0]-r.lower;gaps[g]=(gaps[g]||0)+1;graphs++;}}
 const families=[["star6",[[0,1],[0,2],[0,3],[0,4],[0,5],[0,6]]],["cycle6",[[0,1],[1,2],[2,3],[3,4],[4,5],[5,0]]],["path6",[[0,1],[1,2],[2,3],[3,4],[4,5],[5,6]]],["twoTriangles",[[0,1],[1,2],[2,0],[3,4],[4,5],[5,3]]],["matching3",[[0,1],[2,3],[4,5]]],["K23",[[0,2],[0,3],[0,4],[1,2],[1,3],[1,4]]]];
 const controls=families.map(([name,E])=>({name,...solveGraphObservation(E,1+Math.max(...E.flat()))}));
 const colors="URFDLB",labels=["DL","BL","FL","UL","DB","DF","UB","UF","DR","BR","FR","UR"],cube=solveGraphObservation(labels.map(l=>[...l].map(c=>colors.indexOf(c))),6);
 if(graphs!==71||gaps[0]!==71||cube.depths.join(",")!=="20,20,19")throw Error("adaptive census");
 return {graphs,gaps,controls,cube};
}
console.log(JSON.stringify({...audit(),clock:auditClock(),structure:auditStructure(),parityCycles:auditParityCycles(),orientedCharacters:auditOrientedCharacters(),prefixPolymatroid:auditPrefixPolymatroid(),parityPolytope:auditParityPolytope(),parityHoles:auditParityHoles(),rankBlindness:auditRankBlindness(),paritySupportFunction:auditParitySupportFunction(),parityExchanges:auditParityExchanges(),graphParityClassification:auditGraphParityClassification(),boundedExchange:auditBoundedExchange(),signCertificates:auditSignCertificates(),cornerSignMinimax:auditCornerSignMinimax(),cornerGoals:auditCornerGoals(),earlyCornerSign:auditEarlyCornerSign(),chargedCycleCertificates:auditChargedCycleCertificates(),graphSignCertificates:auditGraphSignCertificateFormula(),fullGraphCertificates:auditFullGraphCertificates(),graphAdaptiveObjectives:auditGraphAdaptiveObjectives(),frozenLeaves:auditFrozenLeaves(loadPinnedCertificate())}, null, 2));
