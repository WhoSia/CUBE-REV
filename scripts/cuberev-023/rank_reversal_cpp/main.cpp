// CUBE-REV 0.23 P3-R0 — independent C++ physical R6 PDB-order receipt verifier.
#include <algorithm>
#include <cassert>
#include <fstream>
#include <iostream>
#include <set>
#include <sstream>
#include <string>
#include <vector>
using namespace std;
int main() {
 ifstream in("data/cuberev-023/p3_r0_source_matched_R6_real_PDB_10_action_census.csv");
 if(!in) return 1;
 string header,line;getline(in,header);
 if(header!="move,main_d,alt_d,main_h,alt_h,main_corner,alt_corner,main_edge,alt_edge")return 2;
 int n=0,reverse=0,both=0,low=100,high=-100,sm=0,sa=0,sh=0,ah=0;
 set<string> seen;
 while(getline(in,line)){
  if(line.empty())continue;
  stringstream ss(line);string x;vector<string> p;
  while(getline(ss,x,','))p.push_back(x);
  if(p.size()!=9||!seen.insert(p[0]).second)return 3;
  vector<int> a; for(size_t i=1;i<p.size();i++){try {a.push_back(stoi(p[i]));}catch(...){return 4;}}
  const int dm=a[0],da=a[1],hm=a[2],ha=a[3],cm=a[4],ca=a[5],em=a[6],ea=a[7];
  if(hm!=max(cm,em)||ha!=max(ca,ea)||hm>dm||ha>da)return 5;
  if(cm<ca||em<=ea||ha>=hm||da<=dm)return 6;
  if(cm>ca&&em>ea)both++;
  if(ha<hm&&da>dm)reverse++;
  int gap=1+da-dm;
  if(gap<2||gap>5)return 7;
  low=min(low,gap);high=max(high,gap);
  sm+=dm;sa+=da;sh+=hm;ah+=ha;
  n++;
 }
 if(n!=10||reverse!=10||seen.size()!=10)return 8;
 for(auto s:{"U","U2","U'","D","D2","D'","R2","L2","F2","B2"})if(!seen.count(s))return 9;
 cout<<"CUBE_REV_023_P3_R0_ROWS="<<n<<" REVERSE="<<reverse
 <<" STRICT_BOTH="<<both<<" RAW_GAP_MIN="<<low<<" RAW_GAP_MAX="<<high
 <<" MAIN_D_SUM="<<sm<<" ALT_D_SUM="<<sa<<" MAIN_H_SUM="<<sh
 <<" ALT_H_SUM="<<ah<<" ALL18_CHILD_EXACT=NOT_COMPUTED HUMAN_COGNITION=NOT_IDENTIFIED\n";
}
