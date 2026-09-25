# Docs-to-Action Reliability Agent

A six-week AI-engineering learning and portfolio sprint running from **September 23 through November 3, 2026**.

The capstone will become a domain-neutral, production-minded workflow over one approved open-source documentation corpus. It will answer technical questions with verifiable citations, abstain when evidence is insufficient, use narrowly bounded tools, and place a draft-producing action behind explicit human approval. The primary output is engineering evidence: tests, evaluations, security controls, operational behavior, decisions, and clear explanations.

## Current status

Session 2 is complete. The repository now has a reproducible Python 3.12 project, an importable `src/` package, and a passing pytest smoke test. FastAPI English documentation remains provisionally selected pending an immutable version pin and bounded path allowlist.

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
- [Current status](docs/STATUS.md)
- [Architecture decisions](docs/DECISIONS.md)
- [Evidence ledger](docs/EVIDENCE.md)
- [Learning sources](docs/SOURCES.md)
- [Repository working agreement](AGENTS.md)

## Scope at a glance

One corpus, one index, one workflow, two read-only tools, one approval-gated draft tool, and no external writes. Kubernetes, fine-tuning, elaborate UI work, multi-agent orchestration, LangChain, MCP, and Pinecone are outside the default six-week scope.

The application behavior will be added incrementally during Week 1. The current harness intentionally tests only package import and test discovery.

## Development setup

```bash
uv sync --locked
uv run python --version
uv run pytest -q
```

`uv sync --locked` synchronizes the project environment from the existing lockfile and fails if the lockfile is outdated. `uv run python --version` confirms the Python version selected for the project environment. `uv run pytest -q` runs the test suite inside that environment with concise output.
