// P12-P3-R2: independent true geometric incidence audit.
// Uses the REAL 288-byte P9 native 18HTM CP/CO snapshots rather than
// inferring face structure from the P12 observed duplicate-fiber masks.
package main
import (
 "bufio"
 "encoding/hex"
 "fmt"
 "math/bits"
 "os"
 "strconv"
 "strings"
)
func fail(s string){fmt.Fprintln(os.Stderr,"P12_P3_R2_FACE_FAIL",s);os.Exit(2)}
func maskHex(n uint8)string{return fmt.Sprintf("%02x",n)}
func main(){
 if len(os.Args)!=3{fail("usage: original-18-corner-turns.bin P12-P3-exact-geometry.log")}
 turns,e:=os.ReadFile(os.Args[1]);if e!=nil||len(turns)!=288{fail("original 18 HTM corner turns missing or corrupt length")}
 var faces [6]uint8
 faceNames:=[]string{"U","R","F","D","L","B"}
 for f:=0;f<6;f++{
  var mask uint8
  var seen uint8
  for i:=0;i<8;i++{
   j:=turns[(f*3)*16+i]
   if j>=8||seen&(1<<j)!=0{fail("physical turn is not a CP permutation")}
   seen|=1<<j
   if int(j)!=i{mask|=1<<uint(i)}
  }
  if seen!=255||bits.OnesCount8(mask)!=4{fail("physical face does not move exactly four corners")}
  faces[f]=mask
  fmt.Printf("P12_P3_R2_TRUE_PHYSICAL_FACE FACE %s MASK %02x\n",faceNames[f],mask)
 }
 faceMask:=map[uint8]bool{}
 for _,m:=range faces{if faceMask[m]{fail("duplicate original face position support")};faceMask[m]=true}
 var edgeMask map[uint8]bool=make(map[uint8]bool)
 var adjacent [8][8]bool
 for i:=0;i<8;i++{
  incident:=0
  for _,m:=range faces{if m&(1<<uint(i))!=0{incident++}}
  if incident!=3{fail("physical corner position not incident to three faces")}
  for j:=i+1;j<8;j++{
   common:=0
   for _,m:=range faces{if m&(1<<uint(i))!=0&&m&(1<<uint(j))!=0{common++}}
   if common==2{
    adjacent[i][j]=true;adjacent[j][i]=true
    fixed:=uint8((1<<uint(i))|(1<<uint(j)))
    edgeMask[^fixed]=true
    fmt.Printf("P12_P3_R2_TRUE_EDGE_ENDPOINTS POSITIONS %d %d MOVED_COMPLEMENT_MASK %02x\n",i,j,^fixed)
   }else if common>2{fail("invalid distinct position face co-incidence")}
  }
 }
 if len(edgeMask)!=12{fail("physical 3-cube incidence not exactly 12 edges")}
 f,e:=os.Open(os.Args[2]);if e!=nil{fail(e.Error())};defer f.Close()
 scanner:=bufio.NewScanner(f)
 enriched:=make(map[uint8]int)
 low:=make(map[uint8]int)
 six:=make(map[uint8]int)
 for scanner.Scan(){
  s:=scanner.Text()
  if !strings.HasPrefix(s,"P12_P3_EQUAL_SUPPORT_MASK KEY "){continue}
  var fiber int
  var cycle string
  var maskstr string
  var count int
  tok:=strings.Fields(s)
  if len(tok)!=7||tok[1]!="KEY"||tok[5]!="PAIRS"{fail("malformed support ledger line")}
  for _,v:=range tok{
   if strings.HasPrefix(v,"fiber="){fiber,_=strconv.Atoi(strings.TrimPrefix(v,"fiber="))}
   if strings.HasPrefix(v,"cycle="){cycle=strings.TrimPrefix(v,"cycle=")}
   if strings.HasPrefix(v,"mask="){maskstr=strings.TrimPrefix(v,"mask=")}
  }
  count,errCount:=strconv.Atoi(tok[6]);if errCount!=nil{fail("invalid support count")}
  raw,err:=hex.DecodeString(maskstr)
  if err!=nil||len(raw)!=1{fail("invalid mask hex")}
  m:=raw[0]
  if fiber==1&&cycle=="2+4"{
   if bits.OnesCount8(m)!=6||count!=16{fail("expected exact P12 6-moved support histogram")}
   if _,ok:=six[m];ok{fail("duplicated support6")}
   six[m]=count
  }else if fiber==4&&cycle=="2+2"{
   if bits.OnesCount8(m)!=4{fail("expected four support for 2+2")}
   if count==32{enriched[m]=count}else if count==8{low[m]=count}else{fail("unexpected P12 support4 weight")}
  }else{fail("unexpected fiber class in support mask ledger")}
 }
 if err:=scanner.Err();err!=nil{fail(err.Error())}
 if len(enriched)!=6||len(low)!=24||len(six)!=12{fail("support distribution differs from previous original B6")}
 // Native actual face sets are not the six enriched masks! The
 // previous R2 "six enriched masks = six faces" was falsified by CI.
 // R3 instead computes TRUE antipodal-edge unions from face incidence.
 var opposite [8]int
 for i:=0;i<8;i++ {
  match,count:=0,0
  for j:=0;j<8;j++ {
   if i==j{continue}
   shared:=0
   for _,m:=range faces{if m&(1<<uint(i))!=0&&m&(1<<uint(j))!=0{shared++}}
   if shared==0{match=j;count++}
  }
  if count!=1{fail("physical corner has not exactly one antipode")}
  opposite[i]=match
 }
 oppositeEdgeUnions:=make(map[uint8]bool)
 for i:=0;i<8;i++{for j:=i+1;j<8;j++{
  if !adjacent[i][j]{continue}
  oi,oj:=opposite[i],opposite[j]
  if oi==oj||!adjacent[oi][oj]{fail("antipode does not take edge to edge")}
  mask:=uint8((1<<uint(i))|(1<<uint(j))|(1<<uint(oi))|(1<<uint(oj)))
  if bits.OnesCount8(mask)!=4{fail("opposite edge union not four distinct corners")}
  oppositeEdgeUnions[mask]=true
 }}
 if len(oppositeEdgeUnions)!=6{fail("physical opposite-edge unions != six")}
 for m:=range oppositeEdgeUnions{
  if _,ok:=enriched[m];!ok{fail("opposite-edge union missing among 32x masks "+maskHex(m))}
  if faceMask[m]{fail("physical opposite-edge union wrongly equals a face")}
 }
 for m:=range enriched{if !oppositeEdgeUnions[m]{fail("enriched E support not opposite-edge union "+maskHex(m))}}
 for m:=range edgeMask{if _,ok:=six[m];!ok{fail("six-moved support not edge complement "+maskHex(m))}}
 for m:=range six{if !edgeMask[m]{fail("extra edge-complement support "+maskHex(m))}}
 // The remaining 24 observed four-vertex supports must induce a
 // length-three path (4 vertices, degree multiset 1,1,2,2).
 for m,n:=range low{
  var degree [8]int
  internalEdges:=0
  for i:=0;i<8;i++{for j:=i+1;j<8;j++{
   if adjacent[i][j]&&m&(1<<uint(i))!=0&&m&(1<<uint(j))!=0{
    internalEdges++;degree[i]++;degree[j]++
   }
  }}
  d1,d2:=0,0
  for i:=0;i<8;i++{
   if m&(1<<uint(i))==0{continue}
   if degree[i]==1{d1++}else if degree[i]==2{d2++}else{fail("nonface support is not a simple 4-vertex path "+maskHex(m))}
  }
  if internalEdges!=3||d1!=2||d2!=2{fail("observed 8x support not induced P4")}
  fmt.Printf("P12_P3_R3_TRUE_THREE_EDGE_PATH MASK %02x PAIRS %d INTERNAL_EDGES %d DEGREE1 %d DEGREE2 %d\n",m,n,internalEdges,d1,d2)
 }
 fmt.Printf("P12_P3_R3_OPPOSITE_EDGE_AND_PATH_SUPPORT_PASS ORIGINAL_FACES 6 ORIGINAL_EDGES 12 OPPOSITE_EDGE_UNIONS_AT_32 6 THREE_EDGE_PATHS_AT_8 24 MOVED_SIX_EDGE_COMPLEMENTS_AT_16 12 GLOBAL_LOWER17_CLAIMED 0\n")
}
