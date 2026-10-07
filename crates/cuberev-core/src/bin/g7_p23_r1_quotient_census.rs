use cuberev_core::{CornerState, STATE_DOMAIN};
use std::{collections::{HashMap, HashSet}, env, fs::File, io::{BufWriter, Write}};

const N_SOURCE: usize = 88_179_840;
const NONANCHOR: [usize; 7] = [0, 1, 2, 3, 4, 5, 7];
const POS_FACES: [[u8; 3]; 8] = [
    [b'U', b'R', b'F'], [b'U', b'F', b'L'], [b'U', b'L', b'B'], [b'U', b'B', b'R'],
    [b'D', b'F', b'R'], [b'D', b'L', b'F'], [b'D', b'B', b'L'], [b'D', b'R', b'B'],
];
const FACE_ORDER: [u8; 6] = [b'U', b'R', b'F', b'D', b'L', b'B'];
const CUBIE_COLORS: [[u8; 3]; 8] = POS_FACES;

#[derive(Clone, Copy, Debug)]
struct State { cp: [u8; 8], co: [u8; 8] }
#[derive(Clone, Copy, Debug)]
struct Rot { m: [[i8; 3]; 3] }

fn face_vec(f: u8) -> [i8; 3] { match f {
    b'U' => [0,1,0], b'R' => [1,0,0], b'F' => [0,0,1],
    b'D' => [0,-1,0], b'L' => [-1,0,0], b'B' => [0,0,-1], _ => panic!("face")
}}
fn pos_vec(p: usize) -> [i8; 3] {
    let a=face_vec(POS_FACES[p][0]); let b=face_vec(POS_FACES[p][1]); let c=face_vec(POS_FACES[p][2]);
    [a[0]+b[0]+c[0],a[1]+b[1]+c[1],a[2]+b[2]+c[2]]
}
fn apply_vec(r: Rot, v: [i8;3]) -> [i8;3] {
    let mut o=[0;3]; for i in 0..3 { for j in 0..3 { o[i]+=r.m[i][j]*v[j]; }} o
}
fn rotations() -> Vec<Rot> {
    let perms=[[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]];
    let mut out=Vec::new();
    for p in perms { for sx in [-1i8,1] { for sy in [-1i8,1] { for sz in [-1i8,1] {
        let signs=[sx,sy,sz];
        let inv=(p[0]>p[1]) as i8+(p[0]>p[2]) as i8+(p[1]>p[2]) as i8;
        if (if inv%2==0 {1} else {-1})*sx*sy*sz == 1 {
            let mut m=[[0i8;3];3]; for row in 0..3 { m[row][p[row]]=signs[row]; }
            out.push(Rot{m});
        }
    }}}}
    out.sort_by_key(|r| (r.m[0][0],r.m[0][1],r.m[0][2],r.m[1][0],r.m[1][1],r.m[1][2],r.m[2][0],r.m[2][1],r.m[2][2]));
    assert_eq!(out.len(),24); out
}
fn face_for_vec(v:[i8;3])->u8 {
    for f in FACE_ORDER { if face_vec(f)==v { return f; } }
    panic!("not a face normal: {v:?}")
}
fn position_for_vec(v:[i8;3])->usize {
    (0..8).find(|&p|pos_vec(p)==v).expect("rotated corner position")
}
fn twist_for_piece_at(r:Rot, p:usize, c:usize, o:u8)->(usize,u8) {
    let q=position_for_vec(apply_vec(r,pos_vec(p)));
    let mut colors_at=[255u8;3]; let mut normals_at=[ [0i8;3];3];
    for k in 0..3 {
        let nf=face_for_vec(apply_vec(r,face_vec(POS_FACES[p][k])));
        let l=POS_FACES[q].iter().position(|&f|f==nf).expect("rotated sticker slot");
        assert_eq!(colors_at[l],255);
        colors_at[l]=CUBIE_COLORS[c][(k+3-o as usize)%3];
        normals_at[l]=face_vec(nf);
    }
    let mut found=None;
    for cand in 0..3u8 {
        let mut ok=true;
        for l in 0..3 {
            let nf=face_for_vec(normals_at[l]);
            ok &= POS_FACES[q][l]==nf &&
                  CUBIE_COLORS[c][(l+3-cand as usize)%3]==colors_at[l];
        }
        if ok { assert!(found.is_none(),"nonunique twist"); found=Some(cand); }
    }
    (q,found.expect("no twist matches rotated stickers"))
}
fn rotate(s:State,r:Rot)->State {
    let mut out=State{cp:[255;8],co:[255;8]};
    for p in 0..8 {
        let c=s.cp[p] as usize; let o=s.co[p];
        let (q,no)=twist_for_piece_at(r,p,c,o);
        assert_eq!(out.cp[q],255,"position collision");
        out.cp[q]=c as u8; out.co[q]=no;
    }
    assert!(out.cp.iter().all(|&x|x<8));
    assert_eq!(out.co.iter().map(|&x|x as usize).sum::<usize>()%3,0);
    out
}
fn anchor_rotation(s:State,rs:&[Rot])->usize {
    let p=s.cp.iter().position(|&c|c==6).unwrap(); let o=s.co[p];
    let mut found=None;
    for (i,&r) in rs.iter().enumerate() {
        if twist_for_piece_at(r,p,6,o)==(6,0) {
            assert!(found.is_none(),"nonunique DBL anchor rotation"); found=Some(i);
        }
    }
    found.expect("no DBL anchor rotation")
}
fn corner_state(s:State)->CornerState {
    assert_eq!(s.cp[6],6); assert_eq!(s.co[6],0);
    let mut perm=[0u8;7]; let mut ori=[0u8;7];
    for i in 0..7 { perm[i]=NONANCHOR.iter().position(|&p|p==s.cp[NONANCHOR[i]]).expect("anchored cubie") as u8; ori[i]=s.co[NONANCHOR[i]]; }
    CornerState{perm,ori}
}
fn full_from_target(rank:u32)->State {
    let t=CornerState::unrank(rank).expect("target unrank");
    let mut s=State{cp:[255;8],co:[0;8]}; s.cp[6]=6;
    for i in 0..7 { s.cp[NONANCHOR[i]]=NONANCHOR[t.perm[i] as usize] as u8; s.co[NONANCHOR[i]]=t.ori[i]; }
    s
}
fn factorial(n:usize)->u64 { (1..=n as u64).product::<u64>().max(1) }
fn raw_rank(s:State)->usize {
    let mut lehmer=0u64;
    for i in 0..8 {
        let lower=s.cp[i+1..].iter().filter(|&&x|x<s.cp[i]).count() as u64;
        lehmer += lower*factorial(7-i);
    }
    let mut ori=0u64; for &x in &s.co[..7] { ori=ori*3+x as u64; }
    (lehmer*2187+ori) as usize
}
fn face_index(f:u8)->usize { FACE_ORDER.iter().position(|&x|x==f).unwrap() }
fn face_slot(face:u8,pos:usize)->usize {
    let ps:&[usize]=match face { b'U'=>&[0,1,2,3],b'R'=>&[0,3,4,7],b'F'=>&[0,1,4,5],
        b'D'=>&[4,5,6,7],b'L'=>&[1,2,5,6],b'B'=>&[2,3,6,7],_=>panic!("face") };
    ps.iter().position(|&p|p==pos).unwrap()
}
fn face_codes(s:State)->[u8;24] {
    let mut out=[255u8;24];
    for pos in 0..8 {
        let c=s.cp[pos] as usize; let o=s.co[pos] as usize;
        for k in 0..3 {
            let f=POS_FACES[pos][k]; let color=CUBIE_COLORS[c][(k+3-o)%3];
            out[face_index(f)*4+face_slot(f,pos)]=FACE_ORDER.iter().position(|&x|x==color).unwrap() as u8;
        }
    }
    assert!(out.iter().all(|&x|x<6)); out
}
fn obs(c:&[u8;24],faces:&[u8])->u64 {
    let mut k=0; for &f in faces { let i=face_index(f); for j in 0..4 { k=(k<<4)|c[i*4+j] as u64; }} k
}
fn fnv(mut h:u64,bytes:&[u8])->u64 { for &b in bytes { h^=b as u64; h=h.wrapping_mul(0x100000001b3); } h }
fn main() {
    let out_path=env::args().nth(1).expect("usage: g7_p23_r1_quotient_census <receipt.txt>");
    assert_eq!(STATE_DOMAIN,3_674_160);
    let rs=rotations();
    let mut pose_to_anchor=[[0usize;3];8];
    for p in 0..8 { for o in 0..3u8 {
        let mut found=None;
        for (ri,&r) in rs.iter().enumerate() { if twist_for_piece_at(r,p,6,o)==(6,0) { assert!(found.is_none()); found=Some(ri); }}
        pose_to_anchor[p][o as usize]=found.expect("pose rotation");
    }}
    let mut seen=vec![0u8;(N_SOURCE+7)/8];
    let mut unique_source=0usize; let mut ufr:HashMap<u64,u32>=HashMap::with_capacity(3_100_000); let mut ufrd=HashSet::with_capacity(3_800_000);
    let mut stream_hash=0xcbf29ce484222325u64;
    let mut varying_fixed=0u32; let mut max_fixed=0usize;
    let mut witness:Option<(usize,usize,usize,u64,u64,u32)>=None;
    for target_rank in 0..STATE_DOMAIN {
        let anchor=full_from_target(target_rank);
        let ast=corner_state(anchor); assert_eq!(ast.rank().unwrap(),target_rank);
        let ac=face_codes(anchor); let akd=obs(&ac,&[b'U',b'F',b'R',b'D']); let aku=obs(&ac,&[b'U',b'F',b'R']);
        *ufr.entry(aku).or_insert(0)+=1; ufrd.insert(akd);
        let mut orbit=Vec::with_capacity(24);
        let mut fixed=Vec::with_capacity(24);
        for (ri,&r) in rs.iter().enumerate() {
            let src=rotate(anchor,r); let idx=raw_rank(src);
            let bit=1u8<<(idx%8); let slot=idx/8;
            assert_eq!(seen[slot]&bit,0,"duplicate raw source {idx}");
            seen[slot]|=bit; unique_source+=1;
            let canon=rotate(src,rs[pose_to_anchor[src.cp.iter().position(|&c|c==6).unwrap()][src.co[src.cp.iter().position(|&c|c==6).unwrap()] as usize]]);
            let cr=corner_state(canon).rank().unwrap();
            assert_eq!(cr,target_rank,"representative invariance: raw={idx}, rot={ri}");
            let cc=face_codes(canon); assert_eq!(obs(&cc,&[b'U',b'F',b'R',b'D']),akd); assert_eq!(obs(&cc,&[b'U',b'F',b'R']),aku);
            let fk=obs(&face_codes(src),&[b'U',b'F',b'R',b'D']);
            orbit.push((idx,ri,cr)); fixed.push((idx,ri,fk));
            for v in [idx as u64,target_rank as u64,ri as u64,fk] { stream_hash=fnv(stream_hash,&v.to_le_bytes()); }
        }
        assert_eq!(orbit.len(),24); orbit.sort_unstable();
        let mut fs:Vec<u64>=fixed.iter().map(|x|x.2).collect(); fs.sort_unstable(); fs.dedup();
        if fs.len()>1 {
            varying_fixed+=1; max_fixed=max_fixed.max(fs.len());
            fixed.sort_unstable_by_key(|x|(x.0,x.1));
            'pairs: for i in 0..fixed.len() { for j in i+1..fixed.len() { if fixed[i].2!=fixed[j].2 {
                let candidate=(fixed[i].0,fixed[i].1,fixed[j].0,fixed[j].1,fixed[i].2,fixed[j].2,target_rank);
                if witness.as_ref().map_or(true,|w|candidate < (w.0,w.1,w.2,w.3,w.4,w.5,w.6)) { witness=Some(candidate); }
                break 'pairs;
            }}}
        }
    }
    assert_eq!(unique_source,N_SOURCE);
    assert!(seen.iter().all(|&x|x==255));
    assert_eq!(ufrd.len(),3_674_160); assert_eq!(ufr.len(),2_906_280);
    let mut hist:HashMap<u32,u32>=HashMap::new(); for &n in ufr.values(){*hist.entry(n).or_insert(0)+=1;}
    assert_eq!(hist.get(&1),Some(&2_177_280)); assert_eq!(hist.get(&2),Some(&719_280)); assert_eq!(hist.get(&6),Some(&9_720)); assert_eq!(hist.len(),3);
    assert!(varying_fixed>0,"fixed-center nontransport counterexample absent");
    let w=witness.expect("fixed-center witness");
    let mut f=BufWriter::new(File::create(out_path).expect("create receipt"));
    writeln!(f,"G7_P23_R1_EXECUTABLE_QUOTIENT_CENSUS_PASS").unwrap();
    writeln!(f,"TARGET_DOMAIN\t{}",STATE_DOMAIN).unwrap();
    writeln!(f,"SOURCE_DOMAIN\t{}",N_SOURCE).unwrap();
    writeln!(f,"ROTATION_GROUP\t24_proper_signed_permutations").unwrap();
    writeln!(f,"UNIQUE_SOURCE_INDICES\t{}",unique_source).unwrap();
    writeln!(f,"FIBER_MULTIPLICITY\t24_every_target").unwrap();
    writeln!(f,"REPRESENTATIVE_INVARIANCE\tall_88179840_source_members").unwrap();
    writeln!(f,"UFRD_UNIQUE\t{}",ufrd.len()).unwrap();
    writeln!(f,"UFR_UNIQUE\t{}",ufr.len()).unwrap();
    writeln!(f,"UFR_FIBER_HIST\t1:2177280,2:719280,6:9720").unwrap();
    writeln!(f,"FIXED_CENTER_NONINVARIANT_QUOTIENT_FIBERS\t{}",varying_fixed).unwrap();
    writeln!(f,"FIXED_CENTER_MAX_DISTINCT_UFRD_KEYS_PER_FIBER\t{}",max_fixed).unwrap();
    writeln!(f,"FIXED_CENTER_WITNESS\tquotient_rank={},source_a={},rotation_a={},key_a={},source_b={},rotation_b={},key_b={}",w.6,w.0,w.1,w.4,w.2,w.3,w.5).unwrap();
    writeln!(f,"TRANSCRIPT_FNV1A64\t{:016x}",stream_hash).unwrap();
    f.flush().unwrap();
}
