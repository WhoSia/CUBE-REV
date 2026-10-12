// CUBE-REV 0.24 P1-R6: SOURCE-COMPLETE GLOBAL 18 HTM finite ball certificate.
// All 8 corners + 12 edges, actual legal 54-facelet sourced turn maps.
// NOT a DR/HTR-constrained search: all eighteen moves are included.
// No probabilistic hash collision is allowed to cause false nonintersection:
// keys preserve all original cubie permutation and orientation bits exactly.
#define main inherited_p1r3_main
#include "../p1_r3_true_54_facelet_multiaxis_dr_cpp/main.cpp"
#undef main
#include <chrono>

using U64=uint64_t;
struct FullKey { U64 c,e; bool operator==(FullKey const&o)const{return c==o.c&&e==o.e;} };
struct FullKeyHash { size_t operator()(FullKey const&k)const noexcept { U64 a=k.c+0x9e3779b97f4a7c15ULL; a=(a^(a>>30))*0xbf58476d1ce4e5b9ULL; a=(a^(a>>27))*0x94d049bb133111ebULL; a^=a>>31; U64 b=k.e+0x3c79ac492ba7b653ULL; b=(b^(b>>27))*0x3c79ac492ba7b653ULL; b=(b^(b>>33))*0x1c69b3f74ac4ae35ULL; return static_cast<size_t>(a^(b^(b>>27))); } };
FullKey exactKey(Cube const&s){
 U64 c=0,e=0;
 for(int i=0;i<8;i++){if(s.cp[i]>=8||s.co[i]>=3)throw runtime_error("bad original corner digit");c|=U64(s.cp[i])<<(3*i);c|=U64(s.co[i])<<(24+2*i);}
 for(int i=0;i<12;i++){if(s.ep[i]>=12||s.eo[i]>=2)throw runtime_error("bad original edge digit");e|=U64(s.ep[i])<<(4*i);e|=U64(s.eo[i])<<(48+i);}
 return {c,e};
}
Cube cubeFromKey(FullKey key){Cube s{};for(int i=0;i<8;i++){s.cp[i]=(key.c>>(3*i))&7;s.co[i]=(key.c>>(24+2*i))&3;}for(int i=0;i<12;i++){s.ep[i]=(key.e>>(4*i))&15;s.eo[i]=(key.e>>(48+i))&1;}return s;}
void assertExactPackedState(Cube const&s){const Cube x=cubeFromKey(exactKey(s));if(x.cp!=s.cp||x.co!=s.co||x.ep!=s.ep||x.eo!=s.eo)throw runtime_error("KEY IS NOT LOSSLESS");}

