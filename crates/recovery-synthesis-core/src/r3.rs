use cuberev_core::{CornerState, ORIENTATIONS, PERMUTATIONS};

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct AllocationPoint {
    pub target_bits: u8,
    pub external_bits: u8,
    pub internal_bits: u8,
    pub internal_states: u32,
    pub external_states: u32,
    pub joint_states: u32,
}

pub fn controller_states_for_target_bits(k: u8) -> u32 {
    assert!((1..=8).contains(&k));
    1u32 << k
}

pub fn internal_memory_lower_bound_bits(k: u8) -> u8 {
    assert!((1..=8).contains(&k));
    k
}

pub fn allocation_point(k: u8, external_bits: u8) -> AllocationPoint {
    assert!((1..=8).contains(&k));
    assert!(external_bits <= k);
    let internal_bits = k - external_bits;
    let internal_states = 1u32 << internal_bits;
    let external_states = 1u32 << external_bits;
    AllocationPoint {
        target_bits: k,
        external_bits,
        internal_bits,
        internal_states,
        external_states,
        joint_states: internal_states * external_states,
    }
}

pub fn allocation_lattice(k: u8) -> Vec<AllocationPoint> {
    (0..=k).map(|s| allocation_point(k, s)).collect()
}

pub fn minimal_scratch_bits_for_internal_budget(k: u8, internal_budget_bits: u8) -> u8 {
    assert!((1..=8).contains(&k));
    k.saturating_sub(internal_budget_bits.min(k))
}

pub fn xor_target(events: &[u8], k: u8) -> u8 {
    assert!((1..=8).contains(&k));
    let mask = if k == 8 { u8::MAX } else { (1u8 << k) - 1 };
    events.iter().fold(0u8, |acc, event| {
        assert!(*event <= mask);
        acc ^ *event
    })
}

pub fn split_xor_controller(events: &[u8], k: u8, external_bits: u8) -> u8 {
    assert!((1..=8).contains(&k));
    assert!(external_bits <= k);

    let external_mask = if external_bits == 0 {
        0
    } else {
        (1u8 << external_bits) - 1
    };
    let internal_mask = if k == 8 { u8::MAX } else { (1u8 << k) - 1 };

    let mut external = 0u8;
    let mut internal = 0u8;

    for &event in events {
        let projected = event & internal_mask;
        external ^= projected & external_mask;
        internal ^= projected >> external_bits;
    }

    (internal << external_bits) | external
}

pub fn split_update_is_reversible(
    internal: u8,
    external: u8,
    event: u8,
    k: u8,
    external_bits: u8,
) -> bool {
    assert!((1..=8).contains(&k));
    assert!(external_bits <= k);

    let external_mask = if external_bits == 0 {
        0
    } else {
        (1u8 << external_bits) - 1
    };
    let internal_width = k - external_bits;
    let internal_mask = if internal_width == 0 {
        0
    } else {
        (1u8 << internal_width) - 1
    };

    assert!(external <= external_mask);
    assert!(internal <= internal_mask);

    let e = event & external_mask;
    let i = (event >> external_bits) & internal_mask;

    let once_internal = internal ^ i;
    let once_external = external ^ e;
    let twice_internal = once_internal ^ i;
    let twice_external = once_external ^ e;

    twice_internal == internal && twice_external == external
}

pub fn exact_allocation_law_holds(k: u8) -> bool {
    allocation_lattice(k).into_iter().all(|point| {
        point.internal_bits + point.external_bits == k
            && point.joint_states == controller_states_for_target_bits(k)
            && point.internal_states * point.external_states == (1u32 << k)
    })
}

fn feature_membership_mask(i: usize, j: usize) -> u8 {
    debug_assert!(i < j && j < 7);
    let mut mask = 0u8;

    // T1: full inversion parity.
    mask |= 1 << 0;

    // T2: parity of inversions involving position 0.
    if i == 0 || j == 0 {
        mask |= 1 << 1;
    }

    // T3: parity of inversions within the first four positions.
    if i < 4 && j < 4 {
        mask |= 1 << 2;
    }

    // T4: parity of cross inversions between positions [0,3) and [3,7).
    if i < 3 && j >= 3 {
        mask |= 1 << 3;
    }

    // T5: parity of adjacent-position inversions.
    if j == i + 1 {
        mask |= 1 << 4;
    }

    mask
}

pub fn cube_factor_event_stream(state: &CornerState) -> Vec<u8> {
    let mut out = Vec::with_capacity(21);
    for i in 0..7 {
        for j in i + 1..7 {
            let inversion = (state.perm[i] > state.perm[j]) as u8;
            out.push(if inversion == 1 {
                feature_membership_mask(i, j)
            } else {
                0
            });
        }
    }
    out
}

