//! Real RVF witness-chain boundary (ADR-006, DDD-06).
use pf_events::DomainEvent;
use rvf_crypto::{WitnessEntry, create_witness_chain, shake256_256, verify_witness_chain};
use thiserror::Error;
#[derive(Clone, Debug)]
pub struct Seal {
    pub chain: Vec<u8>,
}
#[derive(Debug, Error)]
pub enum SealError {
    #[error("empty event stream")]
    Empty,
    #[error("invalid witness chain")]
    Invalid,
}
pub fn seal(events: &[DomainEvent]) -> Result<Seal, SealError> {
    if events.is_empty() {
        return Err(SealError::Empty);
    }
    let mut entries = Vec::new();
    for e in events {
        let bytes = format!("{}:{:?}:{}", e.sequence, e.kind, e.detail);
        entries.push(WitnessEntry {
            prev_hash: [0; 32],
            action_hash: shake256_256(bytes.as_bytes()),
            timestamp_ns: e.sequence,
            witness_type: 1,
        });
    }
    Ok(Seal {
        chain: create_witness_chain(&entries),
    })
}
pub fn verify(seal: &Seal) -> Result<(), SealError> {
    verify_witness_chain(&seal.chain)
        .map(|_| ())
        .map_err(|_| SealError::Invalid)
}
#[cfg(test)]
mod tests {
    use super::*;
    use pf_events::EventKind;
    use pf_identity::DigestId;
    #[test]
    fn chain() {
        let e = DomainEvent::new(1, EventKind::EvidenceSealed, DigestId::of(b"x"), "x");
        let s = seal(&[e]).unwrap();
        verify(&s).unwrap();
    }
}
