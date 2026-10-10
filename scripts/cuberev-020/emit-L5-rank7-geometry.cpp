// CUBE-REV 0.20 P1-E: exact L=5 rank-seven physical-edge cut-witness emitter.
// Input is a source-locked ORIGINAL sticker-derived 18x24 oriented-edge map.
// Run: c++ -std=c++20 -O3 -Wall -Wextra -Werror -pedantic emit-L5-rank7-geometry.cpp -o rank7
//      rank7 original_move_maps.txt rank7.csv
// Negative controls may supply a separately labelled NONCUBE map; do not ascribe those to Rubik.
#include <array>
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
using namespace std;
using Moves=array<array<int,24>,18>;
Moves M;
ofstream out;
uint64_t emitted=0;
void enumerate(int depth,int q,array<int,12> cur,array<int,12> sig,
               array<int,5> actions,array<int,5> cuts) {
 if(depth==5) {
  array<int,12> observed{};
  int rank=0;
  uint64_t key=0;
  for(int s=0;s<12;s++) {
   int j=0;
   while(j<rank && observed[j]!=sig[s])++j;
   if(j==rank)observed[rank++]=sig[s];
   key|=uint64_t(j)<<(4*s);
  }
  if(rank==7) {
   out<<key<<","<<q;
   for(int a:actions)out<<","<<a;
   for(int c:cuts)out<<","<<c;
   out<<",7\n";
   ++emitted;
  }
  return;
 }
 for(int a=0;a<18;a++) {
  auto next=cur,nsig=sig;
  auto na=actions,nc=cuts;
  na[depth]=a;
  int cut=0;
  for(int s=0;s<12;s++){
   next[s]=M[a][cur[s]];
   if((next[s]&1)!=(cur[s]&1))cut|=1<<s;
   nsig[s]=(sig[s]<<1)|(next[s]&1);
  }
  nc[depth]=cut;
  enumerate(depth+1,q+(cut!=0),next,nsig,na,nc);
 }
}
int main(int argc,char**argv){
 try {
  if(argc!=3)throw runtime_error("Usage: rank7 ORIGINAL_MAPS.txt OUTPUT.csv");
  ifstream in(argv[1]);
  if(!in)throw runtime_error("Cannot open oriented-edge maps");
  for(auto& a:M){
   array<bool,24> seen{};
   for(int& x:a){
    if(!(in>>x) || x<0 || x>=24 || seen[x])throw runtime_error("Invalid 24-state bijection");
    seen[x]=true;
   }
   for(int p=0;p<12;p++)
    if(a[2*p]/2!=a[2*p+1]/2 || (a[2*p]&1)==(a[2*p+1]&1))
     throw runtime_error("Original XOR orientation contract violated");
  }
  int trailing=0;
  if(in>>trailing)throw runtime_error("Too many map entries");
  out.open(argv[2]);
  if(!out)throw runtime_error("Cannot write rank-seven records");
  out<<"key,q,a0,a1,a2,a3,a4,c0,c1,c2,c3,c4,rank\n";
  array<int,12> start{},sig{};
  for(int i=0;i<12;i++)start[i]=2*i;
  enumerate(0,0,start,sig,{}, {});
  cout<<"RANK7_GEOMETRY_WORDS "<<emitted<<"\n";
 } catch(const exception& e){cerr<<e.what()<<"\n";return 1;}
}
