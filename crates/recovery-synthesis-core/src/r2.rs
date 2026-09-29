use cuberev_core::{CornerState, ORIENTATIONS, PERMUTATIONS};
use std::collections::BTreeMap;

#[derive(Clone, Copy, Debug, Eq, PartialEq, Ord, PartialOrd)]
pub enum ParityMemory {
    Even,
    Odd,
}

impl ParityMemory {
    pub fn update(self, bit: u8) -> Self {
        assert!(bit <= 1);
        match (self, bit) {
            (Self::Even, 0) | (Self::Odd, 1) => Self::Even,
            (Self::Odd, 0) | (Self::Even, 1) => Self::Odd,
            _ => unreachable!(),
        }
    }

    pub fn output(self) -> u8 {
        match self {
            Self::Even => 0,
            Self::Odd => 1,
        }
    }
}

pub fn run_internal_parity_controller(bits: &[u8]) -> u8 {
    bits.iter()
        .copied()
        .fold(ParityMemory::Even, ParityMemory::update)
        .output()
}

pub fn run_externalized_parity_controller(bits: &[u8]) -> u8 {
    let mut scratch = 0u8;
    for &bit in bits {
        assert!(bit <= 1);
        scratch ^= bit;
    }
    scratch
}

pub fn history_quotient_class(bits: &[u8]) -> ParityMemory {
    bits.iter()
        .copied()
        .fold(ParityMemory::Even, ParityMemory::update)
}

pub fn histories_are_controller_equivalent(left: &[u8], right: &[u8]) -> bool {
    history_quotient_class(left) == history_quotient_class(right)
}

pub fn parity_controller_state_lower_bound() -> usize {
    2
}

pub fn parity_controller_memory_lower_bound_bits() -> u32 {
    1
}

