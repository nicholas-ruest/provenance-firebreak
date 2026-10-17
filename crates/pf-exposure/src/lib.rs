//! Exposure computation (DDD-03).
use pf_lineage::Lineage;
use serde::{Deserialize, Serialize};
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Exposure {
    pub deployment: String,
    pub service: String,
    pub tier: u8,
    pub blast_weight: f64,
}
pub fn compute(lineage: &Lineage, root: &str) -> Vec<Exposure> {
    let mut ids = lineage.descendants(root);
    ids.insert(root.to_owned());
    let mut v: Vec<_> = ids
        .into_iter()
        .filter_map(|id| {
            lineage.get(&id).map(|d| Exposure {
                deployment: id,
                service: d.service.clone(),
                tier: d.artifact.tier,
                blast_weight: 1.0 / (f64::from(d.artifact.tier) + 1.0),
            })
        })
        .collect();
    v.sort_by(|a, b| a.deployment.cmp(&b.deployment));
    v
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn empty() {
        assert!(compute(&Lineage::default(), "x").is_empty());
    }
}
