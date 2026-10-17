//! Quarantine policy (ADR-004, DDD-04).
use pf_exposure::Exposure;
use serde::{Deserialize, Serialize};
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Policy {
    pub preserve_tier_zero: bool,
    pub max_quarantine: usize,
}
impl Policy {
    pub fn eligible(&self, e: &Exposure) -> bool {
        !(self.preserve_tier_zero && e.tier == 0)
    }
    pub fn default_firebreak() -> Self {
        Self {
            preserve_tier_zero: true,
            max_quarantine: 16,
        }
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn tier_zero() {
        let e = Exposure {
            deployment: "x".into(),
            service: "s".into(),
            tier: 0,
            blast_weight: 1.,
        };
        assert!(!Policy::default_firebreak().eligible(&e));
    }
}
