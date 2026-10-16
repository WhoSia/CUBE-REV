// CUBE-REV 0.25 P0-R6I-P12-P1: exact cycle refinement of the P11 B6 duplicate fibers.
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
)

const originalGoalSHA = "82fe545bcad3537c989ec22afce9d286926ddce5f4ef9428c0307951ec2d0979"
const goalRows = 8240087
const domainHeader = "CUBE-REV-025-P8:FULL-CP-CO-EP-EO:LE64x2:v1;radius=6;count=8240087\n"

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
func main() {
 if len(os.Args)!=2 { fail("usage: p12-cycle <true-original-P9-B6.bin>") }
 f,e:=os.Open(os.Args[1]);if e!=nil{fail(e.Error())};defer f.Close()
 st,e:=f.Stat();if e!=nil||st.Size()!=goalRows*16{fail("whole B6 size not 131841392")}
 h:=sha256.New();h.Write([]byte(domainHeader))
 classes:=make(map[string]*firstCorner,1405068)
 pairs:=make([]cornerPair,0,576)
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
 required:=map[string]int{"1/6/2":96,"1/6/4":96,"4/4/0":256,"4/4/4":128}
 if len(coarse)!=len(required){fail("unexpected coarse fiber classes")}
 for k,n:=range required{if coarse[k]!=n{fail("P11 coarse type mismatch "+k)}}
 keys:=make([]string,0,len(fine));for k:=range fine{keys=append(keys,k)};sort.Strings(keys)
 fmt.Printf("P12_ORIGINAL_B6_RELATIVE_CYCLE_CENSUS_PASS GOAL_SHA256 %s PAIRS %d CLASSES %d COARSE_TYPES %d SOURCE_B10_GLOBAL_COMPLETE 0 GLOBAL_LOWER17_CLAIMED 0\n",
  originalGoalSHA,len(pairs),len(classes),len(coarse))
 for _,k:=range keys{fmt.Printf("P12_FINE_TYPE %s PAIRS %d\n",k,fine[k])}
}
