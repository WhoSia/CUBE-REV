// CUBE-REV 0.24 P1-R3 — independent original-facelet C++17 DR bridge.
// Unlike IDA from scratch on the full 18HTM group, this computes admissible
// (corner-orientation,slice) and (edge-orientation,slice) PDBs to a genuine
// two-phase physical subgroup, then exact PDB IDA* in its 10-move grammar.
// Constructive solution is a certified full-cube UPPER BOUND, not HTM optimum.
#include <bits/stdc++.h>
using namespace std;
using Clock=chrono::steady_clock;
struct Vec {int x,y,z; bool operator==(const Vec&v)const{return x==v.x&&y==v.y&&z==v.z;}};
Vec plusv(Vec a,Vec b){return {a.x+b.x,a.y+b.y,a.z+b.z};}
Vec rot(Vec v,int axis,int q){q=(q%4+4)%4;while(q--){int x=v.x,y=v.y,z=v.z;if(axis==0)v={x,-z,y};if(axis==1)v={z,y,-x};if(axis==2)v={-y,x,z};}return v;}
struct Sticker{Vec p,n;char c;};
using Stickers=array<Sticker,54>;
const string faceNames="URFDLB";
Vec norm(char face){switch(face){case 'U':return {0,1,0};case 'R':return {1,0,0};case 'F':return {0,0,1};case 'D':return {0,-1,0};case 'L':return {-1,0,0};default:return {0,0,-1};}}
Stickers solvedStickers(){Stickers s;int k=0;for(char f:faceNames){Vec n=norm(f);for(int a=-1;a<=1;a++)for(int b=-1;b<=1;b++){Vec p=n.x?Vec{n.x,a,b}:n.y?Vec{a,n.y,b}:Vec{a,b,n.z};s[k++]={p,n,f};}}return s;}
void physicalTurn(Stickers &s, const string&t){char f=t[0];int axis,layer,q;if(f=='U'){axis=1;layer=1;q=-1;}else if(f=='D'){axis=1;layer=-1;q=1;}else if(f=='R'){axis=0;layer=1;q=-1;}else if(f=='L'){axis=0;layer=-1;q=1;}else if(f=='F'){axis=2;layer=1;q=-1;}else if(f=='B'){axis=2;layer=-1;q=1;}else throw runtime_error("non outer-face turn");int power=t.size()==1?1:t[1]=='2'?2:3;for(auto &st:s){int d=axis==0?st.p.x:axis==1?st.p.y:st.p.z;if(d==layer){st.p=rot(st.p,axis,q*power);st.n=rot(st.n,axis,q*power);}}}
string stickerAt(const Stickers&s,Vec p,Vec n){for(auto v:s)if(v.p==p&&v.n==n)return string(1,v.c);throw runtime_error("physical sticker missing");}
const vector<vector<Vec>> cornerN={{{0,1,0},{1,0,0},{0,0,1}},{{0,1,0},{0,0,1},{-1,0,0}},{{0,1,0},{-1,0,0},{0,0,-1}},{{0,1,0},{0,0,-1},{1,0,0}},{{0,-1,0},{0,0,1},{1,0,0}},{{0,-1,0},{-1,0,0},{0,0,1}},{{0,-1,0},{0,0,-1},{-1,0,0}},{{0,-1,0},{1,0,0},{0,0,-1}}};
const array<string,8> cornerC={"URF","UFL","ULB","UBR","DFR","DLF","DBL","DRB"};
const vector<vector<Vec>> edgeN={{{0,1,0},{1,0,0}},{{0,1,0},{0,0,1}},{{0,1,0},{-1,0,0}},{{0,1,0},{0,0,-1}},{{0,-1,0},{1,0,0}},{{0,-1,0},{0,0,1}},{{0,-1,0},{-1,0,0}},{{0,-1,0},{0,0,-1}},{{0,0,1},{1,0,0}},{{0,0,1},{-1,0,0}},{{0,0,-1},{-1,0,0}},{{0,0,-1},{1,0,0}}};
const array<string,12> edgeC={"UR","UF","UL","UB","DR","DF","DL","DB","FR","FL","BL","BR"};
struct Cube{array<uint8_t,8>cp,co;array<uint8_t,12>ep,eo;};
Cube solved(){Cube s;for(int i=0;i<8;i++)s.cp[i]=i,s.co[i]=0;for(int i=0;i<12;i++)s.ep[i]=i,s.eo[i]=0;return s;}
Cube fromStickers(const Stickers&st){Cube s;for(int p=0;p<8;p++){Vec v={0,0,0};for(auto n:cornerN[p])v=plusv(v,n);string c;for(auto n:cornerN[p])c+=stickerAt(st,v,n);int ori=0;while(ori<3&&c[ori]!='U'&&c[ori]!='D')ori++;if(ori==3)throw runtime_error("corner orientation illegal");bool match=false;for(int i=0;i<8;i++)if(c[(ori+1)%3]==cornerC[i][1]&&c[(ori+2)%3]==cornerC[i][2]){s.cp[p]=i;s.co[p]=ori;match=true;break;}if(!match)throw runtime_error("corner identity illegal");}
for(int p=0;p<12;p++){Vec v=plusv(edgeN[p][0],edgeN[p][1]);string c;for(auto n:edgeN[p])c+=stickerAt(st,v,n);bool match=false;for(int i=0;i<12;i++)if(c==edgeC[i]||c==string(edgeC[i].rbegin(),edgeC[i].rend())){s.ep[p]=i;s.eo[p]=(c!=edgeC[i]);match=true;break;}if(!match)throw runtime_error("edge identity illegal");}return s;}
bool solvedState(const Cube&s){Cube z=solved();return s.cp==z.cp&&s.co==z.co&&s.ep==z.ep&&s.eo==z.eo;}
Cube composeCube(const Cube&s,const Cube&m){Cube out;for(int i=0;i<8;i++){out.cp[i]=s.cp[m.cp[i]];out.co[i]=(s.co[m.cp[i]]+m.co[i])%3;}for(int i=0;i<12;i++){out.ep[i]=s.ep[m.ep[i]];out.eo[i]=s.eo[m.ep[i]]^m.eo[i];}return out;}
const vector<string> names=[](){vector<string>n;for(char c:faceNames)for(string suf:{string(""),string("'"),string("2")})n.push_back(string(1,c)+suf);return n;}();
array<Cube,18> turn;
int fromName(string s){auto i=find(names.begin(),names.end(),s);if(i==names.end())throw runtime_error("invalid legal move: "+s);return int(i-names.begin());}
void initTurns(){for(int i=0;i<18;i++){Stickers s=solvedStickers();physicalTurn(s,names[i]);turn[i]=fromStickers(s);Cube x=solved();x=composeCube(x,turn[i]);if(x.cp!=turn[i].cp||x.ep!=turn[i].ep)throw runtime_error("broken generator");}}
vector<int>parse(string input){istringstream in(input);vector<int>out;string token;while(in>>token)out.push_back(fromName(token));return out;}
Cube cubeAfter(const vector<int>&w){Cube s=solved();for(int m:w)s=composeCube(s,turn[m]);return s;}
bool physicalSolves(const vector<int>&scr,const vector<int>&word){Stickers s=solvedStickers();for(int i:scr)physicalTurn(s,names[i]);for(int i:word)physicalTurn(s,names[i]);return solvedState(fromStickers(s));}
vector<int>normalizeLegalHTM(const vector<int>&word){
 vector<int>out;
 for(int m:word){
  if(!out.empty() && out.back()/3==m/3){
   auto power=[](int id){return id%3==0?1:id%3==1?3:2;};
   int sum=(power(out.back())+power(m))%4;
   out.pop_back();
   if(sum){int face=m/3;out.push_back(face*3+(sum==1?0:sum==2?2:1));}
  }else out.push_back(m);
 }
 return out;
}
string join(const vector<int>&w){string s;for(auto i:w){if(!s.empty())s+=' ';s+=names[i];}return s;}
// True whole-cube axis conjugacy: rotate the original fixed facelets and
// rename ALL six color labels using transformed physical centers, so that
// the rotated solved reference remains the original solved target.
char faceOfNormal(Vec n){for(char f:faceNames)if(norm(f)==n)return f;throw runtime_error("bad frame normal");}
struct Frame{Stickers cube;array<char,6>originalToLocal;array<char,6>localToOriginal;};
Frame inFrame(const Stickers&base, int axis){
 Frame f;f.cube=base;for(int i=0;i<6;i++)f.originalToLocal[i]=faceNames[i],f.localToOriginal[i]=faceNames[i];
 if(axis<0)return f;
 for(auto &st:f.cube){st.p=rot(st.p,axis,-1);st.n=rot(st.n,axis,-1);}
 for(const auto &st:f.cube)if(st.p==st.n)f.originalToLocal[faceNames.find(st.c)]=faceOfNormal(st.n);
 for(int i=0;i<6;i++){int j=faceNames.find(f.originalToLocal[i]);f.localToOriginal[j]=faceNames[i];}
 for(auto &st:f.cube)st.c=f.originalToLocal[faceNames.find(st.c)];
 return f;
}
vector<int>backToOriginal(const vector<int>&words,const Frame&f){vector<int>v;for(int m:words){string t=names[m];t[0]=f.localToOriginal[faceNames.find(t[0])];v.push_back(fromName(t));}return v;}
int factorial[13];
int rankPerm(const uint8_t*p,int n){int r=0;for(int i=0;i<n;i++){int d=0;for(int j=i+1;j<n;j++)d+=(p[j]<p[i]);r=r*(n-i)+d;}return r;}
void unrankPerm(int r,int n,uint8_t*p){vector<int>pool(n);iota(pool.begin(),pool.end(),0);int idx[12];for(int i=n-1;i>=0;i--){idx[i]=r%(n-i);r/=n-i;}if(r)throw runtime_error("perm rank overrun");for(int i=0;i<n;i++){p[i]=pool[idx[i]];pool.erase(pool.begin()+idx[i]);}}
int coIndex(const Cube&s){int r=0;for(int i=0;i<7;i++)r=3*r+s.co[i];return r;}
int eoIndex(const Cube&s){int r=0;for(int i=0;i<11;i++)r=2*r+s.eo[i];return r;}
void unrankOri(int i,int n,int base,uint8_t*a){int sum=0;for(int j=n-2;j>=0;j--){a[j]=i%base;i/=base;sum+=a[j];}a[n-1]=(base-sum%base)%base;}
int rankOri(const uint8_t*a,int n,int base){int r=0;for(int j=0;j<n-1;j++)r=r*base+a[j];return r;}
int sliceMask(const Cube&s){int mask=0;for(int i=0;i<12;i++)if(s.ep[i]>=8)mask|=1<<i;return mask;}
int sliceID[4096];int masks[495];array<array<uint16_t,18>,2187>coTurn;array<array<uint16_t,18>,2048>eoTurn;array<array<uint16_t,18>,495>slTurn;
array<uint8_t,1082565>pdbCOslice;array<uint8_t,1013760>pdbEOslice;
int goalSl;
void initPhase1(){fill(begin(sliceID),end(sliceID),-1);int k=0;for(int mask=0;mask<4096;mask++)if(__builtin_popcount((unsigned)mask)==4){sliceID[mask]=k;masks[k++]=mask;}if(k!=495)throw runtime_error("invalid slice count");goalSl=sliceID[(1<<8)|(1<<9)|(1<<10)|(1<<11)];
for(int x=0;x<2187;x++){Cube s=solved();unrankOri(x,8,3,s.co.data());for(int j=0;j<18;j++)coTurn[x][j]=coIndex(composeCube(s,turn[j]));}
for(int x=0;x<2048;x++){Cube s=solved();unrankOri(x,12,2,s.eo.data());for(int j=0;j<18;j++)eoTurn[x][j]=eoIndex(composeCube(s,turn[j]));}
for(int x=0;x<495;x++){Cube s=solved();int mask=masks[x],a=0,b=8;for(int i=0;i<12;i++)s.ep[i]=(mask&(1<<i))?b++:a++;for(int j=0;j<18;j++)slTurn[x][j]=sliceID[sliceMask(composeCube(s,turn[j]))];}
auto fillPdb=[&](auto&dist,int na,const auto&trans){fill(dist.begin(),dist.end(),255);vector<int>q(dist.size());int goal=goalSl;dist[goal]=0;q[0]=goal;size_t head=0,tail=1;while(head<tail){int state=q[head++],c=state/495,sl=state%495;auto d=dist[state];for(int a=0;a<18;a++){int child=trans[c][a]*495+slTurn[sl][a];if(dist[child]!=255)continue;dist[child]=d+1;q[tail++]=child;}}if(tail!=dist.size())throw runtime_error("incomplete phase1 PDB "+to_string(tail));};
fillPdb(pdbCOslice,2187,coTurn);fillPdb(pdbEOslice,2048,eoTurn);
}
int phase1H(const Cube&s){int sl=sliceID[sliceMask(s)];return max<int>(pdbCOslice[coIndex(s)*495+sl],pdbEOslice[eoIndex(s)*495+sl]);}
const vector<int> moves2=[](){vector<int>v;for(int i=0;i<18;i++){string s=names[i];if(s[0]=='U'||s[0]=='D'||s.back()=='2')v.push_back(i);}return v;}();
array<array<uint16_t,10>,40320>cpTurn,udTurn;array<array<uint8_t,10>,24>esTurn;
vector<uint8_t> pdbCPE,pdbUDE;
int rankCP(const Cube&s){return rankPerm(s.cp.data(),8);}
int rankUD(const Cube&s){return rankPerm(s.ep.data(),8);}
int rankES(const Cube&s){uint8_t a[4];for(int i=0;i<4;i++)a[i]=s.ep[8+i]-8;return rankPerm(a,4);}
void initPhase2(){for(int p=0;p<40320;p++){uint8_t perm[8];unrankPerm(p,8,perm);Cube c=solved(),e=solved();for(int i=0;i<8;i++)c.cp[i]=perm[i],e.ep[i]=perm[i];for(int j=0;j<10;j++){cpTurn[p][j]=rankCP(composeCube(c,turn[moves2[j]]));udTurn[p][j]=rankUD(composeCube(e,turn[moves2[j]]));}}
for(int p=0;p<24;p++){uint8_t perm[4];unrankPerm(p,4,perm);Cube s=solved();for(int i=0;i<4;i++)s.ep[i+8]=perm[i]+8;for(int j=0;j<10;j++)esTurn[p][j]=rankES(composeCube(s,turn[moves2[j]]));}
int n=40320*24;pdbCPE.assign(n,255);pdbUDE.assign(n,255);auto fillPdb=[&](vector<uint8_t>&dist,const auto&trans){vector<int>q(n);dist[0]=0;q[0]=0;int head=0,tail=1;while(head<tail){int idx=q[head++],a=idx/24,b=idx%24,d=dist[idx];for(int j=0;j<10;j++){int v=trans[a][j]*24+esTurn[b][j];if(dist[v]!=255)continue;dist[v]=d+1;q[tail++]=v;}}if(tail!=n)throw runtime_error("incomplete phase2 967680 table "+to_string(tail));};fillPdb(pdbCPE,cpTurn);fillPdb(pdbUDE,udTurn);
}
int phase2H(int cp,int ud,int es){return max<int>(pdbCPE[cp*24+es],pdbUDE[ud*24+es]);}
bool sameFace(int a,int b){return a/3==b/3;}
bool canonical(int last,int next){if(last<0)return true;if(sameFace(last,next))return false;int fa=last/3,fb=next/3;bool opposite=(fa==0&&fb==3)||(fa==3&&fb==0)||(fa==1&&fb==4)||(fa==4&&fb==1)||(fa==2&&fb==5)||(fa==5&&fb==2);return !opposite||fb>=fa;}
struct Result{bool solved=false;vector<int>p1,p2;uint64_t node1=0,node2=0;int phase2Optimal=-1;int contacts=0;string status;double runtime=0;};
const uint64_t P1CAP=10000000,P2CAP=140000000;
struct Search{Result res;vector<int>path1,path2;int limit1;int phase2Goal;bool stop=false;chrono::steady_clock::time_point start;int seconds=65;string why="";int sampleLimit=1;
 bool timeout(){return chrono::duration_cast<chrono::seconds>(Clock::now()-start).count()>seconds;}
 bool phase2dfs(int cp,int ud,int es,int g,int bound,int last){if(res.node2++>=P2CAP||timeout()){stop=true;why="phase2_resource";return false;}if(g+phase2H(cp,ud,es)>bound)return false;if(cp==0&&ud==0&&es==0)return true;if(g==bound)return false;for(int i=0;i<10;i++){int a=moves2[i];if(!canonical(last,a))continue;path2.push_back(a);if(phase2dfs(cpTurn[cp][i],udTurn[ud][i],esTurn[es][i],g+1,bound,a))return true;path2.pop_back();if(stop)return false;}return false;}
 bool solvePhase2(const Cube&s){int cp=rankCP(s),ud=rankUD(s),es=rankES(s);int h=phase2H(cp,ud,es);for(int bound=h;bound<=21;bound++){path2.clear();if(phase2dfs(cp,ud,es,0,bound,-1)){res.phase2Optimal=bound;return true;}if(stop)return false;}return false;}
 bool dfs1(Cube s,int co,int eo,int sl,int g,int bound,int last){if(res.node1++>=P1CAP||timeout()){stop=true;why="phase1_resource";return false;}int h=max<int>(pdbCOslice[co*495+sl],pdbEOslice[eo*495+sl]);if(g+h>bound)return false;if(h==0){if(solvePhase2(s)){
   res.contacts++;
   if(!res.solved||path1.size()+path2.size()<res.p1.size()+res.p2.size()){
     res.p1=path1;res.p2=path2;res.solved=true;
   }
   return res.contacts>=sampleLimit;
 }return false;}
 if(g==bound)return false;for(int a=0;a<18;a++){if(!canonical(last,a))continue;path1.push_back(a);if(dfs1(composeCube(s,turn[a]),coTurn[co][a],eoTurn[eo][a],slTurn[sl][a],g+1,bound,a))return true;path1.pop_back();if(stop)return false;}return false;}
 Result solve(const Cube&s,int sec=65){start=Clock::now();seconds=sec;int co=coIndex(s),eo=eoIndex(s),sl=sliceID[sliceMask(s)];int initH=max<int>(pdbCOslice[co*495+sl],pdbEOslice[eo*495+sl]);for(int b=initH;b<=15;b++){limit1=b;path1.clear();if(dfs1(s,co,eo,sl,0,b,-1)){res.status="SOLVED_SAMPLED_DR_FIRST_BOUND_NOT_GLOBAL_OPTIMAL";break;}if(res.solved){res.status="SOLVED_PARTIAL_DR_CONTACTS_NOT_GLOBAL_OPTIMAL";break;}if(stop)break;}if(!res.solved)res.status="HOLD_"+(why.empty()?string("DEPTH15"):why);res.runtime=chrono::duration<double>(Clock::now()-start).count();return res;}
};
int main(int argc,char**argv){try{auto init=Clock::now();initTurns();initPhase1();auto d1=chrono::duration<double>(Clock::now()-init).count();initPhase2();auto d2=chrono::duration<double>(Clock::now()-init).count();cerr<<"PDB_BUILD_SECONDS phase1="<<d1<<" total="<<d2<<" phase1_states="<<(1082565+1013760)<<" phase2_states="<<(2*967680)<<"\n";
vector<pair<string,string>>cases={{"WCA_SeoulSummer2026_333_Final_A_1","R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2"},{"WCA_SeoulSummer2026_333_First_A_1","L2 F2 U F2 R2 U B2 R2 D U F L U F' R2 B R' D B'"},{"FMC_World2026_Miao_main_EO_DR","R' U' F L2 D' L2 U' R U F' D R L' F U2 D2 F L2 F' R2 F2 D R' U' F L2 F' L D L2 F2 B L B2 L"},{"FMC_World2026_Riabov_main_EO_DR","R' U' F L2 D' L2 U' R U F' D R L' F U2 D2 F L2 F' R2 F2 D R' U' F L2 F' L D L2 B F2 L B2 L"}};
if(argc>1){cases.clear();string s;for(int i=1;i<argc;i++){if(i>1)s+=' ';s+=argv[i];}cases.push_back({"CUSTOM",s});}
for(auto [name,s]:cases){auto scramble=parse(s);Stickers facelet=solvedStickers();for(int m:scramble)physicalTurn(facelet,names[m]);Cube state=fromStickers(facelet);Cube fast=cubeAfter(scramble);if(state.cp!=fast.cp||state.co!=fast.co||state.ep!=fast.ep||state.eo!=fast.eo)throw runtime_error("cubie action and physical 54 sticker mismatch!");// All three axis choices share identical physical moves by conjugacy.
// The local phase2 proof remains grammar-relative, never global full18.
int bestLen=10000,bestAxis=-1;vector<int>bestWord;Result bestResult;
for(int axis : {-1,0,2}){
 Frame f=inFrame(facelet,axis);
 auto local=fromStickers(f.cube);
 Search solver;solver.sampleLimit=128;auto result=solver.solve(local,65);
 vector<int>localWord=result.p1;localWord.insert(localWord.end(),result.p2.begin(),result.p2.end());
 vector<int>word=backToOriginal(localWord,f);
 if(result.solved&&!physicalSolves(scramble,word))throw runtime_error("54-sticker full original replay FAILED under frame conjugacy");
 cout<<"FRAME "<<name<<" AXIS "<<(axis<0?"UD":axis==0?"FB":"LR")<<" STATUS "<<result.status<<" P1 "<<result.p1.size()<<" P2 "<<result.p2.size()<<" CONTACTS "<<result.contacts<<" RAW_TOTAL "<<(result.solved?int(word.size()):-1)<<" N1 "<<result.node1<<" N2 "<<result.node2<<" SECONDS "<<result.runtime<<"\n";
 if(result.solved && word.size()<size_t(bestLen)){bestLen=word.size();bestAxis=axis;bestWord=word;bestResult=result;}
}
cout<<"CASE "<<name<<" STATUS "<<(bestAxis>=-1&&bestLen<10000?"SOLVED_PHYSICALLY_ALL54":"HOLD")<<" SCRAMBLE_LEN "<<scramble.size()<<" BEST_AXIS "<<(bestAxis<0?"UD":bestAxis==0?"FB":"LR")<<" P1 "<<bestResult.p1.size()<<" P2 "<<bestResult.p2.size()<<" SOLUTION_LEN "<<(bestLen<10000?bestLen:-1)<<"\n";
// Preserve the trivial reverse-scramble complete-solve baseline. A longer
// two-phase solution cannot be presented as a search improvement.
vector<int>inverse;
for(auto it=scramble.rbegin();it!=scramble.rend();++it){int face=*it/3,variant=*it%3;inverse.push_back(3*face+(variant==0?1:variant==1?0:2));}
if(!physicalSolves(scramble,inverse))throw runtime_error("inverse-original-HTM baseline failed physical full replay");
auto inverseNormalized=normalizeLegalHTM(inverse);
if(!physicalSolves(scramble,inverseNormalized))throw runtime_error("normalized inverse scramble failed");
if(bestLen<10000){auto normword=normalizeLegalHTM(bestWord);if(!physicalSolves(scramble,normword))throw runtime_error("normalized source original cube not solved");
 cout<<"NORMALIZED_LENGTH "<<normword.size()<<"\n";
 cout<<"SOLUTION "<<join(normword)<<"\n";
 cout<<"INVERSE_SCRAMBLE_BASELINE_LEN "<<inverseNormalized.size()<<"\n";
 if(inverseNormalized.size()<=normword.size())cout<<"WINNER INVERSE_OR_TIE_SCRAMBLE_UPPER_BOUND\n";
 else cout<<"WINNER STRICTLY_SHORTER_CONSTRUCTIVE_TWOPHASE_UPPER_BOUND\n";
}
cout.flush();}
}catch(const exception&e){cerr<<"CRITICAL_ERROR "<<e.what()<<"\n";return 1;}}