# Architecture

## System Overview

Provenance Firebreak is a 22-crate Rust supply-chain lineage containment system. The architecture organizes around three layers: **Evidence (bottom)**, **Attestation & Policy (middle)**, **Application & Control (top)**, with **Adapters** bridging external systems.

---

## Crate Dependency & Responsibility Matrix

| Crate | Context | Responsibility | Typed API | Dependencies / Callers | ADR / DDD Refs | Tasks | Tests | Acceptance | Non-Ceremonial Reason |
|-------|---------|-----------------|-----------|------------------------|----------------|-------|-------|-----------|----------------------|
| **pf-identity** | Bottom-left: foundational | Cryptographic identity anchors; keypair lifecycle; issuer / subject URIs; aud/iss/sub claims model | `Identity`, `KeyMaterial`, `Subject`, `Issuer`, `Claim` (all generic over Algorithm) | Called by: `pf-attestation`, `pf-policy`, `pf-service`, `pf-cli` | DDD: Identity aggregate; ADR-001 (algorithm agnosticity) | Enum Algorithm variants; Keypair serialize/deserialize; claim resolution; subject URI canonicalization | Unit: Algorithm round-trip; Integration: Identity in attestation verification | Can verify an attestation signed by a stored identity without network calls; keypair never leaves process unless explicitly exported | Cryptographic identity is the root of all trust; without it, attestation is orphaned |
| **pf-artifact** | Bottom-left: evidence | Artifact representation; content-addressable storage; hash genealogy; multiple hash formats | `Artifact`, `ArtifactID`, `Hash`, `Digest`, `StorageRef` | Called by: `pf-lineage`, `pf-graph`, `pf-evidence`, `pf-application`, `pf-evaluation` | DDD: Artifact aggregate; ADR-002 (content-addressed naming) | Hash function support (SHA256, SHA512, BLAKE3); storage backend abstraction; digest normalization; content streaming | Unit: Hash round-trip, digest equality; Integration: Artifact in lineage graph | Store and retrieve artifacts by multiple hash formats; compare artifacts by digest equivalence | Content-addressed storage decouples artifact identity from transport; essential for reproducible builds |
| **pf-attestation** | Middle-left: evidence binding | Attestation envelope; signing & verification; predicate + subject binding; temporal claims; signature algorithms | `Attestation`, `SignedStatement`, `Predicate`, `PredicateType`, `Signature`, `VerificationResult` | Depends: `pf-identity`, `pf-artifact`; Called by: `pf-policy`, `pf-evaluation`, `pf-service` | DDD: Attestation aggregate; ADR-003 (SLSA Provenance v1 subset); ADR-004 (Timestamp service integration) | Predicate type registry; signature verification against identity; timestamp proof chaining; predicate JSON schema validation | Unit: Sign & verify round-trip; predicate type dispatch; Integration: Attestation validation in policy | Verify an attestation with a recorded timestamp and confirm signature matches identity; reject if timestamp outside acceptable window | Attestation is the binding glue; without it, artifacts and their provenance are unrelated |
| **pf-lineage** | Middle: provenance graph | Artifact provenance chains; predecessor/successor edges; build step history; dependency trees; cyclic detection | `Lineage`, `LineageNode`, `Edge`, `ProvenanceStep`, `DependencyTree`, `CycleDetection` | Depends: `pf-artifact`, `pf-attestation`; Called by: `pf-graph`, `pf-policy`, `pf-evaluation`, `pf-application` | DDD: Lineage aggregate; ADR-005 (DAG enforcement, no cycles) | Lineage serialization (JSON, binary); cycle detection algorithm; path finding (artifact A → B → C); transitive dependency resolution | Unit: Cycle detection; path finding; Integration: Lineage in policy evaluation | Trace an artifact back to its sources; confirm no cycles in the lineage; list all transitive dependencies | Lineage is the logical spine of the system; it answers "how did this artifact come to be?" |
| **pf-exposure** | Middle: risk surface | Exposure scoring; vulnerability surface area; privilege elevation paths; dependency risk propagation | `ExposureScore`, `Vulnerability`, `ElevationPath`, `RiskVector`, `SurfaceArea` | Depends: `pf-lineage`, `pf-artifact`; Called by: `pf-policy`, `pf-evaluation` | DDD: ExposureScore value object; ADR-006 (risk propagation algorithm) | Vulnerability data source integration; transitive risk aggregation; path enumeration; score normalization | Unit: Score calculation; path finding; Integration: Exposure in policy gates | Calculate a score (0–100) for an artifact; trace which dependencies contribute risk | Exposure lets policies quantify "how broken can this get?"; without it, risk gates are binary |
| **pf-policy** | Middle-right: control gates | Policy definition; evaluation rules; enforcement gates; approval workflows; audit trails | `Policy`, `PolicyRule`, `Condition`, `Gate`, `ApprovalWorkflow`, `PolicyEvaluationLog` | Depends: `pf-identity`, `pf-attestation`, `pf-lineage`, `pf-exposure`; Called by: `pf-planning`, `pf-evaluation`, `pf-service`, `pf-application` | DDD: Policy aggregate; ADR-007 (CEL-based rules); ADR-008 (policy versioning and rollout) | Policy language compiler; gate evaluation engine; condition predicates (language, hash, identity, exposure, time); audit log write | Unit: CEL parsing & evaluation; gate dispatch; Integration: Policy in deployment decision | Evaluate a policy rule against an attestation + lineage; log the decision and condition values | Policy is where the human intent ("we only deploy from main, signed by trusted key") meets enforcement |
| **pf-planning** | Top-left: orchestration | Deployment planning; supply-chain workflow definition; task DAGs; retry logic; conditional steps | `Plan`, `WorkflowDAG`, `Task`, `TaskDependency`, `RetryPolicy`, `ConditionalStep` | Depends: `pf-policy`; Calls: `pf-policy`, `pf-events`, `pf-calibration`; Called by: `pf-application`, `pf-service` | DDD: Plan aggregate; ADR-009 (workflow DAG semantics) | Workflow DSL parsing; DAG validation; task scheduling; branch-on-condition logic | Unit: DAG validation, cycle detection; Integration: Plan execution in application | Load a plan, validate it, execute tasks in dependency order, handle conditional branches | Planning separates the "what to do" (workflow) from "can we do it?" (policy) |
| **pf-calibration** | Middle: tuning | Model calibration; gate sensitivity tuning; exposure thresholds; cost/security tradeoffs | `Calibration`, `ModelParameters`, `ThresholdSet`, `TuningMetric`, `CostSecurityTradeoff` | Depends: `pf-exposure`, `pf-policy`; Called by: `pf-planning`, `pf-service` | DDD: Calibration value object; ADR-010 (Bayesian threshold learning) | Threshold setting; sensitivity analysis; cost-security Pareto frontier; online learning loop | Unit: Threshold computation; Pareto frontier calculation; Integration: Calibration in policy reload | Compute a sensitivity-adjusted gate threshold from historical deployment data; trade off false positives vs. false negatives | Calibration prevents gates from being "too loud" or "asleep"; it's the feedback loop |
| **pf-events** | Middle: observable | Event log; state transitions; audit trail; external event publication; time-ordered stream | `Event`, `EventType`, `EventLog`, `StateTransition`, `ExternalEventPublisher`, `EventTimestamp` | Depends: none (but messages travel everywhere); Called by: `pf-planning`, `pf-service`, `pf-cli`, `pf-application`, `pf-recovery` | DDD: Event (Domain Event pattern); ADR-011 (immutable event log, append-only) | Event serialization (JSON, protobuf); timestamp assignment; event publisher abstraction; stream replay | Unit: Event round-trip; timestamp ordering; Integration: Event replay in recovery | Write 100 events; replay them and confirm final state matches live state | Events are the transaction log; without them, recovery and audit are impossible |
| **pf-ports** | Bottom-right: I/O abstraction | Storage backend abstraction; network transport abstraction; filesystem/DB pluggability | `StorageBackend`, `TransportBackend`, `FilesystemBackend`, `DatabaseBackend` (all traits) | Depends: none; Called by: all other crates (via trait objects) | DDD: Port/Adapter pattern | Storage trait definition; transport trait definition; in-memory + filesystem implementations | Unit: each backend against its trait contract; Integration: crates swapping backends | Swap storage from filesystem to in-memory in a test without changing application logic | Ports isolate application logic from infrastructure; they're why the system is testable at all |
| **pf-adapter-sigstore** | Bottom-right: external binding | Sigstore client integration; OIDC bridge; signature verification against Sigstore PKI | `SigstoreClient`, `OIDCBridge`, `TransparencyLogProof`, `VerificationRequest` | Depends: `pf-identity`, `pf-attestation`, `pf-ports`; Called by: `pf-service`, `pf-application`, `pf-evaluation` | DDD: Adapter pattern; ADR-012 (Sigstore transparency log inclusion) | Sigstore API client; OIDC token acquisition; transparency log proof verification; rate limiting | Unit: OIDC token acquisition (mocked); proof verification; Integration: Sigstore identity verification in policy | Verify an attestation signature against Sigstore's public key; confirm artifact was included in the transparency log | Sigstore makes identity issuance ephemeral and audit-friendly; it's where production identity comes from |
| **pf-adapter-ruvector** | Bottom-right: external binding | RuvVector client integration; vector database interface; similarity search for artifacts | `RuvectorClient`, `VectorEmbedding`, `SimilaritySearch`, `EmbeddingIndex` | Depends: `pf-artifact`, `pf-ports`; Called by: `pf-evaluation`, `pf-application` | DDD: Adapter pattern; ADR-013 (semantic artifact clustering) | RuvVector API client; embedding generation/caching; similarity threshold tuning | Unit: embedding distance calculation; Integration: similarity-based gates in policy | Find artifacts semantically similar to a given artifact; score their distance | RuvVector adds semantic gates ("did we build something like this before?") |
| **pf-adapter-rvf** | Bottom-right: external binding | RVF (Rust Verification Framework) integration; compiler plugin hookpoint; build-time proof collection | `RVFClient`, `BuildProof`, `CompilerPluginAdapter`, `VerificationReport` | Depends: `pf-attestation`, `pf-artifact`, `pf-ports`; Called by: `pf-service`, `pf-application` | DDD: Adapter pattern; ADR-014 (build-time proof collection) | RVF API client; build harness integration; proof serialization; plugin handshake | Unit: proof round-trip; Integration: RVF proofs in attestation | Capture a build proof from RVF; embed it in an attestation; verify it later | RVF proofs anchor attestations to compiler events; they prevent backdoors in the build |
| **pf-graph** | Middle: data structure | Provenance graph datastructure; graph query engine; reachability; subgraph extraction | `Graph`, `GraphNode`, `GraphEdge`, `Reachability`, `SubgraphExtractor`, `GraphQuery` | Depends: `pf-artifact`, `pf-lineage`, `pf-attestation`; Called by: `pf-policy`, `pf-evaluation`, `pf-application` | DDD: Graph value object; ADR-015 (immutable graph snapshots for query consistency) | Graph serialization (GraphML, DOT, JSON); BFS/DFS traversal; reachability matrix computation; subgraph extraction by predicate | Unit: reachability correctness; subgraph correctness; Integration: graph in policy queries | Query: "all artifacts reachable from X"; "all attestors on the path X → Y" | Graph is the query engine; it turns lineage into actionable intelligence |
| **pf-evidence** | Bottom-center: repository | Evidence repository; immutable storage; content-addressed evidence chunks; deduplication | `EvidenceRepository`, `EvidenceChunk`, `EvidenceIndex`, `ChunkHash`, `DeduplicationMap` | Depends: `pf-ports`, `pf-artifact`, `pf-attestation`; Called by: `pf-recovery`, `pf-service`, `pf-evaluation` | DDD: Repository aggregate; ADR-016 (immutable append-only evidence store) | Chunk storage; content deduplication; index maintenance; garbage collection (mark-and-sweep) | Unit: chunk round-trip; deduplication verification; Integration: evidence recovery | Store 1000 attestations; query all evidence for artifact X; confirm deduplication removes half | Evidence is the physical store; it must never be mutable, or recovery becomes impossible |
| **pf-recovery** | Top-right: resilience | State recovery; crash consistency; replay from event log; evidence reconstruction; orphaned attestation cleanup | `RecoveryEngine`, `CrashConsistency`, `ReplayState`, `RecoveryReport` | Depends: `pf-events`, `pf-evidence`, `pf-lineage`, `pf-attestation`; Called by: `pf-service`, `pf-application` | DDD: Recovery aggregate; ADR-017 (three-phase recovery: validate, replay, GC) | Event log replay; consistency check; orphan detection & cleanup; roll-forward recovery | Unit: replay correctness; orphan detection; Integration: recovery after simulated crash | Corrupt the event log and evidence store; run recovery; confirm final state is consistent | Recovery is the system's immune system; it must survive Byzantine evidence |
| **pf-application** | Top: orchestrator | Main orchestration; endpoint routing; policy/planning/evaluation coordination; error handling; context propagation | `Application`, `RequestContext`, `EndpointRouter`, `ErrorHandler`, `ContextPropagation` | Depends: `pf-service` (calls it); Calls: all crates via service; Called by: `pf-cli`, `pf-service` | DDD: Application service (Layered Architecture); ADR-018 (context as ambient authority) | Request routing; service coordination; error propagation; telemetry integration | Unit: routing correctness; Integration: end-to-end workflows | Receive a deploy request; route through policy → planning → evaluation; return result | Application is the glue; it's where policy, planning, and evaluation meet user intent |
| **pf-config** | Bottom-right: configuration | Configuration schema; environment variable parsing; file-based config loading; validation | `Config`, `ConfigSchema`, `EnvironmentParser`, `FileLoader`, `ConfigValidator` | Depends: `pf-ports`; Called by: `pf-service`, `pf-application` | DDD: Config value object; ADR-019 (schema-validated configuration) | Schema definition (JSON Schema); env var interpolation; file format support (TOML, YAML); validation | Unit: parse & validate config; Integration: config in service initialization | Load a config file; confirm all required fields are present; confirm types are correct | Config determines runtime behavior; it must be validated and auditable |
| **pf-telemetry** | Top-right: observability | Metrics, traces, and logs; structured logging; metric emission; distributed tracing integration | `Telemetry`, `MetricRegistry`, `Tracer`, `Logger`, `SpanContext` | Depends: `pf-events`, `pf-ports`; Called by: all crates (via macros) | DDD: Telemetry value object; ADR-020 (structured logging, OpenTelemetry compat) | Metric types (Counter, Histogram, Gauge); trace span creation/propagation; log level filtering; backend abstraction | Unit: metric emission; Integration: metrics in service monitoring | Emit a counter, query it; emit a span, confirm parent-child relationship | Telemetry is how we know the system is alive; it's non-negotiable for production |
| **pf-service** | Top: runtime | Service runtime; lifecycle management; background tasks; signal handling; graceful shutdown | `Service`, `Lifecycle`, `BackgroundTask`, `SignalHandler`, `GracefulShutdown` | Depends: `pf-application`, `pf-config`, `pf-telemetry`, `pf-events`, `pf-recovery`; Called by: `pf-cli` | DDD: Service aggregate (Domain Service); ADR-021 (structured service lifecycle) | Service startup/shutdown; task scheduling; signal trapping (SIGTERM, SIGINT); drain + GC | Unit: lifecycle state transitions; Integration: service under load | Start service; send SIGTERM; confirm graceful drain (in-flight requests complete, no new ones accepted) | Service is the runtime; it must shutdown cleanly or data is lost |
| **pf-cli** | Top: interface | Command-line interface; argument parsing; subcommand dispatch; human output formatting | `CLI`, `Command`, `SubcommandDispatcher`, `OutputFormatter`, `ArgumentParser` | Depends: `pf-service`, `pf-application`, `pf-events`; Called by: user | DDD: CLI value object; ADR-022 (12-factor CLI design) | Argument parser (clap); subcommand registry; structured output (JSON, YAML, table); completion generation | Unit: command parsing; Integration: end-to-end CLI workflows | Run `pf-cli deploy --artifact X --policy-id Y`; confirm output format and exit code | CLI is the human interface; it must be discoverable and forgiving |
| **pf-evaluation** | Top-left: decision engine | Attestation + lineage evaluation; compliance checking; deployment fitness scoring | `Evaluator`, `EvaluationContext`, `ComplianceReport`, `FitnessScore`, `EvaluationAuditLog` | Depends: `pf-policy`, `pf-lineage`, `pf-graph`, `pf-exposure`, `pf-attestation`, `pf-artifact`; Called by: `pf-application`, `pf-service`, `pf-planning` | DDD: Evaluator service; ADR-023 (policy evaluation as pure function) | Evaluation engine; condition evaluation; report generation; decision logging | Unit: policy evaluation correctness; Integration: evaluation in deployment gate | Evaluate policy rule X against attestation + lineage + exposure; log all condition values | Evaluation is where policy becomes binary: approve or deny |

