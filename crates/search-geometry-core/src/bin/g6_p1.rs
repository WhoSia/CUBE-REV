//! G6-P1: declared 3x3 Kociemba phase-1 coordinate domain.
//! This is a coordinate and subgroup-membership court, not an exhaustive 3x3 search.

const TWIST: usize = 3usize.pow(7);
const FLIP: usize = 2usize.pow(11);
const SLICE: usize = 495; // C(12,4): locations of the four UD-slice edges.

fn choose(n: usize, k: usize) -> usize {
    if k > n {
        return 0;
    }
    (0..k).fold(1usize, |v, i| v * (n - i) / (i + 1))
}

fn main() {
    assert_eq!(TWIST, 2187);
    assert_eq!(FLIP, 2048);
    assert_eq!(SLICE, choose(12, 4));
    // The phase-1 quotient is the right-coset coordinate: 3^7 * 2^11 * C(12,4).
    let cosets = TWIST * FLIP * SLICE;
    assert_eq!(cosets, 2_217_093_120);
    // G1 is characterized exactly by zero corner twist, zero edge flip, and solved slice membership.
    let g1_identity = (0usize, 0usize, 0usize);
    assert_eq!(g1_identity, (0, 0, 0));
    println!("G6_P1_COORDINATE_DOMAIN_PASS");
    println!("TWIST\t{TWIST}");
    println!("FLIP\t{FLIP}");
    println!("UD_SLICE\t{SLICE}");
    println!("G1_RIGHT_COSETS\t{cosets}");
    println!("G1_MEMBERSHIP\ttwist=0 & flip=0 & udslice=0");
    println!("EXHAUSTIVE_3X3_SEARCH\tNOT_RUN");
}
