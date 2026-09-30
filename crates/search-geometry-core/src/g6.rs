//! 3x3 phase-1 Schreier coordinate oracle and Kociemba-style projected PDBs.
//! Move convention matches Kociemba CubieCube: position arrays, right composition.

use std::collections::{HashMap, HashSet, VecDeque};
use std::sync::OnceLock;

pub const TWIST_COUNT: usize = 2_187;
pub const FLIP_COUNT: usize = 2_048;
pub const SLICE_COUNT: usize = 495;
pub const COSET_COUNT: usize = TWIST_COUNT * FLIP_COUNT * SLICE_COUNT;
pub const MOVE_COUNT: usize = 18;

#[derive(Clone, Copy, Debug, Eq, PartialEq, Hash)]
#[repr(u8)]
pub enum Face {
    U,
    R,
    F,
    D,
    L,
    B,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq, Hash)]
pub struct Move {
    pub face: Face,
    pub power: u8,
}

pub const HTM: [Move; MOVE_COUNT] = [
    Move {
        face: Face::U,
        power: 1,
    },
    Move {
        face: Face::U,
        power: 2,
    },
    Move {
        face: Face::U,
        power: 3,
    },
    Move {
        face: Face::R,
        power: 1,
    },
    Move {
        face: Face::R,
        power: 2,
    },
    Move {
        face: Face::R,
        power: 3,
    },
    Move {
        face: Face::F,
        power: 1,
    },
    Move {
        face: Face::F,
        power: 2,
    },
    Move {
        face: Face::F,
        power: 3,
    },
    Move {
        face: Face::D,
        power: 1,
    },
    Move {
        face: Face::D,
        power: 2,
    },
    Move {
        face: Face::D,
        power: 3,
    },
    Move {
        face: Face::L,
        power: 1,
    },
    Move {
        face: Face::L,
        power: 2,
    },
    Move {
        face: Face::L,
        power: 3,
    },
    Move {
        face: Face::B,
        power: 1,
    },
    Move {
        face: Face::B,
        power: 2,
    },
    Move {
        face: Face::B,
        power: 3,
    },
];

#[derive(Clone, Copy, Debug, Eq, PartialEq, Hash)]
pub struct Cube {
    pub cp: [u8; 8],
    pub co: [u8; 8],
    pub ep: [u8; 12],
    pub eo: [u8; 12],
}

impl Cube {
    pub const SOLVED: Self = Self {
        cp: [0, 1, 2, 3, 4, 5, 6, 7],
        co: [0; 8],
        ep: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        eo: [0; 12],
    };

    pub fn apply(self, mv: Move) -> Self {
        assert!((1..=3).contains(&mv.power));
        let mut out = self;
        for _ in 0..mv.power {
            out = out.quarter(mv.face);
        }
        out
    }

    fn quarter(self, face: Face) -> Self {
        let (cp, co, ep, eo) = basic_move(face);
        let mut out = Self::SOLVED;
        for i in 0..8 {
            out.cp[i] = self.cp[cp[i] as usize];
            out.co[i] = (self.co[cp[i] as usize] + co[i]) % 3;
        }
        for i in 0..12 {
            out.ep[i] = self.ep[ep[i] as usize];
            out.eo[i] = (self.eo[ep[i] as usize] + eo[i]) % 2;
        }
        out
    }

    pub fn phase1(self) -> Phase1 {
        let mut twist = 0usize;
        for &x in &self.co[..7] {
            twist = twist * 3 + x as usize;
        }
        let mut flip = 0usize;
        for &x in &self.eo[..11] {
            flip = (flip << 1) | x as usize;
        }
        let mut mask = 0u16;
        for (pos, &cubie) in self.ep.iter().enumerate() {
            if cubie >= 8 {
                mask |= 1 << pos;
            }
        }
        Phase1 {
            twist: twist as u16,
            flip: flip as u16,
            slice: subset_rank(mask),
        }
    }

    pub fn is_solved(self) -> bool {
        self == Self::SOLVED
    }

