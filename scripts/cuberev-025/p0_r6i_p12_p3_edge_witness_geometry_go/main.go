// CUBE-REV 0.25 P0-R6I-P12-P3: edge-witness relation versus exact duplicate-fiber relation of the P11 B6 duplicate fibers.
// All counts are computed from the same SHA-pinned actual sorted 54-facelet-derived
// whole CP/CO/EP/EO goal, never inferred from the four known coarse counts.
// The theorem-side cycle and twist laws are necessary conditions, NOT a
// new physical shortest-distance certification.
package main

import (
 "crypto/sha256"
 "encoding/binary"
 "encoding/hex"
 "fmt"
 "io"
 "os"
 "sort"
 "strings"
 "math/bits"
 "bufio"
)

const originalGoalSHA = "82fe545bcad3537c989ec22afce9d286926ddce5f4ef9428c0307951ec2d0979"
const goalRows = 8240087
const domainHeader = "CUBE-REV-025-P8:FULL-CP-CO-EP-EO:LE64x2:v1;radius=6;count=8240087\n"

type rowKey struct { c,e uint64 }
type pairKey struct { a,b uint64 }
type cornerPair struct { first, second uint64; fiberSize int }
type firstCorner struct { corner uint64; multiplicity int }
type fineType struct {
 fiberSize, cpMoved, coMoved, plus, minus int
 cycles string
}
func fail(s string) { fmt.Fprintln(os.Stderr,"P12_FAIL",s); os.Exit(2) }
func cp(k uint64,i int) int { return int((k>>uint(3*i))&7) }
func co(k uint64,i int) int { return int((k>>uint(24+2*i))&3) }
func inspectPair(p cornerPair) fineType {
 var inverse [8]int
 var seenA,seenB [8]bool
 var rel [8]int
 for i:=0;i<8;i++ {
  a,b:=cp(p.first,i),cp(p.second,i)
  if seenA[a] || seenB[b] { fail("corner permutation not bijective") }
  seenA[a]=true; seenB[b]=true
  inverse[a]=i
  if co(p.first,i)>2 || co(p.second,i)>2 { fail("invalid corner orientation") }
 }
 for i:=0;i<8;i++ { rel[i]=inverse[cp(p.second,i)] }
 var seen [8]bool
 cycles:=[]int{}
 moved:=0
 for i:=0;i<8;i++ {
  if seen[i] { continue }
  j,n:=i,0
  for !seen[j] { seen[j]=true;n++;j=rel[j] }
  if n>1 { cycles=append(cycles,n);moved+=n }
 }
 sort.Ints(cycles)
 plus,minus:=0,0
 for i:=0;i<8;i++ {
  delta:=(co(p.second,i)-co(p.first,i)+3)%3
  if delta==1 { plus++ } else if delta==2 { minus++ }
 }
 if (plus+2*minus)%3!=0 { fail("twist conservation fails") }
 if (moved-len(cycles))%2!=0 { fail("relative permutation parity fails") }
 if moved!=4 && moved!=6 { fail("new moved permutation count beyond original P11") }
 if moved==4 && !(len(cycles)==2&&cycles[0]==2&&cycles[1]==2) { fail("unexpected CP four-slot cycle type") }
 if moved==6 && !(len(cycles)==2 && ((cycles[0]==3&&cycles[1]==3)||(cycles[0]==2&&cycles[1]==4))) { fail("unexpected CP six-slot cycle type") }
 if (plus+minus)==2 && !(plus==1&&minus==1) { fail("twist support2 unbalanced") }
 if (plus+minus)==4 && !(plus==2&&minus==2) { fail("twist support4 unbalanced") }
 if (plus+minus)!=0 && (plus+minus)!=2 && (plus+minus)!=4 { fail("unexpected twist support") }
 cycleStr:=strings.Trim(strings.ReplaceAll(fmt.Sprint(cycles)," ","+"),"[]")
 return fineType{p.fiberSize,moved,plus+minus,plus,minus,cycleStr}
}

