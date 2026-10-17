// CUBE-REV 0.26 R2: original physical 18HTM paired marginal-order benchmark.
// Exact identical admissible bound: C6 AND E6 after each canonical second turn.
// Baseline is inherited CORNER-first P9, candidate EDGE-first reorders the same
// two mathematically necessary predicates. No stronger novel heuristic presumed.
#define CUBEREV_P9_AS_LIBRARY
#include "../../cuberev-025/p0_r6i_p9_projection_cpp/main.cpp"
#undef CUBEREV_P9_AS_LIBRARY
#include <array>
#include <vector>
#include <algorithm>
#include <numeric>
#include <limits>
#include <cmath>

struct EdgeFirstCourt:PackedOrderedCourt{
 uint64_t alternativeEdgeProbe=0,alternativeCornerProbe=0,altPassedPairs=0;
 bool edgeVisit(Cube const&s,int depth,int limit,int last){
  if(limit-depth==1)return jointVisit(s,depth,limit,last);
  ++visits;
  if((visits&0xffff)==0&&court.expired()){cut=true;return false;}
  FullKey key=exactKey(s);
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
    Cube next=composeCube(s,turn[a]);
    FullKey n=exactKey(next);
    const bool onePossible=c6.find(n.c)!=c6.end()&&edge6.find(n.e)!=edge6.end();
    bool twoPossible=false;
    if(c7.find(n.c)==c7.end())++earlyCorner7Rejections;
    else if(!onePossible){
     for(int b=0;b<18;b++){
      if(!canonical(a,b))continue;
      ++orderedPairChecks;
      ++secondFullCubeMovesAvoided;
      ++edgePackedChecks;
      ++alternativeEdgeProbe;
      const Key64 e=edgeTurnPacked(n.e,b);
      if(edge6.find(e)==edge6.end())continue;
      ++cornerPackedChecks;
      ++alternativeCornerProbe;
      const Key64 c=cornerTurnPacked(n.c,b);
      if(c6.find(c)==c6.end())continue;
      ++orderedPairPasses;
      ++altPassedPairs;
      twoPossible=true;
      break;
     }
    }
    if(!onePossible&&!twoPossible){
     ++twoStepRejectedBranches;
     auto removed=canonicalSubtreeOne(a);
     skippedChildren+=removed;
     twoStepRejectedCalls+=removed;
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
   if(edgeVisit(composeCube(s,turn[a]),depth+1,limit,a))return true;
   path.pop_back();
   if(cut)return false;
  }
  return false;
 }
 void clear(){
  visits=0;skippedChildren=0;fullHits=0;fullQueries=0;
  orderedPairChecks=0;edgePackedChecks=0;cornerPackedChecks=0;
  secondFullCubeMovesAvoided=0;earlyCorner7Rejections=0;
  twoStepRejectedBranches=0;twoStepRejectedCalls=0;
  twoStepCandidateParents=0;orderedPairParents=0;orderedPairPasses=0;
  alternativeEdgeProbe=0;alternativeCornerProbe=0;altPassedPairs=0;
  cut=false;meet=false;foundPrefix.clear();path.clear();
 }
};

struct Snapshot{
 uint64_t visited=0,omitted=0,pairs=0,passes=0,full=0,early=0,candidates=0,pruned=0,corner=0,edge=0;
 double durationMs=0;
};

