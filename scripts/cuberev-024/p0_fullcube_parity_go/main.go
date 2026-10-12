// CUBE-REV 0.24 P0: independent Go original 54-sticker cube and exact parity court.
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
 var builder strings.Builder;for _,f:=range []byte("URFDLB"){builder.WriteString(strings.Repeat(string(f),9))}
 goal:=builder.String();require(len(moves)==18&&len(goal)==54,"geometry")
 alphabet:=[]int{};half:=[]int{}
 for i,m:=range moves{alphabet=append(alphabet,i);if strings.HasSuffix(m.Name,"2"){half=append(half,i)}}
 full,fl:=bfs(goal,moves,alphabet,3);h5,hl:=bfs(goal,moves,half,5)
 require(fmt.Sprint(fl)=="[1 18 243 3240]","18HTM Cayley layers")
 require(fmt.Sprint(hl)=="[1 6 27 120 519 1932]","halfturn Cayley layers")
 corners:=map[string][]int{}
 for i,s:=range slots{if s.P[0]!=0&&s.P[1]!=0&&s.P[2]!=0{p:=xyz(s.P);corners[p]=append(corners[p],i)}}
 names:=[]string{};for k:=range corners{names=append(names,k)};sort.Strings(names)
 require(len(names)==8,"corner positions")
 triads:=[][]int{};identity:=[]string{}
 for _,name:=range names{ids:=corners[name];require(len(ids)==3,"corner stickers");triads=append(triads,ids)
  x:=[]byte{goal[ids[0]],goal[ids[1]],goal[ids[2]]};sort.Slice(x,func(i,j int)bool{return x[i]<x[j]});identity=append(identity,string(x))
 }
 type Row struct{H int `json:"half5"`; E int `json:"even_outside_half5"`; O int `json:"odd_proven_outside_half_group"`}
 byDepth:=[4]Row{}
 for state,v:=range full{
  p:=parity(state,triads,identity);_,inHalf:=h5[state];row:=&byDepth[v.D]
  if inHalf{require(p==0,"parity subgroup invariant");row.H++}else if p==1{row.O++}else{row.E++}
  if v.D>0{
   count:=0;for _,m:=range moves{r,ok:=full[apply(state,m)];if ok&&r.D==v.D-1{count+=r.Words}}
   require(count==v.Words,"exact geodesic DAG path multiplicity")
  }
 }
 require(byDepth==[4]Row{{1,0,0},{6,0,12},{27,108,108},{120,1440,1680}},"physical parity census")
 j,_:=json.Marshal(struct{Marker string `json:"marker"`;Full []int `json:"full18_layers"`;Half []int `json:"half6_layers"`;Census [4]Row `json:"by_depth"`;StateCount int `json:"full_state_count"`}{
 "CUBE_REV_024_P0_GO_PHYSICAL_PARITY_PASS",fl,hl,byDepth,len(full)})
 fmt.Println(string(j))
}
