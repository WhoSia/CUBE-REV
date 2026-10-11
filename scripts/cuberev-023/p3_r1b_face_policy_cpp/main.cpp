// P3-R1B independent C++17 exact optimal six-face-query frontier across
// 62 real physical cubie source states. No human perception inference.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <functional>
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <string>
#include <tuple>
#include <vector>
using namespace std;
static constexpr int N=62;
static constexpr char FACES[]="URFDLB";
array<array<string,6>,N> state;
map<tuple<uint64_t,int,int>,int> memo;
int pop(uint64_t x){return __builtin_popcountll(x);}
vector<uint64_t> branches(uint64_t subset,int face){
 map<string,uint64_t> p;
 for(int i=0;i<N;i++)if(subset&(1ULL<<i))p[state[i][face]]|=1ULL<<i;
 vector<uint64_t> out;for(auto &v:p)out.push_back(v.second);return out;
}
int leaves(uint64_t subset,int used,int q){
 if(pop(subset)<=1||q==0)return 1;
 auto k=make_tuple(subset,used,q);auto v=memo.find(k);if(v!=memo.end())return v->second;
 int best=1;
 for(int face=0;face<6;face++)if(!(used&(1<<face))){
  auto parts=branches(subset,face);if(parts.size()<2)continue;
  int sum=0;
  for(auto part:parts)sum+=leaves(part,used|(1<<face),q-1);
  best=max(best,sum);
 }
 if(best>pop(subset))return -999;
 return memo[k]=best;
}
int main(){
 ifstream in("data/cuberev-023/p3_r1b_real_62_physical_face9_cubie_fixture.csv");if(!in)return 1;
 string line;getline(in,line);if(line!="index,U,R,F,D,L,B,source_HTM,cubie_sha256")return 2;
 set<string> observations,hashes;
 for(int i=0;i<N;i++){
  if(!getline(in,line))return 3;
  stringstream ss(line);vector<string> vals;string v;while(getline(ss,v,','))vals.push_back(v);
  if(vals.size()!=9||stoi(vals[0])!=i||stoi(vals[7])>5||stoi(vals[7])<0)return 4;
  if(vals[8].size()!=64||!hashes.insert(vals[8]).second)return 5;
  map<char,int> colors;string all;
  for(int j=0;j<6;j++){
   if(vals[j+1].size()!=9)return 6;
   state[i][j]=vals[j+1];all+=state[i][j];
   for(char c:state[i][j])if(string(FACES).find(c)==string::npos)return 7;else colors[c]++;
  }
  for(int c=0;c<6;c++)if(colors[FACES[c]]!=9)return 8;
  if(!observations.insert(all).second)return 9;
 }
 if(getline(in,line)&&!line.empty())return 10;
 array<int,7> fixed{};int minFixed=7;vector<string> best;
 for(int mask=0;mask<64;mask++){
  int n=__builtin_popcount(unsigned(mask));set<string> patterns;
  for(int i=0;i<N;i++){
   string sig;
   for(int j=0;j<6;j++)sig+=(mask&(1<<j))?state[i][j]:"?";
   patterns.insert(sig);
  }
  int nClasses=int(patterns.size());fixed[n]=max(fixed[n],nClasses);
  if(nClasses==N){
   string faces;for(int j=0;j<6;j++)if(mask&(1<<j))faces+=FACES[j];
   if(n<minFixed){minFixed=n;best={faces};}else if(n==minFixed)best.push_back(faces);
  }
 }
 const uint64_t ALL=(1ULL<<N)-1ULL;
 array<int,7> adaptive{};int minAdaptive=-1;
 for(int q=0;q<=6;q++){
  adaptive[q]=leaves(ALL,0,q);
  if(adaptive[q]<fixed[q])return 11;
  if(minAdaptive==-1&&adaptive[q]==N)minAdaptive=q;
 }
 if(minFixed!=4||minAdaptive!=4||fixed!=array<int,7>{1,12,38,50,62,62,62}||adaptive!=array<int,7>{1,12,42,58,62,62,62})return 12;
 if(best!=vector<string>{"URFB","RFDB","UFLB","FDLB"})return 13;
 auto fmt=[](const array<int,7>& a){string s;for(int i=0;i<7;i++){if(i)s+="/";s+=to_string(a[i]);}return s;};
 string bestStr;for(size_t i=0;i<best.size();i++){if(i)bestStr+=";";bestStr+=best[i];}
 cout<<"CUBE_REV_023_P3_R1B_STATES=62 CORNER_WORDS=1 FULL_WORDS=62 ADAPTIVE_MIN="<<minAdaptive<<" FIXED_MIN="<<minFixed
  <<" ADAPTIVE_FRONTIER="<<fmt(adaptive)<<" FIXED_FRONTIER="<<fmt(fixed)<<" BEST_FIXED="<<bestStr
  <<" SOURCE=ORIGINAL_CUBIE_STICKERS HUMAN_COGNITION=NOT_MEASURED\n";
}
