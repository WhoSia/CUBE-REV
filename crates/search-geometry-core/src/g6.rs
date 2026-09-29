//! 3x3 phase-1 Schreier coordinate oracle and Kociemba-style projected PDBs.
//! Move convention matches Kociemba CubieCube: position arrays, right composition.

use std::collections::VecDeque;
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
