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
func main() {
 if len(os.Args)!=3 {fail("usage: auditor P0R5.log P0R6.log")}
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