    pub fn validate(self) -> bool {
        let mut corners = self.cp.to_vec();
        corners.sort_unstable();
        let mut edges = self.ep.to_vec();
        edges.sort_unstable();
        corners == (0..8).collect::<Vec<_>>()
            && edges == (0..12).collect::<Vec<_>>()
            && self.co.iter().all(|&x| x < 3)
            && self.co.iter().map(|&x| x as usize).sum::<usize>() % 3 == 0
            && self.eo.iter().all(|&x| x < 2)
            && self.eo.iter().map(|&x| x as usize).sum::<usize>() % 2 == 0
            && parity(&self.cp) == parity(&self.ep)
    }
}

fn basic_move(f: Face) -> ([u8; 8], [u8; 8], [u8; 12], [u8; 12]) {
    use Face::*;
    match f {
        U => (
            [3, 0, 1, 2, 4, 5, 6, 7],
            [0; 8],
            [3, 0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11],
            [0; 12],
        ),
        R => (
            [4, 1, 2, 0, 7, 5, 6, 3],
            [2, 0, 0, 1, 1, 0, 0, 2],
            [8, 1, 2, 3, 11, 5, 6, 7, 4, 9, 10, 0],
            [0; 12],
        ),
        F => (
            [1, 5, 2, 3, 0, 4, 6, 7],
            [1, 2, 0, 0, 2, 1, 0, 0],
            [0, 9, 2, 3, 4, 8, 6, 7, 1, 5, 10, 11],
            [0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0],
        ),
        D => (
            [0, 1, 2, 3, 5, 6, 7, 4],
            [0; 8],
            [0, 1, 2, 3, 5, 6, 7, 4, 8, 9, 10, 11],
            [0; 12],
        ),
        L => (
            [0, 2, 6, 3, 4, 1, 5, 7],
            [0, 1, 2, 0, 0, 2, 1, 0],
            [0, 1, 10, 3, 4, 5, 9, 7, 8, 2, 6, 11],
            [0; 12],
        ),
        B => (
            [0, 1, 3, 7, 4, 5, 2, 6],
            [0, 0, 1, 2, 0, 0, 2, 1],
            [0, 1, 2, 11, 4, 5, 6, 10, 8, 9, 3, 7],
            [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1],
        ),
    }
}

fn parity(p: &[u8]) -> u8 {
    let mut n = 0;
    for i in 0..p.len() {
        for j in i + 1..p.len() {
            n += (p[i] > p[j]) as usize;
        }
    }
    (n % 2) as u8
}

#[derive(Clone, Copy, Debug, Eq, PartialEq, Hash)]
pub struct Phase1 {
    pub twist: u16,
    pub flip: u16,
    pub slice: u16,
}

impl Phase1 {
    pub fn rank(self) -> u32 {
        ((self.twist as u32 * FLIP_COUNT as u32 + self.flip as u32) * SLICE_COUNT as u32)
            + self.slice as u32
    }
    pub fn is_g1(self) -> bool {
        self.twist == 0 && self.flip == 0 && self.slice == 0
    }
}

fn subset_masks() -> Vec<u16> {
    fn rec(pos: usize, left: usize, mask: u16, out: &mut Vec<u16>) {
        if left == 0 {
            out.push(mask);
            return;
        }
        if pos + left > 12 {
            return;
        }
        rec(pos + 1, left - 1, mask | (1 << pos), out);
        rec(pos + 1, left, mask, out);
    }
    let mut out = Vec::with_capacity(SLICE_COUNT);
    rec(0, 4, 0, &mut out);
    out.sort_unstable();
    let solved = (0b1111u16) << 8;
    out.retain(|&m| m != solved);
    out.insert(0, solved);
    out
}

fn subset_rank(mask: u16) -> u16 {
    static RANK: OnceLock<Vec<u16>> = OnceLock::new();
    let rank = RANK.get_or_init(|| {
        let mut table = vec![u16::MAX; 1 << 12];
        for (idx, subset) in subset_masks().into_iter().enumerate() {
            table[subset as usize] = idx as u16;
        }
        table
    });
    let value = rank[mask as usize];
    assert_ne!(value, u16::MAX, "four UD-slice edges");
    value
}

