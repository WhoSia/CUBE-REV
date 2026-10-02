use search_geometry_core::phase1::{Cube, Phase1Moves, Phase1Pdb, MOVE_COUNT};
use std::io::{self, BufRead};

fn parse_arr<const N: usize>(s: &str) -> [u8; N] {
    let vals: Vec<u8> = s.split(',').map(|x| x.parse::<u8>().expect("u8")).collect();
    assert_eq!(vals.len(), N);
    let mut out = [0u8; N];
    out.copy_from_slice(&vals);
    out
}
fn join_u8(v:&[u8])->String{v.iter().map(|x|x.to_string()).collect::<Vec<_>>().join(",")}
fn join_usize(v:&[usize])->String{v.iter().map(|x|x.to_string()).collect::<Vec<_>>().join(",")}

fn main(){
    let moves=Phase1Moves::build();
    let pdb=Phase1Pdb::build(&moves);
    println!("source_id\tprefix_index\tphase1_lb\tis_g1\tnext_lbs\tdesc_actions\tplateau_actions\tasc_actions\tg1_next_actions");
    for line in io::stdin().lock().lines(){
        let line=line.expect("line");
        if line.trim().is_empty() || line.starts_with("source_id\t"){continue;}
        let f:Vec<&str>=line.split('\t').collect();
        assert_eq!(f.len(),8);
        let cube=Cube{
            cp:parse_arr::<8>(f[4]),co:parse_arr::<8>(f[5]),
            ep:parse_arr::<12>(f[6]),eo:parse_arr::<12>(f[7])
        };
        assert!(cube.validate());
        let q=cube.phase1();
        let lb=pdb.lower_bound(q);
        let mut nlb=Vec::with_capacity(MOVE_COUNT);
        let mut desc=Vec::new(); let mut eq=Vec::new(); let mut asc=Vec::new(); let mut g1=Vec::new();
        for a in 0..MOVE_COUNT{
            let nq=moves.next(q,a);
            let d=pdb.lower_bound(nq);
            nlb.push(d);
            if d<lb{desc.push(a);}else if d==lb{eq.push(a);}else{asc.push(a);}
            if nq.is_g1(){g1.push(a);}
        }
        println!("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
            f[0],f[1],lb,if q.is_g1(){1}else{0},join_u8(&nlb),
            join_usize(&desc),join_usize(&eq),join_usize(&asc),join_usize(&g1));
    }
}