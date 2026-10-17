//! Temporal graph façade (ADR-002, DDD-02).
use pf_exposure::{Exposure, compute};
use pf_lineage::{Deployment, Lineage, LineageError};
use thiserror::Error;
#[derive(Default)]
pub struct IncidentGraph {
    lineage: Lineage,
}
#[derive(Debug, Error)]
pub enum GraphError {
    #[error(transparent)]
    Lineage(#[from] LineageError),
}
impl IncidentGraph {
    pub fn add(&mut self, d: Deployment) -> Result<(), GraphError> {
        self.lineage.add(d)?;
        Ok(())
    }
    pub fn exposure(&self, root: &str) -> Vec<Exposure> {
        compute(&self.lineage, root)
    }
    pub fn node_count(&self) -> usize {
        self.lineage.len()
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn starts_empty() {
        assert_eq!(IncidentGraph::default().node_count(), 0);
    }
}