#[derive(Clone)]
pub struct Phase1Moves {
    pub twist: Vec<[u16; 18]>,
    pub flip: Vec<[u16; 18]>,
    pub slice: Vec<[u16; 18]>,
}

impl Phase1Moves {
    pub fn build() -> Self {
        let mut twist = vec![[0; 18]; TWIST_COUNT];
        for idx in 0..TWIST_COUNT {
            let mut co = [0u8; 8];
            let mut x = idx;
            for i in (0..7).rev() {
                co[i] = (x % 3) as u8;
                x /= 3;
            }
            co[7] = ((3 - co[..7].iter().map(|&v| v as usize).sum::<usize>() % 3) % 3) as u8;
            for (mi, &mv) in HTM.iter().enumerate() {
                let mut c = Cube::SOLVED;
                c.co = co;
                twist[idx][mi] = c.apply(mv).phase1().twist;
            }
        }
        let mut flip = vec![[0; 18]; FLIP_COUNT];
        for idx in 0..FLIP_COUNT {
            let mut eo = [0u8; 12];
            for i in 0..11 {
                eo[i] = ((idx >> (10 - i)) & 1) as u8;
            }
            eo[11] = (eo[..11].iter().map(|&v| v as usize).sum::<usize>() % 2) as u8;
            for (mi, &mv) in HTM.iter().enumerate() {
                let mut c = Cube::SOLVED;
                c.eo = eo;
                flip[idx][mi] = c.apply(mv).phase1().flip;
            }
        }
        let masks = subset_masks();
        let mut slice = vec![[0; 18]; SLICE_COUNT];
        for (idx, &mask) in masks.iter().enumerate() {
            let mut ep = [0u8; 12];
            let mut regular = 0u8;
            let mut sliced = 8u8;
            for pos in 0..12 {
                if mask & (1 << pos) != 0 {
                    ep[pos] = sliced;
                    sliced += 1;
                } else {
                    ep[pos] = regular;
                    regular += 1;
                }
            }
            for (mi, &mv) in HTM.iter().enumerate() {
                let mut c = Cube::SOLVED;
                c.ep = ep;
                slice[idx][mi] = c.apply(mv).phase1().slice;
            }
        }
        Self { twist, flip, slice }
    }

    pub fn next(&self, q: Phase1, action: usize) -> Phase1 {
        assert!(action < MOVE_COUNT);
        Phase1 {
            twist: self.twist[q.twist as usize][action],
            flip: self.flip[q.flip as usize][action],
            slice: self.slice[q.slice as usize][action],
        }
    }
}

pub struct Phase1Pdb {
    pub twist_slice: Vec<u8>,
    pub flip_slice: Vec<u8>,
}

impl Phase1Pdb {
    pub fn build(m: &Phase1Moves) -> Self {
        let twist_slice = projected_bfs(TWIST_COUNT, &m.twist, SLICE_COUNT, &m.slice);
        let flip_slice = projected_bfs(FLIP_COUNT, &m.flip, SLICE_COUNT, &m.slice);
        Self {
            twist_slice,
            flip_slice,
        }
    }
    pub fn lower_bound(&self, q: Phase1) -> u8 {
        self.twist_slice[q.twist as usize * SLICE_COUNT + q.slice as usize]
            .max(self.flip_slice[q.flip as usize * SLICE_COUNT + q.slice as usize])
    }
}

fn projected_bfs(
    a_count: usize,
    a_moves: &[[u16; 18]],
    b_count: usize,
    b_moves: &[[u16; 18]],
) -> Vec<u8> {
    let mut dist = vec![u8::MAX; a_count * b_count];
    let mut queue = VecDeque::new();
    dist[0] = 0;
    queue.push_back(0usize);
    while let Some(id) = queue.pop_front() {
        let a = id / b_count;
        let b = id % b_count;
        let nd = dist[id] + 1;
        for action in 0..MOVE_COUNT {
            let next = a_moves[a][action] as usize * b_count + b_moves[b][action] as usize;
            if dist[next] == u8::MAX {
                dist[next] = nd;
                queue.push_back(next);
            }
        }
    }
    dist
}

