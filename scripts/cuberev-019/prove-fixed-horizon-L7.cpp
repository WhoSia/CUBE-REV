// CUBE-REV 0.19 — exhaustive seven-HTM observation rank obstruction.
// Analytic cases: q<=2 flip-capable actions give at most 4 histories;
// q>=6 leaves at most one non-F/B action so F/B-group confinement gives <=9.
// Exhaust remaining q=3,4,5 on the exact physical 18x24 sticker edge maps.
#include <array>
#include <cassert>
#include <iostream>
using namespace std;
int moves[18][24],flip[18]={};
unsigned long long counts[6][13]={};
void visit(int depth,int q,array<unsigned char,12>s,array<unsigned char,12>h){
 if(q>5||q+(7-depth)<3)return;
 if(depth==7){
  if(q<3||q>5)return;
  bool seen[128]={};int rank=0;
  for(int i=0;i<12;i++)if(!seen[h[i]]){seen[h[i]]=true;rank++;}
  counts[q][rank]++;return;
 }
 for(int a=0;a<18;a++){
  auto next=s,trace=h;
  for(int i=0;i<12;i++){
   next[i]=static_cast<unsigned char>(moves[a][s[i]]);
   trace[i]|=(next[i]&1)<<depth;
  }
  visit(depth+1,q+flip[a],next,trace);
 }
}
int main(){
 for(auto &m:moves){
  bool seen[24]={};
  for(int &x:m){if(!(cin>>x))return 2;assert(x>=0&&x<24&&!seen[x]);seen[x]=true;}
 }
 for(int a:{6,7,15,16})flip[a]=1;
 array<unsigned char,12>s{},h{};
 for(int i=0;i<12;i++)s[i]=static_cast<unsigned char>(2*i);
 visit(0,0,s,h);
 const unsigned long long totals[]={0,0,0,86051840ULL,24586240ULL,4214784ULL};
 const int maxima[]={0,0,0,8,10,9};
 for(int q=3;q<=5;q++){
  unsigned long long total=0;int maxrank=0;
  for(int r=0;r<=12;r++)if(counts[q][r]){
   total+=counts[q][r];maxrank=r;
  }
  assert(total==totals[q]);assert(maxrank==maxima[q]);
  cout<<"q "<<q<<" words "<<total<<" maxRank "<<maxrank<<"\n";
 }
 cout<<"CUBE_REV_019_ALL_L7_114852864_RELEVANT_WORDS_MAX_RANK10_PASS\n";
}
