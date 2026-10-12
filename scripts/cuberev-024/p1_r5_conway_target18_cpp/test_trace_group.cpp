// Independent exact group trace rewrites physically checked under the REAL
// original C++17 54-facelet turns and all-cubie group composition.
#define main inherited_p1r3_group_test_main
#include "../p1_r3_true_54_facelet_multiaxis_dr_cpp/main.cpp"
#undef main
#include "group_trace_rewrite.hpp"
int main(){
 initTurns();
 // Two disjoint-face commuting pairs: R L R2 L2 = R' L'.
 const auto source=parse("R L R2 L2"),expected=parse("R' L'");
 const auto res=traceRewrite(source,2,2000);
 if(!res.success||res.word.size()!=2||!res.exhausted)throw runtime_error("two face-pair contraction unavailable");
 Cube l=cubeAfter(source),r=cubeAfter(expected),z=cubeAfter(res.word);
 if(l.cp!=r.cp||l.co!=r.co||l.ep!=r.ep||l.eo!=r.eo)throw runtime_error("R,L physical cubie identity invalid");
 if(l.cp!=z.cp||l.co!=z.co||l.ep!=z.ep||l.eo!=z.eo)throw runtime_error("trace closure equivalent cubies invalid");
 // The physically completed WCA witness is 19, while its raw DR program is 20.
 const auto scr=parse("R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2");
 const auto raw=parse("F2 R B U2 B' L F' U2 F U' L2 B B2 R' D2 L R' U2 L2 U2");
 const auto norm=parse("F2 R B U2 B' L F' U2 F U' L2 B' R' D2 L R' U2 L2 U2");
 auto rw=traceRewrite(raw,19,5000);
 if(!rw.success||rw.word.size()!=19||!physicalSolves(scr,rw.word)||!physicalSolves(scr,norm))
    throw runtime_error("official whole-cube boundary19 positive trace control failed");
 cout<<"P1R5_TRUE_WHOLE_CUBE_GROUP_TRACE_REWRITE_PASS TWO_DISJOINT_MERGES_4_TO_2 AND_OFFICIAL_WCA_20_TO_19\n";
}