use recovery_synthesis_core::r3::{
    allocation_lattice, cube_minimal_internal_states,
    cube_minimal_scratch_bits_for_zero_internal_memory, verify_cube_controller_lattice,
};

fn main() {
    let cube = verify_cube_controller_lattice();

    println!("k\texternal_bits\tinternal_bits\tinternal_states\texternal_states\tjoint_states\tcube_reachable_targets\tcube_min_internal_states");
    for k in 1..=5u8 {
        for point in allocation_lattice(k) {
            println!(
                "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
                k,
                point.external_bits,
                point.internal_bits,
                point.internal_states,
                point.external_states,
                point.joint_states,
                cube.reachable_target_counts[(k - 1) as usize],
                cube_minimal_internal_states(k, point.external_bits)
            );
        }
    }

    println!("metric\tvalue");
    println!(
        "cube_permutation_representatives_checked\t{}",
        cube.permutation_representatives_checked
    );
    println!(
        "cube_orientations_per_permutation\t{}",
        cube.orientations_per_permutation
    );
    println!("cube_implied_ranked_states\t{}", cube.implied_ranked_states);
    println!("cube_allocation_checks\t{}", cube.allocation_checks);
    println!("cube_allocation_failures\t{}", cube.allocation_failures);
    println!(
        "cube_nested_projection_failures\t{}",
        cube.nested_projection_failures
    );
    for k in 1..=5u8 {
        println!(
            "cube_min_scratch_bits_k{}\t{}",
            k,
            cube_minimal_scratch_bits_for_zero_internal_memory(k)
        );
    }
}
