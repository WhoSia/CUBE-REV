// R8: exact per-state edge color certificate census, complete corner oracle.
// Not an adaptive decision tree: selected queries may depend on true state.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
const array<string,12> names={"UR","UF","UL","UB","DR","DF","DL","DB","FR","FL","BL","BR"};
array<string,12> colors;
vector<int> partial;
array<int,12> assigned{};
array<bool,12> occupied{};
uint32_t missing=0, example=0;
int solutions=0;
uint64_t singles=0, doubles=0;
int rank_color(char c){
 if(c=='U'||c=='D')return 0;
 if(c=='F'||c=='B')return 1;
 return 2;
}
void recurse(int d,int parity,int flip_parity,int fully_unknown){
 if(solutions>=2)return;
 if(d==int(partial.size())){
  if(parity==0)solutions+=fully_unknown?(1<<(fully_unknown-1)):(flip_parity==0);
  return;
 }
 int dest=partial[d];
 int absent=(missing>>(2*dest))&3;
 for(int j=0;j<int(partial.size());j++){
  if(occupied[j])continue;
  int src=partial[j],flip=0;
  if(absent!=3){
   int read=(absent&1)?1:0;
   char color=colors[dest][read];
   if(colors[src][0]==color)flip=read;
   else if(colors[src][1]==color)flip=read^1;
   else continue;
  }
  int inv=0;
  for(int k=0;k<d;k++)inv+=(assigned[k]>j);
  assigned[d]=j;occupied[j]=true;
  recurse(d+1,(parity+inv)&1,(flip_parity+flip)&1,fully_unknown+(absent==3));
  occupied[j]=false;
  if(solutions>=2)return;
 }
}
int count_up_to_two(uint32_t mask){
 missing=mask;partial.clear();occupied.fill(false);
 for(int i=0;i<12;i++)if((mask>>(2*i))&3)partial.push_back(i);
 solutions=0;recurse(0,0,0,0);
 assert(solutions>=1);
 return min(solutions,2);
}
void enumerate(int remain,int start,uint32_t mask){
 if(remain==0){
  if(count_up_to_two(mask)==1){++singles;if(example==0)example=mask;}
  else ++doubles;
  return;
 }
 for(int i=start;i<=24-remain;i++)enumerate(remain-1,i+1,mask|(1u<<i));
}
uint64_t choose24(int k){
 uint64_t result=1;
 for(int j=1;j<=k;j++)result=result*(25-j)/j;
 return result;
}
int main(){
 for(int i=0;i<12;i++){
  colors[i]=names[i];
  sort(colors[i].begin(),colors[i].end(),[](char x,char y){return rank_color(x)<rank_color(y);});
 }
 const array<uint64_t,9> expected={0,0,0,0,9426,26400,36184,14664,0};
 for(int omitted=4;omitted<=8;omitted++){
  singles=doubles=0;example=0;
  enumerate(omitted,0,0);
  assert(singles==expected[omitted]);
  assert(singles+doubles==choose24(omitted));
  cout<<"R8_EDGE_CERT_MASK omitted="<<omitted<<" total="<<choose24(omitted)
      <<" singleton="<<singles<<" ambiguous="<<doubles<<"\n";
  if(omitted==7){
   cout<<"R8_EDGE_17_CERTIFICATE_EXAMPLE hidden=";
   for(int i=0;i<12;i++)for(int k=0;k<2;k++)
    if(example&(1u<<(2*i+k)))cout<<names[i]<<":"<<colors[i][k]<<" ";
   cout<<"\n";
  }
 }
 cout<<"R8_EDGE_CORNER_ORACLE_LOCAL_CERTIFICATE_17_PASS tested_16_read_masks=735471 singleton_17_read_masks=14664\n";
 cout<<"R8_BOUNDARY state-dependent certificate; adaptive policy still 18..21\n";
}