---

## Dependency Direction Graph

```
┌─────────────────────────────────────────────────────────────────┐
│                     pf-application (Top)                         │
│              (Orchestrator: policy→planning→eval)                │
└─────────────────────────────────────────────────────────────────┘
        ↑           ↑                  ↑           ↑
        │           │                  │           │
    ┌───┴──────┬────┴───┐          ┌───┴──────┬────┴──┐
    │          │        │          │          │       │
    ↓          ↓        ↓          ↓          ↓       ↓
┌────────┐ ┌──────────┐ ┌──────────┐  ┌────────────┐  ┌──────────┐
│pf-cli  │ │pf-service│ │pf-planning│  │pf-evaluation│ │pf-config │
└────────┘ └──────────┘ └──────────┘  └────────────┘  └──────────┘
    │          ↓              ↓              ↓             │
    │      (all deps)     ┌───┴──────┐      ↓             │
    │          │          │          │      ↓             ↓
    │          ↓          ↓          ↓      ↓          ┌──────────┐
    │      ┌──────────────┴──────────┴──────┴──────────→│pf-ports  │
    │      │                                            └──────────┘
    │      ↓
    │  ┌──────────┐      ┌──────────┐      ┌────────────────────┐
    │  │pf-policy │←─────│pf-lineage│      │pf-attestation      │
    │  └──────────┘      └──────────┘      └────────────────────┘
    │      ↑                   ↑                    ↑       ↑
    │      │                   │                    │       │
    │      ↓                   ↓                    ↓       ↓
    │  ┌──────────────┐   ┌──────────────┐   ┌──────────┐  │
    │  │pf-exposure   │   │pf-graph      │   │pf-identity│  │
    │  └──────────────┘   └──────────────┘   └──────────┘  │
    │      ↑                   ↑                           │
    │      │                   │       ┌─────────────────┐ │
    │      └───────────────────┴───────→│pf-artifact      │ │
    │                                    └─────────────────┘ │
    │                                           ↑            │
    │                                           │            │
    └───────────────────────────────────────────┴────────────┘
              (pf-cli & pf-service call everything)

    ┌──────────────────────────────────────┐
    │      Adapters (Extern Boundary)      │
    ├──────────────────────────────────────┤
    │  pf-adapter-sigstore  (→ Sigstore)   │
    │  pf-adapter-ruvector  (→ RuvVector)  │
    │  pf-adapter-rvf       (→ RVF)        │
    └──────────────────────────────────────┘
         ↑           ↑           ↑
         │           │           │
    Calls from: pf-service, pf-application, pf-evaluation

    ┌──────────────────────────────────────┐
    │    Infrastructure (Event/Evidence)   │
    ├──────────────────────────────────────┤
    │  pf-events (immutable log)           │
    │  pf-evidence (repository)            │
    │  pf-recovery (replay + consistency)  │
    │  pf-telemetry (metrics/traces)       │
    │  pf-calibration (tuning)             │
    └──────────────────────────────────────┘
         ↑           ↑           ↑
         │           │           │
    Calls from: all others, especially pf-service & pf-application
```

