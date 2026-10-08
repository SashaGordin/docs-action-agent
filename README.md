# Docs-to-Action Reliability Agent

A six-week AI-engineering learning and portfolio sprint running from **September 23 through November 3, 2026**.

The capstone will become a domain-neutral, production-minded workflow over one approved open-source documentation corpus. It will answer technical questions with verifiable citations, abstain when evidence is insufficient, use narrowly bounded tools, and place a draft-producing action behind explicit human approval. The primary output is engineering evidence: tests, evaluations, security controls, operational behavior, decisions, and clear explanations.

## Current status

The foundation through Session 6 is complete: the repository has a typed FastAPI vertical slice, deterministic provider fake, offline failure tests, and a verified container health path. The bounded agent-loop design, both read-only tools, and the executable two-tool allowlist are implemented and tested; the recall checkpoint and explicit capped loop are next. FastAPI English documentation remains provisionally selected pending an immutable version pin and bounded path allowlist.

The workspace is a local Git repository on `main`. No GitHub repository or remote has been created.

## Proposed system boundary

```text
versioned public docs -> deterministic ingestion -> one searchable index
                                                    |
client -> FastAPI -> explicit workflow -> retrieval + structured lookup
                    |               |
                    |               -> cited, typed answer or abstention
                    -> approved draft tool (no external write)

cross-cutting: typed validation, authorization, audit events, tests,
evaluation set, structured telemetry, configuration, Docker, runbook
```

The hosted model sits behind a small provider interface. An OpenAI-compatible local adapter may be evaluated later without changing domain or tool contracts.

## Project documents

- [Product specification](docs/SPEC.md)
- [Daily six-week sprint](docs/SPRINT.md)
- [October 26 readiness and session queue](docs/OCTOBER_26_READINESS.md)
- [Current status](docs/STATUS.md)
- [Architecture decisions](docs/DECISIONS.md)
- [Bounded agent-loop design](docs/AGENT_LOOP.md)
- [Evidence ledger](docs/EVIDENCE.md)
- [Learning sources](docs/SOURCES.md)
- [Repository working agreement](AGENTS.md)

## Scope at a glance

One corpus, one index, one workflow, two read-only tools, one approval-gated draft tool, and no external writes. Kubernetes, fine-tuning, elaborate UI work, multi-agent orchestration, LangChain, MCP, and Pinecone are outside the default six-week scope.

The current application exposes `GET /health` and `POST /questions`. The question route still uses a deterministic fake provider. Fixture-backed `evidence_search` and `source_lookup` tools exist behind typed execution boundaries and an explicit allowlist but are not yet connected to the question route; no hosted provider call or external write occurs.

## Development setup

```bash
uv sync --locked
uv run python --version
uv run pytest -q
```

`uv sync --locked` synchronizes the project environment from the existing lockfile and fails if the lockfile is outdated. `uv run python --version` confirms the Python version selected for the project environment. `uv run pytest -q` runs the test suite inside that environment with concise output.

Run the development API with:

```bash
uv run uvicorn docs_action_agent.api:app --host 127.0.0.1 --port 8000
```

In another terminal, verify liveness with:

```bash
curl -fsS http://127.0.0.1:8000/health
```

## Container setup

Build the local development image from the locked runtime dependencies:

```bash
docker build -t docs-action-agent:dev .
```

Start it on local port 8000:

```bash
docker run --rm --name docs-action-agent -p 8000:8000 docs-action-agent:dev
```

In another terminal, run the same `/health` command above. The endpoint and Docker
health check prove HTTP liveness only; they do not prove provider or workflow
readiness. The current fake-provider application requires no runtime credential.
