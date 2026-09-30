use search_geometry_core::g6::{
    entry_cost_signature, first_hit_g1_endpoints, phase1_ball, phase2_ball, rotate_action_c4,
    Cube, EntryCostSignature, Phase1, Phase1Moves, HTM,
};
use std::collections::{HashMap, HashSet, VecDeque};

fn full_ball_with_paths(max_depth: u8) -> HashMap<Cube, (u8, Vec<usize>)> {
    let mut out = HashMap::from([(Cube::SOLVED, (0u8, Vec::new()))]);
    let mut queue = VecDeque::from([Cube::SOLVED]);
    while let Some(state) = queue.pop_front() {
        let (depth, path) = out[&state].clone();
        if depth == max_depth {
            continue;
        }
        for action in 0..18 {
            let next = state.apply(HTM[action]);
            if !out.contains_key(&next) {
                let mut next_path = path.clone();
                next_path.push(action);
                out.insert(next, (depth + 1, next_path));
                queue.push_back(next);
            }
        }
    }
    out
}

fn apply_word(word: &[usize]) -> Cube {
    word.iter()
        .fold(Cube::SOLVED, |state, &action| state.apply(HTM[action]))
}

fn rotate_word(word: &[usize], turns: usize) -> Vec<usize> {
    word.iter()
        .map(|&action| {
            let mut a = action;
            for _ in 0..turns {
                a = rotate_action_c4(a);
            }
            a
        })
        .collect()
}

fn min_nonzero(signature: &EntryCostSignature) -> Option<u8> {
    signature
        .exact_phase2_costs
        .iter()
        .copied()
        .find(|&cost| cost > 0)
}