type geometricSignature struct {
 cycles string
 relative [8]uint8
 permMask, twistMask, overlap uint8
 plus, minus int
}
func geometry(a,b uint64) geometricSignature {
 var inverse [8]int
 var rel [8]int
 var seenA,seenB [8]bool
 for i:=0;i<8;i++ {
  x,y:=cp(a,i),cp(b,i)
  if seenA[x]||seenB[y] { fail("invalid physical permutation") }
  seenA[x]=true;seenB[y]=true;inverse[x]=i
  if co(a,i)>2||co(b,i)>2 { fail("invalid twist") }
 }
 g:=geometricSignature{}
 for i:=0;i<8;i++ {
  rel[i]=inverse[cp(b,i)];g.relative[i]=uint8(rel[i])
  if cp(a,i)!=cp(b,i) {g.permMask|=uint8(1<<uint(i))}
  d:=(co(b,i)-co(a,i)+3)%3
  if d==1 {g.plus++;g.twistMask|=uint8(1<<uint(i))}
  if d==2 {g.minus++;g.twistMask|=uint8(1<<uint(i))}
 }
 var visited [8]bool
 cycles:=[]int{}
 moved,transpositionParity:=0,0
 for i:=0;i<8;i++ {
  if visited[i] { continue }
  j,n:=i,0
  for !visited[j] {visited[j]=true;n++;j=rel[j]}
  if n>1 {cycles=append(cycles,n);moved+=n;transpositionParity+=n-1}
 }
 if transpositionParity%2!=0 {fail("shared-edge corners have different CP parity")}
 if (g.plus+2*g.minus)%3!=0 {fail("corner twist conservation broken")}
 if moved!=bits.OnesCount8(g.permMask) {fail("relative support inconsistent")}
 g.overlap=g.permMask&g.twistMask
 sort.Ints(cycles)
 g.cycles=strings.Trim(strings.ReplaceAll(fmt.Sprint(cycles)," ","+"),"[]")
 return g
}
func fmtPerm(p [8]uint8)string{
 return fmt.Sprintf("%d%d%d%d%d%d%d%d",p[0],p[1],p[2],p[3],p[4],p[5],p[6],p[7])
}

