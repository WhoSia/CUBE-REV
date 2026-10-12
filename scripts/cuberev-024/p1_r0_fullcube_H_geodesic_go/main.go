// CUBE-REV 0.24 P1-R0: independent Go exact complete H subgroup and whole-cube geodesic distortion.
// No imports from JavaScript, no source/participant private data.
package main
import("fmt";"sort";"strings")
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
 all:=[]int{};H:=[]int{}
 for i,m:=range moves{all=append(all,i);if strings.HasSuffix(m.Name,"2"){H=append(H,i)}}
 full,fl:=bfs(goal,moves,all,5)
 Hfull,hl:=bfs(goal,moves,H,16)
 require(fmt.Sprint(fl)=="[1 18 243 3240 43239 574908]","entire 18 HTM exact original-state shells")
 require(fmt.Sprint(hl)=="[1 6 27 120 519 1932 6484 20310 55034 113892 178495 179196 89728 16176 1488 144 0]","complete halfturn generated subgroup shells")
 require(len(Hfull)==663552,"independently enumerated exact H group order")
 edges:=map[string][]int{}
 for i,s:=range slots{
  zeros:=0;for ax:=0;ax<3;ax++{if s.P[ax]==0{zeros++}}
  if zeros==1{p:=xyz(s.P);edges[p]=append(edges[p],i)}
 }
 names:=[]string{};for p:=range edges{names=append(names,p)};sort.Strings(names)
 require(len(names)==12,"all real twelve physical edges")
 pairSlots:=[][]int{};edgeIds:=[]string{};byColor:=map[string]int{}
 for _,place:=range names{
  ix:=edges[place];require(len(ix)==2,"two genuine original edge stickers")
  pairSlots=append(pairSlots,ix)
  colors:=[]byte{goal[ix[0]],goal[ix[1]]}
  sort.Slice(colors,func(i,j int)bool{return colors[i]<colors[j]})
  edgeIds=append(edgeIds,string(colors))
  byColor[string(colors)]=len(edgeIds)-1
 }
 require(len(byColor)==12,"twelve distinct physical cubies")
 parent:=make([]int,12);for i:=0;i<12;i++{parent[i]=i}
 var root func(int)int
 root=func(i int)int{for parent[i]!=i{i=parent[i]};return i}
 for _,m:=range H{
  state:=apply(goal,moves[m])
  for i,ix:=range pairSlots{
   color:=[]byte{state[ix[0]],state[ix[1]]}
   sort.Slice(color,func(a,b int)bool{return color[a]<color[b]})
   j,ok:=byColor[string(color)];require(ok,"halfturn preserved valid edge identity")
   parent[root(i)]=root(j)
  }
 }
 orbitGroup:=map[int][]string{}
 for i,c:=range edgeIds{rootID:=root(i);orbitGroup[rootID]=append(orbitGroup[rootID],c)}
 orbitNames:=[]string{}
 for _,group:=range orbitGroup{sort.Strings(group);require(len(group)==4,"must be actual four-edge orbit");orbitNames=append(orbitNames,strings.Join(group,","))}
 sort.Strings(orbitNames)
 require(fmt.Sprint(orbitNames)=="[BD,BU,DF,FU BL,BR,FL,FR DL,DR,LU,RU]","exact real physical edge tetrads")
 orbit:=func(state string)bool{
  for pos,ix:=range pairSlots{
   colors:=[]byte{state[ix[0]],state[ix[1]]}
   sort.Slice(colors,func(a,b int)bool{return colors[a]<colors[b]})
   piece,ok:=byColor[string(colors)];require(ok,"real edge colors")
   if root(pos)!=root(piece){return false}
  }
  return true
 }
 var byDepthOrbit,byDepthMember [6]int
 hCosts:=map[int]int{}
 for state,rec:=range full{
  preserving:=orbit(state)
  member,exists:=Hfull[state]
  if preserving{byDepthOrbit[rec.D]++}
  if exists{byDepthMember[rec.D]++;require(preserving,"true H word broke actual generator orbit");if rec.D==5{hCosts[member.D]++}}
  require(preserving==exists,"finite whole 18HTM radius5 real-orbit classifier discrepancy")
 }
 require(byDepthOrbit==[6]int{1,6,27,120,519,2124},"real all18 d5 orbit-positive census")
 require(byDepthMember==byDepthOrbit,"full H subgroup membership within finite radius5")
 require(hCosts[5]==1932&&hCosts[8]==96&&hCosts[9]==96&&len(hCosts)==3,"exact full versus H geodesic distortion")
 index:=map[string]int{};for i,m:=range moves{index[m.Name]=i}
 actual:=func(word string)string{state:=goal;for _,token:=range strings.Fields(word){i,ok:=index[token];require(ok,"known legal original move");state=apply(state,moves[i])};return state}
 for _,tc:=range []struct{word string;hDist int}{
  {"D U R2 D U",9},{"D U R2 D' U",8},
 }{
  source:=actual(tc.word)
  s18,ok:=full[source];require(ok&&s18.D==5,"full HTM exact five physical source")
  sH,ok:=Hfull[source];require(ok&&sH.D==tc.hDist,"true subgroup exact distance")
  require(orbit(source),"actual edge tetrads preserved")
 }
 require(actual("D U R2 D U U' D' R2 U' D'")==goal,"original 54-sticker exact five-move witness")
 require(actual("D U R2 D U U2 B2 R2 D2 F2 U2 L2 U2 F2")==goal,"original 54-sticker exact nine-move subgroup witness")
 require(actual("D U R2 D' U U' D R2 U' D'")==goal,"second original 54-sticker exact five-move witness")
 require(actual("D U R2 D' U F2 R2 U2 F2 U2 R2 U2 F2")==goal,"second original 54-sticker exact eight-move subgroup witness")
 fmt.Printf("CUBE_REV_024_P1_R0_GO_FULL_PHYSICAL_H_GEODESIC_PASS FULL18=%v H_CAYLEY=%v H_ORDER=%d ORBITS=%v SOURCE_POSITIVES=%v DISTORTION_D5_TO_H=%v\n",fl,hl,len(Hfull),orbitNames,byDepthOrbit,hCosts)
}
