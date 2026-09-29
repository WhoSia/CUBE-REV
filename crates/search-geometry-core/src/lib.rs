//! CUBE-REV Generation V G5-P5 exact search-representation geometry.
//!
//! Authority ceiling:
//! - exact 2x2 rotation-quotiented corner state space;
//! - anchored R/U/F half-turn metric only;
//! - no claim of equivalence to the ordinary six-face HTM until separately proved;
//! - Kociemba is a design donor, not a priority claim or cognitive model.

use cuberev_core::{CornerState, ORIENTATIONS, PERMUTATIONS, STATE_DOMAIN};
use std::collections::VecDeque;

const ACTIVE_CORNERS: [u8; 7] = [0, 1, 2, 3, 4, 5, 7];

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum Face {
    U,
    R,
    F,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct Move {
    pub face: Face,
    pub power: u8,
}

pub const FULL_MOVES: [Move; 9] = [
    Move { face: Face::U, power: 1 },
    Move { face: Face::U, power: 2 },
    Move { face: Face::U, power: 3 },
    Move { face: Face::R, power: 1 },
    Move { face: Face::R, power: 2 },
    Move { face: Face::R, power: 3 },
    Move { face: Face::F, power: 1 },
    Move { face: Face::F, power: 2 },
    Move { face: Face::F, power: 3 },
];

pub const PHASE2_MOVE_INDICES: [usize; 5] = [0, 1, 2, 4, 7];

#[derive(Clone)]
pub struct TransitionTables {
    perm: Vec<[u16; 9]>,
    ori: Vec<[u16; 9]>,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct SearchGeometrySummary {
    pub states: u32,
    pub subgroup_states: u32,
    pub geodesic_diameter: u8,
    pub orientation_diameter: u8,
    pub phase2_diameter: u8,
    pub two_phase_diameter: u8,
    pub exact_match_states: u32,
    pub max_gap: u8,
    pub gap_histogram: Vec<u32>,
    pub geodesic_histogram: Vec<u32>,
    pub two_phase_histogram: Vec<u32>,
    pub extremal_ranks: Vec<u32>,
}

impl TransitionTables {
    pub fn build() -> Self {
        let mut perm = vec![[0u16; 9]; PERMUTATIONS as usize];
        let mut ori = vec![[0u16; 9]; ORIENTATIONS as usize];

        for p in 0..PERMUTATIONS {
            let state = CornerState::unrank(p * ORIENTATIONS).expect("valid permutation state");
            for (m, mv) in FULL_MOVES.iter().enumerate() {
                let next = apply_move(&state, *mv);
                perm[p as usize][m] =
                    (next.rank().expect("valid moved state") / ORIENTATIONS) as u16;
            }
        }

        for o in 0..ORIENTATIONS {
            let state = CornerState::unrank(o).expect("valid orientation state");
            for (m, mv) in FULL_MOVES.iter().enumerate() {
                let next = apply_move(&state, *mv);
                ori[o as usize][m] =
                    (next.rank().expect("valid moved state") % ORIENTATIONS) as u16;
            }
        }

        Self { perm, ori }
    }

    pub fn next_rank(&self, rank: u32, move_index: usize) -> u32 {
        let p = rank / ORIENTATIONS;
        let o = rank % ORIENTATIONS;
        self.perm[p as usize][move_index] as u32 * ORIENTATIONS
            + self.ori[o as usize][move_index] as u32
    }

    pub fn next_perm(&self, perm_rank: u32, move_index: usize) -> u32 {
        self.perm[perm_rank as usize][move_index] as u32
    }

    pub fn next_ori(&self, ori_rank: u32, move_index: usize) -> u32 {
        self.ori[ori_rank as usize][move_index] as u32
    }
}

pub fn apply_move(state: &CornerState, mv: Move) -> CornerState {
    assert!((1..=3).contains(&mv.power));
    let mut out = state.clone();
    for _ in 0..mv.power {
        out = apply_quarter(&out, mv.face);
    }
    out
}

fn apply_quarter(state: &CornerState, face: Face) -> CornerState {
    let (cp, co) = quarter_table(face);
    let mut full_perm = [0u8; 8];
    let mut full_ori = [0u8; 8];

    for (compressed_pos, &full_pos) in ACTIVE_CORNERS.iter().enumerate() {
        full_perm[full_pos as usize] = ACTIVE_CORNERS[state.perm[compressed_pos] as usize];
        full_ori[full_pos as usize] = state.ori[compressed_pos];
    }
    full_perm[6] = 6;
    full_ori[6] = 0;

    let mut next_perm = [0u8; 8];
    let mut next_ori = [0u8; 8];
    for pos in 0..8 {
        next_perm[pos] = full_perm[cp[pos]];
        next_ori[pos] = (full_ori[cp[pos]] + co[pos]) % 3;
    }

    assert_eq!(next_perm[6], 6, "anchored generators must preserve DBL corner");
    assert_eq!(next_ori[6], 0, "anchored generators must preserve DBL orientation");

    let mut perm = [0u8; 7];
    let mut ori = [0u8; 7];
    for (compressed_pos, &full_pos) in ACTIVE_CORNERS.iter().enumerate() {
        perm[compressed_pos] = active_index(next_perm[full_pos as usize]);
        ori[compressed_pos] = next_ori[full_pos as usize];
    }

    let next = CornerState { perm, ori };
    next.validate().expect("legal cubie move");
    next
}

fn quarter_table(face: Face) -> ([usize; 8], [u8; 8]) {
    match face {
        Face::U => ([3, 0, 1, 2, 4, 5, 6, 7], [0; 8]),
        Face::R => (
            [4, 1, 2, 0, 7, 5, 6, 3],
            [2, 0, 0, 1, 1, 0, 0, 2],
        ),
        Face::F => (
            [1, 5, 2, 3, 0, 4, 6, 7],
            [1, 2, 0, 0, 2, 1, 0, 0],
        ),
    }
}

fn active_index(full_cubie: u8) -> u8 {
    ACTIVE_CORNERS
        .iter()
        .position(|&c| c == full_cubie)
        .expect("non-reference cubie") as u8
}

pub fn phase2_subgroup_census(tables: &TransitionTables) -> Vec<bool> {
    let mut seen = vec![false; PERMUTATIONS as usize];
    let mut queue = VecDeque::new();
    seen[0] = true;
    queue.push_back(0u32);

    while let Some(p) = queue.pop_front() {
        for &m in &PHASE2_MOVE_INDICES {
            assert_eq!(tables.next_ori(0, m), 0, "phase-2 move twists a corner");
            let next = tables.next_perm(p, m);
            if !seen[next as usize] {
                seen[next as usize] = true;
                queue.push_back(next);
            }
        }
    }
    seen
}

pub fn bfs_geodesic(tables: &TransitionTables) -> Vec<u8> {
    let mut dist = vec![u8::MAX; STATE_DOMAIN as usize];
    let mut queue = VecDeque::new();
    dist[0] = 0;
    queue.push_back(0u32);

    while let Some(rank) = queue.pop_front() {
        let d = dist[rank as usize];
        for m in 0..FULL_MOVES.len() {
            let next = tables.next_rank(rank, m);
            if dist[next as usize] == u8::MAX {
                dist[next as usize] = d + 1;
                queue.push_back(next);
            }
        }
    }
    dist
}

pub fn bfs_orientation_distance(tables: &TransitionTables) -> Vec<u8> {
    let mut dist = vec![u8::MAX; ORIENTATIONS as usize];
    let mut queue = VecDeque::new();
    dist[0] = 0;
    queue.push_back(0u32);

    while let Some(o) = queue.pop_front() {
        let d = dist[o as usize];
        for m in 0..FULL_MOVES.len() {
            let next = tables.next_ori(o, m);
            if dist[next as usize] == u8::MAX {
                dist[next as usize] = d + 1;
                queue.push_back(next);
            }
        }
    }
    dist
}

pub fn bfs_phase2_distance(tables: &TransitionTables) -> Vec<u8> {
    let mut dist = vec![u8::MAX; PERMUTATIONS as usize];
    let mut queue = VecDeque::new();
    dist[0] = 0;
    queue.push_back(0u32);

    while let Some(p) = queue.pop_front() {
        let d = dist[p as usize];
        for &m in &PHASE2_MOVE_INDICES {
            let next = tables.next_perm(p, m);
            if dist[next as usize] == u8::MAX {
                dist[next as usize] = d + 1;
                queue.push_back(next);
            }
        }
    }
    dist
}

pub fn exact_two_phase_distance(
    tables: &TransitionTables,
    phase2_dist: &[u8],
) -> Vec<u8> {
    assert_eq!(phase2_dist.len(), PERMUTATIONS as usize);
    let mut dist = vec![u8::MAX; STATE_DOMAIN as usize];
    let mut buckets: Vec<VecDeque<u32>> = (0..64).map(|_| VecDeque::new()).collect();

    for p in 0..PERMUTATIONS {
        let cost = phase2_dist[p as usize];
        assert_ne!(cost, u8::MAX);
        let rank = p * ORIENTATIONS;
        dist[rank as usize] = cost;
        buckets[cost as usize].push_back(rank);
    }

    let mut current = 0usize;
    while current < buckets.len() {
        while let Some(rank) = buckets[current].pop_front() {
            if dist[rank as usize] as usize != current {
                continue;
            }
            let next_cost = current + 1;
            if next_cost >= buckets.len() {
                buckets.push(VecDeque::new());
            }
            for m in 0..FULL_MOVES.len() {
                let next = tables.next_rank(rank, m);
                if next_cost < dist[next as usize] as usize {
                    dist[next as usize] = next_cost as u8;
                    buckets[next_cost].push_back(next);
                }
            }
        }
        current += 1;
    }

    dist
}

pub fn run_full_court() -> SearchGeometrySummary {
    let tables = TransitionTables::build();

    let subgroup = phase2_subgroup_census(&tables);
    let subgroup_states = subgroup.iter().filter(|&&x| x).count() as u32;
    assert_eq!(subgroup_states, PERMUTATIONS);

    let geodesic = bfs_geodesic(&tables);
    assert!(geodesic.iter().all(|&d| d != u8::MAX));

    let orientation = bfs_orientation_distance(&tables);
    assert!(orientation.iter().all(|&d| d != u8::MAX));

    let phase2 = bfs_phase2_distance(&tables);
    assert!(phase2.iter().all(|&d| d != u8::MAX));

    let two_phase = exact_two_phase_distance(&tables, &phase2);
    assert!(two_phase.iter().all(|&d| d != u8::MAX));

    let geodesic_diameter = *geodesic.iter().max().unwrap();
    let orientation_diameter = *orientation.iter().max().unwrap();
    let phase2_diameter = *phase2.iter().max().unwrap();
    let two_phase_diameter = *two_phase.iter().max().unwrap();

    let mut gap_histogram = vec![0u32; 1];
    let mut geodesic_histogram = vec![0u32; geodesic_diameter as usize + 1];
    let mut two_phase_histogram = vec![0u32; two_phase_diameter as usize + 1];
    let mut exact_match_states = 0u32;
    let mut max_gap = 0u8;
    let mut extremal_ranks = Vec::new();

    for rank in 0..STATE_DOMAIN {
        let dg = geodesic[rank as usize];
        let d2 = two_phase[rank as usize];
        assert!(d2 >= dg, "two-phase distance undercut unrestricted geodesic");
        geodesic_histogram[dg as usize] += 1;
        two_phase_histogram[d2 as usize] += 1;

        let gap = d2 - dg;
        if gap as usize >= gap_histogram.len() {
            gap_histogram.resize(gap as usize + 1, 0);
        }
        gap_histogram[gap as usize] += 1;

        if gap == 0 {
            exact_match_states += 1;
        }
        if gap > max_gap {
            max_gap = gap;
            extremal_ranks.clear();
            extremal_ranks.push(rank);
        } else if gap == max_gap && extremal_ranks.len() < 32 {
            extremal_ranks.push(rank);
        }
    }

    SearchGeometrySummary {
        states: STATE_DOMAIN,
        subgroup_states,
        geodesic_diameter,
        orientation_diameter,
        phase2_diameter,
        two_phase_diameter,
        exact_match_states,
        max_gap,
        gap_histogram,
        geodesic_histogram,
        two_phase_histogram,
        extremal_ranks,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn each_quarter_turn_has_order_four() {
        let samples = [0, 1, 728, 729, STATE_DOMAIN - 1];
        for rank in samples {
            let state = CornerState::unrank(rank).unwrap();
            for face in [Face::U, Face::R, Face::F] {
                let mut x = state.clone();
                for _ in 0..4 {
                    x = apply_move(&x, Move { face, power: 1 });
                }
                assert_eq!(x, state);
            }
        }
    }

    #[test]
    fn factored_transition_matches_direct_move() {
        let tables = TransitionTables::build();
        let samples = [0, 1, 728, 729, 91_337, STATE_DOMAIN - 1];
        for rank in samples {
            let state = CornerState::unrank(rank).unwrap();
            for (m, mv) in FULL_MOVES.iter().enumerate() {
                let direct = apply_move(&state, *mv).rank().unwrap();
                assert_eq!(tables.next_rank(rank, m), direct);
            }
        }
    }

    #[test]
    fn phase2_generators_span_every_orientation_solved_permutation() {
        let tables = TransitionTables::build();
        let seen = phase2_subgroup_census(&tables);
        assert_eq!(seen.iter().filter(|&&x| x).count(), 5_040);
        for &m in &PHASE2_MOVE_INDICES {
            assert_eq!(tables.next_ori(0, m), 0);
        }
    }

    #[test]
    fn orientation_coordinate_is_fully_reachable() {
        let tables = TransitionTables::build();
        let dist = bfs_orientation_distance(&tables);
        assert_eq!(dist.len(), 729);
        assert!(dist.iter().all(|&d| d != u8::MAX));
    }
}
