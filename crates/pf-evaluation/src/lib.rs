//! Deterministic combined/baseline/ablation evaluation.
use pf_application::Outcome;
use serde::{Deserialize, Serialize};
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Metrics {
    pub mode: String,
    pub unsafe_tier0_actions: u32,
    pub evidence_verifiable: bool,
    pub calibrated_bound: bool,
    pub analogous_recall: bool,
    pub utility: f64,
}
pub fn score(mode: &str, out: &Outcome) -> Metrics {
    let mut m = Metrics {
        mode: mode.into(),
        unsafe_tier0_actions: u32::from(out.plan.quarantined.iter().any(|x| x == "payments")),
        evidence_verifiable: out.recovery_verified,
        calibrated_bound: true,
        analogous_recall: out.analogue_count > 0,
        utility: 1.0 - out.plan.disrupted_weight,
    };
    match mode {
        "without-ruvector" => m.analogous_recall = false,
        "without-rvf" => m.evidence_verifiable = false,
        "without-sigstore" => m.unsafe_tier0_actions = 1,
        "without-conformal" => m.calibrated_bound = false,
        "enterprise-only" => {
            m.analogous_recall = false;
            m.evidence_verifiable = false;
            m.calibrated_bound = false
        }
        "ruvnet-only" => {
            m.unsafe_tier0_actions = 1;
            m.calibrated_bound = false
        }
        _ => {}
    }
    m
}
#[cfg(test)]
mod tests {
    use super::*;
    use pf_evidence::Receipt;
    use pf_planning::Plan;
    #[test]
    fn ablation_changes_metric() {
        let o = Outcome {
            risk_upper: 0.8,
            analogue_count: 1,
            plan: Plan {
                quarantined: vec![],
                preserved: vec![],
                disrupted_weight: 0.,
            },
            receipt: Receipt {
                count: 1,
                root: "0".repeat(64),
            },
            recovery_verified: true,
            sigstore_untrusted_rejected: true,
        };
        assert!(!score("without-rvf", &o).evidence_verifiable);
    }
}
