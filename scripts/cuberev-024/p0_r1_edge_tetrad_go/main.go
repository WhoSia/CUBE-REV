// CUBE-REV 0.24 P0-R1: independent Go original 54-sticker and H edge-orbit court.
// No imports from JavaScript, no source/participant private data.
package main
import("encoding/json";"fmt";"sort";"strings")
type V [3]int
type Slot struct{P,N V}
type Move struct{Name string; Dest [54]int}
func require(b bool,s string){if !b{panic(s)}}
func xyz(v V)string{return fmt.Sprintf("%d,%d,%d",v[0],v[1],v[2])}
func normal(f byte)V{switch f{case 'U':return V{0,1,0};case 'R':return V{1,0,0};case 'F':return V{0,0,1};case 'D':return V{0,-1,0};case 'L':return V{-1,0,0};case 'B':return V{0,0,-1}};panic("face")}
func rule(f byte)(int,int,int){switch f{case 'U':return 1,1,-1;case 'R':return 0,1,-1;case 'F':return 2,1,-1;case 'D':return 1,-1,1;case 'L':return 0,-1,1;case 'B':return 2,-1,1};panic("face")}
func rotate(v V,axis,q int)V{for k:=0;k<((q%4)+4)%4;k++{x,y,z:=v[0],v[1],v[2];switch axis{case 0:v=V{x,-z,y};case 1:v=V{z,y,-x};case 2:v=V{-y,x,z}}};return v}
func where(s Slot)string{return xyz(s.P)+"|"+xyz(s.N)}
func geometry()([]Slot,[]Move){
 slots:=[]Slot{}
 for _,f:=range []byte("URFDLB"){n:=normal(f);part:=[]Slot{}
  for a:=-1;a<=1;a++{for b:=-1;b<=1;b++{p:=V{};if n[0]!=0{p=V{n[0],a,b}}else if n[1]!=0{p=V{a,n[1],b}}else{p=V{a,b,n[2]}};part=append(part,Slot{p,n})}}
  sort.Slice(part,func(i,j int)bool{return xyz(part[i].P)<xyz(part[j].P)})
  slots=append(slots,part...)
 }
 require(len(slots)==54,"facelets")
 lookup:=map[string]int{};for i,s:=range slots{lookup[where(s)]=i}
 require(len(lookup)==54,"positions")
 out:=[]Move{}
 for _,f:=range []byte("URFDLB"){for _,suf:=range []string{"","'","2"}{
  axis,layer,q:=rule(f);power:=1;if suf=="'"{power=3}else if suf=="2"{power=2}
  move:=Move{Name:string(f)+suf};used:=map[int]bool{}
  for i,v:=range slots{
   w:=v;if v.P[axis]==layer{w.P=rotate(v.P,axis,q*power);w.N=rotate(v.N,axis,q*power)}
   to,ok:=lookup[where(w)];require(ok&&!used[to],"legal sticker permutation");used[to]=true;move.Dest[i]=to
  }
  out=append(out,move)
 }}
 return slots,out
}
func apply(s string,m Move)string{var dst [54]byte;for i,j:=range m.Dest{dst[j]=s[i]};return string(dst[:])}
type Record struct{D,Words int}
func bfs(goal string,moves []Move,alphabet []int,limit int)(map[string]Record,[]int){
 seen:=map[string]Record{goal:{0,1}};front:=[]string{goal};layers:=[]int{1}
 for depth:=1;depth<=limit;depth++{
  next:=[]string{}
  for _,s:=range front{for _,i:=range alphabet{
   child:=apply(s,moves[i]);r,ok:=seen[child]
   if ok{if r.D==depth{r.Words+=seen[s].Words;seen[child]=r};continue}
   seen[child]=Record{depth,seen[s].Words};next=append(next,child)
  }}
  front=next;layers=append(layers,len(front))
 }
 return seen,layers
}
func parity(s string,triads [][]int,identity []string)int{
 order:=[]int{}
 for _,ids:=range triads{
  x:=[]byte{s[ids[0]],s[ids[1]],s[ids[2]]}
  sort.Slice(x,func(i,j int)bool{return x[i]<x[j]})
  ix:=-1;for i,t:=range identity{if string(x)==t{ix=i;break}}
  require(ix>=0,"full cubie corner ID");order=append(order,ix)
 }
 inversions:=0;for i:=0;i<8;i++{for j:=i+1;j<8;j++{if order[i]>order[j]{inversions++}}};return inversions%2
}
func main(){
 slots,moves:=geometry()
 var b strings.Builder
 for _,face:=range []byte("URFDLB"){b.WriteString(strings.Repeat(string(face),9))}
 goal:=b.String()
 fullAlphabet:=[]int{};halfs:=[]int{}
 for i,m:=range moves{fullAlphabet=append(fullAlphabet,i);if strings.HasSuffix(m.Name,"2"){halfs=append(halfs,i)}}
 full,fullLayers:=bfs(goal,moves,fullAlphabet,4)
 h5,halfLayers:=bfs(goal,moves,halfs,5)
 require(fmt.Sprint(fullLayers)=="[1 18 243 3240 43239]","full18 physical shells")
 require(fmt.Sprint(halfLayers)=="[1 6 27 120 519 1932]","physical half shells")
 edgePositions:=map[string][]int{}
 for i,s:=range slots{
  zeros:=0;for j:=0;j<3;j++{if s.P[j]==0{zeros++}}
  if zeros==1{edgePositions[xyz(s.P)]=append(edgePositions[xyz(s.P)],i)}
 }
 names:=[]string{};for k:=range edgePositions{names=append(names,k)};sort.Strings(names)
 require(len(names)==12,"twelve original physical edge positions")
 pairs:=[][]int{};ids:=[]string{}
 for _,place:=range names{
  ix:=edgePositions[place];require(len(ix)==2,"each edge has exactly two original stickers")
  pairs=append(pairs,ix)
  c:=[]byte{goal[ix[0]],goal[ix[1]]};sort.Slice(c,func(i,j int)bool{return c[i]<c[j]});ids=append(ids,string(c))
 }
 byId:=map[string]int{};for i,id:=range ids{byId[id]=i};require(len(byId)==12,"12 different original edges")
 parent:=make([]int,12);for i:=range parent{parent[i]=i}
 var root func(int)int
 root=func(i int)int{for parent[i]!=i{i=parent[i]};return i}
 for _,i:=range halfs{
  state:=apply(goal,moves[i])
  for pos,ix:=range pairs{
   color:=[]byte{state[ix[0]],state[ix[1]]}
   sort.Slice(color,func(a,b int)bool{return color[a]<color[b]})
   src,ok:=byId[string(color)];require(ok,"edge color identification")
   parent[root(pos)]=root(src)
  }
 }
 groups:=map[int][]string{}
 for i,c:=range ids{group:=root(i);groups[group]=append(groups[group],c)}
 require(len(groups)==3,"halfturn edge orbits must form three tetrads")
 orbitNames:=[]string{}
 for _,colors:=range groups{
  sort.Strings(colors);require(len(colors)==4,"four real edge cubies in each orbit")
  orbitNames=append(orbitNames,strings.Join(colors,","))
 }
 sort.Strings(orbitNames)
 require(fmt.Sprint(orbitNames)=="[BD,BU,DF,FU BL,BR,FL,FR DL,DR,LU,RU]","physical three tetrad classes")
 orbitOK:=func(state string)bool{
  for pos,ix:=range pairs{
   color:=[]byte{state[ix[0]],state[ix[1]]}
   sort.Slice(color,func(a,b int)bool{return color[a]<color[b]})
   src,ok:=byId[string(color)];require(ok,"physically legal edge ID")
   if root(src)!=root(pos){return false}
  }
  return true
 }
 for state:=range h5{require(orbitOK(state),"all physical H-words preserve three edge tetrads")}
 var good,bad,hit [5]int
 for state,v:=range full{
  condition:=orbitOK(state);_,inH5:=h5[state]
  if condition{good[v.D]++}else{bad[v.D]++}
  if inH5{hit[v.D]++}
  require(!inH5||condition,"halfturn orbit soundness")
  require(condition==inH5,"physical radius-four orbit gate exactness")
 }
 require(good==[5]int{1,6,27,120,519},"true H-domain census")
 require(bad==[5]int{0,12,216,3120,42720},"true excluded domain census")
 require(hit==good,"all positive source states have real H <=5 witness")
 fmt.Printf("CUBE_REV_024_P0_R1_GO_REAL_CUBE_EDGE_TETRAD_PASS FULL18=%v HALF6=%v ORBITS=%v GOOD=%v EXCLUDED=%v FULL_STATES=%d HALF5_STATES=%d GLOBAL_NONMEMBERS_IN_FULL_R4=%d\n",fullLayers,halfLayers,orbitNames,good,bad,len(full),len(h5),12+216+3120+42720)
}
