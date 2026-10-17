//! Append-only domain events (DDD-10).
use pf_identity::DigestId;
use serde::{Deserialize, Serialize};
#[derive(Clone, Debug, Serialize, Deserialize)]
pub enum EventKind {
    AttestationVerified,
    LineageBuilt,
    RecallCompleted,
    RiskCalibrated,
    PlanAuthorized,
    EvidenceSealed,
    RecoveryVerified,
}
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct DomainEvent {
    pub sequence: u64,
    pub kind: EventKind,
    pub subject: DigestId,
    pub detail: String,
}
impl DomainEvent {
    pub fn new(
        sequence: u64,
        kind: EventKind,
        subject: DigestId,
        detail: impl Into<String>,
    ) -> Self {
        Self {
            sequence,
            kind,
            subject,
            detail: detail.into(),
        }
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn seq() {
        assert_eq!(
            DomainEvent::new(1, EventKind::LineageBuilt, DigestId::of(b"x"), "ok").sequence,
            1
        );
    }
}
