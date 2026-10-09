// CUBE-REV 0.19: prove NO fixed word of <=8 HTM turns separates all
// 12 initially orientation-zero edge slots. Complementary analytic barriers:
// q<=4 flip-capable turns: twelve distinct q-bit signatures would need
// >=19 ones for q=4, but four physically transported 4-slot cuts have 16.
// q>=7 flip-capable turns at L=8: at most one action outside F/B
// quarter-turns, hence at most 3*3=9 initial-group histories.
// This program exhausts EXACTLY the remaining q=5 and q=6 cases.
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <vector>
using namespace std;
int edge_move[18][24];
int flip_capable[18]={};
unsigned long long tested=0;
int maximum=0;
unsigned long long rank_hist[13]={};
void visit(int depth,int q,array<uint8_t,12> state,array<uint8_t,12> output){
 if(q+(8-depth)<5||q>6)return;
 if(depth==8){
  if(q<5||q>6)return;
  bool seen[256]={};int rank=0;
  for(int i=0;i<12;i++)if(!seen[output[i]]){
   seen[output[i]]=true;rank++;
  }
  tested++;rank_hist[rank]++;
  if(rank>maximum)maximum=rank;
  return;
 }
 for(int a=0;a<18;a++){
  if(q+flip_capable[a]>6)continue;
  auto nxt=state;auto hist=output;
  for(int i=0;i<12;i++){
   nxt[i]=static_cast<uint8_t>(edge_move[a][state[i]]);
   hist[i]|=(nxt[i]&1)<<depth;
  }
  visit(depth+1,q+flip_capable[a],nxt,hist);
 }
}
int main(){
 for(auto &map:edge_move){
  bool seen[24]={};
  for(int &x:map){if(!(cin>>x))return 2;assert(x>=0&&x<24);assert(!seen[x]);seen[x]=true;}
 }
 for(int i:{6,7,15,16})flip_capable[i]=1;
 array<uint8_t,12> state{},output{};
 for(int i=0;i<12;i++)state[i]=static_cast<uint8_t>(2*i);
 visit(0,0,state,output);
 assert(tested==179830784ULL);
 assert(maximum==11);
 cout<<"CUBE_REV_019_LENGTH8_ALL_Q5_Q6_179830784_WORDS_MAX_RANK11_PASS "<<tested<<" "<<maximum<<"\n";
 for(int i=0;i<13;i++)if(rank_hist[i])cout<<"rank "<<i<<" count "<<rank_hist[i]<<"\n";
}