// Complete right-Cayley 18HTM goal ball, collision-free equality.
struct GlobalCourt{
 unordered_set<FullKey,FullKeyHash> goal;
 uint64_t nodesGoal=0,nodesSource=0,meetCount=0;
 vector<uint64_t> layerGoal,layerSource;
 vector<Cube> previous, next;
 int goalRadius=5,sourceRadius=5;
 Clock::time_point started;
 double secondsBudget=75;
 bool cut=false,match=false;
 vector<int>path,foundPath;
 bool expired(){return chrono::duration<double>(Clock::now()-started).count()>secondsBudget;}
 bool build(int rad){
  goalRadius=rad;
  previous={solved()}; goal.reserve(rad>=6?9400000:720000);
  goal.insert(exactKey(solved()));layerGoal={1};
  for(int d=1;d<=rad;d++){
   next.clear();
   // BFS expands each distinct full cubie configuration with all legal turns.
   for(auto const&s:previous){
    if((++nodesGoal%8192)==0&&expired()){cut=true;return false;}
    for(int a=0;a<18;a++){
     Cube v=composeCube(s,turn[a]);FullKey key=exactKey(v);
     if(goal.insert(key).second)next.push_back(v);
    }
   }
   layerGoal.push_back(next.size());
   if(d==4 && layerGoal.back()!=43239)throw runtime_error("EXACT GLOBAL HTM DEPTH4 REGRESSION");
   if(d==5 && layerGoal.back()!=574908)throw runtime_error("EXACT GLOBAL HTM DEPTH5 REGRESSION");
   if(d==6 && layerGoal.back()!=7618438)throw runtime_error("EXACT GLOBAL HTM DEPTH6 REGRESSION");
   previous.swap(next);
   cout<<"P1R6_GLOBAL_FULL18_GOAL_LAYER "<<d<<" EXACT_DISTINCT "<<layerGoal.back()<<" TOTAL "<<goal.size()<<"\n"<<flush;
  }
  return true;
 }
 bool visit(Cube const&s,int d,int limit,int last){
  ++nodesSource;
  if((nodesSource&0xffff)==0 &&expired()){cut=true;return false;}
  if(goal.find(exactKey(s))!=goal.end()){
   match=true;foundPath=path;return true;
  }
  if(d==limit)return false;
  for(int a=0;a<18;a++){
    if(!canonical(last,a))continue; // proven group-complete normal form: combine same-face, reorder commuting opposite faces
    path.push_back(a);
    if(visit(composeCube(s,turn[a]),d+1,limit,a))return true;
    path.pop_back();if(cut)return false;
  }
  return false;
 }
 bool check(Cube const&source,int sourceRad){
  sourceRadius=sourceRad;
  for(int depth=0;depth<=sourceRad;depth++){
   auto before=nodesSource;path.clear();
   bool result=visit(source,0,depth,-1);
   layerSource.push_back(nodesSource-before);
   cout<<"P1R6_GLOBAL_FULL18_SOURCE_BOUND "<<depth<<" COMPLETED "<<(!cut?1:0)<<" VISITS "<<(nodesSource-before)<<" MATCH "<<(result?1:0)<<"\n"<<flush;
   if(result||cut)return result;
  }
  return false;
 }
};
int main(int argc,char**argv){
 try{
  int rg=argc>1?stoi(argv[1]):5,rs=argc>2?stoi(argv[2]):6;
  int seconds=argc>3?stoi(argv[3]):75;
  if(rg<0||rg>6||rs<0||rs>7||seconds<=0)throw runtime_error("certification domain rg<=6, rs<=7");
  initTurns();
  string literal="R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2";
  auto sourceMoves=parse(literal);Cube source=cubeAfter(sourceMoves);
  Stickers original=solvedStickers();for(auto t:sourceMoves)physicalTurn(original,names[t]);
  const Cube sourceDirect=fromStickers(original);
  if(!(exactKey(sourceDirect)==exactKey(source)))throw runtime_error("REAL 54-STICKER SOURCE DISAGREES WITH CUBIE TRANSITIONS");
  assertExactPackedState(source);
  {Cube state=solved();uint32_t x=0xC0BEE6A1u;for(int k=0;k<256;k++){x^=x<<13;x^=x>>17;x^=x<<5;state=composeCube(state,turn[x%18]);assertExactPackedState(state);}}
  auto eighteen=parse("F U F D' R' F' L' F' D' L B L2 F2 U2 L2 U F' R2");
  if(eighteen.size()!=18||!physicalSolves(sourceMoves,eighteen))throw runtime_error("PRIOR EXACT ORIGINAL EIGHTEEN SOLVE FAIL");
  GlobalCourt work;work.started=Clock::now();work.secondsBudget=seconds;
  cout<<"P1R6_SOURCE_REAL_ORIGINAL_WCA_SCRAMBLE "<<literal<<"\n";
  cout<<"P1R6_SOURCE_ORIGINAL_54_FACELET_CUBIE_ROUNDTRIP PASS ALL_EIGHT_CORNERS_TWELVE_EDGES_LOSSLESS_PACKED_EQUIVALENCE PASS\n";
  cout<<"P1R6_EXISTING_REAL_18HTM_COMPLETION_INDEPENDENT_54_FACELET PASS UPPER_BOUND 18\n";
  if(!work.build(rg)){
    cout<<"P1R6_SOURCE_COMPLETE_GLOBAL_BALL RESOURCE_HOLD_STAGE_GOAL\n";return 2;
  }
  bool intersection=work.check(source,rs);
  if(work.cut){cout<<"P1R6_SOURCE_COMPLETE_GLOBAL_BALL RESOURCE_HOLD_STAGE_SOURCE\n";return 2;}
  if(intersection){cout<<"P1R6_FULL18_INTERSECTION_FOUND WITHIN_DISTANCE "<<(rg+rs)<<" SOURCE_PREFIX "<<join(work.foundPath)<<"\n";return 0;}
  cout<<"P1R6_FULL18_SOURCE_COMPLETE_EXCLUSION COMPLETE 1 ALL18LEGAL_ACTIONS 1 ALL_ORIGINAL_CUBIES 1 GOAL_RADIUS "<<rg<<" SOURCE_RADIUS "<<rs<<" EXCLUDED_ALL_WORDS_LENGTH_LEQ "<<(rg+rs)<<" GOAL_STATES "<<work.goal.size()<<" SOURCE_NODES "<<work.nodesSource<<" HASH_COLLISION_FALSE_POSITIVE_SAFE 1 NO_SOURCE_STABILIZER_SHORTCUT_USED 1\n";
  cout<<"P1R6_CURRENT_PROOF_DISTANCE_BOUNDS LOWER "<<(rg+rs+1)<<" UPPER 18 GLOBAL17_NOT_YET_EXCLUDED "<<((rg+rs+1)<=17?1:0)<<"\n";
  return 0;
 }catch(exception const&e){cerr<<"P1R6_ERROR "<<e.what()<<"\n";return 3;}
}