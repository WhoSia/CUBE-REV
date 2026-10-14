// CUBE-REV 0.25 P0-R6E: exact packed corner-first, then edge,
// ordered two-generator global source search. Same inherited real
// 54-sticker physical turn maps. No new projection caches / RAM explosion.
#define CUBEREV_P0R6D_AS_LIBRARY
#include "../p0_r6_ordered_two_turn_cpp/main.cpp"
#undef CUBEREV_P0R6D_AS_LIBRARY

using Key64=uint64_t;
Key64 cornerTurnPacked(Key64 c,int action) {
 const Cube&m=turn[action];
 Key64 next=0;
 for(int i=0;i<8;i++){
   const unsigned from=m.cp[i];
   const unsigned cp=(c>>(3*from))&7ULL;
   const unsigned co=(c>>(24+2*from))&3ULL;
   next|=Key64(cp)<<(3*i);
   next|=Key64((co+m.co[i])%3)<<(24+2*i);
 }
 return next;
}
Key64 edgeTurnPacked(Key64 e,int action) {
 const Cube&m=turn[action];
 Key64 next=0;
 for(int i=0;i<12;i++){
   const unsigned from=m.ep[i];
   const unsigned ep=(e>>(4*from))&15ULL;
   const unsigned eo=((e>>(48+from))&1ULL)^m.eo[i];
   next|=Key64(ep)<<(4*i);
   next|=Key64(eo)<<(48+i);
 }
 return next;
}
uint64_t physicallyAuditFastProjection(int samples=256){
 Cube s=solved();
 uint32_t rng=0xC0BEE6A1u;
 uint64_t checked=0;
 for(int k=0;k<samples;k++) {
   rng^=rng<<13;rng^=rng>>17;rng^=rng<<5;
   s=composeCube(s,turn[rng%18]);
   FullKey start=exactKey(s);
   for(int a=0;a<18;a++) {
     FullKey expect=exactKey(composeCube(s,turn[a]));
     if(cornerTurnPacked(start.c,a)!=expect.c)
       throw std::runtime_error("FAST_CORNER_NOT_EQUAL_TO_54_FACELET_DERIVED_MOVE");
     if(edgeTurnPacked(start.e,a)!=expect.e)
       throw std::runtime_error("FAST_EDGE_NOT_EQUAL_TO_54_FACELET_DERIVED_MOVE");
     ++checked;
   }
 }
 return checked;
}
struct PackedOrderedCourt : OrderedTwoTurnCourt {
 uint64_t cornerPackedChecks=0,edgePackedChecks=0;
 uint64_t secondFullCubeMovesAvoided=0;
 bool fastVisit(Cube const&s,int depth,int limit,int last){
   if(limit-depth==1)return jointVisit(s,depth,limit,last);
   ++visits;
   if((visits&0xffff)==0 && court.expired()){cut=true;return false;}
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
     for(int a=0;a<18;a++) {
       if(!canonical(last,a))continue;
       const Cube next=composeCube(s,turn[a]);
       const FullKey n=exactKey(next);
       const bool onePossible=c6.find(n.c)!=c6.end()&&edge6.find(n.e)!=edge6.end();
       bool twoPossible=false;
       if(c7.find(n.c)==c7.end())++earlyCorner7Rejections;
       else if(!onePossible){
         for(int b=0;b<18;b++) {
           if(!canonical(a,b))continue;
           ++orderedPairChecks;
           ++cornerPackedChecks;
           ++secondFullCubeMovesAvoided;
           const Key64 endCorner=cornerTurnPacked(n.c,b);
           if(c6.find(endCorner)==c6.end())continue;
           ++edgePackedChecks;
           if(edge6.find(edgeTurnPacked(n.e,b))!=edge6.end()){
             ++orderedPairPasses;twoPossible=true;break;
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
   for(int a=0;a<18;a++) {
     if(!canonical(last,a))continue;
     path.push_back(a);
     if(fastVisit(composeCube(s,turn[a]),depth+1,limit,a))return true;
     path.pop_back();
     if(cut)return false;
   }
   return false;
 }
 bool fastCheck(Cube const&source,int radius){
   for(int k=0;k<=radius;k++) {
     const auto old=visits,omitted=skippedChildren;
     path.clear();
     const bool result=fastVisit(source,0,k,-1);
     std::cout<<"P0R6E_DEPTH "<<k<<" COMPLETE "<<(!cut?1:0)
       <<" VISITS "<<visits-old<<" OMITTED "<<skippedChildren-omitted
       <<" MEET "<<(result?1:0)<<"\n"<<std::flush;
     if(result||cut)return result;
   }
   return false;
 }
};
int main(int argc,char**argv){
 try{
   const int rg=argc>1?std::stoi(argv[1]):3;
   const int rs=argc>2?std::stoi(argv[2]):3;
   const int seconds=argc>3?std::stoi(argv[3]):450;
   if(rg<0||rg>6||rs<0||rs>9||seconds<1)
     throw std::runtime_error("physical radius domain goal<=6 source<=9");
   initTurns();
   const auto scramble=parse("R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2");
   const auto solution=parse("F U F D' R' F' L' F' D' L B L2 F2 U2 L2 U F' R2");
   const Cube src=cubeAfter(scramble);
   Stickers stickers=solvedStickers();
   for(int a:scramble)physicalTurn(stickers,names[a]);
   if(!(exactKey(src)==exactKey(fromStickers(stickers))) ||
      solution.size()!=18 || !physicalSolves(scramble,solution))
     throw std::runtime_error("original physical 54-facelet or known 18-turn solve mismatch");
   const auto uf=parse("U F"),fu=parse("F U");
   if(uf.size()!=2||fu.size()!=2||
      exactKey(cubeAfter(uf))==exactKey(cubeAfter(fu)))
      throw std::runtime_error("real noncommuting physical order regression");
   const auto physicalCrossChecks=physicallyAuditFastProjection();
   std::cout<<"P0R6E_PACKED_PHYSICAL_TURN_REGRESSION PASS CASES "<<physicalCrossChecks
     <<" ALL18_REAL_MOVES 1 ORDER_SENSITIVE_UF_NE_FU 1\n"<<std::flush;
   PackedOrderedCourt r;
   r.court.started=Clock::now();r.court.secondsBudget=seconds;
   if(!r.court.build(rg)){std::cout<<"P0R6E_HOLD_GOAL\n";return 2;}
   r.project();r.prepareEdges();
   std::cout<<"P0R6E_GOAL_FULL "<<r.court.goal.size()
     <<" CORNER6 "<<r.c6.size()<<" CORNER7 "<<r.c7.size()
     <<" EDGE6 "<<r.edge6.size()<<"\n"<<std::flush;
   const bool found=r.fastCheck(src,rs);
   if(r.cut||r.court.expired()){std::cout<<"P0R6E_HOLD_SOURCE\n";return 2;}
   if(found){
     std::cout<<"P0R6E_TRUE_WHOLE_CUBE_MEET FOUND 1 SOURCE_PREFIX "
       <<join(r.foundPrefix)<<" LOWER_CERTIFICATE_WITHHELD 1\n";
     return 3;
   }
   const uint64_t baseline=canonicalBaselineVisits(rs);
   if(r.visits+r.skippedChildren!=baseline)
     throw std::runtime_error("source normal form exact full cover FAILED");
   if(r.cornerPackedChecks!=r.orderedPairChecks ||
      r.secondFullCubeMovesAvoided!=r.orderedPairChecks)
     throw std::runtime_error("packed pair accounting FAILED");
   std::cout<<"P0R6E_EXACT_COVER BASELINE "<<baseline<<" ACTUAL_VISITS "<<r.visits
     <<" SKIPPED_CANONICAL_CALLS "<<r.skippedChildren
     <<" TWO_STEP_REJECTED_FIRST_ACTION_BRANCHES "<<r.twoStepRejectedBranches
     <<" ORDERED_PAIR_CHECKS "<<r.orderedPairChecks
     <<" PACKED_CORNER_CHECKS "<<r.cornerPackedChecks
     <<" PACKED_EDGE_CHECKS "<<r.edgePackedChecks
     <<" AVOIDED_WHOLE_CUBE_SECOND_MOVES "<<r.secondFullCubeMovesAvoided
     <<" FULL_HITS "<<r.fullHits<<" COMPLETE 1\n";
   if(rg==6&&(rs==7||rs==8||rs==9)){
     const uint64_t expected=rs==7?120213368ULL:rs==8?1604664504ULL:21419814808ULL;
     if(baseline!=expected||r.court.goal.size()!=8240087ULL||
        r.c6.size()!=1405068ULL||r.fullHits!=0)
       throw std::runtime_error("full original B6/B7/B8/B9 baseline mismatch");
     std::cout<<"P0R6E_GLOBAL_LOWER "<<(rg+rs+1)
       <<" UPPER 18 FULL_PHYSICAL_SOURCE_COMPLETE 1"
       <<" SOURCE_RADIUS "<<rs<<" PROJECTION_EQUIVALENCE_4608 1\n";
   }
   return 0;
 }catch(const std::exception&e){std::cerr<<"P0R6E_ERROR "<<e.what()<<"\n";return 4;}
}
