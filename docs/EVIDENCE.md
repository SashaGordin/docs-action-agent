# Evidence Ledger

Use repository-relative links until a public remote exists. Replace `planned` entries with commit hashes/URLs and durable artifacts as work is produced. Each evaluation must state code revision, corpus version, evaluation-set version, provider/model, and configuration.

## 2026-09-22 — Bootstrap

| Evidence | Link | State / result |
|---|---|---|
| Product and final definition of done | [SPEC](SPEC.md) | Produced |
| 42-session execution plan | [SPRINT](SPRINT.md) | Produced |
| Architecture decisions | [DECISIONS](DECISIONS.md) | Produced; corpus/provider details pending |
| Learning resource map | [SOURCES](SOURCES.md) | Produced |
| Planning consistency validation | [STATUS](STATUS.md#validation-state) | Passing |
| Commit | — | Not available: directory was not a Git repository at bootstrap |
| Application tests/evaluations | — | Not applicable: no application code was created |

## 2026-09-23 — Session 1 baseline and corpus decision

| Evidence | Link | State / result |
|---|---|---|
| Learning and roadmap baseline | [Learning matrix](LEARNING_MATRIX.md) | Produced from Sasha's diagnostic explanations; gaps and deferred topics retained |
| Written request-path explanation | [Request-path evidence](LEARNING_MATRIX.md#request-path-explanation-evidence) | Produced; provider-adapter and deterministic validation gaps identified |
| Provisional corpus decision | [ADR-006](DECISIONS.md#adr-006--provisional-fastapi-english-documentation-corpus) | FastAPI English docs selected; immutable pin and bounded paths due by 2026-10-06 |
| Local version control | [Status](STATUS.md) | Git initialized on `main`; no remote or GitHub repository created |
| Session validation | [Status](STATUS.md#validation-state) | All Session 1 and documentation checks passed on 2026-09-23 |
| Application tests/evaluations | — | Not applicable: Session 1 intentionally added no application code |

## Planned weekly evidence

| Gate | Required durable evidence |
|---|---|
| Week 1 | Gap matrix, architecture sketch, typed API vertical slice, tests, container smoke check, request-path explanation, weekly note |
| Week 2 | Tool scenario results, allowlist/timeout/step-limit tests, agent-vs-workflow ADR, denied-tool evidence, short demo |
| Week 3 | Corpus manifest, 15–20 case evaluation set, retrieval comparison, citation/abstention results, retrieval ADR |
| Week 4 | Repeatable evaluation report, traces/log evidence, threat model, approval/authorization tests, failure analysis |
| Week 5 | CI run, Docker/setup proof, health/reset/runbook exercise, reviewer notes, prioritized failure and fix |
| Week 6 | Final report, diagrams, runbook, known limitations, two-minute demo, five-minute walkthrough, case study, resume bullets, presentation notes |

## Session entry template

```text
Date / session:
Commit or artifact link:
Concept explained without notes:
Commands and results:
Evaluation configuration (if applicable):
Failure or confusion:
Decision/status changes:
Next smallest step:
```
