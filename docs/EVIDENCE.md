# Evidence Ledger

Use repository-relative links for files and public GitHub URLs for remotely verifiable repository evidence. Replace `planned` entries with commit hashes/URLs and durable artifacts as work is produced. Each evaluation must state code revision, corpus version, evaluation-set version, provider/model, and configuration.

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
| Local version control | [Status](STATUS.md) | Git initialized on `main`; later published with the original history intact |
| Session artifact commit | `409ec75` | `Record Session 1 baseline and corpus decision` |
| Session validation | [Status](STATUS.md#validation-state) | All Session 1 and documentation checks passed on 2026-09-23 |
| Application tests/evaluations | — | Not applicable: Session 1 intentionally added no application code |

## 2026-10-12 — Public repository publication

| Evidence | Link | State / result |
|---|---|---|
| Public GitHub repository | [`SashaGordin/docs-action-agent`](https://github.com/SashaGordin/docs-action-agent) | Public; default branch `main` |
| History preservation | [Commit history](https://github.com/SashaGordin/docs-action-agent/commits/main/) | Existing local history published intact; no repository restart |
| Local tracking branch | [Status](STATUS.md) | Local `main` tracks `origin/main` over HTTPS |

## 2026-09-24 — Session 2 Python project and test harness

| Evidence | Link | State / result |
|---|---|---|
| Reproducible project definition | [`pyproject.toml`](../pyproject.toml) and [`uv.lock`](../uv.lock) | Python 3.12+ project; pytest 9.1.1 isolated in the `dev` dependency group |
| Package layout | [`src/docs_action_agent`](../src/docs_action_agent) | Importable `src/` package with no product behavior |
| First test | [`tests/test_smoke.py`](../tests/test_smoke.py) | Package import and pytest discovery passed |
| Concept explanation | [Status](STATUS.md) | Sasha distinguished project metadata, exact locked dependencies, project-scoped execution, and the limits of a passing unit test after targeted instruction |
| Validation | [Status](STATUS.md#validation-state) | `uv sync --locked`; Python 3.12.14; `1 passed in 0.00s` |
| Session artifact commit | `03239ae` | `Build Session 2 Python test harness` |

## 2026-09-25 — Session 3 typed HTTP boundary

| Evidence | Link | State / result |
|---|---|---|
| Provider-independent request/result contract | [`src/docs_action_agent/models.py`](../src/docs_action_agent/models.py) | `QuestionRequest` rejects missing, integer, empty, and whitespace-only questions; `QuestionResponse` limits status to `answered` or `abstained` |
| Model validation tests | [`tests/test_models.py`](../tests/test_models.py) | Valid input, malformed input, serialization, and unsupported status covered |
| Contract schema | [`QuestionRequest`](../src/docs_action_agent/models.py) | Generated schema requires a string with `minLength: 1`; no provider or retrieval fields |
| Concept explanation | [Status](STATUS.md) | Sasha classified valid/missing/malformed payloads and explained boundary validation as fail-fast protection; corrected redirect versus client-error status categories |
| Targeted resources | [Sources](SOURCES.md#fastapi-pydantic-and-pytest-primary-documentation) | Added exact Pydantic and pytest sections after the implementation diagnostic exposed missing mechanics |
| Validation | [Status](STATUS.md#validation-state) | Locked sync passed; Python 3.12.14; `8 passed in 0.03s`; model import and schema generation passed |
| Session artifact commit | `da1119e` | `Define Session 3 typed API contract` |

## 2026-09-30 — Session 4 provider seam and structured generation

| Evidence | Link | State / result |
|---|---|---|
| Application-owned provider boundary | [`src/docs_action_agent/provider.py`](../src/docs_action_agent/provider.py) | Async `TextProvider` protocol exposes one structured generation operation with no vendor SDK types |
| Structured provider output | [`ProviderResult` and `ProviderUsage`](../src/docs_action_agent/provider.py) | Answer plus input/output token usage represented by Pydantic models |
| Controlled failures | [`ProviderError` and `ProviderTimeout`](../src/docs_action_agent/provider.py) | Timeout crosses the boundary as an application-owned raised exception rather than a provider SDK error or success value |
| Deterministic fake tests | [`tests/test_provider.py`](../tests/test_provider.py) | Configured success and timeout paths pass with no network access |
| Environment-based settings | [`settings.py`](../src/docs_action_agent/settings.py) and [`.env.example`](../.env.example) | Required API key/model name load explicitly; secret uses `SecretStr`; real `.env` is ignored |
| Settings tests | [`tests/test_settings.py`](../tests/test_settings.py) | Controlled environment loads successfully and missing API key fails fast; no real credential used |
| Concept explanation | [Status](STATUS.md) | Sasha distinguished adapter/application responsibilities, provider usage from application telemetry, raised failures from returned success values, and explicit from import-time settings loading |
| Validation | [Status](STATUS.md#validation-state) | Locked sync passed; provider/settings imports passed; `12 passed in 0.05s`; `git diff --check` passed; secret scan reviewed with no credential value |
| Hosted adapter/live call | — | Intentionally deferred: optional for Session 4 and no provider/model or credential selected |
| Session artifact commit | `109ddfb` | `Build Session 4 provider seam` |

Provider boundary recorded during the session:

```text
Future application use case (Session 5)
                |
                v
         TextProvider protocol
          /               \
FakeTextProvider       future hosted adapter
          \               /
           ProviderResult
          or ProviderError
```

## 2026-09-30 — Session 5 FastAPI vertical slice

| Evidence | Link | State / result |
|---|---|---|
| Application use case | [`usecase.py`](../src/docs_action_agent/usecase.py) | Async provider orchestration remains independent of FastAPI and HTTP status codes |
| FastAPI transport | [`api.py`](../src/docs_action_agent/api.py) | Typed question route and liveness route call inward through the application boundary |
| Dependency injection | [`get_provider`](../src/docs_action_agent/api.py) | Deterministic fake is supplied behind `TextProvider`; tests replace it through FastAPI dependency overrides |
| API behavior tests | [`test_api.py`](../tests/test_api.py) | Success, four invalid payloads, provider timeout, unexpected exception, and health covered offline |
| Controlled failure response | [`test_timeout_questions_endpoint`](../tests/test_api.py) | `ProviderTimeout` becomes HTTP 504 with a stable message rather than leaking provider details |
| Unexpected failure response | [`test_unexpected_failure_provider`](../tests/test_api.py) | Runtime error becomes generic HTTP 500 and its internal message is absent from the response |
| Validation | [Status](STATUS.md#validation-state) | `20 passed in 0.18s`; locked sync and documentation checks passed; `git diff --check` passed |
| Live health check | [README command](../README.md#development-setup) | Uvicorn startup succeeded; `curl -fsS http://127.0.0.1:8000/health` returned `{"status":"ok"}` with HTTP 200 |
| Session artifact commit | `3f8f172` | `Build Session 5 FastAPI vertical slice` |

Request path explained and implemented during the session:

```text
HTTP client
  -> FastAPI route and QuestionRequest validation
  -> generate_question application use case
  -> injected TextProvider
  -> deterministic FakeTextProvider
  -> QuestionResponse serialized by FastAPI

Invalid input stops at validation (422).
ProviderTimeout crosses the application boundary and is mapped at HTTP (504).
Unexpected exceptions remain generic, non-leaky server failures (500).
```

## 2026-10-02 — Session 6 container and baseline assumptions

| Evidence | Link | State / result |
|---|---|---|
| Container definition | [`Dockerfile`](../Dockerfile) | Python 3.12 slim image; pinned uv executable; two-phase locked runtime sync; noninteractive Uvicorn startup |
| Build-context boundary | [`.dockerignore`](../.dockerignore) | Excludes `.env`, host `.venv`, Git history, tests, documentation, bytecode, and local caches |
| Baseline threat assumptions | [Threat model](THREAT_MODEL.md) | Separates untrusted input, untrusted model output, and credentials; records current controls and residual limitations |
| Concept explanation | [Threat model](THREAT_MODEL.md#baseline-assumptions) | Sasha explained runtime-only secrets and liveness limits, then corrected image composition, dependency-layer caching, bind versus probe addresses, and structure-versus-content trust |
| Image build | [`Dockerfile`](../Dockerfile) | `docker build -t docs-action-agent:dev .` passed; image ID began `a75ec1f3a2a9` |
| Container smoke check | [README container commands](../README.md#container-setup) | Temporary container started; `GET /health` returned `{"status":"ok"}`; Docker reported `running healthy`; container was stopped and removed |
| Resource substitution | [Sources](SOURCES.md#docker-and-uv-primary-documentation) | Inaccessible paid material replaced by exact free official Docker and uv sections |
| Session artifact commit | `0975698` | `Add Session 6 container baseline` |
| Daily score | — | 5/5: Recall, Build, Verify, Explain, and Record completed; planned 20 minutes, actual 2 hours |

Daily log:

```text
Date / planned time / actual time: 2026-10-02 / 20 minutes / 2 hours
Today's workstream and agent-architecture layer: Capstone / production-operation container and trust boundaries
Recall before notes: Partially correct image contents, runtime-secret rationale, and liveness limits; gaps in host environment exclusion and runtime configuration
Artifact or observation produced: Dockerfile, .dockerignore, baseline threat model, container README path, and free primary-source substitution
Verification and result: 20 offline tests passed; locked sync passed; image built; /health returned {"status":"ok"}; Docker reported running healthy; excluded paths absent from image
What I can now explain: Image versus container, build context, two-phase uv sync, runtime configuration, bind versus probe addresses, health limits, and typed structure versus trusted content
Failure, uncertainty, or limitation: Paid material was inaccessible; initial cached-build instructions omitted --no-install-project and the second sync; no maximum question length or production secret manager exists
Score (Recall / Build-observe / Verify / Explain / Record): 5 / 5
Actual hours this week / planned hours: 2 hours / 5 hours 30 minutes
Call-critical gates complete / remaining: 1 / 8
Estimated remaining hours / planned capacity remaining: 34 hours 45 minutes / 34 hours 45 minutes; reforecast Sunday
Next smallest step: Run the Session 7 Week 1 evidence gate and closed-notes whole-slice explanation
```

## 2026-10-03 — Restructured Session 7 agent/workflow design

| Evidence | Link | State / result |
|---|---|---|
| Agent-versus-workflow decision | [ADR-007](DECISIONS.md#adr-007--bounded-model-directed-tool-selection) | Model may select between two read-only tools; execution authority and safety controls remain deterministic |
| Explicit loop and budgets | [Bounded agent loop](AGENT_LOOP.md) | Three tool calls, four iterations, per-tool and provider timeouts, two-minute deadline, and one budget-counting transient retry recorded |
| Classification exercise | [Operation ownership](AGENT_LOOP.md#operation-ownership) | Validation, retrieval ranking, and approval classified as deterministic; tool selection and answer generation classified separately |
| Concept explanation | [Why the model selects tools](AGENT_LOOP.md#why-the-model-selects-tools) | Sasha identified avoided unnecessary calls as the benefit and nondeterminism, diagnostic complexity, and attack surface as costs |
| Schedule decision | [Readiness plan](OCTOBER_26_READINESS.md#calendar-and-completion-queue) | Repeated foundation review deferred into the October 10 explicit-loop gate; it was not marked complete |
| Documentation validation | [Status](STATUS.md#validation-state) | Required files and all 42 session-card fields present; learning-state check and `git diff --check` passed |

## 2026-10-05 — First read-only tool contract and implementation

| Evidence | Link | State / result |
|---|---|---|
| Typed tool boundary | [`tools.py`](../src/docs_action_agent/tools.py) | Arguments, results, hits, URLs, scores, output count, and stable errors are bounded and reject extra fields |
| Deterministic placeholder search | [`evidence_search`](../src/docs_action_agent/tools.py) | Three controlled records; token-overlap ranking; chunk-ID tie-breaker; zero-score filtering; no network, filesystem, model, or external write |
| Safe raw-argument boundary | [`execute_evidence_search`](../src/docs_action_agent/tools.py) | Invalid raw arguments return `invalid_arguments` without exposing the raw payload or Pydantic details |
| Focused behavior tests | [`test_tools.py`](../tests/test_tools.py) | 32 passed; covers validation, matching, ranking, limit, empty result, determinism, malicious text as data, and safe error mapping |
| Full regression suite | [Status](STATUS.md#validation-state) | 52 passed in 0.14 seconds |
| Failure caught during development | [`test_tools.py`](../tests/test_tools.py) | Existing tests initially passed while the uncalled search function crashed; added direct behavior tests and corrected dictionary-to-model construction |

Daily log:

```text
Date / planned time / actual time: 2026-10-05 / 2 hours 45 minutes combined / 3 hours
Today's workstream and agent-architecture layer: Capstone / typed tool contract, trust boundary, and deterministic retrieval placeholder
Recall before notes: No initial tool-contract baseline; learned schema bounds, inert data versus execution, application-owned errors, and output validation from the assigned Lesson 04/06 material and guided implementation
Artifact or observation produced: Typed evidence_search arguments/results/errors, controlled fixtures, deterministic search, raw-argument execution boundary, and focused tests
Verification and result: 32 focused tests passed; 52 full-suite tests passed; git diff --check passed
What I can now explain: Models propose calls but application code validates and authorizes them; malicious-looking text is safe here because it is treated as data by a read-only capability; tests only prove exercised paths
Failure, uncertainty, or limitation: Old tests passed while the uncalled search crashed; raw overlap also matched a common word, showing why this placeholder is not a measured retrieval implementation
Score (Recall / Build-observe / Verify / Explain / Record): 5 / 5
Actual hours this week / planned hours: 3 hours / 9 hours 45 minutes
Call-critical gates complete / remaining: 1 / 8; bounded tools and loop gate remains in progress
Estimated remaining hours / planned capacity remaining: Reforecast required after the second-tool/loop gate / 30 hours 45 minutes scheduled after October 5
Next smallest step: Implement source_lookup and an explicit two-tool allowlist; prove unknown tool names fail closed
```

## 2026-10-07 — Second read-only tool and executable allowlist

| Evidence | Link | State / result |
|---|---|---|
| Exact lookup contract | [`SourceLookupArguments` and `SourceLookupResult`](../src/docs_action_agent/tools.py) | One bounded chunk ID selects one bounded controlled record; extra fields are forbidden |
| Distinct tool responsibilities | [`evidence_search` and `source_lookup`](../src/docs_action_agent/tools.py) | Search returns ranked previews across records; lookup returns full content for one already-known ID |
| Safe raw-argument boundary | [`execute_source_lookup`](../src/docs_action_agent/tools.py) | Invalid raw arguments become non-retryable `invalid_arguments`; absent valid IDs become `not_found` |
| Executable allowlist | [`execute_tool`](../src/docs_action_agent/tools.py) | Exactly two registered executors; unknown `delete_repository` request returns `tool_not_allowed` without dynamic lookup |
| Focused behavior tests | [`test_tools.py`](../tests/test_tools.py) | 44 passed in 0.06 seconds, including allowed dispatch, invalid lookup arguments, deterministic lookup, exact registry names, and unknown-tool denial |
| Full regression suite | [Status](STATUS.md#validation-state) | 64 passed in 0.17 seconds; `git diff --check` passed |
| Failure caught during development | [`test_tools.py`](../tests/test_tools.py) | Tests caught dispatch through the stored name string instead of the stored executor and an invalid test that constructed a typed model before the raw boundary |

Daily log:

```text
Date / planned time / actual time: 2026-10-07 / 90 minutes / 2 hours
Today's workstream and agent-architecture layer: Capstone / bounded tool capabilities, validation, and deterministic authorization
Recall before notes: Correctly distinguished broad evidence discovery from exact source lookup; needed guidance on fixture provenance, exact lookup inputs, and unknown tool names
Artifact or observation produced: Typed source_lookup contract, bounded full fixture content, safe raw-argument executor, explicit two-tool registry, generic dispatcher, and denial tests
Verification and result: 44 focused tests passed; 64 full-suite tests passed; git diff --check passed
What I can now explain: Search returns small ranked previews; lookup retrieves one full controlled record by an ID produced by search; application-owned registry membership grants execution authority, not model output
Failure, uncertainty, or limitation: Three static hand-authored fixtures prove the boundary but not corpus coverage, realistic chunking, scaling, retrieval quality, or useful grounded answers
Score (Recall / Build-observe / Verify / Explain / Record): 5 / 5
Actual hours this week / planned hours: 5 hours / 9 hours 45 minutes
Call-critical gates complete / remaining: 1 / 8; bounded-tools portion complete and explicit-loop portion remains open
Estimated remaining hours / planned capacity remaining: Reforecast after the October 10 explicit-loop gate
Next smallest step: Complete the closed-notes recall checkpoint, then implement the capped explicit tool loop
```

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
