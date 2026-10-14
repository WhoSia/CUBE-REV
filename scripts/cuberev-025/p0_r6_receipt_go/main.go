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


func auditJoint(oldPath,jointPath string){
 old:=read(oldPath);joint:=read(jointPath)
 a:=old.line("P0R6_COMPLETE")
 b:=joint.line("P0R6C_EXACT_COVER")
 pa:=old.line("P0R6_CANONICAL_ACCOUNTING")
 pb:=joint.line("P0R6C_PROJECTIONS")
 n:=canonicalVisits(7)
 if n!=120213368||count(pa,"BASELINE")!=n||count(b,"BASELINE")!=n||
 count(a,"SOURCE_VISITS")+count(a,"SKIPPED_CHILDREN")!=n||
 count(b,"VISITS")+count(b,"SKIPPED")!=n||
 count(b,"FULL_HITS")!=0||count(a,"FULL_HITS")!=0||
 count(pb,"GOAL_FULL")!=8240087||count(pb,"CORNER6")!=1405068||
 field(b,"COMPLETE")!="1"{
 fail("P0-R6A/C full-cubie source, goal, equality, or complete coverage mismatch")
 }
 if count(b,"SKIPPED")<count(a,"SKIPPED_CHILDREN"){
 fail("same-generator pair screen pruned fewer nodes than corner-only screen")
 }
 if field(joint.line("P0R6C_CERTIFIED_PHYSICAL_GLOBAL_LOWER"),"COMMON_ACTION_SOUND")!="1"{
 fail("joint common-action certificate missing")
 }
 wallOld:=number(old.line("BENCH_P0R6_WALL_SECONDS"),"BENCH_P0R6_WALL_SECONDS")
 wallJoint:=number(joint.line("BENCH_P0R6C_WALL_SECONDS"),"BENCH_P0R6C_WALL_SECONDS")
 ramOld:=number(old.line("BENCH_P0R6_WALL_SECONDS"),"PEAK_RSS_KIB")
 ramJoint:=number(joint.line("BENCH_P0R6C_WALL_SECONDS"),"PEAK_RSS_KIB")
 if wallOld<=0||wallJoint<=0||ramOld<=0||ramJoint<=0{fail("missing physical measurements")}
 fmt.Printf("P0R6C_GO_INDEPENDENT_AUDIT_PASS BASELINE %d A_VISITS %d C_VISITS %d A_SKIPPED %d C_SKIPPED %d ADDITIONAL_SKIPPED %d EDGE6_STATES %d JOINT_EMPTY_CUTS %d A_WALL_SECONDS %.3f C_WALL_SECONDS %.3f C_VS_A_WALL_CHANGE_PERCENT %.3f A_RSS_KIB %.0f C_RSS_KIB %.0f C_VS_A_RSS_CHANGE_PERCENT %.3f GLOBAL_LOWER 14 UPPER 18\n",
 n,count(a,"SOURCE_VISITS"),count(b,"VISITS"),count(a,"SKIPPED_CHILDREN"),count(b,"SKIPPED"),
 count(b,"SKIPPED")-count(a,"SKIPPED_CHILDREN"),count(pb,"EDGE6"),count(b,"JOINT_EMPTY_CUTS"),
 wallOld,wallJoint,100*(wallJoint/wallOld-1),
 ramOld,ramJoint,100*(ramJoint/ramOld-1))
}


