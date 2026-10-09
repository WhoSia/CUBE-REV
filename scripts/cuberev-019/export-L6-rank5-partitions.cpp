/** CUBE-REV 0.19. Exhaustive real-cube L6 candidate enumeration for k=3.
 * Needs 18×24 maps exported from physically sticker-derived urMoveAutomaton().
 * Only q=3..5 F/F'/B/B' flip-capable actions and output rank>=5 are emitted.
 * Excluded actions have rank<=4 by 2^q and all-F/B confinement.
 */
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <unordered_map>
using namespace std;
int maps[18][24],flip[18]={};
unordered_map<unsigned long long,array<unsigned char,6>> words;
unsigned long long tested=0;
void visit(int depth,int q,array<unsigned char,12> state,
           array<unsigned char,12> history,array<unsigned char,6>&word){
 if(q>5||q+(6-depth)<3)return;
 if(depth==6){
  tested++;unsigned char codes[64];
  fill(begin(codes),end(codes),255);
  int rank=0;unsigned long long signature=0;
  for(int i=0;i<12;i++){
   if(codes[history[i]]==255)codes[history[i]]=rank++;
   signature|=static_cast<unsigned long long>(codes[history[i]])<<(4*i);
  }
  if(rank>=5)words.emplace(signature,word);
  return;
 }
 for(int a=0;a<18;a++){
  auto next=state,trace=history;
  for(int i=0;i<12;i++){
   next[i]=maps[a][state[i]];
   trace[i]|=(next[i]&1)<<depth;
  }
  word[depth]=a;visit(depth+1,q+flip[a],next,trace,word);
 }
}
int main(){
 for(auto &m:maps){
  bool seen[24]={};
  for(int &v:m){if(!(cin>>v))return 2;assert(v>=0&&v<24&&!seen[v]);seen[v]=true;}
 }
 for(int a:{6,7,15,16})flip[a]=1;
 array<unsigned char,12> starts{},history{},word{};
 for(int i=0;i<12;i++)starts[i]=2*i;
 visit(0,0,starts,history,word);
 assert(tested==4350976ULL);assert(words.size()==53528);
 for(const auto &v:words){
  cout<<v.first;
  for(int a:v.second)cout<<" "<<int(a);
  cout<<"\n";
 }
 cerr<<"CUBE_REV_019_L6_PHYSICAL_Q3TO5_RANK5_PARTITIONS_53528_PASS tested="
     <<tested<<" unique="<<words.size()<<"\n";
}
