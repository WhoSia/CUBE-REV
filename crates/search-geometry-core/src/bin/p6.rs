use cuberev_core::{ORIENTATIONS, STATE_DOMAIN};
use search_geometry_core::{
    bfs_geodesic, bfs_orientation_distance, bfs_phase2_distance, build_generator_cycle_c3,
    entry_surface_shortest_orientation, first_hit_two_phase_family, full_permutation_distance,
    TransitionTables, FULL_MOVES, PHASE2_MOVE_INDICES,
};
use std::collections::{BTreeMap, BTreeSet, HashMap};
use std::hash::Hash;

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
struct Q346 {
    dg: u8,
    do_: u8,
    entry_min: u8,
}

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
struct Pdb {
    do_: u8,
    dp: u8,
}

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
struct Sym {
    dg: u8,
    phase: [u8; 3],
}

#[derive(Clone, Copy, Debug)]
struct StateRow {
    dg: u8,
    pdb: Pdb,
    q: Q346,
    policy: u16,
    delta: u8,
    psi: [u8; 3],
    sym: Sym,
}

fn main() {
    let tables = TransitionTables::build();
    let dg = bfs_geodesic(&tables);
    let d_o = bfs_orientation_distance(&tables);
    let d_p = full_permutation_distance(&tables);
    let d_h = bfs_phase2_distance(&tables);
    let (entry_min, _) = entry_surface_shortest_orientation(&tables, &d_o, &d_h);
    let first_hit = first_hit_two_phase_family(&tables, &d_o, &d_h, 0)
        .into_iter()
        .next()
        .expect("slack-zero family");
    let c3 = build_generator_cycle_c3(&tables);

    let mut base_delta = vec![0u8; STATE_DOMAIN as usize];
    let mut base_policy = vec![0u16; STATE_DOMAIN as usize];

    for rank in 0..STATE_DOMAIN {
        let p = (rank / ORIENTATIONS) as usize;
        let o = (rank % ORIENTATIONS) as usize;
        base_delta[rank as usize] = d_o[o] + entry_min[rank as usize] - dg[rank as usize];
        base_policy[rank as usize] =
            optimal_policy_mask(rank, &tables, &d_o, &d_h, &first_hit);
        let _ = d_p[p];
    }

    let mut rows = Vec::with_capacity(STATE_DOMAIN as usize);
    for rank in 0..STATE_DOMAIN {
        let p = (rank / ORIENTATIONS) as usize;
        let o = (rank % ORIENTATIONS) as usize;
        let b = c3[rank as usize];
        let c = c3[b as usize];

        let mut psi = [
            base_delta[rank as usize],
            base_delta[b as usize],
            base_delta[c as usize],
        ];
        psi.sort_unstable();

        let mut phase = [
            d_o[o] + entry_min[rank as usize],
            d_o[(b % ORIENTATIONS) as usize] + entry_min[b as usize],
            d_o[(c % ORIENTATIONS) as usize] + entry_min[c as usize],
        ];
        phase.sort_unstable();

        rows.push(StateRow {
            dg: dg[rank as usize],
            pdb: Pdb { do_: d_o[o], dp: d_p[p] },
            q: Q346 {
                dg: dg[rank as usize],
                do_: d_o[o],
                entry_min: entry_min[rank as usize],
            },
            policy: base_policy[rank as usize],
            delta: base_delta[rank as usize],
            psi,
            sym: Sym { dg: dg[rank as usize], phase },
        });
    }

    let full_transition: Vec<[u32; 9]> = (0..STATE_DOMAIN)
        .map(|rank| {
            let mut out = [0u32; 9];
            for m in 0..FULL_MOVES.len() {
                out[m] = tables.next_rank(rank, m);
            }
            out
        })
        .collect();

    let repr_names = ["GEO", "PDB", "PHASE", "POLICY", "C3SYM", "FULL"];
    let claim_names = ["GEODESIC", "DELTA0", "POLICY", "PSI", "FULL_TRANSITION"];

    let geo: Vec<u8> = rows.iter().map(|r| r.dg).collect();
    let pdb: Vec<Pdb> = rows.iter().map(|r| r.pdb).collect();
    let phase: Vec<Q346> = rows.iter().map(|r| r.q).collect();
    let policy_repr: Vec<(Q346,u16)> = rows.iter().map(|r| (r.q,r.policy)).collect();
    let sym: Vec<Sym> = rows.iter().map(|r| r.sym).collect();
    let full: Vec<u32> = (0..STATE_DOMAIN).collect();

    let targets_geo: Vec<u8> = rows.iter().map(|r| r.dg).collect();
    let targets_delta: Vec<u8> = rows.iter().map(|r| r.delta).collect();
    let targets_policy: Vec<u16> = rows.iter().map(|r| r.policy).collect();
    let targets_psi: Vec<[u8;3]> = rows.iter().map(|r| r.psi).collect();

    let class_counts = [
        classes(&geo),
        classes(&pdb),
        classes(&phase),
        classes(&policy_repr),
        classes(&sym),
        classes(&full),
    ];

    let matrix = [
        [
            sufficient(&geo,&targets_geo).0,
            sufficient(&geo,&targets_delta).0,
            sufficient(&geo,&targets_policy).0,
            sufficient(&geo,&targets_psi).0,
            sufficient(&geo,&full_transition).0,
        ],
        [
            sufficient(&pdb,&targets_geo).0,
            sufficient(&pdb,&targets_delta).0,
            sufficient(&pdb,&targets_policy).0,
            sufficient(&pdb,&targets_psi).0,
            sufficient(&pdb,&full_transition).0,
        ],
        [
            sufficient(&phase,&targets_geo).0,
            sufficient(&phase,&targets_delta).0,
            sufficient(&phase,&targets_policy).0,
            sufficient(&phase,&targets_psi).0,
            sufficient(&phase,&full_transition).0,
        ],
        [
            sufficient(&policy_repr,&targets_geo).0,
            sufficient(&policy_repr,&targets_delta).0,
            sufficient(&policy_repr,&targets_policy).0,
            sufficient(&policy_repr,&targets_psi).0,
            sufficient(&policy_repr,&full_transition).0,
        ],
        [
            sufficient(&sym,&targets_geo).0,
            sufficient(&sym,&targets_delta).0,
            sufficient(&sym,&targets_policy).0,
            sufficient(&sym,&targets_psi).0,
            sufficient(&sym,&full_transition).0,
        ],
        [true,true,true,true,true],
    ];

    // Required inherited expectations.
    assert_eq!(class_counts[2], 346);
    assert_eq!(class_counts[3], 9_284);
    assert_eq!(class_counts[4], 1_046);
    assert!(matrix[2][0] && matrix[2][1]);
    assert!(!matrix[2][2]);
    assert!(matrix[3][0] && matrix[3][1] && matrix[3][2]);
    assert!(matrix[4][0] && matrix[4][3]);
    assert!(!matrix[4][1]);
    assert!(matrix[5].iter().all(|x| *x));

    println!("representation\tclasses");
    for (name,n) in repr_names.iter().zip(class_counts.iter()) {
        println!("{}\t{}",name,n);
    }

    println!("representation\tclaim\tsufficient");
    for (i,rn) in repr_names.iter().enumerate() {
        for (j,cn) in claim_names.iter().enumerate() {
            println!("{}\t{}\t{}",rn,cn,matrix[i][j]);
        }
    }

    // Deterministic collision witnesses for failed relations.
    emit_witness("GEO_to_DELTA", sufficient(&geo,&targets_delta).1);
    emit_witness("PDB_to_DELTA", sufficient(&pdb,&targets_delta).1);
    emit_witness("PHASE_to_POLICY", sufficient(&phase,&targets_policy).1);
    emit_witness("POLICY_to_FULL_TRANSITION", sufficient(&policy_repr,&full_transition).1);
    emit_witness("C3SYM_to_DELTA", sufficient(&sym,&targets_delta).1);

    // Matched-state packet seeds.
    emit_pair("H_GEO_PHASE", collision_pair(&geo,&targets_delta));
    emit_pair("H_PDB_ENTRY", collision_pair(&pdb,&targets_delta));
    emit_pair("H_STATIC_POLICY", collision_pair(&phase,&targets_policy));

    let c3_pair = (0..STATE_DOMAIN)
        .find_map(|rank| {
            let b = c3[rank as usize];
            if rank < b
                && dg[rank as usize] == dg[b as usize]
                && base_delta[rank as usize] != base_delta[b as usize]
            {
                Some((rank,b))
            } else { None }
        })
        .expect("R1 established C3 phase asymmetry");
    println!(
        "matched_packet\tH_C3_REP\trank_a={} rank_b={} dg={} delta_a={} delta_b={}",
        c3_pair.0,c3_pair.1,dg[c3_pair.0 as usize],
        base_delta[c3_pair.0 as usize],base_delta[c3_pair.1 as usize]
    );

    println!("prospective_packet\tH_VIEW\tSTATUS=BLOCKED_UNTIL_AUTHORITATIVE_UI_VIEWPOINT_STATE_MODEL");
    println!("human_world_contact\tCLOSED");
}

