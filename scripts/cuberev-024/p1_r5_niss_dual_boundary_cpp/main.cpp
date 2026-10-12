// CUBE-REV 0.24 P1-R5 — authentic official 3x3 Final A1 exact legal
// 18 HTM challenge through 3 conjugate DR grammars with honest horizon.
// Original cubie engine from inherited C++ physical 54-sticker P1-R3.
// Does NOT prove unrestricted 18HTM optimality if no solution is found.
#define main inherited_original_p1r3_main
#include "../p1_r3_true_54_facelet_multiaxis_dr_cpp/main.cpp"
#undef main
#include "../p1_r5_conway_target18_cpp/group_trace_rewrite.hpp"

struct P1R5Target18 {
  uint64_t nodes1=0, nodes2=0, contacts=0, phase2Attempts=0, normalizedCandidates=0;
  bool stopped=false, found=false, rewriteBudgetHold=false; int maxSeconds=25, maxPhase1=13;
  Clock::time_point began;
  vector<int>p1,p2,winning1,winning2,winningNormalized; Frame currentFrame; int premoveOriginal=0; vector<int>originalScramble;
  bool cap(){
    // Stop is always reported and never recorded as exhaustive.
    return nodes1>2000000000ULL || nodes2>500000000ULL || chrono::duration<double>(Clock::now()-began).count()>maxSeconds;
  }
  bool phase2DFS(int cp,int ud,int es,int depth,int bound,int last){
    ++nodes2; if((nodes2&0x3fff)==0&&cap()){stopped=true;return false;}
    if(depth+phase2H(cp,ud,es)>bound)return false;
    if(cp==0&&ud==0&&es==0){
      vector<int>word=p1;word.insert(word.end(),p2.begin(),p2.end());
      auto absolute=backToOriginal(word,currentFrame); absolute.push_back(premoveOriginal);
      auto closure=traceRewrite(absolute,18,50000);
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
      // NISS: no local-frame boundary-face prefilter; source-side suffix may merge.
      p2.push_back(m);
      if(phase2DFS(cpTurn[cp][j],udTurn[ud][j],esTurn[es][j],depth+1,bound,m))return true;
      p2.pop_back();if(stopped)return false;
    }
    return false;
  }
  bool phase2(Cube s,int p1len){
    int cp=rankCP(s),ud=rankUD(s),es=rankES(s),h=phase2H(cp,ud,es);
    if(p1len+h>19)return false;
    ++phase2Attempts;
    for(int b=h;b<=19-p1len;b++){
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
  initTurns();initPhase1();initPhase2();
  auto scramble=parse("R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2");
  int seconds=argc>1?stoi(argv[1]):2,maxDepth=argc>2?stoi(argv[2]):11;
  int preset=argc>3?stoi(argv[3]):-1;
  int tests=0;uint64_t total1=0,total2=0,totalContacts=0;
  for(int q=0;q<18;q++){
   if(preset>=0&&q!=preset)continue;
   Stickers shifted=solvedStickers();
   physicalTurn(shifted,names[q]);
   for(int move:scramble)physicalTurn(shifted,names[move]);
   for(int axis : {2,0,-1}){
    auto f=inFrame(shifted,axis);
    P1R5Target18 t;t.currentFrame=f;t.premoveOriginal=q;t.originalScramble=scramble;
    bool won=t.run(fromStickers(f.cube),seconds,maxDepth);
    total1+=t.nodes1;total2+=t.nodes2;totalContacts+=t.contacts;
    cout<<"PREMOVE_CASE "<<names[q]<<" AXIS "<<(axis==2?"LR":axis==0?"FB":"UD")
      <<" WIN "<<won<<" CUT "<<t.stopped<<" LAST_NODES1 "<<t.nodes1<<" LAST_NODES2 "<<t.nodes2
      <<" ORIGINAL_ENDPOINT_CONTRACT q*S*x=e implies S*x*q=e"<<"\n"<<flush;
    tests++;
    if(won){
      auto w=normalizeLegalHTM(t.winningNormalized);
      if(w.size()>18||!physicalSolves(scramble,w))throw runtime_error("NISS source full 54 facelets did not solve");
      cout<<"NISS_FULL_18_OR_LESS_REAL_54_FACELET_SOLUTION "<<join(w)<<" LENGTH "<<w.size()<<" PREMOVE "<<names[q]<<" AXIS "<<(axis==2?"LR":axis==0?"FB":"UD")<<"\n"<<flush;
      return 0;
    }
   }
  }
  cout<<"NISS_ONE_PREMOVE_SCOPE_RESULT NO_18_FOUND TESTS "<<tests<<" SUM_NODES1 "<<total1<<" SUM_NODES2 "<<total2
    <<" SUM_CONTACTS "<<totalContacts<<" NOT_AN_UNRESTRICTED_18HTM_DISTANCE_PROOF\n";
 }catch(exception&e){cerr<<"ERROR "<<e.what()<<"\n";return 2;}
}