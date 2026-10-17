use pf_application::{IncidentInput, execute};
use pf_evaluation::score;
use serde::Deserialize;
use std::{fs, path::PathBuf, time::Instant};

#[derive(Deserialize)]
struct Fixture {
    compromised: String,
    sigstore_bundle: String,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let fixture: Fixture = serde_json::from_str(&fs::read_to_string("fixtures/incident.json")?)?;
    let input = IncidentInput {
        compromised: fixture.compromised,
        sigstore_bundle: fixture.sigstore_bundle,
    };
    let state = PathBuf::from("target/evaluation-live");
    fs::create_dir_all(&state)?;
    let _ = fs::remove_file(state.join("ruvector.db"));
    let _ = fs::remove_file(state.join("evidence.jsonl"));
    let start = Instant::now();
    let outcome = execute(&input, &state)?;
    let elapsed_us = start.elapsed().as_micros();
    let modes = [
        "combined",
        "without-ruvector",
        "without-rvf",
        "without-sigstore",
        "without-conformal",
        "enterprise-only",
        "ruvnet-only",
    ];
    println!(
        "{{\"seed\":20261016,\"workload\":\"signed-lineage-incident-v1\",\"elapsed_us\":{elapsed_us}}}"
    );
    for mode in modes {
        println!("{}", serde_json::to_string(&score(mode, &outcome))?);
    }
    Ok(())
}
