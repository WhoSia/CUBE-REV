//! CUBE-REV Generation V G5-P4 protocol-synthesis authority.
//!
//! This crate consumes, but does not redefine, G5-P3 recovery semantics.
//! It synthesizes finite adaptive policies and their resource frontiers.
//! Human executability, learned-policy adequacy, and adversarial robustness
//! remain claims to be earned by later courts.

pub mod r1;
pub mod r2;
pub mod r3;

use recovery_game_core::{
    permanent_target_collision, target_is_constant, FiniteDynamics, HypothesisRecord,
    ObservationChannel, ResourceVector,
};
use std::collections::BTreeMap;

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum PolicyNode<A, O> {
    Resolved,
    Act {
        action: A,
        branches: BTreeMap<O, Box<PolicyNode<A, O>>>,
    },
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct SynthesizedPolicy<A, O> {
    pub root: PolicyNode<A, O>,
    pub cost: ResourceVector,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct ResourceBudget {
    pub max: ResourceVector,
}

impl ResourceBudget {
    pub fn allows(&self, cost: ResourceVector) -> bool {
        cost.query <= self.max.query
            && cost.external_actions <= self.max.external_actions
            && cost.internal_ops <= self.max.internal_ops
            && cost.memory_bits <= self.max.memory_bits
    }
}

pub fn synthesize_pareto<D, O, T, F>(
    dynamics: &D,
    observation: &O,
    actions: &[D::Action],
    belief: &[HypothesisRecord<D::State, T>],
    max_depth: usize,
    action_cost: &F,
) -> Vec<SynthesizedPolicy<D::Action, O::Observation>>
where
    D: FiniteDynamics,
    D::State: Ord,
    D::Action: Ord,
    O: ObservationChannel<D::State>,
    O::Observation: Ord,
    T: Clone + Eq + Ord,
    F: Fn(&D::Action) -> ResourceVector,
{
    let mut out = synthesize_rec(
        dynamics,
        observation,
        actions,
        belief,
        max_depth,
        action_cost,
    );
    pareto_policies(&mut out);
    out
}

fn synthesize_rec<D, O, T, F>(
    dynamics: &D,
    observation: &O,
    actions: &[D::Action],
    belief: &[HypothesisRecord<D::State, T>],
    depth: usize,
    action_cost: &F,
) -> Vec<SynthesizedPolicy<D::Action, O::Observation>>
where
    D: FiniteDynamics,
    D::State: Ord,
    D::Action: Ord,
    O: ObservationChannel<D::State>,
    O::Observation: Ord,
    T: Clone + Eq + Ord,
    F: Fn(&D::Action) -> ResourceVector,
{
    if target_is_constant(belief) {
        return vec![SynthesizedPolicy {
            root: PolicyNode::Resolved,
            cost: zero_cost(),
        }];
    }
    if depth == 0 || permanent_target_collision(belief) {
        return Vec::new();
    }

    let mut candidates = Vec::new();
    for action in actions {
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

        let mut child_frontiers = Vec::new();
        let mut feasible = true;
        for (obs, child_belief) in children {
            let child = synthesize_rec(
                dynamics,
                observation,
                actions,
                &child_belief,
                depth - 1,
                action_cost,
            );
            if child.is_empty() {
                feasible = false;
                break;
            }
            child_frontiers.push((obs, child));
        }
        if !feasible {
            continue;
        }

        let partials = combine_children(&child_frontiers);
        for (branches, downstream) in partials {
            candidates.push(SynthesizedPolicy {
                root: PolicyNode::Act {
                    action: action.clone(),
                    branches,
                },
                cost: add_cost(action_cost(action), downstream),
            });
        }
    }

    pareto_policies(&mut candidates);
    candidates
}

fn combine_children<A, O>(
    child_frontiers: &[(O, Vec<SynthesizedPolicy<A, O>>)],
) -> Vec<(BTreeMap<O, Box<PolicyNode<A, O>>>, ResourceVector)>
where
    A: Clone + Eq + Ord,
    O: Clone + Eq + Ord,
{
    let mut partials = vec![(BTreeMap::new(), zero_cost())];

    for (obs, frontier) in child_frontiers {
        let mut next = Vec::new();
        for (branches, accumulated) in &partials {
            for candidate in frontier {
                let mut new_branches = branches.clone();
                new_branches.insert(obs.clone(), Box::new(candidate.root.clone()));
                next.push((new_branches, max_cost(*accumulated, candidate.cost)));
            }
        }
        pareto_branch_partials(&mut next);
        partials = next;
    }

    partials
}

fn pareto_branch_partials<A, O>(
    candidates: &mut Vec<(BTreeMap<O, Box<PolicyNode<A, O>>>, ResourceVector)>,
) where
    A: Clone + Eq + Ord,
    O: Clone + Eq + Ord,
{
    let costs: Vec<_> = candidates.iter().map(|(_, cost)| *cost).collect();
    let mut keep = Vec::new();
    for (idx, candidate) in candidates.drain(..).enumerate() {
        if !costs
            .iter()
            .enumerate()
            .any(|(j, other)| j != idx && other.dominates(candidate.1))
        {
            keep.push(candidate);
        }
    }
    *candidates = keep;
}

fn pareto_policies<A, O>(candidates: &mut Vec<SynthesizedPolicy<A, O>>)
where
    A: Clone + Eq + Ord,
    O: Clone + Eq + Ord,
{
    let costs: Vec<_> = candidates.iter().map(|p| p.cost).collect();
    let mut keep = Vec::new();
    for (idx, candidate) in candidates.drain(..).enumerate() {
        if !costs
            .iter()
            .enumerate()
            .any(|(j, other)| j != idx && other.dominates(candidate.cost))
        {
            if !keep
                .iter()
                .any(|p: &SynthesizedPolicy<A, O>| p == &candidate)
            {
                keep.push(candidate);
            }
        }
    }
    *candidates = keep;
}

pub fn executable_under<A, O>(
    policies: &[SynthesizedPolicy<A, O>],
    budget: ResourceBudget,
) -> Vec<&SynthesizedPolicy<A, O>> {
    policies
        .iter()
        .filter(|policy| budget.allows(policy.cost))
        .collect()
}

pub fn failure_localization<A, O>(
    baseline: &[SynthesizedPolicy<A, O>],
    variants: &[Vec<SynthesizedPolicy<A, O>>],
    budget: ResourceBudget,
) -> Vec<usize> {
    let baseline_feasible = baseline.iter().any(|p| budget.allows(p.cost));
    if !baseline_feasible {
        return (0..variants.len()).collect();
    }

    variants
        .iter()
        .enumerate()
        .filter_map(|(idx, variant)| {
            (!variant.iter().any(|p| budget.allows(p.cost))).then_some(idx)
        })
        .collect()
}

pub fn policy_node_count<A, O>(node: &PolicyNode<A, O>) -> u32 {
    match node {
        PolicyNode::Resolved => 1,
        PolicyNode::Act { branches, .. } => {
            1 + branches
                .values()
                .map(|child| policy_node_count(child))
                .sum::<u32>()
        }
    }
}

pub fn policy_depth<A, O>(node: &PolicyNode<A, O>) -> u32 {
    match node {
        PolicyNode::Resolved => 0,
        PolicyNode::Act { branches, .. } => {
            1 + branches
                .values()
                .map(|child| policy_depth(child))
                .max()
                .unwrap_or(0)
        }
    }
}

pub fn structural_compression_ratio<A, O>(
    exact: &PolicyNode<A, O>,
    candidate: &PolicyNode<A, O>,
) -> f64 {
    let exact_nodes = policy_node_count(exact) as f64;
    let candidate_nodes = policy_node_count(candidate) as f64;
    exact_nodes / candidate_nodes.max(1.0)
}

fn zero_cost() -> ResourceVector {
    ResourceVector {
        query: 0,
        external_actions: 0,
        internal_ops: 0,
        memory_bits: 0,
    }
}

fn add_cost(a: ResourceVector, b: ResourceVector) -> ResourceVector {
    ResourceVector {
        query: a.query.saturating_add(b.query),
        external_actions: a.external_actions.saturating_add(b.external_actions),
        internal_ops: a.internal_ops.saturating_add(b.internal_ops),
        memory_bits: a.memory_bits.max(b.memory_bits),
    }
}

fn max_cost(a: ResourceVector, b: ResourceVector) -> ResourceVector {
    ResourceVector {
        query: a.query.max(b.query),
        external_actions: a.external_actions.max(b.external_actions),
        internal_ops: a.internal_ops.max(b.internal_ops),
        memory_bits: a.memory_bits.max(b.memory_bits),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use recovery_game_core::{
        bit_query_exact_belief, bit_query_parity_belief, BitQueryDynamics, BitQueryObservation,
        RotateProbe,
    };

    fn read_cost(_: &RotateProbe) -> ResourceVector {
        ResourceVector {
            query: 1,
            external_actions: 1,
            internal_ops: 0,
            memory_bits: 0,
        }
    }

    #[test]
    fn synthesis_recovers_exact_bit_query_at_expected_depth() {
        let n = 3;
        let dynamics = BitQueryDynamics { n };
        let observation = BitQueryObservation;
        let actions: Vec<_> = (0..n).map(RotateProbe).collect();
        let belief = bit_query_exact_belief(n);
        let policies = synthesize_pareto(&dynamics, &observation, &actions, &belief, 3, &read_cost);

        assert!(!policies.is_empty());
        assert!(policies.iter().all(|p| p.cost.query == 3));
        assert!(policies.iter().all(|p| policy_depth(&p.root) == 3));
    }

    #[test]
    fn too_shallow_budget_produces_no_protocol() {
        let n = 3;
        let dynamics = BitQueryDynamics { n };
        let observation = BitQueryObservation;
        let actions: Vec<_> = (0..n).map(RotateProbe).collect();
        let belief = bit_query_exact_belief(n);
        let policies = synthesize_pareto(&dynamics, &observation, &actions, &belief, 2, &read_cost);

        assert!(policies.is_empty());
    }

    #[test]
    fn target_choice_changes_the_synthesis_problem() {
        let n = 3;
        let dynamics = BitQueryDynamics { n };
        let observation = BitQueryObservation;
        let actions: Vec<_> = (0..n).map(RotateProbe).collect();
        let exact = bit_query_exact_belief(n);
        let parity = bit_query_parity_belief(n);

        let exact_policies =
            synthesize_pareto(&dynamics, &observation, &actions, &exact, 3, &read_cost);
        let parity_policies =
            synthesize_pareto(&dynamics, &observation, &actions, &parity, 3, &read_cost);

        assert!(!exact_policies.is_empty());
        assert!(!parity_policies.is_empty());
        assert_eq!(
            exact_policies.iter().map(|p| p.cost).min(),
            parity_policies.iter().map(|p| p.cost).min()
        );
    }

    #[test]
    fn bounded_agent_filter_is_resource_relative() {
        let n = 3;
        let dynamics = BitQueryDynamics { n };
        let observation = BitQueryObservation;
        let actions: Vec<_> = (0..n).map(RotateProbe).collect();
        let belief = bit_query_exact_belief(n);
        let policies = synthesize_pareto(&dynamics, &observation, &actions, &belief, 3, &read_cost);

        let tight = ResourceBudget {
            max: ResourceVector {
                query: 2,
                external_actions: 3,
                internal_ops: 0,
                memory_bits: 0,
            },
        };
        let sufficient = ResourceBudget {
            max: ResourceVector {
                query: 3,
                external_actions: 3,
                internal_ops: 0,
                memory_bits: 0,
            },
        };

        assert!(executable_under(&policies, tight).is_empty());
        assert!(!executable_under(&policies, sufficient).is_empty());
    }

    #[test]
    fn adversarial_failure_localization_identifies_only_broken_variant() {
        let n = 2;
        let dynamics = BitQueryDynamics { n };
        let observation = BitQueryObservation;
        let actions: Vec<_> = (0..n).map(RotateProbe).collect();
        let belief = bit_query_exact_belief(n);
        let baseline = synthesize_pareto(&dynamics, &observation, &actions, &belief, 2, &read_cost);
        let preserved = baseline.clone();
        let broken = Vec::new();
        let budget = ResourceBudget {
            max: ResourceVector {
                query: 2,
                external_actions: 2,
                internal_ops: 0,
                memory_bits: 0,
            },
        };

        assert_eq!(
            failure_localization(&baseline, &[preserved, broken], budget),
            vec![1]
        );
    }
}
