// CUBE-REV 0.25 P0-R1: original physical 3x3 Schreier quotients,
// exact 4-cubie PDB, common face-Parikh parity synchronization, no-go.
// Existing WCA 14<=d18<=18 is NOT strengthened by these quotients.
#include <bits/stdc++.h>
using namespace std;
struct V{int x,y,z;bool operator==(V b)const{return x==b.x&&y==b.y&&z==b.z;}V operator+(V b)const{return{x+b.x,y+b.y,z+b.z};}};
V rotateV(V v,int axis,int power){power=(power%4+4)%4;while(power--){int x=v.x,y=v.y,z=v.z;if(axis==0)v={x,-z,y};if(axis==1)v={z,y,-x};if(axis==2)v={-y,x,z};}return v;}
const array<V,6> faces={{{0,1,0},{1,0,0},{0,0,1},{0,-1,0},{-1,0,0},{0,0,-1}}};
const V corners[8][3]={
 {{0,1,0},{1,0,0},{0,0,1}}, {{0,1,0},{0,0,1},{-1,0,0}},
 {{0,1,0},{-1,0,0},{0,0,-1}}, {{0,1,0},{0,0,-1},{1,0,0}},
 {{0,-1,0},{0,0,1},{1,0,0}}, {{0,-1,0},{-1,0,0},{0,0,1}},
 {{0,-1,0},{0,0,-1},{-1,0,0}}, {{0,-1,0},{1,0,0},{0,0,-1}}};
const V edges[12][2]={
 {{0,1,0},{1,0,0}},{{0,1,0},{0,0,1}},{{0,1,0},{-1,0,0}},{{0,1,0},{0,0,-1}},
 {{0,-1,0},{1,0,0}},{{0,-1,0},{0,0,1}},{{0,-1,0},{-1,0,0}},{{0,-1,0},{0,0,-1}},
 {{0,0,1},{1,0,0}},{{0,0,1},{-1,0,0}},{{0,0,-1},{-1,0,0}},{{0,0,-1},{1,0,0}}};
