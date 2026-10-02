use search_geometry_core::g6::{Phase1, Phase1Moves, Phase1Pdb};
use std::io::{self, Read};

const FLIP_COUNT: u32 = 2_048;
const SLICE_COUNT: u32 = 495;

fn decode(rank: u32) -> Phase1 {
    let slice = (rank % SLICE_COUNT) as u16;
    let t = rank / SLICE_COUNT;
    let flip = (t % FLIP_COUNT) as u16;
    let twist = (t / FLIP_COUNT) as u16;
    Phase1 { twist, flip, slice }
}

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).expect("stdin");
    let moves = Phase1Moves::build();
    let pdb = Phase1Pdb::build(&moves);

    println!("source_id\tmove_index\trank_before\trank_after\taction_index\tmethod_family\treconstructor\th_before\th_after\tbest_h\tbest_count\tlocal_regret\tdescent");
    for (li,line) in input.lines().enumerate() {
        if li==0 && line.starts_with("source_id\t") { continue; }
        if line.trim().is_empty() { continue; }
        let parts: Vec<&str> = line.splitn(7, '\t').collect();
        assert_eq!(parts.len(),7,"TSV_FIELDS");
        let rank_before: u32 = parts[2].parse().expect("rank_before");
        let rank_after: u32 = parts[3].parse().expect("rank_after");
        let action: usize = parts[4].parse().expect("action");
        assert!(action < 18,"ACTION_RANGE");
        let q0=decode(rank_before);
        let q1=decode(rank_after);
        assert_eq!(q0.rank(),rank_before,"RANK0_DECODE");
        assert_eq!(q1.rank(),rank_after,"RANK1_DECODE");
        let predicted=moves.next(q0,action);
        assert_eq!(predicted.rank(),rank_after,"PHASE1_TRANSITION_MISMATCH");

        let h_before=pdb.lower_bound(q0);
        let h_after=pdb.lower_bound(q1);
        let mut best_h=u8::MAX;
        let mut best_count=0usize;
        for a in 0..18 {
            let h=pdb.lower_bound(moves.next(q0,a));
            if h<best_h { best_h=h; best_count=1; }
            else if h==best_h { best_count+=1; }
        }
        let regret=h_after as i16-best_h as i16;
        println!(
            "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
            parts[0],parts[1],rank_before,rank_after,action,parts[5],parts[6],
            h_before,h_after,best_h,best_count,regret,if h_after<h_before {1}else{0}
        );
    }
}