---

## State Machine

### Core Attestation Lifecycle

```
[New Attestation]
        │
        ↓
   [Signing] ────→ (requires pf-identity + key material)
        │
        ↓
   [Signed] ────→ (immutable, in memory or pf-events log)
        │
        ↓
 [Policy Eval] ──→ (pf-policy evaluates conditions against pf-lineage, pf-exposure)
        │
        ├─→ [Approved] ──→ [Stored in pf-evidence] ──→ [Recovery Eligible]
        │
        └─→ [Denied] ────→ [Event logged, not stored]
```

### Deployment Planning & Execution

```
[Request] (from pf-cli/pf-application)
    │
    ↓
[Policy Gate] (pf-policy evaluates against attestation + lineage)
    │
    ├─→ [DENY] ──→ [Return Error] ──→ End
    │
    └─→ [APPROVE]
        │
        ↓
    [Planning] (pf-planning creates workflow DAG from pf-planning rules)
        │
        ↓
    [Calibration] (pf-calibration tunes gate thresholds)
        │
        ↓
    [Task Execution] (pf-service executes tasks in DAG order)
        │
        ├─→ [Task Fail] ──→ [Retry Logic] ──→ (from pf-planning)
        │
        └─→ [Task Success]
            │
            ↓
        [Evaluation] (pf-evaluation scores fitness; pf-graph queries reachability)
            │
            ├─→ [Fitness Below Threshold] ──→ [Rollback via pf-recovery]
            │
            └─→ [Fitness Adequate]
                │
                ↓
            [Emit Event] (pf-events appends to log)
                │
                ↓
            [Complete]
```

