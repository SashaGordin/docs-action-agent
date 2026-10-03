# Current Status

**Last updated:** 2026-09-30
**Sprint state:** Session 5 complete; offline FastAPI vertical slice and failure mapping established
**Current sprint gate:** Week 1 — application foundations and vertical slice
**Current session:** Session 5 — FastAPI vertical slice complete
**Next planned session:** Session 6 — container and baseline assumptions (originally scheduled 2026-09-28, 20 minutes)

**October 26 scheduling overlay:** The local [Stephen Anthony readiness plan](OCTOBER_26_READINESS.md) now governs call-critical sequencing, weekly capacity, catch-up decisions, and the protected October 22–25 review window. Sasha may say `Start the next session` to advance the agent-architecture capstone track; FDE and Riser are separate self-directed tracks. Available time is optional unless it differs from the current card or calendar timebox.

## Completed in Session 5

- Corrected the request direction from HTTP transport into the application use case and provider boundary; distinguished liveness from readiness.
- Added an async `generate_question` use case with no FastAPI or HTTP dependencies.
- Added `GET /health` and typed `POST /questions` routes with `TextProvider` supplied through FastAPI dependency injection.
- Mapped the controlled `ProviderTimeout` failure to a stable, non-leaky `504` response while leaving unexpected failures to the framework's generic `500` handling.
- Added offline ASGI tests for health, successful generation, missing/malformed/blank inputs, provider timeout, and non-leaky unexpected exceptions.
- Replaced the deprecated test-client dependency path with the installed Starlette version's supported `httpx2` test transport.
- Verified the complete suite with 20 passing tests and confirmed the live `/health` response through Uvicorn and `curl`.

## Blocked or pending decisions

- **Required before corpus ingestion:** confirm an immutable FastAPI tag/commit, bounded English-documentation path allowlist, exclusions, attribution, and source-URL rule by 2026-10-06, before Session 15.
- **Optional repository publication:** no GitHub repository or remote exists; decide public versus private before publication.
- Hosted model provider and model name remain unselected; choose them only before a scheduled hosted-adapter or evaluation requirement, and provide credentials at runtime rather than committing them.

## Next action

Begin the Session 6 card in `docs/SPRINT.md`. Sasha should explain which files enter a container image, which configuration values arrive only at runtime, and why `.env` must not enter the build context before drafting the minimal container and baseline threat assumptions.

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
| Corpus candidate decision | Passing provisionally | ADR-006; exact pin/path due by 2026-10-06 |
| Python requirement and selected interpreter | Passing | `requires-python = ">=3.12"`; `uv run python --version` returned Python 3.12.14 |
| Locked environment resolution | Passing | `uv sync --locked` completed against the Session 5 lockfile on 2026-09-30 |
| Package import and pytest discovery | Passing | `uv run pytest -q` returned `20 passed in 0.18s` |
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
