//! Attestation aggregate and trust-boundary result (ADR-001, DDD-01).
use pf_artifact::Artifact;
use pf_identity::DigestId;
use serde::{Deserialize, Serialize};
use thiserror::Error;

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Attestation {
    pub artifact: Artifact,
    pub issuer: String,
    pub bundle_digest: DigestId,
    pub verified: bool,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub enum BundleStatus {
    Verified { digest: DigestId },
    RejectedUntrusted { digest: DigestId },
}

#[derive(Debug, Error)]
pub enum AttestationError {
    #[error("issuer is empty")]
    Issuer,
}

impl Attestation {
    pub fn admitted(
        artifact: Artifact,
        issuer: impl Into<String>,
        raw: &[u8],
    ) -> Result<Self, AttestationError> {
        let issuer = issuer.into();
        if issuer.trim().is_empty() {
            return Err(AttestationError::Issuer);
        }
        Ok(Self {
            artifact,
            issuer,
            bundle_digest: DigestId::of(raw),
            verified: true,
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn issuer_invariant() {
        let artifact = Artifact::new(DigestId::of(b"a"), "a", 1).unwrap();
        assert!(Attestation::admitted(artifact, "", b"x").is_err());
    }
}
