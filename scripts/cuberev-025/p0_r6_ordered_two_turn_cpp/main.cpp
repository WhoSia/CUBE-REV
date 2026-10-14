// CUBE-REV 0.25 P0-R6D — ordered TWO-turn same-word necessary condition.
// Source physical 54-facelet 18HTM transitions from pre-existing C++17 court.
#define CUBEREV_P0R6C_AS_LIBRARY
#include "../p0_r6_joint_next_action_cpp/main.cpp"
#undef CUBEREV_P0R6C_AS_LIBRARY

struct OrderedTwoTurnCourt : JointNextActionCourt {
 uint64_t twoStepCandidateParents=0,twoStepRejectedBranches=0;
 uint64_t twoStepRejectedCalls=0,orderedPairChecks=0,orderedPairPasses=0;
 uint64_t earlyCorner7Rejections=0,orderedPairParents=0;
 uint64_t canonicalSubtreeOne(int last) const {
   uint64_t n=1; // one omitted first-action child
   for(int b=0;b<18;b++)if(canonical(last,b))++n; // all its terminal children
   return n;
 }
 bool twoVisit(Cube const&s,int depth,int limit,int last) {
   // Reuse the independently defined exact one-step C/E screening unchanged.
   if(limit-depth==1)return jointVisit(s,depth,limit,last);
   ++visits;
   if((visits&0xffff)==0&&court.expired()){cut=true;return false;}
   FullKey key=exactKey(s);
   if(c6.find(key.c)!=c6.end()) {
     ++fullQueries;
     if(court.goal.find(key)!=court.goal.end()){
       ++fullHits;meet=true;foundPrefix=path;foundKey=key;return true;
     }
   }
   if(depth==limit)return false;

   if(limit-depth==2) {
     ++orderedPairParents;
     for(int a=0;a<18;a++){
       if(!canonical(last,a))continue;
       const Cube next=composeCube(s,turn[a]);
       FullKey n=exactKey(next);
       // A solve may finish after exactly ONE of the TWO available turns.
       const bool onePossible=
         c6.find(n.c)!=c6.end() && edge6.find(n.e)!=edge6.end();

       bool twoPossible=false;
       // If the first move's corners are not in the exact inverse one-step
       // envelope, NO legal second move can meet the true B6 corner image.
       if(c7.find(n.c)==c7.end()) {
         ++earlyCorner7Rejections;
       } else if(!onePossible) {
         for(int b=0;b<18;b++){
           if(!canonical(a,b))continue;
           ++orderedPairChecks;
           // Preserve the genuine ORDERED original-cube word (a followed by b).
           FullKey end=exactKey(composeCube(next,turn[b]));
           if(c6.find(end.c)!=c6.end() &&
              edge6.find(end.e)!=edge6.end()){
             ++orderedPairPasses;
             twoPossible=true;
             break;
           }
         }
       }
       if(!onePossible&&!twoPossible){
         ++twoStepRejectedBranches;
         const uint64_t removed=canonicalSubtreeOne(a);
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
     if(twoVisit(composeCube(s,turn[a]),depth+1,limit,a))return true;
     path.pop_back();
     if(cut)return false;
   }
   return false;
 }
 bool twoCheck(Cube const&source,int radius){
   for(int k=0;k<=radius;k++){
     path.clear();
     const auto oldVisits=visits,oldSkips=skippedChildren;
     bool found=twoVisit(source,0,k,-1);
     std::cout<<"P0R6D_DEPTH "<<k<<" COMPLETED "<<(!cut?1:0)
       <<" VISITS "<<visits-oldVisits
       <<" SKIPPED_CANONICAL_CALLS "<<skippedChildren-oldSkips
       <<" FULL_INTERSECTION "<<(found?1:0)<<"\n"<<std::flush;
     if(found||cut)return found;
   }
   return false;
 }
};

int main(int argc,char**argv){
 try {
   int rg=argc>1?std::stoi(argv[1]):3;
   int rs=argc>2?std::stoi(argv[2]):3;
   int seconds=argc>3?std::stoi(argv[3]):360;
   if(rg<0||rg>6||rs<0||rs>8||seconds<1)
     throw std::runtime_error("original physical safe goal<=6 source<=8");
   initTurns();
   const auto scramble=parse("R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2");
   const auto solution=parse("F U F D' R' F' L' F' D' L B L2 F2 U2 L2 U F' R2");
   Cube source=cubeAfter(scramble);
   Stickers stickers=solvedStickers();
   for(int a:scramble)physicalTurn(stickers,names[a]);
   if(!(exactKey(source)==exactKey(fromStickers(stickers))) ||
      solution.size()!=18 || !physicalSolves(scramble,solution))
     throw std::runtime_error("original 54-sticker physical source or 18-word mismatch");

   const auto uf=parse("U F"),fu=parse("F U");
   if(uf.size()!=2||fu.size()!=2 ||
     exactKey(cubeAfter(uf))==exactKey(cubeAfter(fu)))
       throw std::runtime_error("real physical 18HTM two-word noncommutativity regression");
   OrderedTwoTurnCourt r;
   r.court.started=Clock::now();r.court.secondsBudget=seconds;
   if(!r.court.build(rg)){std::cout<<"P0R6D_HOLD_GOAL\n";return 2;}
   r.project();r.prepareEdges();
   std::cout<<"P0R6D_GOAL_FULL "<<r.court.goal.size()
     <<" CORNER6 "<<r.c6.size()<<" CORNER7 "<<r.c7.size()
     <<" EDGE6 "<<r.edge6.size()
     <<" REAL_ORIGINAL_CUBE_UF_NE_FU 1\n"<<std::flush;
   bool found=r.twoCheck(source,rs);
   if(r.cut||r.court.expired()){std::cout<<"P0R6D_HOLD_SOURCE\n";return 2;}
   if(found) {
     std::cout<<"P0R6D_FULL_CUBIE_INTERSECTION FOUND 1 SOURCE_PREFIX "
       <<join(r.foundPrefix)<<" LOWER_CERTIFICATE_WITHHELD 1\n";return 3;
   }
   const uint64_t baseline=canonicalBaselineVisits(rs);
   if(r.visits+r.skippedChildren!=baseline)
     throw std::runtime_error("exact ordered-two-turn source call accounting FAILED");
   std::cout<<"P0R6D_EXACT_COVER BASELINE "<<baseline
     <<" ACTUAL_VISITS "<<r.visits
     <<" SKIPPED_CANONICAL_CALLS "<<r.skippedChildren
     <<" TWO_STEP_REJECTED_FIRST_ACTION_BRANCHES "<<r.twoStepRejectedBranches
     <<" TWO_STEP_REJECTED_RECURSIVE_CALLS "<<r.twoStepRejectedCalls
     <<" TWO_STEP_CANDIDATE_FIRST_ACTION_BRANCHES "<<r.twoStepCandidateParents
     <<" ORDERED_PAIR_CHECKS "<<r.orderedPairChecks
     <<" ORDERED_PAIR_PASSES "<<r.orderedPairPasses
     <<" FULL_HITS "<<r.fullHits<<" COMPLETE 1\n";
   if(rg==6&&(rs==7||rs==8)){
     uint64_t expected=rs==7?120213368ULL:1604664504ULL;
     if(baseline!=expected||r.court.goal.size()!=8240087||
        r.c6.size()!=1405068||r.fullHits!=0)
       throw std::runtime_error("original full-cubie P1-R6 regression FAILED");
     std::cout<<"P0R6D_GLOBAL_LOWER "<<(rg+rs+1)
       <<" UPPER 18 COMPLETE 1 ORDERED_TWO_MOVE_PREDICATE_SOUND 1\n";
   }
   return 0;
 } catch(const std::exception&e){
   std::cerr<<"P0R6D_ERROR "<<e.what()<<"\n";return 4;
 }
}
