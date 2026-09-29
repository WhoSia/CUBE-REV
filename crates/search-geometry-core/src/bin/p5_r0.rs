use search_geometry_core::run_full_court;

fn main() {
    let s = run_full_court(4);

    println!("metric\tvalue");
    println!("states\t{}", s.states);
    println!("phase2_subgroup_states\t{}", s.subgroup_states);
    println!("anchored_ruf_geodesic_diameter\t{}", s.geodesic_diameter);
    println!("orientation_layer_diameter\t{}", s.orientation_diameter);
    println!("phase2_restricted_diameter\t{}", s.phase2_diameter);

    for (d, count) in s.geodesic_histogram.iter().enumerate() {
        println!("geodesic_d{}\t{}", d, count);
    }

    for regime in &s.phase_slack {
        println!("slack_{}_diameter\t{}", regime.slack, regime.diameter);
        println!(
            "slack_{}_exact_match_states\t{}",
            regime.slack, regime.exact_match_states
        );
        println!("slack_{}_max_gap\t{}", regime.slack, regime.max_gap);

        for (gap, count) in regime.gap_histogram.iter().enumerate() {
            println!("slack_{}_gap_{}\t{}", regime.slack, gap, count);
        }
        for (i, rank) in regime.extremal_ranks.iter().enumerate() {
            println!("slack_{}_max_gap_rank_{}\t{}", regime.slack, i, rank);
        }
    }
}