func main() {
 if len(os.Args)!=3 { fail("usage: p12-P3 <true-original-P9-B6.bin> <full-576-pairs.tsv>") }
 witnessOut,e:=os.Create(os.Args[2]);if e!=nil{fail(e.Error())};defer witnessOut.Close()
 writer:=bufio.NewWriter(witnessOut)
 fmt.Fprintln(writer,"corner1_u64\tcorner2_u64\tfiber_size\tcp_cycle\trelative_cp_perm\tcp_mask_hex\tco_mask_hex\tco_overlap_hex\tplus\tminus")
 f,e:=os.Open(os.Args[1]);if e!=nil{fail(e.Error())};defer f.Close()
 st,e:=f.Stat();if e!=nil||st.Size()!=goalRows*16{fail("whole B6 size not 131841392")}
 h:=sha256.New();h.Write([]byte(domainHeader))
 classes:=make(map[string]*firstCorner,1405068)
 pairs:=make([]cornerPair,0,576)
 records:=make([]rowKey,0,goalRows)
 countCorners:=0
 var prevC,prevE uint64
 var edges []uint64
 flush:=func(){
  if len(edges)==0{fail("empty original corner fiber")}
  packed:=make([]byte,len(edges)*8)
  for i,v:=range edges{binary.LittleEndian.PutUint64(packed[8*i:],v)}
  key:=string(packed)
  if old,ok:=classes[key];ok{
   if old.multiplicity!=1{fail("fiber occurrence >2")}
   old.multiplicity++
   pairs=append(pairs,cornerPair{old.corner,prevC,len(edges)})
  }else{classes[key]=&firstCorner{prevC,1}}
  countCorners++
 }
 var row [16]byte
 for i:=0;i<goalRows;i++ {
  if _,e:=io.ReadFull(f,row[:]);e!=nil{fail("whole B6 truncated")}
  h.Write(row[:])
  c,edge:=binary.LittleEndian.Uint64(row[:8]),binary.LittleEndian.Uint64(row[8:])
  if i>0&&(c<prevC||(c==prevC&&edge<=prevE)){fail("whole B6 unsorted or duplicate")}
  records=append(records,rowKey{c,edge})
  if i==0 {prevC=c}
  if c!=prevC{flush();edges=edges[:0];prevC=c}
  edges=append(edges,edge);prevE=edge
 }
 flush()
 if hex.EncodeToString(h.Sum(nil))!=originalGoalSHA{fail("original domain-separated goal SHA mismatch")}
 if countCorners!=1405068||len(classes)!=1404492||len(pairs)!=576{fail("P11 exact fiber cardinalities drift")}
 coarse:=make(map[string]int)
 fine:=make(map[string]int)
 for _,p:=range pairs{
  sig:=inspectPair(p)
  ck:=fmt.Sprintf("%d/%d/%d",sig.fiberSize,sig.cpMoved,sig.coMoved)
  coarse[ck]++
  fk:=fmt.Sprintf("size=%d cpCycle=%s cpMoved=%d coMoved=%d deltaPlus=%d deltaMinus=%d",
   sig.fiberSize,sig.cycles,sig.cpMoved,sig.coMoved,sig.plus,sig.minus)
  fine[fk]++
 }
 // P3 full relative geometry of the 576 EQUAL-FIBER pairs.
 exactPairSet:=make(map[pairKey]int,576)
 relativeMaps:=make(map[string]int)
 supportMasks:=make(map[string]int)
 twistMasks:=make(map[string]int)
 intersectionHist:=make(map[string]int)
 for _,p:=range pairs {
  key:=pairKey{p.first,p.second}
  if _,ok:=exactPairSet[key];ok {fail("same exact duplicated pair appears twice")}
  exactPairSet[key]=p.fiberSize
  g:=geometry(p.first,p.second)
  if (g.cycles!="2+4"&&g.cycles!="2+2") {fail("P12 fine cycle result changed")}
  if int(bits.OnesCount8(g.twistMask))!=g.plus+g.minus{fail("twist mask invalid")}
  mk:=g.cycles+"/"+fmtPerm(g.relative)
  relativeMaps[mk]++
  ck:=fmt.Sprintf("fiber=%d cycle=%s mask=%02x",p.fiberSize,g.cycles,g.permMask)
  supportMasks[ck]++
  tw:=fmt.Sprintf("fiber=%d cycle=%s coMask=%02x",p.fiberSize,g.cycles,g.twistMask)
  twistMasks[tw]++
  intersectionHist[fmt.Sprintf("fiber=%d cycle=%s cpMoved=%d coMoved=%d overlap=%d",p.fiberSize,g.cycles,bits.OnesCount8(g.permMask),bits.OnesCount8(g.twistMask),bits.OnesCount8(g.overlap))]++
  fmt.Fprintf(writer,"%d\t%d\t%d\t%s\t%s\t%02x\t%02x\t%02x\t%d\t%d\n",
    p.first,p.second,p.fiberSize,g.cycles,fmtPerm(g.relative),g.permMask,g.twistMask,g.overlap,g.plus,g.minus)
 }
 if err:=writer.Flush();err!=nil{fail("witness flush: "+err.Error())}
 if err:=witnessOut.Close();err!=nil{fail("witness close: "+err.Error())}
 // New falsification court: all pairs with some common edge witness, not
 // just the 576 pairs with exactly identical complete edge fibers.
 // Sorting (edge,corner) of the EXACT same pinned B6 records avoids a
 // massive sparse map and preserves every physical occurrence.
 sort.Slice(records,func(i,j int)bool{
  if records[i].e!=records[j].e{return records[i].e<records[j].e}
  return records[i].c<records[j].c
 })
 sharedEdgePairIncidences:=uint64(0)
 duplicateEdgeIncidences:=uint64(0)
 witnessNonDuplicateThreeThree:=uint64(0)
 witnessAllThreeThree:=uint64(0)
 wCycles:=make(map[string]uint64)
 maxCornersPerEdge:=0
 var witnessRow rowKey
 var witnessCorners [2]uint64
 for lo:=0;lo<len(records); {
  hi:=lo+1
  for hi<len(records)&&records[hi].e==records[lo].e{hi++}
  n:=hi-lo
  if n>maxCornersPerEdge{maxCornersPerEdge=n}
  for i:=lo;i<hi;i++ {for j:=i+1;j<hi;j++{
   a,b:=records[i].c,records[j].c
   if a==b{fail("repeated corner/edge in sorted original goal")}
   if a>b{a,b=b,a}
   g:=geometry(a,b)
   sharedEdgePairIncidences++
   wCycles[g.cycles]++
   if _,ok:=exactPairSet[pairKey{a,b}];ok{duplicateEdgeIncidences++}
   if g.cycles=="3+3" {
    witnessAllThreeThree++
    if _,ok:=exactPairSet[pairKey{a,b}];ok{fail("P12 verified equal fiber (3)(3) contradiction")}
    witnessNonDuplicateThreeThree++
    if witnessAllThreeThree==1 {witnessRow=records[i];witnessCorners=[2]uint64{a,b}}
   }
  }}
  lo=hi
 }
 if duplicateEdgeIncidences!=uint64(192+4*384){fail("equal-fiber witness incidence did not equal sum(size of 576 shared fibers)")}
 fmt.Printf("P12_P3_EDGE_WITNESS_VS_EQUAL_FIBER_PASS FULL_B6_SHA256 %s FULL_STATES %d PAIRS_WITH_LITERAL_EQUAL_FIBER %d DISTINCT_EQUAL_RELATIVE_MAPS %d EDGE_WITNESS_PAIR_INCIDENCES %d DUPLICATE_FIBER_EDGE_INCIDENCES %d WITNESS_ONLY_NON_EQUAL_THREE_THREE %d ALL_SHARED_EDGE_THREE_THREE %d MAX_CORNER_MULTIPLICITY_PER_EDGE %d GLOBAL_LOWER17_CLAIMED 0\n",
 originalGoalSHA,goalRows,len(exactPairSet),len(relativeMaps),sharedEdgePairIncidences,duplicateEdgeIncidences,witnessNonDuplicateThreeThree,witnessAllThreeThree,maxCornersPerEdge)
 if witnessAllThreeThree>0{
   fmt.Printf("P12_P3_EDGE_WITNESS_THREE_THREE_COUNTEREXAMPLE EDGE %d CORNER_A %d CORNER_B %d ALREADY_IN_FULL_B6 1 EXACT_FIBERS_NOT_EQUAL 1\n",witnessRow.e,witnessCorners[0],witnessCorners[1])
 }
 printCounts:=func(label string,m map[string]int){
  keys:=make([]string,0,len(m));for k:=range m{keys=append(keys,k)};sort.Strings(keys)
  for _,k:=range keys{fmt.Printf("%s KEY %s PAIRS %d\n",label,k,m[k])}
 }
 printCounts("P12_P3_EQUAL_RELATIVE_MAP",relativeMaps)
 printCounts("P12_P3_EQUAL_SUPPORT_MASK",supportMasks)
 printCounts("P12_P3_EQUAL_TWIST_MASK",twistMasks)
 printCounts("P12_P3_EQUAL_MASK_OVERLAP",intersectionHist)
 wKeys:=make([]string,0,len(wCycles));for k:=range wCycles{wKeys=append(wKeys,k)};sort.Strings(wKeys)
 for _,k:=range wKeys{fmt.Printf("P12_P3_COMMON_EDGE_CYCLE KEY %s PAIR_INCIDENCES %d\n",k,wCycles[k])}

 required:=map[string]int{"1/6/2":96,"1/6/4":96,"4/4/0":256,"4/4/4":128}
 if len(coarse)!=len(required){fail("unexpected coarse fiber classes")}
 for k,n:=range required{if coarse[k]!=n{fail("P11 coarse type mismatch "+k)}}
 keys:=make([]string,0,len(fine));for k:=range fine{keys=append(keys,k)};sort.Strings(keys)
 fmt.Printf("P12_P3_ORIGINAL_B6_RELATIVE_CYCLE_CENSUS_PASS GOAL_SHA256 %s PAIRS %d CLASSES %d COARSE_TYPES %d SOURCE_B10_GLOBAL_COMPLETE 0 GLOBAL_LOWER17_CLAIMED 0\n",
  originalGoalSHA,len(pairs),len(classes),len(coarse))
 for _,k:=range keys{fmt.Printf("P12_FINE_TYPE %s PAIRS %d\n",k,fine[k])}
}
