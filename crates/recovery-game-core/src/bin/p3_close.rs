use recovery_game_core::{
    bit_query_parity_belief, bit_query_protocol, minimal_query_depth, ActionProtocol,
    BitQueryObservation, BitQueryState, Collapse, CollapseChannel, FiniteDynamics,
    HypothesisRecord, ObservationChannel, ResourceVector, RotateProbe, TargetCollapsingMerge,
    TargetLosslessCollapse,
};
use std::collections::{BTreeMap, BTreeSet, VecDeque};

#[derive(Clone, Debug, Eq, PartialEq, Ord, PartialOrd)]
enum LiveState {
    Live(BitQueryState),
    JunkA,
    JunkB,
    Sink,
}

struct LiveIrreversibleDynamics {
    n: u8,
}

impl FiniteDynamics for LiveIrreversibleDynamics {
    type State = LiveState;
    type Action = RotateProbe;

    fn step(&self, state: &Self::State, action: &Self::Action) -> Self::State {
        match state {
            LiveState::Live(s) => LiveState::Live(BitQueryState {
                bits: s.bits,
                pointer: (s.pointer + action.0) % self.n,
            }),
            LiveState::JunkA | LiveState::JunkB | LiveState::Sink => LiveState::Sink,
        }
    }
}

#[derive(Clone, Debug, Eq, PartialEq, Ord, PartialOrd)]
enum LiveObs {
    Bit(u8, u8),
    Junk,
}

struct LiveObservation;

impl ObservationChannel<LiveState> for LiveObservation {
    type Observation = LiveObs;

    fn observe(&self, state: &LiveState) -> Self::Observation {
        match state {
            LiveState::Live(s) => LiveObs::Bit(s.pointer, ((s.bits >> s.pointer) & 1) as u8),
            _ => LiveObs::Junk,
        }
    }
}

fn li_parity_belief(n: u8) -> Vec<HypothesisRecord<LiveState, u8>> {
    (0..(1u16 << n))
        .map(|bits| HypothesisRecord {
            root_hypothesis_id: bits as u32,
            current_state: LiveState::Live(BitQueryState { bits, pointer: 0 }),
            target_value: (bits.count_ones() & 1) as u8,
        })
        .collect()
}

fn choose2(x: u64) -> u64 {
    x.saturating_mul(x.saturating_sub(1)) / 2
}

fn hm_exact_ambiguity(n: u8, p: u8) -> u64 {
    let blocks = 1u64 << p;
    let block_size = 1u64 << (n - p);
    blocks * choose2(block_size)
}

fn hm_parity_ambiguity(n: u8, p: u8) -> u64 {
    if p == n {
        0
    } else {
        1u64 << (2 * n - p - 2)
    }
}

#[derive(Clone)]
struct PublishedFsm {
    states: Vec<u8>,
    inputs: Vec<u8>,
    transitions: BTreeMap<(u8, u8, u8), u8>,
}

impl PublishedFsm {
    fn succ(&self, state: u8, input: u8, output: u8) -> Option<u8> {
        self.transitions.get(&(state, input, output)).copied()
    }

    fn pair_successors(&self, pair: (u8, u8), input: u8) -> BTreeSet<(u8, u8)> {
        let mut out = BTreeSet::new();
        for output in 1..=2 {
            if let (Some(a), Some(b)) = (
                self.succ(pair.0, input, output),
                self.succ(pair.1, input, output),
            ) {
                if a != b {
                    out.insert(if a < b { (a, b) } else { (b, a) });
                }
            }
        }
        out
    }

    fn pair_is_adaptively_homing(&self, start: (u8, u8)) -> bool {
        let mut live = BTreeSet::new();
        for i in 0..self.states.len() {
            for j in i + 1..self.states.len() {
                live.insert((self.states[i], self.states[j]));
            }
        }

        loop {
            let remove: Vec<_> = live
                .iter()
                .copied()
                .filter(|pair| {
                    self.inputs.iter().any(|input| {
                        self.pair_successors(*pair, *input)
                            .iter()
                            .all(|next| !live.contains(next))
                    })
                })
                .collect();
            if remove.is_empty() {
                break;
            }
            for pair in remove {
                live.remove(&pair);
            }
        }
        !live.contains(&start)
    }
}

