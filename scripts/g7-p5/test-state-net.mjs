import {faceMatrices} from "../../g7/p5/web/state-net.mjs";
const solved=faceMatrices("");
for(const f of ["U","R","F","D","L","B"]) if(new Set(solved[f].flat()).size!==1||solved[f][1][1]!==f) throw new Error("SOLVED:"+f);
const mixed=faceMatrices("R U2 F'");
for(const f of ["U","R","F","D","L","B"]) if(mixed[f].flat().length!==9||mixed[f][1][1]!==f) throw new Error("CENTER:"+f);
console.log("G7_P5_STATE_NET_TEST_PASS");
