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
  vector<int>p1,p2,winning1,winning2,winningNormalized; Frame currentFrame; vector<int>premovesOriginal; vector<int>originalScramble;
  bool cap(){
    // Stop is always reported and never recorded as exhaustive.
    return nodes1>2000000000ULL || nodes2>500000000ULL || chrono::duration<double>(Clock::now()-began).count()>maxSeconds;
  }
  bool phase2DFS(int cp,int ud,int es,int depth,int bound,int last){
    ++nodes2; if((nodes2&0x3fff)==0&&cap()){stopped=true;return false;}
    if(depth+phase2H(cp,ud,es)>bound)return false;
    if(cp==0&&ud==0&&es==0){
      vector<int>word=p1;word.insert(word.end(),p2.begin(),p2.end());
      auto absolute=backToOriginal(word,currentFrame); absolute.insert(absolute.end(),premovesOriginal.begin(),premovesOriginal.end());
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
    if(p1len+h>18)return false;
    ++phase2Attempts;
    for(int b=h;b<=18-p1len;b++){
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
int main(int argc,char**argv){try{
 initTurns();initPhase1();initPhase2();
 auto scramble=parse("R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2");
 int seconds=argc>1?stoi(argv[1]):2,maxDepth=argc>2?stoi(argv[2]):10;
 uint64_t totals1=0,totals2=0,contacts=0;int checked=0,cuts=0,found=0;
 for(int a=0;a<18;a++)for(int b=0;b<18;b++){
  if(!canonical(a,b))continue;
  Stickers shifted=solvedStickers();physicalTurn(shifted,names[a]);physicalTurn(shifted,names[b]);
  for(int move:scramble)physicalTurn(shifted,names[move]);
  for(int axis:{2,0,-1}){
   auto f=inFrame(shifted,axis);
   P1R5Target18 t;t.currentFrame=f;t.premovesOriginal={a,b};t.originalScramble=scramble;
   bool solved18=t.run(fromStickers(f.cube),seconds,maxDepth);
   checked++;totals1+=t.nodes1;totals2+=t.nodes2;contacts+=t.contacts;cuts+=t.stopped;
   if(solved18){
     auto p1original=backToOriginal(t.winning1,f);
     auto p2original=backToOriginal(t.winning2,f);
     vector<int>phase1Check={a,b};phase1Check.insert(phase1Check.end(),scramble.begin(),scramble.end());
     phase1Check.insert(phase1Check.end(),p1original.begin(),p1original.end());
     Cube drReached=cubeAfter(phase1Check);
     if(phase1H(drReached)!=0)throw runtime_error("NISS reached candidate is not genuine DR member");
     int certifiedPhase2Lower=phase2H(rankCP(drReached),rankUD(drReached),rankES(drReached));
     if(certifiedPhase2Lower!=6 || p2original.size()!=6)throw runtime_error("independent quotient PDB fails to certify actual six-turn DR suffix");
     cout<<"NISS2_EXACT_DR_SUFFIX_PDB_SANDWICH LOWER "<<certifiedPhase2Lower<<" ACTUAL_WORD_LEN "<<p2original.size()<<" TRUE_DR_MEMBER 1\n";
     vector<int>raw=p1original;raw.insert(raw.end(),p2original.begin(),p2original.end());raw.push_back(a);raw.push_back(b);
     if(!physicalSolves(scramble,raw))throw runtime_error("NISS2 raw group identity incorrect for original whole cube");
     auto word=normalizeLegalHTM(t.winningNormalized);
     if(word.size()>18||!physicalSolves(scramble,word))throw runtime_error("two premoves invalid full original 54-sticker witness");
     cout<<"NISS2_ACTUAL_GROUP_FACTOR_CERTIFICATE P1_LEN "<<p1original.size()<<" P2_LEN "<<p2original.size()<<" SUFFIX_PREMOVES_LEN 2 RAW_LEN "<<raw.size()<<" TRACENORM_LEN "<<word.size()<<"\n";
     cout<<"NISS2_P1_ORIGINAL "<<join(p1original)<<"\n";
     cout<<"NISS2_P2_ORIGINAL "<<join(p2original)<<"\n";
     cout<<"NISS2_RAW_ORIGINAL_COMPLETE_WORD "<<join(raw)<<"\n";
     cout<<"NISS2_SOURCE_VERIFIED_COMPLETE_18_WITNESS "<<join(word)<<" LENGTH "<<word.size()
         <<" PREMOVES "<<names[a]<<" "<<names[b]<<" AXIS "<<(axis==2?"LR":axis==0?"FB":"UD")<<"\n";
     return 0;
   }
   if(t.stopped)cout<<"NISS2_RESOURCE_CUT PREMOVES "<<names[a]<<" "<<names[b]<<" AXIS "<<(axis==2?"LR":axis==0?"FB":"UD")<<"\n";
  }
  if((checked%72)==0)cout<<"NISS2_PROGRESS TESTS "<<checked<<" NODES1 "<<totals1<<" CUTS "<<cuts<<"\n"<<flush;
 }
 cout<<"NISS2_SOURCE_SCOPE_DONE TESTS "<<checked<<" CUTS "<<cuts<<" WINS "<<found
  <<" SUM_NODES1 "<<totals1<<" SUM_NODES2 "<<totals2<<" CONTACTS "<<contacts
  <<" NOT_A_GLOBAL_18HTM_DISTANCE_PROOF\n";
 return 0;
}catch(exception&e){cerr<<"ERROR "<<e.what()<<"\n";return 2;}}