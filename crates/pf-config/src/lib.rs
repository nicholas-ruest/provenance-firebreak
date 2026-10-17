//! Runtime configuration (ADR-008).
use thiserror::Error;
#[derive(Clone, Debug)]
pub struct Config {
    pub alpha: f64,
    pub recall_k: usize,
    pub evidence_path: String,
}
#[derive(Debug, Error)]
pub enum ConfigError {
    #[error("invalid runtime configuration")]
    Invalid,
}
impl Config {
    pub fn validate(self) -> Result<Self, ConfigError> {
        if (0.0..1.0).contains(&self.alpha) && self.recall_k > 0 && !self.evidence_path.is_empty() {
            Ok(self)
        } else {
            Err(ConfigError::Invalid)
        }
    }
}
impl Default for Config {
    fn default() -> Self {
        Self {
            alpha: 0.1,
            recall_k: 3,
            evidence_path: "evidence.jsonl".into(),
        }
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn default_valid() {
        Config::default().validate().unwrap();
    }
}
