//! Exact finite recovery-game primitives for CUBE-REV Generation V.
//!
//! Authority ceiling:
//! - structural / finite-world recovery only;
//! - no human-behavior claim;
//! - no cryptographic hardness claim;
//! - no R2 oracle-equivalence claim.

use std::collections::BTreeMap;

pub trait FiniteDynamics {
    type State: Clone + Eq + Ord;
    type Action: Clone + Eq + Ord;

    fn step(&self, state: &Self::State, action: &Self::Action) -> Self::State;
}

pub trait ObservationChannel<S> {
    type Observation: Clone + Eq + Ord;

    fn observe(&self, state: &S) -> Self::Observation;
}

#[derive(Clone, Debug, Eq, PartialEq, Ord, PartialOrd)]
pub struct HypothesisRecord<S, T> {
    pub root_hypothesis_id: u32,
    pub current_state: S,
    pub target_value: T,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ActionProtocol<A> {
    pub actions: Vec<A>,
}

impl<A> ActionProtocol<A> {
    pub fn new(actions: Vec<A>) -> Self {
        Self { actions }
    }
}

pub fn target_is_constant<S, T: Eq>(belief: &[HypothesisRecord<S, T>]) -> bool {
    match belief.first() {
        None => true,
        Some(first) => belief
            .iter()
            .all(|h| h.target_value == first.target_value),
    }
}

pub fn permanent_target_collision<S: Eq, T: Eq>(
    belief: &[HypothesisRecord<S, T>],
) -> bool {
    for (i, left) in belief.iter().enumerate() {
        for right in &belief[i + 1..] {
            if left.current_state == right.current_state
                && left.target_value != right.target_value
            {
                return true;
            }
        }
    }
    false
}

pub fn ambiguity_pairs<K: Ord, T: Eq>(
    pairs: impl IntoIterator<Item = (K, T)>,
) -> u64 {
    let mut groups: BTreeMap<K, Vec<T>> = BTreeMap::new();
    for (key, target) in pairs {
        groups.entry(key).or_default().push(target);
    }

    let mut total = 0u64;
    for targets in groups.values() {
        for i in 0..targets.len() {
            for j in i + 1..targets.len() {
                if targets[i] != targets[j] {
                    total += 1;
                }
            }
        }
    }
    total
}

pub fn minimal_query_depth<D, O, T>(
    dynamics: &D,
    observation: &O,
    protocol: &ActionProtocol<D::Action>,
    belief: &[HypothesisRecord<D::State, T>],
    max_depth: usize,
) -> Option<usize>
where
    D: FiniteDynamics,
    D::State: Ord,
    O: ObservationChannel<D::State>,
    T: Clone + Eq + Ord,
{
    for depth in 0..=max_depth {
        let mut memo = BTreeMap::new();
        if solvable_within(
            dynamics,
            observation,
            protocol,
            belief,
            depth,
            &mut memo,
        ) {
            return Some(depth);
        }
    }
    None
}

fn solvable_within<D, O, T>(
    dynamics: &D,
    observation: &O,
    protocol: &ActionProtocol<D::Action>,
    belief: &[HypothesisRecord<D::State, T>],
    depth: usize,
    memo: &mut BTreeMap<(Vec<HypothesisRecord<D::State, T>>, usize), bool>,
) -> bool
where
    D: FiniteDynamics,
    D::State: Ord,
    O: ObservationChannel<D::State>,
    T: Clone + Eq + Ord,
{
    if target_is_constant(belief) {
        return true;
    }
    if permanent_target_collision(belief) || depth == 0 {
        return false;
    }

    let mut key_belief = belief.to_vec();
    key_belief.sort_by_key(|h| h.root_hypothesis_id);
    let key = (key_belief, depth);
    if let Some(cached) = memo.get(&key) {
        return *cached;
    }

    for action in &protocol.actions {
        let mut children: BTreeMap<O::Observation, Vec<HypothesisRecord<D::State, T>>> =
            BTreeMap::new();

        for h in belief {
            let next_state = dynamics.step(&h.current_state, action);
            let obs = observation.observe(&next_state);
            children.entry(obs).or_default().push(HypothesisRecord {
                root_hypothesis_id: h.root_hypothesis_id,
                current_state: next_state,
                target_value: h.target_value.clone(),
            });
        }

        if children.values().all(|child| {
            solvable_within(
                dynamics,
                observation,
                protocol,
                child,
                depth - 1,
                memo,
            )
        }) {
            memo.insert(key, true);
            return true;
        }
    }

    memo.insert(key, false);
    false
}

pub fn canonical_rgs(labels: &[usize]) -> Vec<usize> {
    let mut map = BTreeMap::new();
    let mut next = 0usize;
    labels
        .iter()
        .map(|label| {
            *map.entry(*label).or_insert_with(|| {
                let current = next;
                next += 1;
                current
            })
        })
        .collect()
}

pub fn enumerate_rgs(n: usize) -> Vec<Vec<usize>> {
    if n == 0 {
        return vec![Vec::new()];
    }
    let mut out = Vec::new();
    let mut current = vec![0usize];
    enumerate_rgs_rec(n, &mut current, &mut out);
    out
}

fn enumerate_rgs_rec(n: usize, current: &mut Vec<usize>, out: &mut Vec<Vec<usize>>) {
    if current.len() == n {
        out.push(current.clone());
        return;
    }
    let max_label = current.iter().copied().max().unwrap_or(0);
    for label in 0..=max_label + 1 {
        current.push(label);
        enumerate_rgs_rec(n, current, out);
        current.pop();
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq, Ord, PartialOrd)]
pub struct ResourceVector {
    pub query: u32,
    pub external_actions: u32,
    pub internal_ops: u32,
    pub memory_bits: u32,
}

impl ResourceVector {
    pub fn dominates(self, other: Self) -> bool {
        let weak = self.query <= other.query
            && self.external_actions <= other.external_actions
            && self.internal_ops <= other.internal_ops
            && self.memory_bits <= other.memory_bits;
        let strict = self != other;
        weak && strict
    }
}

pub fn pareto_frontier(mut vectors: Vec<ResourceVector>) -> Vec<ResourceVector> {
    vectors.sort();
    vectors.dedup();
    let snapshot = vectors.clone();
    vectors
        .into_iter()
        .filter(|candidate| {
            !snapshot
                .iter()
                .copied()
                .any(|other| other.dominates(*candidate))
        })
        .collect()
}

#[derive(Clone, Debug, Eq, PartialEq, Ord, PartialOrd)]
pub struct BitQueryState {
    pub bits: u16,
    pub pointer: u8,
}

#[derive(Clone, Debug, Eq, PartialEq, Ord, PartialOrd)]
pub struct RotateProbe(pub u8);

#[derive(Clone, Debug)]
pub struct BitQueryDynamics {
    pub n: u8,
}

impl FiniteDynamics for BitQueryDynamics {
    type State = BitQueryState;
    type Action = RotateProbe;