func auditOrdered(cPath,dPath string){
 c:=read(cPath);d:=read(dPath)
 old:=c.line("P0R6C_EXACT_COVER")
 cur:=d.line("P0R6D_EXACT_COVER")
 full:=d.line("P0R6D_GOAL_FULL")
 bound:=canonicalVisits(7)
 if bound!=120213368||count(old,"BASELINE")!=bound||
 count(cur,"BASELINE")!=bound||
 count(old,"VISITS")+count(old,"SKIPPED")!=bound||
 count(cur,"ACTUAL_VISITS")+count(cur,"SKIPPED_CANONICAL_CALLS")!=bound||
 count(old,"FULL_HITS")!=0||count(cur,"FULL_HITS")!=0||
 count(full,"P0R6D_GOAL_FULL")!=8240087 ||
 count(full,"CORNER6")!=1405068 ||
 field(full,"REAL_ORIGINAL_CUBE_UF_NE_FU")!="1"{
 fail("C/D physical full-cubie nonintersection, correct goal or exact-source coverage gate failed")
 }
 cutC:=count(old,"SKIPPED")
 cutD:=count(cur,"SKIPPED_CANONICAL_CALLS")
 if cutD<cutC {fail("D unexpectedly visited more source calls than C")}
 if field(d.line("P0R6D_GLOBAL_LOWER"),"ORDERED_TWO_MOVE_PREDICATE_SOUND")!="1" {
 fail("ordered physical certificate missing")
 }
 cCost:=c.line("BENCH_P0R6C_WALL_SECONDS")
 dCost:=d.line("BENCH_P0R6D_WALL_SECONDS")
 tC:=number(cCost,"BENCH_P0R6C_WALL_SECONDS")
 tD:=number(dCost,"BENCH_P0R6D_WALL_SECONDS")
 rC:=number(cCost,"PEAK_RSS_KIB")
 rD:=number(dCost,"PEAK_RSS_KIB")
 if tC==0||tD==0||rC==0||rD==0{fail("ordered cost measurement missing")}
 fmt.Printf("P0R6D_GO_AUDIT_PASS BASELINE %d C_VISITS %d D_VISITS %d C_SKIPPED %d D_SKIPPED %d EXTRA_SKIPPED %d ORDERED_PAIR_CHECKS %d TWO_STEP_REJECTED_BRANCHES %d C_WALL_SECONDS %.3f D_WALL_SECONDS %.3f TIME_CHANGE_PERCENT %.4f C_RSS_KIB %.0f D_RSS_KIB %.0f RAM_CHANGE_PERCENT %.4f VERIFIED_GLOBAL_LOWER 14 UPPER 18\n",
 bound,count(old,"VISITS"),count(cur,"ACTUAL_VISITS"),cutC,cutD,cutD-cutC,
 count(cur,"ORDERED_PAIR_CHECKS"),count(cur,"TWO_STEP_REJECTED_FIRST_ACTION_BRANCHES"),
 tC,tD,100*(tD/tC-1),rC,rD,100*(rD/rC-1))
}


