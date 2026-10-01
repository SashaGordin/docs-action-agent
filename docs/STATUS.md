# Current Status

**Last updated:** 2026-09-30
**Sprint state:** Session 4 complete; provider seam, deterministic fake, and environment settings established
**Current sprint gate:** Week 1 — application foundations and vertical slice
**Current session:** Session 4 — provider seam and structured generation complete
**Next planned session:** Session 5 — FastAPI vertical slice (originally scheduled 2026-09-27, 90 minutes)

## Completed in Session 4

- Explained the provider-adapter/application boundary, why application-owned failures cross it, and why usage metadata is distinct from user telemetry.
- Defined an application-owned async `TextProvider` protocol with typed `ProviderResult` and token-usage models.
- Added application-owned `ProviderError` and `ProviderTimeout` exceptions so provider-specific failures cannot leak inward.
- Implemented a deterministic `FakeTextProvider` that returns a configured result or raises a configured controlled error without network access.
- Added environment-based typed settings using `SecretStr`, committed placeholder names in `.env.example`, and ignored the real `.env` file.
- Added offline success, timeout, configured-settings, and missing-settings tests; the full suite passes with 12 tests.
- Deferred the optional hosted adapter and live call because no provider/model or credential has been selected; no acceptance criterion depends on them.

## Blocked or pending decisions

- **Required before corpus ingestion:** confirm an immutable FastAPI tag/commit, bounded English-documentation path allowlist, exclusions, attribution, and source-URL rule by 2026-10-06, before Session 15.
- **Optional repository publication:** no GitHub repository or remote exists; decide public versus private before publication.
- Hosted model provider and model name can remain undecided until the Week 1 vertical slice; do not commit a credential.

## Next action

Begin the Session 5 card in `docs/SPRINT.md`. Sasha should trace the request lifecycle and classify validation, provider-timeout, and unexpected failures before implementing the FastAPI route and application use case against `TextProvider`.

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
| Corpus candidate decision | Passing provisionally | ADR-006; exact pin/path due by 2026-10-06 |
| Python requirement and selected interpreter | Passing | `requires-python = ">=3.12"`; `uv run python --version` returned Python 3.12.14 |
| Locked environment resolution | Passing | `uv sync --locked` resolved 12 package records and checked 11 packages on 2026-09-30 |
| Package import and pytest discovery | Passing | `uv run pytest -q` returned `12 passed in 0.05s` |
| Application behavior | Passing for current scope | Typed HTTP models and provider seam exist; routes and the application use case remain intentionally absent until Session 5 |
| Live provider call | Deferred | Optional in Session 4; no provider/model or credential selected, and ordinary tests remain offline |

## Current validation commands

Run the project checks followed by the documentation checks:

```bash
uv sync --locked
uv run python --version
uv run pytest -q
test -f AGENTS.md && test -f README.md
for file in SPEC SPRINT STATUS DECISIONS EVIDENCE SOURCES; do test -f "docs/${file}.md"; done
test "$(grep -c '^### Session [0-9]' docs/SPRINT.md)" -eq 42
test "$(grep -c '^\*\*Date / duration:\*\*' docs/SPRINT.md)" -eq 42
for field in 'Objective' 'Concepts first' 'Diagnostic / skip' 'Resources' 'Sasha attempts' 'Outcome / files' 'Acceptance' 'Validation' 'Evidence' 'Non-goals' 'Next smallest step'; do test "$(grep -c "^\\*\\*${field}:\\*\\*" docs/SPRINT.md)" -eq 42; done
test -f docs/LEARNING_MATRIX.md
grep -q 'Explain\|Build\|Operate\|Defer' docs/LEARNING_MATRIX.md
git status --short --branch
```
