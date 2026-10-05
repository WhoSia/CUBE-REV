use cuberev_core::{CornerState, STATE_DOMAIN};
use std::collections::{HashMap, HashSet};
use std::env;
use std::fs::File;
use std::io::{BufWriter, Write};

const FACE_ORDER: [u8; 6] = [b'U', b'R', b'F', b'D', b'L', b'B'];
const NONANCHOR_ACTUAL: [usize; 7] = [0,1,2,3,4,5,7];

const POS_FACES: [[u8;3];8] = [
    [b'U',b'R',b'F'], [b'U',b'F',b'L'], [b'U',b'L',b'B'], [b'U',b'B',b'R'],
    [b'D',b'F',b'R'], [b'D',b'L',b'F'], [b'D',b'B',b'L'], [b'D',b'R',b'B']
];
const CUBIE_COLORS: [[u8;3];8] = POS_FACES;

fn color_code(c:u8)->u8 {
    match c { b'U'=>0,b'R'=>1,b'F'=>2,b'D'=>3,b'L'=>4,b'B'=>5,_=>panic!("color") }
}
fn face_index(f:u8)->usize {
    FACE_ORDER.iter().position(|&x|x==f).unwrap()
}
fn face_slot(face:u8,pos:usize)->usize {
    let ps: &[usize] = match face {
        b'U'=>&[0,1,2,3], b'R'=>&[0,3,4,7], b'F'=>&[0,1,4,5],
        b'D'=>&[4,5,6,7], b'L'=>&[1,2,5,6], b'B'=>&[2,3,6,7],
        _=>panic!("face")
    };
    ps.iter().position(|&p|p==pos).unwrap()
}
fn face_codes(s:&CornerState)->[u8;24] {
    let mut out=[255u8;24];
    let mut cubie_at=[0usize;8];
    let mut ori_at=[0u8;8];
    cubie_at[6]=6; ori_at[6]=0;
    for i in 0..7 {
        let pos=NONANCHOR_ACTUAL[i];
        cubie_at[pos]=NONANCHOR_ACTUAL[s.perm[i] as usize];
        ori_at[pos]=s.ori[i];
    }
    for pos in 0..8 {
        let cubie=cubie_at[pos];
        let ori=ori_at[pos] as usize;
        for k in 0..3 {
            let face=POS_FACES[pos][k];
            let src=(k+3-ori)%3;
            let color=CUBIE_COLORS[cubie][src];
            let idx=face_index(face)*4+face_slot(face,pos);
            out[idx]=color_code(color);
        }
    }
    assert!(out.iter().all(|&x|x<6));
    out
}
fn pack_atlas(c:&[u8;24])->[u8;12] {
    let mut b=[0u8;12];
    for i in 0..12 { b[i]=(c[2*i]<<4)|c[2*i+1]; }
    b
}
fn obs_key(c:&[u8;24], faces:&[u8])->u64 {
    let mut x=0u64;
    for &f in faces {
        let fi=face_index(f);
        for j in 0..4 { x=(x<<4)|(c[fi*4+j] as u64); }
    }
    x
}
fn fnv1a64(mut h:u64, bytes:&[u8])->u64 {
    for &b in bytes { h^=b as u64; h=h.wrapping_mul(0x100000001b3); }
    h
}

fn main() {
    let out_path=env::args().nth(1).expect("usage: g7_p22_observation_atlas <atlas.bin>");
    assert_eq!(STATE_DOMAIN,3_674_160);

    let file=File::create(&out_path).expect("create atlas");
    let mut w=BufWriter::new(file);
    let mut fnv=0xcbf29ce484222325u64;
    let mut ufr:HashMap<u64,u32>=HashMap::with_capacity(3_100_000);

    for rank in 0..STATE_DOMAIN {
        let s=CornerState::unrank(rank).expect("unrank");
        assert_eq!(s.rank().unwrap(),rank);
        let c=face_codes(&s);
        let rec=pack_atlas(&c);
        w.write_all(&rec).expect("write");
        fnv=fnv1a64(fnv,&rec);
        *ufr.entry(obs_key(&c,&[b'U',b'F',b'R'])).or_insert(0)+=1;
    }
    w.flush().unwrap();

    let ufr_unique=ufr.len() as u32;
    let mut hist:HashMap<u32,u32>=HashMap::new();
    let mut max_fiber=0u32;
    for &n in ufr.values() {
        *hist.entry(n).or_insert(0)+=1;
        max_fiber=max_fiber.max(n);
    }
    drop(ufr);

    let mut ufrd:HashSet<u64>=HashSet::with_capacity(3_800_000);
    for rank in 0..STATE_DOMAIN {
        let s=CornerState::unrank(rank).unwrap();
        let c=face_codes(&s);
        ufrd.insert(obs_key(&c,&[b'U',b'F',b'R',b'D']));
    }
    let ufrd_unique=ufrd.len() as u32;

    let mut hs:Vec<(u32,u32)>=hist.into_iter().collect();
    hs.sort_unstable();
    println!("G7_P22_OBSERVATION_COMPILER_PASS");
    println!("STATE_DOMAIN\t{}",STATE_DOMAIN);
    println!("ATLAS_RECORD_BYTES\t12");
    println!("ATLAS_PAYLOAD_BYTES\t{}",STATE_DOMAIN as u64*12);
    println!("ATLAS_FNV1A64_NEW_NAMESPACE\t{:016x}",fnv);
    println!("UFR_UNIQUE\t{}",ufr_unique);
    println!("UFR_MAP_UNIFORM\t{:.12}",ufr_unique as f64/STATE_DOMAIN as f64);
    println!("UFR_MAX_FIBER\t{}",max_fiber);
    println!("UFR_FIBER_HIST\t{}",hs.iter().map(|(k,v)|format!("{}:{}",k,v)).collect::<Vec<_>>().join(","));
    println!("UFRD_UNIQUE\t{}",ufrd_unique);
    println!("UFRD_INJECTIVE\t{}",ufrd_unique==STATE_DOMAIN);
}