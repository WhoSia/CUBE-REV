// CUBE-REV P0-R6I-P8 independent Go proof-carrying court auditor.
// Stream the ACTUAL canonical sorted CP/CO/EP/EO 16-byte goal image,
// independently compute domain-separated SHA-256 and validate ordered
// uniqueness, physical permutation/orientation invariants, exact
// source DFA coverage, all individual receipts and immutable digests.
// Does NOT infer goal-ball BFS completeness merely from its hash.
package main
import(
 "crypto/sha256"
 "encoding/binary"
 "encoding/hex"
 "fmt"
 "io"
 "os"
 "strconv"
 "strings"
)
func fail(s string){fmt.Fprintln(os.Stderr,"P8_GO_AUDIT_FAIL",s);os.Exit(2)}
func kv(line,key string)string{
 w:=strings.Fields(line)
 for i:=0;i+1<len(w);i++{if w[i]==key{return w[i+1]}}
 fail("missing "+key);return ""
}
func integer(line,key string)uint64{
 v,e:=strconv.ParseUint(kv(line,key),10,64)
 if e!=nil{fail("noninteger "+key)}
 return v
}
func signed(line,key string)int{
 v,e:=strconv.Atoi(kv(line,key))
 if e!=nil{fail("noninteger signed "+key)}
 return v
}
func canonical(last,next int)bool{
 if last<0{return true}
 a,b:=last/3,next/3
 if a==b{return false}
 opposite:=(a==0&&b==3)||(a==3&&b==0)||(a==1&&b==4)||(a==4&&b==1)||(a==2&&b==5)||(a==5&&b==2)
 return !opposite||b>=a
}
func sourceCalls(last,k int)uint64{
 var prev [18]uint64
 total:=uint64(k+1)
 for d:=1;d<=k;d++{
  var next [18]uint64
  if d==1{for a:=0;a<18;a++{if canonical(last,a){next[a]=1}}}else{
   for b,v:=range prev{for a:=0;a<18;a++{if canonical(b,a){next[a]+=v}}}
  }
  prev=next
  var layer uint64;for _,v:=range next{layer+=v}
  total+=uint64(k-d+1)*layer
 }
 return total
}
func validCubie(c,e uint64)bool{
 var corners,edges uint16
 sumCo,sumEo:=0,0
 var cp [8]int;var ep [12]int
 for i:=0;i<8;i++{
  digit:=int((c>>(3*i))&7)
  co:=int((c>>(24+2*i))&3)
  if co>=3||corners&(1<<digit)!=0{return false}
  corners|=1<<digit;sumCo+=co;cp[i]=digit
 }
 for i:=0;i<12;i++{
  digit:=int((e>>(4*i))&15)
  eo:=int((e>>(48+i))&1)
  if digit>=12||edges&(1<<digit)!=0{return false}
  edges|=1<<digit;sumEo+=eo;ep[i]=digit
 }
 if corners!=255||edges!=4095||sumCo%3!=0||sumEo%2!=0{return false}
 cpParity,epParity:=0,0
 for i:=0;i<8;i++{for j:=i+1;j<8;j++{if cp[i]>cp[j]{cpParity^=1}}}
 for i:=0;i<12;i++{for j:=i+1;j<12;j++{if ep[i]>ep[j]{epParity^=1}}}
 return cpParity==epParity
}
func goalDigest(path string,radius int,count uint64)string{
 f,e:=os.Open(path);if e!=nil{fail("cannot open full original sorted goal image")}
 defer f.Close()
 st,e:=f.Stat();if e!=nil||st.Size()!=int64(count*16){fail("canonical image has wrong complete count/byte length")}
 hash:=sha256.New()
 header:=fmt.Sprintf("CUBE-REV-025-P8:FULL-CP-CO-EP-EO:LE64x2:v1;radius=%d;count=%d\n",radius,count)
 hash.Write([]byte(header))
 buf:=make([]byte,16)
 var beforeC,beforeE uint64
 for i:=uint64(0);i<count;i++{
  if _,e:=io.ReadFull(f,buf);e!=nil{fail("truncated full original cubie set")}
  hash.Write(buf)
  c:=binary.LittleEndian.Uint64(buf[:8])
  ep:=binary.LittleEndian.Uint64(buf[8:])
  if i>0&&(c<beforeC||(c==beforeC&&ep<=beforeE)){
   fail("goal snapshot not sorted strictly or contains duplicates")
  }
  if !validCubie(c,ep){fail(fmt.Sprintf("invalid physical CP/CO/EP/EO at goal index %d",i))}
  beforeC,beforeE=c,ep
 }
 extra:=make([]byte,1)
 if n,_:=f.Read(extra);n!=0{fail("unexpected trailing goal bytes")}
 return hex.EncodeToString(hash.Sum(nil))
}
func main(){
 if len(os.Args)!=4{fail("usage: actual_immutable_batch.log canonical_goal.bin smoke|b7|b10sample")}
 logPath,image,mode:=os.Args[1],os.Args[2],os.Args[3]
 rg,rs:=6,7
 if mode=="smoke"{rg=3;rs=3}else if mode=="b10sample"{rs=10}else if mode!="b7"{fail("unsupported mode")}
 raw,e:=os.ReadFile(logPath);if e!=nil{fail("missing real physical batch log")}
 t:=string(raw)
 if strings.Contains(t,"P8_ERROR")||strings.Contains(t,"P8_RESOURCE_HOLD")||
   strings.Contains(t,"P8_TRUE_LEAF_CUBIE_MEET")||strings.Contains(t,"P8_TRUE_INTERNAL_CUBIE_MEET")||
   strings.Contains(t,"P8_HOLD_GOAL"){fail("physical failure/HOLD/positive full-cubie intersection")}
 lines:=strings.Split(t,"\n")
 expectedStates:=uint64(8240087);expectedTotal:=uint64(120213368)
 if mode=="smoke"{expectedStates=3502;expectedTotal=3784}
 targetDigest:=goalDigest(image,rg,expectedStates)
 gotGoal,gotFinal:=false,false
 internalCount,leafCount:=0,0
 var internalWeight,leafWeight,leafVisits,leafSkips uint64
 var occupied [18][18]bool
 var singleton [18]bool
 for _,line:=range lines{
  line=strings.TrimSpace(line)
  if strings.HasPrefix(line,"P8_GOAL_COMMIT "){
   if gotGoal||kv(line,"MODE")!=mode||kv(line,"SHA256")!=targetDigest||
     integer(line,"RADIUS")!=uint64(rg)||integer(line,"STATES")!=expectedStates||
     integer(line,"SNAPSHOT_BYTES")!=expectedStates*16||
     integer(line,"PHYSICAL_TURNS_CHECKED")!=4608{fail("wrong snapshot binding or original physics")}
   if mode!="smoke"&&(integer(line,"C")!=1405068||integer(line,"E")!=7672278){
    fail("whole original B6 projection cardinality mismatch")
   }
   gotGoal=true
  }else if strings.HasPrefix(line,"P8_INTERNAL "){
   if !gotGoal||mode=="b10sample"{fail("unexpected internal first-prefix certificate")}
   depth:=int(integer(line,"DEPTH"))
   first:=signed(line,"FIRST")
   if internalCount==0{
    if depth!=0||first!=-1{fail("missing real physical original source root")}
   }else if internalCount==1{
    if depth!=1||first!=0{fail("missing first-U original physical internal check")}
   }else if internalCount==2{
    if depth!=1||first!=9{fail("missing first-D original physical internal check")}
   }else{fail("extra internal check")}
   count:=uint64(rs-depth+1)
   if integer(line,"REPEATED_CALLS")!=count||integer(line,"WHOLE_CUBIE_MEETS")!=0||
      kv(line,"GOAL_SHA256")!=targetDigest{fail("unsound physical internal prefix receipt")}
   internalWeight+=count;internalCount++
  }else if strings.HasPrefix(line,"P8_LEAF "){
   if !gotGoal||gotFinal{fail("leaf outside batch context")}
   leafCount++
   if integer(line,"INDEX")!=uint64(leafCount)||kv(line,"MODE")!=mode||
     kv(line,"GOAL_SHA256")!=targetDigest||integer(line,"FULL_CUBIE_MEETS")!=0||
     integer(line,"COMPLETE")!=1{fail("incorrect or duplicated leaf completion")}
   a,b:=signed(line,"FIRST"),signed(line,"SECOND")
   depth:=int(integer(line,"PREFIX_DEPTH"))
   if a<0||a>=18{fail("source action outside original 18HTM")}
   last:=a
   if b<0{
    if depth!=1||mode=="b10sample"||a==0||a==9||singleton[a]{
      fail("illegal/duplicate first-action leaf")
    }
    singleton[a]=true
   }else{
    if depth!=2||b>=18||!canonical(a,b)||occupied[a][b]{
     fail("invalid ordered two-action canonical leaf")
    }
    if mode=="b10sample"{
     if !((leafCount==1&&a==0&&b==3)||(leafCount==2&&a==9&&b==3)){
       fail("unexpected original B10 calibrated sibling")
     }
    }else if a!=0&&a!=9{fail("unrequested deeper leaf")}
    occupied[a][b]=true;last=b
   }
   // Verify the physical root-state key values are even permissible cubies.
   if !validCubie(integer(line,"SOURCE_KEY_C"),integer(line,"SOURCE_KEY_E")){
    fail("not a genuine legally oriented and permuted source cubie")
   }
   expected:=sourceCalls(last,rs-depth)
   visits,omissions:=integer(line,"VISITED"),integer(line,"OMITTED")
   if integer(line,"WORD_CALLS")!=expected||visits+omissions!=expected||
      integer(line,"EDGES")>integer(line,"PAIRS"){fail("not an exact original physical source DFS accounting")}
   leafWeight+=expected;leafVisits+=visits;leafSkips+=omissions
  }else if strings.HasPrefix(line,"P8_BATCH_CERT "){
   if gotFinal||kv(line,"MODE")!=mode||kv(line,"GOAL_SHA256")!=targetDigest||
     kv(line,"POST_SEARCH_SHA256")!=targetDigest||integer(line,"IMMUTABLE")!=1||
     integer(line,"ORIGINAL_PHYSICS_4608")!=1||
     integer(line,"GOAL_RADIUS")!=uint64(rg)||integer(line,"SOURCE_RADIUS")!=uint64(rs)||
     integer(line,"LOWER17_CLAIMED")!=0||integer(line,"FULL_CUBIE_GOAL_MEETS")!=0{
    fail("batch target or original physical negative certificate changed")
   }
   full:=mode!="b10sample"
   expectedLeaves,expectedInternals:=43,3
   if !full{expectedLeaves=2;expectedInternals=0}
   if integer(line,"LEAVES")!=uint64(expectedLeaves)||
     integer(line,"INTERNAL_CALLS")!=internalWeight||
     integer(line,"VISITED")!=internalWeight+leafVisits||
     integer(line,"OMITTED")!=leafSkips||
     integer(line,"WEIGHT_TOTAL")!=internalWeight+leafWeight||
     integer(line,"SOURCE_GLOBAL_COMPLETE")!=uint64(map[bool]int{true:1,false:0}[full]){
      fail("wrong summarized goal-binding or actual canonical source count")
   }
   if full{
    if integer(line,"BASELINE")!=expectedTotal||
       internalWeight+leafWeight!=expectedTotal{fail("full original R7 global source cover not conserved")}
   }else if integer(line,"BASELINE")!=0{fail("sampled R10 cannot masquerade as global source coverage")}
   if leafCount!=expectedLeaves||internalCount!=expectedInternals{
    fail("missing source proof leaf or internal checks")
   }
   gotFinal=true
  }
 }
 if !gotGoal||!gotFinal{fail("missing goal image provenance or completed original proof batch")}
 if mode!="b10sample"{
  for a:=0;a<18;a++{
   if a==0||a==9{
    for b:=0;b<18;b++{if canonical(a,b)&&!occupied[a][b]{fail("source DFA prefix partition misses physical branch")}}
   }else if !singleton[a]{fail("missing an entire first-action source cylinder")}
  }
 }
 fmt.Printf("P8_GO_INDEPENDENT_SHA256_AND_PHYSICAL_DFA_BATCH_PASS MODE %s GOAL_SHA256 %s GOAL_STATES %d CANONICAL_GOAL_BYTES %d LEGALLY_PACKED_CUBIES_CHECKED %d LEAVES %d INTERNAL_NODES %d WEIGHT_TOTAL %d SOURCE_VISITS %d SOUNDLY_OMITTED %d PHYSICAL_BALL_COMMITMENT_RECHECKED 1 ORIGINAL_GOAL_GENERATION_BFS_INDEPENDENTLY_REIMPLEMENTED 0 FULL_SOURCE_RADIUS %d GLOBAL_LOWER17_NOT_CLAIMED 1\n",
  mode,targetDigest,expectedStates,expectedStates*16,expectedStates,leafCount,internalCount,internalWeight+leafWeight,internalWeight+leafVisits,leafSkips,rs)
}
