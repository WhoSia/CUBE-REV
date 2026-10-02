import {spawnSync} from "node:child_process";
const p=spawnSync("cargo",["run","-q","-p","search-geometry-core","--bin","g7_p5_rival_ecology"],{encoding:"utf8"});
if(p.status!==0) throw new Error(p.stderr||p.stdout);
const m=Object.fromEntries(p.stdout.trim().split(/\r?\n/).filter(x=>x.includes("\t")&&!x.startsWith("LB\t")).map(x=>{const [k,v]=x.split("\t");return [k,Number(v)];}));
if(m.STATES<3000) throw new Error("SUPPORT");
if(!(m.H1_H3_DISAGREE_RATE>0&&m.H1_H3_DISAGREE_RATE<1)) throw new Error("H13");
if(!(m.TS_FS_DISAGREE_RATE>0)) throw new Error("COMPONENTS");
console.log("G7_P5_RIVAL_ECOLOGY_TEST_PASS");
