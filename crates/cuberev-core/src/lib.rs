//! Exact 2x2 corner-state primitives for the R3-R3 instrument boundary.
//! This crate deliberately does not make an R2 census or oracle-equivalence claim.

pub const PERMUTATIONS: u32 = 5_040; // 7!
pub const ORIENTATIONS: u32 = 729; // 3^6
pub const STATE_DOMAIN: u32 = PERMUTATIONS * ORIENTATIONS;

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct CornerState {
    /// Corner occupying each of the seven independently stored positions.
    pub perm: [u8; 7],
    /// Corner twists; the seventh is determined by the zero-sum constraint.
    pub ori: [u8; 7],
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum StateError {
    InvalidPermutation,
    InvalidOrientation,
    OrientationSum,
}

impl CornerState {
    pub fn solved() -> Self {
        Self {
            perm: [0, 1, 2, 3, 4, 5, 6],
            ori: [0; 7],
        }
    }

    pub fn validate(&self) -> Result<(), StateError> {
        let mut seen = [false; 7];
        for &p in &self.perm {
            if p > 6 || seen[p as usize] {
                return Err(StateError::InvalidPermutation);
            }
            seen[p as usize] = true;
        }
        let mut sum = 0u8;
        for &o in &self.ori {
            if o > 2 {
                return Err(StateError::InvalidOrientation);
            }
            sum = (sum + o) % 3;
        }
        if sum != 0 {
            return Err(StateError::OrientationSum);
        }
        Ok(())
    }

    /// Packed rank convention: Lehmer(perm) * 3^6 + first-six base-3 orientations.
    pub fn rank(&self) -> Result<u32, StateError> {
        self.validate()?;
        let mut lehmer = 0u32;
        for i in 0..7 {
            let lower = self.perm[i + 1..]
                .iter()
                .filter(|&&p| p < self.perm[i])
                .count() as u32;
            lehmer += lower * factorial(6 - i);
        }
        let mut orientation = 0u32;
        for &o in &self.ori[..6] {
            orientation = orientation * 3 + o as u32;
        }
        Ok(lehmer * ORIENTATIONS + orientation)
    }

    pub fn unrank(rank: u32) -> Option<Self> {
        if rank >= STATE_DOMAIN {
            return None;
        }
        let lehmer = rank / ORIENTATIONS;
        let mut orient_value = rank % ORIENTATIONS;
        let mut ori = [0u8; 7];
        for i in (0..6).rev() {
            ori[i] = (orient_value % 3) as u8;
            orient_value /= 3;
        }
        ori[6] = (3 - ori[..6].iter().copied().fold(0u8, |a, x| (a + x) % 3)) % 3;
        let mut values = vec![0u8, 1, 2, 3, 4, 5, 6];
        let mut rem = lehmer;
        let mut perm = [0u8; 7];
        for i in 0..7 {
            let f = factorial(6 - i);
            let index = (rem / f) as usize;
            rem %= f;
            perm[i] = values.remove(index);
        }
        Some(Self { perm, ori })
    }

    /// Canonical SymbolicFrame bytes. Renderer consumes this string; it cannot infer state back from UI.
    pub fn symbolic_frame_bytes(&self, authorized_view: &str) -> Result<String, StateError> {
        self.validate()?;
        Ok(format!(
            "sf1|view={authorized_view}|perm={}|ori={}",
            csv(&self.perm),
            csv(&self.ori)
        ))
    }

    pub fn canonical_stimulus_bytes(
        &self,
        authorized_view: &str,
        arm: &str,
    ) -> Result<String, StateError> {
        Ok(format!(
            "cs1|rank={}|frame={}|arm={arm}",
            self.rank()?,
            self.symbolic_frame_bytes(authorized_view)?
        ))
    }
}

fn factorial(n: usize) -> u32 {
    (1..=n as u32).product::<u32>().max(1)
}
fn csv(values: &[u8]) -> String {
    values
        .iter()
        .map(u8::to_string)
        .collect::<Vec<_>>()
        .join(",")
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn solved_rank_roundtrip() {
        let s = CornerState::solved();
        assert_eq!(s.rank().unwrap(), 0);
        assert_eq!(CornerState::unrank(0), Some(s));
    }
    #[test]
    fn every_rank_boundary_roundtrips() {
        for r in [0, 1, 728, 729, STATE_DOMAIN - 1] {
            let s = CornerState::unrank(r).unwrap();
            assert_eq!(s.rank().unwrap(), r);
        }
    }
    #[test]
    fn illegal_orientation_is_refused() {
        let mut s = CornerState::solved();
        s.ori[0] = 1;
        assert_eq!(s.validate(), Err(StateError::OrientationSum));
    }
}
