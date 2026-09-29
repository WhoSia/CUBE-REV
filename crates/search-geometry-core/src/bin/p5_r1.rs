use cuberev_core::{ORIENTATIONS, STATE_DOMAIN};
use search_geometry_core::{
    bfs_geodesic, bfs_orientation_distance, bfs_phase2_distance, build_generator_cycle_c3,
    entry_surface_shortest_orientation, first_hit_two_phase_family, full_permutation_distance,
    TransitionTables,
};
use std::collections::{BTreeMap, BTreeSet};

fn main() {
    let tables = TransitionTables::build();
    let dg = bfs_geodesic(&tables);
    let d_o_coord = bfs_orientation_distance(&tables);
    let d_h = bfs_phase2_distance(&tables);
    let d_p = full_permutation_distance(&tables);
    let (entry_min, entry_max) =
        entry_surface_shortest_orientation(&tables, &d_o_coord, &d_h);
    let first_hit_0 =
        first_hit_two_phase_family(&tables, &d_o_coord, &d_h, 0)
            .into_iter()
            .next()
            .expect("slack-zero court");
    let c3 = build_generator_cycle_c3(&tables);

    let mut by_do: BTreeMap<u8, (u64, u64, u8)> = BTreeMap::new();
    let mut by_entry: BTreeMap<u8, (u64, u64, u8)> = BTreeMap::new();
    let mut by_pdb_residual: BTreeMap<u8, (u64, u64, u8)> = BTreeMap::new();
    let mut entry_width_hist: BTreeMap<u8, u64> = BTreeMap::new();

    let mut max_gap = 0u8;
    let mut max_gap_states = Vec::new();
    let mut decomposition_violations = 0u32;
    let mut pdb_violations = 0u32;

    let mut same_dg: BTreeMap<u8, (u32, u8, u32, u8)> = BTreeMap::new();
    let mut same_do: BTreeMap<u8, (u32, u8, u32, u8)> = BTreeMap::new();
    let mut same_pdb: BTreeMap<u8, (u32, u8, u32, u8)> = BTreeMap::new();

    for rank in 0..STATE_DOMAIN {
        let p = (rank / ORIENTATIONS) as usize;
        let o = (rank % ORIENTATIONS) as usize;
        let do_s = d_o_coord[o];
        let hpdb = do_s.max(d_p[p]);
        if hpdb > dg[rank as usize] {
            pdb_violations += 1;
        }

        let phase0 = do_s + entry_min[rank as usize];
        let gap = phase0 - dg[rank as usize];
        if phase0 != first_hit_0[rank as usize] {
            decomposition_violations += 1;
        }

        let width = entry_max[rank as usize] - entry_min[rank as usize];
        *entry_width_hist.entry(width).or_default() += 1;

        push_stat(&mut by_do, do_s, gap);
        push_stat(&mut by_entry, entry_min[rank as usize], gap);
        push_stat(&mut by_pdb_residual, dg[rank as usize] - hpdb, gap);

        witness_collision(&mut same_dg, dg[rank as usize], rank, gap);
        witness_collision(&mut same_do, do_s, rank, gap);
        witness_collision(&mut same_pdb, hpdb, rank, gap);

        if gap > max_gap {
            max_gap = gap;
            max_gap_states.clear();
            max_gap_states.push(rank);
        } else if gap == max_gap && max_gap_states.len() < 64 {
            max_gap_states.push(rank);
        }
    }

    assert_eq!(decomposition_violations, 0);
    assert_eq!(pdb_violations, 0);

    let mut visited = vec![false; STATE_DOMAIN as usize];
    let mut orbit_count = 0u32;
    let mut fixed_count = 0u32;
    let mut geodesic_symmetry_violations = 0u32;
    let mut phase_invariant_orbits = 0u32;
    let mut phase_varying_orbits = 0u32;
    let mut max_gap_orbit_spread = 0u8;
    let mut max_gap_orbit_canon = Vec::new();

    for rank in 0..STATE_DOMAIN {
        if visited[rank as usize] {
            continue;
        }
        let a = rank;
        let b = c3[a as usize];
        let c = c3[b as usize];
        assert_eq!(c3[c as usize], a);

        let mut orbit = vec![a, b, c];
        orbit.sort_unstable();
        orbit.dedup();
        orbit_count += 1;
        if orbit.len() == 1 {
            fixed_count += 1;
        }
        for &x in &orbit {
            visited[x as usize] = true;
        }

        let dg0 = dg[orbit[0] as usize];
        if orbit.iter().any(|&x| dg[x as usize] != dg0) {
            geodesic_symmetry_violations += 1;
        }

        let gaps: Vec<u8> = orbit
            .iter()
            .map(|&x| gap_of(x, &dg, &d_o_coord, &entry_min))
            .collect();
        let lo = *gaps.iter().min().unwrap();
        let hi = *gaps.iter().max().unwrap();
        if lo == hi {
            phase_invariant_orbits += 1;
        } else {
            phase_varying_orbits += 1;
        }
        let spread = hi - lo;
        if spread > max_gap_orbit_spread {
            max_gap_orbit_spread = spread;
            max_gap_orbit_canon.clear();
            max_gap_orbit_canon.push(orbit[0]);
        } else if spread == max_gap_orbit_spread && max_gap_orbit_canon.len() < 32 {
            max_gap_orbit_canon.push(orbit[0]);
        }
    }

    assert_eq!(geodesic_symmetry_violations, 0);

    println!("metric\tvalue");
    println!("states\t{}", STATE_DOMAIN);
    println!("c3_orbits\t{}", orbit_count);
    println!("c3_fixed_states\t{}", fixed_count);
    println!(
        "geodesic_symmetry_violations\t{}",
        geodesic_symmetry_violations
    );
    println!("phase_invariant_orbits\t{}", phase_invariant_orbits);
    println!("phase_varying_orbits\t{}", phase_varying_orbits);
    println!("max_phase_gap_orbit_spread\t{}", max_gap_orbit_spread);
    println!("decomposition_violations\t{}", decomposition_violations);
    println!("pdb_lower_bound_violations\t{}", pdb_violations);
    println!("max_gap\t{}", max_gap);

    for (k, (n, sum, mx)) in &by_do {
        println!(
            "by_do_{}\tn={} mean_gap={:.6} max_gap={}",
            k,
            n,
            *sum as f64 / *n as f64,
            mx
        );
    }
    for (k, (n, sum, mx)) in &by_entry {
        println!(
            "by_entry_hmin_{}\tn={} mean_gap={:.6} max_gap={}",
            k,
            n,
            *sum as f64 / *n as f64,
            mx
        );
    }
    for (k, (n, sum, mx)) in &by_pdb_residual {
        println!(
            "by_pdb_residual_{}\tn={} mean_gap={:.6} max_gap={}",
            k,
            n,
            *sum as f64 / *n as f64,
            mx
        );
    }
    for (k, n) in &entry_width_hist {
        println!("entry_width_{}\t{}", k, n);
    }

    for (i, &rank) in max_gap_states.iter().enumerate() {
        print_witness(
            "max_gap",
            i,
            rank,
            &dg,
            &d_o_coord,
            &d_p,
            &entry_min,
            &entry_max,
            &c3,
        );
    }
    for (i, &rank) in max_gap_orbit_canon.iter().enumerate() {
        let a = rank;
        let b = c3[a as usize];
        let c = c3[b as usize];
        println!(
            "max_orbit_spread_{}\tcanon={} orbit={},{},{} gaps={},{},{}",
            i,
            rank,
            a,
            b,
            c,
            gap_of(a, &dg, &d_o_coord, &entry_min),
            gap_of(b, &dg, &d_o_coord, &entry_min),
            gap_of(c, &dg, &d_o_coord, &entry_min)
        );
    }

    emit_collision("same_dg_diff_gap", &same_dg);
    emit_collision("same_do_diff_gap", &same_do);
    emit_collision("same_pdb_diff_gap", &same_pdb);

    let mut phase_asym_witnesses = BTreeSet::new();
    for rank in 0..STATE_DOMAIN {
        let mate = c3[rank as usize];
        if gap_of(rank, &dg, &d_o_coord, &entry_min)
            != gap_of(mate, &dg, &d_o_coord, &entry_min)
        {
            let canon = rank.min(mate).min(c3[mate as usize]);
            phase_asym_witnesses.insert(canon);
            if phase_asym_witnesses.len() >= 16 {
                break;
            }
        }
    }
    for (i, rank) in phase_asym_witnesses.into_iter().enumerate() {
        let b = c3[rank as usize];
        let c = c3[b as usize];
        println!(
            "c3_phase_asym_{}\torbit={},{},{} dg={},{},{} gap={},{},{}",
            i,
            rank,
            b,
            c,
            dg[rank as usize],
            dg[b as usize],
            dg[c as usize],
            gap_of(rank, &dg, &d_o_coord, &entry_min),
            gap_of(b, &dg, &d_o_coord, &entry_min),
            gap_of(c, &dg, &d_o_coord, &entry_min)
        );
    }
}

