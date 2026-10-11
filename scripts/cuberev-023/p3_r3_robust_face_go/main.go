package main

// P3-R3 exact 62-state six-face error geometry.
// Independently compute one-error capacity via minimum vertex cover.
// Source is the existing P3-R1B frozen real physical-sticker fixture.
import (
 "encoding/csv"
 "fmt"
 "math/bits"
 "os"
 "strconv"
 "strings"
)
const N=62
const Fixture="data/cuberev-023/p3_r1b_real_62_physical_face9_cubie_fixture.csv"
var obs [N][6]string
func must(b bool,msg string){if !b{panic(msg)}}
func dist(i,j,mask int)int{n:=0;for f:=0;f<6;f++{if mask&(1<<f)!=0&&obs[i][f]!=obs[j][f]{n++}};return n}
func cover(adj []uint64)int{
 memo:=map[uint64]int{}
 var solve func(uint64)int
 solve=func(mask uint64)int{
  if v,ok:=memo[mask];ok{return v}
  pivot,degree:=-1,0
  for i:=range adj{if mask&(uint64(1)<<i)!=0{d:=bits.OnesCount64(adj[i]&mask);if d>degree{degree=d;pivot=i}}}
  if pivot<0{memo[mask]=0;return 0}
  neighbor:=bits.TrailingZeros64(adj[pivot]&mask)
  a:=solve(mask &^ (uint64(1)<<pivot))
  b:=solve(mask &^ (uint64(1)<<neighbor))
  if b<a{a=b};memo[mask]=1+a;return 1+a
 }
 return solve((uint64(1)<<len(adj))-1)
}
func main(){
 file,e:=os.Open(Fixture);if e!=nil{panic(e)};defer file.Close()
 rows,e:=csv.NewReader(file).ReadAll();if e!=nil{panic(e)}
 must(len(rows)==N+1,"row count")
 must(strings.Join(rows[0],",")=="index,U,R,F,D,L,B,source_HTM,cubie_sha256","header")
 uniq:=map[string]bool{}
 for i:=0;i<N;i++{
  r:=rows[i+1];must(len(r)==9,"row width")
  idx,e:=strconv.Atoi(r[0]);must(e==nil&&idx==i,"index")
  depth,e:=strconv.Atoi(r[7]);must(e==nil&&depth>=0&&depth<=5,"depth")
  must(len(r[8])==64&&!uniq[r[8]],"cubie key");uniq[r[8]]=true
  for f:=0;f<6;f++{must(len(r[1+f])==9,"9 stickers");obs[i][f]=r[1+f]}
 }
 var hist[7]int;var best[7]int;erasureMasks:=[]int{};adj:=make([]uint64,N)
 for mask:=0;mask<64;mask++{
  minD:=7
  for i:=0;i<N;i++{for j:=i+1;j<N;j++{
   d:=dist(i,j,mask);if d<minD{minD=d}
   if mask==63{hist[d]++;if d<=2{adj[i]|=uint64(1)<<j;adj[j]|=uint64(1)<<i}}
  }}
  q:=bits.OnesCount(uint(mask));if minD>best[q]{best[q]=minD}
  if minD>=2{erasureMasks=append(erasureMasks,mask)}
 }
 must(hist==[7]int{0,0,142,216,390,400,743},"histogram")
 must(best==[7]int{0,0,0,0,1,1,2},"subset distances")
 must(len(erasureMasks)==1&&erasureMasks[0]==63,"fixed erasure masks")
 unseen:=(uint64(1)<<N)-1;ncover:=0;sizes:=[]int{}
 for unseen!=0{
  root:=bits.TrailingZeros64(unseen);group:=uint64(1)<<root
  for{expanded:=group;for i:=0;i<N;i++{if group&(uint64(1)<<i)!=0{expanded|=adj[i]}};if expanded==group{break};group=expanded}
  unseen &^=group
  vertices:=[]int{};for i:=0;i<N;i++{if group&(uint64(1)<<i)!=0{vertices=append(vertices,i)}}
  must(len(vertices)<=23,"unexpected component size")
  local:=make([]uint64,len(vertices))
  for i,u:=range vertices{for j,v:=range vertices{if adj[u]&(uint64(1)<<v)!=0{local[i]|=uint64(1)<<j}}}
  ncover+=cover(local);sizes=append(sizes,len(vertices))
 }
 must(N-ncover==26,"exact maximum robust subcode")
 fmt.Printf("P3R3 GO STATES=62 PAIRS=1891 HIST=%v BEST_MIN_DISTANCE=%v ONE_ERASURE_MASKS=%v ONE_ERROR_CORRECTABLE_CAPACITY=%d COMPONENTS=%v PROOF=EXHAUSTIVE_VERTEX_COVER\n",hist,best,erasureMasks,N-ncover,sizes)
}
