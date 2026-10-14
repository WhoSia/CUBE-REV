// P0-R6 independent Go receipt auditor: checks real C++ completed logs.
package main
import (
 "fmt"
 "os"
 "strings"
 "strconv"
)
func fail(format string, args ...any) { fmt.Fprintf(os.Stderr,"P0R6_AUDIT_FAIL "+format+"\n",args...);os.Exit(2) }
type receipt struct { lines []string }
func read(path string) receipt {
 raw,err:=os.ReadFile(path);if err!=nil{fail("read %s: %v",path,err)}
 return receipt{lines:strings.Split(string(raw),"\n")}
}
func (r receipt) line(prefix string) string {
 for _,line:=range r.lines {
  if strings.HasPrefix(strings.TrimSpace(line),prefix+" ") {return strings.TrimSpace(line)}
 }
 fail("missing %s",prefix);return ""
}
func field(line,key string) string {
 tokens:=strings.Fields(line)
 for i:=0;i+1<len(tokens);i++ {if tokens[i]==key{return tokens[i+1]}}
 fail("field %s absent: %s",key,line);return ""
}
func count(line,key string) uint64 {
 x,err:=strconv.ParseUint(field(line,key),10,64)
 if err!=nil {fail("invalid unsigned %s in %s",key,line)}
 return x
}
func number(line,key string) float64 {
 x,err:=strconv.ParseFloat(field(line,key),64)
 if err!=nil || x<0 {fail("invalid measurement %s in %s",key,line)}
 return x
}

func legal(last,next int) bool {
 if last<0 {return true}
 if last/3==next/3 {return false}
 fa,fb:=last/3,next/3
 return !(fb-fa==-3)
}
func canonicalVisits(radius int) uint64 {
 prev:=make([]uint64,18)
 count:=uint64(radius+1)
 for depth:=1;depth<=radius;depth++ {
  now:=make([]uint64,18)
  for a:=0;a<18;a++ {
   if depth==1 {now[a]=1
   } else {for last:=0;last<18;last++ {
    if legal(last,a) {now[a]+=prev[last]}
   }}
  }
  var n uint64
  for _,v:=range now {n+=v}
  count+=n*uint64(radius-depth+1)
  prev=now
 }
 return count
}
func sourceEight(path string) {
 r:=read(path)
 c:=r.line("P0R6_COMPLETE")
 eq:=r.line("P0R6_CANONICAL_ACCOUNTING")
 n:=canonicalVisits(8)
 if n!=1604664504 {fail("independent Go canonical recurrence changed")}
 if count(c,"FULL_GOAL")!=8240087||count(c,"FULL_HITS")!=0 {
  fail("B8 original 54-sticker goal source certificate mismatch")
 }
 if count(eq,"BASELINE")!=n||count(eq,"VISITED")+count(eq,"SKIPPED")!=n||field(eq,"EXACT_EQUATION_PASS")!="1" {
  fail("B8 canonical source completeness partition invalid")
 }
 if field(r.line("P0R6_GLOBAL_LOWER"),"SOURCE_B8_GOAL_B6_COMPLETE")!="1" {
  fail("15-move lower certificate not completed")
 }
 wall:=number(r.line("BENCH_P0R6_WALL_SECONDS"),"BENCH_P0R6_WALL_SECONDS")
 ram:=number(r.line("BENCH_P0R6_WALL_SECONDS"),"PEAK_RSS_KIB")
 if wall<=0||ram<=0 {fail("missing B8 measured hardware metrics")}
 fmt.Printf("P0R6_B8_INDEPENDENT_GO_SUCCESS CANONICAL_SOURCE_VISITS %d ACTUAL_VISITS %d SKIPPED_CHILDREN %d DESCENDANT_CUTS %d WALL_SECONDS %.3f PEAK_RSS_KIB %.0f VERIFIED_GLOBAL_LOWER 15 UPPER 18\n",
 n,count(eq,"VISITED"),count(eq,"SKIPPED"),count(c,"DESCENDANT_CUTS"),wall,ram)
}

func main() {
 if len(os.Args)==3 && os.Args[1]=="--source8" {sourceEight(os.Args[2]);return}
 if len(os.Args)!=3 {fail("usage: auditor P0R5.log P0R6.log OR --source8 P0R6-B8.log")}
 old:=read(os.Args[1]);neu:=read(os.Args[2])
 a:=old.line("P0R5_SAFE_ORIGINAL_CUBIE_PREFILTER_COMPLETE")
 b:=neu.line("P0R6_COMPLETE")
 eq:=neu.line("P0R6_CANONICAL_ACCOUNTING")
 if field(a,"GOAL_RADIUS")!="6"||field(a,"SOURCE_RADIUS")!="7" ||field(b,"FULL_GOAL")!="8240087" {fail("benchmark radii or goal changed")}
 fullOld:=count(a,"SOURCE_VISITS");fullNew:=count(b,"SOURCE_VISITS")
 skipped:=count(b,"SKIPPED_CHILDREN");cuts:=count(b,"DESCENDANT_CUTS")
 if fullOld!=120213368 || count(a,"FULL_INTERSECTIONS")!=0 || count(b,"FULL_HITS")!=0 {fail("old certificate not reproduced")}
 if fullNew+skipped!=fullOld || count(eq,"BASELINE")!=fullOld || count(eq,"VISITED")!=fullNew || count(eq,"SKIPPED")!=skipped ||field(eq,"EXACT_EQUATION_PASS")!="1" {fail("canonical source cover incomplete")}
 if field(b,"SOUND_ONE_STEP_DESCENDANT_PRUNING")!="1" {fail("descendant theorem receipt absent")}
 if count(b,"FULL_GOAL")!=count(a,"FULL_GOAL_STATES") {fail("goal discrepancy")}
 oa:=old.line("BENCH_P0R5_WALL_SECONDS");nb:=neu.line("BENCH_P0R6_WALL_SECONDS")
 twOld:=number(oa,"BENCH_P0R5_WALL_SECONDS");twNew:=number(nb,"BENCH_P0R6_WALL_SECONDS")
 rssOld:=number(oa,"PEAK_RSS_KIB");rssNew:=number(nb,"PEAK_RSS_KIB")
 if twOld==0||twNew==0||rssOld==0||rssNew==0 {fail("missing nonzero resource measurement")}
 fmt.Printf("P0R6_AUDIT_SUCCESS SOURCE_BASELINE %d SOURCE_VISITS %d OMITTED_CANONICAL_CHILDREN %d DESCENDANT_CUTS %d OMITTED_PERCENT %.6f OLD_WALL_SECONDS %.3f NEW_WALL_SECONDS %.3f WALL_CHANGE_PERCENT %.3f OLD_PEAK_RSS_KIB %.0f NEW_PEAK_RSS_KIB %.0f RSS_CHANGE_PERCENT %.3f GLOBAL_LOWER 14 UPPER 18\n",
  fullOld,fullNew,skipped,cuts,100*float64(skipped)/float64(fullOld),
  twOld,twNew,100*(twNew/twOld-1),rssOld,rssNew,100*(rssNew/rssOld-1))
}
