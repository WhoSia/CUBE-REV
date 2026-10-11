package main
// P3-R1B independent Go exact 62-real-cubie face-query signature policy re-analysis.
// Original real facelets are externally frozen by P3-R1A original sticker oracle.
// Model ideal 9-color face observations, NOT an actual timed human glance.
import (
 "encoding/csv"
 "fmt"
 "math/bits"
 "os"
 "strconv"
 "strings"
)
const N=62
const Faces="URFDLB"
type Sample struct { f [6]string }
type Key struct { mask uint64; used uint8; q uint8 }
var states [N]Sample
var memo=map[Key]int{}
func check(ok bool,msg string){if !ok{panic(msg)}}
func classes(mask uint64, face int) []uint64 {
 out:=map[string]uint64{}
 for i:=0;i<N;i++ {if mask&(uint64(1)<<uint(i))!=0 {s:=states[i].f[face];out[s]|=uint64(1)<<uint(i)}}
 result:=make([]uint64,0,len(out))
 for _,v:=range out {result=append(result,v)}
 return result
}
func leaves(mask uint64,used uint8,q uint8)int{
 if bits.OnesCount64(mask)<=1||q==0{return 1}
 k:=Key{mask,used,q}
 if v,ok:=memo[k];ok{return v}
 best:=1
 for f:=0;f<6;f++{
  if used&(1<<uint(f))!=0{continue}
  parts:=classes(mask,f);if len(parts)<2{continue}
  sum:=0
  for _,part:=range parts{sum+=leaves(part,used|(1<<uint(f)),q-1)}
  if sum>best{best=sum}
 }
 check(best<=bits.OnesCount64(mask),"leaf overflow")
 memo[k]=best;return best
}
func main(){
 f,err:=os.Open("data/cuberev-023/p3_r1b_real_62_physical_face9_cubie_fixture.csv");if err!=nil{panic(err)};defer f.Close()
 r:=csv.NewReader(f);records,err:=r.ReadAll();if err!=nil{panic(err)}
 check(len(records)==N+1,"62 rows")
 check(strings.Join(records[0],",")=="index,U,R,F,D,L,B,source_HTM,cubie_sha256","header")
 signatures:=map[string]bool{};stateIds:=map[string]bool{}
 for i:=0;i<N;i++{
  v:=records[i+1];check(len(v)==9,"width")
  idx,e:=strconv.Atoi(v[0]);check(e==nil&&idx==i,"idx")
  depth,e:=strconv.Atoi(v[7]);check(e==nil&&depth>=0&&depth<=5,"depth")
  check(len(v[8])==64&&!stateIds[v[8]],"cubie digest");stateIds[v[8]]=true
  colorCount:=map[byte]int{}
  for face:=0;face<6;face++ {
   x:=v[face+1];check(len(x)==9,"face9")
   states[i].f[face]=x
   for j:=0;j<9;j++{check(strings.ContainsRune(Faces,rune(x[j])),"not a cube face color");colorCount[x[j]]++}
  }
  for j:=0;j<6;j++{check(colorCount[Faces[j]]==9,"whole cube nine stickers per color")}
  id:=strings.Join(v[1:7],"");check(!signatures[id],"full 6 face identity collision");signatures[id]=true
 }
 var fixed [7]int
 minFixed:=7;bestFixed:=[]string{}
 for mask:=0;mask<64;mask++{
  n:=bits.OnesCount(uint(mask));parts:=map[string]bool{}
  for i:=0;i<N;i++{
   var b strings.Builder
   for f:=0;f<6;f++{if mask&(1<<uint(f))!=0{b.WriteString(states[i].f[f])}else{b.WriteByte('?')}}
   parts[b.String()]=true
  }
  sz:=len(parts);if sz>fixed[n]{fixed[n]=sz}
  if sz==N{
   names:="";for f:=0;f<6;f++{if mask&(1<<uint(f))!=0{names+=Faces[f:f+1]}}
   if n<minFixed{minFixed=n;bestFixed=[]string{names}}else if n==minFixed{bestFixed=append(bestFixed,names)}
  }
 }
 mask:=(uint64(1)<<N)-1
 adaptive:=make([]int,7)
 minAdapt:=-1
 for q:=0;q<=6;q++{
  adaptive[q]=leaves(mask,0,uint8(q))
  if minAdapt==-1&&adaptive[q]==N{minAdapt=q}
  check(adaptive[q]>=fixed[q],"fixed worse than adaptive")
 }
 check(minFixed==4&&minAdapt==4,"minimum exact physical face budget")
 check(fmt.Sprint(bestFixed)=="[URFB RFDB UFLB FDLB]","fixed optimal face sets")
 check(fmt.Sprint(fixed)=="[1 12 38 50 62 62 62]","all fixed face partitions")
 check(fmt.Sprint(adaptive)=="[1 12 42 58 62 62 62]","adaptive dynamic frontier")
 fmt.Printf("CUBE_REV_023_P3_R1B_STATES=62 CORNER_WORDS=1 FULL_WORDS=62 ADAPTIVE_MIN=%d FIXED_MIN=%d ADAPTIVE_FRONTIER=%s FIXED_FRONTIER=%s BEST_FIXED=%s SOURCE=ORIGINAL_CUBIE_STICKERS HUMAN_COGNITION=NOT_MEASURED\n",
  minAdapt,minFixed,strings.Trim(strings.ReplaceAll(fmt.Sprint(adaptive)," ","/"),"[]"),strings.Trim(strings.ReplaceAll(fmt.Sprint(fixed)," ","/"),"[]"),strings.Join(bestFixed,";"))
}