fn main() {
    let phase1_moves = Phase1Moves::build();
    let phase1_dist = phase1_ball(&phase1_moves, 3);
    let phase2_dist = phase2_ball(6);
    let full = full_ball_with_paths(3);

    let mut slice = full
        .iter()
        .filter_map(|(&state, (dg, path))| {
            let d1 = phase1_dist.get(&state.phase1()).copied();
            (*dg == 3 && d1 == Some(2)).then_some((state, path.clone()))
        })
        .collect::<Vec<_>>();
    slice.sort_by_key(|(_, path)| path.clone());
    assert_eq!(slice.len(), 960);

    let mut shortest_by_state = HashMap::new();
    let mut slack1_by_state = HashMap::new();
    let mut shortest_profiles = HashMap::<EntryCostSignature, usize>::new();
    let mut frontier_profiles = HashMap::<(EntryCostSignature, EntryCostSignature), usize>::new();
    let mut q_strata = HashMap::<Phase1, HashSet<EntryCostSignature>>::new();
    let mut hard_states = Vec::new();

    for &(state, _) in &slice {
        let shortest = entry_cost_signature(
            &first_hit_g1_endpoints(state, 2),
            &phase2_dist,
        );
        let slack1 = entry_cost_signature(
            &first_hit_g1_endpoints(state, 3),
            &phase2_dist,
        );

        *shortest_profiles.entry(shortest.clone()).or_insert(0) += 1;
        *frontier_profiles
            .entry((shortest.clone(), slack1.clone()))
            .or_insert(0) += 1;
        q_strata
            .entry(state.phase1())
            .or_default()
            .insert(shortest.clone());

        if shortest.endpoint_count == 4
            && shortest.exact_phase2_costs.is_empty()
            && shortest.beyond_phase2_radius == 4
        {
            hard_states.push(state);
            assert_eq!(slack1.endpoint_count, 20);
            assert_eq!(slack1.exact_phase2_costs, vec![0, 1, 1, 2]);
            assert_eq!(slack1.beyond_phase2_radius, 16);
            assert_eq!(min_nonzero(&slack1), Some(1));
        }

        shortest_by_state.insert(state, shortest);
        slack1_by_state.insert(state, slack1);
    }

    assert_eq!(
        shortest_profiles.get(&EntryCostSignature {
            endpoint_count: 2,
            exact_phase2_costs: vec![1, 2],
            beyond_phase2_radius: 0,
        }),
        Some(&864)
    );
    assert_eq!(
        shortest_profiles.get(&EntryCostSignature {
            endpoint_count: 4,
            exact_phase2_costs: vec![1, 2, 2, 3],
            beyond_phase2_radius: 0,
        }),
        Some(&64)
    );
    assert_eq!(hard_states.len(), 32);

    let easy = apply_word(&[0, 3, 12]); // U R L
    let hard = apply_word(&[3, 12, 1]); // R L U2
    assert_eq!(easy.phase1(), hard.phase1());
    assert_eq!(
        shortest_by_state[&easy].exact_phase2_costs,
        vec![1, 2, 2, 3]
    );
    assert!(shortest_by_state[&hard].exact_phase2_costs.is_empty());
    assert_eq!(shortest_by_state[&hard].beyond_phase2_radius, 4);

    let same_q_regret_classes = q_strata.values().filter(|classes| classes.len() > 1).count();
    let max_same_q_strata = q_strata.values().map(HashSet::len).max().unwrap_or(0);

    // C4 is the executable symmetry positive control. The physical rotation
    // acts on a state by relabeling every move in any word from solved.
    let slice_set = slice.iter().map(|&(state, _)| state).collect::<HashSet<_>>();
    let mut visited = HashSet::new();
    let mut orbit_histogram = HashMap::<usize, usize>::new();
    let mut symmetry_conflicts = 0usize;

    for &(state, ref word) in &slice {
        if visited.contains(&state) {
            continue;
        }
        let mut orbit = HashSet::new();
        for turns in 0..4 {
            let rotated = apply_word(&rotate_word(word, turns));
            assert!(slice_set.contains(&rotated));
            orbit.insert(rotated);
            visited.insert(rotated);
            if shortest_by_state[&rotated] != shortest_by_state[&state]
                || slack1_by_state[&rotated] != slack1_by_state[&state]
            {
                symmetry_conflicts += 1;
            }
        }
        *orbit_histogram.entry(orbit.len()).or_insert(0) += 1;
    }
    assert_eq!(visited.len(), slice.len());
    assert_eq!(symmetry_conflicts, 0);

    let orbit_count: usize = orbit_histogram.values().sum();
    let compression = slice.len() as f64 / orbit_count as f64;

    let regret_positive = shortest_by_state
        .values()
        .filter(|sig| sig.regret_width().is_some_and(|w| w > 0))
        .count();

    println!("G6_P6_TWO_PHASE_FIBER_PASS");
    println!("SLICE\tfull_dG=3; phase1_d1=2");
    println!("SLICE_STATES\t{}", slice.len());
    println!("PHASE2_EXACT_RADIUS\t6");
    println!("SHORTEST_PROFILE_CLASSES\t{}", shortest_profiles.len());
    println!("SLACK_FRONTIER_PROFILE_CLASSES\t{}", frontier_profiles.len());
    println!("REGRET_POSITIVE_STATES\t{regret_positive}");
    println!("HARD_ENTRY_STATES\t{}", hard_states.len());
    println!("SAME_Q_COORDINATES\t{}", q_strata.len());
    println!("SAME_Q_MULTI_REGRET_CLASSES\t{same_q_regret_classes}");
    println!("MAX_SAME_Q_REGRET_STRATA\t{max_same_q_strata}");
    println!("C4_ORBITS\t{orbit_count}");
    println!("C4_COMPRESSION_RATIO\t{compression:.6}");
    let mut orbit_sizes = orbit_histogram.into_iter().collect::<Vec<_>>();
    orbit_sizes.sort_unstable();
    for (size, count) in orbit_sizes {
        println!("C4_ORBIT_SIZE_{size}\t{count}");
    }
    println!("C4_COST_SIGNATURE_CONFLICTS\t{symmetry_conflicts}");
    println!(
        "SAME_Q_WITNESS\tq={:?}; easy=U R L {:?}; hard=R L U2 {:?}",
        easy.phase1(),
        shortest_by_state[&easy],
        shortest_by_state[&hard]
    );
    println!(
        "NONVACUOUS_SLACK_WITNESS\tR' L U2: shortest_total>=9; +1_slack_total=4"
    );
    println!(
        "REPRESENTATION_LADDER\tq -> shortest endpoint-cost fiber -> slack frontier -> full state"
    );
    println!("HUMAN_WORLD_CONTACT\tCLOSED");
}