pub fn inverse_action(action: usize) -> usize {
    let face = action / 3;
    let power = action % 3;
    face * 3 + (2 - power)
}

pub fn c4_face(face: Face) -> Face {
    use Face::*;
    match face {
        U => U,
        D => D,
        R => B,
        B => L,
        L => F,
        F => R,
    }
}

pub fn rotate_action_c4(action: usize) -> usize {
    let mv = HTM[action];
    let face_idx = match c4_face(mv.face) {
        Face::U => 0,
        Face::R => 1,
        Face::F => 2,
        Face::D => 3,
        Face::L => 4,
        Face::B => 5,
    };
    face_idx * 3 + mv.power as usize - 1
}

/// The ten half-turn-metric generators allowed inside Kociemba phase 2:
/// U/U2/U', D/D2/D', and half turns of the four side faces.
pub const G1_ACTIONS: [usize; 10] = [0, 1, 2, 9, 10, 11, 4, 13, 7, 16];

#[derive(Clone, Copy, Debug, Eq, PartialEq, Hash, Ord, PartialOrd)]
pub struct Phase2 {
    pub corner_perm: u16,
    pub ud_edge_perm: u16,
    pub slice_perm: u8,
}

impl Cube {
    /// Exact natural phase-2 coordinate for states in G1.
    ///
    /// The triple is a lossless identifier of a legal G1 cubie state:
    /// corner permutation (8!), U/D-edge permutation (8!), and
    /// slice-edge permutation (4!), subject to the ordinary parity coupling.
    pub fn phase2(self) -> Option<Phase2> {
        if !self.phase1().is_g1() {
            return None;
        }
        let corner_perm = rank_perm(&self.cp) as u16;
        let ud_edge_perm = rank_perm(&self.ep[..8]) as u16;
        let mut slice = [0u8; 4];
        for (i, &edge) in self.ep[8..].iter().enumerate() {
            debug_assert!((8..12).contains(&edge));
            slice[i] = edge - 8;
        }
        Some(Phase2 {
            corner_perm,
            ud_edge_perm,
            slice_perm: rank_perm(&slice) as u8,
        })
    }

    pub fn is_g1(self) -> bool {
        self.phase1().is_g1()
    }
}

fn rank_perm(values: &[u8]) -> usize {
    let mut rank = 0usize;
    for i in 0..values.len() {
        let smaller_right = values[i + 1..].iter().filter(|&&x| x < values[i]).count();
        rank = rank * (values.len() - i) + smaller_right;
    }
    rank
}

#[cfg(test)]
mod phase2_tests {
    use super::*;

    #[test]
    fn phase2_coordinate_is_defined_exactly_on_g1() {
        assert_eq!(
            Cube::SOLVED.phase2(),
            Some(Phase2 {
                corner_perm: 0,
                ud_edge_perm: 0,
                slice_perm: 0
            })
        );
        for (action, &mv) in HTM.iter().enumerate() {
            let state = Cube::SOLVED.apply(mv);
            assert_eq!(
                state.phase2().is_some(),
                G1_ACTIONS.contains(&action),
                "G1 membership disagreement for action {action}"
            );
        }
    }

    #[test]
    fn phase2_coordinate_separates_local_g1_states() {
        use std::collections::{HashMap, VecDeque};

        let mut queue = VecDeque::from([(Cube::SOLVED, 0u8)]);
        let mut seen = HashMap::from([(Cube::SOLVED, 0u8)]);
        let mut coordinate_owner = HashMap::new();

        while let Some((state, depth)) = queue.pop_front() {
            let coord = state.phase2().expect("G1 BFS state");
            if let Some(previous) = coordinate_owner.insert(coord, state) {
                assert_eq!(previous, state, "phase-2 coordinate collision");
            }
            if depth == 4 {
                continue;
            }
            for &action in &G1_ACTIONS {
                let next = state.apply(HTM[action]);
                assert!(next.is_g1());
                if !seen.contains_key(&next) {
                    seen.insert(next, depth + 1);
                    queue.push_back((next, depth + 1));
                }
            }
        }
    }

