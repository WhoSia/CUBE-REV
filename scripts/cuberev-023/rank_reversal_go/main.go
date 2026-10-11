package main
// CUBE-REV P3-R0: independently type-check the EXACT SOURCE original-cubie R6 receipt.
// Never import/assume a computation of all-18-HTM child distances.
import (
 "bufio"
 "fmt"
 "os"
 "strconv"
 "strings"
)
func must(x bool, message string) { if !x { panic(message) } }
func main(){
 path:="data/cuberev-023/p3_r0_source_matched_R6_real_PDB_10_action_census.csv"
 f,e:=os.Open(path);if e!=nil{panic(e)};defer f.Close()
 scan:=bufio.NewScanner(f);must(scan.Scan(),"header")
 must(scan.Text()=="move,main_d,alt_d,main_h,alt_h,main_corner,alt_corner,main_edge,alt_edge","schema")
 n,reverse,strictBoth:=0,0,0
 minGap,maxGap:=100,-100
 var sumMain,sumAlt,sumMainH,sumAltH int
 moves:=map[string]bool{}
 for scan.Scan(){
  fields:=strings.Split(scan.Text(),",");must(len(fields)==9,"width")
  name:=fields[0];must(!moves[name],"duplicate move");moves[name]=true
  vals:=make([]int,8)
  for i:=1;i<9;i++{v,err:=strconv.Atoi(fields[i]);if err!=nil{panic(err)};vals[i-1]=v}
  dm,da,hm,ha,cm,ca,em,ea:=vals[0],vals[1],vals[2],vals[3],vals[4],vals[5],vals[6],vals[7]
  must(hm==max(cm,em)&&ha==max(ca,ea),"joint PDB")
  must(hm<=dm&&ha<=da,"not admissible")
  must(cm>=ca&&em>ea&&ha<hm,"componentwise reversed")
  must(da>dm,"true physical stage rank opposite to both PDBs")
  if cm>ca&&em>ea{strictBoth++}
  if ha<hm&&da>dm{reverse++}
  gap:=1+da-dm;must(gap>=2&&gap<=5,"wrong actual raw source cost gap")
  if gap<minGap{minGap=gap};if gap>maxGap{maxGap=gap}
  sumMain+=dm;sumAlt+=da;sumMainH+=hm;sumAltH+=ha
  n++
 }
 if e:=scan.Err();e!=nil{panic(e)}
 must(n==10&&reverse==10,"all ten actual one-step DR physical interventions")
 must(moves["U"]&&moves["U2"]&&moves["U'"]&&moves["D"]&&moves["D2"]&&moves["D'"]&&moves["R2"]&&moves["L2"]&&moves["F2"]&&moves["B2"],"DR action coverage")
 fmt.Printf("CUBE_REV_023_P3_R0_ROWS=%d REVERSE=%d STRICT_BOTH=%d RAW_GAP_MIN=%d RAW_GAP_MAX=%d MAIN_D_SUM=%d ALT_D_SUM=%d MAIN_H_SUM=%d ALT_H_SUM=%d ALL18_CHILD_EXACT=NOT_COMPUTED HUMAN_COGNITION=NOT_IDENTIFIED\n",n,reverse,strictBoth,minGap,maxGap,sumMain,sumAlt,sumMainH,sumAltH)
}
