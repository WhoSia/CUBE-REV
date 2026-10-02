use search_geometry_core::g6::{Cube, Face, Move, HTM, Phase1Moves, Phase1Pdb};

fn arg_value(args: &[String], key: &str) -> Option<String> {
    args.iter().position(|x| x == key).and_then(|i| args.get(i + 1)).cloned()
}

fn parse_token(raw: &str) -> Result<Move, String> {
    let t = raw.trim();
    if t.is_empty() {
        return Err("empty token".into());
    }
    let mut chars = t.chars();
    let face = match chars.next().unwrap() {
        'U' => Face::U,
        'R' => Face::R,
        'F' => Face::F,
        'D' => Face::D,
        'L' => Face::L,
        'B' => Face::B,
        _ => return Err(format!("unsupported HTM token: {t}")),
    };
    let suffix: String = chars.collect();
    let power = match suffix.as_str() {
        "" => 1,
        "2" | "2'" => 2,
        "'" => 3,
        _ => return Err(format!("unsupported HTM suffix: {t}")),
    };
    Ok(Move { face, power })
}

fn parse_alg(text: &str) -> Result<Vec<(String, Move)>, String> {
    text.split_whitespace()
        .filter(|x| !x.is_empty())
        .map(|x| Ok((x.to_string(), parse_token(x)?)))
        .collect()
}

fn state_signature(c: Cube) -> String {
    format!(
        "cp={:?};co={:?};ep={:?};eo={:?}",
        c.cp, c.co, c.ep, c.eo
    )
}

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let scramble = arg_value(&args, "--scramble").expect("--scramble required");
    let solution = arg_value(&args, "--solution").expect("--solution required");

    let scramble_moves = parse_alg(&scramble).unwrap_or_else(|e| panic!("SCRAMBLE_PARSE:{e}"));
    let solution_moves = parse_alg(&solution).unwrap_or_else(|e| panic!("SOLUTION_PARSE:{e}"));

    let mut cube = Cube::SOLVED;
    for (_, mv) in &scramble_moves {
        cube = cube.apply(*mv);
    }
    assert!(cube.validate(), "invalid scrambled state");

    println!("G7_P4_EXACT_REPLAY_PASS");
    println!("SCRAMBLE_MOVES\t{}", scramble_moves.len());
    println!("SOLUTION_MOVES\t{}", solution_moves.len());
    println!("START_PHASE1_RANK\t{}", cube.phase1().rank());
    println!("START_STATE\t{}", state_signature(cube));

    let phase1_moves = Phase1Moves::build();
    let phase1_pdb = Phase1Pdb::build(&phase1_moves);

    for (i, (raw, mv)) in solution_moves.iter().enumerate() {
        let before = cube.phase1();
        let h_before = phase1_pdb.lower_bound(before);
        let mut best_h = u8::MAX;
        let mut best_count = 0usize;
        for &rival in &HTM {
            let h = phase1_pdb.lower_bound(cube.apply(rival).phase1());
            if h < best_h {
                best_h = h;
                best_count = 1;
            } else if h == best_h {
                best_count += 1;
            }
        }

        cube = cube.apply(*mv);
        assert!(cube.validate(), "invalid prefix state");
        let h_after = phase1_pdb.lower_bound(cube.phase1());
        println!(
            "PREFIX\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
            i + 1,
            raw,
            cube.phase1().rank(),
            if cube.is_g1() { 1 } else { 0 },
            if cube.is_solved() { 1 } else { 0 },
            h_before,
            h_after,
            best_h,
            best_count
        );
    }
    println!("FINAL_SOLVED\t{}", if cube.is_solved() { 1 } else { 0 });
    println!("FINAL_STATE\t{}", state_signature(cube));
}
