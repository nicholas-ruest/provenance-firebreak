//! Hexagonal ports (DDD-12).
use async_trait::async_trait;
use pf_attestation::{Attestation, BundleStatus};
use pf_events::DomainEvent;
use thiserror::Error;

#[derive(Debug, Error)]
pub enum PortError {
    #[error("upstream: {0}")]
    Upstream(String),
}

#[async_trait]
pub trait AttestationVerifier: Send + Sync {
    async fn verify(&self, raw: &[u8]) -> Result<Attestation, PortError>;
}

pub trait BundleGate: Send + Sync {
    fn inspect(&self, raw: &[u8]) -> Result<BundleStatus, PortError>;
}

#[async_trait]
pub trait EvidenceSink: Send + Sync {
    async fn append(&self, event: &DomainEvent) -> Result<(), PortError>;
}
