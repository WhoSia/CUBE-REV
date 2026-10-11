// CUBE-REV 0.23 P3-R3. Independent C++20 maximum-independent-set
// oracle for physically sourced 62 x 6 face observations. Not human perception.
#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <string>
#include <vector>
using namespace std;
constexpr int N=62;
constexpr const char* PATH="data/cuberev-023/p3_r1b_real_62_physical_face9_cubie_fixture.csv";
array<array<string,6>,N> observation;
struct ExactIndependentSet {
 vector<uint64_t> neighbors;
 map<uint64_t,uint64_t> memo;
 uint64_t solve(uint64_t mask){
  auto found=memo.find(mask);if(found!=memo.end())return found->second;
  int pivot=-1,maxDegree=0;
  for(int i=0;i<(int)neighbors.size();i++)if(mask&(1ULL<<i)){
   int degree=popcount(neighbors[i]&mask);
   if(degree>maxDegree){maxDegree=degree;pivot=i;}
  }
  if(pivot<0)return memo[mask]=mask;
  uint64_t excluded=solve(mask&~(1ULL<<pivot));
  uint64_t included=solve(mask&~(neighbors[pivot]|(1ULL<<pivot)))|(1ULL<<pivot);
  return memo[mask]=(popcount(excluded)>=popcount(included))?excluded:included;
 }
};
int distance(int i,int j,int mask){
 int n=0;for(int f=0;f<6;f++)if(mask&(1<<f))n+=observation[i][f]!=observation[j][f];return n;
}
int main(){
 ifstream in(PATH);if(!in)return 1;string line;
 if(!getline(in,line)||line!="index,U,R,F,D,L,B,source_HTM,cubie_sha256")return 2;
 set<string> uniqueKeys;
 for(int i=0;i<N;i++){
  if(!getline(in,line))return 3;
  stringstream ss(line);string cell;vector<string> row;
  while(getline(ss,cell,','))row.push_back(cell);
  if(row.size()!=9||stoi(row[0])!=i||stoi(row[7])<0||stoi(row[7])>5||row[8].size()!=64||!uniqueKeys.insert(row[8]).second)return 4;
  for(int f=0;f<6;f++){if(row[f+1].size()!=9)return 5;observation[i][f]=row[f+1];}
 }
 if(getline(in,line)&&!line.empty())return 6;
 array<int,7> hist{},best{};vector<uint64_t> edge(N);vector<int> erasure;
 for(int mask=0;mask<64;mask++){
  int minimum=7;
  for(int i=0;i<N;i++)for(int j=i+1;j<N;j++){
   int d=distance(i,j,mask);minimum=min(minimum,d);
   if(mask==63){hist[d]++;if(d<=2){edge[i]|=1ULL<<j;edge[j]|=1ULL<<i;}}
  }
  int q=popcount((unsigned)mask);best[q]=max(best[q],minimum);
  if(minimum>=2)erasure.push_back(mask);
 }
 uint64_t unseen=(1ULL<<N)-1;vector<int> witness,components;
 while(unseen){
  uint64_t group=1ULL<<countr_zero(unseen),previous=0;
  while(group!=previous){previous=group;for(int i=0;i<N;i++)if(group&(1ULL<<i))group|=edge[i];}
  unseen&=~group;vector<int> vertices;
  for(int i=0;i<N;i++)if(group&(1ULL<<i))vertices.push_back(i);
  components.push_back((int)vertices.size());
  if(vertices.size()>23)return 7;
  ExactIndependentSet oracle;oracle.neighbors.resize(vertices.size());
  for(int i=0;i<(int)vertices.size();i++)for(int j=0;j<(int)vertices.size();j++)
   if(edge[vertices[i]]&(1ULL<<vertices[j]))oracle.neighbors[i]|=1ULL<<j;
  uint64_t selected=oracle.solve((1ULL<<vertices.size())-1);
  for(int i=0;i<(int)vertices.size();i++)if(selected&(1ULL<<i))witness.push_back(vertices[i]);
 }
 sort(witness.begin(),witness.end());
 for(int i=0;i<(int)witness.size();i++)for(int j=i+1;j<(int)witness.size();j++)if(distance(witness[i],witness[j],63)<3)return 8;
 if(hist!=array<int,7>{0,0,142,216,390,400,743})return 9;
 if(best!=array<int,7>{0,0,0,0,1,1,2}||erasure!=vector<int>{63})return 10;
 if(witness.size()!=26)return 11;
 cout<<"P3R3 CPP STATES=62 PAIRS=1891 HIST=";
 for(int i=0;i<7;i++){if(i)cout<<"/";cout<<hist[i];}
 cout<<" ONE_ERROR_CORRECTABLE_CAPACITY="<<witness.size()<<" WITNESS=";
 for(int i=0;i<(int)witness.size();i++){if(i)cout<<",";cout<<witness[i];}
 cout<<" COMPONENTS=";for(int i=0;i<(int)components.size();i++){if(i)cout<<",";cout<<components[i];}
 cout<<" PROOF=EXHAUSTIVE_INDEPENDENT_SET\n";
}
