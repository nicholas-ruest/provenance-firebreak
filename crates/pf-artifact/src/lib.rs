//! Artifact aggregate (ADR-001, DDD-01).
use pf_identity::DigestId;
use serde::{Deserialize, Serialize};
use thiserror::Error;
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Artifact {
    pub digest: DigestId,
    pub name: String,
    pub tier: u8,
}
#[derive(Debug, Error)]
pub enum ArtifactError {
    #[error("empty artifact name")]
    Empty,
    #[error("tier exceeds 3")]
    Tier,
}
impl Artifact {
    pub fn new(digest: DigestId, name: impl Into<String>, tier: u8) -> Result<Self, ArtifactError> {
        let name = name.into();
        if name.trim().is_empty() {
            return Err(ArtifactError::Empty);
        }
        if tier > 3 {
            return Err(ArtifactError::Tier);
        }
        Ok(Self { digest, name, tier })
    }
    pub fn is_tier_zero(&self) -> bool {
        self.tier == 0
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn invariant() {
        assert!(Artifact::new(DigestId::of(b"a"), "", 0).is_err());
    }
}
