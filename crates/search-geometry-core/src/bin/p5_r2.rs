use cuberev_core::{ORIENTATIONS, STATE_DOMAIN};
use search_geometry_core::{
    bfs_geodesic, bfs_orientation_distance, bfs_phase2_distance, build_generator_cycle_c3,
    entry_surface_shortest_orientation, entry_surface_spectrum_shortest_orientation,
    full_permutation_distance, spectrum_cardinality, spectrum_max, spectrum_min, TransitionTables,
};
use std::collections::{BTreeMap, BTreeSet, HashMap};

const F_DG: u8 = 1 << 0;
const F_DO: u8 = 1 << 1;
const F_DP: u8 = 1 << 2;
const F_ENTRY_MIN: u8 = 1 << 3;
const F_ENTRY_WIDTH: u8 = 1 << 4;
const F_SPECTRUM: u8 = 1 << 5;
const ALL_FEATURES: u8 =
    F_DG | F_DO | F_DP | F_ENTRY_MIN | F_ENTRY_WIDTH | F_SPECTRUM;

#[derive(Clone, Copy)]
struct Coordinates {
    dg: u8,
    do_: u8,
    dp: u8,
    entry_min: u8,
    entry_width: u8,
    spectrum: u16,
    delta: u8,
}

#[derive(Debug)]
struct SufficiencyResult {
    mask: u8,
    sufficient: bool,
    classes: usize,
    witness: Option<(u32, u8, u32, u8)>,
}