int main(int argc,char**argv){
 try{
  if(argc!=2||std::stoi(argv[1])<300||std::stoi(argv[1])>1100)
   throw std::runtime_error("usage seconds_budget 300..1100");
  const int budget=std::stoi(argv[1]);
  initTurns();
  auto scr=parse("R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2");
  auto sol=parse("F U F D' R' F' L' F' D' L B L2 F2 U2 L2 U F' R2");
  Cube src=cubeAfter(scr);
  Stickers original=solvedStickers();
  for(int a:scr)physicalTurn(original,names[a]);
  if(!equalCube(fromStickers(original),src)||sol.size()!=18||
     !physicalSolves(scr,sol)||physicallyAuditFastProjection()!=4608)
   throw std::runtime_error("original WCA physical 54-sticker source HOLD");
  EdgeFirstCourt r;
  r.court.started=Clock::now();r.court.secondsBudget=budget;
  if(!r.court.build(6)){std::cout<<"R2_GOAL_BUILD_HOLD\n";return 2;}
  r.project();r.prepareEdges();
  if(r.court.goal.size()!=8240087||r.c6.size()!=1405068||
    r.c7.size()!=6807696||r.edge6.size()!=7672278)
   throw std::runtime_error("original B6 full/projection cardinality mismatch");
  const auto sha=goalDigest(r.court,6,"");
  if(sha!="82fe545bcad3537c989ec22afce9d286926ddce5f4ef9428c0307951ec2d0979")
   throw std::runtime_error("immutable original B6 SHA mismatch");
  std::cout<<"R2_ORIGINAL_GOAL_FULL VERIFIED_SHA "<<sha
    <<" ACTUAL_54_FACELET_4608 1 SOURCE_RADIUS 10"
    <<" GOAL_STATES "<<r.court.goal.size()<<" C6 "<<r.c6.size()
    <<" C7 "<<r.c7.size()<<" E6 "<<r.edge6.size()
    <<" GLOBAL_LOWER17_CLAIMED 0\n"<<std::flush;
  // Control: previously certified B first15 second0; open first16 second0.
  // NO conclusion about full first16 root from only its one second child.
  const std::array<std::array<int,2>,2> prefixes={{{15,0},{16,0}}};
  uint64_t count=0;
  double ratios[2]{};
  for(int fixture=0;fixture<2;fixture++){
   int first=prefixes[fixture][0],second=prefixes[fixture][1];
   if(!canonical(first,second))throw std::runtime_error("not canonical original source fixture");
   Cube node=composeCube(composeCube(src,turn[first]),turn[second]);
   auto expected=p8Weight(second,8);
   std::array<Snapshot,4> got;
   for(int round=0;round<4;round++){
    // ABBA so order/runner drift does not mechanically favor one method.
    const bool candidate=round==1||round==2;
    r.clear();
    const auto start=std::chrono::steady_clock::now();
    for(int lim=2;lim<=10;lim++){
     r.path={first,second};
     const bool found=candidate?r.edgeVisit(node,2,lim,second):r.fastVisit(node,2,lim,second);
     if(found){
      std::cout<<"R2_TRUE_ORIGINAL_WHOLE_CUBIE_MEET FIRST "<<first<<" SECOND "<<second
        <<" MODE "<<(candidate?"EDGE_FIRST":"CORNER_FIRST")
        <<" SOURCE_PATH "<<join(r.foundPrefix)
        <<" AB_COMPARISON_HOLD 1 GLOBAL_LOWER17_CLAIMED 0\n"<<std::flush;
      return 3;
     }
     if(r.cut||r.court.expired()){
      std::cout<<"R2_RESOURCE_HOLD FIRST "<<first<<" SECOND "<<second
        <<" ROUND "<<round<<" GLOBAL_LOWER17_CLAIMED 0\n"<<std::flush;
      return 2;
     }
    }
    const double ms=std::chrono::duration<double,std::milli>(
      std::chrono::steady_clock::now()-start).count();
    if(r.visits+r.skippedChildren!=expected||r.fullHits||
       r.secondFullCubeMovesAvoided!=r.orderedPairChecks)
      throw std::runtime_error("original normal-form weighted coverage or exact whole goal mismatch");
    auto &s=got[round];
    s.visited=r.visits;s.omitted=r.skippedChildren;s.pairs=r.orderedPairChecks;
    s.passes=r.orderedPairPasses;s.full=r.fullQueries;s.early=r.earlyCorner7Rejections;
    s.candidates=r.twoStepCandidateParents;s.pruned=r.twoStepRejectedBranches;
    s.corner=r.cornerPackedChecks;s.edge=r.edgePackedChecks;s.durationMs=ms;
    std::cout<<"R2_MATCHED_ORIGINAL_AB FIRST "<<first<<" SECOND "<<second
      <<" FIXTURE "<<fixture<<" ROUND "<<round
      <<" MODE "<<(candidate?"EDGE_FIRST":"CORNER_FIRST")
      <<" SOURCE_B6_SHA "<<sha<<" WORD_CALLS "<<expected
      <<" VISITED "<<s.visited<<" OMITTED "<<s.omitted
      <<" TWO_STEP_PAIR_CHECKS "<<s.pairs
      <<" PROVEN_TWO_STEP_PASSES "<<s.passes
      <<" FULL_GOAL_QUERIES "<<s.full<<" CORNER7_REJECTIONS "<<s.early
      <<" CANDIDATE_BRANCHES "<<s.candidates<<" PRUNED_BRANCHES "<<s.pruned
      <<" CORNER_PACKED_CHECKS "<<s.corner<<" EDGE_PACKED_CHECKS "<<s.edge
      <<" WALL_MS "<<std::fixed<<std::setprecision(3)<<ms
      <<" ACTUAL_FULL_GOAL_HITS 0 COMPLETE_DEPTH2_SOURCE_PREFIX 1"
      <<" COMPLETE_FIRST_ACTION_ROOT 0 GLOBAL_LOWER17_CLAIMED 0\n"<<std::flush;
    count++;
   }
   for(int i=1;i<4;i++){
    if(got[i].visited!=got[0].visited||got[i].omitted!=got[0].omitted||
      got[i].pairs!=got[0].pairs||got[i].passes!=got[0].passes||
      got[i].full!=got[0].full||got[i].early!=got[0].early||
      got[i].candidates!=got[0].candidates||got[i].pruned!=got[0].pruned)
      throw std::runtime_error("SOUNDNESS HOLD: same original source has DIFFERENT true visited/omitted/candidate classifications");
   }
   const double base=(got[0].durationMs+got[3].durationMs)/2.0;
   const double alt=(got[1].durationMs+got[2].durationMs)/2.0;
   if(base<=0||alt<=0)throw std::runtime_error("clock did not capture paired benchmark");
   ratios[fixture]=alt/base;
   std::cout<<"R2_MATCHED_ABBA_SUMMARY FIRST "<<first<<" SECOND "<<second
     <<" BASELINE_AVG_MS "<<std::fixed<<std::setprecision(3)<<base
     <<" EDGE_FIRST_AVG_MS "<<alt<<" EDGE_OVER_BASE_RATIO "<<std::setprecision(7)<<ratios[fixture]
     <<" EXACT_SAME_VISITS "<<got[0].visited
     <<" EXACT_SAME_OMISSIONS "<<got[0].omitted
     <<" ACTUAL_FIRST_ROOT_COMPLETE 0\n"<<std::flush;
  }
  if(goalDigest(r.court,6,"")!=sha)throw std::runtime_error("goal source mutated during counterfactual");
  std::cout<<"R2_ORIGINAL_MATCHED_ADMISSIBLE_ORDER_ABBA_PASS"
    <<" SOURCE_PREFIXES 2 PAIRED_COMPLETE_SEARCH_RUNS "<<count
    <<" CHECKS_PROVEN_EQUIVALENT 1 ORIGINAL_B6_TARGET_IMMUTABLE 1"
    <<" SAME_VISITS_AND_OMISSIONS 1 VERIFIED_GOAL_SHA "<<sha
    <<" EDGE_OVER_BASE_RATIO_FIXTURE0 "<<std::fixed<<std::setprecision(7)<<ratios[0]
    <<" EDGE_OVER_BASE_RATIO_FIXTURE1 "<<ratios[1]
    <<" ROOTS_CURRENT_CERTIFIED 5 ROOTS_OPEN 13"
    <<" NEW_FULL_FIRST_ROOT_CERTIFIED 0 GLOBAL_LOWER17_CLAIMED 0"
    <<" PEAK_RSS_KIB "<<rssKiB()<<"\n"<<std::flush;
  return 0;
 }catch(const std::exception&e){std::cerr<<"R2_BENCHMARK_ERROR "<<e.what()<<"\n";return 4;}
}
