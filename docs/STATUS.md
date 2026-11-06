# Current Status

**Last updated:** 2026-11-04
**Sprint state:** Bounded loop and pinned corpus contract complete; deterministic ingestion and evaluation seed next
**Current sprint gate:** Week 3 — parse the controlled corpus deterministically and version the first evaluation cases
**Current session:** Session 15 corpus manifest and ingestion contract complete
**Next planned session:** Combine Sessions 16–17 for deterministic parsing/normalization and evaluation-set v0.1

**Scheduling note:** The October 26 readiness overlay is now historical. The project continues evidence-first from the next incomplete capstone gate; original dates do not override failed or unfinished acceptance criteria.

## Completed in the corpus-contract session

- Pinned FastAPI release `0.162.0` to immutable commit `7a0a3f0b286c6c865cf4398ea0e957a87b8bffa4`.
- Bounded the initial corpus to five foundational English tutorial pages with exact paths, byte sizes, SHA-256 hashes, and commit-pinned citation URLs.
- Preserved MIT attribution and the upstream license text under `corpus/`.
- Implemented strict manifest, license, and file models; default-deny path checks; explicit exclusions; traversal rejection; deterministic logical and snapshot-version IDs; source URLs; and byte/hash verification.
- Added a synthetic checked-in Markdown fixture and manifest so all unit tests run without network access.
- Verified 18 focused corpus scenarios and 98 total tests.
- Caught and corrected false-green tests whose unrelated extra field caused the expected validation error before the intended commit/path rules were exercised.
- Daily score: 5/5. Actual active time was approximately 1.5–2 hours.

## Blocked or pending decisions

- Hosted model provider and model name remain unselected; choose them only before a scheduled hosted-adapter or evaluation requirement, and provide credentials at runtime rather than committing them.
- The five-page corpus is intentionally narrow. Expand it only after the first evaluation set exposes a measured coverage gap.

## Next action

Parse and normalize the checked-in fixture deterministically, preserve headings/code/source metadata, prove repeat ingestion is idempotent, and create evaluation-set v0.1 with answerable, misleading, and unanswerable cases.

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
| Explicit loop public seam | Passing | `run_agent` accepts an application-owned provider and tool executor and returns typed terminal outcomes |
| Explicit loop budgets and timeouts | Passing | Three tool calls, four iterations, five-second tool, 45-second model, and 120-second overall defaults are typed and tested |
| Explicit loop fail-closed behavior | Passing | Repeats, unknown tools, second malformed request, invalid trusted result, exhausted budgets, and timeouts terminate predictably |
| Explicit loop terminal schemas | Passing | Final answer and abstention are typed, whitespace-stripped, nonblank, and bounded |
| Explicit loop focused scenarios | Passing | `uv run pytest -q tests/test_agent_loop.py` returned 16 passed in 0.06s on 2026-10-16 |
| Session 11 full regression suite | Passing | `uv run pytest -q` returned 80 passed in 0.19s on 2026-10-16 |
| Session 11 live health check | Passing | Uvicorn returned `{"status":"ok"}` with HTTP 200 on `127.0.0.1:8000` |
| Session 11 container gate | Passing | Image `docs-action-agent:session11` built; offline-network container reached Docker `healthy` after entrypoint correction |
| Session 11 actual time / daily score | Passing | Planned 3 hours; approximately 5.5 hours actual; 5/5 |
| Corpus revision and scope | Passing | FastAPI `0.162.0`; commit `7a0a3f0b286c6c865cf4398ea0e957a87b8bffa4`; five exact English tutorial paths in the production manifest |
| Corpus attribution and durable URLs | Passing | MIT notice preserved; source URLs render the immutable commit and repository-relative path |
| Corpus schema and path policy | Passing | Strict models reject extra fields, malformed hashes/commits, out-of-scope paths, explicit exclusions, and traversal |
| Corpus deterministic identities | Passing | Logical IDs remain stable across source revisions; snapshot-version IDs change with commit or content hash |
| Corpus offline fixture verification | Passing | Checked-in fixture byte size and SHA-256 match its fixture manifest; changed bytes fail verification |
| Session 15 focused tests | Passing | `uv run pytest -q tests/test_corpus.py` returned 18 passed in 0.05 seconds on 2026-11-04 |
| Session 15 full regression suite | Passing | `uv run pytest -q` returned 98 passed in 0.19 seconds on 2026-11-04 |
| Session 15 actual time / daily score | Passing | Planned 90 minutes; approximately 1.5–2 hours actual; daily rubric 5/5 |
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