fn kushik_yevtushenko_table1() -> PublishedFsm {
    let mut t = BTreeMap::new();
    let rows = [
        (1, 1, 1, 1),
        (1, 1, 2, 3),
        (2, 1, 2, 2),
        (2, 1, 1, 3),
        (3, 1, 2, 2),
        (1, 2, 1, 1),
        (1, 2, 2, 2),
        (2, 2, 1, 3),
        (2, 2, 2, 3),
        (3, 2, 1, 1),
        (1, 3, 1, 1),
        (1, 3, 2, 3),
        (2, 3, 1, 2),
        (3, 3, 2, 1),
    ];
    for (state, input, output, next) in rows {
        t.insert((state, input, output), next);
    }
    PublishedFsm {
        states: vec![1, 2, 3],
        inputs: vec![1, 2, 3],
        transitions: t,
    }
}

fn subsets_rec(
    start: usize,
    n_exclusive: usize,
    k: usize,
    current: &mut Vec<usize>,
    out: &mut Vec<Vec<usize>>,
) {
    if current.len() == k {
        out.push(current.clone());
        return;
    }
    for value in start..n_exclusive {
        current.push(value);
        subsets_rec(value + 1, n_exclusive, k, current, out);
        current.pop();
    }
}

fn subsets(n_exclusive: usize, k: usize) -> Vec<Vec<usize>> {
    let mut out = Vec::new();
    subsets_rec(0, n_exclusive, k, &mut Vec::new(), &mut out);
    out
}

fn max_order_perm(k: usize) -> (Vec<usize>, usize) {
    match k {
        2 => (vec![1, 0], 2),
        3 => (vec![1, 2, 0], 3),
        _ => panic!("P3 frozen donor grid only authorizes k=2 or k=3"),
    }
}

fn panteleev_generators(n: usize, k: usize) -> (Vec<Vec<usize>>, usize) {
    let ds = subsets(n - 1, k);
    let (perm, order) = max_order_perm(k);
    let sink = n - 1;
    let mut generators = Vec::new();

    for i in 0..ds.len() {
        let mut map = vec![sink; n];
        for j in 0..k {
            map[ds[i][j]] = if i + 1 < ds.len() {
                ds[i + 1][j]
            } else {
                ds[0][perm[j]]
            };
        }
        map[sink] = sink;
        generators.push(map);
    }
    (generators, order)
}

fn apply_after(current: &[usize], generator: &[usize]) -> Vec<usize> {
    current.iter().map(|q| generator[*q]).collect()
}

fn cycle_target(n: usize, generators: &[Vec<usize>], repeats: usize) -> Vec<usize> {
    let mut transform: Vec<_> = (0..n).collect();
    for _ in 0..repeats {
        for generator in generators {
            transform = apply_after(&transform, generator);
        }
    }
    transform
}

fn shortest_transform_length(
    n: usize,
    generators: &[Vec<usize>],
    target: &[usize],
) -> Option<usize> {
    let identity: Vec<_> = (0..n).collect();
    if identity == target {
        return Some(0);
    }
    let mut seen = BTreeMap::new();
    let mut queue = VecDeque::new();
    seen.insert(identity.clone(), 0usize);
    queue.push_back(identity);

    while let Some(current) = queue.pop_front() {
        let depth = seen[&current];
        for generator in generators {
            let next = apply_after(&current, generator);
            if seen.contains_key(&next) {
                continue;
            }
            if next == target {
                return Some(depth + 1);
            }
            seen.insert(next.clone(), depth + 1);
            queue.push_back(next);
        }
    }
    None
}

fn panteleev_case(n: usize, k: usize) -> (usize, usize) {
    let (generators, order) = panteleev_generators(n, k);
    let target = cycle_target(n, &generators, order - 1);
    let exact = shortest_transform_length(n, &generators, &target)
        .expect("finite transformation semigroup must contain generated target");
    let expected = generators.len() * (order - 1);
    (exact, expected)
}

fn print_row(fields: [&str; 12]) {
    println!("{}", fields.join("\t"));
}

