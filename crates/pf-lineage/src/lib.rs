//! Temporal deployment lineage (ADR-002, DDD-02).
use pf_artifact::Artifact;
use serde::{Deserialize, Serialize};
use std::collections::{HashMap, HashSet};
use thiserror::Error;
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Deployment {
    pub id: String,
    pub artifact: Artifact,
    pub parents: Vec<String>,
    pub service: String,
    pub observed_at: u64,
}
#[derive(Clone, Debug, Default)]
pub struct Lineage {
    nodes: HashMap<String, Deployment>,
}
#[derive(Debug, Error)]
pub enum LineageError {
    #[error("duplicate deployment")]
    Duplicate,
    #[error("self parent")]
    SelfParent,
}
impl Lineage {
    pub fn add(&mut self, d: Deployment) -> Result<(), LineageError> {
        if d.parents.iter().any(|p| p == &d.id) {
            return Err(LineageError::SelfParent);
        }
        if self.nodes.insert(d.id.clone(), d).is_some() {
            return Err(LineageError::Duplicate);
        }
        Ok(())
    }
    pub fn descendants(&self, root: &str) -> HashSet<String> {
        let mut out = HashSet::new();
        let mut q = vec![root.to_owned()];
        while let Some(x) = q.pop() {
            for (n, d) in &self.nodes {
                if d.parents.contains(&x) && out.insert(n.clone()) {
                    q.push(n.clone())
                }
            }
        }
        out
    }
    pub fn get(&self, id: &str) -> Option<&Deployment> {
        self.nodes.get(id)
    }
    pub fn len(&self) -> usize {
        self.nodes.len()
    }
    pub fn is_empty(&self) -> bool {
        self.nodes.is_empty()
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    use pf_identity::DigestId;
    #[test]
    fn closure() {
        let a = Artifact::new(DigestId::of(b"a"), "a", 1).unwrap();
        let mut l = Lineage::default();
        l.add(Deployment {
            id: "r".into(),
            artifact: a.clone(),
            parents: vec![],
            service: "s".into(),
            observed_at: 1,
        })
        .unwrap();
        l.add(Deployment {
            id: "c".into(),
            artifact: a,
            parents: vec!["r".into()],
            service: "t".into(),
            observed_at: 2,
        })
        .unwrap();
        assert!(l.descendants("r").contains("c"));
    }
}
