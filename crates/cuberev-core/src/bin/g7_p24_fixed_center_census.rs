use std::collections::{hash_map::Entry, HashMap, HashSet};
use std::env;
use std::fs::{self, File};
use std::hash::Hash;
use std::io::{BufRead, BufReader, BufWriter, Write};

const DOMAIN: u64 = 88_179_840;
const ORIENTATIONS: u64 = 2_187;
const FACE_ORDER: [u8; 6] = [b'U', b'R', b'F', b'D', b'L', b'B'];
const POS_FACES: [[u8; 3]; 8] = [
    [b'U', b'R', b'F'], [b'U', b'F', b'L'], [b'U', b'L', b'B'], [b'U', b'B', b'R'],
    [b'D', b'F', b'R'], [b'D', b'L', b'F'], [b'D', b'B', b'L'], [b'D', b'R', b'B'],
];
const CUBIE_COLORS: [[u8; 3]; 8] = POS_FACES;
const FACE_SLOTS: [[usize; 8]; 6] = [
    [0, 1, 2, 3, 99, 99, 99, 99],
    [0, 99, 99, 1, 2, 99, 99, 3],
    [0, 1, 99, 99, 2, 3, 99, 99],
    [99, 99, 99, 99, 0, 1, 2, 3],
    [99, 0, 1, 99, 99, 2, 3, 99],
    [99, 99, 0, 1, 99, 99, 2, 3],
];

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
struct State { cp: [u8; 8], co: [u8; 8] }

#[derive(Clone, Copy, Default)]
struct Fiber { count: u32, first: u32, second: u32 }

#[derive(Default)]
struct NatFiber { rows: u64, states: HashSet<u32> }

fn face_index(f: u8) -> usize { FACE_ORDER.iter().position(|&x| x == f).expect("face") }

fn factorial(n: usize) -> u64 {
    match n { 0 | 1 => 1, 2 => 2, 3 => 6, 4 => 24, 5 => 120, 6 => 720, 7 => 5040, 8 => 40320, _ => unreachable!() }
}

fn state_at(rank: u32) -> State {
    let perm_rank = rank as u64 / ORIENTATIONS;
    let ori_rank = rank as u64 % ORIENTATIONS;
    let mut available: Vec<u8> = (0..8).collect();
    let mut rem = perm_rank;
    let mut cp = [0u8; 8];
    for i in 0..8 {
        let f = factorial(7 - i);
        let digit = (rem / f) as usize;
        rem %= f;
        cp[i] = available.remove(digit);
    }
    let mut co = [0u8; 8];
    let mut sum = 0usize;
    let mut orem = ori_rank as usize;
    for i in 0..7 {
        let p = 3usize.pow((6 - i) as u32);
        co[i] = (orem / p) as u8;
        orem %= p;
        sum += co[i] as usize;
    }
    co[7] = ((3 - sum % 3) % 3) as u8;
    State { cp, co }
}

fn permutation_at(perm_rank: u64) -> [u8; 8] {
    let mut available: Vec<u8> = (0..8).collect();
    let mut rem = perm_rank;
    let mut cp = [0u8; 8];
    for i in 0..8 {
        let f = factorial(7 - i);
        let digit = (rem / f) as usize;
        rem %= f;
        cp[i] = available.remove(digit);
    }
    cp
}

fn orientation_at(ori_rank: u64, cp: [u8; 8]) -> State {
    let mut co = [0u8; 8];
    let mut sum = 0usize;
    let mut rem = ori_rank as usize;
    for i in 0..7 {
        let p = 3usize.pow((6 - i) as u32);
        co[i] = (rem / p) as u8;
        rem %= p;
        sum += co[i] as usize;
    }
    co[7] = ((3 - sum % 3) % 3) as u8;
    State { cp, co }
}

