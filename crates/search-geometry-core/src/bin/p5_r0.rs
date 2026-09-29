use search_geometry_core::run_full_court;

fn main() {
    let s = run_full_court();

    println!("metric\tvalue");
    println!("states\t{}", s.states);
    println!("phase2_subgroup_states\t{}", s.subgroup_states);
    println!("anchored_ruf_geodesic_diameter\t{}", s.geodesic_diameter);
    println!("orientation_layer_diameter\t{}", s.orientation_diameter);
    println!("phase2_restricted_diameter\t{}", s.phase2_diameter);
    println!("two_phase_diameter\t{}", s.two_phase_diameter);
    println!("two_phase_exact_match_states\t{}", s.exact_match_states);
    println!("two_phase_max_gap\t{}", s.max_gap);

    for (gap, count) in s.gap_histogram.iter().enumerate() {
        println!("gap_{}\t{}", gap, count);
    }
    for (d, count) in s.geodesic_histogram.iter().enumerate() {
        println!("geodesic_d{}\t{}", d, count);
    }
    for (d, count) in s.two_phase_histogram.iter().enumerate() {
        println!("two_phase_d{}\t{}", d, count);
    }
    for (i, rank) in s.extremal_ranks.iter().enumerate() {
        println!("max_gap_rank_{}\t{}", i, rank);
    }
}
