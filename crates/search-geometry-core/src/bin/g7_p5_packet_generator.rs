use search_geometry_core::g6::{Cube, HTM, Phase1, Phase1Moves, Phase1Pdb};
use std::collections::{BTreeMap, BTreeSet};

fn min_lb_depth(moves:&Phase1Moves,pdb:&Phase1Pdb,q:Phase1,depth:u8)->u8{
    if depth==0 { return pdb.lower_bound(q); }
    let mut best=u8::MAX;
    for a in 0..18 { best=best.min(min_lb_depth(moves,pdb,moves.next(q,a),depth-1)); }
    best
}
fn scores(moves:&Phase1Moves,pdb:&Phase1Pdb,q:Phase1,h:u8)->[u8;18]{
    let mut out=[0u8;18];
    for a in 0..18 { out[a]=min_lb_depth(moves,pdb,moves.next(q,a),h-1); }
    out
}
fn best_set(s:&[u8;18])->BTreeSet<usize>{
    let b=*s.iter().min().unwrap();
    s.iter().enumerate().filter_map(|(i,&x)|if x==b{Some(i)}else{None}).collect()
}
fn set_text(s:&BTreeSet<usize>)->String{
    s.iter().map(|x|x.to_string()).collect::<Vec<_>>().join(",")
}
fn arr<T:std::fmt::Display,const N:usize>(x:&[T;N])->String{
    x.iter().map(|v|v.to_string()).collect::<Vec<_>>().join(",")
}
fn move_name(i:usize)->String{
    let faces=["U","R","F","D","L","B"];
    let f=faces[i/3];
    let p=["","2","'"][i%3];
    format!("{f}{p}")
}
fn alg_text(seq:&[usize])->String{
    seq.iter().map(|&i|move_name(i)).collect::<Vec<_>>().join(" ")
}
fn lcg(x:&mut u64)->u64{
    *x=x.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
    *x
}
#[derive(Clone)]
struct Candidate{
    state_id:String,
    cube:Cube,
    lb:u8,
    h1:BTreeSet<usize>,
    h3:BTreeSet<usize>,
    scramble:Vec<usize>,
    disagreement:u8,
    h1_ties:usize,
    h3_ties:usize,
}
fn main(){
    let moves=Phase1Moves::build();
    let pdb=Phase1Pdb::build(&moves);
    let mut seed=std::env::var("G7_P5_PACKET_SEED_HEX")
        .ok()
        .and_then(|s|u64::from_str_radix(s.trim_start_matches("0x"),16).ok())
        .unwrap_or(0xC0BE_5A17_2026_1002u64);
    let mut by_lb:BTreeMap<u8,Vec<Candidate>>=BTreeMap::new();
    let mut seen=BTreeSet::new();

    for serial in 0..12000usize {
        let len=12+(lcg(&mut seed)%14) as usize;
        let mut cube=Cube::SOLVED;
        let mut seq=Vec::with_capacity(len);
        let mut prev_face=99usize;
        for _ in 0..len {
            let mut a=(lcg(&mut seed)%18) as usize;
            if a/3==prev_face { a=(a+3+(lcg(&mut seed)%12) as usize)%18; }
            prev_face=a/3;
            cube=cube.apply(HTM[a]);
            seq.push(a);
        }
        let q=cube.phase1();
        let rank=q.rank();
        if q.is_g1() || !seen.insert(rank) { continue; }
        let s1=scores(&moves,&pdb,q,1);
        let s3=scores(&moves,&pdb,q,3);
        let b1=best_set(&s1);
        let b3=best_set(&s3);
        if b1==b3 { continue; }
        let symdiff=b1.symmetric_difference(&b3).count() as u8;
        if symdiff<2 { continue; }
        let lb=pdb.lower_bound(q);
        if !(3..=8).contains(&lb) { continue; }
        by_lb.entry(lb).or_default().push(Candidate{
            state_id:format!("S{:05}",serial),
            cube,lb,h1:b1.clone(),h3:b3.clone(),scramble:seq,
            disagreement:symdiff,h1_ties:b1.len(),h3_ties:b3.len()
        });
    }

    let mut chosen=Vec::new();
    for (lb,mut xs) in by_lb {
        xs.sort_by_key(|x|(std::cmp::Reverse(x.disagreement),x.h1_ties+x.h3_ties,x.state_id.clone()));
        while xs.len()>=2 && chosen.len()<24 {
            let a=xs.remove(0);
            let b=xs.remove(0);
            chosen.push((lb,a,b));
        }
        if chosen.len()>=24 { break; }
    }
    assert!(chosen.len()>=12,"insufficient matched rival-disagreement pairs");

    println!("pair_id\ttrial_side\tstate_id\tphase1_lb\th1_best\th3_best\tdisagreement\th1_ties\th3_ties\tscramble\tcp\tco\tep\teo");
    for (pi,(lb,a,b)) in chosen.into_iter().take(12).enumerate(){
        for (side,c) in [("A",a),("B",b)] {
            println!(
                "P{:02}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
                pi+1,side,c.state_id,lb,set_text(&c.h1),set_text(&c.h3),c.disagreement,
                c.h1_ties,c.h3_ties,alg_text(&c.scramble),
                arr(&c.cube.cp),arr(&c.cube.co),arr(&c.cube.ep),arr(&c.cube.eo)
            );
        }
    }
}