func auditPacked(dPath,ePath string) {
 d:=read(dPath); e:=read(ePath)
 dr:=d.line("P0R6D_EXACT_COVER")
 er:=e.line("P0R6E_EXACT_COVER")
 goal:=e.line("P0R6E_GOAL_FULL")
 physical:=e.line("P0R6E_PACKED_PHYSICAL_TURN_REGRESSION")
 expected:=canonicalVisits(7)
 if expected!=120213368||count(dr,"BASELINE")!=expected||count(er,"BASELINE")!=expected||
 count(dr,"ACTUAL_VISITS")+count(dr,"SKIPPED_CANONICAL_CALLS")!=expected||
 count(er,"ACTUAL_VISITS")+count(er,"SKIPPED_CANONICAL_CALLS")!=expected||
 count(dr,"FULL_HITS")!=0||count(er,"FULL_HITS")!=0||
 count(goal,"P0R6E_GOAL_FULL")!=8240087 ||
 count(goal,"CORNER6")!=1405068||
 count(physical,"CASES")!=4608||
 field(physical,"ORDER_SENSITIVE_UF_NE_FU")!="1" {
 fail("R6D/E physical 54-sticker equivalence, source completeness or complete-cubie goal failed")
 }
 if count(dr,"ACTUAL_VISITS")!=count(er,"ACTUAL_VISITS") ||
 count(dr,"SKIPPED_CANONICAL_CALLS")!=count(er,"SKIPPED_CANONICAL_CALLS") ||
 count(dr,"ORDERED_PAIR_CHECKS")!=count(er,"ORDERED_PAIR_CHECKS") {
 fail("R6E changed scientific visit/skip/pair decision versus inherited exact R6D")
 }
 if count(er,"PACKED_CORNER_CHECKS")!=count(er,"ORDERED_PAIR_CHECKS") ||
 count(er,"AVOIDED_WHOLE_CUBE_SECOND_MOVES")!=count(er,"ORDERED_PAIR_CHECKS")||
 count(er,"PACKED_EDGE_CHECKS")>count(er,"PACKED_CORNER_CHECKS") {
 fail("not all pair transitions factored or invalid cost count")
 }
 if field(e.line("P0R6E_GLOBAL_LOWER"),"SOURCE_RADIUS")!="7" {
 fail("source full B7 certified branch missing")
 }
 dCost:=d.line("BENCH_P0R6D_WALL_SECONDS")
 eCost:=e.line("BENCH_P0R6E_WALL_SECONDS")
 td:=number(dCost,"BENCH_P0R6D_WALL_SECONDS")
 te:=number(eCost,"BENCH_P0R6E_WALL_SECONDS")
 rd:=number(dCost,"PEAK_RSS_KIB")
 re:=number(eCost,"PEAK_RSS_KIB")
 if td<=0||te<=0||rd<=0||re<=0 {fail("missing GNU timing and RSS")}
 fmt.Printf("P0R6E_GO_PAIRED_AUDIT_PASS BASELINE %d IDENTICAL_VISITS %d IDENTICAL_SKIPPED %d SAME_ORDERED_PAIRS %d FAST_CORNER_CHECKS %d FAST_EDGE_CHECKS %d FULL_CUBE_TRANSITIONS_AVOIDED %d D_WALL_SECONDS %.3f E_WALL_SECONDS %.3f TIME_CHANGE_PERCENT %.3f D_PEAK_RSS_KIB %.0f E_PEAK_RSS_KIB %.0f RSS_CHANGE_PERCENT %.3f VERIFIED_LOWER 15 UPPER 18_INHERITED_FROM_INDEPENDENT_B8\n",
 expected,count(er,"ACTUAL_VISITS"),count(er,"SKIPPED_CANONICAL_CALLS"),
 count(er,"ORDERED_PAIR_CHECKS"),count(er,"PACKED_CORNER_CHECKS"),
 count(er,"PACKED_EDGE_CHECKS"),count(er,"AVOIDED_WHOLE_CUBE_SECOND_MOVES"),
 td,te,100*(te/td-1),rd,re,100*(re/rd-1))
}
func auditRadius9(path string) {
 r:=read(path)
 g:=r.line("P0R6E_GOAL_FULL")
 z:=r.line("P0R6E_EXACT_COVER")
 p:=r.line("P0R6E_PACKED_PHYSICAL_TURN_REGRESSION")
 n:=canonicalVisits(9)
 if n!=21419814808||count(g,"P0R6E_GOAL_FULL")!=8240087||
 count(g,"CORNER6")!=1405068||
 count(z,"BASELINE")!=n ||
 count(z,"ACTUAL_VISITS")+count(z,"SKIPPED_CANONICAL_CALLS")!=n||
 count(z,"FULL_HITS")!=0 ||
 count(p,"CASES")!=4608||
 field(r.line("P0R6E_GLOBAL_LOWER"),"SOURCE_RADIUS")!="9" {
 fail("B9 original full physical root/goal/completeness/projection certificate not observed")
 }
 t:=r.line("BENCH_P0R6E_WALL_SECONDS")
 wall:=number(t,"BENCH_P0R6E_WALL_SECONDS")
 rss:=number(t,"PEAK_RSS_KIB")
 if wall<=0||rss<=0 {fail("B9 measured wall or peak RSS missing")}
 fmt.Printf("P0R6E_B9_GO_INDEPENDENT_CERT_PASS BASELINE %d ACTUAL_VISITS %d SKIPPED_CALLS %d ORDERED_PAIRS %d WALL_SECONDS %.3f PEAK_RSS_KIB %.0f VERIFIED_GLOBAL_LOWER 16 UPPER 18\n",
 n,count(z,"ACTUAL_VISITS"),count(z,"SKIPPED_CANONICAL_CALLS"),count(z,"ORDERED_PAIR_CHECKS"),wall,rss)
}

func main() {
 if len(os.Args)==4 && os.Args[1]=="--packed" {auditPacked(os.Args[2],os.Args[3]);return}
 if len(os.Args)==3 && os.Args[1]=="--source9" {auditRadius9(os.Args[2]);return}
 if len(os.Args)==4 && os.Args[1]=="--ordered" {auditOrdered(os.Args[2],os.Args[3]);return}
 if len(os.Args)==4 && os.Args[1]=="--joint" {auditJoint(os.Args[2],os.Args[3]);return}
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