struct Move{string name;int axis,layer,q;};array<Move,18> moves;using Table=array<array<uint8_t,24>,18>;Table eMove{},cMove{};constexpr int CAP=24*24*24*24;
int coord(V v,int ax){return ax==0?v.x:ax==1?v.y:v.z;}
V physical(V v,V place,Move m){return coord(place,m.axis)==m.layer?rotateV(v,m.axis,m.q):v;}
void check(bool x,const string&msg){if(!x)throw runtime_error(msg);}
void init(){string ns="URFDLB";for(int f=0;f<6;f++){int ax=f==0||f==3?1:f==1||f==4?0:2;int layer=f<3?1:-1;int q=(f<3?-1:1);for(int t=0;t<3;t++){int k=3*f+t;moves[k]={string(1,ns[f])+(t==1?"'":t==2?"2":""),ax,layer,q*(t==1?3:t==2?2:1)};}}
for(int a=0;a<18;a++){auto m=moves[a];for(int p=0;p<12;p++){V x=edges[p][0]+edges[p][1];V nx=physical(x,x,m);for(int o=0;o<2;o++){V n=physical(edges[p][o],x,m);int target=-1;for(int j=0;j<12;j++)if(edges[j][0]+edges[j][1]==nx)for(int k=0;k<2;k++)if(edges[j][k]==n)target=2*j+k;check(target>=0,"edge physical move no target");eMove[a][2*p+o]=target;}}
for(int p=0;p<8;p++){V x=corners[p][0]+corners[p][1]+corners[p][2];V nx=physical(x,x,m);for(int o=0;o<3;o++){V n=physical(corners[p][o],x,m);V n2=physical(corners[p][(o+1)%3],x,m);int target=-1;for(int j=0;j<8;j++)if(corners[j][0]+corners[j][1]+corners[j][2]==nx)for(int k=0;k<3;k++)if(corners[j][k]==n&&corners[j][(k+1)%3]==n2)target=3*j+k;check(target>=0,"corner chirality orientation map no target");cMove[a][3*p+o]=target;}}
array<bool,24> se{},sc{};for(int k=0;k<24;k++){int e=eMove[a][k],c=cMove[a][k];check(!se[e]&&!sc[c],"token bijection invalid");se[e]=sc[c]=true;}}
cout<<"P0R1_REAL_PHYSICAL_3X3_ALL18_ORIENTED_TOKEN_MAPS PASS\n";}
uint32_t code(array<uint8_t,4>p){uint32_t n=0;for(auto v:p)n=n*24+v;return n;}
array<uint8_t,4> decode(uint32_t n){array<uint8_t,4>p{};for(int i=3;i>=0;i--){p[i]=n%24;n/=24;}return p;}
uint32_t act(uint32_t c,const Table&t,int a){auto p=decode(c);for(auto&v:p)v=t[a][v];return code(p);}
int moveIndex(const string&t){for(int a=0;a<18;a++)if(moves[a].name==t)return a;throw runtime_error("unrecognized actual outer face move");}
vector<int> split(string s){istringstream in(s);vector<int>a;for(string t;in>>t;)a.push_back(moveIndex(t));return a;}
int ones(uint64_t x){return __builtin_popcountll(x);}
uint64_t flip(uint64_t b,int face){constexpr array<uint64_t,6> lo={0x5555555555555555ULL,0x3333333333333333ULL,0x0f0f0f0f0f0f0f0fULL,0x00ff00ff00ff00ffULL,0x0000ffff0000ffffULL,0x00000000ffffffffULL};auto n=1<<face;return ((b&lo[face])<<n)|((b&~lo[face])>>n);}
struct DB{string name;int mod;array<uint8_t,4> ids;const Table*tab;vector<uint8_t> d;vector<uint32_t> queue;int dia=0;array<int,32>layers{};DB(string name_,int mod_,array<uint8_t,4>ids_,const Table*tb):name(name_),mod(mod_),ids(ids_),tab(tb),d(CAP,255){}
uint32_t goal()const{array<uint8_t,4>p;for(int i=0;i<4;i++)p[i]=ids[i]*mod;return code(p);}
uint32_t apply(uint32_t c,const vector<int>&word)const{for(int a:word)c=act(c,*tab,a);return c;}
void build(){uint32_t zero=goal();queue.push_back(zero);d[zero]=0;for(size_t h=0;h<queue.size();h++){auto u=queue[h];int n=d[u];for(int a=0;a<18;a++){uint32_t v=act(u,*tab,a);if(d[v]!=255)continue;auto p=decode(v);unsigned mask=0;for(auto x:p){int pos=x/mod;check(!(mask&(1u<<pos)),"actual positions collided");mask|=(1u<<pos);}d[v]=n+1;queue.push_back(v);}}
int expected=(24/mod)*(24/mod-1)*(24/mod-2)*(24/mod-3);for(int i=0;i<4;i++)expected*=mod;check(queue.size()==size_t(expected),"finite quotient not complete");for(auto u:queue){int n=d[u];dia=max(dia,n);layers[n]++;for(int a=0;a<18;a++){int z=d[act(u,*tab,a)];check(z>=0&&abs(z-n)<=1,"distance fails admissible Lipschitz edge");}}cout<<"P0R1_EXACT_PHYSICAL_PDB "<<name<<" STATES "<<queue.size()<<" DIAMETER "<<dia<<" SOURCE_IDS ";for(int i:ids)cout<<i<<",";cout<<" ONE_LIPSCHITZ PASS\n";}
int h(const vector<int>&w)const{return d[apply(goal(),w)];}
vector<uint64_t> parity(const vector<int>&source,int maxL)const{vector<uint64_t>curr(CAP),next(CAP),out(maxL+1);curr[apply(goal(),source)]=1;out[0]=curr[goal()];vector<array<uint32_t,18>>trans(CAP);for(auto u:queue)for(int a=0;a<18;a++)trans[u][a]=act(u,*tab,a);for(int L=1;L<=maxL;L++){fill(next.begin(),next.end(),0);for(auto u:queue){auto mask=curr[u];if(!mask)continue;for(int a=0;a<18;a++)next[trans[u][a]]|=flip(mask,a/3);}curr.swap(next);out[L]=curr[goal()];}cout<<"P0R1_QUOTIENT_FACE_PARIKH "<<name<<" EVEN_L8 "<<ones(out[8])<<" ODD_L9 "<<ones(out[9])<<"\n";check(ones(out[8])==32&&ones(out[9])==32,"parity-saturation exact receipt failed");return out;}
};
struct Sticker{V p,n;int id;};
vector<Sticker> physical54(const vector<int>&word){vector<Sticker>s;for(V n:faces)for(int a=-1;a<=1;a++)for(int b=-1;b<=1;b++){V p=n.x?V{n.x,a,b}:n.y?V{a,n.y,b}:V{a,b,n.z};s.push_back({p,n,int(s.size())});}check(s.size()==54,"original physical sticker count");for(int a:word)for(auto&st:s){auto m=moves[a];if(coord(st.p,m.axis)==m.layer){st.n=rotateV(st.n,m.axis,m.q);st.p=rotateV(st.p,m.axis,m.q);}}return s;}
void physicalCompare(const vector<DB>&dbs,const vector<int>&word){auto original=physical54({}),now=physical54(word);for(auto&db:dbs){auto projected=decode(db.apply(db.goal(),word));for(int k=0;k<4;k++){int piece=db.ids[k];V loc=db.mod==2?edges[piece][0]+edges[piece][1]:corners[piece][0]+corners[piece][1]+corners[piece][2];V norm=db.mod==2?edges[piece][0]:corners[piece][0];int marker=-1;for(auto x:original)if(x.p==loc&&x.n==norm){marker=x.id;break;}check(marker>=0,"physical cubie marker not present");Sticker st{};for(auto x:now)if(x.id==marker){st=x;break;}int position=-1;for(int i=0;i<(db.mod==2?12:8);i++){V p=db.mod==2?edges[i][0]+edges[i][1]:corners[i][0]+corners[i][1]+corners[i][2];if(st.p==p){for(int j=0;j<db.mod;j++){V n=db.mod==2?edges[i][j]:corners[i][j];if(st.n==n)position=i*db.mod+j;}}}check(position==projected[k],"full original sticker contradicts quotient source projection");}}}

