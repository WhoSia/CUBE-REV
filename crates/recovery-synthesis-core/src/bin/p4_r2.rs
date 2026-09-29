use recovery_synthesis_core::r2::{
    externalization_state_transfer_witness, learned_compression_against_cube_authority,
    observation_history_partition, parity_controller_memory_lower_bound_bits,
    parity_controller_state_lower_bound, verify_cube_permutation_transport,
};

fn main() {
    let classes = observation_history_partition(8);
    let transfer = externalization_state_transfer_witness();
    let cube = verify_cube_permutation_transport();
    let learned = learned_compression_against_cube_authority();

    println!("metric\tvalue");
    println!("history_quotient_classes\t{}", classes.len());
    println!(
        "internal_controller_states\t{}",
        parity_controller_state_lower_bound()
    );
    println!(
        "internal_memory_lower_bound_bits\t{}",
        parity_controller_memory_lower_bound_bits()
    );
    println!(
        "externalized_internal_states\t{}",
        transfer.internal_states_after
    );
    println!(
        "externalized_world_scratch_states\t{}",
        transfer.external_states_after
    );
    println!(
        "joint_capacity_before\t{}",
        transfer.joint_capacity_before()
    );
    println!("joint_capacity_after\t{}", transfer.joint_capacity_after());
    println!(
        "cube_permutation_representatives_checked\t{}",
        cube.permutation_representatives_checked
    );
    println!(
        "cube_orientations_per_permutation\t{}",
        cube.orientations_per_permutation
    );
    println!("cube_implied_states\t{}", cube.implied_cube_states);
    println!("cube_observation_stream_length\t{}", cube.stream_length);
    println!("learned_authority_states\t{}", learned.authority_states);
    println!("learned_candidate_states\t{}", learned.learned_states);
    println!(
        "one_state_compression_rejected\t{}",
        learned.one_state_candidate_rejected
    );
    println!(
        "cube_held_out_permutations\t{}",
        learned.cube_permutations_held_out
    );
    println!("cube_held_out_failures\t{}", learned.held_out_failures);
}
