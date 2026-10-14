// CUBE-REV P0-R6E: exact 2-class transfer matrix for source canonical
// 18HTM grammar. Independent of physical cubie state search.
package main
import ("fmt";"os")
func die(s string){fmt.Fprintln(os.Stderr,"P0R6E_GRAMMAR_FAIL",s);os.Exit(2)}
func legal(a,b int)bool{
 fa,fb:=a/3,b/3
 if fa==fb{return false}
 opposite:=(fa==0&&fb==3)||(fa==3&&fb==0)||
 (fa==1&&fb==4)||(fa==4&&fb==1)||
 (fa==2&&fb==5)||(fa==5&&fb==2)
 return !opposite||fb>=fa
}

// shardCalls checks the original full 18-generator grammar starting with an
// EXACT first action. The source root's (R+1) IDDFS visits are handled separately.
func shardCalls(firstAction,limit int)uint64{
 current:=make([]uint64,18)
 current[firstAction]=1
 var weighted uint64
 for depth:=1;depth<=limit;depth++{
  if depth>1{
   next:=make([]uint64,18)
   for a:=0;a<18;a++{for b,v:=range current{
    if legal(b,a){next[a]+=v}
   }}
   current=next
  }
  var layer uint64
  for _,v:=range current{layer+=v}
  weighted+=uint64(limit-depth+1)*layer
 }
 return weighted
}

func main(){
 var low,high uint64=9,9 // 3 low faces and 3 high faces × 3 HTM powers
 byLast:=make([]uint64,18)
 for i:=range byLast{byLast[i]=1}
 var summed uint64=1
 var cumulative uint64=1
 var prev2,prev1 uint64
 for d:=1;d<=10;d++{
  current:=low+high
  if d>1{
   next:=make([]uint64,18)
   for a:=0;a<18;a++{for b,v:=range byLast{
    if legal(b,a){next[a]+=v}
   }}
   byLast=next
  }
  var raw uint64
  for _,v:=range byLast{raw+=v}
  if raw!=current{die(fmt.Sprintf("18-letter DP disagrees at depth %d: %d vs %d",d,raw,current))}
  if d>=3&&current!=12*prev1+18*prev2{
   die("exact characteristic recurrence fails")
  }
  summed+=current
  cumulative+=summed
  fmt.Printf("P0R6E_CANONICAL_DEPTH %d WORDS %d CURRENT_LOW %d CURRENT_HIGH %d ITERATIVE_DFS_VISITS %d\n",d,current,low,high,cumulative)
  if d==7&&cumulative!=120213368{die("old B7 court mismatch")}
  if d==8&&cumulative!=1604664504{die("old B8 global lower15 court mismatch")}
  if d==9&&cumulative!=21419814808{die("B9 source count mismatch")}
  prev2,prev1=prev1,current
  low,high=6*low+6*high,9*low+6*high
 }
 for radius:=1;radius<=10;radius++{
  low:=shardCalls(0,radius)
  high:=shardCalls(9,radius)
  var previousHigh uint64
  if radius>=2{previousHigh=shardCalls(9,radius-1)}
  if low!=high+3*previousHigh{
   die(fmt.Sprintf("exact low/high rational language derivative identity fails at radius %d",radius))
  }
  fmt.Printf("P0R6H_SHARD_CLASS_EXACT_IDENTITY RADIUS %d LOW %d HIGH %d HIGH_PREVIOUS %d LOW_EQUALS_HIGH_PLUS_3_PREVIOUS 1\n",radius,low,high,previousHigh)
 }
 fmt.Printf("P0R6H_RATIONAL_LANGUAGE_CLASS_IDENTITY_PASS VERIFIED_RADII 1_TO_10 1 FORMULA LOW_R_EQUALS_HIGH_R_PLUS_3_HIGH_R_MINUS_1 1\n")
 var shards uint64
 for a:=0;a<18;a++{
  size:=shardCalls(a,10)
  expected:=uint64(17489205559)
  if a>=9{expected=14279876542}
  if size!=expected{die(fmt.Sprintf("normal-form source first-move shard %d unexpectedly contains %d",a,size))}
  fmt.Printf("P0R6G_SOURCE_B10_FIRST_MOVE_SHARD ACTION_ID %d CANONICAL_ITERATIVE_CALLS %d CLASS %s\n",a,size,func()string{if a<9{return "LOW"};return "HIGH"}())
  shards+=size
 }
 if 11+shards!=285921738920{die("18 first-move shards + all repeated root visits do not exactly cover B10")}
 fmt.Printf("P0R6G_B10_SOURCE_FIRST_MOVE_PARTITION_PASS ROOT_VISITS 11 LOW_SHARD_SIZE 17489205559 HIGH_SHARD_SIZE 14279876542 LOW_SHARDS 9 HIGH_SHARDS 9 TOTAL_CANONICAL_CALLS 285921738920\n")
 fmt.Printf("P0R6E_TWO_STATE_GRAMMAR_EXACT_PASS TRANSFER_LOW_TO_LOW 6 LOW_TO_HIGH 9 HIGH_TO_LOW 6 HIGH_TO_HIGH 6 CHARACTERISTIC_RECURRENCE C_D_PLUS_2_EQUALS_12_C_D_PLUS_1_PLUS_18_C_D 1 R7 120213368 R8 1604664504 R9 21419814808\n")
}
