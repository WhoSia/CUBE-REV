// CUBE-REV 0.24 P1-R1: independent Go exact certified full18/H5 solver comparison.
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
 for _,f:=range []byte("URFDLB"){b.WriteString(strings.Repeat(string(f),9))}
 goal:=b.String()
 alphabet:=[]int{};H:=[]int{}
 for i,m:=range moves{alphabet=append(alphabet,i);if strings.HasSuffix(m.Name,"2"){H=append(H,i)}}
 R4,r4Shells:=bfs(goal,moves,alphabet,4)
 H5,h5Shells:=bfs(goal,moves,H,5)
 Full5,fullShells:=bfs(goal,moves,alphabet,5)
 HGroup,_:=bfs(goal,moves,H,16)
 require(fmt.Sprint(r4Shells)=="[1 18 243 3240 43239]","independent full18 radius4 table")
 require(fmt.Sprint(h5Shells)=="[1 6 27 120 519 1932]","independent halfturn radius5 table")
 require(fmt.Sprint(fullShells)=="[1 18 243 3240 43239 574908]","independent full18 radius5 evaluator")
 require(len(HGroup)==663552,"entire original physical halfturn group")
 applyWord:=func(s string,path []int)string{for _,i:=range path{s=apply(s,moves[i])};return s}
 var construct func(string,map[string]Record,[]int)[]int
 construct=func(s string,table map[string]Record,alphabet []int)[]int{
  path:=[]int{}
  for s!=goal{
   v,ok:=table[s];require(ok&&v.D>0,"distance witness must exist")
   found:=false
   for _,i:=range alphabet{
    child:=apply(s,moves[i])
    r,ok:=table[child]
    if ok&&r.D==v.D-1{
     s=child;path=append(path,i);found=true;break
    }
   }
   require(found,"facelet geodesic predecessor")
  }
  return path
 }
 type Result struct{Path []int;Probes int;Rotations int;Mode string}
 baseline:=func(s string)Result{
  probes:=1
  if _,ok:=R4[s];ok{return Result{construct(s,R4,alphabet),probes,0,"goal4"}}
  for _,i:=range alphabet{
   child:=apply(s,moves[i]);probes++
   if _,ok:=R4[child];ok{
    suffix:=construct(child,R4,alphabet)
    return Result{append([]int{i},suffix...),probes,probes-1,"full18"}
   }
  }
  return Result{nil,probes,18,"HOLD_OUTSIDE_RADIUS5"}
 }
 hybrid:=func(s string)Result{
  probes:=1
  if _,ok:=R4[s];ok{return Result{construct(s,R4,alphabet),probes,0,"goal4"}}
  h,ok:=H5[s];probes++
  if ok&&h.D==5{return Result{construct(s,H5,H),probes,0,"certified_H5"}}
  for _,i:=range alphabet{
   child:=apply(s,moves[i]);probes++
   if _,ok:=R4[child];ok{
    suffix:=construct(child,R4,alphabet)
    return Result{append([]int{i},suffix...),probes,probes-2,"full18"}
   }
  }
  return Result{nil,probes,18,"HOLD_OUTSIDE_RADIUS5"}
 }
 // Independently derive genuine physical edge-cubie two-sticker positions.
 // Allowed pair patterns come only from the H5 physical solver table.
 physicalEdges:=map[string][]int{}
 for i,slot:=range slots{
  hits:=0;for j:=0;j<3;j++{if slot.P[j]!=0{hits++}}
  if hits==2{p:=xyz(slot.P);physicalEdges[p]=append(physicalEdges[p],i)}
 }
 edgeNames:=[]string{};for p:=range physicalEdges{edgeNames=append(edgeNames,p)};sort.Strings(edgeNames)
 require(len(edgeNames)==12,"twelve true two-sticker edge positions")
 pairs:=[][]int{};allowed:=[]map[string]bool{}
 for _,p:=range edgeNames{
  ix:=physicalEdges[p];require(len(ix)==2,"edge position physical slot pair")
  pairs=append(pairs,ix);allowed=append(allowed,map[string]bool{})
 }
 for s:=range H5{
  for j,pair:=range pairs{allowed[j][string([]byte{s[pair[0]],s[pair[1]]})]=true}
 }
 for _,set:=range allowed{require(len(set)==4,"four physical edge pair signatures per orbit position")}
 edgeAllowed:=func(s string)bool{
  for j,p:=range pairs{
   if !allowed[j][string([]byte{s[p[0]],s[p[1]]})]{return false}
  }
  return true
 }
 for s:=range HGroup{require(edgeAllowed(s),"no true halfturn group member violates its edge tetrad")}
 gatePassD5:=0;gateCertified:=0
 for source,r:=range Full5{
  if r.D!=5{continue}
  pass:=edgeAllowed(source)
  if pass{gatePassD5++}
  if h,ok:=H5[source];ok&&h.D==5{gateCertified++;require(pass,"gate cannot lose exact H5 certificate")}
 }
 require(gatePassD5==2124&&gateCertified==1932,"finite entire full18 radius5 physical edge orbit gate")

 type Total struct{BaseProbes,DualProbes,BaseRotations,DualRotations,Count,Certified int}
 tally:=map[string]*Total{
  "H5_exact_global5":{},
  "H_members_but_cost8or9":{},
  "outside_H_d5":{},
 }
 // Go map iteration order is not the JS cohort order, so an independent
 // deterministic lexical 4096 subset is chosen below; no claims that its
 // timing/sample is identical to the seeded JS reservoir.
 outside:=[]string{}
 for source,r:=range Full5{
  if r.D!=5{continue}
  h,ok:=HGroup[source]
  category:=""
  if ok{
   if h.D==5{category="H5_exact_global5"}else if h.D==8||h.D==9{category="H_members_but_cost8or9"}else{panic("unexpected true physical H distance")}
  }else{outside=append(outside,source);continue}
  a,z:=baseline(source),hybrid(source)
  require(len(a.Path)==5&&len(z.Path)==5,"global exact physical HTM solution 5")
  require(applyWord(source,a.Path)==goal,"baseline solved real cube")
  require(applyWord(source,z.Path)==goal,"hybrid solved real cube")
  total:=tally[category];total.Count++;total.BaseProbes+=a.Probes;total.DualProbes+=z.Probes
  total.BaseRotations+=a.Rotations;total.DualRotations+=z.Rotations
  if z.Mode=="certified_H5"{total.Certified++}
 }
 sort.Strings(outside)
 require(len(outside)==572784,"source-independent full18 d5 outside H")
 for _,source:=range outside[:4096]{
  a,z:=baseline(source),hybrid(source)
  require(len(a.Path)==5&&len(z.Path)==5,"independent held-out physical full18 length5")
  require(applyWord(source,a.Path)==goal&&applyWord(source,z.Path)==goal,"original 54 facelets independently solved")
  t:=tally["outside_H_d5"];t.Count++;t.BaseProbes+=a.Probes;t.DualProbes+=z.Probes
  t.BaseRotations+=a.Rotations;t.DualRotations+=z.Rotations
  require(z.Mode=="full18","out-of-H must not be miscertified")
 }
 require(tally["H5_exact_global5"].Count==1932&&tally["H5_exact_global5"].Certified==1932,"real subgroup easy case")
 require(tally["H_members_but_cost8or9"].Count==192&&tally["H_members_but_cost8or9"].Certified==0,"192 actual H-distortion controls")
 require(tally["H5_exact_global5"].BaseProbes==20007&&tally["H5_exact_global5"].DualProbes==3864,"exact fair easy baseline probes")
 require(tally["H_members_but_cost8or9"].BaseProbes==1056&&tally["H_members_but_cost8or9"].DualProbes==1248,"exact fair adversarial probes")
 require(tally["outside_H_d5"].Count==4096,"independently sampled out-of-H cohort")
 // Radius-six physical negative control is outside both stated solvers'
 // completeness scopes: never emit an unverified word as exact.
 holdFound:=false
 for s,v:=range Full5{
  if v.D!=5||holdFound{continue}
  for _,i:=range alphabet{
   beyond:=apply(s,moves[i])
   if _,known:=Full5[beyond];known{continue}
   a,z:=baseline(beyond),hybrid(beyond)
   require(a.Mode=="HOLD_OUTSIDE_RADIUS5"&&z.Mode=="HOLD_OUTSIDE_RADIUS5","no out-of-domain false certificate")
   holdFound=true;break
  }
 }
 require(holdFound,"actual full18 radius6 negative control")
 require(gatePassD5-gateCertified-(tally["H5_exact_global5"].BaseProbes-tally["H5_exact_global5"].DualProbes)==-15951,"complete real d5 source cohort certified edge gate lookup reduction")
 fmt.Printf("CUBE_REV_024_P1_R1_GO_INDEPENDENT_REAL_54_FACELET_CERTIFIED_DISPATCH_PASS TABLES=full18_r4:%d_H5:%d EVAL_FULL5=%d EVAL_HGROUP=%d EASY=%+v DISTORTION=%+v OUTSIDE_H_4096=%+v R6_HOLD=true EDGE_ORBIT_COMPLETE_D5_PASSES=%d GATED_GLOBAL_PROBE_CHANGE=-15951\n",len(R4),len(H5),len(Full5),len(HGroup),*tally["H5_exact_global5"],*tally["H_members_but_cost8or9"],*tally["outside_H_d5"],gatePassD5)
}
