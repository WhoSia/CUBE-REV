use search_geometry_core::g6::{
    entry_cost_signature, first_hit_g1_endpoints, phase1_ball, phase2_ball, rotate_action_c4, Cube,
    EntryCostSignature, Phase1, Phase1Moves, HTM,
};
use std::collections::{HashMap, VecDeque};

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

fn word_text(word: &[usize]) -> String {
    word.iter()
        .map(|&action| MOVE_NAMES[action])
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

fn signature_key(sig: &EntryCostSignature) -> String {
    let costs = sig
        .exact_phase2_costs
        .iter()
        .map(u8::to_string)
        .collect::<Vec<_>>()
        .join(",");
    format!(
        "n{}:[{}]:gt6={}",
        sig.endpoint_count, costs, sig.beyond_phase2_radius
    )
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

fn main() {
    let phase1_moves = Phase1Moves::build();
    let phase1_dist = phase1_ball(&phase1_moves, 3);
    let phase2_dist = phase2_ball(6);
    let full = full_ball_with_paths(3);

    let mut by_q = HashMap::<Phase1, Vec<Record>>::new();
    for (&state, (dg, path)) in &full {
        if *dg != 3 || phase1_dist.get(&state.phase1()).copied() != Some(2) {
            continue;
        }
        let record = Record {
            state,
            path: path.clone(),
            shortest: entry_cost_signature(&first_hit_g1_endpoints(state, 2), &phase2_dist),
            slack1: entry_cost_signature(&first_hit_g1_endpoints(state, 3), &phase2_dist),
        };
        by_q.entry(state.phase1()).or_default().push(record);
    }
    assert_eq!(by_q.len(), 50);
    assert_eq!(by_q.values().map(Vec::len).sum::<usize>(), 960);

    let mut qs = by_q.keys().copied().collect::<Vec<_>>();
    qs.sort_by_key(|q| (q.twist, q.flip, q.slice));

    let mut pairs = Vec::<(Phase1, Record, Record)>::new();
    let mut slack_only_q = 0usize;

    for q in qs {
        let group = &by_q[&q];
        let mut shortest_classes = HashMap::<String, Vec<Record>>::new();
        for record in group {
            shortest_classes
                .entry(signature_key(&record.shortest))
                .or_default()
                .push(record.clone());
        }
        if shortest_classes.len() > 1 {
            let mut classes = shortest_classes.into_iter().collect::<Vec<_>>();
            classes.sort_by(|a, b| a.0.cmp(&b.0));
            assert_eq!(classes.len(), 2);
            for (_, states) in &mut classes {
                states.sort_by(|a, b| a.path.cmp(&b.path));
            }
            pairs.push((q, classes[0].1[0].clone(), classes[1].1[0].clone()));
        }

        let mut q_has_slack_only = false;
        let mut by_shortest_then_slack = HashMap::<String, HashMap<String, usize>>::new();
        for record in group {
            *by_shortest_then_slack
                .entry(signature_key(&record.shortest))
                .or_default()
                .entry(signature_key(&record.slack1))
                .or_insert(0) += 1;
        }
        if by_shortest_then_slack
            .values()
            .any(|slack_classes| slack_classes.len() > 1)
        {
            q_has_slack_only = true;
        }
        if q_has_slack_only {
            slack_only_q += 1;
        }
    }

    assert_eq!(pairs.len(), 2);

    let mut slack_pairs = Vec::<(Phase1, Record, Record)>::new();
    let mut q_values = by_q.keys().copied().collect::<Vec<_>>();
    q_values.sort_by_key(|q| (q.twist, q.flip, q.slice));
    for q in q_values {
        let group = &by_q[&q];
        let mut classes = HashMap::<String, HashMap<String, Vec<Record>>>::new();
        for record in group {
            classes
                .entry(signature_key(&record.shortest))
                .or_default()
                .entry(signature_key(&record.slack1))
                .or_default()
                .push(record.clone());
        }

        let mut shortest_keys = classes.keys().cloned().collect::<Vec<_>>();
        shortest_keys.sort();
        for shortest_key in shortest_keys {
            let slack_classes = classes.remove(&shortest_key).unwrap();
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
                    slack_pairs.push((q, ordered[i].1[0].clone(), ordered[j].1[0].clone()));
                }
            }
        }
    }

    let mut c4_families = HashMap::<String, Vec<usize>>::new();
    for (idx, (_, a, b)) in pairs.iter().enumerate() {
        c4_families
            .entry(pair_c4_key(&a.path, &b.path))
            .or_default()
            .push(idx + 1);
    }

    println!("G6_CLOSE_MATCHED_STATE_BANK_PASS");
    println!("SLICE_STATES\t960");
    println!("PHASE1_Q_COUNT\t{}", by_q.len());
    println!("RAW_SAME_Q_DIVERGENT_PAIRS\t{}", pairs.len());
    let mut slack_c4_families = HashMap::<String, Vec<usize>>::new();
    for (idx, (_, a, b)) in slack_pairs.iter().enumerate() {
        slack_c4_families
            .entry(pair_c4_key(&a.path, &b.path))
            .or_default()
            .push(idx + 1);
    }

    println!("C4_MATCHED_PAIR_FAMILIES\t{}", c4_families.len());
    println!("SLACK_ONLY_DIVERGENT_Q\t{slack_only_q}");
    println!("RAW_SLACK_ONLY_PAIRS\t{}", slack_pairs.len());
    println!("C4_SLACK_ONLY_FAMILIES\t{}", slack_c4_families.len());

    for (idx, (q, a, b)) in pairs.iter().enumerate() {
        assert_eq!(a.state.phase1(), b.state.phase1());
        assert_ne!(a.shortest, b.shortest);
        println!(
            "PAIR\t{}\tq={},{},{}\tA={}\tA_short={}\tA_slack1={}\tB={}\tB_short={}\tB_slack1={}\tC4_family={}",
            idx + 1,
            q.twist,
            q.flip,
            q.slice,
            word_text(&a.path),
            signature_key(&a.shortest),
            signature_key(&a.slack1),
            word_text(&b.path),
            signature_key(&b.shortest),
            signature_key(&b.slack1),
            pair_c4_key(&a.path, &b.path),
        );
    }

    let mut families = c4_families.into_iter().collect::<Vec<_>>();
    families.sort_by(|a, b| a.0.cmp(&b.0));
    for (idx, (key, members)) in families.iter().enumerate() {
        println!(
            "C4_FAMILY\t{}\tmembers={:?}\tcanonical={}",
            idx + 1,
            members,
            key
        );
    }

    for (idx, (q, a, b)) in slack_pairs.iter().enumerate() {
        assert_eq!(a.state.phase1(), b.state.phase1());
        assert_eq!(a.shortest, b.shortest);
        assert_ne!(a.slack1, b.slack1);
        println!(
            "SLACK_PAIR\t{}\tq={},{},{}\tA={}\tshort={}\tA_slack1={}\tB={}\tB_slack1={}\tC4_family={}",
            idx + 1,
            q.twist,
            q.flip,
            q.slice,
            word_text(&a.path),
            signature_key(&a.shortest),
            signature_key(&a.slack1),
            word_text(&b.path),
            signature_key(&b.slack1),
            pair_c4_key(&a.path, &b.path),
        );
    }

    let mut slack_families = slack_c4_families.into_iter().collect::<Vec<_>>();
    slack_families.sort_by(|a, b| a.0.cmp(&b.0));
    for (idx, (key, members)) in slack_families.iter().enumerate() {
        println!(
            "SLACK_C4_FAMILY\t{}\tmembers={:?}\tcanonical={}",
            idx + 1,
            members,
            key
        );
    }
}
