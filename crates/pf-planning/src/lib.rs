//! Least-disruptive planner (ADR-004, DDD-04).
use pf_exposure::Exposure;
use pf_policy::Policy;
use serde::{Deserialize, Serialize};
use thiserror::Error;
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Plan {
    pub quarantined: Vec<String>,
    pub preserved: Vec<String>,
    pub disrupted_weight: f64,
}
#[derive(Debug, Error)]
pub enum PlanError {
    #[error("no safe firebreak exists")]
    NoSafePlan,
}
pub fn plan(exposures: &[Exposure], policy: &Policy, risk_upper: f64) -> Result<Plan, PlanError> {
    if !(0.0..=1.0).contains(&risk_upper) {
        return Err(PlanError::NoSafePlan);
    }
    let mut candidates: Vec<_> = exposures.iter().filter(|e| policy.eligible(e)).collect();
    candidates.sort_by(|a, b| {
        a.blast_weight
            .total_cmp(&b.blast_weight)
            .then(a.deployment.cmp(&b.deployment))
    });
    let take = if risk_upper >= 0.8 {
        candidates.len().min(policy.max_quarantine)
    } else if risk_upper >= 0.5 {
        candidates.len().div_ceil(2).min(policy.max_quarantine)
    } else {
        0
    };
    let quarantined = candidates
        .iter()
        .take(take)
        .map(|e| e.deployment.clone())
        .collect::<Vec<_>>();
    let preserved = exposures
        .iter()
        .filter(|e| !quarantined.contains(&e.deployment))
        .map(|e| e.deployment.clone())
        .collect();
    let disrupted_weight = candidates.iter().take(take).map(|e| e.blast_weight).sum();
    Ok(Plan {
        quarantined,
        preserved,
        disrupted_weight,
    })
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn preserve() {
        let e = vec![
            Exposure {
                deployment: "a".into(),
                service: "s".into(),
                tier: 0,
                blast_weight: 1.,
            },
            Exposure {
                deployment: "b".into(),
                service: "t".into(),
                tier: 2,
                blast_weight: 0.3,
            },
        ];
        let p = plan(&e, &Policy::default_firebreak(), 0.9).unwrap();
        assert_eq!(p.quarantined, vec!["b"]);
    }
}
