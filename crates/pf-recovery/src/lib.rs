//! Recovery verification (ADR-007, DDD-07).
use pf_evidence::Receipt;
use thiserror::Error;
#[derive(Debug, Error)]
pub enum RecoveryError {
    #[error("empty or malformed receipt")]
    Invalid,
}
pub fn verify_receipt(r: &Receipt) -> Result<(), RecoveryError> {
    if r.count > 0 && r.root.len() == 64 && r.root.bytes().all(|b| b.is_ascii_hexdigit()) {
        Ok(())
    } else {
        Err(RecoveryError::Invalid)
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn rejects_empty() {
        assert!(
            verify_receipt(&Receipt {
                count: 0,
                root: "0".repeat(64)
            })
            .is_err()
        );
    }
}
