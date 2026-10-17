//! Canonical identities (ADR-001, DDD-01).
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use thiserror::Error;
#[derive(Clone, Debug, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct DigestId(String);
#[derive(Debug, Error)]
pub enum IdentityError {
    #[error("digest must be sha256:<64 hex>")]
    Invalid,
}
impl DigestId {
    pub fn parse(v: impl Into<String>) -> Result<Self, IdentityError> {
        let v = v.into();
        let ok = v
            .strip_prefix("sha256:")
            .is_some_and(|x| x.len() == 64 && x.bytes().all(|b| b.is_ascii_hexdigit()));
        if ok {
            Ok(Self(v.to_ascii_lowercase()))
        } else {
            Err(IdentityError::Invalid)
        }
    }
    pub fn of(bytes: &[u8]) -> Self {
        Self(format!("sha256:{:x}", Sha256::digest(bytes)))
    }
    pub fn as_str(&self) -> &str {
        &self.0
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn stable() {
        assert_eq!(DigestId::of(b"x"), DigestId::of(b"x"));
        assert!(DigestId::parse("bad").is_err());
    }
}