### Crash Recovery

```
[Service Crash]
    │
    ↓
[Restart]
    │
    ↓
[pf-recovery starts: Phase 1 — Validate]
    │ (read pf-evidence repository, check integrity)
    │
    ├─→ [Evidence Corrupt] ──→ [Stop, alert operator]
    │
    └─→ [Evidence Valid]
        │
        ↓
    [Phase 2 — Replay Events]
        │ (read pf-events log from last checkpoint, apply in order)
        │
        ↓
    [Phase 3 — Consistency Check & GC]
        │ (orphaned attestations; unreachable lineage nodes)
        │
        ↓
    [Ready to Accept Requests]
```

---

## End-to-End Path: Deploy an Artifact

### Entry Point: User runs `pf-cli deploy --artifact <ID> --policy-id <policy-id>`

```
1. CLI Parsing (pf-cli)
   └─→ Deserialize args, load config (pf-config)

2. Service Initialization (pf-service)
   └─→ Read pf-config, start pf-telemetry, load pf-events log, run pf-recovery

3. Policy Evaluation (pf-policy + pf-attestation + pf-lineage + pf-exposure)
   ├─→ Load policy rule from pf-policy
   ├─→ Fetch attestation (already in pf-evidence or from pf-adapter-sigstore)
   ├─→ Fetch artifact from pf-artifact
   ├─→ Build lineage graph from pf-lineage (via pf-graph)
   ├─→ Calculate exposure score from pf-exposure
   └─→ Evaluate CEL rule: IF (identity_trusted AND lineage_from_main AND exposure < 50) → APPROVE

4. Planning (pf-planning)
   └─→ Load deployment workflow from pf-planning rules
       ├─→ Task 1: fetch binary from cache
       ├─→ Task 2: verify signature (calls pf-adapter-sigstore)
       ├─→ Task 3: check RVF proofs (calls pf-adapter-rvf)
       └─→ Task 4: deploy to cluster

5. Calibration (pf-calibration)
   └─→ Tune policy thresholds based on historical data

6. Task Execution (pf-service orchestrates)
   ├─→ Execute Task 1: Success → emit event
   ├─→ Execute Task 2: Success → emit event
   ├─→ Execute Task 3: Fail → retry (from pf-planning retry policy)
   │   └─→ Retry succeeds → emit event
   └─→ Execute Task 4: Success → emit event

7. Evaluation (pf-evaluation)
   └─→ Score deployment fitness
       ├─→ Check: "All lineage ancestors from trusted sources?" (via pf-graph)
       ├─→ Check: "Exposure did not increase?" (via pf-exposure)
       └─→ Fitness = 95 → APPROVE

8. Event Logging (pf-events)
   └─→ Append DeploymentApproved, TaskSuccess, EvaluationResult to log

9. Evidence Storage (pf-evidence)
   └─→ Store attestation, lineage snapshot, evaluation report (deduplicated)

10. Return to User (pf-cli)
    └─→ Print: "Deployment approved. Artifact <ID> deployed to production."

11. Telemetry (pf-telemetry)
    └─→ Emit: counter (deployments_approved), histogram (policy_eval_ms), trace (deploy_request_span)
```

