use search_geometry_core::g6::{
    entry_cost_signature, first_hit_g1_endpoints, phase1_ball, phase2_ball, rotate_action_c4, Cube,
    EntryCostSignature, Phase1, Phase1Moves, HTM,
};
use std::collections::{HashMap, HashSet, VecDeque};

const MOVE_NAMES: [&str; 18] = [
    "U", "U2", "U'", "R", "R2", "R'", "F", "F2", "F'", "D", "D2", "D'", "L", "L2", "L'", "B", "B2",
    "B'",
];

#[derive(Clone, Debug, Eq, PartialEq, Hash)]
struct GeoSignature {
    solution_count: u64,
    first_action_mask: u32,
    prefix2_count: usize,
}

#[derive(Clone)]
struct Candidate {
    state: Cube,
    scramble: Vec<usize>,
    dg: u8,
    q: Phase1,
    d1: u8,
    shortest: EntryCostSignature,
    slack1: EntryCostSignature,
    geo: GeoSignature,
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

fn geodesic_solution_counts(
    full: &HashMap<Cube, (u8, Vec<usize>)>,
    max_depth: u8,
) -> HashMap<Cube, u64> {
    let mut counts = HashMap::from([(Cube::SOLVED, 1u64)]);
    for depth in 1..=max_depth {
        let states = full
            .iter()
            .filter_map(|(&state, (d, _))| (*d == depth).then_some(state))
            .collect::<Vec<_>>();
        for state in states {
            let mut total = 0u64;
            for action in 0..18 {
                let next = state.apply(HTM[action]);
                if full.get(&next).is_some_and(|(d, _)| *d + 1 == depth) {
                    total += counts[&next];
                }
            }
            assert!(total > 0);
            counts.insert(state, total);
        }
    }
    counts
}

fn geodesic_signature(
    state: Cube,
    dg: u8,
    full: &HashMap<Cube, (u8, Vec<usize>)>,
    counts: &HashMap<Cube, u64>,
) -> GeoSignature {
    let mut first_action_mask = 0u32;
    let mut prefix2 = HashSet::<(usize, usize)>::new();
    for a in 0..18 {
        let s1 = state.apply(HTM[a]);
        if !full.get(&s1).is_some_and(|(d, _)| *d + 1 == dg) {
            continue;
        }
        first_action_mask |= 1u32 << a;
        if dg >= 2 {
            for b in 0..18 {
                let s2 = s1.apply(HTM[b]);
                if full.get(&s2).is_some_and(|(d, _)| *d + 2 == dg) {
                    prefix2.insert((a, b));
                }
            }
        }
    }
    GeoSignature {
        solution_count: counts[&state],
        first_action_mask,
        prefix2_count: prefix2.len(),
    }
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

fn sig_text(sig: &EntryCostSignature) -> String {
    format!(
        "n{}:{:?}:gt6={}",
        sig.endpoint_count, sig.exact_phase2_costs, sig.beyond_phase2_radius
    )
}

fn main() {
    let max_depth = 4u8;
    let full = full_ball_with_paths(max_depth);
    let counts = geodesic_solution_counts(&full, max_depth);
    let phase1_moves = Phase1Moves::build();
    let phase1_dist = phase1_ball(&phase1_moves, max_depth);
    let phase2 = phase2_ball(6);

    let depth4 = full.values().filter(|(d, _)| *d == 4).count();
    let mut groups =
        HashMap::<(u8, Phase1, EntryCostSignature, GeoSignature), Vec<Candidate>>::new();

    for (&state, (dg, scramble)) in &full {
        if *dg < 3 {
            continue;
        }
        let q = state.phase1();
        let Some(&d1) = phase1_dist.get(&q) else {
            continue;
        };
        if d1 == 0 || d1 >= *dg {
            continue;
        }
        let shortest_endpoints = first_hit_g1_endpoints(state, d1);
        if shortest_endpoints.is_empty() {
            continue;
        }
        let shortest = entry_cost_signature(&shortest_endpoints, &phase2);
        let slack1 = entry_cost_signature(&first_hit_g1_endpoints(state, d1 + 1), &phase2);
        let geo = geodesic_signature(state, *dg, &full, &counts);
        let candidate = Candidate {
            state,
            scramble: scramble.clone(),
            dg: *dg,
            q,
            d1,
            shortest: shortest.clone(),
            slack1,
            geo: geo.clone(),
        };
        groups
            .entry((*dg, q, shortest, geo))
            .or_default()
            .push(candidate);
    }

    let mut raw_pairs = Vec::<(Candidate, Candidate)>::new();
    for states in groups.values() {
        let mut by_slack = HashMap::<EntryCostSignature, Vec<Candidate>>::new();
        for state in states {
            by_slack
                .entry(state.slack1.clone())
                .or_default()
                .push(state.clone());
        }
        if by_slack.len() < 2 {
            continue;
        }
        let mut classes = by_slack.into_iter().collect::<Vec<_>>();
        classes.sort_by(|a, b| format!("{:?}", a.0).cmp(&format!("{:?}", b.0)));
        for (_, members) in &mut classes {
            members.sort_by(|a, b| a.scramble.cmp(&b.scramble));
        }
        for i in 0..classes.len() {
            for j in i + 1..classes.len() {
                raw_pairs.push((classes[i].1[0].clone(), classes[j].1[0].clone()));
            }
        }
    }

    let mut c4 = HashMap::<String, Vec<(Candidate, Candidate)>>::new();
    for pair in raw_pairs {
        c4.entry(pair_c4_key(&pair.0.scramble, &pair.1.scramble))
            .or_default()
            .push(pair);
    }

    let mut family_keys = c4.keys().cloned().collect::<Vec<_>>();
    family_keys.sort();

    println!("G7_P1_RADIUS4_MATCH_SEARCH_PASS");
    println!("FULL_BALL_RADIUS4_STATES\t{}", full.len());
    println!("DEPTH4_STATES\t{depth4}");
    println!(
        "MATCHED_RAW_PAIRS\t{}",
        c4.values().map(Vec::len).sum::<usize>()
    );
    println!("MATCHED_C4_FAMILIES\t{}", c4.len());
    println!("family\tdg\td1\tq\tsolutions\tfirst_mask\tprefix2\tA\tA_slack\tB\tB_slack");

    for (idx, key) in family_keys.iter().enumerate() {
        let mut pairs = c4[key].clone();
        pairs.sort_by(|a, b| {
            (a.0.scramble.clone(), a.1.scramble.clone())
                .cmp(&(b.0.scramble.clone(), b.1.scramble.clone()))
        });
        let (a, b) = &pairs[0];
        assert_eq!(a.dg, b.dg);
        assert_eq!(a.q, b.q);
        assert_eq!(a.d1, b.d1);
        assert_eq!(a.shortest, b.shortest);
        assert_eq!(a.geo, b.geo);
        assert_ne!(a.slack1, b.slack1);
        assert_eq!(a.state.phase1(), b.state.phase1());
        println!(
            "{}\t{}\t{}\t{},{},{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
            idx + 1,
            a.dg,
            a.d1,
            a.q.twist,
            a.q.flip,
            a.q.slice,
            a.geo.solution_count,
            a.geo.first_action_mask,
            a.geo.prefix2_count,
            word_text(&a.scramble),
            sig_text(&a.slack1),
            word_text(&b.scramble),
            sig_text(&b.slack1),
        );
    }
}