fn main() {
    let tables = TransitionTables::build();
    let dg = bfs_geodesic(&tables);
    let d_o_coord = bfs_orientation_distance(&tables);
    let d_h = bfs_phase2_distance(&tables);
    let d_p = full_permutation_distance(&tables);
    let (entry_min, entry_max) =
        entry_surface_shortest_orientation(&tables, &d_o_coord, &d_h);
    let spectrum =
        entry_surface_spectrum_shortest_orientation(&tables, &d_o_coord, &d_h);
    let c3 = build_generator_cycle_c3(&tables);

    let mut coords = Vec::with_capacity(STATE_DOMAIN as usize);
    let mut spectrum_cardinality_hist = BTreeMap::<u8, u64>::new();
    let mut unique_spectra = BTreeSet::<u16>::new();
    let mut topology_to_delta = HashMap::<u16, (u32, u8)>::new();
    let mut topology_collision = None;

    for rank in 0..STATE_DOMAIN {
        let p = (rank / ORIENTATIONS) as usize;
        let o = (rank % ORIENTATIONS) as usize;
        let do_ = d_o_coord[o];
        let emin = entry_min[rank as usize];
        let emax = entry_max[rank as usize];
        let mask = spectrum[rank as usize];

        assert_eq!(spectrum_min(mask), emin);
        assert_eq!(spectrum_max(mask), emax);

        let delta = do_ + emin - dg[rank as usize];
        let c = Coordinates {
            dg: dg[rank as usize],
            do_,
            dp: d_p[p],
            entry_min: emin,
            entry_width: emax - emin,
            spectrum: mask,
            delta,
        };
        coords.push(c);

        let card = spectrum_cardinality(mask);
        *spectrum_cardinality_hist.entry(card).or_default() += 1;
        unique_spectra.insert(mask);

        match topology_to_delta.get(&mask).copied() {
            None => {
                topology_to_delta.insert(mask, (rank, delta));
            }
            Some((r0, d0)) if d0 != delta && topology_collision.is_none() => {
                topology_collision = Some((mask, r0, d0, rank, delta));
            }
            _ => {}
        }
    }

    // A. True refinement of the 729-state orientation coordinate.
    // Search all subsets of non-orientation structural coordinates.
    let orientation_extras = F_DG | F_DP | F_ENTRY_MIN | F_ENTRY_WIDTH | F_SPECTRUM;
    let mut orientation_results = Vec::new();
    for mask in 0..=ALL_FEATURES {
        if mask & !orientation_extras != 0 {
            continue;
        }
        orientation_results.push(check_sufficiency(
            &coords,
            Some(&orientation_rank_vector()),
            mask,
        ));
    }
    let min_orientation_added = orientation_results
        .iter()
        .filter(|r| r.sufficient)
        .map(|r| r.mask.count_ones())
        .min()
        .expect("some orientation refinement must be sufficient");
    let best_orientation = orientation_results
        .iter()
        .filter(|r| r.sufficient && r.mask.count_ones() == min_orientation_added)
        .min_by_key(|r| r.classes)
        .unwrap();

    // B. Alternative structural representation not required to refine orientation rank.
    let mut structural_results = Vec::new();
    for mask in 1..=ALL_FEATURES {
        structural_results.push(check_sufficiency(&coords, None, mask));
    }
    let min_structural_features = structural_results
        .iter()
        .filter(|r| r.sufficient)
        .map(|r| r.mask.count_ones())
        .min()
        .expect("some structural representation must be sufficient");
    let best_structural = structural_results
        .iter()
        .filter(|r| r.sufficient && r.mask.count_ones() == min_structural_features)
        .min_by_key(|r| r.classes)
        .unwrap();

    // C. C3 impossibility for the unsymmetrized delta target.
    let mut visited = vec![false; STATE_DOMAIN as usize];
    let mut orbit_count = 0u32;
    let mut varying_delta_orbits = 0u32;
    let mut impossibility_witness = None;
    let mut gap_profiles = BTreeSet::<[u8; 3]>::new();
    let mut phase_profiles = BTreeSet::<(u8, [u8; 3])>::new();
    let mut phase_profile_to_gap = HashMap::<[u8; 3], [u8; 3]>::new();
    let mut phase_profile_without_dg_collision = None;
    let mut structural_profile_to_gap =
        HashMap::<(u8, [(u8, u8); 3]), [u8; 3]>::new();

    for rank in 0..STATE_DOMAIN {
        if visited[rank as usize] {
            continue;
        }

        let b = c3[rank as usize];
        let c = c3[b as usize];
        let mut orbit = [rank, b, c];
        orbit.sort_unstable();
        orbit_count += 1;
        for &x in &orbit {
            visited[x as usize] = true;
        }

        let mut gaps = [
            coords[orbit[0] as usize].delta,
            coords[orbit[1] as usize].delta,
            coords[orbit[2] as usize].delta,
        ];
        let raw_gaps = gaps;
        gaps.sort_unstable();
        gap_profiles.insert(gaps);

        if raw_gaps[0] != raw_gaps[1] || raw_gaps[1] != raw_gaps[2] {
            varying_delta_orbits += 1;
            if impossibility_witness.is_none() {
                impossibility_witness = Some((orbit, raw_gaps));
            }
        }

        let dg_orbit = coords[orbit[0] as usize].dg;
        assert_eq!(coords[orbit[1] as usize].dg, dg_orbit);
        assert_eq!(coords[orbit[2] as usize].dg, dg_orbit);

        let mut phase_lengths = [
            coords[orbit[0] as usize].do_ + coords[orbit[0] as usize].entry_min,
            coords[orbit[1] as usize].do_ + coords[orbit[1] as usize].entry_min,
            coords[orbit[2] as usize].do_ + coords[orbit[2] as usize].entry_min,
        ];
        phase_lengths.sort_unstable();
        phase_profiles.insert((dg_orbit, phase_lengths));

        match phase_profile_to_gap.get(&phase_lengths).copied() {
            None => {
                phase_profile_to_gap.insert(phase_lengths, gaps);
            }
            Some(old) if old != gaps && phase_profile_without_dg_collision.is_none() => {
                phase_profile_without_dg_collision = Some((phase_lengths, old, gaps));
            }
            _ => {}
        }

        let mut structural = [
            (
                coords[orbit[0] as usize].do_,
                coords[orbit[0] as usize].entry_min,
            ),
            (
                coords[orbit[1] as usize].do_,
                coords[orbit[1] as usize].entry_min,
            ),
            (
                coords[orbit[2] as usize].do_,
                coords[orbit[2] as usize].entry_min,
            ),
        ];
        structural.sort_unstable();
        match structural_profile_to_gap.get(&(dg_orbit, structural)).copied() {
            None => {
                structural_profile_to_gap.insert((dg_orbit, structural), gaps);
            }
            Some(old) => assert_eq!(
                old, gaps,
                "(dG, sorted(dO,entryMin)) must determine the orbit gap profile"
            ),
        }
    }

    assert!(varying_delta_orbits > 0);
    assert!(impossibility_witness.is_some());

    // D. Exact target quotient and structural compression counts.
    let delta_classes = coords
        .iter()
        .map(|c| c.delta)
        .collect::<BTreeSet<_>>()
        .len();
    let orientation_classes = orientation_rank_vector()
        .into_iter()
        .collect::<BTreeSet<_>>()
        .len();

    println!("metric\tvalue");
    println!("states\t{}", STATE_DOMAIN);
    println!("orientation_coordinate_classes\t{}", orientation_classes);
    println!("delta_target_classes\t{}", delta_classes);
    println!("unique_entry_spectra\t{}", unique_spectra.len());
    println!("c3_orbits\t{}", orbit_count);
    println!("c3_delta_varying_orbits\t{}", varying_delta_orbits);
    println!("orbit_gap_profile_classes\t{}", gap_profiles.len());
    println!(
        "c3_structural_phase_profile_classes\t{}",
        phase_profiles.len()
    );
    println!(
        "c3_pair_structural_profile_classes\t{}",
        structural_profile_to_gap.len()
    );

    println!(
        "orientation_refinement_min_added_features\t{}",
        min_orientation_added
    );
    println!(
        "orientation_refinement_best_mask\t{}",
        feature_names(best_orientation.mask)
    );
    println!(
        "orientation_refinement_best_classes\t{}",
        best_orientation.classes
    );

    println!(
        "structural_min_feature_count\t{}",
        min_structural_features
    );
    println!(
        "structural_best_mask\t{}",
        feature_names(best_structural.mask)
    );
    println!("structural_best_classes\t{}", best_structural.classes);

    for r in orientation_results
        .iter()
        .filter(|r| r.sufficient && r.mask.count_ones() == min_orientation_added)
    {
        println!(
            "orientation_minimal_sufficient\tmask={} classes={}",
            feature_names(r.mask),
            r.classes
        );
    }
    for r in structural_results
        .iter()
        .filter(|r| r.sufficient && r.mask.count_ones() == min_structural_features)
    {
        println!(
            "structural_minimal_sufficient\tmask={} classes={}",
            feature_names(r.mask),
            r.classes
        );
    }

    for (card, n) in spectrum_cardinality_hist {
        println!("entry_spectrum_cardinality_{}\t{}", card, n);
    }

    if let Some((mask, r0, d0, r1, d1)) = topology_collision {
        println!(
            "same_entry_spectrum_diff_delta\tmask={} low_rank={} delta={} high_rank={} delta={}",
            mask, r0, d0, r1, d1
        );
    } else {
        println!("same_entry_spectrum_diff_delta\tNONE");
    }

    let (orbit, raw_gaps) = impossibility_witness.unwrap();
    println!(
        "c3_invariant_delta_sufficiency_impossible_witness\torbit={},{},{} gaps={},{},{}",
        orbit[0], orbit[1], orbit[2], raw_gaps[0], raw_gaps[1], raw_gaps[2]
    );

    if let Some((phase, old, new)) = phase_profile_without_dg_collision {
        println!(
            "phase_profile_without_dg_not_sufficient\tphase={:?} gaps_a={:?} gaps_b={:?}",
            phase, old, new
        );
    } else {
        println!("phase_profile_without_dg_not_sufficient\tNONE");
    }

    // Explicitly certify the structural symmetric quotient.
    for ((dg, structural), gaps) in structural_profile_to_gap.iter() {
        let mut derived = [
            structural[0].0 + structural[0].1 - *dg,
            structural[1].0 + structural[1].1 - *dg,
            structural[2].0 + structural[2].1 - *dg,
        ];
        derived.sort_unstable();
        assert_eq!(&derived, gaps);
    }
    println!("symmetric_structural_quotient_violations\t0");

    // Print first insufficiency witnesses for the simplest candidate families.
    for mask in [F_DO, F_ENTRY_MIN, F_DG, F_DP, F_SPECTRUM, F_DG | F_ENTRY_MIN] {
        let r = structural_results.iter().find(|r| r.mask == mask).unwrap();
        if let Some((a, da, b, db)) = r.witness {
            println!(
                "insufficient_{}\trank_a={} delta_a={} rank_b={} delta_b={}",
                feature_names(mask),
                a,
                da,
                b,
                db
            );
        }
    }
}

