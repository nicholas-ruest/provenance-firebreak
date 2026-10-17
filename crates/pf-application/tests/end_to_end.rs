use pf_application::{IncidentInput, execute};

#[test]
fn signed_lineage_incident_preserves_tier_zero_and_seals_replay() {
    let state = tempfile::tempdir().expect("temporary state");
    let bundle = serde_json::json!({
        "base64Signature": "AA==",
        "cert": "AA==",
        "rekorBundle": {
            "SignedEntryTimestamp": "AA==",
            "Payload": {
                "body": "e30=",
                "integratedTime": 1,
                "logIndex": 1,
                "logID": "x"
            }
        }
    });
    let outcome = execute(
        &IncidentInput {
            compromised: "registry.example/acme/checkout@sha256:bad".into(),
            sigstore_bundle: bundle.to_string(),
        },
        state.path(),
    )
    .expect("end-to-end workload succeeds");

    assert!(outcome.sigstore_untrusted_rejected);
    assert_eq!(outcome.analogue_count, 1);
    assert!(outcome.plan.preserved.contains(&"payments".to_owned()));
    assert!(!outcome.plan.quarantined.contains(&"payments".to_owned()));
    assert!(outcome.recovery_verified);
    assert_eq!(outcome.receipt.count, 6);
}

#[test]
fn malformed_sigstore_bundle_fails_closed() {
    let state = tempfile::tempdir().expect("temporary state");
    let result = execute(
        &IncidentInput {
            compromised: "bad".into(),
            sigstore_bundle: "{}".into(),
        },
        state.path(),
    );
    assert!(result.is_err());
}