---

## Policy, Failure, and Recovery

### Policy Gates (pf-policy)

| Gate Name | Condition | Failure Mode | Recovery |
|-----------|-----------|--------------|----------|
| **trusted_identity** | Attestation signed by identity in pf-identity trust store | Deny if signer unknown | Operator approves signer via pf-cli; stored in pf-config |
| **lineage_from_main** | All ancestors of artifact reachable from main branch (via pf-lineage + pf-graph) | Deny if feature branch detected | Rebase branch onto main, re-run build, re-attest |
| **exposure_threshold** | ExposureScore (from pf-exposure) < 50 | Deny if vulnerable deps | Update deps, rebuild, re-attest |
| **no_orphans** | No unreachable attestations in artifact lineage (pf-graph reachability) | Deny if orphans found | pf-recovery GC phase removes orphans; re-evaluate |
| **time_window** | Attestation timestamp within last 24h (pf-attestation temporal claims) | Deny if stale | Re-attest fresh; old attestations can be re-signed by pf-adapter-sigstore |

### Failure Modes & Recovery

| Failure | Detection | Recovery |
|---------|-----------|----------|
| **Attestation invalid** (signature mismatch) | pf-attestation verification fails | Reject artifact; operator inspects signature; re-attest if compromise ruled out |
| **Lineage cycle detected** | pf-lineage or pf-graph detects loop | pf-recovery orphan cleanup; manual graph inspection |
| **Exposure explosion** (new CVE) | pf-exposure score jumps | Gate denies deployment; operator patches deps, triggers rebuild |
| **Evidence corruption** | pf-evidence integrity check fails (checksum mismatch) | pf-recovery detects and stops; alert operator; rollback recent merges |
| **Event log gap** (missing events) | pf-recovery replay finds state jump | Replayed state != live state; fall back to manual reconciliation |
| **Service crash during task** | pf-service killed mid-deployment | pf-recovery Phase 2: replay events from checkpoint; re-run incomplete task if safe |

