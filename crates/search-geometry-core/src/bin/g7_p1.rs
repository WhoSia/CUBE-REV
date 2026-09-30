use search_geometry_core::g6::{
    entry_cost_signature, phase1_ball, phase2_ball, rotate_action_c4, Cube, EntryCostSignature,
    Phase1, Phase1Moves, HTM,
};
use std::collections::{HashMap, HashSet, VecDeque};

const MOVE_NAMES: [&str; 18] = [
    "U", "U2", "U'", "R", "R2", "R'", "F", "F2", "F'", "D", "D2", "D'", "L", "L2", "L'", "B", "B2",
    "B'",
];

#[derive(Clone)]
struct Record {
    state: Cube,
    path: Vec<usize>,
    shortest: EntryCostSignature,
    slack1: EntryCostSignature,
}

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

fn endpoints_by_first_action(start: Cube, steps: u8) -> HashMap<usize, HashSet<Cube>> {
    let mut frontier = vec![(start, usize::MAX)];
    for depth in 1..=steps {
        let mut next = Vec::new();
        for (state, first) in frontier {
            for action in 0..18 {
                let target = state.apply(HTM[action]);
                let first_action = if depth == 1 { action } else { first };
                if depth == steps {
                    if target.is_g1() {
                        next.push((target, first_action));
                    }
                } else if !target.is_g1() {
                    next.push((target, first_action));
                }
            }
        }
        frontier = next;
    }
    let mut out = HashMap::<usize, HashSet<Cube>>::new();
    for (state, first) in frontier {
        out.entry(first).or_default().insert(state);
    }
    out
}

fn best_cost_by_first(start: Cube, steps: u8, phase2: &HashMap<Cube, u8>) -> HashMap<usize, u8> {
    let mut out = HashMap::new();
    for (first, endpoints) in endpoints_by_first_action(start, steps) {
        if let Some(best_d2) = endpoints
            .iter()
            .filter_map(|s| phase2.get(s).copied())
            .min()
        {
            out.insert(first, steps + best_d2);
        }
    }
    out
}

fn optimal_actions(costs: &HashMap<usize, u8>) -> HashSet<usize> {
    let Some(best) = costs.values().copied().min() else {
        return HashSet::new();
    };
    costs
        .iter()
        .filter_map(|(&a, &c)| (c == best).then_some(a))
        .collect()
}

fn combined_optimal_actions(
    shortest: &HashMap<usize, u8>,
    slack: &HashMap<usize, u8>,
) -> HashSet<usize> {
    let mut merged = shortest.clone();
    for (&a, &c) in slack {
        merged
            .entry(a)
            .and_modify(|old| *old = (*old).min(c))
            .or_insert(c);
    }
    optimal_actions(&merged)
}

fn signature(endpoints: &HashSet<Cube>, phase2: &HashMap<Cube, u8>) -> EntryCostSignature {
    entry_cost_signature(endpoints, phase2)
}

