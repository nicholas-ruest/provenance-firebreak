//! Structured tracing boundary (DDD-11).
use pf_events::DomainEvent;
use tracing::info;
pub fn init() {
    let _ = tracing_subscriber::fmt()
        .with_env_filter("info")
        .with_test_writer()
        .try_init();
}
pub fn record(e: &DomainEvent) {
    info!(sequence=e.sequence,kind=?e.kind,subject=%e.subject.as_str(),"domain_event");
}
#[cfg(test)]
mod tests {
    use super::*;
    use pf_events::EventKind;
    use pf_identity::DigestId;
    #[test]
    fn records() {
        init();
        record(&DomainEvent::new(
            1,
            EventKind::LineageBuilt,
            DigestId::of(b"x"),
            "x",
        ));
    }
}
