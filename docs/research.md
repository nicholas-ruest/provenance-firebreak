# Provenance Firebreak — Research

## 1. Research method and a disclosed limitation

This document is required to cite primary sources, not secondary summaries,
and to never invent a fact it cannot support. In this session, the network
research tools available to the agent (`WebSearch`, `WebFetch`) were denied
by the session's permission mode, and the RuvNet grounding tool
(`search_ruvnet`) and the `ruvector` MCP server both failed to connect
(`CONNECTION_CLOSED` / `CONNECT_TIMEOUT`) before this document was written.
No live fetch of any external page happened in this session.

Consequently every claim below is labeled with one of:

- **Verified locally** — confirmed against a file or hash on this machine,
  in this session (git blob hashes, local repo contents).
- **Stated by the task brief** — taken directly from the ingredient
  specification given for this project, not independently re-derived.
- **From training knowledge, not live-verified this session** — a fact the
  model holds with high confidence from pretraining (e.g., a well-known
  project's existence, license, and general API shape) but did not
  re-fetch from a primary URL this session. These are flagged so a human
  can re-verify before Phase 2 pins any lockfile or commit SHA.
- **`PENDING_VERIFICATION`** — could not be confirmed from any source
  available this session. Not asserted as fact anywhere else in this
  repository. Per [ADR-0025](adrs/0025-pending-verification-discipline.md),
  this status is the required substitute for inventing a commit SHA, a
  paper citation, or an external claim.

## 2. Ingredient research (build-standard requirement: 2 Ruvnet + 1 enterprise OSS + 1 frontier research mechanism)

### 2.1 Ruvnet component #1 — `ruvector-core` 2.4.0, Apache-2.0

**Stated by the task brief**: version 2.4.0, Apache-2.0, exposes `insert` /
`search` / `get`. This project uses that exact surface as its incident-
retrieval memory (see [pf-ruvector-adapter in architecture.md](architecture.md)
and [DDD-06](ddd/06-incident-retrieval.md)): sealed incident records are
`insert`-ed with an embedding of the lineage/attestation context, candidate
historical incidents are `search`-ed by nearest neighbor at decision time,
and the full incident record is `get`-ed by id once a candidate is selected
for use as a calibration or planning input.

Attempted grounding this session: `search_ruvnet` (the RuvNet brain MCP
tool) and the `ruvector` MCP server were both called as part of this
project's research step and both failed to connect
(`ruvnet-brain`: `CONNECT_TIMEOUT`; `ruvector`: `CONNECTION_CLOSED`). No
additional API surface beyond `insert`/`search`/`get` is asserted. Exact
function signatures, the embedding dimensionality, and the distance metric
are `PENDING_VERIFICATION` and must be confirmed against the real
`ruvector-core` 2.4.0 crate docs before `pf-ruvector-adapter` is implemented
in Phase 2.

### 2.2 Ruvnet component #2 — `rvf-crypto` 0.2.0, Apache-2.0

**Stated by the task brief**: version 0.2.0, Apache-2.0, provides
sealing and tamper-rejection primitives ("RVF" = Ruvnet's cognitive-
container format referenced in this machine's own `CLAUDE.md`). This
project uses that surface to seal replay evidence (decision inputs,
retrieved incidents, calibration scores, selected plan) into an
append-only, tamper-evident record — see
[pf-rvf-adapter / pf-evidence-ledger in architecture.md](architecture.md)
and [DDD-10](ddd/10-evidence-sealing.md).

Same grounding attempt and same outcome as §2.1: `search_ruvnet` and the
`ruvector` MCP server (which also surfaces RVF container tooling per this
machine's `CLAUDE.md`) were unreachable this session. The exact seal/verify
function names and the tamper-rejection error taxonomy are
`PENDING_VERIFICATION`.

### 2.3 Enterprise OSS component — `sigstore` crate 0.14.0, from `sigstore/sigstore-rs`, Apache-2.0

**From training knowledge, not live-verified this session**: `sigstore-rs`
is the Rust client for the Sigstore project (keyless signing via a Fulcio-
issued short-lived certificate bound to an OIDC identity, transparency
logging via Rekor, and bundle verification combining both). It is
maintained under the `sigstore` GitHub organization
(`https://github.com/sigstore/sigstore-rs`) and published to crates.io as
`sigstore` (`https://crates.io/crates/sigstore`), historically under the
Apache-2.0 license. This project uses the real upstream verification types
— certificate-chain verification against the Fulcio root, Rekor inclusion-
proof checking, and bundle (DSSE envelope) verification — as the Sigstore
boundary check in [pf-sigstore-adapter](architecture.md) and
[DDD-03](ddd/03-attestation-trust-boundary.md), per the task's explicit
requirement to use "real upstream types/interfaces," not a hand-rolled
re-implementation of signature verification.

The exact 0.14.0 release commit SHA on `sigstore/sigstore-rs` is
`PENDING_VERIFICATION` — it was not fetched this session and must not be
invented. Phase 2 must pin it from `Cargo.lock` once the crate is actually
added to a workspace.

### 2.4 Frontier research mechanism — split-conformal risk control

**From training knowledge, not live-verified this session**: split-
conformal prediction (holding out a calibration set, computing
nonconformity scores, and taking an empirical quantile to get a
distribution-free coverage guarantee) traces to Vovk, Gammerman, and
Shafer's conformal prediction framework, with the "split" variant
popularized by Lei, G'Sell, Rinaldo, Tibshirani, and Wasserman, "Distribution-
Free Predictive Inference for Regression" (2018). The specific shape this
project needs — a calibrated upper bound on a *risk/loss* (residual
exposure after quarantine), not just a prediction interval — is "conformal
risk control" as formalized in Angelopoulos, Bates, Candès, Jordan, and
Lei, "Conformal Risk Control" (arXiv:2208.02814), which generalizes split-
conformal calibration to monotone risk functions and is what this project
cites as its risk-bound construction in [pf-calibration](architecture.md)
and [DDD-07](ddd/07-risk-calibration.md).

This citation is given with the verification caveat stated in §1: it was
not re-fetched this session, so the arXiv identifier should be re-checked
against `https://arxiv.org/abs/2208.02814` before it is used in any
externally published material (e.g. [publication/](../publication/)).

## 3. Novelty — comparison against named prior systems

The task requires proving novelty against three named systems — JitterMap,
ToolRecall, EvoSeal — and against "primitive validators" as a generic
baseline class.

**Disclosure**: no primary source for JitterMap, ToolRecall, or EvoSeal was
located this session. Network research tools were denied and the model
does not hold a confident, source-backed recollection of published systems
with these exact names in the provenance/supply-chain-security space. Per
the anti-fabrication requirement in this project's own constraints
(§5 of [specification.md](specification.md), [ADR-0025](adrs/0025-pending-verification-discipline.md)),
this document does **not** invent a description, URL, or paper citation for
any of the three. Each is marked `PENDING_VERIFICATION` below. The
comparison table states, for each, the narrowest claim Provenance Firebreak
can defend without assuming unverified facts about the named system: that
Provenance Firebreak's five success criteria (exact reachability,
deterministic digest, calibrated coverage, cost beating quarantine-all,
explicit ablations — [specification.md §4](specification.md)) are not
satisfied by a name-matching architecture inferred from general industry
practice, and that if the named system turns out to satisfy one of them,
the gap narrows to exactly that criterion rather than invalidating the
others. This is weaker than a sourced comparison and is reported as such
rather than overstated.

| System | Source status | What the name suggests it does | Criterion Provenance Firebreak claims it as novel on, if the inferred description holds |
|--------|---------------|----------------------------------|---|
| JitterMap | `PENDING_VERIFICATION` — no primary source located this session | Name suggests network/timing jitter mapping, not an artifact-to-service lineage graph with cryptographic trust-boundary verification. | No evidence it performs Sigstore-boundary-verified, tenant-isolated, exact-reachability closure over a temporal deployment graph with a calibrated risk bound gating admission. |
| ToolRecall | `PENDING_VERIFICATION` — no primary source located this session | Name suggests tool-call/tool-use auditing or recall of prior tool invocations, not incident-retrieval-informed quarantine planning. | No evidence it ties retrieval to a statistically calibrated admission gate (split-conformal) rather than an uncalibrated similarity score. |
| EvoSeal | `PENDING_VERIFICATION` — no primary source located this session | Name suggests evolutionary sealing — plausibly adjacent to evidence sealing, but no evidence it combines sealing with least-disruptive planning under a hard tier-0 availability constraint. | No evidence of a least-disruptive planner that is provably cheaper than quarantine-all while respecting a calibrated risk bound; sealing alone does not establish that. |
| Primitive validators | Generic baseline class, not a specific system — no citation needed | Signature-presence checks, allow/deny lists, or single-hop "what did this builder touch" lookups with no temporal graph, no calibration, no planning. | Primitive validators have no notion of transitive closure over time-bounded deployment edges, no calibrated coverage guarantee, and typically degrade to quarantine-all or quarantine-nothing with no cost model. Provenance Firebreak's §4 success criteria in [specification.md](specification.md) are, by construction, criteria a primitive validator does not attempt. |

This table must be revisited the first time network research tools are
available: replace every `PENDING_VERIFICATION` row with a sourced
description and a primary URL, or retract the novelty claim for that row
if the source contradicts the inferred description.

## 4. Open research items carried into Phase 2

1. Confirm `ruvector-core` 2.4.0 and `rvf-crypto` 0.2.0 exact API signatures
   once `search_ruvnet`/`ruvector` MCP connectivity is restored.
2. Confirm the `sigstore` 0.14.0 commit SHA from a real `Cargo.lock` once the
   crate is vendored into a workspace (Phase 2; no workspace exists yet).
3. Re-verify the conformal-risk-control citation (§2.4) against a live
   fetch of the arXiv page.
4. Locate and re-run the novelty comparison in §3 against real primary
   sources for JitterMap, ToolRecall, and EvoSeal.