fn classes<K: Eq + Hash>(keys:&[K])->usize {
    let mut set=HashMap::<&K,()>::new();
    for k in keys { set.insert(k,()); }
    set.len()
}

fn sufficient<K,T>(keys:&[K], targets:&[T])->(bool,Option<(u32,u32)>)
where K: Eq+Hash+Copy, T: Eq+Copy {
    let mut map=HashMap::<K,(T,u32)>::new();
    for (i,(&k,&t)) in keys.iter().zip(targets.iter()).enumerate() {
        match map.get(&k).copied() {
            None=>{map.insert(k,(t,i as u32));}
            Some((old,j)) if old!=t=>return (false,Some((j,i as u32))),
            _=>{}
        }
    }
    (true,None)
}

fn collision_pair<K,T>(keys:&[K],targets:&[T])->(u32,u32)
where K:Eq+Hash+Copy,T:Eq+Copy {
    sufficient(keys,targets).1.expect("requested failed relation needs collision")
}

fn emit_witness(label:&str,w:Option<(u32,u32)>) {
    match w {
        Some((a,b))=>println!("collision\t{}\trank_a={} rank_b={}",label,a,b),
        None=>println!("collision\t{}\tNONE",label),
    }
}

fn emit_pair(label:&str,p:(u32,u32)) {
    println!("matched_packet\t{}\trank_a={} rank_b={}",label,p.0,p.1);
}

fn optimal_policy_mask(
    rank:u32,
    tables:&TransitionTables,
    d_o:&[u8],
    d_h:&[u8],
    first_hit:&[u8],
)->u16 {
    if rank==0 { return 0; }
    let o=(rank%ORIENTATIONS) as usize;
    let p=(rank/ORIENTATIONS) as usize;
    let mut mask=0u16;
    if d_o[o]==0 {
        let here=d_h[p];
        for &m in &PHASE2_MOVE_INDICES {
            let next=tables.next_rank(rank,m);
            let np=(next/ORIENTATIONS) as usize;
            if d_h[np]+1==here { mask|=1u16<<m; }
        }
    } else {
        let here=first_hit[rank as usize];
        for m in 0..FULL_MOVES.len() {
            let next=tables.next_rank(rank,m);
            let no=(next%ORIENTATIONS) as usize;
            if d_o[no]+1==d_o[o] && first_hit[next as usize]+1==here {
                mask|=1u16<<m;
            }
        }
    }
    mask
}
