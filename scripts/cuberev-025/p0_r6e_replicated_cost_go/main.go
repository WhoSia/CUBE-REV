// P0-R6E replicated same-runner D/E/E/D x2 experimental cost court.
// Preserve negative results: this program requires equivalent FULL original
// physical B6/B7 certificates, but NEVER requires E to be faster than D.
package main
import (
 "fmt"
 "os"
 "path/filepath"
 "strconv"
 "strings"
 "sort"
 "math"
)
type receipt struct { variant string; wall float64; rss float64; visits,skipped,pairs uint64 }
func fail(msg string){fmt.Fprintln(os.Stderr,"R6E_REPLICATED_FAIL",msg);os.Exit(2)}
func line(s,p string)string {
 for _,v:=range strings.Split(s,"\n"){
  v=strings.TrimSpace(v)
  if strings.HasPrefix(v,p+" "){return v}
 }
 fail("missing receipt line "+p);return ""
}
func field(s,k string)string{
 w:=strings.Fields(s)
 for i:=0;i+1<len(w);i++{if w[i]==k{return w[i+1]}}
 fail("field missing "+k);return ""
}
func integer(s,k string)uint64{
 x,err:=strconv.ParseUint(field(s,k),10,64)
 if err!=nil{fail("invalid integer "+k)}
 return x
}
func number(s,k string)float64{
 x,err:=strconv.ParseFloat(field(s,k),64)
 if err!=nil||math.IsNaN(x)||math.IsInf(x,0)||x<=0{fail("invalid positive measured float "+k)}
 return x
}
func read(path,variant string)receipt {
 b,err:=os.ReadFile(path);if err!=nil{fail("read "+path+": "+err.Error())}
 s:=string(b)
 p:="P0R6D_";visit:="ACTUAL_VISITS";skips:="SKIPPED_CANONICAL_CALLS"
 if variant=="E"{p="P0R6E_"}
 g:=line(s,p+"GOAL_FULL")
 c:=line(s,p+"EXACT_COVER")
 if integer(g,p+"GOAL_FULL")!=8240087||integer(g,"CORNER6")!=1405068||
 integer(c,"BASELINE")!=120213368||integer(c,"FULL_HITS")!=0||
 field(c,"COMPLETE")!="1" {fail("not an original complete source B7 vs goal B6 court: "+path)}
 n:=integer(c,visit);omit:=integer(c,skips)
 if n+omit!=120213368{fail("source proof equation invalid "+path)}
 if variant=="D"{
  if field(line(s,"P0R6D_GLOBAL_LOWER"),"ORDERED_TWO_MOVE_PREDICATE_SOUND")!="1"{fail("D proof flag invalid")}
 } else {
  if field(line(s,"P0R6E_GLOBAL_LOWER"),"SOURCE_RADIUS")!="7"{fail("E source radius invalid")}
  if integer(line(s,"P0R6E_PACKED_PHYSICAL_TURN_REGRESSION"),"CASES")!=4608{fail("E packed physics not cross-checked")}
  if integer(c,"AVOIDED_WHOLE_CUBE_SECOND_MOVES")!=integer(c,"ORDERED_PAIR_CHECKS"){fail("E cost elimination invalid")}
 }
 t:=line(s,"BENCH_R6E_CROSS_WALL_SECONDS")
 if field(t,"VARIANT")!=variant{fail("expected exact variant "+variant+" in "+path)}
 return receipt{variant,number(t,"BENCH_R6E_CROSS_WALL_SECONDS"),number(t,"PEAK_RSS_KIB"),n,omit,integer(c,"ORDERED_PAIR_CHECKS")}
}
func mean(xs []float64)float64{var n float64;for _,x:=range xs{n+=x};return n/float64(len(xs))}
func median(xs []float64)float64{
 c:=append([]float64(nil),xs...);sort.Float64s(c)
 return (c[(len(c)-1)/2]+c[len(c)/2])/2
}
func main(){
 if len(os.Args)!=2{fail("usage: checker directory_of_D1_E1_E2_D2_D3_E3_E4_D4_logs")}
 order:=[]struct{label,name string}{
  {"D","D1"},{"E","E1"},{"E","E2"},{"D","D2"},
  {"D","D3"},{"E","E3"},{"E","E4"},{"D","D4"},
 }
 var d,e []receipt
 for _,entry:=range order {
  r:=read(filepath.Join(os.Args[1],entry.name+".log"),entry.label)
  if r.visits!=674679||r.skipped!=119538689||r.pairs!=7462988{
   fail("original source D/E decision drift in "+entry.name)
  }
  if entry.label=="D"{d=append(d,r)}else{e=append(e,r)}
  fmt.Printf("R6E_CROSS_OBSERVATION VARIANT %s SLOT %s WALL_SECONDS %.3f RSS_KIB %.0f VISITS %d SKIPPED %d PAIRS %d\n",entry.label,entry.name,r.wall,r.rss,r.visits,r.skipped,r.pairs)
 }
 var dw,ew,dr,er []float64
 for i:=range d{
  dw=append(dw,d[i].wall);ew=append(ew,e[i].wall)
  dr=append(dr,d[i].rss);er=append(er,e[i].rss)
 }
 fmt.Printf("R6E_CROSS_AUDIT_SUCCESS REPETITIONS_D 4 REPETITIONS_E 4 ORIGINAL_EXACT_B7 1 IDENTICAL_VISITS 674679 IDENTICAL_SKIPPED 119538689 IDENTICAL_ORDERED_PAIRS 7462988 D_MEAN_WALL %.4f E_MEAN_WALL %.4f E_VS_D_MEAN_WALL_PERCENT %.4f D_MEDIAN_WALL %.4f E_MEDIAN_WALL %.4f E_VS_D_MEDIAN_WALL_PERCENT %.4f D_MEAN_RSS_KIB %.1f E_MEAN_RSS_KIB %.1f E_VS_D_MEAN_RSS_PERCENT %.4f\n",
  mean(dw),mean(ew),100*(mean(ew)/mean(dw)-1),
  median(dw),median(ew),100*(median(ew)/median(dw)-1),
  mean(dr),mean(er),100*(mean(er)/mean(dr)-1))
}
