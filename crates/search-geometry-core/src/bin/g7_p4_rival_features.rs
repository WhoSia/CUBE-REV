use search_geometry_core::g6::{Cube, HTM, Phase1, Phase1Moves, Phase1Pdb};
use std::io::{self, BufRead};

fn parse_arr<const N: usize>(s: &str) -> [u8; N] {
    let vals: Vec<u8> = s.split(',').map(|x| x.parse::<u8>().expect("u8")).collect();
    assert_eq!(vals.len(), N);
    let mut out = [0u8; N];
    out.copy_from_slice(&vals);
    out
}
fn lb(pdb: &Phase1Pdb, q: Phase1) -> u8 {
    pdb.lower_bound(q)
}
fn component(pdb: &Phase1Pdb, q: Phase1) -> (u8,u8) {
    let ts = pdb.twist_slice[q.twist as usize * 495 + q.slice as usize];
    let fs = pdb.flip_slice[q.flip as usize * 495 + q.slice as usize];
    (ts,fs)
}
fn min_lb_depth(moves: &Phase1Moves, pdb: &Phase1Pdb, q: Phase1, depth: u8) -> u8 {
    if depth == 0 { return lb(pdb,q); }
    let mut best=u8::MAX;
    for a in 0..18 {
        best=best.min(min_lb_depth(moves,pdb,moves.next(q,a),depth-1));
    }
    best
}
fn first_action_scores(moves: &Phase1Moves, pdb: &Phase1Pdb, q: Phase1, horizon: u8) -> [u8;18] {
    assert!(horizon>=1);
    let mut out=[0u8;18];
    for a in 0..18 {
        let q1=moves.next(q,a);
        out[a]=min_lb_depth(moves,pdb,q1,horizon-1);
    }
    out
}

fn main() {
    let moves=Phase1Moves::build();
    let pdb=Phase1Pdb::build(&moves);
    println!("source_id\tprefix_index\tq_rank\tlb\tts_lb\tfs_lb\tis_g1\tboundary_after\tobs_next_action\th1_regret\th2_regret\th3_regret\thorizon_optimal_count\th1_opt_count\th2_opt_count\th3_opt_count");
    for line in io::stdin().lock().lines() {
        let line=line.expect("line");
        if line.trim().is_empty(){continue;}
        let f:Vec<&str>=line.split('\t').collect();
        assert_eq!(f.len(),8);
        let source=f[0];
        let prefix=f[1];
        let obs:i32=f[2].parse().expect("obs");
        let boundary=f[3];
        let cube=Cube{
            cp:parse_arr::<8>(f[4]),
            co:parse_arr::<8>(f[5]),
            ep:parse_arr::<12>(f[6]),
            eo:parse_arr::<12>(f[7]),
        };
        assert!(cube.validate(),"invalid cube");
        let q=cube.phase1();
        let l=lb(&pdb,q);
        let (ts,fs)=component(&pdb,q);
        let mut regrets=[-1i16;3];
        let mut opt_counts=[0usize;3];
        let mut stable=0usize;
        for h in 1..=3u8 {
            let scores=first_action_scores(&moves,&pdb,q,h);
            let best=*scores.iter().min().unwrap();
            opt_counts[(h-1) as usize]=scores.iter().filter(|&&x|x==best).count();
            if obs>=0 {
                let o=scores[obs as usize];
                regrets[(h-1) as usize]=(o as i16)-(best as i16);
                if o==best {stable+=1;}
            }
        }
        println!(
            "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
            source,prefix,q.rank(),l,ts,fs,if q.is_g1(){1}else{0},boundary,obs,
            regrets[0],regrets[1],regrets[2],stable,opt_counts[0],opt_counts[1],opt_counts[2]
        );
    }
}