fn main() {
    print_row([
        "kind",
        "family",
        "n",
        "p",
        "target",
        "recoverable",
        "depth",
        "memory",
        "ambiguity",
        "external",
        "internal",
        "note",
    ]);

    for n in 1u8..=12 {
        let ns = n.to_string();
        print_row([
            "grid",
            "B",
            &ns,
            "",
            "exact",
            "true",
            &ns,
            &ns,
            "",
            "",
            "",
            "analytic_law",
        ]);
        print_row([
            "grid",
            "B",
            &ns,
            "",
            "parity",
            "true",
            &ns,
            "1",
            "",
            "",
            "",
            "analytic_law",
        ]);
        print_row([
            "grid",
            "LI",
            &ns,
            "",
            "parity",
            "true",
            &ns,
            "1",
            "",
            "",
            "",
            "matched_live_support",
        ]);
    }

    for n in 2u8..=12 {
        let ns = n.to_string();
        print_row([
            "grid",
            "TL",
            &ns,
            "",
            "parity",
            "true",
            "1",
            "1",
            "",
            "",
            "",
            "target_lossless_merge",
        ]);
        print_row([
            "grid",
            "M2O",
            &ns,
            "",
            "parity",
            "false",
            "inf",
            "",
            "",
            "",
            "",
            "PERMANENT_TARGET_COLLISION",
        ]);

        let raw_internal = (n as u32 - 1).to_string();
        print_row([
            "grid",
            "E",
            &ns,
            "",
            "parity",
            "true",
            "0",
            "",
            "0",
            "0",
            &raw_internal,
            "raw",
        ]);
        print_row([
            "grid",
            "E",
            &ns,
            "",
            "parity",
            "true",
            "0",
            "",
            "0",
            "1",
            "0",
            "normalized",
        ]);

        for p in 0u8..=n {
            let ps = p.to_string();
            let exact = hm_exact_ambiguity(n, p);
            let parity = hm_parity_ambiguity(n, p);
            let exacts = exact.to_string();
            let paritys = parity.to_string();
            print_row([
                "grid",
                "HM",
                &ns,
                &ps,
                "exact",
                if exact == 0 { "true" } else { "false" },
                if exact == 0 { "0" } else { "inf" },
                "",
                &exacts,
                "",
                "",
                "component_channel;joint_ambiguity=0",
            ]);
            print_row([
                "grid",
                "HM",
                &ns,
                &ps,
                "parity",
                if parity == 0 { "true" } else { "false" },
                if parity == 0 { "0" } else { "inf" },
                "",
                &paritys,
                "",
                "",
                "component_channel;joint_ambiguity=0",
            ]);
        }
    }

    for (source, target, verdict, note) in [
        (
            "B",
            "LI",
            "PASS",
            "transcript_partition+dstar+pareto;off_support_global_dynamics_ignored",
        ),
        (
            "B_exact",
            "B_parity",
            "PASS_PARTIAL",
            "dstar;memory_transport_fail_n_vs_1",
        ),
        (
            "B_parity",
            "TL_parity",
            "PASS_PARTIAL",
            "finite_recoverability;dstar_transport_fail_n_vs_1",
        ),
        (
            "TL_parity",
            "M2O_parity",
            "FAIL",
            "recoverability;target_distinction_destroyed",
        ),
        (
            "E_raw",
            "E_normalized",
            "PASS_PARTIAL",
            "target_sufficiency;resource_vector_nontransport",
        ),
    ] {
        print_row([
            "transport",
            source,
            "",
            "",
            target,
            verdict,
            "",
            "",
            "",
            "",
            "",
            note,
        ]);
    }

    let fsm = kushik_yevtushenko_table1();
    let all_homing = [(1, 2), (1, 3), (2, 3)]
        .into_iter()
        .all(|pair| fsm.pair_is_adaptively_homing(pair));
    print_row([
        "hard",
        "A_HOME_KY2015_TABLE1",
        "3",
        "",
        "adaptive_homing",
        if all_homing { "true" } else { "false" },
        "",
        "",
        "",
        "",
        "",
        "published_table_reconstructed",
    ]);

    for (n, k) in [(4usize, 2usize), (5, 2), (5, 3), (6, 3)] {
        let (exact, expected) = panteleev_case(n, k);
        let ns = n.to_string();
        let ks = k.to_string();
        let ds = exact.to_string();
        let note = format!("expected={expected};not_a_direct_PDS_instance");
        print_row([
            "hard",
            "A_TS_PANTELEEV_LEMMA8_DONOR",
            &ns,
            &ks,
            "shortest_transformation_word",
            if exact == expected { "true" } else { "false" },
            &ds,
            "",
            "",
            "",
            "",
            &note,
        ]);
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use recovery_game_core::{
        bit_query_exact_belief, collapse_exact_belief, collapse_parity_belief, pareto_frontier,
        BitQueryDynamics,
    };

    #[test]
    fn li_matches_b_on_live_support() {
        for n in 1u8..=5 {
            let protocol = bit_query_protocol(n);
            let b = minimal_query_depth(
                &BitQueryDynamics { n },
                &BitQueryObservation,
                &protocol,
                &bit_query_parity_belief(n),
                n as usize,
            );
            let li = minimal_query_depth(
                &LiveIrreversibleDynamics { n },
                &LiveObservation,
                &protocol,
                &li_parity_belief(n),
                n as usize,
            );
            assert_eq!(b, li);
            assert_eq!(li, Some(n as usize));
        }

        let dynamics = LiveIrreversibleDynamics { n: 2 };
        assert_eq!(
            dynamics.step(&LiveState::JunkA, &RotateProbe(0)),
            dynamics.step(&LiveState::JunkB, &RotateProbe(0))
        );
    }

    #[test]
    fn published_adaptive_homing_example_reproduces_table2_edges() {
        let fsm = kushik_yevtushenko_table1();
        assert_eq!(
            fsm.pair_successors((1, 2), 1),
            BTreeSet::from([(1, 3), (2, 3)])
        );
        assert_eq!(fsm.pair_successors((1, 2), 3), BTreeSet::from([(1, 2)]));
        for pair in [(1, 2), (1, 3), (2, 3)] {
            assert!(fsm.pair_is_adaptively_homing(pair));
        }
    }

    #[test]
    fn panteleev_finite_donor_matches_lemma8_word_lower_bound() {
        for (n, k) in [(4usize, 2usize), (5, 2), (5, 3), (6, 3)] {
            let (exact, expected) = panteleev_case(n, k);
            assert_eq!(exact, expected, "n={n}, k={k}");
        }
    }

    #[test]
    fn transport_matrix_core_contrasts_execute() {
        for n in 2u8..=5 {
            let b_exact = minimal_query_depth(
                &BitQueryDynamics { n },
                &BitQueryObservation,
                &bit_query_protocol(n),
                &bit_query_exact_belief(n),
                n as usize,
            );
            let b_parity = minimal_query_depth(
                &BitQueryDynamics { n },
                &BitQueryObservation,
                &bit_query_protocol(n),
                &bit_query_parity_belief(n),
                n as usize,
            );
            assert_eq!(b_exact, b_parity);

            let tl = minimal_query_depth(
                &TargetLosslessCollapse,
                &CollapseChannel,
                &ActionProtocol::new(vec![Collapse]),
                &collapse_parity_belief(n),
                1,
            );
            let tl_exact = minimal_query_depth(
                &TargetLosslessCollapse,
                &CollapseChannel,
                &ActionProtocol::new(vec![Collapse]),
                &collapse_exact_belief(n),
                1,
            );
            let m2o = minimal_query_depth(
                &TargetCollapsingMerge,
                &CollapseChannel,
                &ActionProtocol::new(vec![Collapse]),
                &collapse_parity_belief(n),
                2,
            );
            assert_eq!(tl, Some(1));
            assert_eq!(tl_exact, None);
            assert_eq!(m2o, None);

            let raw = ResourceVector {
                query: 0,
                external_actions: 0,
                internal_ops: n as u32 - 1,
                memory_bits: 0,
            };
            let normalized = ResourceVector {
                query: 0,
                external_actions: 1,
                internal_ops: 0,
                memory_bits: 0,
            };
            assert_eq!(pareto_frontier(vec![raw, normalized]).len(), 2);
        }
    }

    #[test]
    fn frozen_grid_cardinality_is_256() {
        let hm: usize = (2usize..=12).map(|n| 2 * (n + 1)).sum();
        assert_eq!(24 + 12 + 11 + 11 + 22 + hm, 256);
    }
}