---

## Evidence

### Evidence Sources

| Source | Format | Stored In | Retention | Use |
|--------|--------|-----------|-----------|-----|
| **Attestations** | SLSA Provenance + custom predicates | pf-evidence (deduplicated by hash) | Forever (append-only) | Policy gates; lineage reconstruction |
| **Build Proofs** | RVF compiler plugin output | pf-attestation (embedded as predicate) | Forever | Antitampering; proof of compiler state |
| **Lineage Graphs** | DAG serialized to JSON (pf-graph snapshots) | pf-evidence | Per-deployment (n snapshots for n deploys) | Reachability queries; risk propagation |
| **Events** | Domain events (DeploymentRequested, PolicyApproved, etc.) | pf-events (append-only log) | Forever | Recovery replay; audit trail |
| **Exposure Scores** | JSON (artifact ID + vulnerability list + score) | pf-evidence | Per-scan (historical) | Threshold trending; policy calibration |
| **Policy Decisions** | CEL rule + condition values + decision (approve/deny) | pf-events | Forever | Audit compliance; policy effectiveness review |

### Evidence Reconstruction from Events

```
Live state at time T:
  - Run pf-recovery Phase 2: replay all pf-events from time 0 to T
  - Apply each event in order: attestation added, policy evaluated, artifact deployed, etc.
  - Final state = authoritative lineage + exposure + policy decisions
  - Proof: pf-evidence repository has all artifacts; deduplication hash confirms we can reconstruct
```

