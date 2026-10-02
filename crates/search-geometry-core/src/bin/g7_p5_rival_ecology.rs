use search_geometry_core::g6::{Cube, HTM, Phase1, Phase1Moves, Phase1Pdb};
use std::collections::{BTreeMap,BTreeSet};

fn min_lb(m:&Phase1Moves,p:&Phase1Pdb,q:Phase1,depth:u8,mode:u8)->u8{
    if depth==0 {
        let ts=p.twist_slice[q.twist as usize*495+q.slice as usize];
        let fs=p.flip_slice[q.flip as usize*495+q.slice as usize];
        return match mode {0=>ts.max(fs),1=>ts,2=>fs,_=>unreachable!()};
    }
    let mut best=u8::MAX;
    for a in 0..18 { best=best.min(min_lb(m,p,m.next(q,a),depth-1,mode)); }
    best
}
fn best(m:&Phase1Moves,p:&Phase1Pdb,q:Phase1,h:u8,mode:u8)->BTreeSet<usize>{
    let mut scores=[0u8;18];
    for a in 0..18 { scores[a]=min_lb(m,p,m.next(q,a),h-1,mode); }
    let b=*scores.iter().min().unwrap();
    scores.iter().enumerate().filter_map(|(i,&x)|if x==b{Some(i)}else{None}).collect()
}
fn lcg(x:&mut u64)->u64{*x=x.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);*x}
fn same(a:&BTreeSet<usize>,b:&BTreeSet<usize>)->bool{a==b}
fn jacc(a:&BTreeSet<usize>,b:&BTreeSet<usize>)->f64{
    let i=a.intersection(b).count() as f64; let u=a.union(b).count() as f64; if u==0.0{1.0}else{i/u}
}
fn main(){
    let moves=Phase1Moves::build(); let pdb=Phase1Pdb::build(&moves);
    let mut seed=0xC0BE_5A17_55AA_2026u64;
    let mut n=0usize; let mut h13=0usize; let mut h12=0usize; let mut h23=0usize;
    let mut h2_unique=0usize; let mut ts_fs=0usize; let mut component_unique=0usize;
    let mut jac13=0.0; let mut jac12=0.0; let mut jac23=0.0;
    let mut by_lb:BTreeMap<u8,[usize;4]>=BTreeMap::new(); // n,h13,h2unique,componentunique
    for _ in 0..20000 {
        let len=12+(lcg(&mut seed)%15) as usize;
        let mut c=Cube::SOLVED; let mut pf=99usize;
        for _ in 0..len {
            let mut a=(lcg(&mut seed)%18) as usize;
            if a/3==pf {a=(a+3+(lcg(&mut seed)%12) as usize)%18;}
            pf=a/3;c=c.apply(HTM[a]);
        }
        let q=c.phase1(); if q.is_g1(){continue;}
        let lb=pdb.lower_bound(q); if !(3..=8).contains(&lb){continue;}
        let h1=best(&moves,&pdb,q,1,0);
        let h2=best(&moves,&pdb,q,2,0);
        let h3=best(&moves,&pdb,q,3,0);
        let ts=best(&moves,&pdb,q,1,1);
        let fs=best(&moves,&pdb,q,1,2);
        n+=1;
        let d13=!same(&h1,&h3); let d12=!same(&h1,&h2); let d23=!same(&h2,&h3);
        h13+=d13 as usize;h12+=d12 as usize;h23+=d23 as usize;
        let hu=!same(&h2,&h1)&&!same(&h2,&h3);h2_unique+=hu as usize;
        let cf=!same(&ts,&fs);ts_fs+=cf as usize;
        let cu=cf && !same(&ts,&h1)&&!same(&ts,&h2)&&!same(&ts,&h3)
                   && !same(&fs,&h1)&&!same(&fs,&h2)&&!same(&fs,&h3);
        component_unique+=cu as usize;
        jac13+=jacc(&h1,&h3);jac12+=jacc(&h1,&h2);jac23+=jacc(&h2,&h3);
        let e=by_lb.entry(lb).or_insert([0;4]);e[0]+=1;e[1]+=d13 as usize;e[2]+=hu as usize;e[3]+=cu as usize;
        if n>=6000 {break;}
    }
    assert!(n>=3000);
    println!("G7_P5_RIVAL_ECOLOGY_PASS");
    println!("STATES\t{}",n);
    println!("H1_H3_DISAGREE_RATE\t{:.8}",h13 as f64/n as f64);
    println!("H1_H2_DISAGREE_RATE\t{:.8}",h12 as f64/n as f64);
    println!("H2_H3_DISAGREE_RATE\t{:.8}",h23 as f64/n as f64);
    println!("H2_UNIQUE_RATE\t{:.8}",h2_unique as f64/n as f64);
    println!("TS_FS_DISAGREE_RATE\t{:.8}",ts_fs as f64/n as f64);
    println!("COMPONENT_UNIQUE_RATE\t{:.8}",component_unique as f64/n as f64);
    println!("JACCARD_H1_H3\t{:.8}",jac13/n as f64);
    println!("JACCARD_H1_H2\t{:.8}",jac12/n as f64);
    println!("JACCARD_H2_H3\t{:.8}",jac23/n as f64);
    for (lb,x) in by_lb {
        println!("LB\t{}\t{}\t{:.8}\t{:.8}\t{:.8}",lb,x[0],x[1] as f64/x[0] as f64,x[2] as f64/x[0] as f64,x[3] as f64/x[0] as f64);
    }
}
