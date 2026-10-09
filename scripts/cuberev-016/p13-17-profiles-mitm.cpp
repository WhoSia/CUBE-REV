// CUBE-REV 0.16/P13: independent exact 3+2 certificate for all 17
// five-word coverage profiles. DOES NOT enumerate all C(80,5)=24,040,016
// quintets; tests only 82,160 triples and 3,160 inverted-index pairs.
// Finite computational certificate; nonenumerative physical classification OPEN.
#include <array>
#include <fstream>
#include <iostream>
#include <map>
#include <cstdint>
using namespace std;
struct Pair {int d,e;uint32_t heavy;unsigned light;};
int main(int argc,char**argv){
 if(argc!=2)return 2;ifstream f(argv[1]);array<uint32_t,80> cols{};
 for(auto &x:cols)if(!(f>>x))return 3;
 constexpr uint32_t FULL=(1u<<20)-1;
 array<Pair,3160> pairs{};int np=0;
 array<array<uint64_t,50>,20> inv{};
 for(int d=0;d<79;d++)for(int e=d+1;e<80;e++){
  uint32_t h=(cols[d]|cols[e])&FULL;
  pairs[np]={d,e,h,static_cast<unsigned>(((cols[d]|cols[e])>>20)&255u)};
  for(int bit=0;bit<20;bit++)if((h>>bit)&1u)inv[bit][np>>6]|=1ull<<(np&63);
  np++;
 }
 if(np!=3160)return 4;
 map<int,uint64_t> hist;uint64_t done=0,checked=0,triples=0;
 for(int a=0;a<78;a++)for(int b=a+1;b<79;b++)for(int c=b+1;c<80;c++){
  triples++;uint32_t abc=cols[a]|cols[b]|cols[c];
  uint32_t missing=FULL&~abc;
  for(int chunk=0;chunk<50;chunk++){
   uint64_t mask=~0ull;
   for(int bit=0;bit<20;bit++)if((missing>>bit)&1u)mask&=inv[bit][chunk];
   while(mask){int k=__builtin_ctzll(mask);mask&=mask-1;
    int j=chunk*64+k;if(j>=3160)continue;
    const auto &p=pairs[j];if(p.d<=c)continue;
    checked++;auto total=abc|cols[p.d]|cols[p.e];
    if((total&FULL)!=FULL)return 5;
    hist[int((total>>20)&255u)]++;done++;
   }
  }
 }
 const map<int,uint64_t> expected={
  {85,624},{90,312},{95,20},{102,312},{105,312},
  {119,20},{125,20},{153,312},{165,312},{170,624},
  {175,20},{187,20},{221,20},{235,20},{238,20},
  {245,20},{250,20}};
 if(triples!=82160||done!=3008||hist!=expected)return 6;
 cout<<"P13_MITM_17_PROFILE_COMPLETE_PASS\n";
 cout<<"TRIPLES="<<triples<<" PAIRS="<<np
     <<" FILTERED_FIVE_WORD_SETS="<<checked
     <<" COVERING_HEAVY20="<<done<<" PROFILES="<<hist.size()<<"\n";
}
