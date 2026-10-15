// CUBE-REV 0.25 P0-R6I-P10 exact conditional B6 edge fibers.
// Independent, lossless string equality (no hash-only collision guesses).
// Stream the REAL golden original B6 8,240,087 sorted whole cubie image.
// Count distinct edge-fiber equivalence classes, multiplicities and sizes,
// calculate fixed-length label cardinality/bit lower bound and the exact
// uniform Cartesian-marginal false positive fraction.  No model guesses.
package main
import("crypto/sha256";"encoding/binary";"encoding/hex";"fmt";"io";"math";"os";"sort";"strconv";"strings")
const golden="82fe545bcad3537c989ec22afce9d286926ddce5f4ef9428c0307951ec2d0979"
type fiberClass struct{freq int; size int}
func fail(msg string){fmt.Fprintln(os.Stderr,"P10_FIBER_AUDIT_FAIL",msg);os.Exit(2)}
func get(line,k string)string{w:=strings.Fields(line);for i:=0;i+1<len(w);i++{if w[i]==k{return w[i+1]}};fail("missing "+k);return ""}
func num(line,k string)uint64{v,e:=strconv.ParseUint(get(line,k),10,64);if e!=nil{fail("bad "+k)};return v}
func main(){
 if len(os.Args)!=4{fail("usage: full-golden-B6.bin original-native-P9-audit.log independent-P9-projection-Go-audit.log")}
 wholePath,nativePath,goPath:=os.Args[1],os.Args[2],os.Args[3]
 raw,e:=os.ReadFile(nativePath);if e!=nil{fail("original complete native goal provenance missing")}
 ng:=string(raw)
 nativeOK:=false
 for _,line:=range strings.Split(ng,"\n"){
  if strings.HasPrefix(line,"P9_COMPLETE MODE audit "){
   if nativeOK||get(line,"GOAL_SHA256")!=golden||num(line,"TARGET_IMMUTABLE")!=1||
     num(line,"LOWER17_CLAIMED")!=0{fail("not pinned native real B6")}
   nativeOK=true
  }
 }
 audit,e:=os.ReadFile(goPath);if e!=nil{fail("independent exact projection audit not present")}
 if !nativeOK||!strings.Contains(string(audit),
  "P9_GO_INDEPENDENT_PROJECTION_CLOSURE_PASS GOAL_SHA256 "+golden+" "){
   fail("missing successful original B6 and C6/C7/E6 independently reconstructed projection audit")
 }
 f,e:=os.Open(wholePath);if e!=nil{fail("whole original B6 8.24M snapshot missing")};defer f.Close()
 info,e:=f.Stat();if e!=nil||info.Size()!=8240087*16{fail("whole B6 byte length not exactly 131841392")}
 h:=sha256.New();h.Write([]byte("CUBE-REV-025-P8:FULL-CP-CO-EP-EO:LE64x2:v1;radius=6;count=8240087\n"))
 classes:=make(map[string]*fiberClass,1500000)
 sizeHist:=make(map[int]int)
 classFrequency:=make(map[int]int)
 var row [16]byte
 var prevC,prevE uint64
 var edges []uint64
 corners,rows,maxFiber:=0,0,0
 flush:=func(){
  if len(edges)==0{fail("empty fiber in original present corner image")}
  if len(edges)>maxFiber{maxFiber=len(edges)}
  sizeHist[len(edges)]++
  packed:=make([]byte,8*len(edges))
  for i,e:=range edges{binary.LittleEndian.PutUint64(packed[8*i:8*(i+1)],e)}
  key:=string(packed)
  if v,ok:=classes[key];ok{
   if v.size!=len(edges){fail("fiber canonical equality inconsistent")}
   v.freq++
  }else{classes[key]=&fiberClass{freq:1,size:len(edges)}}
  corners++
 }
 for i:=0;i<8240087;i++{
  if _,e:=io.ReadFull(f,row[:]);e!=nil{fail("B6 snapshot unexpectedly truncated")}
  h.Write(row[:])
  c,edge:=binary.LittleEndian.Uint64(row[:8]),binary.LittleEndian.Uint64(row[8:])
  if i>0&&(c<prevC||(c==prevC&&edge<=prevE)){fail("whole B6 unsorted or duplicate")}
  if i==0{prevC=c}
  if c!=prevC{flush();edges=edges[:0];prevC=c}
  edges=append(edges,edge)
  prevE=edge;rows++
 }
 flush()
 if hex.EncodeToString(h.Sum(nil))!=golden{fail("original B6 SHA256 changed")}
 if rows!=8240087||corners!=1405068{fail("full target or distinct physical corner count changed")}
 maxClass,sharedCorners,singletonClasses:=0,0,0
 minLabelBits:=0
 if len(classes)>1{minLabelBits=int(math.Ceil(math.Log2(float64(len(classes)))))}
 classSizeHist:=make(map[int]int)
 for _,fiber:=range classes{
  if fiber.freq>maxClass{maxClass=fiber.freq}
  if fiber.freq==1{singletonClasses++}else{sharedCorners+=fiber.freq}
  classFrequency[fiber.freq]++
  classSizeHist[fiber.size]++
 }
 var checkCorner,checkRows int
 for size,count:=range sizeHist{checkCorner+=count;checkRows+=size*count}
 if checkRows!=rows||checkCorner!=corners{fail("fiber size distribution conservation failed")}
 checkClass:=0
 for n,c:=range classFrequency{checkClass+=n*c}
 if checkClass!=corners{fail("fiber equivalence partition conservation failed")}
 // A conditional exact joint oracle accepts precisely |B6| pairs,
 // while a separate exact C6 and E6 marginal intersection accepts
 // |C6|*|E6| distinct pairs under UNIFORM counting across the Cartesian
 // marginal product. This is NOT the visited-source false-positive rate.
 product:=uint64(corners)*uint64(7672278)
 if product<=uint64(rows){fail("unexpected rectangular whole target")}
 fmt.Printf("P10_FIBER_EXACT_PASS GOAL_SHA256 %s PHYSICAL_WHOLE_ROWS %d CORNERS_WITH_SUPPORT %d EDGE_MARGINAL_SIZE 7672278 EXACT_DISTINCT_FIBERS %d SINGLETON_EQUIVALENCE_CLASSES %d CORNERS_IN_SHARED_CLASSES %d MAX_CLASS_MULTIPLICITY %d MAX_FIBER_EDGES %d FIXED_WIDTH_LABEL_MIN_BITS %d LABEL_ARRAY_BIT_LOWER %d UNIFORM_MARGINAL_PRODUCT_PAIRS %d REAL_JOINT_PAIRS %d UNIFORM_MARGINAL_FALSE_POSITIVE_PAIRS %d UNIFORM_MARGINAL_FALSE_POSITIVE_RATE %.12f ENTIRE_FIBER_ROWS_CHECKED 1 EXACT_BYTE_COMPARISON_NO_DIGEST_COLLISION 1 GLOBAL_B10_COMPLETE 0\n",
 golden,rows,corners,len(classes),singletonClasses,sharedCorners,maxClass,maxFiber,
 minLabelBits,uint64(minLabelBits)*uint64(corners),product,rows,product-uint64(rows),
 float64(product-uint64(rows))/float64(product))
 sizes:=make([]int,0,len(sizeHist));for v:=range sizeHist{sizes=append(sizes,v)};sort.Ints(sizes)
 for _,size:=range sizes{
  fmt.Printf("P10_FIBER_SIZE SIZE %d CORNERS %d TOTAL_WHOLE_GOAL_STATES %d UNIQUE_EXACT_EDGE_FIBER_CLASSES %d\n",
   size,sizeHist[size],size*sizeHist[size],classSizeHist[size])
 }
 multiplicities:=make([]int,0,len(classFrequency));for v:=range classFrequency{multiplicities=append(multiplicities,v)};sort.Ints(multiplicities)
 for _,mult:=range multiplicities{
  fmt.Printf("P10_FIBER_CLASS_MULTIPLICITY CORNERS_PER_IDENTICAL_FIBER %d DISTINCT_CLASSES %d CORNERS_COVERED %d\n",
   mult,classFrequency[mult],mult*classFrequency[mult])
 }
}
