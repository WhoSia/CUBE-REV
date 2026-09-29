use cuberev_core::{ORIENTATIONS, STATE_DOMAIN};
use search_geometry_core::{
    bfs_geodesic, bfs_orientation_distance, bfs_phase2_distance,
    entry_surface_shortest_orientation, first_hit_two_phase_family, TransitionTables,
    FULL_MOVES, PHASE2_MOVE_INDICES,
};
use std::collections::{BTreeMap, BTreeSet, HashMap};

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
struct Q346 {
    dg: u8,
    do_: u8,
    entry_min: u8,
}

fn main() {
    let tables = TransitionTables::build();
    let dg = bfs_geodesic(&tables);
    let d_o = bfs_orientation_distance(&tables);
    let d_h = bfs_phase2_distance(&tables);
    let (entry_min, _) = entry_surface_shortest_orientation(&tables, &d_o, &d_h);
    let first_hit = first_hit_two_phase_family(&tables, &d_o, &d_h, 0)
        .into_iter()
        .next()
        .expect("slack-zero family");

    let mut labels = Vec::with_capacity(STATE_DOMAIN as usize);
    let mut classes = BTreeSet::new();
    let mut zero_states = 0u32;
    for rank in 0..STATE_DOMAIN {
        let o = (rank % ORIENTATIONS) as usize;
        let q = Q346 {
            dg: dg[rank as usize],
            do_: d_o[o],
            entry_min: entry_min[rank as usize],
        };
        if q.dg == 0 {
            zero_states += 1;
        }
        classes.insert((q.dg, q.do_, q.entry_min));
        labels.push(q);
    }
    assert_eq!(classes.len(), 346);
    assert_eq!(zero_states, 1);
    assert!(dg.iter().all(|&d| d != u8::MAX));

    // Court A: q346 action congruence witness.
    let mut seen_successor = HashMap::<(Q346, usize), (Q346, u32)>::new();
    let mut congruence_violations = 0u64;
    let mut first_congruence_witness = None;

    for rank in 0..STATE_DOMAIN {
        let q = labels[rank as usize];
        for m in 0..FULL_MOVES.len() {
            let next = tables.next_rank(rank, m);
            let qn = labels[next as usize];
            match seen_successor.get(&(q, m)).copied() {
                None => {
                    seen_successor.insert((q, m), (qn, rank));
                }
                Some((old, old_rank)) if old != qn => {
                    congruence_violations += 1;
                    if first_congruence_witness.is_none() {
                        first_congruence_witness = Some((old_rank, rank, m, old, qn));
                    }
                }
                _ => {}
            }
        }
    }
    assert!(congruence_violations > 0);
    let witness = first_congruence_witness.expect("q346 must fail action congruence");

    // Court B executable premises: inverse closure.
    let inverse_move: [usize; 9] = [2, 1, 0, 5, 4, 3, 8, 7, 6];
    let samples = [0u32, 1, 728, 729, 91_337, STATE_DOMAIN - 1];
    let mut inverse_violations = 0u32;
    for &rank in &samples {
        for m in 0..FULL_MOVES.len() {
            let next = tables.next_rank(rank, m);
            let back = tables.next_rank(next, inverse_move[m]);
            if back != rank {
                inverse_violations += 1;
            }
        }
    }
    assert_eq!(inverse_violations, 0);

    // Court C: exact slack-0 optimal phase-policy mask.
    let mut policy_masks = BTreeSet::new();
    let mut q_to_masks = BTreeMap::<(u8, u8, u8), BTreeSet<u16>>::new();
    let mut q_policy_classes = BTreeSet::<(u8, u8, u8, u16)>::new();
    let mut first_policy_witness = None;
    let mut q_first_rank_mask = HashMap::<Q346, (u32, u16)>::new();

    for rank in 0..STATE_DOMAIN {
        let mask = optimal_policy_mask(rank, &tables, &d_o, &d_h, &first_hit);
        if rank == 0 {
            assert_eq!(mask, 0);
        } else {
            assert_ne!(mask, 0, "every nonterminal state must have an optimal move");
            policy_masks.insert(mask);
        }

        let q = labels[rank as usize];
        q_to_masks
            .entry((q.dg, q.do_, q.entry_min))
            .or_default()
            .insert(mask);
        q_policy_classes.insert((q.dg, q.do_, q.entry_min, mask));

        match q_first_rank_mask.get(&q).copied() {
            None => {
                q_first_rank_mask.insert(q, (rank, mask));
            }
            Some((r0, m0)) if m0 != mask && first_policy_witness.is_none() => {
                first_policy_witness = Some((r0, m0, rank, mask, q));
            }
            _ => {}
        }
    }

    let split_q_classes = q_to_masks.values().filter(|s| s.len() > 1).count();
    assert!(split_q_classes > 0);
    let policy_witness = first_policy_witness.expect("q346 must not determine policy");

    println!("metric\tvalue");
    println!("states\t{}", STATE_DOMAIN);
    println!("q346_classes\t{}", classes.len());
    println!("unique_dg_zero_states\t{}", zero_states);
    println!("reachable_states\t{}", dg.iter().filter(|&&d| d != u8::MAX).count());
    println!("inverse_sample_violations\t{}", inverse_violations);
    println!("q346_action_congruence_violations\t{}", congruence_violations);
    println!("minimal_full_action_predictive_classes\t{}", STATE_DOMAIN);
    println!(
        "distinct_nonterminal_optimal_policy_masks\t{}",
        policy_masks.len()
    );
    println!(
        "q346_classes_split_by_policy_mask\t{}",
        split_q_classes
    );
    println!(
        "q346_plus_policy_mask_classes\t{}",
        q_policy_classes.len()
    );

    println!(
        "action_congruence_witness\trank_a={} rank_b={} move={} successor_a=({},{},{}) successor_b=({},{},{})",
        witness.0,
        witness.1,
        witness.2,
        witness.3.dg,
        witness.3.do_,
        witness.3.entry_min,
        witness.4.dg,
        witness.4.do_,
        witness.4.entry_min
    );

    println!(
        "policy_output_witness\trank_a={} mask_a={} rank_b={} mask_b={} q346=({},{},{})",
        policy_witness.0,
        policy_witness.1,
        policy_witness.2,
        policy_witness.3,
        policy_witness.4.dg,
        policy_witness.4.do_,
        policy_witness.4.entry_min
    );
}

fn optimal_policy_mask(
    rank: u32,
    tables: &TransitionTables,
    d_o: &[u8],
    d_h: &[u8],
    first_hit: &[u8],
) -> u16 {
    if rank == 0 {
        return 0;
    }

    let o = (rank % ORIENTATIONS) as usize;
    let p = (rank / ORIENTATIONS) as usize;
    let mut mask = 0u16;

    if d_o[o] == 0 {
        let here = d_h[p];
        for &m in &PHASE2_MOVE_INDICES {
            let next = tables.next_rank(rank, m);
            let next_p = (next / ORIENTATIONS) as usize;
            if d_h[next_p] + 1 == here {
                mask |= 1u16 << m;
            }
        }
    } else {
        let here = first_hit[rank as usize];
        for m in 0..FULL_MOVES.len() {
            let next = tables.next_rank(rank, m);
            let next_o = (next % ORIENTATIONS) as usize;
            if d_o[next_o] + 1 == d_o[o] && first_hit[next as usize] + 1 == here {
                mask |= 1u16 << m;
            }
        }
    }

    mask
}
