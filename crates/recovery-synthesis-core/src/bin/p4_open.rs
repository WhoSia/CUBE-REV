use recovery_game_core::{
    bit_query_exact_belief, BitQueryDynamics, BitQueryObservation, ResourceVector, RotateProbe,
};
use recovery_synthesis_core::{policy_depth, synthesize_pareto};

fn main() {
    println!("family\ttarget\tn\tdepth\tpareto_count\tquery\texternal_actions\tinternal_ops\tmemory_bits");

    for n in 1..=4 {
        let dynamics = BitQueryDynamics { n };
        let observation = BitQueryObservation;
        let actions: Vec<_> = (0..n).map(RotateProbe).collect();
        let belief = bit_query_exact_belief(n);
        let policies = synthesize_pareto(
            &dynamics,
            &observation,
            &actions,
            &belief,
            n as usize,
            &|_| ResourceVector {
                query: 1,
                external_actions: 1,
                internal_ops: 0,
                memory_bits: 0,
            },
        );

        let depth = policies
            .iter()
            .map(|p| policy_depth(&p.root))
            .min()
            .unwrap_or(0);
        let cost = policies
            .iter()
            .map(|p| p.cost)
            .min()
            .unwrap_or(ResourceVector {
                query: 0,
                external_actions: 0,
                internal_ops: 0,
                memory_bits: 0,
            });

        println!(
            "B_n\texact_state\t{n}\t{depth}\t{}\t{}\t{}\t{}\t{}",
            policies.len(),
            cost.query,
            cost.external_actions,
            cost.internal_ops,
            cost.memory_bits
        );
    }
}
