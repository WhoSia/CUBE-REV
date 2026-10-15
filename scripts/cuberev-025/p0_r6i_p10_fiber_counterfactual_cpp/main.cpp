// CUBE-REV P0-R6I-P10 genuine original full CP/CO/EP/EO
// source-B10 matched baseline-marginal vs exact-corner-fiber physical
// counterfactual. The exact conditional fiber membership oracle is
// implemented via the ALREADY PRESENT complete B6 full-cubie hash set:
// it adds NO new precomputed fiber index and must not be called a new
// sparse compressed cache. The marginal case matches inherited R6E.
#define CUBEREV_P9_AS_LIBRARY
#include "../p0_r6i_p9_projection_cpp/main.cpp"
#undef CUBEREV_P9_AS_LIBRARY

struct MeasuredJointCourt : PackedOrderedCourt {
 bool exactFiber=false;
 uint64_t dualMarginalChecks=0, fullConditionalChecks=0;
 uint64_t invalidJointCandidates=0, oneMarginalPass=0,oneExactRejected=0;
 bool measuredVisit(Cube const&s,int depth,int limit,int last){
  if(limit-depth==1)return jointVisit(s,depth,limit,last);
  ++visits;
  if((visits&0xffff)==0&&court.expired()){cut=true;return false;}
  const FullKey key=exactKey(s);
  if(c6.find(key.c)!=c6.end()){
   ++fullQueries;
   if(court.goal.find(key)!=court.goal.end()){
    ++fullHits;meet=true;foundPrefix=path;foundKey=key;return true;
   }
  }
  if(depth==limit)return false;
  if(limit-depth==2){
   ++orderedPairParents;
   for(int a=0;a<18;a++){
    if(!canonical(last,a))continue;
    const Cube next=composeCube(s,turn[a]);
    const FullKey n=exactKey(next);
    bool onePossible=c6.find(n.c)!=c6.end()&&edge6.find(n.e)!=edge6.end();
    if(onePossible){
     ++oneMarginalPass;
     if(exactFiber){
      ++fullConditionalChecks;
      if(court.goal.find(n)==court.goal.end()){
       ++oneExactRejected;onePossible=false;
      }
     }
    }
    bool twoPossible=false;
    if(c7.find(n.c)==c7.end())++earlyCorner7Rejections;
    else if(!onePossible){
     for(int b=0;b<18;b++){
      if(!canonical(a,b))continue;
      ++orderedPairChecks;
      ++cornerPackedChecks;
      ++secondFullCubeMovesAvoided;
      const Key64 c=cornerTurnPacked(n.c,b);
      if(c6.find(c)==c6.end())continue;
      ++edgePackedChecks;
      const Key64 e=edgeTurnPacked(n.e,b);
      if(edge6.find(e)==edge6.end())continue;
      ++dualMarginalChecks;
      if(exactFiber){
       ++fullConditionalChecks;
       if(court.goal.find(FullKey{c,e})==court.goal.end()){
        ++invalidJointCandidates;
        continue;
       }
      }
      ++orderedPairPasses;twoPossible=true;break;
     }
    }
    if(!onePossible&&!twoPossible){
     ++twoStepRejectedBranches;
     const uint64_t removed=canonicalSubtreeOne(a);
     skippedChildren+=removed;twoStepRejectedCalls+=removed;
     continue;
    }
    ++twoStepCandidateParents;
    path.push_back(a);
    if(jointVisit(next,depth+1,limit,a))return true;
    path.pop_back();
    if(cut)return false;
   }
   return false;
  }
  for(int a=0;a<18;a++){
   if(!canonical(last,a))continue;
   path.push_back(a);
   if(measuredVisit(composeCube(s,turn[a]),depth+1,limit,a))return true;
   path.pop_back();
   if(cut)return false;
  }
  return false;
 }
 void resetCounters(){
  visits=0;skippedChildren=0;fullHits=0;fullQueries=0;
  orderedPairChecks=0;edgePackedChecks=0;cornerPackedChecks=0;
  secondFullCubeMovesAvoided=0;earlyCorner7Rejections=0;
  twoStepRejectedBranches=0;twoStepRejectedCalls=0;
  twoStepCandidateParents=0;orderedPairParents=0;orderedPairPasses=0;
  dualMarginalChecks=0;fullConditionalChecks=0;
  invalidJointCandidates=0;oneMarginalPass=0;oneExactRejected=0;
  cut=false;meet=false;foundPrefix.clear();
 }
};
int main(int argc,char**argv){
 try{
  if(argc!=2)throw std::runtime_error("usage: seconds<=400");
  int seconds=std::stoi(argv[1]);
  if(seconds<5||seconds>400)throw std::runtime_error("time budget invalid");
  initTurns();
  const auto scramble=parse("R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2");
  const auto solution=parse("F U F D' R' F' L' F' D' L B L2 F2 U2 L2 U F' R2");
  const Cube source=cubeAfter(scramble);
  Stickers check=solvedStickers();for(int a:scramble)physicalTurn(check,names[a]);
  if(!(exactKey(source)==exactKey(fromStickers(check)))||
    !physicalSolves(scramble,solution)||physicallyAuditFastProjection()!=4608)
   throw std::runtime_error("original 54-sticker WCA source invalid");
  MeasuredJointCourt r;
  r.court.started=Clock::now();r.court.secondsBudget=seconds;
  if(!r.court.build(6)){std::cout<<"P10_COMPARISON_GOAL_HOLD\n";return 2;}
  r.project();r.prepareEdges();
  if(r.court.goal.size()!=8240087||r.c6.size()!=1405068||
     r.c7.size()!=6807696||r.edge6.size()!=7672278)
   throw std::runtime_error("original physical target cardinality drift");
  const auto digest=goalDigest(r.court,6,"");
  if(digest!="82fe545bcad3537c989ec22afce9d286926ddce5f4ef9428c0307951ec2d0979")
   throw std::runtime_error("original whole target SHA changed");
  const int first=12, second=0;
  Cube x=composeCube(composeCube(source,turn[first]),turn[second]);
  const auto startRss=rssKiB();
  for(int condition=0;condition<2;condition++){
   r.exactFiber=condition==1;
   r.resetCounters();
   const auto clock=std::chrono::steady_clock::now();
   for(int depth=2;depth<=10;depth++){
    r.path={first,second};
    if(r.measuredVisit(x,2,depth,second)){
     std::cout<<"P10_COMPARISON_TRUE_FULL_CUBIE_MEET HOLD_AND_NO_NEGATIVE_CERT\n";return 3;
    }
    if(r.cut||r.court.expired()){
     std::cout<<"P10_COMPARISON_RESOURCE_HOLD PHASE "<<condition<<"\n";return 2;
    }
   }
   auto expected=p8Weight(second,8);
   if(r.visits+r.skippedChildren!=expected||r.fullHits)
    throw std::runtime_error("marginal-vs-exact source B10 normal-form not full");
   // Original native R6E reference from independent P9 original physical
   // successful source B10 (12,0) (same 54-sticker/turn/court):
   if(condition==0&&(r.visits!=7353279ULL||r.skippedChildren!=1302849804ULL||
      r.orderedPairChecks!=88974568ULL||r.edgePackedChecks!=18087662ULL||
      r.fullQueries!=106665ULL))
    throw std::runtime_error("baseline marginal branch drift from earlier independently audited P9");
   const auto ms=std::chrono::duration<double,std::milli>(
      std::chrono::steady_clock::now()-clock).count();
   std::cout<<"P10_COMPARISON ORIGINAL_FIRST "<<first<<" SECOND "<<second
    <<" MODE "<<(condition?"EXACT_EXISTING_GOAL_FIBER":"INDEPENDENT_C6_E6_MARGINAL")
    <<" GOAL_SHA "<<digest<<" WORD_CALLS "<<expected
    <<" VISITED "<<r.visits<<" OMITTED "<<r.skippedChildren
    <<" PAIRS "<<r.orderedPairChecks<<" EDGE_CHECKS "<<r.edgePackedChecks
    <<" FULL_QUERIES "<<r.fullQueries<<" DUAL_MARGINAL_PAIR_PASSES "<<r.dualMarginalChecks
    <<" EXACT_CONDITIONAL_LOOKUPS "<<r.fullConditionalChecks
    <<" EXACT_CONDITIONAL_REJECTS "<<r.invalidJointCandidates
    <<" FIRST_ONE_MARGINAL_PASSES "<<r.oneMarginalPass
    <<" FIRST_ONE_EXACT_REJECTS "<<r.oneExactRejected
    <<" SOURCE_WALL_MS "<<std::fixed<<std::setprecision(3)<<ms
    <<" FULL_CUBIE_GOAL_HITS 0 COMPLETE_LOCAL_R10 1 GLOBAL_R10_COMPLETE 0"
    <<" PEAK_RSS_KIB "<<rssKiB()<<"\n"<<std::flush;
  }
  if(goalDigest(r.court,6,"")!=digest)throw std::runtime_error("source changed goal");
  std::cout<<"P10_FIBER_EXACT_VS_PRODUCT_MARGINAL_PHYSICAL_COMPARE_PASS"
    <<" FIRST 12 SECOND 0 SOURCE_RADIUS 10"
    <<" WHOLE_GOAL_SHA "<<digest<<" TARGET_IMMUTABLE 1"
    <<" TRUE_GOAL_HITS 0 BOTH_BOUNDED_SEARCHES_COMPLETE 1"
    <<" EXTRA_SPARSE_FIBER_INDEX_BUILT 0"
    <<" EXISTING_B6_GOAL_MEMBERSHIP_REUSED 1"
    <<" WHOLE_B10_COMPLETE 0 LOWER17_CLAIMED 0"
    <<" START_RSS_KIB "<<startRss<<" PEAK_RSS_KIB "<<rssKiB()<<"\n";
  return 0;
 }catch(const std::exception&e){std::cerr<<"P10_COMPARISON_ERROR "<<e.what()<<"\n";return 4;}
}
