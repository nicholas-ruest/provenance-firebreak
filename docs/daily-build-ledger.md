# Dream Machine daily-build ledger

| Date | Project | Repository | Capability | Status |
|---|---|---|---|---|
| prior | JitterMap | `nicholas-ruest/jitter-map` | fair, evidence-bound retry orchestration | reference benchmark only |
| prior | ToolRecall | `nicholas-ruest/toolrecall` | tool-use recall and selection | reference benchmark only |
| prior | EvoSeal | `nicholas-ruest/evo-seal` | evolutionary policy sealing | prior art |
| 2026-10-16 | Provenance Firebreak | `nicholas-ruest/provenance-firebreak` | signed lineage incident containment and sealed recovery | candidate |

## Novelty decision

Provenance Firebreak is materially distinct from retry admission (JitterMap), tool retrieval (ToolRecall), and evolutionary policy promotion (EvoSeal). Its problem is software-supply-chain incident containment; its architecture centers on signed attestations, temporal deployment lineage, calibrated risk, survivability-constrained graph cuts, and sealed replay evidence. Failed utilities such as `cordon-budget`, `proposal-sieve`, and `epoch-envelope` were rejected as negative scale examples, not reused.
