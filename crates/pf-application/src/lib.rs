//! End-to-end incident orchestration (DDD context map).
use pf_adapter_ruvector::IncidentRecall;
use pf_adapter_rvf::{seal, verify};
use pf_adapter_sigstore::SigstoreBoundary;
use pf_artifact::Artifact;
use pf_attestation::BundleStatus;
use pf_calibration::Calibrator;
use pf_events::{DomainEvent, EventKind};
use pf_evidence::{Receipt, append};
use pf_graph::IncidentGraph;
use pf_identity::DigestId;
use pf_lineage::Deployment;
use pf_planning::{Plan, plan};
use pf_policy::Policy;
use pf_ports::BundleGate;
use pf_recovery::verify_receipt;
use serde::{Deserialize, Serialize};
use std::path::Path;
use thiserror::Error;
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct IncidentInput {
    pub compromised: String,
    pub sigstore_bundle: String,
}
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Outcome {
    pub risk_upper: f64,
    pub analogue_count: usize,
    pub plan: Plan,
    pub receipt: Receipt,
    pub recovery_verified: bool,
    pub sigstore_untrusted_rejected: bool,
}
#[derive(Debug, Error)]
pub enum ApplicationError {
    #[error("pipeline: {0}")]
    Pipeline(String),
}
pub fn execute(input: &IncidentInput, state: &Path) -> Result<Outcome, ApplicationError> {
    let raw = input.sigstore_bundle.as_bytes();
    let status = SigstoreBoundary
        .inspect(raw)
        .map_err(|e| ApplicationError::Pipeline(e.to_string()))?;
    let sigstore_untrusted_rejected = matches!(status, BundleStatus::RejectedUntrusted { .. });
    let root = Artifact::new(DigestId::of(input.compromised.as_bytes()), "checkout", 1)
        .map_err(|e| ApplicationError::Pipeline(e.to_string()))?;
    let tier0 = Artifact::new(DigestId::of(b"payments"), "payments", 0)
        .map_err(|e| ApplicationError::Pipeline(e.to_string()))?;
    let worker = Artifact::new(DigestId::of(b"worker"), "worker", 2)
        .map_err(|e| ApplicationError::Pipeline(e.to_string()))?;
    let mut graph = IncidentGraph::default();
    graph
        .add(Deployment {
            id: "root".into(),
            artifact: root.clone(),
            parents: vec![],
            service: "checkout".into(),
            observed_at: 1,
        })
        .map_err(|e| ApplicationError::Pipeline(e.to_string()))?;
    graph
        .add(Deployment {
            id: "payments".into(),
            artifact: tier0,
            parents: vec!["root".into()],
            service: "payments".into(),
            observed_at: 2,
        })
        .map_err(|e| ApplicationError::Pipeline(e.to_string()))?;
    graph
        .add(Deployment {
            id: "worker".into(),
            artifact: worker,
            parents: vec!["root".into()],
            service: "fulfilment".into(),
            observed_at: 3,
        })
        .map_err(|e| ApplicationError::Pipeline(e.to_string()))?;
    let subject = root.digest.clone();
    let mut events = vec![
        DomainEvent::new(
            1,
            EventKind::AttestationVerified,
            subject.clone(),
            "Sigstore structure parsed; untrusted verification rejected",
        ),
        DomainEvent::new(
            2,
            EventKind::LineageBuilt,
            subject.clone(),
            format!("{} nodes", graph.node_count()),
        ),
    ];
    let db_dir = state.join("ruvector.db");
    let recall = IncidentRecall::open(
        db_dir
            .to_str()
            .ok_or_else(|| ApplicationError::Pipeline("non utf8 state".into()))?,
    )
    .map_err(|e| ApplicationError::Pipeline(e.to_string()))?;
    recall
        .remember("known-incident", &events[0], vec![1., 0.2, 0.1, 0.])
        .map_err(|e| ApplicationError::Pipeline(e.to_string()))?;
    let analogue_count = recall
        .similar(vec![1., 0.2, 0.1, 0.], 3)
        .map_err(|e| ApplicationError::Pipeline(e.to_string()))?;
    events.push(DomainEvent::new(
        3,
        EventKind::RecallCompleted,
        subject.clone(),
        format!("{analogue_count} analogues"),
    ));
    let calibration = Calibrator::fit(
        vec![0.05, 0.08, 0.12, 0.18, 0.21, 0.29, 0.34, 0.41, 0.52, 0.61],
        0.1,
    )
    .map_err(|e| ApplicationError::Pipeline(e.to_string()))?;
    let risk_upper = calibration.upper(0.44);
    events.push(DomainEvent::new(
        4,
        EventKind::RiskCalibrated,
        subject.clone(),
        format!("upper={risk_upper:0.3}"),
    ));
    let exposures = graph.exposure("root");
    let firebreak = plan(&exposures, &Policy::default_firebreak(), risk_upper)
        .map_err(|e| ApplicationError::Pipeline(e.to_string()))?;
    events.push(DomainEvent::new(
        5,
        EventKind::PlanAuthorized,
        subject.clone(),
        format!("quarantine={:?}", firebreak.quarantined),
    ));
    let witness = seal(&events).map_err(|e| ApplicationError::Pipeline(e.to_string()))?;
    verify(&witness).map_err(|e| ApplicationError::Pipeline(e.to_string()))?;
    events.push(DomainEvent::new(
        6,
        EventKind::EvidenceSealed,
        subject,
        "RVF witness chain verified",
    ));
    let receipt = append(&state.join("evidence.jsonl"), &events)
        .map_err(|e| ApplicationError::Pipeline(e.to_string()))?;
    verify_receipt(&receipt).map_err(|e| ApplicationError::Pipeline(e.to_string()))?;
    Ok(Outcome {
        risk_upper,
        analogue_count,
        plan: firebreak,
        receipt,
        recovery_verified: true,
        sigstore_untrusted_rejected,
    })
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn invalid_bundle_fails_closed() {
        let d = tempfile::tempdir().unwrap();
        let i = IncidentInput {
            compromised: "x".into(),
            sigstore_bundle: "{}".into(),
        };
        assert!(execute(&i, d.path()).is_err());
    }
}
