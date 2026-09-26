# Current Status

**Last updated:** 2026-09-25
**Sprint state:** Session 3 complete; typed request/response contract established
**Current week:** Week 1 — application foundations and vertical slice  
**Current session:** Session 3 — typed HTTP boundary complete
**Next scheduled session:** Session 4 — 2026-09-26, 3 hours

## Completed in Session 3

- Classified valid, missing, and malformed question payloads; corrected the distinction between redirect and client-error HTTP categories.
- Explained why validation belongs at the HTTP boundary: reject bad data early and prevent wasted or unsafe downstream work.
- Added Pydantic 2.13.5 as a locked runtime dependency.
- Defined provider-independent `QuestionRequest` and `QuestionResponse` models with an explicit `answered`/`abstained` status.
- Rejected missing, non-string, empty, whitespace-only, and unsupported-status input through model validation tests.
- Generated the request JSON Schema and confirmed that the question is required with a minimum length of one.
- Added the exact Pydantic and pytest sections needed after the implementation diagnostic exposed a resource gap.

## Blocked or pending decisions

- **Required before corpus ingestion:** confirm an immutable FastAPI tag/commit, bounded English-documentation path allowlist, exclusions, attribution, and source-URL rule by 2026-10-06, before Session 15.
- **Optional repository publication:** no GitHub repository or remote exists; decide public versus private before publication.
- Hosted model provider and model name can remain undecided until the Week 1 vertical slice; do not commit a credential.

## Next action

Begin the Session 4 card in `docs/SPRINT.md`. Sasha should explain the provider/application boundary and identify which tests need no network, then define the smallest provider protocol and deterministic fake before considering one hosted adapter or live call.

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
| Corpus candidate decision | Passing provisionally | ADR-006; exact pin/path due by 2026-10-06 |
| Python requirement and selected interpreter | Passing | `requires-python = ">=3.12"`; `uv run python --version` returned Python 3.12.14 |
| Locked environment resolution | Passing | `uv sync --locked` resolved 12 package records and checked 11 packages on 2026-09-25 |
| Package import and pytest discovery | Passing | `uv run pytest -q` returned `8 passed in 0.03s` |
| Application behavior | Passing for current scope | Typed validation and serialization only; routes and provider behavior remain intentionally absent |
| Live provider call | Not run | Deliberately excluded from bootstrap |

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