fn state_rank(s: State) -> u32 {
    let mut lehmer = 0u64;
    for i in 0..8 {
        let lower = s.cp[i + 1..].iter().filter(|&&x| x < s.cp[i]).count() as u64;
        lehmer += lower * factorial(7 - i);
    }
    let mut ori = 0u64;
    for &x in &s.co[..7] { ori = ori * 3 + x as u64; }
    (lehmer * ORIENTATIONS + ori) as u32
}

fn validate_state(s: State) {
    let mut cp = s.cp;
    cp.sort_unstable();
    assert_eq!(cp, [0, 1, 2, 3, 4, 5, 6, 7], "corner permutation legality");
    assert!(s.co.iter().all(|&x| x < 3), "corner orientation range");
    assert_eq!(s.co.iter().map(|&x| x as usize).sum::<usize>() % 3, 0, "corner twist constraint");
}

fn face_codes(s: State) -> [u8; 24] {
    let mut out = [255u8; 24];
    for pos in 0..8 {
        let cubie = s.cp[pos] as usize;
        let ori = s.co[pos] as usize;
        for k in 0..3 {
            let face = POS_FACES[pos][k];
            let color = CUBIE_COLORS[cubie][(k + 3 - ori) % 3];
            let idx = face_index(face) * 4 + FACE_SLOTS[face_index(face)][pos];
            assert!(out[idx] == 255, "duplicate physical sticker slot");
            out[idx] = FACE_ORDER.iter().position(|&x| x == color).unwrap() as u8;
        }
    }
    assert!(out.iter().all(|&x| x < 6), "incomplete six-face sticker record");
    out
}

fn obs_key(c: &[u8; 24], faces: &[u8]) -> u64 {
    let mut key = 0u64;
    for &face in faces {
        let fi = face_index(face);
        for j in 0..4 { key = (key << 4) | c[fi * 4 + j] as u64; }
    }
    key
}

fn fc6_key(c: &[u8; 24]) -> [u8; 12] {
    let mut out = [0u8; 12];
    for i in 0..12 { out[i] = (c[2 * i] << 4) | c[2 * i + 1]; }
    out
}

fn key_text(c: &[u8; 24], faces: &[u8]) -> String {
    let mut out = String::new();
    for &face in faces {
        let fi = face_index(face);
        for j in 0..4 { out.push(FACE_ORDER[c[fi * 4 + j] as usize] as char); }
    }
    out
}

fn build_decoder() -> [[[u8; 2]; 216]; 8] {
    let mut table = [[[255u8; 2]; 216]; 8];
    for pos in 0..8 {
        for cubie in 0..8 {
            for ori in 0..3 {
                let mut ix = 0usize;
                for k in 0..3 {
                    let color = CUBIE_COLORS[cubie][(k + 3 - ori) % 3];
                    ix = ix * 6 + FACE_ORDER.iter().position(|&x| x == color).unwrap();
                }
                assert_eq!(table[pos][ix][0], 255, "FC6 decoder is not unique");
                table[pos][ix] = [cubie as u8, ori as u8];
            }
        }
    }
    table
}

fn reconstruct_fc6(c: &[u8; 24], decoder: &[[[u8; 2]; 216]; 8]) -> State {
    let mut cp = [255u8; 8];
    let mut co = [255u8; 8];
    for pos in 0..8 {
        let mut ix = 0usize;
        for &face in &POS_FACES[pos] {
            let fi = face_index(face);
            ix = ix * 6 + c[fi * 4 + FACE_SLOTS[fi][pos]] as usize;
        }
        let pair = decoder[pos][ix];
        assert!(pair[0] < 8 && pair[1] < 3, "FC6 inverse rejected a corner sticker triple");
        cp[pos] = pair[0];
        co[pos] = pair[1];
    }
    let s = State { cp, co };
    validate_state(s);
    s
}

