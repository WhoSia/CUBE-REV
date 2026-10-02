use search_geometry_core::phase1::{Cube, Phase1, Phase1Moves, Phase1Pdb};
use std::collections::BTreeSet;
use std::io::{self, BufRead};

fn parse_arr<const N: usize>(s: &str) -> [u8; N] {
    let vals: Vec<u8> = s.split(',').map(|x| x.parse::<u8>().expect("u8")).collect();
    assert_eq!(vals.len(), N);
    let mut out = [0u8; N];
    out.copy_from_slice(&vals);
    out
}
fn score(pdb:&Phase1Pdb,q:Phase1,mode:u8)->u8{
    let ts=pdb.twist_slice[q.twist as usize*495+q.slice as usize];
    let fs=pdb.flip_slice[q.flip as usize*495+q.slice as usize];
    match mode {0=>ts.max(fs),1=>ts,2=>fs,_=>unreachable!()}
}
fn min_depth(m:&Phase1Moves,p:&Phase1Pdb,q:Phase1,depth:u8,mode:u8)->u8{
    if depth==0{return score(p,q,mode);}
    let mut best=u8::MAX;
    for a in 0..18 {best=best.min(min_depth(m,p,m.next(q,a),depth-1,mode));}
    best
}
fn best(m:&Phase1Moves,p:&Phase1Pdb,q:Phase1,h:u8,mode:u8)->BTreeSet<usize>{
    let mut s=[0u8;18];
    for a in 0..18{s[a]=min_depth(m,p,m.next(q,a),h-1,mode);}
    let b=*s.iter().min().unwrap();
    s.iter().enumerate().filter_map(|(i,&x)|if x==b{Some(i)}else{None}).collect()
}
fn txt(s:&BTreeSet<usize>)->String{s.iter().map(|x|x.to_string()).collect::<Vec<_>>().join(",")}
fn jacc(a:&BTreeSet<usize>,b:&BTreeSet<usize>)->f64{
    let i=a.intersection(b).count() as f64;
    let u=a.union(b).count() as f64;
    if u==0.0{1.0}else{i/u}
}
fn main(){
    let moves=Phase1Moves::build();
    let pdb=Phase1Pdb::build(&moves);
    println!("source_id\tprefix_index\tphase1_lb\tts_lb\tfs_lb\tis_g1\tboundary_after\tnext_action\th1_best\th2_best\th3_best\tts_best\tfs_best\trival_unique_sets\tmean_pairwise_jaccard_distance\tobserved_match_h1\tobserved_match_h2\tobserved_match_h3\tobserved_match_ts\tobserved_match_fs");
    for line in io::stdin().lock().lines(){
        let line=line.expect("line");
        if line.trim().is_empty() || line.starts_with("source_id\t"){continue;}
        let f:Vec<&str>=line.split('\t').collect();
        assert_eq!(f.len(),8);
        let source=f[0]; let prefix=f[1]; let boundary=f[2];
        let next:i32=f[3].parse().expect("next");
        let cube=Cube{
            cp:parse_arr::<8>(f[4]),co:parse_arr::<8>(f[5]),
            ep:parse_arr::<12>(f[6]),eo:parse_arr::<12>(f[7])
        };
        assert!(cube.validate());
        let q=cube.phase1();
        let ts=pdb.twist_slice[q.twist as usize*495+q.slice as usize];
        let fs=pdb.flip_slice[q.flip as usize*495+q.slice as usize];
        let h1=best(&moves,&pdb,q,1,0);
        let h2=best(&moves,&pdb,q,2,0);
        let h3=best(&moves,&pdb,q,3,0);
        let t=best(&moves,&pdb,q,1,1);
        let fl=best(&moves,&pdb,q,1,2);
        let sets=[&h1,&h2,&h3,&t,&fl];
        let unique=sets.iter().map(|s|txt(s)).collect::<BTreeSet<_>>().len();
        let mut jd=0.0; let mut pairs=0.0;
        for i in 0..sets.len(){for j in i+1..sets.len(){jd+=1.0-jacc(sets[i],sets[j]);pairs+=1.0;}}
        let obs=|s:&BTreeSet<usize>| if next<0{-1}else if s.contains(&(next as usize)){1}else{0};
        println!("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{:.8}\t{}\t{}\t{}\t{}\t{}",
            source,prefix,pdb.lower_bound(q),ts,fs,if q.is_g1(){1}else{0},boundary,next,
            txt(&h1),txt(&h2),txt(&h3),txt(&t),txt(&fl),unique,jd/pairs,
            obs(&h1),obs(&h2),obs(&h3),obs(&t),obs(&fl));
    }
}