// 0.25 P0-R2 independent C++17 full 88,179,840 corner group exact BFS.
// Based on independently derived real 54-facelet physical movement geometry.
constexpr int C_ORI=2187, C_PERM=40320, C_FULL=C_ORI*C_PERM;
array<uint8_t,8> decodePermC(int k){array<uint8_t,8>v{},pool={0,1,2,3,4,5,6,7};int n=8;for(int i=0;i<8;i++){int radix=1;for(int t=2;t<n;t++)radix*=t;int j=k/radix;k%=radix;v[i]=pool[j];for(int t=j;t<n-1;t++)pool[t]=pool[t+1];n--;}return v;}
int encodePermC(array<uint8_t,8>p){int r=0;array<bool,8>used{};for(int i=0;i<8;i++){int z=0;for(int k=0;k<p[i];k++)if(!used[k])z++;r=r*(8-i)+z;used[p[i]]=true;}return r;}
array<uint8_t,8> decodeOriC(int n){array<uint8_t,8>o{};int sum=0;for(int i=6;i>=0;i--){o[i]=n%3;sum+=o[i];n/=3;}o[7]=(3-sum%3)%3;return o;}
int encodeOriC(array<uint8_t,8>o){int v=0;for(int i=0;i<7;i++)v=v*3+o[i];return v;}
array<array<uint8_t,8>,18>movePos{},twist{};
void originalCornerTransitions(){for(int a=0;a<18;a++)for(int p=0;p<8;p++){int v=cMove[a][3*p];movePos[a][p]=v/3;twist[a][p]=v%3;for(int o=0;o<3;o++)check(cMove[a][3*p+o]==3*(v/3)+(v%3+o)%3,"corner physical orientation is not additive");}}
void physicalFullCornerIntertwining(vector<int>const&w){auto initial=physical54({}),actual=physical54(w);array<uint8_t,8> position{},orientation{};for(int i=0;i<8;i++)position[i]=i,orientation[i]=0;
 for(int a:w){for(int i=0;i<8;i++){int p=position[i];orientation[i]=(orientation[i]+twist[a][p])%3;position[i]=movePos[a][p];}}
 for(int i=0;i<8;i++){V p=corners[i][0]+corners[i][1]+corners[i][2],n=corners[i][0];int marker=-1;for(auto st:initial)if(st.p==p&&st.n==n)marker=st.id;check(marker>=0,"original corner witness marker missing");Sticker dest{};bool found=false;for(auto st:actual)if(st.id==marker){dest=st;found=true;break;}check(found,"original sticker after word marker missing");V expectedP=corners[position[i]][0]+corners[position[i]][1]+corners[position[i]][2];check(dest.p==expectedP&&dest.n==corners[position[i]][orientation[i]],"independent physical 54facelet invalidates oriented corner cube abstraction");}}
