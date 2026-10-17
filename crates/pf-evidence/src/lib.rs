//! Append-only auditable evidence (ADR-018, DDD-11).
use pf_events::DomainEvent;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::{fs::OpenOptions, io::Write, path::Path};
use thiserror::Error;
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Receipt {
    pub count: usize,
    pub root: String,
}
#[derive(Debug, Error)]
pub enum EvidenceError {
    #[error("io: {0}")]
    Io(#[from] std::io::Error),
    #[error("json: {0}")]
    Json(#[from] serde_json::Error),
}
pub fn append(path: &Path, events: &[DomainEvent]) -> Result<Receipt, EvidenceError> {
    let mut f = OpenOptions::new().create(true).append(true).open(path)?;
    let mut h = Sha256::new();
    for e in events {
        let line = serde_json::to_vec(e)?;
        h.update(&line);
        f.write_all(&line)?;
        f.write_all(b"\n")?;
    }
    Ok(Receipt {
        count: events.len(),
        root: format!("{:x}", h.finalize()),
    })
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn empty_receipt() {
        let d = tempfile::tempdir().unwrap();
        assert_eq!(append(&d.path().join("e"), &[]).unwrap().count, 0);
    }
}
