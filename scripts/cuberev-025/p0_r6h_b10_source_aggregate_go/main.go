// CUBE-REV 0.25 P0-R6H: SOURCE-B10 receipt aggregator.
// This checks 18 distinct first-letter cylinder receipts and full-cover
// counts against a pinned human-owned source revision and raw log hashes.
// IMPORTANT: It is a finite receipt/coverage auditor, not an independent
// physical original 54-sticker transition model or proof of authenticity.
// There is deliberately no "GLOBAL_LOWER17" output without ALL 18 receipts.
package main

import (
 "crypto/sha256"
 "encoding/hex"
 "encoding/json"
 "fmt"
 "os"
 "path/filepath"
 "strconv"
 "strings"
)

type Shard struct {
 Action int `json:"action"`
 RunID int64 `json:"run_id"`
 JobID int64 `json:"job_id"`
 Path string `json:"path"`
 SHA256 string `json:"sha256"`
}
type Manifest struct {
 Schema string `json:"schema"`
 Source string `json:"source"`
 GoalRadius int `json:"goal_radius"`
 SourceRadius int `json:"source_radius"`
 CommitSHA string `json:"commit_sha"`
 RootChecked bool `json:"root_checked"`
 Shards []Shard `json:"shards"`
}
func bad(msg string) {fmt.Fprintln(os.Stderr,"P0R6H_AGGREGATE_REJECT",msg);os.Exit(2)}
func field(line,key string) string {
 s:=strings.Fields(line)
 for i:=0;i+1<len(s);i++{if s[i]==key{return s[i+1]}}
 bad("missing receipt field "+key)
 return ""
}
func num(line,key string) uint64 {
 x,err:=strconv.ParseUint(field(line,key),10,64)
 if err!=nil{bad("invalid integer "+key)}
 return x
}
func oneLine(raw,heading string)string{
 var found string
 for _,line:=range strings.Split(raw,"\n"){
  line=strings.TrimSpace(line)
  if strings.HasPrefix(line,heading+" "){
   if found!=""{bad("duplicate "+heading)}
   found=line
  }
 }
 if found==""{bad("missing "+heading)}
 return found
}
func physicalShard(file Shard,baseDir string) (uint64,uint64) {
 if file.Action<0||file.Action>=18||file.RunID<=0||file.JobID<=0{
  bad("invalid first-action ID or missing public Actions run/job IDs")
 }
 if filepath.IsAbs(file.Path)||file.Path==""||
   strings.HasPrefix(filepath.Clean(file.Path),".."){
  bad("shard log must reside under manifest directory")
 }
 fullPath:=filepath.Join(baseDir,file.Path)
 b,err:=os.ReadFile(fullPath)
 if err!=nil{bad("missing original job log "+file.Path)}
 digest:=sha256.Sum256(b)
 if hex.EncodeToString(digest[:])!=strings.ToLower(file.SHA256){
  bad("raw Actions log SHA256 mismatch for "+file.Path)
 }
 content:=string(b)
 if strings.Contains(content,"P0R6G_RESOURCE_HOLD")||
  strings.Contains(content,"P0R6G_ERROR")||
  strings.Contains(content,"P0R6G_TRUE_FULL_CUBIE_MEET") {
  bad("resource HOLD, error or genuine whole-cubie meet in shard log")
 }
 goal:=oneLine(content,"P0R6G_GOAL_FULL")
 result:=oneLine(content,"P0R6G_PHYSICAL_SHARD_COMPLETE")
 finish:=oneLine(content,"P0R6G_SINGLE_SHARD_COMPLETE")
 if num(goal,"P0R6G_GOAL_FULL")!=8240087 ||
  num(goal,"CORNER6")!=1405068 ||
  num(goal,"EDGE6")!=7672278 ||
  num(goal,"PHYSICAL_PACKED_CASES")!=4608 ||
  field(goal,"ROOT_CHECKED")!="1" ||
  num(result,"ACTION_ID")!=uint64(file.Action) ||
  num(finish,"P0R6G_SINGLE_SHARD_COMPLETE")!=1 ||
  num(finish,"ACTION_ID")!=uint64(file.Action) ||
  num(finish,"GOAL_RADIUS")!=6 ||
  num(finish,"SOURCE_RADIUS")!=10 ||
  field(finish,"ROOT_PHYSICAL_CHECKED")!="1" ||
  field(finish,"CANONICAL_LAST_ACTION_CONTEXT_PRESERVED")!="1" ||
  field(finish,"ORIGINAL_54_STICKER_PHYSICS_PASS")!="1" ||
  field(finish,"NOT_A_GLOBAL_SOURCE_COVER")!="1" ||
  num(result,"GOAL_MEETS")!=0 ||
  num(finish,"FULL_CUBIE_GOAL_MEETS")!=0 {
  bad("wrong original cube physics, goal, source radius, scope or full-state absence for action "+strconv.Itoa(file.Action))
 }
 expected:=uint64(17489205559)
 if file.Action>=9{expected=14279876542}
 visited:=num(result,"VISITED")
 skipped:=num(result,"SKIPPED")
 if num(result,"BASELINE")!=expected||
  num(finish,"SHARD_BASELINE")!=expected ||
  num(finish,"SHARD_VISITED")!=visited||
  num(finish,"SHARD_SAFE_SKIPS")!=skipped||
  visited+skipped!=expected {
  bad("exact canonical first-generator coverage failed for "+strconv.Itoa(file.Action))
 }
 // /usr/bin/time must have genuinely emitted both real wall and max RSS;
 // typed standalone original proof excludes incomplete resource runs.
 cost:=oneLine(content,"R6G_SINGLE_B10_WALL_SECONDS")
 wall,err:=strconv.ParseFloat(field(cost,"R6G_SINGLE_B10_WALL_SECONDS"),64)
 if err!=nil||wall<=0{bad("invalid measured real elapsed wall time")}
 if num(cost,"PEAK_RSS_KIB")==0{bad("invalid measured peak RAM")}
 return visited,skipped
}
func main(){
 if len(os.Args)!=2{bad("usage: source_b10_18shard_manifest.json")}
 path:=os.Args[1]
 b,err:=os.ReadFile(path);if err!=nil{bad("manifest unavailable")}
 var m Manifest
 if e:=json.Unmarshal(b,&m);e!=nil{bad("invalid manifest JSON")}
 if m.Schema!="cuberev-025-r6h-original-source-b10-18shard-v1"||
   m.GoalRadius!=6||m.SourceRadius!=10||
   m.Source!="WCA_Seoul_Summer_2026_333_Final_A1_original"||
   !m.RootChecked||len(m.CommitSHA)!=40||len(m.Shards)!=18{
   bad("wrong actual source context, unpinned revision, missing root or incomplete 18-shard cover")
 }
 for _,c:=range m.CommitSHA{
  if !strings.ContainsRune("0123456789abcdef",c){bad("commit pin not lowercase SHA40")}
 }
 present:=make(map[int]bool)
 var visited,skipped uint64
 for _,sh:=range m.Shards{
  if present[sh.Action]{bad("duplicate first action")}
  present[sh.Action]=true
  v,omitted:=physicalShard(sh,filepath.Dir(path))
  visited+=v;skipped+=omitted
 }
 for a:=0;a<18;a++{if !present[a]{bad("missing first action "+strconv.Itoa(a))}}
 const expected uint64=285921738920
 if 11+visited+skipped!=expected {
  bad("all first-action disjoint cylinders + 11 source-root calls do not cover B10")
 }
 // No counterfeit "independent physical re-enumeration" claim. The
 // attached raw logs and pinned commits still require actual GitHub cross
 // verification, and the abstract prefix-cut proof must be paired with
 // the original physical kernel/normal-form simulation argument.
 fmt.Printf("P0R6H_ALL_18_SOURCE_B10_LOG_RECEIPTS_CONDITIONALLY_AGGREGATED FULL_ORIGINAL_SOURCE_COVER %d DISTINCT_FIRST_ACTIONS 18 SOURCE_ROOT_CALLS 11 SOURCE_TOTAL_RECURSIVE_CALLS %d ACTUAL_VISITS_EXCLUDING_ROOT %d SAFELY_OMITTED %d PHYSICAL_FULL_GOAL_MEETS 0 PINNED_COMMIT %s REQUIRES_EXTERNAL_GITHUB_RUN_AUTHENTICITY_CHECK 1 NO_INDEPENDENT_SECOND_PHYSICS_ENGINE 1\n",1,expected,visited,skipped,m.CommitSHA)
}