    fn step(&self, state: &Self::State, action: &Self::Action) -> Self::State {
        assert!(self.n > 0);
        Self::State {
            bits: state.bits,
            pointer: (state.pointer + action.0) % self.n,
        }
    }
}

#[derive(Clone, Debug)]
pub struct BitQueryObservation;

impl ObservationChannel<BitQueryState> for BitQueryObservation {
    type Observation = (u8, u8);

    fn observe(&self, state: &BitQueryState) -> Self::Observation {
        (state.pointer, ((state.bits >> state.pointer) & 1) as u8)
    }
}

pub fn bit_query_protocol(n: u8) -> ActionProtocol<RotateProbe> {
    ActionProtocol::new((0..n).map(RotateProbe).collect())
}

pub fn bit_query_exact_belief(n: u8) -> Vec<HypothesisRecord<BitQueryState, u16>> {
    assert!(n > 0 && n <= 15);
    (0..(1u16 << n))
        .map(|bits| HypothesisRecord {
            root_hypothesis_id: bits as u32,
            current_state: BitQueryState { bits, pointer: 0 },
            target_value: bits,
        })
        .collect()
}

pub fn bit_query_parity_belief(n: u8) -> Vec<HypothesisRecord<BitQueryState, u8>> {
    assert!(n > 0 && n <= 15);
    (0..(1u16 << n))
        .map(|bits| HypothesisRecord {
            root_hypothesis_id: bits as u32,
            current_state: BitQueryState { bits, pointer: 0 },
            target_value: (bits.count_ones() & 1) as u8,
        })
        .collect()
}

#[derive(Clone, Debug, Eq, PartialEq, Ord, PartialOrd)]
pub enum CollapseState {
    Root(u16),
    ParitySink(u8),
    CommonSink,
}

#[derive(Clone, Debug, Eq, PartialEq, Ord, PartialOrd)]
pub enum CollapseObservation {
    Hidden,
    Parity(u8),
    Common,
}

#[derive(Clone, Debug, Eq, PartialEq, Ord, PartialOrd)]
pub struct Collapse;

#[derive(Clone, Debug)]
pub struct TargetLosslessCollapse;

impl FiniteDynamics for TargetLosslessCollapse {
    type State = CollapseState;
    type Action = Collapse;

    fn step(&self, state: &Self::State, _action: &Self::Action) -> Self::State {
        match state {
            CollapseState::Root(bits) => CollapseState::ParitySink(
                (bits.count_ones() & 1) as u8,
            ),
            sink => sink.clone(),
        }
    }
}

#[derive(Clone, Debug)]
pub struct TargetCollapsingMerge;

impl FiniteDynamics for TargetCollapsingMerge {
    type State = CollapseState;
    type Action = Collapse;

