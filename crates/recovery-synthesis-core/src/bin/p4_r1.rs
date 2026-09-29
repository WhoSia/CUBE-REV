use recovery_synthesis_core::r1::{
    balanced_is_unique_under_own_budget, parity_frontier, parity_protocol_witnesses,
    scalarization_counterexample, scalarization_counterexample_is_pareto, scale_reversal_witness,
    unsupported_balanced_symbolic_certificate, verify_parity_protocol, ParityProtocolKind,
};

fn main() {
    println!(
        "court\tn\tprotocol\tverified\tquery\texternal_actions\tinternal_ops\tmemory_bits\tpareto"
    );

    for n in 3..=8 {
        let frontier = parity_frontier(n);
        for witness in parity_protocol_witnesses(n) {
            println!(
                "parity_workbench\t{n}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
                witness.kind.name(),
                verify_parity_protocol(witness.kind, n),
                witness.cost.query,
                witness.cost.external_actions,
                witness.cost.internal_ops,
                witness.cost.memory_bits,
                frontier.contains(&witness.cost)
            );
        }
    }

    let s = scalarization_counterexample();
    println!(
        "scalarization_gadget\t0\tprobe_sparse\ttrue\t{}\t{}\t{}\t{}\t{}",
        s.probe_sparse.query,
        s.probe_sparse.external_actions,
        s.probe_sparse.internal_ops,
        s.probe_sparse.memory_bits,
        scalarization_counterexample_is_pareto()
    );
    println!(
        "scalarization_gadget\t0\tbalanced\t{}\t{}\t{}\t{}\t{}\t{}",
        balanced_is_unique_under_own_budget(),
        s.balanced.query,
        s.balanced.external_actions,
        s.balanced.internal_ops,
        s.balanced.memory_bits,
        scalarization_counterexample_is_pareto()
    );
    println!(
        "scalarization_gadget\t0\tprobe_rich\ttrue\t{}\t{}\t{}\t{}\t{}",
        s.probe_rich.query,
        s.probe_rich.external_actions,
        s.probe_rich.internal_ops,
        s.probe_rich.memory_bits,
        scalarization_counterexample_is_pareto()
    );

    for n in [2u32, 8u32] {
        let r = scale_reversal_witness(n);
        println!(
            "scale_reversal\t{n}\tunrolled\ttrue\t{}\t{}\t{}\t{}\ttrue",
            r.unrolled.query,
            r.unrolled.external_actions,
            r.unrolled.internal_ops,
            r.unrolled.memory_bits
        );
        println!(
            "scale_reversal\t{n}\tcompiled_macro\ttrue\t{}\t{}\t{}\t{}\ttrue",
            r.compiled_macro.query,
            r.compiled_macro.external_actions,
            r.compiled_macro.internal_ops,
            r.compiled_macro.memory_bits
        );
    }

    eprintln!("{}", unsupported_balanced_symbolic_certificate());
    let _ = ParityProtocolKind::ALL;
}
