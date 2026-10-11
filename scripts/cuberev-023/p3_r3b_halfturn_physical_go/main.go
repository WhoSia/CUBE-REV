// CUBE-REV 0.23 P3-R3B — independent Go original-54-facelet audit.
// Recreates actual layer-rotation permutations and exact all18/half6 BFS.
// Neither imports the JavaScript cube engine nor human reconstruction data.
package main
import(
 "encoding/csv"
 "fmt"
 "os"
 "sort"
 "strconv"
 "strings"
)
type vec [3]int
type slot struct{p,n vec}
type action struct{name string; permutation [54]int}
type info struct{depth int;count int}
func require(b bool,s string){if !b{panic(s)}}
func faceNormal(f byte)vec{switch f{case 'U':return vec{0,1,0};case 'R':return vec{1,0,0};case 'F':return vec{0,0,1};case 'D':return vec{0,-1,0};case 'L':return vec{-1,0,0};case 'B':return vec{0,0,-1}};panic("face")}
func str(v vec)string{return fmt.Sprintf("%d,%d,%d",v[0],v[1],v[2])}
func rot(v vec,axis int,q int)vec{for j:=0;j<((q%4)+4)%4;j++{x,y,z:=v[0],v[1],v[2];switch axis{case 0:v=vec{x,-z,y};case 1:v=vec{z,y,-x};case 2:v=vec{-y,x,z}}};return v}
func moveLayer(f byte)(int,int,int){switch f{case 'U':return 1,1,-1;case 'D':return 1,-1,1;case 'R':return 0,1,-1;case 'L':return 0,-1,1;case 'F':return 2,1,-1;case 'B':return 2,-1,1};panic("unknown")}
func key(s slot)string{return str(s.p)+"|"+str(s.n)}
func physicalActions()[]action{
 slots:=[]slot{}
 for _,f:=range []byte("URFDLB"){
  n:=faceNormal(f);local:=[]slot{}
  for a:=-1;a<=1;a++{for b:=-1;b<=1;b++{
   var p vec
   if n[0]!=0{p=vec{n[0],a,b}}else if n[1]!=0{p=vec{a,n[1],b}}else{p=vec{a,b,n[2]}}
   local=append(local,slot{p:p,n:n})
  }}
  sort.Slice(local,func(i,j int)bool{return str(local[i].p)<str(local[j].p)})
  slots=append(slots,local...)
 }
 require(len(slots)==54,"slots")
 positions:=map[string]int{};for i,s:=range slots{positions[key(s)]=i}
 require(len(positions)==54,"positions")
 out:=[]action{}
 for _,f:=range []byte("URFDLB"){for _,suffix:=range []string{"","'","2"}{
  axis,layer,q:=moveLayer(f);power:=1;if suffix=="'"{power=3}else if suffix=="2"{power=2}
  m:=action{name:string(f)+suffix};seen:=map[int]bool{}
  for i,s:=range slots{
   t:=s;if s.p[axis]==layer{t.p=rot(s.p,axis,q*power);t.n=rot(s.n,axis,q*power)}
   target,ok:=positions[key(t)];require(ok,"face geometry");require(!seen[target],"permutation collision");seen[target]=true;m.permutation[i]=target
  }
  out=append(out,m)
 }}
 return out
}
func turn(s string,m action)string{
 var result [54]byte
 for i,t:=range m.permutation{result[t]=s[i]}
 return string(result[:])
}
func census(goal string,actions []action,alphabet []int,maxDepth int)(map[string]info,[]int){
 vis:=map[string]info{goal:{depth:0,count:1}};front:=[]string{goal};hist:=[]int{1}
 for d:=1;d<=maxDepth;d++{
  next:=[]string{}
  for _,s:=range front{
   p:=vis[s]
   for _,i:=range alphabet{
    child:=turn(s,actions[i]);v,exists:=vis[child]
    if exists{if v.depth==d{v.count+=p.count;vis[child]=v};continue}
    vis[child]=info{depth:d,count:p.count};next=append(next,child)
   }
  }
  front=next;hist=append(hist,len(front))
 }
 return vis,hist
}
func equal(a,b []int)bool{if len(a)!=len(b){return false};for i,v:=range a{if b[i]!=v{return false}};return true}
func main(){
 f,e:=os.Open("data/cuberev-023/p3_r1b_real_62_physical_face9_cubie_fixture.csv");if e!=nil{panic(e)};defer f.Close()
 rows,e:=csv.NewReader(f).ReadAll();if e!=nil{panic(e)}
 require(len(rows)==63,"62 physical source rows");require(strings.Join(rows[0],",")=="index,U,R,F,D,L,B,source_HTM,cubie_sha256","source fixture header")
 moves:=physicalActions()
 require(len(moves)==18,"18 HTM physical moves")
 half:=[]int{};all:=[]int{}
 for i,m:=range moves{all=append(all,i);if strings.HasSuffix(m.name,"2"){half=append(half,i)}}
 require(equal(half,[]int{2,5,8,11,14,17}),"half turns")
 var builder strings.Builder
 for _,f:=range []byte("URFDLB"){builder.WriteString(strings.Repeat(string(f),9))}
 goal:=builder.String()
 full,fullCounts:=census(goal,moves,all,4)
 hg,histHalf:=census(goal,moves,half,5)
 reverse,histRev:=census(goal,moves,half,2)
 require(equal(fullCounts,[]int{1,18,243,3240,43239}),"all18 finite ball")
 require(equal(histHalf,[]int{1,6,27,120,519,1932}),"halfturn finite ball")
 require(equal(histRev,[]int{1,6,27})&&len(reverse)==34,"meet-in-middle goal radius2")
 literal,shortestTotal,firstDouble,wordDouble,scannedMax,scannedSum:=0,0,0,0,0,0
 firstFrequency:=map[string]int{}
 for k:=0;k<62;k++{
  row:=rows[k+1];require(len(row)==9,"width")
  idx,e:=strconv.Atoi(row[0]);require(e==nil&&idx==k,"idx")
  source:=strings.Join(row[1:7],"")
  d,e:=strconv.Atoi(row[7]);require(e==nil&&(d==3||d==5),"source exact HTM")
  h,ok:=hg[source];require(ok&&h.depth==d,"HTR word achieves full source HTM exact distance")
  if x,ok:=full[source];ok{require(x.depth==d,"all18 source lower-bound")}
  first:=0;allWays,halfWays:=0,0
  for i,m:=range moves{
   n,ok:=full[turn(source,m)]
   if ok&&n.depth==d-1{
    require(strings.HasSuffix(m.name,"2"),"nonhalf shortest first move!")
    firstFrequency[m.name]++;first++;allWays+=n.count
   }
  }
  for _,i:=range half{if n,ok:=hg[turn(source,moves[i])];ok&&n.depth==d-1{halfWays+=n.count}}
  require(first>=1&&first<=2,"geodesic first choices")
  require(allWays==halfWays&&(allWays==1||allWays==2),"all shortest 18 HTM are HTR words")
  literal+=d;shortestTotal+=allWays;if first==2{firstDouble++};if allWays==2{wordDouble++}
  // The independent solver makes <=3 forward halfturn steps, then matches
  // one of 34 reverse-goal <=2 states. Record an actual physical solution.
  seen:=map[string][]int{source:{}};front:=[]string{source}
  best:=[]int(nil);scanned:=0
  for depth:=0;depth<=3;depth++{
   next:=[]string{}
   for _,cur:=range front{
    scanned++
    if rev,ok:=reverse[cur];ok{
     // The BFS above records the minimum depth; reconstruct its word
     // through a second tiny <=2 enumeration from solved.
     reverseWord:=[]int(nil)
     if rev.depth==0{reverseWord=[]int{}}
     if rev.depth==1{for _,i:=range half{if turn(goal,moves[i])==cur{reverseWord=[]int{i};break}}}
     if rev.depth==2{
      for _,i:=range half{for _,j:=range half{if turn(turn(goal,moves[i]),moves[j])==cur{reverseWord=[]int{i,j};break}};if reverseWord!=nil{break}}
     }
     require(reverseWord!=nil,"reverse witness")
     candidate:=append(append([]int{},seen[cur]...),reverseWord[len(reverseWord):len(reverseWord)]...)
     for x:=len(reverseWord)-1;x>=0;x--{candidate=append(candidate,reverseWord[x])}
     if best==nil||len(candidate)<len(best){best=candidate}
    }
    if depth==3{continue}
    for _,i:=range half{v:=turn(cur,moves[i]);if _,exists:=seen[v];!exists{seen[v]=append(append([]int{},seen[cur]...),i);next=append(next,v)}}
   }
   front=next
  }
  require(best!=nil&&len(best)==d,"actual solver attained all18 geodesic")
  state:=source;for _,m:=range best{state=turn(state,m)}
  require(state==goal,"all 54 source facelets physically solved")
  if scanned>scannedMax{scannedMax=scanned};scannedSum+=scanned
 }
 require(literal==306&&shortestTotal==74&&firstDouble==4&&wordDouble==12,"exact observed results")
 fmt.Printf("CUBE_REV_023_P3_R3B_GO_PASS SOURCE=ACTUAL_ORIGINAL_54_STICKER_FIXTURE STATES=62 EXACT_ALL18_DEPTH4=%v HALF_DEPTH5=%v GOAL_RADIUS2=34 LITERAL_TOKENS=306 SHORTEST_WORDS=74 FIRST_MOVE_TIES=4 DOUBLE_WORDS=12 MITM_MAX_SCANNED=%d MITM_SUM_SCANNED=%d FIRST_MOVE_SUPPORT=%v\n",fullCounts,histHalf,scannedMax,scannedSum,firstFrequency)
}