fn push_stat(map: &mut BTreeMap<u8, (u64, u64, u8)>, key: u8, gap: u8) {
    let e = map.entry(key).or_insert((0, 0, 0));
    e.0 += 1;
    e.1 += gap as u64;
    e.2 = e.2.max(gap);
}

fn witness_collision(
    map: &mut BTreeMap<u8, (u32, u8, u32, u8)>,
    key: u8,
    rank: u32,
    gap: u8,
) {
    match map.get_mut(&key) {
        None => {
            map.insert(key, (rank, gap, rank, gap));
        }
        Some(v) => {
            if gap < v.1 {
                v.0 = rank;
                v.1 = gap;
            }
            if gap > v.3 {
                v.2 = rank;
                v.3 = gap;
            }
        }
    }
}

fn emit_collision(label: &str, map: &BTreeMap<u8, (u32, u8, u32, u8)>) {
    if let Some((key, (lo_rank, lo_gap, hi_rank, hi_gap))) =
        map.iter().find(|(_, (_, lo, _, hi))| lo != hi)
    {
        println!(
            "{}\tkey={} low_rank={} low_gap={} high_rank={} high_gap={}",
            label, key, lo_rank, lo_gap, hi_rank, hi_gap
        );
    } else {
        println!("{}\tNONE", label);
    }
}

