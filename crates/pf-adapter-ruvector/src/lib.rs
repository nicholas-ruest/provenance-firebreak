//! Real RuVector incident recall (ADR-005, DDD-05).
use pf_events::DomainEvent;
use ruvector_core::types::{DbOptions, HnswConfig};
use ruvector_core::{DistanceMetric, SearchQuery, VectorDB, VectorEntry};
use std::collections::HashMap;
use thiserror::Error;
#[derive(Debug, Error)]
pub enum RecallError {
    #[error("ruvector: {0}")]
    Database(String),
    #[error("event serialization: {0}")]
    Serialize(String),
}
pub struct IncidentRecall {
    db: VectorDB,
}
impl IncidentRecall {
    pub fn open(path: &str) -> Result<Self, RecallError> {
        let o = DbOptions {
            dimensions: 4,
            distance_metric: DistanceMetric::Cosine,
            storage_path: path.into(),
            hnsw_config: Some(HnswConfig::default()),
            quantization: None,
        };
        VectorDB::new(o)
            .map(|db| Self { db })
            .map_err(|e| RecallError::Database(e.to_string()))
    }
    pub fn remember(
        &self,
        id: &str,
        event: &DomainEvent,
        vector: Vec<f32>,
    ) -> Result<String, RecallError> {
        let mut m = HashMap::new();
        m.insert(
            "event".into(),
            serde_json::to_value(event).map_err(|e| RecallError::Serialize(e.to_string()))?,
        );
        self.db
            .insert(VectorEntry {
                id: Some(id.into()),
                vector,
                metadata: Some(m),
            })
            .map_err(|e| RecallError::Database(e.to_string()))
    }
    pub fn similar(&self, vector: Vec<f32>, k: usize) -> Result<usize, RecallError> {
        self.db
            .search(SearchQuery {
                vector,
                k,
                filter: None,
                ef_search: Some(32),
            })
            .map(|v| v.len())
            .map_err(|e| RecallError::Database(e.to_string()))
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    use pf_events::EventKind;
    use pf_identity::DigestId;
    #[test]
    fn real_roundtrip() {
        let d = tempfile::tempdir().unwrap();
        let r = IncidentRecall::open(d.path().join("db.rvf").to_str().unwrap()).unwrap();
        let e = DomainEvent::new(1, EventKind::RecallCompleted, DigestId::of(b"x"), "x");
        r.remember("x", &e, vec![1., 0., 0., 0.]).unwrap();
        assert_eq!(r.similar(vec![1., 0., 0., 0.], 1).unwrap(), 1);
    }
}
