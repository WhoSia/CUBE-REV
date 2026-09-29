use recovery_game_core::{pareto_frontier, ResourceVector};

#[derive(Clone, Copy, Debug, Eq, PartialEq, Ord, PartialOrd)]
pub enum ParityProtocolKind {
    BitStream,
    SnapshotCompute,
    SnapshotLookup,
    ExternalFold,
}

impl ParityProtocolKind {
    pub const ALL: [Self; 4] = [
        Self::BitStream,
        Self::SnapshotCompute,
        Self::SnapshotLookup,
        Self::ExternalFold,
    ];

    pub fn name(self) -> &'static str {
        match self {
            Self::BitStream => "bit_stream",
            Self::SnapshotCompute => "snapshot_compute",
            Self::SnapshotLookup => "snapshot_lookup",
            Self::ExternalFold => "external_fold",
        }
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct ProtocolWitness {
    pub kind: ParityProtocolKind,
    pub cost: ResourceVector,
}

pub fn parity(bits: u16) -> u8 {
    (bits.count_ones() & 1) as u8
}

pub fn execute_parity_protocol(kind: ParityProtocolKind, n: u8, bits: u16) -> u8 {
    assert!((1..=15).contains(&n));
    assert!(bits < (1u16 << n));

    match kind {
        ParityProtocolKind::BitStream => {
            let mut acc = 0u8;
            for i in 0..n {
                acc ^= ((bits >> i) & 1) as u8;
            }
            acc
        }
        ParityProtocolKind::SnapshotCompute => parity(bits),
        ParityProtocolKind::SnapshotLookup => {
            // Exact finite lookup semantics. The resource model below charges
            // one stored target bit for every possible n-bit state.
            parity(bits)
        }
        ParityProtocolKind::ExternalFold => {
            // Each reversible XOR-to-scratch action is an involution.
            // The hidden data bits are preserved; only the external scratch bit changes.
            let mut scratch = 0u8;
            for i in 0..n {
                scratch ^= ((bits >> i) & 1) as u8;
            }
            scratch
        }
    }
}

pub fn parity_protocol_cost(kind: ParityProtocolKind, n: u8) -> ResourceVector {
    assert!((3..=15).contains(&n));
    match kind {
        ParityProtocolKind::BitStream => ResourceVector {
            query: n as u32,
            external_actions: 0,
            internal_ops: (n - 1) as u32,
            memory_bits: 1,
        },
        ParityProtocolKind::SnapshotCompute => ResourceVector {
            query: 1,
            external_actions: 0,
            internal_ops: (n - 1) as u32,
            memory_bits: n as u32,
        },
        ParityProtocolKind::SnapshotLookup => ResourceVector {
            query: 1,
            external_actions: 0,
            internal_ops: 1,
            memory_bits: 1u32 << n,
        },
        ParityProtocolKind::ExternalFold => ResourceVector {
            query: 1,
            external_actions: n as u32,
            internal_ops: 0,
            memory_bits: 0,
        },
    }
}

pub fn parity_protocol_witnesses(n: u8) -> Vec<ProtocolWitness> {
    ParityProtocolKind::ALL
        .into_iter()
        .map(|kind| ProtocolWitness {
            kind,
            cost: parity_protocol_cost(kind, n),
        })
        .collect()
}

pub fn parity_frontier(n: u8) -> Vec<ResourceVector> {
    pareto_frontier(
        parity_protocol_witnesses(n)
            .into_iter()
            .map(|w| w.cost)
            .collect(),
    )
}

pub fn verify_parity_protocol(kind: ParityProtocolKind, n: u8) -> bool {
    assert!((3..=15).contains(&n));
    (0..(1u16 << n)).all(|bits| execute_parity_protocol(kind, n, bits) == parity(bits))
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct ScalarizationCounterexample {
    pub probe_sparse: ResourceVector,
    pub balanced: ResourceVector,
    pub probe_rich: ResourceVector,
}

pub fn scalarization_counterexample() -> ScalarizationCounterexample {
    ScalarizationCounterexample {
        probe_sparse: ResourceVector {
            query: 1,
            external_actions: 4,
            internal_ops: 4,
            memory_bits: 1,
        },
        balanced: ResourceVector {
            query: 3,
            external_actions: 3,
            internal_ops: 3,
            memory_bits: 1,
        },
        probe_rich: ResourceVector {
            query: 4,
            external_actions: 1,
            internal_ops: 1,
            memory_bits: 1,
        },
    }
}

pub fn scalarization_counterexample_is_pareto() -> bool {
    let w = scalarization_counterexample();
    let frontier = pareto_frontier(vec![w.probe_sparse, w.balanced, w.probe_rich]);
    frontier.len() == 3
        && frontier.contains(&w.probe_sparse)
        && frontier.contains(&w.balanced)
        && frontier.contains(&w.probe_rich)
}

pub fn balanced_is_unique_under_own_budget() -> bool {
    let w = scalarization_counterexample();
    let budget = w.balanced;
    let allows = |cost: ResourceVector| {
        cost.query <= budget.query
            && cost.external_actions <= budget.external_actions
            && cost.internal_ops <= budget.internal_ops
            && cost.memory_bits <= budget.memory_bits
    };

    !allows(w.probe_sparse) && allows(w.balanced) && !allows(w.probe_rich)
}

pub fn unsupported_balanced_symbolic_certificate() -> &'static str {
    "If positive weights make B no worse than A and C, then 2*q <= a+c and 2*(a+c) <= q. Hence 4*q <= q, contradicting q>0."
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct ScaleReversal {
    pub n: u32,
    pub unrolled: ResourceVector,
    pub compiled_macro: ResourceVector,
}

pub fn scale_reversal_witness(n: u32) -> ScaleReversal {
    assert!(n >= 2);
    let macro_cost = 2 + ceil_log2(n);
    ScaleReversal {
        n,
        unrolled: ResourceVector {
            query: n,
            external_actions: n,
            internal_ops: n,
            memory_bits: n,
        },
        compiled_macro: ResourceVector {
            query: macro_cost,
            external_actions: macro_cost,
            internal_ops: macro_cost,
            memory_bits: macro_cost,
        },
    }
}

pub fn ceil_log2(n: u32) -> u32 {
    assert!(n > 0);
    if n == 1 {
        0
    } else {
        32 - (n - 1).leading_zeros()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn all_parity_protocols_are_extensionally_exact() {
        for n in 3..=8 {
            for kind in ParityProtocolKind::ALL {
                assert!(verify_parity_protocol(kind, n));
            }
        }
    }

    #[test]
    fn naturalized_parity_workbench_has_four_way_frontier() {
        for n in 3..=8 {
            let frontier = parity_frontier(n);
            assert_eq!(frontier.len(), 4, "n={n}");
        }
    }

    #[test]
    fn unsupported_point_is_still_pareto_and_budget_essential() {
        assert!(scalarization_counterexample_is_pareto());
        assert!(balanced_is_unique_under_own_budget());
    }

    #[test]
    fn scale_change_reverses_coordinatewise_dominance() {
        let small = scale_reversal_witness(2);
        assert!(small.unrolled.dominates(small.compiled_macro));

        let large = scale_reversal_witness(8);
        assert!(large.compiled_macro.dominates(large.unrolled));
    }
}
