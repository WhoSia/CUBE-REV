// CUBE-REV 0.16 P12: independently exhaust ALL C(80,5)=24,040,016
// combinations from the math-only P10-derived near-tight 80×28 incidence.
// This is a FINITE complete proof certificate, not a calculation-free proof.
// Input: 80 unsigned integers, with first 20 bits heavy, next 8 light.
// DO NOT apply the near-tight 80-column restriction to a 25-word M* claim.
#include <array>
#include <cstdint>
#include <iostream>
#include <fstream>
#include <map>
#include <cassert>
using namespace std;
int main(int argc,char**argv){
 if(argc!=2)return 2;
 ifstream f(argv[1]);array<uint32_t,80> v{};
 for(auto &x:v)if(!(f>>x))return 3;
 uint32_t extr; if(f>>extr)return 4;
 const uint32_t H=(1u<<20)-1u;
 map<int,uint64_t> patterns;
 uint64_t tested=0,heavy5=0,forbidden24=0;
 for(int a=0;a<76;a++)for(int b=a+1;b<77;b++)
 for(int c=b+1;c<78;c++)for(int d=c+1;d<79;d++){
   const auto first=v[a]|v[b]|v[c]|v[d];
   for(int e=d+1;e<80;e++){
    ++tested;
    const auto all=first|v[e];
    if((all&H)!=H)continue;
    ++heavy5;
    const int light=int((all>>20)&255u);
    ++patterns[light];
    if(light==255)++forbidden24;
   }
 }
 const map<int,uint64_t> expected={
  {85,624},{90,312},{95,20},{102,312},{105,312},
  {119,20},{125,20},{153,312},{165,312},{170,624},
  {175,20},{187,20},{221,20},{235,20},{238,20},
  {245,20},{250,20}};
 if(tested!=24040016ULL||heavy5!=3008||forbidden24!=0||patterns!=expected){
   cerr<<"P12_FAIL tested="<<tested<<" heavy5="<<heavy5
   <<" forbidden="<<forbidden24<<" profiles="<<patterns.size()<<"\n";
   return 1;
 }
 // The four-light target mask 150 is not contained in any realized profile.
 for(const auto& [mask,count]:patterns)if((mask&150)==150)return 5;
 cout<<"P12_CXX_EXACT_80_CHOOSE_5_24_CORE_17_PROFILES_PASS\n";
 cout<<"tested="<<tested<<" heavy20covers="<<heavy5
     <<" profiles="<<patterns.size()<<" forbidden24="<<forbidden24<<"\n";
}
