// CUBE-REV 0.26 R0: value-of-proof selection and true source stabilizer audit.
// Direct continuation of 0.25 fixed-source source-R10 proof, not a reset.
#define main cuberev026_p12p5_embedded_main_unused
#include "../p12_p5_true_rotation_lift_cpp/main.cpp"
#undef main

static uint64_t canonicalIddfsWeight(int prev,int remaining){
 array<uint64_t,18> last{};uint64_t result=(uint64_t)remaining+1;
 for(int depth=1;depth<=remaining;depth++){
  array<uint64_t,18> next{};
  if(depth==1){
   for(int a=0;a<18;a++)if(canonical(prev,a))next[a]=1;
  }else{
   for(int b=0;b<18;b++)if(last[b])
    for(int a=0;a<18;a++)if(canonical(b,a))next[a]+=last[b];
  }
  last=next;
  uint64_t layer=0;for(auto n:next)layer+=n;
  result+=(uint64_t)(remaining-depth+1)*layer;
 }
 return result;
}
int main(){
 try{
  initTurns();
  const string literal="R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2";
  auto scramble=parse(literal);
  Cube original=cubeAfter(scramble);
  Stickers physical=solvedStickers();
  for(int a:scramble)physicalTurn(physical,names[a]);
  if(!equalCube(fromStickers(physical),original))
   throw runtime_error("source original 54-sticker mismatch");
  auto sol=parse("F U F D' R' F' L' F' D' L B L2 F2 U2 L2 U F' R2");
  if(sol.size()!=18||!physicalSolves(scramble,sol))
   throw runtime_error("original known 18-turn solution fails physics");
  const auto rots=properRotations();
  int fixed=0,identityFixed=0,grammarPreserving=0,fixedAndGrammar=0;
  std::set<string> maps;
  for(auto r:rots){
   if(!equalCube(transformCube(solved(),r),solved()))
    throw runtime_error("actual proper rotation fails solved state");
   string signature;
   for(int a=0;a<18;a++){
    int b=remapAction(a,r);
    if(!equalCube(transformCube(turn[a],r),turn[b]))
      throw runtime_error("physical 18HTM generator map failed");
    signature+=names[b]+",";
   }
   if(!maps.insert(signature).second)throw runtime_error("duplicate physical rotation");
   bool isSourceFixed=equalCube(transformCube(original,r),original);
   if(isSourceFixed)fixed++;
   bool grammar=true;
   for(int a=0;a<18;a++)for(int b=0;b<18;b++){
    if(canonical(a,b)!=canonical(remapAction(a,r),remapAction(b,r)))
      grammar=false;
   }
   if(grammar)grammarPreserving++;
   if(grammar&&isSourceFixed)fixedAndGrammar++;
   if(r.ix==array<int,3>{0,1,2}&&r.sign==array<int,3>{1,1,1}){
    if(!isSourceFixed||!grammar)throw runtime_error("identity source/grammar not fixed");
    identityFixed++;
   }
  }
  if(maps.size()!=24||identityFixed!=1)throw runtime_error("not all original true proper rotations verified");
  if(equalCube(composeCube(original,turn[0]),original))
   throw runtime_error("negative mutation source+U unexpectedly fixed");
  uint64_t minimum=UINT64_MAX;
  int cheap=0,expensive=0;
  for(int a=0;a<18;a++){
   int children=0;uint64_t weighted=10;
   for(int b=0;b<18;b++)if(canonical(a,b)){
    children++;weighted+=canonicalIddfsWeight(b,8);
   }
   if(children!=12&&children!=15)
    throw runtime_error("canonical root has neither12 nor15 second moves");
   if(children==12)cheap++;else expensive++;
   minimum=min(minimum,weighted);
   cout<<"R0_SOURCE_ROOT FIRST "<<a<<" MOVE "<<names[a]
       <<" SECOND_CHILDREN "<<children
       <<" EXACT_VIRTUAL_IDDFS_CALLS "<<weighted
       <<" FULL_ABSENCE_CERTIFIED "<<((a==0||a==3||a==9||a==12)?1:0)
       <<" UNVERIFIED_GOAL_INTERSECTION 1\n";
  }
  if(cheap!=9||expensive!=9||minimum!=14279876542ULL)
   throw runtime_error("source original canonical tree drift");
  cout<<"R0_SOURCE_STABILIZER_AUDIT_PASS VERSION 0.26"
      <<" ORIGINAL_SCRAMBLE_PHYSICAL 1 SOLUTION_18_PHYSICAL 1"
      <<" PHYSICAL_PROPER_ROTATIONS "<<rots.size()
      <<" SOURCE_FIXING_ROTATIONS "<<fixed
      <<" IDENTITY_FIXED "<<identityFixed
      <<" CANONICAL_PAIR_GRAMMAR_PRESERVING_ROTATIONS "<<grammarPreserving
      <<" SOURCE_AND_GRAMMAR_PRESERVING_ROTATIONS "<<fixedAndGrammar
      <<" CHEAP_12_CHILD_ROOTS "<<cheap
      <<" EXPENSIVE_15_CHILD_ROOTS "<<expensive
      <<" MIN_VIRTUAL_IDDFS_CALLS "<<minimum
      <<" PREVIOUS_CERTIFIED_ROOTS 4 OPEN_ROOTS 14"
      <<" GLOBAL_LOWER17_CLAIMED 0 ROOT_CERTIFICATE_UPGRADE 0\n";
  return 0;
 }catch(exception const&e){cerr<<"R0_SOURCE_STABILIZER_FAIL "<<e.what()<<"\n";return 3;}
}