fn orientation_rank_vector() -> Vec<u16> {
    (0..STATE_DOMAIN)
        .map(|rank| (rank % ORIENTATIONS) as u16)
        .collect()
}

fn check_sufficiency(
    coords: &[Coordinates],
    orientation_rank: Option<&[u16]>,
    mask: u8,
) -> SufficiencyResult {
    let mut map = HashMap::<u64, (u32, u8)>::new();
    let mut witness = None;

    for (rank, c) in coords.iter().copied().enumerate() {
        let ori = orientation_rank.map(|v| v[rank]).unwrap_or(0);
        let key = pack_key(c, ori, mask, orientation_rank.is_some());
        match map.get(&key).copied() {
            None => {
                map.insert(key, (rank as u32, c.delta));
            }
            Some((r0, d0)) if d0 != c.delta => {
                witness = Some((r0, d0, rank as u32, c.delta));
                return SufficiencyResult {
                    mask,
                    sufficient: false,
                    classes: map.len(),
                    witness,
                };
            }
            _ => {}
        }
    }

    SufficiencyResult {
        mask,
        sufficient: true,
        classes: map.len(),
        witness,
    }
}

fn pack_key(c: Coordinates, ori: u16, mask: u8, include_ori: bool) -> u64 {
    let mut key = 0u64;
    let mut shift = 0u32;

    if include_ori {
        key |= (ori as u64) << shift;
        shift += 10;
    }
    if mask & F_DG != 0 {
        key |= (c.dg as u64) << shift;
        shift += 4;
    }
    if mask & F_DO != 0 {
        key |= (c.do_ as u64) << shift;
        shift += 3;
    }
    if mask & F_DP != 0 {
        key |= (c.dp as u64) << shift;
        shift += 4;
    }
    if mask & F_ENTRY_MIN != 0 {
        key |= (c.entry_min as u64) << shift;
        shift += 4;
    }
    if mask & F_ENTRY_WIDTH != 0 {
        key |= (c.entry_width as u64) << shift;
        shift += 4;
    }
    if mask & F_SPECTRUM != 0 {
        key |= (c.spectrum as u64) << shift;
    }

    key
}

fn feature_names(mask: u8) -> String {
    let mut names = Vec::new();
    if mask & F_DG != 0 {
        names.push("dG");
    }
    if mask & F_DO != 0 {
        names.push("dO");
    }
    if mask & F_DP != 0 {
        names.push("dP");
    }
    if mask & F_ENTRY_MIN != 0 {
        names.push("entryMin");
    }
    if mask & F_ENTRY_WIDTH != 0 {
        names.push("entryWidth");
    }
    if mask & F_SPECTRUM != 0 {
        names.push("entrySpectrum");
    }
    if names.is_empty() {
        "NONE".to_string()
    } else {
        names.join("+")
    }
}
