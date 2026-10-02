use search_geometry_core::g6::{Cube, HTM, Phase1, Phase1Moves, Phase1Pdb};
use std::collections::{BTreeMap,BTreeSet};

fn lcg(x:&mut u64)->u64{*x=x.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);*x}
fn min_score(m:&Phase1Moves,p:&Phase1Pdb,q:Phase1,d:u8,mode:u8)->u8{
    if d==0 {
        let ts=p.twist_slice[q.twist as usize*495+q.slice as usize];
        let fs=p.flip_slice[q.flip as usize*495+q.slice as usize];
        return match mode {0=>ts.max(fs),1=>ts,2=>fs,_=>unreachable!()};
    }
    let mut b=u8::MAX;
    for a in 0..18 { b=b.min(min_score(m,p,m.next(q,a),d-1,mode)); }
    b
}
fn best(m:&Phase1Moves,p:&Phase1Pdb,q:Phase1,h:u8,mode:u8)->BTreeSet<usize>{
    let mut s=[0u8;18];
    for a in 0..18 {s[a]=min_score(m,p,m.next(q,a),h-1,mode);}
    let b=*s.iter().min().unwrap();
    s.iter().enumerate().filter_map(|(i,&x)|if x==b{Some(i)}else{None}).collect()
}
fn settxt(x:&BTreeSet<usize>)->String{x.iter().map(|v|v.to_string()).collect::<Vec<_>>().join(",")}
fn arr<T:std::fmt::Display,const N:usize>(x:&[T;N])->String{x.iter().map(|v|v.to_string()).collect::<Vec<_>>().join(",")}
fn signature(c:&Cube)->String{format!("{}|{}|{}|{}",arr(&c.cp),arr(&c.co),arr(&c.ep),arr(&c.eo))}
fn motif(h1:&BTreeSet<usize>,h2:&BTreeSet<usize>,h3:&BTreeSet<usize>,ts:&BTreeSet<usize>,fs:&BTreeSet<usize>)->Vec<&'static str>{
    let mut v=Vec::new();
    if h2!=h1 && h2!=h3 {v.push("H2_UNIQUE");}
    if h1!=h2 && h1!=h3 && h2!=h3 {v.push("ALL_HORIZON_DISAGREE");}
    let tsu=ts!=h1&&ts!=h2&&ts!=h3&&ts!=fs;
    let fsu=fs!=h1&&fs!=h2&&fs!=h3&&fs!=ts;
    if tsu||fsu {v.push("COMPONENT_UNIQUE");}
    if ts!=fs && (ts!=h2 || fs!=h2) {v.push("COMPONENT_VS_MAX_CONFLICT");}
    v
}
fn main(){
    let moves=Phase1Moves::build();let pdb=Phase1Pdb::build(&moves);
    let seeds:[u64;8]=[
      0xA601_0001,0xA601_0002,0xA601_0003,0xA601_0004,
      0xA601_0005,0xA601_0006,0xA601_0007,0xA601_0008
    ];
    let motifs=["H2_UNIQUE","ALL_HORIZON_DISAGREE","COMPONENT_UNIQUE","COMPONENT_VS_MAX_CONFLICT"];
    println!("seed_id\tmotif\tstate_id\tphase1_lb\th1_best\th2_best\th3_best\tts_best\tfs_best\tcp\tco\tep\teo");
    let mut global=BTreeSet::new();
    for (si,seed0) in seeds.iter().enumerate(){
        let mut seed=*seed0;
        let mut buckets:BTreeMap<&str,Vec<(Cube,u32)>>=motifs.iter().map(|&x|(x,Vec::new())).collect();
        let mut local=BTreeSet::new();
        for serial in 0..250000u32 {
            if motifs.iter().all(|m|buckets[m].len()>=8){break;}
            let len=12+(lcg(&mut seed)%17) as usize;
            let mut c=Cube::SOLVED;let mut pf=99usize;
            for _ in 0..len{
                let mut a=(lcg(&mut seed)%18) as usize;
                if a/3==pf{a=(a+3+(lcg(&mut seed)%12) as usize)%18;}
                pf=a/3;c=c.apply(HTM[a]);
            }
            let sig=signature(&c);
            if global.contains(&sig)||!local.insert(sig.clone()){continue;}
            let q=c.phase1(); if q.is_g1(){continue;}
            let lb=pdb.lower_bound(q); if !(4..=8).contains(&lb){continue;}
            let h1=best(&moves,&pdb,q,1,0);let h2=best(&moves,&pdb,q,2,0);let h3=best(&moves,&pdb,q,3,0);
            let ts=best(&moves,&pdb,q,1,1);let fs=best(&moves,&pdb,q,1,2);
            for m in motif(&h1,&h2,&h3,&ts,&fs){
                if buckets[m].len()<8 {buckets.get_mut(m).unwrap().push((c,serial));}
            }
        }
        for m in motifs{
            let xs=&buckets[m];
            assert_eq!(xs.len(),8,"insufficient motif {} seed {}",m,si+1);
            for (j,(c,serial)) in xs.iter().enumerate(){
                let q=c.phase1();let lb=pdb.lower_bound(q);
                let h1=best(&moves,&pdb,q,1,0);let h2=best(&moves,&pdb,q,2,0);let h3=best(&moves,&pdb,q,3,0);
                let ts=best(&moves,&pdb,q,1,1);let fs=best(&moves,&pdb,q,1,2);
                global.insert(signature(c));
                println!("S{:02}\t{}\tS{:02}-{}-{:02}-{:06}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
                    si+1,m,si+1,m,j+1,serial,lb,settxt(&h1),settxt(&h2),settxt(&h3),settxt(&ts),settxt(&fs),
                    arr(&c.cp),arr(&c.co),arr(&c.ep),arr(&c.eo));
            }
        }
    }
}
