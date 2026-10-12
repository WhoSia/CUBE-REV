// CUBE-REV 0.24 P1-R4: Conway-style subgroup-boundary word reduction.
// Actual official 20 HTM WCA state, aim for any whole-54-sticker legal solution
// of normalized <=19 moves. Does NOT prove 19 is the global minimum.
// Search raw 20-turn two-phase concatenations, allowing cancellation at phase
// boundary when exact group product is shorter <=19; original 54 sticker replay.
#define main old_P1R3_main
#include "../p1_r3_true_54_facelet_multiaxis_dr_cpp/main.cpp"
#undef main
struct BoundaryTarget19 {
  uint64_t nodes1=0,nodes2=0,contacts=0,p2_calls=0;
  bool stopped=false,found=false;int maxTimeSeconds=14;
  Clock::time_point started;
  vector<int>p1,p2,w1,w2;
  bool overBudget(){if(nodes1>750000000||nodes2>150000000)return true;
    return chrono::duration<double>(Clock::now()-started).count()>maxTimeSeconds;}
  bool secondDFS(int cp,int ud,int es,int depth,int bound,int last){
    nodes2++;if((nodes2&0x1FFF)==0 && overBudget()){stopped=true;return false;}
    if(depth+phase2H(cp,ud,es)>bound)return false;
    if(cp==0&&ud==0&&es==0){
      vector<int>candidate=p1;
      candidate.insert(candidate.end(),p2.begin(),p2.end());
      candidate=normalizeLegalHTM(candidate);
      if(candidate.size()<=19){w2=p2;return true;}
      return false;
    }
    if(depth>=bound)return false;
    for(int a=0;a<10;a++){
      const int m=moves2[a];if(!canonical(last,m))continue;
      p2.push_back(m);
      if(secondDFS(cpTurn[cp][a],udTurn[ud][a],esTurn[es][a],depth+1,bound,m))return true;
      p2.pop_back();if(stopped)return false;
    }return false;
  }
  bool second(Cube s,int p1len){
    int cp=rankCP(s),ud=rankUD(s),es=rankES(s);
    int h=phase2H(cp,ud,es);if(p1len+h>20)return false;
    p2_calls++;
    for(int b=h;b<=20-p1len;b++){
       p2.clear();if(secondDFS(cp,ud,es,0,b,-1))return true;
       if(stopped)return false;
    }return false;
  }
  bool firstDFS(Cube s,int co,int eo,int sl,int d,int bound,int last){
    nodes1++;if((nodes1&0x1FFF)==0 && overBudget()){stopped=true;return false;}
    int h=max<int>(pdbCOslice[co*495+sl],pdbEOslice[eo*495+sl]);
    if(d+h>bound)return false;
    if(h==0){
       contacts++;
       if(second(s,d)) {w1=p1;found=true;return true;}
       if(stopped)return false;
    }
    if(d==bound)return false;
    for(int a=0;a<18;a++){
      if(!canonical(last,a))continue;
      p1.push_back(a);
      if(firstDFS(composeCube(s,turn[a]),coTurn[co][a],eoTurn[eo][a],slTurn[sl][a],d+1,bound,a))return true;
      p1.pop_back();if(stopped)return false;
    }return false;
  }
  bool run(Cube s,int seconds){started=Clock::now();maxTimeSeconds=seconds;
    int co=coIndex(s),eo=eoIndex(s),sl=sliceID[sliceMask(s)];
    int h=max<int>(pdbCOslice[co*495+sl],pdbEOslice[eo*495+sl]);
    for(int b=h;b<=min(15,h+6);b++){
      p1.clear();if(firstDFS(s,co,eo,sl,0,b,-1))return true;
      if(stopped)return false;
    }return false;
  }
};

int main(){try{initTurns();initPhase1();initPhase2();auto scramble=parse("R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2");Stickers base=solvedStickers();for(int m:scramble)physicalTurn(base,names[m]);uint64_t all1=0,all2=0,allContacts=0,eligible=0;
for(int axis:{-1,0,2}){
if(getenv("P1R4_ONLY_LR") && axis!=2)continue;auto f=inFrame(base,axis);BoundaryTarget19 t;bool ok=t.run(fromStickers(f.cube),18);all1+=t.nodes1;all2+=t.nodes2;allContacts+=t.contacts;eligible+=t.p2_calls;
cout<<"BOUNDARY_AXIS "<<(axis<0?"UD":axis==0?"FB":"LR")<<" FOUND "<<ok<<" CONTACTS "<<t.contacts<<" P2_CALLS "<<t.p2_calls<<" NODES1 "<<t.nodes1<<" NODES2 "<<t.nodes2<<" STOPPED "<<t.stopped<<"\n";
if(ok){
  auto w=t.w1;w.insert(w.end(),t.w2.begin(),t.w2.end());
  const int p1len=int(t.w1.size()), p2len=int(t.w2.size());
  auto original=normalizeLegalHTM(backToOriginal(w,f));
  if(p1len!=12||p2len!=8||w.size()!=20||original.size()!=19||t.w1.back()/3!=t.w2.front()/3)
    throw runtime_error("frozen boundary group-word witness regression failed");
  if(find(moves2.begin(),moves2.end(),t.w1.back())!=moves2.end())
    throw runtime_error("DR entrance final letter must be outside G1 alphabet");
  // Verify that this is genuinely the FIRST G1 entry on the winning
  // source prefix, not a later arbitrary subgroup re-entrance.
  auto prefixCube=fromStickers(f.cube);
  for(size_t k=0;k<t.w1.size();k++){
    prefixCube=composeCube(prefixCube,turn[t.w1[k]]);
    if(k+1<t.w1.size() && phase1H(prefixCube)==0)
      throw runtime_error("witness was already in G1 before its stated first arrival");
  }
  if(phase1H(prefixCube)!=0)throw runtime_error("winner did not reach genuine G1");
  if(names[t.w1.back()]!="B"||names[t.w2.front()]!="B2")
    throw runtime_error("specific original-stage B B2 rewrite has drifted");
  cout<<"CONWAY_GROUP_FIRST_G1_ENTRY_CHECK PASS FINAL_OUTSIDE_SUBGROUP_GENERATOR B BOUNDARY B_B2_TO_B_PRIME\n";

  cout<<"SUBGROUP_CROSS_BOUNDARY_LOCAL "<<names[t.w1.back()]<<" "<<names[t.w2.front()]<<" REDUCED_LEN "<<original.size()<<" PHASE1_LEN "<<p1len<<" PHASE2_LEN "<<p2len<<" RAW_LEN "<<w.size()<<"\n";
  if(original.size()>19||!physicalSolves(scramble,original))throw runtime_error("bad full original physical replay");cout<<"BOUNDARY_19_OR_LESS_SOURCE_FULL_CUBE_WITNESS "<<join(original)<<" LENGTH "<<original.size()<<"\n";return 0;}
}cout<<"BOUNDARY_NO_TARGET19_WITHIN_RAW20_AND_ACTUAL_AXIS_LOWER_PLUS6_SCOPE NODES1 "<<all1<<" NODES2 "<<all2<<" CONTACTS "<<allContacts<<" PHASE2_CHECKS "<<eligible<<"\n";return 0;}catch(exception&e){cerr<<"ERROR "<<e.what()<<"\n";return 1;}}