fn word_text(word: &[usize]) -> String {
    word.iter()
        .map(|&a| MOVE_NAMES[a])
        .collect::<Vec<_>>()
        .join(" ")
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

fn pair_c4_key(a: &[usize], b: &[usize]) -> String {
    let mut candidates = Vec::new();
    for turns in 0..4 {
        let mut words = [
            word_text(&rotate_word(a, turns)),
            word_text(&rotate_word(b, turns)),
        ];
        words.sort();
        candidates.push(format!("{} || {}", words[0], words[1]));
    }
    candidates.sort();
    candidates[0].clone()
}

fn action_set_text(actions: &HashSet<usize>) -> String {
    let mut v = actions.iter().copied().collect::<Vec<_>>();
    v.sort_unstable();
    v.into_iter()
        .map(|a| MOVE_NAMES[a])
        .collect::<Vec<_>>()
        .join(",")
}

fn is_flexible(sig: &EntryCostSignature) -> bool {
    sig.exact_phase2_costs.first().copied() == Some(0)
}

fn full_optimal_solutions(start: Cube) -> Vec<[usize; 3]> {
    let mut out = Vec::new();
    for a in 0..18 {
        let s1 = start.apply(HTM[a]);
        for b in 0..18 {
            let s2 = s1.apply(HTM[b]);
            for c in 0..18 {
                if s2.apply(HTM[c]).is_solved() {
                    out.push([a, b, c]);
                }
            }
        }
    }
    out
}

fn full_first_actions(paths: &[[usize; 3]]) -> HashSet<usize> {
    paths.iter().map(|p| p[0]).collect()
}

fn full_prefix2(paths: &[[usize; 3]]) -> HashSet<(usize, usize)> {
    paths.iter().map(|p| (p[0], p[1])).collect()
}

fn first_g1_hit_depth(start: Cube, path: &[usize; 3]) -> u8 {
    let mut state = start;
    for (i, &action) in path.iter().enumerate() {
        state = state.apply(HTM[action]);
        if state.is_g1() {
            return (i + 1) as u8;
        }
    }
    4
}

fn g1_hit_histogram(start: Cube, paths: &[[usize; 3]]) -> [usize; 4] {
    let mut hist = [0usize; 4];
    for path in paths {
        let d = first_g1_hit_depth(start, path);
        assert!((1..=3).contains(&d));
        hist[d as usize] += 1;
    }
    hist
}

fn main() {
    let phase1_moves = Phase1Moves::build();
    let phase1_dist = phase1_ball(&phase1_moves, 3);
    let phase2 = phase2_ball(6);
    let full = full_ball_with_paths(3);

    let mut by_q = HashMap::<Phase1, Vec<Record>>::new();
    for (&state, (dg, path)) in &full {
        if *dg != 3 || phase1_dist.get(&state.phase1()).copied() != Some(2) {
            continue;
        }
        let shortest_endpoints = endpoints_by_first_action(state, 2)
            .into_values()
            .flatten()
            .collect::<HashSet<_>>();
        let slack_endpoints = endpoints_by_first_action(state, 3)
            .into_values()
            .flatten()
            .collect::<HashSet<_>>();
        let record = Record {
            state,
            path: path.clone(),
            shortest: signature(&shortest_endpoints, &phase2),
            slack1: signature(&slack_endpoints, &phase2),
        };
        by_q.entry(state.phase1()).or_default().push(record);
    }

    let mut raw_pairs = Vec::<(Phase1, Record, Record)>::new();
    let mut qs = by_q.keys().copied().collect::<Vec<_>>();
    qs.sort_by_key(|q| (q.twist, q.flip, q.slice));

    for q in qs {
        let group = &by_q[&q];
        let mut classes = HashMap::<String, HashMap<String, Vec<Record>>>::new();
        for r in group {
            let short_key = format!("{:?}", r.shortest);
            let slack_key = format!("{:?}", r.slack1);
            classes
                .entry(short_key)
                .or_default()
                .entry(slack_key)
                .or_default()
                .push(r.clone());
        }
        for slack_classes in classes.into_values() {
            if slack_classes.len() < 2 {
                continue;
            }
            let mut ordered = slack_classes.into_iter().collect::<Vec<_>>();
            ordered.sort_by(|a, b| a.0.cmp(&b.0));
            for (_, states) in &mut ordered {
                states.sort_by(|a, b| a.path.cmp(&b.path));
            }
            for i in 0..ordered.len() {
                for j in i + 1..ordered.len() {
                    raw_pairs.push((q, ordered[i].1[0].clone(), ordered[j].1[0].clone()));
                }
            }
        }
    }
    assert_eq!(raw_pairs.len(), 48);

    let mut families = HashMap::<String, Vec<(Phase1, Record, Record)>>::new();
    for pair in raw_pairs {
        let key = pair_c4_key(&pair.1.path, &pair.2.path);
        families.entry(key).or_default().push(pair);
    }
    assert_eq!(families.len(), 24);

    let mut family_keys = families.keys().cloned().collect::<Vec<_>>();
    family_keys.sort();

    let mut families_with_new_flex_actions = 0usize;
    let mut families_with_policy_difference = 0usize;
    let mut full_solution_count_match = 0usize;
    let mut full_first_action_set_match = 0usize;
    let mut full_prefix2_count_match = 0usize;
    let mut strong_geodesic_match = 0usize;
    let mut g1_hit_distribution_difference = 0usize;

    println!("G7_P1_POLICY_BANK_PASS");
    println!("C4_FAMILIES\t{}", family_keys.len());
    println!("family_id\tq\tflexible_scramble\trigid_scramble\tshort_opt_flex\tcombined_opt_flex\tnew_slack_opt_flex\tshort_opt_rigid\tcombined_opt_rigid\tnew_slack_opt_rigid\tfull_solutions_flex\tfull_solutions_rigid\tfull_first_flex\tfull_first_rigid\tprefix2_flex\tprefix2_rigid\tg1hit2_flex\tg1hit3_flex\tg1hit2_rigid\tg1hit3_rigid");

    for (idx, key) in family_keys.iter().enumerate() {
        let mut candidates = families[key].clone();
        candidates.sort_by(|a, b| {
            (a.1.path.clone(), a.2.path.clone()).cmp(&(b.1.path.clone(), b.2.path.clone()))
        });
        let (q, a, b) = candidates[0].clone();
        let (flex, rigid) = if is_flexible(&a.slack1) {
            (a, b)
        } else {
            (b, a)
        };
        assert!(is_flexible(&flex.slack1));
        assert!(!is_flexible(&rigid.slack1));
        assert_eq!(flex.shortest, rigid.shortest);

        let flex_short_cost = best_cost_by_first(flex.state, 2, &phase2);
        let flex_slack_cost = best_cost_by_first(flex.state, 3, &phase2);
        let rigid_short_cost = best_cost_by_first(rigid.state, 2, &phase2);
        let rigid_slack_cost = best_cost_by_first(rigid.state, 3, &phase2);

        let flex_short = optimal_actions(&flex_short_cost);
        let flex_combined = combined_optimal_actions(&flex_short_cost, &flex_slack_cost);
        let rigid_short = optimal_actions(&rigid_short_cost);
        let rigid_combined = combined_optimal_actions(&rigid_short_cost, &rigid_slack_cost);

        let flex_new = flex_combined
            .difference(&flex_short)
            .copied()
            .collect::<HashSet<_>>();
        let rigid_new = rigid_combined
            .difference(&rigid_short)
            .copied()
            .collect::<HashSet<_>>();

        if !flex_new.is_empty() {
            families_with_new_flex_actions += 1;
        }
        if flex_combined != rigid_combined {
            families_with_policy_difference += 1;
        }

        let flex_full = full_optimal_solutions(flex.state);
        let rigid_full = full_optimal_solutions(rigid.state);
        let flex_full_first = full_first_actions(&flex_full);
        let rigid_full_first = full_first_actions(&rigid_full);
        let flex_prefix2 = full_prefix2(&flex_full);
        let rigid_prefix2 = full_prefix2(&rigid_full);
        let flex_g1 = g1_hit_histogram(flex.state, &flex_full);
        let rigid_g1 = g1_hit_histogram(rigid.state, &rigid_full);

        let count_match = flex_full.len() == rigid_full.len();
        let first_match = flex_full_first == rigid_full_first;
        let prefix_count_match = flex_prefix2.len() == rigid_prefix2.len();
        if count_match {
            full_solution_count_match += 1;
        }
        if first_match {
            full_first_action_set_match += 1;
        }
        if prefix_count_match {
            full_prefix2_count_match += 1;
        }
        if count_match && first_match && prefix_count_match {
            strong_geodesic_match += 1;
        }
        if flex_g1 != rigid_g1 {
            g1_hit_distribution_difference += 1;
        }

        println!(
            "{}\t{},{},{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
            idx + 1,
            q.twist,
            q.flip,
            q.slice,
            word_text(&flex.path),
            word_text(&rigid.path),
            action_set_text(&flex_short),
            action_set_text(&flex_combined),
            action_set_text(&flex_new),
            action_set_text(&rigid_short),
            action_set_text(&rigid_combined),
            action_set_text(&rigid_new),
            flex_full.len(),
            rigid_full.len(),
            action_set_text(&flex_full_first),
            action_set_text(&rigid_full_first),
            flex_prefix2.len(),
            rigid_prefix2.len(),
            flex_g1[2],
            flex_g1[3],
            rigid_g1[2],
            rigid_g1[3],
        );
    }

    println!(
        "FAMILIES_WITH_NEW_FLEX_OPTIMAL_FIRST_ACTIONS\t{}",
        families_with_new_flex_actions
    );
    println!(
        "FAMILIES_WITH_COMBINED_POLICY_DIFFERENCE\t{}",
        families_with_policy_difference
    );
    println!("FULL_SOLUTION_COUNT_MATCH_FAMILIES\t{}", full_solution_count_match);
    println!(
        "FULL_FIRST_ACTION_SET_MATCH_FAMILIES\t{}",
        full_first_action_set_match
    );
    println!(
        "FULL_PREFIX2_COUNT_MATCH_FAMILIES\t{}",
        full_prefix2_count_match
    );
    println!("STRONG_GEODESIC_MATCH_FAMILIES\t{}", strong_geodesic_match);
    println!(
        "G1_HIT_DISTRIBUTION_DIFFERENCE_FAMILIES\t{}",
        g1_hit_distribution_difference
    );
    println!("RETROSPECTIVE_HUMAN_LANE\tSOURCE_BYTES_UNAVAILABLE");
    println!("NEW_HUMAN_COLLECTION\tHOLD_PENDING_INSTRUMENT_AND_LAUNCH_AUTHORITY");
}