fn gap_of(rank: u32, dg: &[u8], d_o_coord: &[u8], entry_min: &[u8]) -> u8 {
    let o = (rank % ORIENTATIONS) as usize;
    d_o_coord[o] + entry_min[rank as usize] - dg[rank as usize]
}

fn print_witness(
    label: &str,
    i: usize,
    rank: u32,
    dg: &[u8],
    d_o_coord: &[u8],
    d_p: &[u8],
    entry_min: &[u8],
    entry_max: &[u8],
    c3: &[u32],
) {
    let p = (rank / ORIENTATIONS) as usize;
    let o = (rank % ORIENTATIONS) as usize;
    let hpdb = d_o_coord[o].max(d_p[p]);
    println!(
        "{}_{}\trank={} dg={} do={} dp={} hpdb={} pdb_residual={} entry_h_min={} entry_h_max={} entry_width={} gap={} c3={},{}",
        label,
        i,
        rank,
        dg[rank as usize],
        d_o_coord[o],
        d_p[p],
        hpdb,
        dg[rank as usize] - hpdb,
        entry_min[rank as usize],
        entry_max[rank as usize],
        entry_max[rank as usize] - entry_min[rank as usize],
        gap_of(rank, dg, d_o_coord, entry_min),
        c3[rank as usize],
        c3[c3[rank as usize] as usize]
    );
}
