# Current Status

**Last updated:** 2026-10-07
**Sprint state:** Two bounded read-only tools and executable allowlist complete; explicit loop pending
**Current sprint gate:** Week 2 — bounded tool use and explicit agent loop
**Current session:** Second read-only `source_lookup` tool and executable allowlist complete
**Next planned session:** Recall checkpoint, then Session 11 explicit tool loop

**October 26 scheduling overlay:** The local [Stephen Anthony readiness plan](OCTOBER_26_READINESS.md) now governs call-critical sequencing, weekly capacity, catch-up decisions, and the protected October 22–25 review window. Sasha may say `Start the next session` to advance the agent-architecture capstone track; FDE and Riser are separate self-directed tracks. Available time is optional unless it differs from the current card or calendar timebox.

## Completed in the second read-only tool and allowlist session

- Added a strict, bounded `source_lookup` contract that returns full controlled content for one known chunk ID and a non-retryable `not_found` error for an absent ID.
- Kept broad discovery and exact retrieval distinct: `evidence_search` returns bounded ranked previews, while `source_lookup` returns one full controlled record.
- Added a raw-argument lookup boundary and an executable registry containing exactly `evidence_search` and `source_lookup`.
- Proved both approved tools execute through the registry, invalid raw arguments fail safely, and the unknown `delete_repository` tool name returns `tool_not_allowed` without dispatch.
- Identified the fixture limitation: three static, hand-authored records prove contracts and denial behavior but not corpus coverage, realistic chunk quality, scaling, or answer usefulness.
- Recorded two hours actual time and a 5/5 daily score.

## Blocked or pending decisions

- **Required before corpus ingestion and now overdue:** confirm an immutable FastAPI tag/commit, bounded English-documentation path allowlist, exclusions, attribution, and source-URL rule before the October 11 corpus-contract block.
- **Optional repository publication:** no GitHub repository or remote exists; decide public versus private before publication.
- Hosted model provider and model name remain unselected; choose them only before a scheduled hosted-adapter or evaluation requirement, and provide credentials at runtime rather than committing them.

## Next action

Run the 30-minute closed-notes recall checkpoint for tools, tokens/context, loops, validation, and deterministic boundaries. Then begin Session 11's explicit capped tool loop without adding tools or corpus ingestion.

## Validation state