int main(){try{
 auto tic=chrono::steady_clock::now();init();originalCornerTransitions();
 for(int i=0;i<C_PERM;i++)check(encodePermC(decodePermC(i))==i,"C++ Lehmer permutation mismatch");for(int i=0;i<C_ORI;i++)check(encodeOriC(decodeOriC(i))==i,"C++ corner twist rank mismatch");
 vector<uint16_t> P(C_PERM*18),O(C_ORI*18);
 for(int i=0;i<C_PERM;i++){auto p=decodePermC(i);for(int a=0;a<18;a++){array<uint8_t,8>np{};for(int j=0;j<8;j++)np[movePos[a][j]]=p[j];P[18*i+a]=encodePermC(np);}}
 for(int i=0;i<C_ORI;i++){auto o=decodeOriC(i);for(int a=0;a<18;a++){array<uint8_t,8>no{};int sum=0;for(int j=0;j<8;j++)no[movePos[a][j]]=(o[j]+twist[a][j])%3;for(auto x:no)sum+=x;check(sum%3==0,"physical twist parity not invariant");O[18*i+a]=encodeOriC(no);}}
 string src="R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2";
 string sol="F U F D' R' F' L' F' D' L B L2 F2 U2 L2 U F' R2";
 auto ws=split(src),ww=split(sol);physicalFullCornerIntertwining(ws);auto combined=ws;combined.insert(combined.end(),ww.begin(),ww.end());physicalFullCornerIntertwining(combined);
 uint32_t seed=0x250021;for(int i=0;i<256;i++){vector<int>word;for(int j=0;j<12;j++){seed^=seed<<13;seed^=seed>>17;seed^=seed<<5;word.push_back(seed%18);}physicalFullCornerIntertwining(word);}
 auto apply=[&](vector<int>const&w){int p=0,o=0;for(int a:w){p=P[18*p+a];o=O[18*o+a];}return p*C_ORI+o;};int srcIndex=apply(ws);check(apply(combined)==0,"actual original 18 word does not solve full corner quotient");
 cout<<"P0R2_CPP_INDEPENDENT_FULL_CORNER_ORIGINAL_54_FACELET_INTERTWINEMENT PASS PUBLIC_WCA_20_AND_18_WORD_AND_256_PHYSICAL_WORDS\n";
 vector<uint8_t>dist(C_FULL,255);vector<uint32_t>queue;queue.reserve(C_FULL);queue.push_back(0);dist[0]=0;size_t head=0;vector<uint64_t>layers={1};
 while(head<queue.size()){uint32_t v=queue[head++];int d=dist[v];if(layers.size()<=size_t(d+1))layers.resize(d+2,0);auto pb=int(v)/C_ORI*18,ob=int(v)%C_ORI*18;for(int a=0;a<18;a++){uint32_t w=uint32_t(P[pb+a])*C_ORI+O[ob+a];if(dist[w]==255){dist[w]=d+1;queue.push_back(w);layers[d+1]++;}}}
 if(!layers.empty()&&layers.back()==0)layers.pop_back();const vector<uint64_t>expected={1,18,243,2874,28000,205416,1168516,5402628,20776176,45391616,15139616,64736};check(layers==expected,"full physical corner diameter11 layers differ from independent Go");check(queue.size()==C_FULL,"full corner state court incomplete");check(dist[srcIndex]==9,"original WCA source full-corner quotient distance not nine");
 cout<<"P0R2_CPP_FULL_CORNER_PDB_EXACT 1 STATES "<<queue.size()<<" DIAMETER "<<(layers.size()-1)<<" ORIGINAL_SOURCE_H 9 ALL_18_PHYSICAL_GENERATORS 1 DISTINCT_LAYER_VECTOR";for(auto n:layers)cout<<" "<<n;cout<<"\n";
 cout<<"P0R2_CPP_FINAL_REPLICATION PHYSICAL_SOURCE_CORNER_PROJECTION_9 PASS WHOLE_CUBE_PREVIOUS_LOWER_14_NOT_UPGRADED 1 RUNTIME_MS "<<chrono::duration_cast<chrono::milliseconds>(chrono::steady_clock::now()-tic).count()<<"\n";return 0;
 }catch(exception const&e){cerr<<"P0R2_CPP_FAIL "<<e.what()<<"\n";return 2;}}