    #[test]
    fn natural_phase2_pairs_each_drop_real_information() {
        use std::collections::{HashMap, VecDeque};

        let mut queue = VecDeque::from([(Cube::SOLVED, 0u8)]);
        let mut seen = HashMap::from([(Cube::SOLVED, 0u8)]);
        let mut cp_ud = HashMap::<(u16, u16), Phase2>::new();
        let mut cp_slice = HashMap::<(u16, u8), Phase2>::new();
        let mut ud_slice = HashMap::<(u16, u8), Phase2>::new();
        let mut witnesses = [false; 3];

        while let Some((state, depth)) = queue.pop_front() {
            let p = state.phase2().expect("G1 BFS state");
            if cp_ud
                .insert((p.corner_perm, p.ud_edge_perm), p)
                .is_some_and(|old| old != p)
            {
                witnesses[0] = true;
            }
            if cp_slice
                .insert((p.corner_perm, p.slice_perm), p)
                .is_some_and(|old| old != p)
            {
                witnesses[1] = true;
            }
            if ud_slice
                .insert((p.ud_edge_perm, p.slice_perm), p)
                .is_some_and(|old| old != p)
            {
                witnesses[2] = true;
            }

            if depth == 4 || witnesses.iter().all(|&x| x) {
                if witnesses.iter().all(|&x| x) {
                    break;
                }
                continue;
            }
            for &action in &G1_ACTIONS {
                let next = state.apply(HTM[action]);
                if !seen.contains_key(&next) {
                    seen.insert(next, depth + 1);
                    queue.push_back((next, depth + 1));
                }
            }
        }
        assert_eq!(witnesses, [true, true, true]);
    }
}

#[derive(Clone, Debug, Eq, PartialEq, Hash)]
pub struct EntryCostSignature {
    pub endpoint_count: usize,
    pub exact_phase2_costs: Vec<u8>,
    pub beyond_phase2_radius: usize,
}

impl EntryCostSignature {
    pub fn regret_width(&self) -> Option<u8> {
        let lo = self.exact_phase2_costs.first().copied()?;
        let hi = self.exact_phase2_costs.last().copied()?;
        Some(hi - lo)
    }

    pub fn best_exact_cost(&self) -> Option<u8> {
        self.exact_phase2_costs.first().copied()
    }
}

/// Exact G1 BFS from solved through a bounded radius.
pub fn phase2_ball(max_depth: u8) -> HashMap<Cube, u8> {
    let mut dist = HashMap::from([(Cube::SOLVED, 0u8)]);
    let mut queue = VecDeque::from([Cube::SOLVED]);
    while let Some(state) = queue.pop_front() {
        let depth = dist[&state];
        if depth == max_depth {
            continue;
        }
        for &action in &G1_ACTIONS {
            let next = state.apply(HTM[action]);
            debug_assert!(next.is_g1());
            if let std::collections::hash_map::Entry::Vacant(slot) = dist.entry(next) {
                slot.insert(depth + 1);
                queue.push_back(next);
            }
        }
    }
    dist
}

/// Exact full-cube HTM BFS from solved through a bounded radius.
pub fn full_htm_ball(max_depth: u8) -> HashMap<Cube, u8> {
    let mut dist = HashMap::from([(Cube::SOLVED, 0u8)]);
    let mut queue = VecDeque::from([Cube::SOLVED]);
    while let Some(state) = queue.pop_front() {
        let depth = dist[&state];
        if depth == max_depth {
            continue;
        }
        for &mv in &HTM {
            let next = state.apply(mv);
            if let std::collections::hash_map::Entry::Vacant(slot) = dist.entry(next) {
                slot.insert(depth + 1);
                queue.push_back(next);
            }
        }
    }
    dist
}