| Check | State | Evidence |
|---|---|---|
| Required planning files exist | Passing | Bootstrap validation on 2026-09-22 |
| 42 scheduled dates from Sep 23 through Nov 3 are represented | Passing | Bootstrap validation on 2026-09-22 |
| Every session card contains all required fields | Passing | Bootstrap validation on 2026-09-22 |
| Candidate count is no more than three; one pending default exists | Passing | `docs/SPEC.md`, ADR-003 |
| Planning documents agree on dates, scope, defaults, and gates | Passing | Manual cross-check on 2026-09-22 |
| Session 1 learning matrix exists and contains required states | Passing | `test -f docs/LEARNING_MATRIX.md`; state grep passed on 2026-09-23 |
| Local Git repository | Passing | Initialized on `main` on 2026-09-23 |
| Session 1 artifact commit | Passing | `409ec75` |
| Session 2 artifact commit | Passing | `03239ae` |
| Session 3 typed model contract | Passing | Request/result models contain no provider-specific or retrieval fields |
| Session 3 model validation | Passing | Seven focused model tests cover valid, missing, malformed, blank, serialization, and status cases |
| Session 3 JSON Schema | Passing | `QuestionRequest` requires a string with `minLength: 1` |
| Session 3 artifact commit | Passing | `da1119e` |
| Session 4 provider boundary | Passing | Async application-owned protocol returns typed output or raises controlled application-owned errors |
| Session 4 deterministic fake | Passing | Success and timeout paths covered without network access |
| Session 4 environment settings | Passing | Required values load explicitly from the environment; `SecretStr` protects display and missing configuration fails fast |
| Session 4 secret hygiene | Passing | `.env` ignored; `.env.example` contains empty placeholders; broad scan reviewed with only documented false positives and no credential value |
| Session 4 artifact commit | Passing | `109ddfb` |
| Session 5 request path | Passing | FastAPI transport calls an application use case, which awaits an injected application-owned provider protocol |
| Session 5 HTTP validation | Passing | Missing, empty, whitespace-only, and non-string questions return `422` before provider execution |
| Session 5 failure mapping | Passing | Provider timeout returns stable `504`; unexpected exception returns generic `500` without its internal message |
| Session 5 offline API tests | Passing | Health, success, validation, controlled failure, and unexpected failure covered without network or paid provider calls |
| Session 5 live health check | Passing | Uvicorn started on `127.0.0.1:8000`; `curl -fsS http://127.0.0.1:8000/health` returned `{"status":"ok"}` with HTTP 200 |
| Session 5 artifact commit | Passing | `3f8f172` |
| Session 6 container build | Passing | `docker build -t docs-action-agent:dev .`; image ID began `a75ec1f3a2a9` |
| Session 6 container liveness | Passing | `/health` returned `{"status":"ok"}` and Docker reported `running healthy` |
| Session 6 build-context secret boundary | Passing | `.env`, host `.venv`, and Git history excluded; image uses explicit `COPY` instructions |
| Session 6 threat baseline | Passing | `docs/THREAT_MODEL.md` distinguishes untrusted input, model output, and credentials with current controls and residual limitations |
| Session 6 artifact commit | Passing | `0975698` |
| Session 6 actual time / daily score | Passing | Planned 20 minutes; actual 2 hours; 5/5 |
| Restructured Session 7 classification | Passing | Deterministic behavior, model generation, and model-selected tool behavior classified and defended |
| Restructured Session 7 loop design | Passing | Allowed tools, budgets, timeouts, retry policy, successful terminal states, and fail-closed states are explicit in `docs/AGENT_LOOP.md` |
| Restructured Session 7 decision record | Passing | ADR-007 contains context, options, decision, consequences, and revisit conditions |
| Restructured Session 7 documentation validation | Passing | Required files and all 42 session-card fields present; learning-state check and `git diff --check` passed on 2026-10-03 |
| First tool argument/result contract | Passing | Strict Pydantic models bound query, result count, identifiers, source metadata, excerpts, scores, and extra fields |
| First tool deterministic behavior | Passing | Fixture-backed `evidence_search` ranks by token overlap and chunk ID, filters zero-score records, and performs no external I/O |
| First tool safe error boundary | Passing | Raw invalid arguments return a bounded application-owned `ToolError` without raw payload or Pydantic detail |
| First tool focused tests | Passing | `uv run pytest -q tests/test_tools.py` returned `32 passed in 0.05s` on 2026-10-05 |
| First tool full regression suite | Passing | `uv run pytest -q` returned `52 passed in 0.14s` on 2026-10-05 |
| First tool actual time / daily score | Passing | Planned combined time 2 hours 45 minutes; actual 3 hours; 5/5 |
| Second tool argument/result contract | Passing | Strict `chunk_id` input and bounded full-record output reject extra fields; absent IDs return non-retryable `not_found` |
| Exact lookup behavior | Passing | `source_lookup` deterministically returns one controlled record and performs no external I/O |
| Executable two-tool allowlist | Passing | Registry exposes exactly `evidence_search` and `source_lookup`; dispatch uses stored executors rather than dynamic name lookup |
| Unknown-tool denial | Passing | `delete_repository` returns non-retryable `tool_not_allowed` before any capability executes |
| Second tool focused tests | Passing | `uv run pytest -q tests/test_tools.py` returned `44 passed in 0.06s` on 2026-10-07 |
| Second tool full regression suite | Passing | `uv run pytest -q` returned `64 passed in 0.17s` on 2026-10-07 |
| Second tool actual time / daily score | Passing | Planned 90 minutes; actual 2 hours; 5/5 |
| Corpus candidate decision | Passing provisionally | ADR-006; exact pin/path due by 2026-10-06 |
| Python requirement and selected interpreter | Passing | `requires-python = ">=3.12"`; `uv run python --version` returned Python 3.12.14 |
| Locked environment resolution | Passing | `uv sync --locked` completed against the lockfile on 2026-10-02 |
| Package import and pytest discovery | Passing | `uv run pytest -q` returned `20 passed in 0.18s` on 2026-10-02 |
| Application behavior | Passing for current scope | Typed `/questions` vertical slice and `/health` liveness route work with a deterministic injected fake |
| Live provider call | Deferred | Optional in Session 4; no provider/model or credential selected, and ordinary tests remain offline |

## Current validation commands

Run the project checks followed by the documentation checks:

```bash
uv sync --locked
uv run python --version
uv run pytest -q
# In one terminal:
uv run uvicorn docs_action_agent.api:app --host 127.0.0.1 --port 8000
# In another terminal:
curl -fsS http://127.0.0.1:8000/health
test -f AGENTS.md && test -f README.md
for file in SPEC SPRINT STATUS DECISIONS EVIDENCE SOURCES; do test -f "docs/${file}.md"; done
test "$(grep -c '^### Session [0-9]' docs/SPRINT.md)" -eq 42
test "$(grep -c '^\*\*Date / duration:\*\*' docs/SPRINT.md)" -eq 42
for field in 'Objective' 'Concepts first' 'Diagnostic / skip' 'Resources' 'Sasha attempts' 'Outcome / files' 'Acceptance' 'Validation' 'Evidence' 'Non-goals' 'Next smallest step'; do test "$(grep -c "^\\*\\*${field}:\\*\\*" docs/SPRINT.md)" -eq 42; done
test -f docs/LEARNING_MATRIX.md
grep -q 'Explain\|Build\|Operate\|Defer' docs/LEARNING_MATRIX.md
git status --short --branch
```
