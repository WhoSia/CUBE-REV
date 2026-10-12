// CUBE-REV 0.24 P1-R5 — authentic official 3x3 Final A1 exact legal
// 18 HTM challenge through 3 conjugate DR grammars with honest horizon.
// Original cubie engine from inherited C++ physical 54-sticker P1-R3.
// Does NOT prove unrestricted 18HTM optimality if no solution is found.
#define main inherited_original_p1r3_main
#include "../p1_r3_true_54_facelet_multiaxis_dr_cpp/main.cpp"
#undef main
#include "group_trace_rewrite.hpp"

struct P1R5Target18 {
  uint64_t nodes1=0, nodes2=0, contacts=0, phase2Attempts=0, normalizedCandidates=0;
  bool stopped=false, found=false, rewriteBudgetHold=false; int maxSeconds=25, maxPhase1=13;
  Clock::time_point began;
  vector<int>p1,p2,winning1,winning2,winningNormalized;
  bool cap(){
    // Stop is always reported and never recorded as exhaustive.
    return nodes1>2000000000ULL || nodes2>500000000ULL || chrono::duration<double>(Clock::now()-began).count()>maxSeconds;
  }
  bool phase2DFS(int cp,int ud,int es,int depth,int bound,int last){
    ++nodes2; if((nodes2&0x3fff)==0&&cap()){stopped=true;return false;}
    if(depth+phase2H(cp,ud,es)>bound)return false;
    if(cp==0&&ud==0&&es==0){
      vector<int>word=p1;word.insert(word.end(),p2.begin(),p2.end());
      auto closure=traceRewrite(word,18,50000);
      ++normalizedCandidates;
      if(!closure.exhausted){rewriteBudgetHold=true;stopped=true;return false;}
      if(closure.success){winningNormalized=closure.word;winning1=p1;winning2=p2;found=true;return true;}
      return false;
    }
    if(depth==bound)return false;
    for(int j=0;j<10;j++){
      const int m=moves2[j]; if(!canonical(last,m))continue;
      // Bound cost at phase boundary. A full solution can reduce raw by ONE
      // across a true first-DR-entry last-side-quarter and phase2 first-halfturn.
      if(depth==0 && !p1.empty() && m/3!=p1.back()/3 && int(p1.size())+bound>20)continue;
      p2.push_back(m);
      if(phase2DFS(cpTurn[cp][j],udTurn[ud][j],esTurn[es][j],depth+1,bound,m))return true;
      p2.pop_back();if(stopped)return false;
    }
    return false;
  }
  bool phase2(Cube s,int p1len){
    int cp=rankCP(s),ud=rankUD(s),es=rankES(s),h=phase2H(cp,ud,es);
    if(p1len+h>20)return false;
    ++phase2Attempts;
    for(int b=h;b<=20-p1len;b++){
      p2.clear();if(phase2DFS(cp,ud,es,0,b,-1))return true;
      if(stopped)return false;
    }
    return false;
  }
  bool dfs(Cube s,int co,int eo,int sl,int depth,int bound,int last){
    nodes1++;if((nodes1&0x3fff)==0&&cap()){stopped=true;return false;}
    int h=max<int>(pdbCOslice[co*495+sl],pdbEOslice[eo*495+sl]);
    if(depth+h>bound)return false;
    if(h==0){contacts++;if(phase2(s,depth))return true;if(stopped)return false;}
    if(depth==bound)return false;
    for(int j=0;j<18;j++){
      if(!canonical(last,j))continue;
      p1.push_back(j);
      if(dfs(composeCube(s,turn[j]),coTurn[co][j],eoTurn[eo][j],slTurn[sl][j],depth+1,bound,j))return true;
      p1.pop_back();if(stopped)return false;
    }return false;
  }
  bool run(Cube s,int timeLimit,int maxD){
    began=Clock::now();maxSeconds=timeLimit;maxPhase1=maxD;
    int co=coIndex(s),eo=eoIndex(s),sl=sliceID[sliceMask(s)];
    int h=max<int>(pdbCOslice[co*495+sl],pdbEOslice[eo*495+sl]);
    cerr<<"INITIAL_ADMISSIBLE_DR_LOWER "<<h<<" EXPLICIT_MAX_PHASE1 "<<maxPhase1<<" TARGET_NORM18\n";
    for(int b=h;b<=maxPhase1;b++){
      uint64_t before1=nodes1,before2=nodes2,beforeC=contacts;
      p1.clear();if(dfs(s,co,eo,sl,0,b,-1)){cout<<"PHASE1_BOUND "<<b<<" COMPLETED 0 FOUND 1\n";return true;}
      cout<<"PHASE1_BOUND "<<b<<" COMPLETED "<<(!stopped)<<" FOUND 0 NODES1 "<<nodes1-before1<<" NODES2 "<<nodes2-before2<<" CONTACTS "<<contacts-beforeC<<"\n"<<flush;
      if(stopped)return false;
    }return false;
  }
};
int main(int argc,char**argv){
 try{
  auto t=Clock::now();initTurns();initPhase1();initPhase2();
  cerr<<"P1R5_PDB_SOURCE_READY_SECONDS "<<chrono::duration<double>(Clock::now()-t).count()<<"\n";
  auto scramble=parse("R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2");
  auto base=solvedStickers();for(int m:scramble)physicalTurn(base,names[m]);
  int seconds=argc>1?stoi(argv[1]):20,maxdepth=argc>2?stoi(argv[2]):13;
  string axis=argc>3?argv[3]:"ALL";bool anyStop=false;
  for(int f:{2,0,-1}){
   string name=f==2?"LR":f==0?"FB":"UD";
   if(axis!="ALL"&&axis!=name)continue;
   auto ff=inFrame(base,f);P1R5Target18 engine;
   bool won=engine.run(fromStickers(ff.cube),seconds,maxdepth);anyStop|=engine.stopped;
   cout<<"P1R5_AXIS "<<name<<" TARGET18_FOUND "<<won<<" RESOURCE_STOP "<<engine.stopped<<" TRACE_CLOSURE_HOLD "<<engine.rewriteBudgetHold
       <<" NODES1 "<<engine.nodes1<<" NODES2 "<<engine.nodes2<<" CONTACTS "<<engine.contacts
       <<" DOWNSTREAM_ATTEMPTS "<<engine.phase2Attempts<<" COMPLETE_WORDS_TESTED "<<engine.normalizedCandidates<<"\n"<<flush;
   if(won){auto w=engine.winning1;w.insert(w.end(),engine.winning2.begin(),engine.winning2.end());
     auto actual=normalizeLegalHTM(backToOriginal(engine.winningNormalized,ff));
     if(actual.size()>18||!physicalSolves(scramble,actual))throw runtime_error("original physical 54-facelet violation");
     cout<<"FULL_SOURCE_REAL_18HTM_WITNESS "<<join(actual)<<" LENGTH "<<actual.size()<<"\n";
     return 0;
   }
  }
  if(anyStop)cout<<"P1R5_RESOURCE_LIMIT_PARTIAL_HOLD_NOT_A_FINITE_EXCLUSION_CERTIFICATE\n";
  else cout<<"P1R5_NO_18_WITNESS_WITHIN_EXPLICIT_RESOURCE_AND_AXIS_BOUNDS_NOT_GLOBAL_DISTANCE_CERTIFICATE\n";
 }catch(const exception&e){cerr<<"ERROR "<<e.what()<<"\n";return 2;}
}