---

## Ablations

### What Breaks If We Remove Each Crate

| Crate Removed | Consequence | Why Impossible to Skip |
|---------------|-------------|------------------------|
| **pf-identity** | No cryptographic identity; attestations float unsigned | Attestations without signing are worthless; trust collapses |
| **pf-artifact** | No artifact versioning; content addressing gone | Can't distinguish two builds of the same software; supply-chain tracking broken |
| **pf-attestation** | Attestations unsigned; no SLSA Provenance | Core promise (verifiable supply-chain) gone |
| **pf-lineage** | No ancestry tracking; "how was this built?" unanswerable | Lineage *is* supply-chain provenance; its absence defeats the whole system |
| **pf-exposure** | No vulnerability scoring; gates become boolean (approve/deny only) | Can't quantify "how risky is this?"; blind spots in dependencies |
| **pf-policy** | No enforcement; all artifacts flow through | Users lose control; system is compliance theater |
| **pf-planning** | No workflow DAG; tasks execute unordered | Deployments become chaotic; dependencies not honored |
| **pf-calibration** | Gate thresholds static; no feedback loop | Gates too loose or too strict; no improvement over time |
| **pf-events** | No audit trail; recovery impossible | Can't replay state; can't answer "what happened?"; compliance failure |
| **pf-ports** | Everything hard-coded to one backend (e.g., PostgreSQL) | Can't test in isolation; can't swap backends; system locked to infra choice |
| **pf-adapter-sigstore** | No OIDC identity issuance; attestations not public-verifiable | Locks system to an organization; no external auditability |
| **pf-adapter-ruvector** | No semantic similarity gates | Can't detect "we built something like this"; redundant builds go undetected |
| **pf-adapter-rvf** | No build-time proofs; backdoors in build undetected | Attestations disconnected from compiler; supply-chain gap |
| **pf-graph** | Lineage not queryable; reachability unknown | Can't answer "all artifacts from main?" or "all dependencies of X?" |
| **pf-evidence** | No immutable store; attestations lost on restart | Recovery impossible; audit trail evaporates |
| **pf-recovery** | Crashes = data loss; no replay | System becomes fragile; ops fear restarts |
| **pf-application** | No orchestrator; crates unusable together | Disconnected components; no supply-chain system |
| **pf-config** | Config hard-coded; no env var support | Deployment inflexible; every env change = recompile |
| **pf-telemetry** | No metrics/logs; system is a black box | Ops blind; can't debug; can't measure SLOs |
| **pf-service** | No runtime; no graceful shutdown | Data corruption on restart; no signal handling |
| **pf-cli** | No human interface; API-only | Only programmable access; operators locked out |
| **pf-evaluation** | No fitness scoring; gates are one-shot | Can't verify deployment outcomes; no feedback for policy tuning |

---

## Implementation Roadmap Notes

- **Phases:** Identity bootstrap (pf-identity) → Attestation signing (pf-attestation) → Lineage tracking (pf-lineage + pf-graph) → Policy gates (pf-policy) → Planning (pf-planning) → Adapters (sigstore/ruvector/rvf) → Recovery (pf-recovery + pf-events) → Production ops (pf-telemetry, pf-calibration).
- **Testing:** Unit tests per crate + integration tests crossing crate boundaries (e.g., "policy evaluation with real lineage graph"). No end-to-end without all crates.
- **Deployment:** pf-service as daemon; pf-cli as operator interface; pf-config determines backend (in-mem for tests, PostgreSQL for prod).
- **Observability:** Every gate decision logged to pf-events and pf-telemetry; every failure routed through pf-recovery.
