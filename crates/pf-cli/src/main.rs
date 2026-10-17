//! Operator CLI (ADR-008).
use anyhow::Context;
use clap::Parser;
use pf_cli::safe_state_path;
use pf_config::Config;
use pf_service::{FirebreakService, ServiceRequest};
use std::path::PathBuf;
#[derive(Parser)]
struct Args {
    #[arg(long)]
    input: PathBuf,
    #[arg(long, default_value = "target/firebreak-state")]
    state: PathBuf,
}
#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let a = Args::parse();
    if !safe_state_path(&a.state) {
        anyhow::bail!("unsafe state path");
    }
    let raw =
        std::fs::read_to_string(&a.input).with_context(|| format!("read {}", a.input.display()))?;
    let req: ServiceRequest = serde_json::from_str(&raw)?;
    std::fs::create_dir_all(&a.state)?;
    let out = FirebreakService::new(Config::default())?.handle(req, &a.state)?;
    println!("{}", serde_json::to_string_pretty(&out)?);
    Ok(())
}
