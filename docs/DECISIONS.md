# Architecture Decision Log

ADRs are append-only. A changed decision receives a new record that supersedes the old one.

## ADR-001 — Initial application stack

- **Status:** Accepted for the sprint
- **Date:** 2026-09-22
- **Context:** The project needs a compact, explainable, typed Python service with reproducible dependencies, tests, and a container path. The supplied learning plan assumes Python 3.12+ and FastAPI.
- **Options:** Python/FastAPI with uv; Python with another API framework/package manager; Node/TypeScript; framework-first agent stack.
- **Decision:** Use Python 3.12+, uv, FastAPI, Pydantic models, pytest, and Docker. Keep framework use at the HTTP and validation boundary; implement the central workflow explicitly.
- **Consequences:** Strong alignment with learning resources and typed API work; one additional tool (`uv`) to learn; application scaffolding must wait for Session 1 rather than bootstrap.
- **Revisit when:** A documented environment limitation prevents Python 3.12, uv, FastAPI, or Docker, or a measured requirement cannot be met.

## ADR-002 — Model provider boundary

- **Status:** Accepted direction; concrete provider pending
- **Date:** 2026-09-22
- **Context:** The sprint needs early hosted-model progress without coupling domain logic to one SDK, plus a later local endpoint experiment.
- **Options:** Direct vendor calls throughout; one minimal provider protocol with adapters; adopt a broad orchestration framework.
- **Decision:** Define a small application-owned provider interface around the exact structured-generation/tool behavior needed. Implement one hosted adapter first. A later OpenAI-compatible local adapter must use the same interface.
- **Consequences:** Tests can use a fake; provider-specific features stay at an edge; the interface must not speculate beyond observed requirements.
- **Revisit when:** The second adapter exposes a proven incompatibility or evaluation shows the abstraction hides required usage/trace data.

## ADR-003 — Public documentation corpus

- **Status:** Pending Sasha approval
- **Date:** 2026-09-22
- **Context:** The project needs one stable, substantive, legally safe, reasonably sized corpus with verifiable citations.
- **Options:** FastAPI English docs; pytest authored docs; uv docs. Criteria and trade-offs are in `docs/SPEC.md`.
- **Decision:** Recommend **FastAPI English documentation**, pinned to an approved tag/commit and a bounded path allowlist. Do not ingest it until Sasha approves. pytest and uv are the only current alternatives.
- **Consequences:** The corpus is relevant to the project and rich in procedures; questions can test citations and version sensitivity. Scope must exclude translations, generated reference noise, and unrelated repository content. Preserve MIT attribution.
- **Revisit when:** The bounded FastAPI subset is too large/small, licensing/source links cannot be preserved, or initial evaluation questions lack useful ambiguity and abstention cases.

## ADR-004 — Single explicit workflow and tool boundary

- **Status:** Accepted for the sprint
- **Date:** 2026-09-22
- **Context:** Learning value and safety require visible control flow. A multi-agent or framework abstraction would add breadth before the core behavior is measured.
- **Options:** Deterministic pipeline only; one bounded model-directed workflow; multi-agent framework.
- **Decision:** Use one explicit workflow. Allow exactly two read-only tools (planned: evidence search and source/chunk lookup) and one draft-producing tool. Authorization and approval remain deterministic application checks. The draft tool performs no external write.
- **Consequences:** The design is easier to test and explain. It will not demonstrate distributed agents or arbitrary plugins, by design.
- **Revisit when:** The completed evaluation demonstrates a concrete task that cannot be expressed safely with this boundary; revisit after November 3 by default.

## ADR-005 — Retrieval choice follows a measured baseline

- **Status:** Accepted direction; storage implementation pending Week 3
- **Date:** 2026-09-22
- **Context:** Choosing a vector database before corpus/evaluation evidence would be tool-led design.
- **Options:** Keyword only; vector only; hybrid; managed vector service.
- **Decision:** Build a keyword/BM25-like baseline first, create a fixed evaluation set, then compare exactly one vector or hybrid alternative using one local store. Record the winner and costs in a later ADR.
- **Consequences:** Week 3 includes comparison work and delays a final store selection. Pinecone and multiple databases remain out of scope.
- **Revisit when:** Corpus characteristics or measured retrieval results justify a different approach.

## ADR-006 — Provisional FastAPI English documentation corpus

- **Status:** Provisionally accepted; pin and bounded path allowlist pending
- **Date:** 2026-09-23
- **Supersedes:** ADR-003's pending-approval status; retains its criteria and alternatives
- **Context:** Sasha approved FastAPI English documentation as the provisional corpus for Session 1, subject to confirming an immutable upstream tag or commit and a bounded path allowlist before ingestion.
- **Decision:** Select the English documentation in `fastapi/fastapi` as the provisional single corpus. Do not ingest or treat the corpus as fully approved until its exact tag/commit, included paths, exclusions, attribution, and durable source-URL rule have been reviewed and recorded.
- **Consequences:** Corpus selection is no longer an open candidate choice, but corpus pinning remains a dated blocker. Translations, generated reference noise, unrelated repository content, and user-generated issue content remain out of scope.
- **Revisit when:** The proposed pin or bounded subset fails the criteria in `docs/SPEC.md`, is impractical to evaluate locally, or cannot preserve MIT attribution and durable citations.