pub fn cube_target_vector(state: &CornerState, k: u8) -> u8 {
    assert!((1..=5).contains(&k));
    let mask = (1u8 << k) - 1;
    xor_target(&cube_factor_event_stream(state), 5) & mask
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct CubeAllocationCertificate {
    pub permutation_representatives_checked: u32,
    pub orientations_per_permutation: u32,
    pub implied_ranked_states: u32,
    pub reachable_target_counts: [u32; 5],
    pub expected_target_counts: [u32; 5],
    pub allocation_checks: u32,
    pub allocation_failures: u32,
    pub nested_projection_failures: u32,
}

pub fn verify_cube_controller_lattice() -> CubeAllocationCertificate {
    let mut seen = [
        vec![false; 2],
        vec![false; 4],
        vec![false; 8],
        vec![false; 16],
        vec![false; 32],
    ];
    let mut allocation_checks = 0u32;
    let mut allocation_failures = 0u32;
    let mut nested_projection_failures = 0u32;

    for lehmer in 0..PERMUTATIONS {
        let rank = lehmer * ORIENTATIONS;
        let state = CornerState::unrank(rank).expect("valid cube representative");
        let alt = CornerState::unrank(rank + ORIENTATIONS - 1)
            .expect("valid orientation variant");

        assert_eq!(state.perm, alt.perm);
        assert_eq!(
            cube_factor_event_stream(&state),
            cube_factor_event_stream(&alt)
        );

        let stream = cube_factor_event_stream(&state);
        let full_target = cube_target_vector(&state, 5);

        for k in 1..=5u8 {
            let mask = (1u8 << k) - 1;
            let target = full_target & mask;
            seen[(k - 1) as usize][target as usize] = true;

            if cube_target_vector(&state, k) != target {
                nested_projection_failures += 1;
            }

            for external_bits in 0..=k {
                allocation_checks += 1;
                if split_xor_controller(&stream, k, external_bits) != target {
                    allocation_failures += 1;
                }
            }
        }
    }

    let reachable_target_counts = [
        seen[0].iter().filter(|x| **x).count() as u32,
        seen[1].iter().filter(|x| **x).count() as u32,
        seen[2].iter().filter(|x| **x).count() as u32,
        seen[3].iter().filter(|x| **x).count() as u32,
        seen[4].iter().filter(|x| **x).count() as u32,
    ];

    CubeAllocationCertificate {
        permutation_representatives_checked: PERMUTATIONS,
        orientations_per_permutation: ORIENTATIONS,
        implied_ranked_states: PERMUTATIONS * ORIENTATIONS,
        reachable_target_counts,
        expected_target_counts: [2, 4, 8, 16, 32],
        allocation_checks,
        allocation_failures,
        nested_projection_failures,
    }
}

pub fn cube_minimal_internal_states(k: u8, external_bits: u8) -> u32 {
    assert!((1..=5).contains(&k));
    assert!(external_bits <= k);
    1u32 << (k - external_bits)
}

pub fn cube_minimal_scratch_bits_for_zero_internal_memory(k: u8) -> u8 {
    assert!((1..=5).contains(&k));
    k
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn allocation_law_conserves_joint_state_capacity() {
        for k in 1..=8 {
            assert!(exact_allocation_law_holds(k));
            for point in allocation_lattice(k) {
                assert_eq!(point.internal_bits + point.external_bits, k);
                assert_eq!(point.joint_states, 1u32 << k);
            }
        }
    }

    #[test]
    fn scratch_capacity_is_exact_for_internal_budget() {
        for k in 1..=8 {
            for budget in 0..=k {
                let scratch = minimal_scratch_bits_for_internal_budget(k, budget);
                assert_eq!(scratch, k - budget);
                let point = allocation_point(k, scratch);
                assert_eq!(point.internal_bits, budget);
            }
        }
    }

    #[test]
    fn split_controller_matches_vector_target_and_updates_are_involutions() {
        for k in 1..=5 {
            let alphabet = 1u8 << k;
            for external_bits in 0..=k {
                for a in 0..alphabet {
                    for b in 0..alphabet {
                        let events = [a, b];
                        assert_eq!(
                            split_xor_controller(&events, k, external_bits),
                            xor_target(&events, k)
                        );
                    }
                }

                let point = allocation_point(k, external_bits);
                for internal in 0..point.internal_states as u8 {
                    for external in 0..point.external_states as u8 {
                        for event in 0..alphabet {
                            assert!(split_update_is_reversible(
                                internal,
                                external,
                                event,
                                k,
                                external_bits
                            ));
                        }
                    }
                }
            }
        }
    }

    #[test]
    fn cube_targets_realize_full_nested_lattice_and_all_allocations() {
        let cert = verify_cube_controller_lattice();
        assert_eq!(cert.permutation_representatives_checked, 5_040);
        assert_eq!(cert.orientations_per_permutation, 729);
        assert_eq!(cert.implied_ranked_states, 3_674_160);
        assert_eq!(cert.reachable_target_counts, cert.expected_target_counts);
        assert_eq!(cert.allocation_failures, 0);
        assert_eq!(cert.nested_projection_failures, 0);
    }

    #[test]
    fn cube_memory_lower_bound_tracks_external_allocation() {
        for k in 1..=5 {
            for external_bits in 0..=k {
                assert_eq!(
                    cube_minimal_internal_states(k, external_bits),
                    1u32 << (k - external_bits)
                );
            }
            assert_eq!(cube_minimal_scratch_bits_for_zero_internal_memory(k), k);
        }
    }
}