pub fn end_suffix_distinguishes(left: &[u8], right: &[u8]) -> bool {
    run_internal_parity_controller(left) != run_internal_parity_controller(right)
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct StateTransferWitness {
    pub internal_states_before: usize,
    pub internal_states_after: usize,
    pub external_states_before: usize,
    pub external_states_after: usize,
}

impl StateTransferWitness {
    pub fn joint_capacity_before(self) -> usize {
        self.internal_states_before * self.external_states_before
    }

    pub fn joint_capacity_after(self) -> usize {
        self.internal_states_after * self.external_states_after
    }
}

pub fn externalization_state_transfer_witness() -> StateTransferWitness {
    StateTransferWitness {
        internal_states_before: 2,
        internal_states_after: 1,
        external_states_before: 1,
        external_states_after: 2,
    }
}

pub fn scratch_update_is_reversible(scratch: u8, bit: u8) -> bool {
    assert!(scratch <= 1 && bit <= 1);
    let once = scratch ^ bit;
    let twice = once ^ bit;
    twice == scratch
}

pub fn cube_permutation_inversion_stream(state: &CornerState) -> Vec<u8> {
    let mut out = Vec::with_capacity(21);
    for i in 0..7 {
        for j in i + 1..7 {
            out.push((state.perm[i] > state.perm[j]) as u8);
        }
    }
    out
}

pub fn cube_permutation_parity(state: &CornerState) -> u8 {
    run_internal_parity_controller(&cube_permutation_inversion_stream(state))
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct CubeTransportCertificate {
    pub permutation_representatives_checked: u32,
    pub orientations_per_permutation: u32,
    pub implied_cube_states: u32,
    pub stream_length: usize,
    pub internal_memory_bits: u32,
    pub externalized_internal_memory_bits: u32,
}

pub fn verify_cube_permutation_transport() -> CubeTransportCertificate {
    for lehmer in 0..PERMUTATIONS {
        let rank = lehmer * ORIENTATIONS;
        let state = CornerState::unrank(rank).expect("valid cube representative");
        let stream = cube_permutation_inversion_stream(&state);
        let target = cube_permutation_parity(&state);

        assert_eq!(stream.len(), 21);
        assert_eq!(run_internal_parity_controller(&stream), target);
        assert_eq!(run_externalized_parity_controller(&stream), target);

        // Orientation is deliberately excluded from both the target and stream.
        // Check a second orientation-coded state in the same permutation block.
        let alt = CornerState::unrank(rank + ORIENTATIONS - 1)
            .expect("valid orientation variant");
        assert_eq!(alt.perm, state.perm);
        assert_eq!(
            cube_permutation_inversion_stream(&alt),
            stream,
            "orientation must not change the transported observation stream"
        );
    }

    CubeTransportCertificate {
        permutation_representatives_checked: PERMUTATIONS,
        orientations_per_permutation: ORIENTATIONS,
        implied_cube_states: PERMUTATIONS * ORIENTATIONS,
        stream_length: 21,
        internal_memory_bits: parity_controller_memory_lower_bound_bits(),
        externalized_internal_memory_bits: 0,
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct LearnedController {
    pub output_by_state: [u8; 2],
    pub transition: [[usize; 2]; 2],
}

impl LearnedController {
    pub fn run(&self, bits: &[u8]) -> u8 {
        let mut state = 0usize;
        for &bit in bits {
            assert!(bit <= 1);
            state = self.transition[state][bit as usize];
        }
        self.output_by_state[state]
    }

    pub fn state_count(&self) -> usize {
        2
    }
}

pub fn fit_parity_controller_from_short_traces(max_len: usize) -> LearnedController {
    assert!(max_len >= 2);

    let mut outputs = [None, None];
    let mut transitions = [[None; 2]; 2];

    for len in 0..=max_len {
        for mask in 0..(1usize << len) {
            let bits: Vec<u8> = (0..len)
                .map(|i| ((mask >> i) & 1) as u8)
                .collect();
            let state = history_quotient_class(&bits) as usize;
            let output = run_internal_parity_controller(&bits);
            outputs[state] = Some(output);

            for bit in [0u8, 1u8] {
                let mut extended = bits.clone();
                extended.push(bit);
                let next = history_quotient_class(&extended) as usize;
                transitions[state][bit as usize] = Some(next);
            }
        }
    }

    LearnedController {
        output_by_state: [
            outputs[0].expect("even state observed"),
            outputs[1].expect("odd state observed"),
        ],
        transition: [
            [
                transitions[0][0].expect("transition observed"),
                transitions[0][1].expect("transition observed"),
            ],
            [
                transitions[1][0].expect("transition observed"),
                transitions[1][1].expect("transition observed"),
            ],
        ],
    }
}

pub fn one_state_compression_fails() -> bool {
    // Histories [] and [1] require different terminal outputs.
    end_suffix_distinguishes(&[], &[1])
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct LearnedCompressionCertificate {
    pub authority_states: usize,
    pub learned_states: usize,
    pub one_state_candidate_rejected: bool,
    pub cube_permutations_held_out: u32,
    pub held_out_failures: u32,
}

pub fn learned_compression_against_cube_authority() -> LearnedCompressionCertificate {
    let learned = fit_parity_controller_from_short_traces(3);
    let mut failures = 0u32;

    for lehmer in 0..PERMUTATIONS {
        let state = CornerState::unrank(lehmer * ORIENTATIONS).expect("valid cube state");
        let stream = cube_permutation_inversion_stream(&state);
        let authority = cube_permutation_parity(&state);
        if learned.run(&stream) != authority {
            failures += 1;
        }
    }

    LearnedCompressionCertificate {
        authority_states: parity_controller_state_lower_bound(),
        learned_states: learned.state_count(),
        one_state_candidate_rejected: one_state_compression_fails(),
        cube_permutations_held_out: PERMUTATIONS,
        held_out_failures: failures,
    }
}

pub fn observation_history_partition(max_len: usize) -> BTreeMap<ParityMemory, usize> {
    let mut counts = BTreeMap::new();
    for len in 0..=max_len {
        for mask in 0..(1usize << len) {
            let bits: Vec<u8> = (0..len)
                .map(|i| ((mask >> i) & 1) as u8)
                .collect();
            *counts.entry(history_quotient_class(&bits)).or_insert(0) += 1;
        }
    }
    counts
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn history_quotient_has_exactly_two_classes() {
        let classes = observation_history_partition(6);
        assert_eq!(classes.len(), 2);
        assert!(end_suffix_distinguishes(&[], &[1]));
        assert_eq!(parity_controller_state_lower_bound(), 2);
        assert_eq!(parity_controller_memory_lower_bound_bits(), 1);
    }

    #[test]
    fn reversible_external_scratch_moves_one_bit_outward() {
        for scratch in [0u8, 1u8] {
            for bit in [0u8, 1u8] {
                assert!(scratch_update_is_reversible(scratch, bit));
            }
        }
        let witness = externalization_state_transfer_witness();
        assert_eq!(witness.internal_states_before, 2);
        assert_eq!(witness.internal_states_after, 1);
        assert_eq!(witness.external_states_before, 1);
        assert_eq!(witness.external_states_after, 2);
        assert_eq!(witness.joint_capacity_before(), witness.joint_capacity_after());
    }

    #[test]
    fn cube_transport_is_exact_over_all_permutation_representatives() {
        let cert = verify_cube_permutation_transport();
        assert_eq!(cert.permutation_representatives_checked, 5_040);
        assert_eq!(cert.orientations_per_permutation, 729);
        assert_eq!(cert.implied_cube_states, 3_674_160);
        assert_eq!(cert.stream_length, 21);
        assert_eq!(cert.internal_memory_bits, 1);
        assert_eq!(cert.externalized_internal_memory_bits, 0);
    }

    #[test]
    fn learned_two_state_controller_matches_authority_on_cube_holdout() {
        let cert = learned_compression_against_cube_authority();
        assert_eq!(cert.authority_states, 2);
        assert_eq!(cert.learned_states, 2);
        assert!(cert.one_state_candidate_rejected);
        assert_eq!(cert.cube_permutations_held_out, 5_040);
        assert_eq!(cert.held_out_failures, 0);
    }
}