/// Exact phase-1 quotient BFS from G1 through a bounded radius.
pub fn phase1_ball(moves: &Phase1Moves, max_depth: u8) -> HashMap<Phase1, u8> {
    let origin = Cube::SOLVED.phase1();
    let mut dist = HashMap::from([(origin, 0u8)]);
    let mut queue = VecDeque::from([origin]);
    while let Some(q) = queue.pop_front() {
        let depth = dist[&q];
        if depth == max_depth {
            continue;
        }
        for action in 0..MOVE_COUNT {
            let next = moves.next(q, action);
            if let std::collections::hash_map::Entry::Vacant(slot) = dist.entry(next) {
                slot.insert(depth + 1);
                queue.push_back(next);
            }
        }
    }
    dist
}

/// Enumerate exact first-hit G1 endpoints after exactly N HTM moves.
///
/// Paths that touch G1 before the final move are not extended, so this is a
/// handoff-surface object rather than an unrestricted path endpoint set.
pub fn first_hit_g1_endpoints(start: Cube, steps: u8) -> HashSet<Cube> {
    if steps == 0 {
        return if start.is_g1() {
            HashSet::from([start])
        } else {
            HashSet::new()
        };
    }

    let mut frontier = HashSet::from([start]);
    for depth in 1..=steps {
        let mut next_frontier = HashSet::new();
        for state in frontier {
            for &mv in &HTM {
                let next = state.apply(mv);
                if depth == steps {
                    if next.is_g1() {
                        next_frontier.insert(next);
                    }
                } else if !next.is_g1() {
                    next_frontier.insert(next);
                }
            }
        }
        frontier = next_frontier;
        if frontier.is_empty() {
            break;
        }
    }
    frontier
}

pub fn entry_cost_signature(
    endpoints: &HashSet<Cube>,
    phase2_dist: &HashMap<Cube, u8>,
) -> EntryCostSignature {
    let mut exact_phase2_costs = Vec::new();
    let mut beyond_phase2_radius = 0usize;
    for endpoint in endpoints {
        if let Some(&cost) = phase2_dist.get(endpoint) {
            exact_phase2_costs.push(cost);
        } else {
            beyond_phase2_radius += 1;
        }
    }
    exact_phase2_costs.sort_unstable();
    EntryCostSignature {
        endpoint_count: endpoints.len(),
        exact_phase2_costs,
        beyond_phase2_radius,
    }
}

#[cfg(test)]
mod entry_fiber_tests {
    use super::*;

    #[test]
    fn phase2_radius_six_matches_generation_vi_receipt() {
        let dist = phase2_ball(6);
        assert_eq!(dist.len(), 146_635);
        let mut shells = [0usize; 7];
        for &d in dist.values() {
            shells[d as usize] += 1;
        }
        assert_eq!(shells, [1, 10, 67, 456, 3_079, 19_948, 123_074]);
    }

    #[test]
    fn first_hit_contract_excludes_early_g1_paths() {
        let r = Cube::SOLVED.apply(HTM[3]);
        let one = first_hit_g1_endpoints(r, 1);
        assert!(!one.is_empty());
        assert!(one.iter().all(|state| state.is_g1()));
        assert_eq!(
            first_hit_g1_endpoints(Cube::SOLVED, 0),
            HashSet::from([Cube::SOLVED])
        );
    }

    #[test]
    fn bounded_entry_signature_reproduces_easy_local_witness() {
        let phase2 = phase2_ball(6);
        let state = Cube::SOLVED.apply(HTM[0]).apply(HTM[3]).apply(HTM[12]);
        let endpoints = first_hit_g1_endpoints(state, 2);
        let signature = entry_cost_signature(&endpoints, &phase2);
        assert_eq!(signature.endpoint_count, 4);
        assert_eq!(signature.exact_phase2_costs, vec![1, 2, 2, 3]);
        assert_eq!(signature.beyond_phase2_radius, 0);
        assert_eq!(signature.regret_width(), Some(2));
    }
}