fn regression_witness() -> (String, String) {
    let a = State { cp: [2, 0, 5, 3, 7, 1, 6, 4], co: [0, 0, 2, 0, 2, 2, 1, 2] };
    let b = State { cp: [2, 0, 6, 3, 7, 1, 5, 4], co: [0, 0, 1, 0, 2, 2, 2, 2] };
    validate_state(a); validate_state(b);
    let ca = face_codes(a); let cb = face_codes(b);
    let a4 = key_text(&ca, b"UFRD"); let b4 = key_text(&cb, b"UFRD");
    let a3 = key_text(&ca, b"UFR"); let b3 = key_text(&cb, b"UFR");
    assert_eq!(a4, "UULUBRBULRDRRFLF", "frozen FC4 witness key drift");
    assert_eq!(a4, b4, "frozen FC4 witness collision not reproduced");
    assert_eq!(a3, b3, "frozen FC3 witness collision not reproduced");
    assert_ne!(a, b, "witness states must differ");
    (a4, a3)
}

fn insert_fiber(map: &mut HashMap<u64, Fiber>, key: u64, rank: u32) -> bool {
    match map.entry(key) {
        Entry::Vacant(v) => { v.insert(Fiber { count: 1, first: rank, second: 0 }); true }
        Entry::Occupied(mut o) => {
            let f = o.get_mut();
            if f.count == 1 { f.second = rank; }
            f.count += 1;
            false
        }
    }
}

fn summarize(map: &HashMap<u64, Fiber>) -> (Vec<(u32, u64)>, u32) {
    let mut h: HashMap<u32, u64> = HashMap::new();
    let mut max = 0;
    for f in map.values() { *h.entry(f.count).or_insert(0) += 1; max = max.max(f.count); }
    let mut v: Vec<_> = h.into_iter().collect(); v.sort_unstable(); (v, max)
}

fn first_collision(map: &HashMap<u64, Fiber>) -> (u64, Fiber) {
    map.iter().filter(|(_, f)| f.count > 1)
        .map(|(&k, &f)| (k, f))
        .min_by_key(|(_, f)| (f.first, f.second))
        .expect("noninjective operator must have collision")
}

fn parse_eight(s: &str) -> [u8; 8] {
    let v: Vec<u8> = s.split(',').map(|x| x.parse::<u8>().expect("integer field")).collect();
    v.try_into().expect("eight cubie coordinates")
}

fn add_nat<K: Eq + Hash>(map: &mut HashMap<K, NatFiber>, key: K, rows: u64, state: u32) {
    let f = map.entry(key).or_default(); f.rows += rows; f.states.insert(state);
}

fn summarize_nat<K: Eq + Hash>(map: &HashMap<K, NatFiber>) -> (u64, u64, u64, u64) {
    let mut keys = 0; let mut rows = 0; let mut pairs = 0; let mut max_distinct = 0;
    for f in map.values() {
        if f.states.len() > 1 { keys += 1; rows += f.rows; }
        let n = f.states.len() as u64; pairs += n * (n - 1) / 2; max_distinct = max_distinct.max(n);
    }
    (keys, rows, pairs, max_distinct)
}

fn hex_u64(x: u64, digits: usize) -> String { format!("{x:0digits$x}") }
fn hex_fc6(x: [u8; 12]) -> String { x.iter().map(|b| format!("{b:02x}")).collect() }

