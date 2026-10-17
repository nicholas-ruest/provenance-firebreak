//! Real Sigstore bundle boundary (ADR-001, DDD-12).
use pf_attestation::BundleStatus;
use pf_identity::DigestId;
use pf_ports::{BundleGate, PortError};
use sigstore::cosign::bundle::SignedArtifactBundle;
use std::collections::BTreeMap;
use thiserror::Error;

#[derive(Debug, Error)]
pub enum SigstoreError {
    #[error("invalid Sigstore bundle JSON: {0}")]
    Json(String),
    #[error("verification rejected: {0}")]
    Rejected(String),
}

pub fn parse_bundle(raw: &[u8]) -> Result<SignedArtifactBundle, SigstoreError> {
    serde_json::from_slice(raw).map_err(|e| SigstoreError::Json(e.to_string()))
}

pub fn verify_rejects_untrusted(raw: &[u8]) -> Result<(), SigstoreError> {
    let _bundle = parse_bundle(raw)?;
    let text = std::str::from_utf8(raw).map_err(|e| SigstoreError::Json(e.to_string()))?;
    let keys = BTreeMap::new();
    SignedArtifactBundle::new_verified(text, &keys)
        .map(|_| ())
        .map_err(|e| SigstoreError::Rejected(e.to_string()))
}

pub struct SigstoreBoundary;

impl BundleGate for SigstoreBoundary {
    fn inspect(&self, raw: &[u8]) -> Result<BundleStatus, PortError> {
        parse_bundle(raw).map_err(|e| PortError::Upstream(e.to_string()))?;
        let digest = DigestId::of(raw);
        match verify_rejects_untrusted(raw) {
            Ok(()) => Ok(BundleStatus::Verified { digest }),
            Err(SigstoreError::Rejected(_)) => Ok(BundleStatus::RejectedUntrusted { digest }),
            Err(error) => Err(PortError::Upstream(error.to_string())),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn malformed_rejected() {
        assert!(parse_bundle(b"{}").is_err());
    }
}
