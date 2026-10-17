// R3-P11-P8: independent Go physical site-coordinate group engine + source root court.
// Rebuilds full cube B6 and all-corner C8 from its OWN 54-sticker geometry.
// Does NOT import any C++ packed physical move table or native count receipt.
package main

import (
 "fmt"
 "os"
 "runtime"
 "strconv"
 "time"
)
type V struct{ x,y,z int8 }
type Site struct{ p,n V }
type Key [20]uint8
type EK [12]uint8
var sites [54]Site
var moveSite [18][54]uint8
var marks [20]uint8
var cornerSites [8][3]uint8
var siteSlot [54]int8
var siteOri [54]int8
var nxtSlot [18][8]uint8
var nxtOri [18][8][3]uint8
var fact=[9]int{1,1,2,6,24,120,720,5040,40320}
var pt [18][]uint16
var ot [18][]uint16
var counts [19][11]uint64
func positions(i int)V {
 f,a,b:=i/9,int8(i%9/3-1),int8(i%3-1)
 switch f {
 case 0:return V{a,1,b}
 case 1:return V{a,-1,b}
 case 2:return V{1,a,b}
 case 3:return V{-1,a,b}
 case 4:return V{a,b,1}
 default:return V{a,b,-1}
 }
}
func normal(f int)V {
 switch f {
 case 0:return V{0,1,0}
 case 1:return V{0,-1,0}
 case 2:return V{1,0,0}
 case 3:return V{-1,0,0}
 case 4:return V{0,0,1}
 default:return V{0,0,-1}
 }
}
func rotate(v V,axis int,q int)V {
 q=((q%4)+4)%4
 for j:=0;j<q;j++ {
 switch axis {
 case 0:v=V{v.x,-v.z,v.y}
 case 1:v=V{v.z,v.y,-v.x}
 case 2:v=V{-v.y,v.x,v.z}
 }
 }
 return v
}
func abs(x int8)int {if x<0{return -int(x)};return int(x)}
func posWeight(v V)int{return abs(v.x)+abs(v.y)+abs(v.z)}
func must(ok bool,msg string){if !ok{panic(msg)}}
func geometry(){
 siteIndex:=make(map[Site]uint8,54)
 for i:=range sites{
 sites[i]=Site{positions(i),normal(i/9)}
 siteIndex[sites[i]]=uint8(i)
 siteSlot[i]=-1
 siteOri[i]=-1
 }
 must(len(siteIndex)==54,"duplicate source site")
 for a:=0;a<18;a++{
 face,shift:=a/3,a%3
 axis,layer,sign:=0,int8(1),-1
 switch face{
 case 0:axis=1;layer=1;sign=-1
 case 1:axis=0;layer=1;sign=-1
 case 2:axis=2;layer=1;sign=-1
 case 3:axis=1;layer=-1;sign=1
 case 4:axis=0;layer=-1;sign=1
 case 5:axis=2;layer=-1;sign=1
 }
 power:=1
 if shift==1{power=2}else if shift==2{power=3}
 for i,s:=range sites{
 v:=s.p;coord:=v.x
 if axis==1{coord=v.y}else if axis==2{coord=v.z}
 if coord==layer{s.p=rotate(s.p,axis,sign*power);s.n=rotate(s.n,axis,sign*power)}
 j,ok:=siteIndex[s];must(ok,"face move out of site space");moveSite[a][i]=j
 }
 }
 ci:=0
 for i:=0;i<18;i++{
 if posWeight(sites[i].p)!=3{continue}
 must(ci<8,"too many corners")
 p:=sites[i].p;fUD:=0;if p.y<0{fUD=1}
 order:=[3]int{fUD,0,0}
 if int(p.x)*int(p.y)*int(p.z)>0{
 if p.x>0{order[1]=2}else{order[1]=3}
 if p.z>0{order[2]=4}else{order[2]=5}
 }else{
 if p.z>0{order[1]=4}else{order[1]=5}
 if p.x>0{order[2]=2}else{order[2]=3}
 }
 for j,face:=range order{
 idx:=-1
 for i2:=0;i2<54;i2++{if i2/9==face&&sites[i2].p==p{idx=i2;break}}
 must(idx>=0,"missing corner site")
 cornerSites[ci][j]=uint8(idx);siteSlot[idx]=int8(ci);siteOri[idx]=int8(j)
 }
 must(int(cornerSites[ci][0])==i,"corner initial order error")
 marks[ci]=uint8(i);ci++
 }
 must(ci==8,"corner count")
 seen:=map[V]bool{};ei:=8
 for i,s:=range sites{
 if posWeight(s.p)!=2||seen[s.p]{continue}
 must(ei<20,"too many edges")
 seen[s.p]=true;marks[ei]=uint8(i);ei++
 }
 must(ei==20,"edge count")
 for a:=0;a<18;a++{
 for k:=0;k<8;k++{
 dest:=-1
 for j:=0;j<3;j++{
 site:=moveSite[a][cornerSites[k][j]]
 ds:=int(siteSlot[site]);must(ds>=0,"corner broken")
 if dest<0{dest=ds};must(dest==ds,"corner split")
 nxtOri[a][k][j]=uint8(siteOri[site])
 }
 nxtSlot[a][k]=uint8(dest)
 }
 }
 for a:=0;a<18;a++{pt[a]=make([]uint16,40320);ot[a]=make([]uint16,2187)}
 for idx:=0;idx<40320;idx++{
 p:=unrankP(idx)
 for a:=0;a<18;a++{
 var t [8]uint8
 for k:=0;k<8;k++{t[nxtSlot[a][k]]=p[k]}
 pt[a][idx]=uint16(rankP(t))
 }
 }
 for idx:=0;idx<2187;idx++{
 o:=unrankO(idx)
 for a:=0;a<18;a++{
 var t [8]uint8
 for k:=0;k<8;k++{t[nxtSlot[a][k]]=nxtOri[a][k][o[k]]}
 ot[a][idx]=uint16(rankO(t))
 }
 }
 fmt.Println("GO_INDEPENDENT_54_SITE_GEOMETRY_OK",len(siteIndex))
}
func rankP(p [8]uint8)int{
 r:=0;var used [8]bool
 for i,v:=range p{
 less:=0
 for z:=0;z<int(v);z++{if !used[z]{less++}}
 r+=less*fact[7-i];used[v]=true
 }
 return r
}
func unrankP(x int)[8]uint8{
 var v [8]uint8
 avail:=[8]uint8{0,1,2,3,4,5,6,7}
 for i:=0;i<8;i++{
 j:=x/fact[7-i];x%=fact[7-i];v[i]=avail[j]
 copy(avail[j:],avail[j+1:8-i])
 }
 return v
}
func rankO(p [8]uint8)int{
 r,s:=0,0
 for i:=0;i<7;i++{
 must(p[i]<3,"bad twist");r=r*3+int(p[i]);s+=int(p[i])
 }
 must((s+int(p[7]))%3==0,"twist conservation failed")
 return r
}
func unrankO(x int)[8]uint8{
 var p [8]uint8;s:=0
 for i:=6;i>=0;i--{p[i]=uint8(x%3);s+=x%3;x/=3}
 p[7]=uint8((3-s%3)%3)
 return p
}
func cornerRank(k Key)int{
 var p,o [8]uint8
 var seen [8]bool
 for i:=0;i<8;i++{
 site:=k[i];dest:=int(siteSlot[site])
 must(dest>=0,"missing corner marker site");must(!seen[dest],"two corners share place")
 seen[dest]=true;p[dest]=uint8(i);o[dest]=uint8(siteOri[site])
 }
 return rankP(p)*2187+rankO(o)
}
func initial()Key{var p Key;for i:=range p{p[i]=marks[i]};return p}
func turn(k Key,a int)Key{for i,v:=range k{k[i]=moveSite[a][v]};return k}
func cornersStep(r uint32,a int)uint32{return uint32(pt[a][r/2187])*2187+uint32(ot[a][r%2187])}
func edge(k Key)EK{var e EK;copy(e[:],k[8:]);return e}
func normLegal(last,a int)bool{
 if last<0{return true}
 f,g:=last/3,a/3
 return f!=g&&!(f>=3&&f-3==g)
}
func desc(last,remaining int)uint64{
 if remaining==0{return 1}
 if counts[last+1][remaining]!=0{return counts[last+1][remaining]}
 n:=uint64(1)
 for a:=0;a<18;a++{if normLegal(last,a){n+=desc(a,remaining-1)}}
 counts[last+1][remaining]=n
 return n
}
func b6goal()(map[Key]struct{},map[EK]struct{}){
 stamp:=time.Now()
 g:=make(map[Key]struct{},8400000)
 q:=make([]Key,1,8400087)
 q[0]=initial();g[q[0]]=struct{}{}
 begin:=0;levels:=[7]int{}
 for d:=0;d<=6;d++{
 end:=len(q);levels[d]=end-begin
 if d<6{
 for i:=begin;i<end;i++{
 v:=q[i]
 for a:=0;a<18;a++{
 w:=turn(v,a)
 if _,exists:=g[w];!exists{g[w]=struct{}{};q=append(q,w)}
 }
 }
 }
 begin=end
 }
 must(len(g)==8240087,"independent full goal count mismatch")
 must(levels==[7]int{1,18,243,3240,43239,574908,7618438},"independent goal layer mismatch")
 e:=make(map[EK]struct{},7800000)
 for _,v:=range q{e[edge(v)]=struct{}{}}
 must(len(e)==7672278,"independent E6 projection mismatch")
 q=nil;runtime.GC()
 fmt.Println("GO_INDEPENDENT_FULL_GOAL_B6_PASS",len(g),"E6",len(e),"SECONDS",time.Since(stamp).Seconds())
 return g,e
}
func c8goal()[]uint8{
 stamp:=time.Now()
 const size=40320*2187
 d:=make([]uint8,size)
 for i:=range d{d[i]=255}
 q:=make([]uint32,1,27600000)
 q[0]=0;d[0]=0;hist:=[9]int{}
 for i:=0;i<len(q);i++{
 r:=q[i];dep:=d[r]
 if dep>8{panic("C8 state depth overflow")}
 hist[dep]++
 if dep==8{continue}
 for a:=0;a<18;a++{
 w:=cornersStep(r,a)
 if d[w]==255{d[w]=dep+1;q=append(q,w)}
 }
 }
 must(len(q)==27583872,"C8 independent count mismatch")
 must(hist==[9]int{1,18,243,2874,28000,205416,1168516,5402628,20776176},"C8 independent histogram mismatch")
 q=nil;runtime.GC()
 fmt.Println("GO_INDEPENDENT_CORNER_C8_PASS",len(d),hist,"SECONDS",time.Since(stamp).Seconds())
 return d
}
func main(){
 started:=time.Now()
 geometry()
 scr:=[20]int{5,17,7,10,7,13,4,2,7,13,10,16,9,6,14,4,15,1,7,4}
 word:=[18]int{6,0,6,11,5,8,14,8,11,12,15,13,7,1,13,0,8,4}
 ss:=initial()
 for _,a:=range scr{ss=turn(ss,a)}
 valid:=ss
 for _,a:=range word{valid=turn(valid,a)}
 must(valid==initial(),"real source witness incorrect")
 fmt.Println("GO_SOURCE_FIXED_PHYSICAL_18HTM_WITNESS_PASS")
 c:=c8goal();g,e:=b6goal()
 root:=14
 if len(os.Args)>1{r,err:=strconv.Atoi(os.Args[1]);must(err==nil,"root arg error");root=r}
 must(root>=0&&root<18,"root out of range")
 child:=-1
 if len(os.Args)>2{z,err:=strconv.Atoi(os.Args[2]);must(err==nil,"child arg error");child=z}
 if child>=0{must(normLegal(root,child),"child not allowed")}
 if _,ok:=g[ss];ok{panic("source already in B6")}
 r0:=turn(ss,root)
 c0:=cornersStep(uint32(cornerRank(ss)),root)
 if _,ok:=g[r0];ok{panic("short solution")}
 fmt.Println("GO_SOURCE_CORNER_LEVEL",c[cornerRank(ss)],"START_ROOT",root,"CHILD",child)
 var visits,omits,hit,full,e6,c8,c7,c6 uint64
 var walk func(last,depth int,st Key,rank uint32)
 walk=func(last,depth int,st Key,rank uint32){
 visits++
 remaining:=10-depth
 if depth>=8{
 v:=c[rank];limit:=6+remaining
 if int(v)>limit{
 omits+=desc(last,remaining)-1
 switch depth{
 case 8:c8++
 case 9:c7++
 case 10:c6++
 }
 return
 }
 }
 if depth==10{
 if _,ok:=e[edge(st)];!ok{e6++;return}
 full++
 if _,ok:=g[st];ok{hit++;fmt.Println("GO_REAL_PHYSICAL_MEET root",root)}
 }else{
 for a:=0;a<18;a++{
 if normLegal(last,a){walk(a,depth+1,turn(st,a),cornersStep(rank,a))}
 }
 }
 }
 jobs:=0
 for a:=0;a<18;a++{
 if normLegal(root,a)&&(child<0||child==a){
 jobs++
 beforeV,beforeO,beforeF:=visits,omits,full
 walk(a,2,turn(r0,a),cornersStep(c0,a))
 exp:=desc(a,8)
 fmt.Printf("GO_SECOND_CHILD root=%d second=%d visits=%d omit=%d full=%d hit=%d total=%d expected=%d\n",root,a,visits-beforeV,omits-beforeO,full-beforeF,hit,(visits-beforeV)+(omits-beforeO),exp)
 must((visits-beforeV)+(omits-beforeO)==exp,"child grammar discrepancy")
 }
 }
 if child<0{visits++}
 exp:=desc(root,9)
 if child>=0{exp=desc(child,8)}
 must(visits+omits==exp,"whole root grammar discrepancy")
 must(hit==0,"physical counterexample found")
 fmt.Printf("GO_ROOT_RESULT root=%d child=%d jobs=%d visits=%d omitted=%d hit=%d full=%d e6=%d corner8=%d corner7=%d corner6=%d virtual=%d seconds=%.2f\n",root,child,jobs,visits,omits,hit,full,e6,c8,c7,c6,exp,time.Since(started).Seconds())
 var m runtime.MemStats
 runtime.ReadMemStats(&m)
 fmt.Printf("GO_MEMORY_ALLOC=%d GO_HEAP_SYS=%d\n",m.Alloc,m.HeapSys)
}