fn run(corpus_path: &str, outdir: &str) {
    let decoder = build_decoder();
    let (fixture4, fixture3) = regression_witness();
    fs::create_dir_all(outdir).expect("output directory");

    let mut fc4: HashMap<u64, Fiber> = HashMap::with_capacity(45_000_000);
    let mut fc3: HashMap<u64, Fiber> = HashMap::with_capacity(12_000_000);
    let mut fc3_fc4: HashMap<u64, u32> = HashMap::with_capacity(12_000_000);
    let mut inverse_ok = 0u64;
    for perm_rank in 0..40_320u64 {
      let cp = permutation_at(perm_rank);
      for ori_rank in 0..ORIENTATIONS {
        let rank = (perm_rank * ORIENTATIONS + ori_rank) as u32;
        let s = orientation_at(ori_rank, cp);
        validate_state(s);
        assert_eq!(state_rank(s), rank, "enumerator rank/unrank mismatch");
        let c = face_codes(s);
        let back = reconstruct_fc6(&c, &decoder);
        assert_eq!(back, s, "FC6 inverse/reconstruction mismatch at rank {rank}");
        inverse_ok += 1;
        let k4 = obs_key(&c, b"UFRD");
        let k3 = obs_key(&c, b"UFR");
        let was_new4 = insert_fiber(&mut fc4, k4, rank);
        insert_fiber(&mut fc3, k3, rank);
        if was_new4 { *fc3_fc4.entry(k3).or_insert(0) += 1; }
      }
    }
    assert_eq!(inverse_ok, DOMAIN);
    let unique4 = fc4.len(); let unique3 = fc3.len();
    let (h4, max4) = summarize(&fc4); let (h3, max3) = summarize(&fc3);
    let (collision4, fiber4) = first_collision(&fc4);
    let (collision3, fiber3) = first_collision(&fc3);
    let mut fc3_split = 0u64; let mut max_fc4_per_fc3 = 0u32;
    for &n in fc3_fc4.values() { if n > 1 { fc3_split += 1; } max_fc4_per_fc3 = max_fc4_per_fc3.max(n); }
    assert!(fc3_split > 0, "FC3-to-FC4 reverse refinement falsifier absent");
    assert!(fc4.len() < DOMAIN as usize && fc3.len() < DOMAIN as usize);
    assert_eq!(fc3_fc4.len(), fc3.len(), "FC4 restriction must map to one FC3 parent");
    drop(fc4); drop(fc3); drop(fc3_fc4);

    let reader = BufReader::new(File::open(corpus_path).expect("open admitted corpus rows"));
    let mut out = BufWriter::new(File::create(format!("{outdir}/observations.tsv")).expect("create serialized observations"));
    let mut nat6: HashMap<[u8; 12], NatFiber> = HashMap::new();
    let mut nat4: HashMap<u64, NatFiber> = HashMap::new();
    let mut nat3: HashMap<u64, NatFiber> = HashMap::new();
    let mut rows = 0u64; let mut ids: HashSet<String> = HashSet::new(); let mut previous: Option<(String, u32)> = None;
    for line in reader.lines() {
        let line = line.expect("read corpus row"); if line.is_empty() { continue; }
        let p: Vec<&str> = line.split('\t').collect(); assert_eq!(p.len(), 4, "corpus TSV schema");
        let source_hex = p[0].to_owned();
        assert!(!source_hex.is_empty() && source_hex.len() % 2 == 0 && source_hex.bytes().all(|b| b.is_ascii_hexdigit()), "source id must be hex UTF-8");
        let prefix: u32 = p[1].parse().expect("prefix index");
        if let Some((ref last_id, last_prefix)) = previous {
            assert!(source_hex > *last_id || (source_hex == *last_id && prefix > last_prefix), "corpus rows not strictly source/prefix ordered");
        }
        previous = Some((source_hex.clone(), prefix)); ids.insert(source_hex.clone());
        let s = State { cp: parse_eight(p[2]), co: parse_eight(p[3]) }; validate_state(s);
        let rank = state_rank(s); assert_eq!(state_at(rank), s, "corpus state outside legal domain");
        let c = face_codes(s); let back = reconstruct_fc6(&c, &decoder); assert_eq!(back, s, "naturalistic FC6 reconstruction mismatch");
        let full = fc6_key(&c); let k4 = obs_key(&c, b"UFRD"); let k3 = obs_key(&c, b"UFR");
        add_nat(&mut nat6, full, 1, rank); add_nat(&mut nat4, k4, 1, rank); add_nat(&mut nat3, k3, 1, rank);
        writeln!(out, "{source_hex}\t{prefix}\t{rank}\t{}\t{}\t{}", hex_fc6(full), hex_u64(k4, 16), hex_u64(k3, 12)).expect("write deterministic serialization");
        rows += 1;
    }
    out.flush().expect("flush observations");
    let (c4_keys, c4_rows, c4_pairs, c4_max) = summarize_nat(&nat4);
    let (c3_keys, c3_rows, c3_pairs, c3_max) = summarize_nat(&nat3);
    let (c6_keys, c6_rows, c6_pairs, c6_max) = summarize_nat(&nat6);
    assert!(rows > 0 && ids.len() == 60, "admitted exact-replay corpus must contain 60 unique source IDs");
    assert!(nat6.len() as u64 <= rows, "unique observations cannot exceed corpus rows");

    let hist = |h: &[(u32, u64)]| h.iter().map(|(k, n)| format!("\"{k}\":{n}")).collect::<Vec<_>>().join(",");
    let witness = |f: Fiber, key: u64| {
        let a = state_at(f.first); let b = state_at(f.second);
        format!("{{\"key_hex\":\"{}\",\"rank_a\":{},\"cp_a\":{:?},\"co_a\":{:?},\"rank_b\":{},\"cp_b\":{:?},\"co_b\":{:?}}}", hex_u64(key, 16), f.first, a.cp, a.co, f.second, b.cp, b.co)
    };
    let head = env::var("P24_HEAD").unwrap_or_else(|_| "LOCAL_UNBOUND".into());
    let corpus_sha = env::var("P24_CORPUS_INPUT_SHA256").unwrap_or_else(|_| "LOCAL_UNBOUND".into());
    let q24 = r#"{"source":"G7-P23-R1 CLOSED/PASS; run 37573665425; artifact 11461892552; receipt SHA-256 639b6665f1f7f4b10b4c31ac9185f27da4ca098c0b82e9f0c909aed6a5e1be19","source_domain":88179840,"gauge_classes":3674160,"source_fiber_size":24,"fixed_center_FC4_noninvariant_classes":3674160,"Q24_equality_implies_FC4_equality":false,"meaning":"gauge-normalized comparator only; never a fixed-center operator"}"#;
    let receipt = format!(
        "{{\n  \"schema\":\"g7-p24-fixed-center-census-v1\",\n  \"science_head\":\"{head}\",\n  \"source_domain\":{DOMAIN},\n  \"enumeration\":\"Lehmer(cp)*2187 + base3(co[0..7]); co[7] closes zero-sum\",\n  \"FC6_C\":{{\"unique_keys\":{DOMAIN},\"singleton_fibers\":{DOMAIN},\"inverse_roundtrips\":{inverse_ok},\"inverse_consistency\":true}},\n  \"FC4_C\":{{\"unique_keys\":{},\"max_fiber\":{},\"fiber_histogram\":{{{}}},\"first_collision\":{}}},\n  \"FC3_C\":{{\"unique_keys\":{},\"max_fiber\":{},\"fiber_histogram\":{{{}}},\"first_collision\":{}}},\n  \"refinement\":{{\"FC6_equal_implies_FC4_equal\":true,\"FC6_equal_implies_FC3_equal\":true,\"FC4_equal_implies_FC3_equal\":true,\"FC3_fibers_with_multiple_FC4_keys\":{fc3_split},\"max_distinct_FC4_keys_per_FC3_key\":{max_fc4_per_fc3},\"FC4_to_FC3_is_function\":true}},\n  \"Q24_C_comparator\":\"{}\",\n  \"presealed_witness_regression\":{{\"PASS\":true,\"FC4_key\":\"{}\",\"FC3_key\":\"{}\"}},\n  \"naturalistic\":{{\"source_contact\":\"NONE\",\"input_sha256\":\"{}\",\"source_ids\":{},\"rows\":{rows},\"serialization_success\":true,\"unique_FC6\":{},\"unique_FC4\":{},\"unique_FC3\":{},\"FC4_multistate_keys\":{c4_keys},\"FC4_rows_in_multistate_fibers\":{c4_rows},\"FC4_distinct_state_pairs\":{c4_pairs},\"FC4_max_distinct_states_per_key\":{c4_max},\"FC4_distinct_state_collision_present\":{},\"FC3_multistate_keys\":{c3_keys},\"FC3_rows_in_multistate_fibers\":{c3_rows},\"FC3_distinct_state_pairs\":{c3_pairs},\"FC3_max_distinct_states_per_key\":{c3_max},\"FC3_distinct_state_collision_present\":{}}}\n}}\n",
        unique4, max4, hist(&h4), witness(fiber4, collision4),
        unique3, max3, hist(&h3), witness(fiber3, collision3), q24, fixture4, fixture3,
        corpus_sha, ids.len(), nat6.len(), nat4.len(), nat3.len(), c4_pairs > 0, c3_pairs > 0
    ).replace(&format!("\"Q24_C_comparator\":\"{q24}\""), &format!("\"Q24_C_comparator\":{q24}"))
     .replace("\"FC4_multistate_keys\":", &format!("\"FC6_multistate_keys\":{c6_keys},\"FC6_rows_in_multistate_fibers\":{c6_rows},\"FC6_distinct_state_pairs\":{c6_pairs},\"FC6_max_distinct_states_per_key\":{c6_max},\"FC6_distinct_state_collision_present\":{},\"FC4_multistate_keys\":", c6_pairs > 0));
    assert_eq!((c6_keys, c6_rows, c6_pairs, c6_max), (0, 0, 0, 1), "FC6 must have no naturalistic distinct-state collisions");
    fs::write(format!("{outdir}/receipt.json"), receipt).expect("write receipt");
    println!("G7_P24_FIXED_CENTER_CENSUS_PASS");
    println!("DOMAIN\t{DOMAIN}");
    println!("FC6_UNIQUE\t{DOMAIN}\tSINGLETON_FIBERS\t{DOMAIN}\tINVERSE\t{inverse_ok}");
    println!("FC4_UNIQUE\t{}\tMAX\t{}\tHIST\t{}", unique4, max4, hist(&h4));
    println!("FC3_UNIQUE\t{}\tMAX\t{}\tHIST\t{}", unique3, max3, hist(&h3));
    println!("NATURALISTIC_ROWS\t{rows}\tSOURCE_IDS\t{}\tFC4_COLLISION_ROWS\t{c4_rows}\tFC3_COLLISION_ROWS\t{c3_rows}", ids.len());
    println!("NATURALISTIC_FC6_COLLISION_KEYS\t{c6_keys}\tROWS\t{c6_rows}\tDISTINCT_STATE_PAIRS\t{c6_pairs}");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    assert!(args.len() == 3, "usage: g7_p24_fixed_center_census <corpus.tsv> <outdir>");
    run(&args[1], &args[2]);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn frozen_collision_witness_and_key_regression() {
        let (fc4, fc3) = regression_witness();
        assert_eq!(fc4, "UULUBRBULRDRRFLF");
        assert_eq!(fc3, "UULUBRBULRDR");
    }

    #[test]
    fn source_rank_roundtrips_at_boundaries_and_samples() {
        for rank in [0, 1, 2_186, 2_187, 2_188, 40_319 * 2_187, DOMAIN as u32 - 1] {
            let s = state_at(rank);
            validate_state(s);
            assert_eq!(state_rank(s), rank);
        }
    }

    #[test]
    fn fc6_roundtrip_for_sampled_legal_states() {
        let decoder = build_decoder();
        for rank in [0, 17, 2_186, 2_187, 1_234_567, DOMAIN as u32 - 1] {
            let s = state_at(rank);
            assert_eq!(reconstruct_fc6(&face_codes(s), &decoder), s);
        }
    }
}

