# Product and Learning Specification

## Goal

Build and be able to defend a domain-neutral Docs-to-Action Reliability Agent over public documentation from one open-source project. The repository must demonstrate transferable, production-minded AI engineering through working software and measured evidence rather than course completion.

## Users

- **Primary learner/operator:** Sasha, who must understand and explain every important boundary and trade-off.
- **Technical evaluator:** an engineer or interviewer assessing implementation, evaluation, security, and operational judgment.
- **Demo user:** a developer asking factual questions about the selected project and requesting a bounded draft artifact.
- **Stakeholder reviewer:** a practitioner testing task fit with public, non-sensitive material.

## Core user outcomes

1. Ask a technical question and receive a typed answer with supporting citations.
2. Receive an explicit `insufficient_evidence` result when the corpus cannot support an answer.
3. Use two narrow read-only tools through validated contracts.
4. Request one draft artifact, review the proposed action, and explicitly approve or deny draft production.
5. Inspect enough telemetry and evaluation evidence to understand quality, latency, usage/cost, tool behavior, and failures.

## Required capabilities

1. Reproducibly ingest and version public Markdown or HTML documentation.
2. Store chunks in one searchable index with source URL/path, heading, corpus version, and stable chunk ID.
3. Prevent silent duplication during re-ingestion.
4. Establish a keyword baseline, then compare it with one vector or hybrid configuration.
5. Return typed results containing status, answer, citations, and relevant operational metadata.
6. Check citation support and abstain on insufficient, irrelevant, or conflicting evidence.
7. Expose exactly two read-only tools and at most one draft-producing tool.
8. Enforce allowlists, typed arguments, timeouts, step limits, identity/role checks, and explicit approval in deterministic code.
9. Version an evaluation set containing answerable, unanswerable, misleading, malformed, unauthorized, and adversarial cases.
10. Measure retrieval quality, citation support, latency, model usage/cost, tool calls, and failures.
11. Test prompt injection, malicious document content/source poisoning, unauthorized tool use, malformed arguments, repeated requests, tool failure, denied approval, and approval bypass.
12. Run locally through documented commands and Docker, with health checks and a runbook.
13. Use a hosted model first behind a provider interface that can later accept an OpenAI-compatible local adapter.

## Quality attributes

- **Grounded:** factual claims trace to retrieved corpus evidence.
- **Safe by construction:** authorization and approval are code boundaries, not prompt requests.
- **Observable:** a failure can be localized across request, retrieval, model, and tool stages.
- **Reproducible:** results identify code, corpus, evaluation-set, and model configuration versions.
- **Understandable:** important control flow remains explicit and explainable by Sasha.
- **Operable:** setup, reset, health, failure, and recovery paths are documented.

## Constraints

- Python 3.12+, FastAPI, Pydantic, pytest, uv, Docker.
- One public corpus; one vector store or searchable persistence implementation.
- One agent/workflow; no more than three tools total.
- Hosted model first; paid calls are excluded from ordinary unit tests.
- Credentials only through environment configuration; provide `.env.example` and never commit `.env`.
- Tests use mocks or controlled fixtures whenever a live model is not the subject under evaluation.
- Evaluation, security, tests, and documentation take priority over optional feature breadth.

## Non-goals

- Casino-specific workflows or private company data.
- Autonomous external writes or issue creation.
- Multi-agent orchestration, general-purpose planning, computer use, or browser automation.
- Fine-tuning, model training, multimodal features, or provider benchmarking across many models.
- Multiple corpora, multiple vector stores, a tool marketplace, or a general integration platform.
- Kubernetes, Terraform, Ansible, broad cloud-platform study, or production-scale multi-tenancy implementation.
- Elaborate frontend, mobile app, or visual polish.
- LangChain, MCP, Pinecone, or another framework absent an approved requirement-driven ADR.

## Corpus selection

### Criteria

The selected corpus must be:

- maintained and versionable from a stable first-party repository;
- technically substantive enough for factual and procedural questions;
- licensed for safe use in a public demonstration, with attribution preserved;
- available primarily as Markdown or clean HTML with durable source links;
- small enough to ingest and evaluate locally during the sprint;
- structured by headings and suitable for exact, verifiable citations;
- free of sensitive data and not dependent on user-generated issue content.

### Candidates (maximum three)

| Candidate | Fit | Risk/limit | Decision |
|---|---|---|---|
| FastAPI English documentation from `fastapi/fastapi` | Mature, MIT-licensed, Markdown in the source repository, rich procedural/API questions, and directly relevant to the capstone stack | Full docs are larger than needed; freeze a bounded section allowlist and commit/tag | **Recommended default; pending Sasha approval** |
| pytest documentation from `pytest-dev/pytest` | Mature, MIT-licensed, strong how-to/reference structure and precise expected answers | Some API reference is generated; select authored guides first | Alternative |
| uv documentation from `astral-sh/uv` | Markdown-first, versioned, technically rich, dual MIT/Apache-2.0 project | Rapid product evolution can make answers version-sensitive; corpus must pin a release/commit | Alternative |

Approval must select one candidate plus a pinned tag or commit and bounded path allowlist. Preserve the upstream license/attribution and source URLs in generated metadata.

## Final deliverables

- Runnable FastAPI service and deterministic ingestion/indexing commands.
- Typed provider, workflow, retrieval, tool, approval, and response boundaries.
- Automated unit, integration, security, and evaluation tests.
- Versioned corpus manifest and 15–20+ case evaluation set.
- Evaluation report with retrieval, citation, abstention, tool, latency, usage/cost, and failure results.
- Docker setup, health check, CI, configuration example, reset path, and runbook.
- Architecture/data-flow diagram, threat model, ADRs, failure analysis, and known limitations.
- Two-minute demo, five-minute technical walkthrough, one-page case study, and truthful resume bullets.
- Evidence ledger and final learning/roadmap matrix.

## Definition of done on November 3

All of the following must be true:

1. A new developer can clone the repository, configure it, ingest the pinned corpus, run tests/evaluations, and start the service using the README.
2. The API returns schema-valid cited answers and explicit abstentions; citations resolve to the pinned source material.
3. Re-ingestion is deterministic and does not silently duplicate chunks.
4. A recorded retrieval comparison supports the selected configuration.
5. The versioned evaluation suite detects regressions in retrieval, grounding/citations, abstention, tool selection, authorization, or approval behavior.
6. Automated tests demonstrate that injection content, malformed arguments, unauthorized tools, denied approval, and approval bypass fail safely.
7. No external write is possible; approved action behavior produces an auditable draft only.
8. Telemetry exposes stage latency, errors, model usage/cost where available, retrieval/tool activity, and an end-to-end correlation identifier without leaking secrets.
9. Docker, health checks, CI, failure/recovery instructions, and the runbook have been exercised.
10. Final evidence reports exact code, corpus, evaluation-set, and provider/model versions and states honest limitations.
11. Sasha can explain the end-to-end request path, deterministic/model boundaries, threat controls, evaluation results, cost/latency trade-offs, and next production steps without notes.
12. The final proof package and demos are linked from `docs/EVIDENCE.md`.

