//! Stateless service façade (DDD context map).
use pf_application::{ApplicationError, IncidentInput, Outcome, execute};
use pf_config::Config;
use pf_telemetry::init;
use serde::{Deserialize, Serialize};
use std::path::Path;
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct ServiceRequest {
    pub compromised: String,
    pub sigstore_bundle: String,
}
pub struct FirebreakService {
    config: Config,
}
impl FirebreakService {
    pub fn new(config: Config) -> Result<Self, pf_config::ConfigError> {
        Ok(Self {
            config: config.validate()?,
        })
    }
    pub fn handle(&self, req: ServiceRequest, state: &Path) -> Result<Outcome, ApplicationError> {
        init();
        let _ = &self.config;
        execute(
            &IncidentInput {
                compromised: req.compromised,
                sigstore_bundle: req.sigstore_bundle,
            },
            state,
        )
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn service_constructs() {
        FirebreakService::new(Config::default()).unwrap();
    }
}
