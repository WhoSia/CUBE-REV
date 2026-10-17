// CUBE-REV 0.26 R1 — inherited exact original WCA source B10 first-action16 certificate
// source proof for ONE previously-open entire first-action cylinder a=16,
// split into TWO independently-running GitHub Actions worker shards.
// Complete means that particular first action only, NEVER entire B10.
#define main r3_pilot_entry_not_called
#include "../r3_c8_automaton_cpp/main.cpp"
#undef main

int main(int argc,char**argv){
 try{
  if(argc!=4)throw std::runtime_error("usage: first-action=12 worker-shard-0-or-1 time-budget-seconds");
  const int first=std::stoi(argv[1]), shard=std::stoi(argv[2]), secs=std::stoi(argv[3]);
  if(first!=16||shard<0||shard>1||secs<1||secs>1000)
   throw std::runtime_error("P11 only first action16, 2 physical shards");
  initTurns();
  const auto scramble=parse("R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2");
  const auto solution=parse("F U F D' R' F' L' F' D' L B L2 F2 U2 L2 U F' R2");
  const Cube src=cubeAfter(scramble);
  Stickers stickers=solvedStickers();
  for(int a:scramble)physicalTurn(stickers,names[a]);
  if(!(exactKey(src)==exactKey(fromStickers(stickers)))||
     !physicalSolves(scramble,solution)||solution.size()!=18||
     physicallyAuditFastProjection()!=4608)
    throw std::runtime_error("ORIGINAL_WCA_REAL_54_FACELET_PHYSICS_HOLD");
  EdgeFirstCourt court;
  court.court.started=Clock::now();court.court.secondsBudget=secs;
  if(!court.court.build(6)){std::cout<<"C026_R3R16_BRANCH_GOAL_HOLD\n";return 2;}
  court.project();court.prepareEdges();
  if(court.court.goal.size()!=8240087||court.c6.size()!=1405068||
     court.c7.size()!=6807696||court.edge6.size()!=7672278)
   throw std::runtime_error("full real B6 goal/projections cardinalities wrong");
  const auto target=goalDigest(court.court,6,"");
  if(target!="82fe545bcad3537c989ec22afce9d286926ddce5f4ef9428c0307951ec2d0979")
   throw std::runtime_error("whole B6 immutable target wrong");
  const std::string root="/tmp/p10-target-"+std::to_string(shard);
  const auto c6hash=projectionDigest(court.c6,"C6",root+"-C6.bin");
  const auto c7hash=projectionDigest(court.c7,"C7",root+"-C7.bin");
  const auto e6hash=projectionDigest(court.edge6,"E6",root+"-E6.bin");
  if(c6hash!="409d46f47d29852f1ced2ed1726aba0ce1085472def92591ecbb6a2346cc1ffc"||
     c7hash!="2fd2a3692147e81cc8bf970bcbbbdde061551065268e207d60aec4354ccd67e6"||
     e6hash!="40de5296f586037e8c5710b6a843263c4370c5faedb8bcf99516a4ae08a070f9")
   throw std::runtime_error("projected target goal contents differ from independently Go audited P9 SHA");
  for(auto c:court.c7){court.c8.put(c);for(int a=0;a<18;a++)court.c8.put(cornerTurnPacked(c,a));}
  auto c8count=court.c8.count(),c8sha=court.c8.sha();
  if(c8count!=27583872||c8sha!="1591559f375779e00d8343d91a753f48a655f7455ae8c67686f101b1b4bcffa3")throw std::runtime_error("wrong original physical C8");
  std::cout<<"C026_R3R16_C8_BUILD_PASS C8_COUNT "<<c8count<<" C8_SHA "<<c8sha<<" DENSE_BYTES "<<court.c8.bits.size()*8<<"\n";
  std::cout<<"C026_R3R16_BRANCH_GOAL FIRST "<<first<<" SHARD "<<shard<<" SHARDS 2"
    <<" GOAL_SHA "<<target<<" C6_SHA "<<c6hash<<" C7_SHA "<<c7hash
    <<" E6_SHA "<<e6hash<<" C8_SHA "<<c8sha<<" C8_COUNT "<<c8count<<" GOAL_STATES "<<court.court.goal.size()
    <<" REAL_54_FACELET_4608 1 SOURCE_RADIUS 10"
    <<" SOURCE_WHOLE_GLOBAL_COMPLETE 0\n"<<std::flush;
  const Cube rootState=composeCube(src,turn[first]);
  uint64_t weight=0,visited=0,omitted=0;
  int childCount=0;
  // The physical depth1 original source after first action16 is
  // checked ONCE by shard0; in the full first-action root's repeated
  // IDDFS, it has multiplicity 10 (bounds 1..10).
  if(shard==0){
   if(court.court.goal.find(exactKey(rootState))!=court.court.goal.end()){
    std::cout<<"C026_R3R16_BRANCH_ROOT_TRUE_MEET ABSENCE_CERT_WITHHELD 1\n";return 3;
   }
   weight=10;visited=10;
   std::cout<<"C026_R3R16_BRANCH_ROOT FIRST 16 SHARD 0 DEPTH 1"
     <<" REPEATED_CALLS 10 WHOLE_GOAL_HITS 0 GOAL_SHA "<<target<<"\n"<<std::flush;
  }
  std::vector<int> actions;
  for(int a=0;a<18;a++)if(canonical(first,a))actions.push_back(a);
  if(actions.size()!=12)throw std::runtime_error("first action16 legal children drift");
  for(size_t i=0;i<actions.size();i++){
   if(int(i%2)!=shard)continue;
   const int second=actions[i];
   const Cube x=composeCube(rootState,turn[second]);
   court.visits=0;court.skippedChildren=0;court.orderedPairChecks=0;
   court.edgePackedChecks=0;court.fullQueries=0;court.fullHits=0;court.cut=false;court.c8Reject=0;court.c8Descendants=0;
   const auto t=std::chrono::steady_clock::now();
   for(int limit=2;limit<=10;limit++){
    court.path={first,second};
    if(court.guardedVisit(x,2,limit,second)){
      std::cout<<"C026_R3R16_BRANCH_TRUE_FULL_CUBIE_MEET FIRST 16 SECOND "<<second
       <<" CERT_WITHHELD 1 SOURCE_PATH "<<join(court.foundPrefix)<<"\n";return 3;
    }
    if(court.cut||court.court.expired()){
      std::cout<<"C026_R3R16_BRANCH_RESOURCE_HOLD FIRST 16 SECOND "<<second
       <<" VISITED "<<court.visits<<" OMITTED "<<court.skippedChildren<<"\n";return 2;
    }
   }
   const uint64_t words=p8Weight(second,8);
   if(court.visits+court.skippedChildren!=words||court.fullHits)
    throw std::runtime_error("physical B10 leaf canonical normal-form incomplete");
   auto ms=std::chrono::duration<double,std::milli>(std::chrono::steady_clock::now()-t).count();
   const auto k=exactKey(x);
   childCount++;weight+=words;visited+=court.visits;omitted+=court.skippedChildren;
   std::cout<<"C026_R3R16_BRANCH_LEAF FIRST 16 SECOND "<<second
    <<" SHARD "<<shard<<" GLOBAL_SECOND_INDEX "<<i
    <<" SOURCE_C "<<k.c<<" SOURCE_E "<<k.e
    <<" WORD_CALLS "<<words<<" VISITED "<<court.visits
    <<" OMITTED "<<court.skippedChildren
    <<" PAIRS "<<court.orderedPairChecks<<" EDGES "<<court.edgePackedChecks
    <<" FULL_QUERIES "<<court.fullQueries<<" C8_REJECT "<<court.c8Reject<<" C8_DESCENDANTS "<<court.c8Descendants
    <<" SEARCH_MS "<<std::fixed<<std::setprecision(3)<<ms
    <<" WHOLE_GOAL_HITS 0 COMPLETE_LEAF 1 GOAL_SHA "<<target
    <<" FIRST_ACTION_CERT_COMPLETE 0 SOURCE_WHOLE_GLOBAL_COMPLETE 0\n"<<std::flush;
  }
  if(goalDigest(court.court,6,"")!=target)
   throw std::runtime_error("whole B6 target mutated in source B10 proof");
  if(visited+omitted!=weight||childCount!=6)
   throw std::runtime_error("original branch source shard accounting invalid");
  std::cout<<"C026_R3R16_BRANCH_SHARD_COMPLETE FIRST 16 SHARD "<<shard
   <<" CHILDREN "<<childCount<<" INTERNAL_CHECKS "<<(shard==0?1:0)
   <<" WEIGHT "<<weight<<" VISITED "<<visited<<" OMITTED "<<omitted
   <<" GOAL_SHA "<<target<<" TARGET_IMMUTABLE 1"
   <<" FIRST_ACTION_CERT_COMPLETE 0 SOURCE_WHOLE_GLOBAL_COMPLETE 0"
   <<" RSS_KIB "<<rssKiB()<<"\n"<<std::flush;
  return 0;
 }catch(const std::exception&e){std::cerr<<"C026_R3R16_BRANCH_ERROR "<<e.what()<<"\n";return 4;}
}