    fn step(&self, state: &Self::State, _action: &Self::Action) -> Self::State {
        match state {
            CollapseState::Root(_) => CollapseState::CommonSink,
            sink => sink.clone(),
        }
    }
}

#[derive(Clone, Debug)]
pub struct CollapseChannel;

impl ObservationChannel<CollapseState> for CollapseChannel {
    type Observation = CollapseObservation;

    fn observe(&self, state: &CollapseState) -> Self::Observation {
        match state {
            CollapseState::Root(_) => CollapseObservation::Hidden,
            CollapseState::ParitySink(value) => CollapseObservation::Parity(*value),
            CollapseState::CommonSink => CollapseObservation::Common,
        }
    }
}

pub fn collapse_parity_belief(n: u8) -> Vec<HypothesisRecord<CollapseState, u8>> {
    assert!(n > 0 && n <= 15);
    (0..(1u16 << n))
        .map(|bits| HypothesisRecord {
            root_hypothesis_id: bits as u32,
            current_state: CollapseState::Root(bits),
            target_value: (bits.count_ones() & 1) as u8,
        })
        .collect()
}

pub fn collapse_exact_belief(n: u8) -> Vec<HypothesisRecord<CollapseState, u16>> {
    assert!(n > 0 && n <= 15);
    (0..(1u16 << n))
        .map(|bits| HypothesisRecord {
            root_hypothesis_id: bits as u32,
            current_state: CollapseState::Root(bits),
            target_value: bits,
        })
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn rgs_counts_match_bell_numbers() {
        assert_eq!(enumerate_rgs(4).len(), 15);
        assert_eq!(enumerate_rgs(8).len(), 4_140);
        assert_eq!(canonical_rgs(&[7, 7, 4, 9, 4]), vec![0, 0, 1, 2, 1]);
    }

    #[test]
    fn bit_query_exact_and_parity_need_n_queries() {
        for n in 1..=4 {
            let dynamics = BitQueryDynamics { n };
            let observation = BitQueryObservation;
            let protocol = bit_query_protocol(n);
            let exact = bit_query_exact_belief(n);
            let parity = bit_query_parity_belief(n);

            assert_eq!(
                minimal_query_depth(
                    &dynamics,
                    &observation,
                    &protocol,
                    &exact,
                    n as usize,
                ),
                Some(n as usize)
            );
            assert_eq!(
                minimal_query_depth(
                    &dynamics,
                    &observation,
                    &protocol,
                    &parity,
                    n as usize,
                ),
                Some(n as usize)
            );
        }
    }

    #[test]
    fn target_lossless_collapse_recovers_parity_but_not_exact_state() {
        let dynamics = TargetLosslessCollapse;
        let observation = CollapseChannel;
        let protocol = ActionProtocol::new(vec![Collapse]);

        for n in 2..=5 {
            let parity = collapse_parity_belief(n);
            let exact = collapse_exact_belief(n);
            assert_eq!(
                minimal_query_depth(&dynamics, &observation, &protocol, &parity, 1),
                Some(1)
            );
            assert_eq!(
                minimal_query_depth(&dynamics, &observation, &protocol, &exact, 1),
                None
            );
        }
    }

    #[test]
    fn target_collapsing_merge_creates_permanent_collision() {
        let dynamics = TargetCollapsingMerge;
        let observation = CollapseChannel;
        let protocol = ActionProtocol::new(vec![Collapse]);

        for n in 2..=5 {
            let parity = collapse_parity_belief(n);
            assert_eq!(
                minimal_query_depth(&dynamics, &observation, &protocol, &parity, 2),
                None
            );
        }
    }

    #[test]
    fn epistemic_offload_points_are_pareto_incomparable() {
        for n in 2..=12 {
            let raw = ResourceVector {
                query: 0,
                external_actions: 0,
                internal_ops: n - 1,
                memory_bits: 0,
            };
            let normalized = ResourceVector {
                query: 0,
                external_actions: 1,
                internal_ops: 0,
                memory_bits: 0,
            };
            let frontier = pareto_frontier(vec![raw, normalized]);
            assert_eq!(frontier.len(), 2);
            assert!(frontier.contains(&raw));
            assert!(frontier.contains(&normalized));
        }
    }

    #[test]
    fn permanent_collision_is_detected_after_m2o_step() {
        let dynamics = TargetCollapsingMerge;
        let root = collapse_parity_belief(2);
        let next: Vec<_> = root
            .iter()
            .map(|h| HypothesisRecord {
                root_hypothesis_id: h.root_hypothesis_id,
                current_state: dynamics.step(&h.current_state, &Collapse),
                target_value: h.target_value,
            })
            .collect();
        assert!(permanent_target_collision(&next));
    }
}
