# Six-Week AI Engineering Sprint

**Dates:** 2026-09-23 through 2026-11-03  
**Budget:** approximately 9 hours per week  
**Execution rule:** complete only the current card. If time is short, narrow features before tests, evaluation, security, or documentation. Each session ends by updating `STATUS.md` and `EVIDENCE.md`; add an ADR when a decision changes architecture or scope.

**October 26 overlay:** Through the Stephen Anthony follow-up, [OCTOBER_26_READINESS.md](OCTOBER_26_READINESS.md) controls call-critical sequencing, capacity, scope cuts, and the protected October 22–25 review window. The cards below retain their acceptance criteria and remain the full-sprint plan, but their original dates are subordinate to the overlay.

## Weekly gates

| Week | Dates | Question | Gate |
|---|---|---|---|
| 1 | Sep 23–29 | Can I build, test, and explain the non-AI system around the model? | Runnable typed API vertical slice, tests, configuration, container, request-path explanation |
| 2 | Sep 30–Oct 6 | Can I give a model useful, tightly bounded capabilities? | Two safe read-only tools, explicit loop limits, fail-closed tests, agent-vs-workflow ADR |
| 3 | Oct 7–13 | Can I ground answers and choose retrieval from measurements? | Versioned ingestion/eval data, retrieval comparison, citations, abstention |
| 4 | Oct 14–20 | Can I detect regressions, diagnose failures, and prevent unsafe action? | Evaluation gate, telemetry, identity/authorization, approved draft, adversarial tests, threat model |
| 5 | Oct 21–27 | Can another person run and assess the system reliably? | CI/container/runbook proof, operational report, reviewer feedback, one evidence-led fix |
| 6 | Oct 28–Nov 3 | Can another person run, evaluate, and understand the system and my judgment? | Reproducible release/demo, complete reports, case study, mock review, final decision review |

## Week 1 — Application foundations and vertical slice

### Session 1 — Baseline and corpus decision

**Date / duration:** Wednesday, 2026-09-23 — 90 minutes  
**Objective:** Establish the learning baseline, initialize version control if approved, and decide whether to accept the recommended corpus.  
**Concepts first:** Python environments; HTTP request/response; JSON/schema validation; unit versus integration tests; secrets; model inference, tokens/context, structured output; deterministic versus model behavior.  
**Diagnostic / skip:** Explain each concept in one or two sentences and sketch `client -> API -> provider -> typed response`. For each Roadmap item mark `Explain`, `Build`, `Operate`, or `Defer`; skip any lesson whose concept and practical example are both sound.  
**Resources:** Roadmap.sh AI Engineer nodes for LLMs/inference, model APIs, tokens and prompting; Full Stack nodes for Git, APIs, testing, Docker and security; Microsoft setup plus Lessons 01–03 READMEs; DataCamp `Working with the OpenAI API` only for failed API items; Manifold `Python Programming Foundations` only for failed Python items.  
**Sasha attempts:** Answer the diagnostic, create the gap matrix, choose whether to initialize Git, and approve FastAPI docs or one recorded alternative with a pinning plan. The agent asks and reviews; it does not fill in Sasha's answers.  
**Outcome / files:** `docs/LEARNING_MATRIX.md`; updated ADR-003, `STATUS.md`, and `EVIDENCE.md`; Git repository initialized only if approved.  
**Acceptance:** Every baseline item has a state and evidence/gap note; corpus is approved or has a dated blocker; no credentials or application code are added.  
**Validation:** `test -f docs/LEARNING_MATRIX.md`; `grep -q 'Explain\|Build\|Operate\|Defer' docs/LEARNING_MATRIX.md`; `git status --short --branch` if Git was initialized; rerun the documentation checks in `STATUS.md`.  
**Evidence:** Baseline matrix plus Sasha's written request-path explanation and corpus decision.  
**Non-goals:** FastAPI scaffolding, provider calls, ingestion, embeddings, or completing either roadmap.  
**Next smallest step:** Select only the Python/package/testing gaps needed to scaffold the service.

### Session 2 — Python project and test harness

**Date / duration:** Thursday, 2026-09-24 — 90 minutes  
**Objective:** Create the smallest Python 3.12 project and a passing test without application behavior.  
**Concepts first:** `pyproject.toml`, lockfiles, virtual environments, import/package layout, Arrange-Act-Assert, dependency groups.  
**Diagnostic / skip:** From memory, explain what `uv sync`, `uv run`, a lockfile, and a unit test each guarantee; skip optional maintainability study if the explanation and a tiny test are correct.  
**Resources:** uv first-steps/project documentation as tool reference; DataCamp `Software Engineering Principles in Python`, Chapter 4 `Maintainability`, only if structure or pytest blocks progress.  
**Sasha attempts:** Initialize the uv project, pin Python 3.12+, choose a simple `src/` layout, add pytest as a development dependency, and write the first non-product smoke test.  
**Outcome / files:** `pyproject.toml`, `uv.lock`, `.python-version`, `src/`, and `tests/test_smoke.py`.  
**Acceptance:** Environment resolves reproducibly; test discovery works; package imports without path hacks; README records the test command.  
**Validation:** `uv sync --locked`; `uv run python --version`; `uv run pytest -q`.  
**Evidence:** First passing test output and a commit link/hash.  
**Non-goals:** FastAPI endpoint, provider SDK, production package hierarchy, or lint-tool shopping.  
**Next smallest step:** Define typed API input/output before connecting a model.

### Session 3 — Typed HTTP boundary

**Date / duration:** Friday, 2026-09-25 — 30 minutes  
**Objective:** Explain and sketch the typed request/response contract for one endpoint.  
**Concepts first:** HTTP methods/status codes, validation, JSON Schema, client errors versus server errors, stable public contracts.  
**Diagnostic / skip:** Given valid, missing, and malformed question payloads, predict the response category and explain why schema validation belongs at the boundary.  
**Resources:** Full Stack roadmap REST/API nodes; FastAPI tutorial sections `Request Body` and `Response Model`; Microsoft Lesson 03 structured/design concepts only if the boundary remains unclear.  
**Sasha attempts:** Draft minimal Pydantic request/result models and three example payloads, including an explicit status suitable for future abstention.  
**Outcome / files:** typed model module and model-validation tests, names chosen by Sasha.  
**Acceptance:** Models reject malformed input, serialize a valid result, and contain no provider-specific types.  
**Validation:** `uv run pytest -q`; `uv run python -c "from app.models import QuestionRequest"` adjusted to the chosen package name.  
**Evidence:** Contract sketch or schema output plus explanation from memory.  
**Non-goals:** Route implementation, live calls, retrieval fields, or exhaustive error taxonomy.  
**Next smallest step:** Introduce the smallest provider protocol and fake.

### Session 4 — Provider seam and structured generation

**Date / duration:** Saturday, 2026-09-26 — 3 hours  
**Objective:** Build and test one hosted-provider-shaped interface using a fake first, then make at most one controlled live call if configured.  
**Concepts first:** dependency inversion, sync/async boundaries, structured model output, nondeterminism, timeouts, token/usage accounting, secret injection.  
**Diagnostic / skip:** Explain what belongs in the provider adapter versus application logic and identify which tests require no network; use DataCamp only for specific failed API concepts.  
**Resources:** Microsoft Lessons 01–03 relevant READMEs; DataCamp `Working with the OpenAI API` sections on authenticated requests, parameters, response handling, tokens/cost and context only as needed; Manifold `LLM API: What to Learn` after the attempt if explanation needs reinforcement.  
**Sasha attempts:** Define the narrow protocol from ADR-002, implement a deterministic fake, write consumer tests, add environment-based settings and `.env.example`, then optionally add one hosted adapter and controlled smoke call.  
**Outcome / files:** provider protocol, fake, settings, `.env.example`, unit tests; optional single adapter/smoke script.  
**Acceptance:** Ordinary tests make zero network calls; secrets are absent from Git; typed output or a controlled error crosses the interface; provider usage metadata can be represented.  
**Validation:** `uv run pytest -q`; `git grep -nE '(sk-|api[_-]?key[[:space:]]*=.+)' -- ':!uv.lock'` returns no secret; optional live command is explicitly marked and not part of pytest.  
**Evidence:** Interface diagram, passing fake tests, and redacted live-call result if run.  
**Non-goals:** Multiple providers, streaming, tool calling, retry library, or local model.  
**Next smallest step:** Put the tested use case behind FastAPI with predictable errors.

### Session 5 — FastAPI vertical slice

**Date / duration:** Sunday, 2026-09-27 — 90 minutes  
**Objective:** Route one request through FastAPI, application use case, provider fake, and typed response.  
**Concepts first:** dependency injection, application versus transport errors, ASGI test clients, correlation IDs, health versus readiness.  
**Diagnostic / skip:** Trace the request lifecycle without notes and classify validation, provider-timeout, and unexpected failures.  
**Resources:** FastAPI tutorial sections `First Steps`, `Dependencies`, `Testing`, and `Handling Errors`; Jam Week 1 FastAPI/health-check patterns only.  
**Sasha attempts:** Implement `/health` and one question endpoint, wire the fake through dependency injection, map controlled errors, and write API tests.  
**Outcome / files:** FastAPI application/routes, use-case module, exception mapping, API tests.  
**Acceptance:** Valid request returns the declared schema; malformed request and fake provider failure have useful distinct responses; tests remain offline.  
**Validation:** `uv run pytest -q`; start with the documented `uv run` command and verify `/health` with `curl -fsS http://127.0.0.1:8000/health`.  
**Evidence:** Test output and a short request-path explanation recorded in `EVIDENCE.md`.  
**Non-goals:** Retrieval, conversational memory, auth, tools, frontend, or production observability.  
**Next smallest step:** Add the first container without changing application behavior.

### Session 6 — Container and baseline assumptions

**Date / duration:** Monday, 2026-09-28 — 20 minutes  
**Objective:** Record the container plan and baseline threat/assumption list; implement only if it fits the protected short block.  
**Concepts first:** image versus container, build context, runtime configuration, least-secret exposure, health checks.  
**Diagnostic / skip:** Explain which files enter the image, which values arrive at runtime, and why `.env` must not be copied.  
**Resources:** Jam Week 1 Docker Compose and health-check patterns; Dockerfile reference only for chosen instructions.  
**Sasha attempts:** Draft a minimal Dockerfile/.dockerignore or, if time is too short, write the exact plan and threats for Session 7.  
**Outcome / files:** Dockerfile and `.dockerignore` or an explicit checked task; `docs/THREAT_MODEL.md` baseline assumptions.  
**Acceptance:** No secret is copied; runtime is noninteractive; health endpoint is identified; threats distinguish untrusted input, model output, and credentials.  
**Validation:** `docker build -t docs-action-agent:dev .` if implemented; otherwise validate linked task and threat file exist.  
**Evidence:** Container plan/build output and initial threat list.  
**Non-goals:** Compose service topology, hardening completeness, authentication, or registry publication.  
**Next smallest step:** Close every Week 1 validation gap and explain the whole slice.

### Session 7 — Week 1 evidence gate

**Schedule adjustment (2026-10-03):** Sasha deferred the repeated foundation review until the explicit agent loop exists. This block was restructured to complete Session 8's agent-versus-workflow content and design artifact. The Week 1 start/test/container checks remain required and will be folded into the explicit-loop gate rather than treated as completed here.

**Date / duration:** Tuesday, 2026-09-29 — 75 minutes  
**Objective:** Finish the minimal container if needed, run the Week 1 gate, and publish a truthful progress note.  
**Concepts first:** reproducibility, validation evidence, known limitation versus failure, why a model call is only one component.  
**Diagnostic / skip:** Explain the request path and one deterministic/model boundary without notes; any weak point becomes the first task, not extra reading.  
**Resources:** Revisit only failed Week 1 sections; no new course or topic.  
**Sasha attempts:** Run all commands from a clean environment, fix failures, update README/status/evidence, and write the four-part weekly note.  
**Outcome / files:** runnable Week 1 slice, tested container, updated README, learning matrix, status/evidence, weekly note.  
**Acceptance:** A new developer has one documented start path; all tests pass; container health works; Sasha can explain tokens/context, structured output, errors, and the architecture without notes.  
**Validation:** `uv sync --locked`; `uv run pytest -q`; `docker build -t docs-action-agent:dev .`; run container and `curl -fsS` its health endpoint; inspect `git status --short`.  
**Evidence:** Week 1 commit, command transcript, architecture sketch, and weekly update #1.  
**Non-goals:** Tool calling, retrieval, database, UI, or Week 2 implementation.  
**Next smallest step:** Specify the first read-only tool contract and deterministic alternative.

## Week 2 — Tool use and the smallest useful agent

### Session 8 — Agent-versus-workflow framing

**Date / duration:** Wednesday, 2026-09-30 — 90 minutes  
**Objective:** Decide which choices, if any, require model-directed tool selection.  
**Concepts first:** tool/function calling, deterministic routing, agent loop, bounded autonomy, step and time budgets, local-model trade-offs.  
**Diagnostic / skip:** For five proposed operations, classify deterministic function, model generation, or model-selected tool and defend each classification.  
**Resources:** Microsoft Lesson 04 introduction and Lesson 17 trade-off/requirements sections; AI Engineer roadmap agents, ReAct, function calling, and local-model nodes.  
**Sasha attempts:** Draw the explicit loop, define failure/stop conditions, and start ADR-006 comparing a deterministic workflow with one bounded model-directed step.  
**Outcome / files:** loop diagram and draft agent-versus-workflow ADR.  
**Acceptance:** Every model decision has a stated reason; maximum steps, timeout, allowed tools, and terminal states are explicit.  
**Validation:** documentation checks plus review that ADR contains context, options, decision, consequences, and revisit conditions.  
**Evidence:** Classification exercise and loop/ADR link.  
**Non-goals:** Implementing tools, multi-agent planning, local inference, or framework adoption.  
**Next smallest step:** Design the first read-only schema and its validation failures.

### Session 9 — First read-only tool contract

**Date / duration:** Thursday, 2026-10-01 — 90 minutes  
**Objective:** Implement one useful, typed, read-only tool behind a framework-free contract.  
**Concepts first:** JSON-schema-style arguments, validation, pure functions, error envelopes, trust boundaries, instructions versus controls.  
**Diagnostic / skip:** Given valid, extra, missing, oversized, and malicious arguments, predict validation behavior and identify where authorization will later run.  
**Resources:** Microsoft Lesson 04 tool definitions/calling workflow and Lesson 06 trustworthy-agent fundamentals; DataCamp Responses API Chapter 2 only if the calling sequence is unclear.  
**Sasha attempts:** Define the tool protocol/registry, implement a deterministic placeholder read-only tool over controlled fixtures, and test argument/result validation.  
**Outcome / files:** tool types/registry, first tool, fixture, unit tests.  
**Acceptance:** Tool has one purpose, no side effects, bounded input/output, stable typed errors, and no provider SDK types.  
**Validation:** `uv run pytest -q` for tool tests and full suite.  
**Evidence:** Schema example and malformed-argument test results.  
**Non-goals:** Second tool, model selection, authorization implementation, or real corpus search.  
**Next smallest step:** Add the second non-overlapping read-only contract.

### Session 10 — Second read-only tool and allowlist

**Date / duration:** Friday, 2026-10-02 — 30 minutes  
**Objective:** Define a second non-overlapping read-only tool and make the allowlist executable.  
**Concepts first:** capability boundaries, allowlist versus name dispatch, least privilege, duplicate tool responsibilities.  
**Diagnostic / skip:** Explain why dynamic name lookup is unsafe and demonstrate that the two tool descriptions lead to distinguishable tasks.  
**Resources:** Microsoft Lesson 04 tool schema examples; DataCamp Responses API Chapter 2 custom tool definitions if needed.  
**Sasha attempts:** Implement/register the second fixture-backed tool and write a disallowed-name test.  
**Outcome / files:** second read-only tool, explicit registry/allowlist, selection fixtures/tests.  
**Acceptance:** Exactly two read-only tools exist; unknown tools fail closed; responsibilities do not overlap materially.  
**Validation:** `uv run pytest -q`; a focused disallowed-tool test passes.  
**Evidence:** Tool table and denial test.  
**Non-goals:** Action tool, prompt routing, corpus ingestion, or more tools.  
**Next smallest step:** Execute validated model tool requests through a capped loop.

### Session 11 — Explicit tool loop

**Date / duration:** Saturday, 2026-10-03 — 3 hours  
**Objective:** Implement the smallest explicit model/tool loop with validation, timeouts, and step limits.  
**Concepts first:** tool-call lifecycle, state machine, termination, timeout boundary, idempotent reads, failure propagation, structured final output.  
**Diagnostic / skip:** Hand-simulate success, malformed arguments, repeated call, unavailable tool, timeout, and max-step exhaustion before coding.  
**Resources:** Microsoft Lesson 04 complete tool-use pattern; DataCamp Responses API Chapter 2 and Chapter 3 structured-output portion only if needed.  
**Sasha attempts:** Extend the fake provider with scripted tool requests, implement the loop explicitly, and write scenario tests before adding optional hosted behavior.  
**Outcome / files:** workflow state/loop, tool executor, scripted fake scenarios, tests.  
**Acceptance:** Loop terminates predictably; every request is validated and allowlisted; timeout/max steps produce typed failures; final response remains schema-valid.  
**Validation:** `uv run pytest -q`; focused scenario suite including success and all stop/failure states.  
**Evidence:** State diagram and scenario result table.  
**Non-goals:** ReAct framework, LangChain, action tool, memory, retries, or retrieval implementation.  
**Next smallest step:** Add useful records without logging secrets or whole sensitive payloads.

### Session 12 — Tool-call records and failure visibility

**Date / duration:** Sunday, 2026-10-04 — 90 minutes  
**Objective:** Record tool requests, validation, outcomes, and failures in a safe structured form.  
**Concepts first:** structured events, correlation IDs, redaction, logs versus audit records, observability without sensitive payload capture.  
**Diagnostic / skip:** Choose safe fields for six events and identify fields that must be omitted/redacted.  
**Resources:** Microsoft Lesson 10 trace/span vocabulary preview; Lesson 06 trust concepts.  
**Sasha attempts:** Define event types, instrument the loop/tool executor, and assert events for success and failure scenarios.  
**Outcome / files:** structured event model/emitter and event-focused tests.  
**Acceptance:** Events correlate a request and expose tool name, validation state, duration and result status without credentials or unrestricted document/model content.  
**Validation:** `uv run pytest -q`; inspect controlled captured logs/events.  
**Evidence:** Redacted sample trace and logging-field decision note.  
**Non-goals:** External observability vendor, dashboards, full distributed tracing, or cost accounting.  
**Next smallest step:** Optionally probe one local endpoint without making it a gate.

### Session 13 — Optional local compatibility probe

**Date / duration:** Monday, 2026-10-05 — 20 minutes  
**Objective:** Decide whether a bounded local-endpoint probe is feasible; do not disrupt the hosted path.  
**Concepts first:** OpenAI-compatible does not mean behavior-identical; local hardware/context/tool-call limits; adapter contract tests.  
**Diagnostic / skip:** If no compatible runtime is already installed or the core tool gate is failing, skip execution and record deferral.  
**Resources:** Microsoft Lesson 17 requirements and bounded-task trade-offs; Jam Week 5 local generation/API patterns only.  
**Sasha attempts:** Record hardware/runtime facts and, only if ready, run one adapter contract case and one bounded tool case.  
**Outcome / files:** short compatibility note and optional result fixture; no new required dependency.  
**Acceptance:** Hosted path remains passing; result or deferral names the exact reason and revisit condition.  
**Validation:** full offline test suite; optional local command documented with model/runtime version.  
**Evidence:** Compatibility result or explicit deferral.  
**Non-goals:** Model benchmarking, installing a large stack, optimizing prompts, or replacing the hosted adapter.  
**Next smallest step:** Run the fixed tool scenarios and close Week 2.

### Session 14 — Week 2 evidence gate

**Date / duration:** Tuesday, 2026-10-06 — 75 minutes  
**Objective:** Demonstrate bounded tools, finalize the workflow decision, and explain the loop.  
**Concepts first:** deterministic versus agentic boundaries, least privilege, fail-closed behavior, test evidence.  
**Diagnostic / skip:** Explain the loop, contracts, stop rules, and why prompts do not enforce permissions without notes.  
**Resources:** Revisit failed Microsoft Lesson 04/06 sections; Manifold `Building Blocks of Agentic AI` only after implementation.  
**Sasha attempts:** Run the scenario set, fix regressions, finalize ADR-006, update docs, record a short demo, and write weekly update #2.  
**Outcome / files:** passing tool scenarios, finalized ADR, demo, updated status/evidence/README.  
**Acceptance:** Useful scenarios select the intended tool; unknown/unavailable/malformed/timed-out calls fail closed; Sasha can defend where an agent is and is not justified.  
**Validation:** `uv run pytest -q`; run documented scenario command; documentation checks; inspect Git diff/status.  
**Evidence:** Scenario table, ADR, denial proof, demo, and Week 2 commit/update.  
**Non-goals:** Retrieval, action tool, expanded autonomy, or Week 3 implementation.  
**Next smallest step:** Pin the approved corpus and design a reproducible manifest.

## Week 3 — Retrieval, citations, and measured RAG

### Session 15 — Corpus manifest and ingestion contract

**Date / duration:** Wednesday, 2026-10-07 — 90 minutes  
**Objective:** Pin the approved corpus and define reproducible ingestion inputs/outputs before parsing.  
**Concepts first:** source licensing/attribution, commit/tag pinning, manifests, content hashes, index-time versus query-time work, deterministic IDs.  
**Diagnostic / skip:** Explain how the same source version yields the same document/chunk identity and how a changed version is detected.  
**Resources:** Microsoft Lesson 05 ingestion/RAG overview; Jam Week 2 ingestion retry/metadata concepts adapted to Markdown/HTML; approved upstream repository/license.  
**Sasha attempts:** Write the corpus manifest schema, bounded path allowlist, attribution record, source-version rule, and ingestion contract using a tiny checked-in fixture subset.  
**Outcome / files:** corpus manifest/config, source attribution, ingestion types, fixtures, contract tests.  
**Acceptance:** Corpus name, upstream URL, license, pin, included paths, fetch method, and content hashes are representable; no network is needed for unit tests.  
**Validation:** schema/unit tests; verify fixture hashes and that out-of-scope paths are rejected.  
**Evidence:** Approved manifest and deterministic-ID explanation.  
**Non-goals:** Full download, chunking optimization, embeddings, vector store, or answer generation.  
**Next smallest step:** Parse and normalize the bounded source deterministically.

### Session 16 — Parse, normalize, and deduplicate

**Date / duration:** Thursday, 2026-10-08 — 90 minutes  
**Objective:** Build deterministic Markdown/HTML parsing and document-level duplicate handling.  
**Concepts first:** normalization, heading hierarchy, canonical source path/URL, exact duplicate versus near duplicate, idempotency.  
**Diagnostic / skip:** For sample pages with repeated navigation, code blocks, duplicate content, and changed headings, state what should be preserved or removed.  
**Resources:** Jam Week 2 ingestion validation/retry/metadata patterns; Microsoft Lesson 05 data preparation; DataCamp embeddings course is not yet needed.  
**Sasha attempts:** Parse controlled fixtures, preserve headings/code/source metadata, assign stable document IDs, and test repeat ingestion and changed content.  
**Outcome / files:** parser/normalizer, document model, fixture corpus, idempotency tests.  
**Acceptance:** Reprocessing identical input yields identical records; exact duplicates are explicit; code and source anchors needed for citation survive.  
**Validation:** `uv run pytest -q` with parser/idempotency focus; run ingestion twice and compare deterministic summaries.  
**Evidence:** Before/after normalized sample and duplicate test result.  
**Non-goals:** Near-duplicate ML, production crawler, chunk-size tuning, or search.  
**Next smallest step:** Create an evaluation set before optimizing retrieval.

### Session 17 — Retrieval evaluation set and keyword baseline

**Date / duration:** Friday, 2026-10-09 — 30 minutes  
**Objective:** Seed versioned questions and define retrieval metrics, then outline the keyword baseline.  
**Concepts first:** relevance judgments, expected source/chunk, Recall@k/Hit@k/MRR, answerable versus unanswerable, leakage.  
**Diagnostic / skip:** Compute one small metric example by hand and explain why questions must exist before comparing retrieval.  
**Resources:** Jam Week 3 BM25/relevance metrics sections; Microsoft Lesson 05 retrieval concepts.  
**Sasha attempts:** Author at least five representative cases now (toward 15–20), including one unanswerable and one misleading query, with expected sources and rationale.  
**Outcome / files:** versioned evaluation dataset/schema and metric definitions; keyword baseline task/spec.  
**Acceptance:** Cases are independent of current search output, cite pinned sources, and define what counts as relevant.  
**Validation:** dataset schema test, unique IDs, valid source references, and a hand-checked metric fixture.  
**Evidence:** Evaluation-set v0.1 and metric explanation.  
**Non-goals:** Finishing all cases, vector search, generation grading, or tuning to pass authored queries.  
**Next smallest step:** Implement the keyword baseline and measure it unchanged.

### Session 18 — Chunking and keyword retrieval baseline

**Date / duration:** Saturday, 2026-10-10 — 3 hours  
**Objective:** Produce stable chunks and a measured keyword/BM25-like search baseline.  
**Concepts first:** section-aware chunking, overlap trade-offs, lexical scoring, filtering, top-k, retrieval versus context construction.  
**Diagnostic / skip:** Predict failure modes for tiny, huge, fixed-character, and section-aware chunks; identify what metric would expose each.  
**Resources:** Jam Week 3 BM25/query/filtering/metrics and Week 4 section-aware chunking; Microsoft Lesson 05; Lesson 12 context-engineering section relevant to evidence selection.  
**Sasha attempts:** Implement stable section-aware chunks, persist one simple keyword index, complete 15–20 retrieval cases, and run the untouched baseline.  
**Outcome / files:** chunker, chunk model/IDs, keyword index/retriever, evaluation runner/data, baseline result artifact.  
**Acceptance:** Chunks retain source/heading/version IDs; re-ingestion is idempotent; metrics are reproducible; baseline failures are recorded rather than hidden.  
**Validation:** full tests; run ingestion twice; run the versioned retrieval evaluation and save machine-readable plus human summary results.  
**Evidence:** Corpus/chunk counts, baseline metrics, and three categorized failures.  
**Non-goals:** Prompt tuning, vector-store shopping, reranker, generation, or changing the dataset after seeing failures without versioning.  
**Next smallest step:** Implement exactly one vector or hybrid comparator.

### Session 19 — One vector/hybrid comparator

**Date / duration:** Sunday, 2026-10-11 — 90 minutes  
**Objective:** Add one embedding-based retrieval configuration using one local store and compare it fairly.  
**Concepts first:** embeddings, cosine similarity, metadata filters, index versioning, hybrid fusion, embedding cost and determinism.  
**Diagnostic / skip:** Explain what an embedding represents, why versions matter, and when lexical search should win; if weak, do the targeted DataCamp lab before implementation.  
**Resources:** DataCamp `Introduction to Embeddings` sections on similarity, semantic search, metadata/filtering and ChromaDB; Jam Week 4 embeddings/hybrid/RRF; AI Engineer roadmap embedding/vector nodes.  
**Sasha attempts:** Implement exactly one comparator (vector or hybrid), capture embedding configuration, run the same dataset/top-k, and resist unversioned question edits.  
**Outcome / files:** one local vector-store adapter/config, comparator retrieval path, reproducible comparison results.  
**Acceptance:** Same corpus/eval cases and metric definitions are used; store can be rebuilt; cost/latency and qualitative failures accompany scores.  
**Validation:** adapter/index tests; clean rebuild; run both configurations with pinned settings and compare saved reports.  
**Evidence:** Side-by-side metric/latency/cost table and recommendation draft.  
**Non-goals:** Pinecone, multiple vector databases, broad embedding benchmark, reranking, or framework migration.  
**Next smallest step:** Turn retrieved evidence into cited output and explicit abstention.

### Session 20 — Cited answer and abstention

**Date / duration:** Monday, 2026-10-12 — 20 minutes  
**Objective:** Specify and test the citation/abstention contract; implement only the smallest slice that fits.  
**Concepts first:** retrieval failure versus generation failure, citation support, evidence threshold, `insufficient_evidence` as a first-class result.  
**Diagnostic / skip:** Classify three answerable and three unanswerable contexts and state what evidence a citation validator can check deterministically.  
**Resources:** Microsoft Lesson 05 grounding/citation sections; Jam Week 5 local generation pattern only as reference.  
**Sasha attempts:** Define cited-answer fields and abstention rules, add fake-provider cases, and implement or queue the smallest evidence-to-answer use case.  
**Outcome / files:** cited result/citation models, abstention policy tests, optional minimal use-case wiring.  
**Acceptance:** No-evidence path makes no factual claim; citations identify source and chunk; unsupported citation fixtures fail.  
**Validation:** focused schema/policy tests plus full offline suite.  
**Evidence:** Answer/abstention examples and support-check rationale.  
**Non-goals:** Perfect automated factuality, LLM-as-judge, prompt optimization, or action tool.  
**Next smallest step:** Finish wiring, choose retrieval from evidence, and close the weekly gate.

### Session 21 — Week 3 evidence gate

**Date / duration:** Tuesday, 2026-10-13 — 75 minutes  
**Objective:** Finalize cited/abstaining RAG, choose retrieval using results, and publish the checkpoint.  
**Concepts first:** comparable experiments, retrieval/generation error attribution, honest limitations, ADR consequences.  
**Diagnostic / skip:** Explain the winning and losing cases and why the selected configuration is justified; inability to do so blocks the ADR.  
**Resources:** Revisit only the exact failed Microsoft/Jam/DataCamp section; no new retrieval technique.  
**Sasha attempts:** Complete wiring, run the fixed suite, write the retrieval ADR, update docs, and prepare the concise Prashant/weekly checkpoint.  
**Outcome / files:** end-to-end cited answer/abstention path, ADR-007, evaluation report v0.1, status/evidence/README updates.  
**Acceptance:** Re-ingestion does not duplicate; selected retrieval has measured justification; factual results expose sources; unanswerable cases abstain according to recorded thresholds.  
**Validation:** clean ingestion twice; complete test suite; fixed retrieval and answer checks; verify report configuration/version metadata.  
**Evidence:** Week 3 commit, retrieval report/ADR, one metric, one failure analysis, repository checkpoint note.  
**Non-goals:** Security action controls, new retrieval algorithms, dashboards, or Week 4 implementation.  
**Next smallest step:** Define the regression gate and telemetry needed to diagnose it.

## Week 4 — Evaluation, security, observability, and approval

### Session 22 — Evaluation contract and regression gate

**Date / duration:** Wednesday, 2026-10-14 — 90 minutes  
**Objective:** Convert current checks into a repeatable, versioned evaluation gate with explicit thresholds.  
**Concepts first:** offline versus online evaluation, deterministic versus model-graded checks, baselines, thresholds, flakiness, regression policy.  
**Diagnostic / skip:** Identify which current metrics can fail CI deterministically and which require repeated or human review.  
**Resources:** Microsoft Lesson 10 accuracy/offline-online evaluation and regression sections; DataCamp `LLMOps Concepts` Development and Operational chapters, one hour maximum, only as checklist.  
**Sasha attempts:** Define evaluation manifest/result schemas, split deterministic and live tiers, set justified initial gates, and add a failing regression fixture before the passing run.  
**Outcome / files:** evaluation command, manifest/version metadata, thresholds, deterministic regression tests, report template.  
**Acceptance:** A known source/grounding/tool regression fails; paid/live evaluation is opt-in; every report identifies all relevant versions/config.  
**Validation:** run a deliberately failing fixture, then the passing deterministic evaluation; full tests.  
**Evidence:** Red/green regression transcript and evaluation policy.  
**Non-goals:** Perfect universal score, opaque LLM judge as sole gate, or CI integration before the command is stable.  
**Next smallest step:** Trace one request across retrieval, model, and tools.

### Session 23 — End-to-end structured telemetry

**Date / duration:** Thursday, 2026-10-15 — 90 minutes  
**Objective:** Make latency, usage/cost, retrieval, model, tool, and error stages diagnosable.  
**Concepts first:** logs, metrics, traces/spans, correlation, cardinality, redaction, usage-derived cost assumptions.  
**Diagnostic / skip:** Given a slow incorrect response, list the minimum events/fields needed to distinguish ingestion, retrieval, model, and tool failure.  
**Resources:** Microsoft Lesson 10 traces/spans, latency/cost/errors and OpenTelemetry concepts; Jam Week 6 tracing and latency/cost patterns.  
**Sasha attempts:** Extend structured events into request-spanning telemetry, capture stage durations and provider usage, and test redaction/correlation.  
**Outcome / files:** telemetry interface/implementation, cost configuration, event tests, sample trace.  
**Acceptance:** One correlation ID links all stages; usage/cost records assumptions; secrets/full uncontrolled content are absent; one injected failure is localized from events.  
**Validation:** full tests; execute success and injected-failure scenarios; inspect captured structured output.  
**Evidence:** Redacted traces and diagnosed failure note.  
**Non-goals:** Vendor dashboard, production sampling strategy, distributed collector, or caching.  
**Next smallest step:** Define identity, roles, and authorization before adding an action.

### Session 24 — Identity and per-tool authorization

**Date / duration:** Friday, 2026-10-16 — 30 minutes  
**Objective:** Specify a credible demo identity boundary and enforce per-tool authorization in code.  
**Concepts first:** authentication versus authorization, subject/role/capability, default deny, confused deputy, service versus user identity.  
**Diagnostic / skip:** For anonymous, reader, and approver roles, state permitted operations and where enforcement runs.  
**Resources:** Microsoft Lesson 06 trust boundaries; Lesson 16 safe tool operation/least privilege; Lesson 18 auditability concept only.  
**Sasha attempts:** Write the access matrix, implement the smallest local/demo identity dependency, and add default-deny authorization tests around tool execution.  
**Outcome / files:** identity/role model, policy function, access matrix, authorization tests.  
**Acceptance:** Missing/unknown identity and unauthorized tools fail closed independently of prompt/model output.  
**Validation:** focused role/tool matrix tests plus full suite.  
**Evidence:** Access matrix and denied-tool trace.  
**Non-goals:** OAuth provider, enterprise SSO, cryptographic receipts, or action implementation.  
**Next smallest step:** Design a two-phase, draft-only action with explicit approval.

### Session 25 — Approval-gated draft tool

**Date / duration:** Saturday, 2026-10-17 — 3 hours  
**Objective:** Implement one draft-producing tool with a deterministic approval state machine and no external write.  
**Concepts first:** propose/review/approve/deny/execute states, TOCTOU, binding approval to exact arguments/content, idempotency, audit trail.  
**Diagnostic / skip:** Hand-simulate denied, altered-after-approval, replayed, unauthorized, expired, malformed, and successful draft flows.  
**Resources:** Microsoft Lesson 16 human approval/evaluation-gate/safe-tool sections; Lesson 18 auditability/receipt concepts without full cryptography; Lesson 10 tracing.  
**Sasha attempts:** Define state and approval records, implement a draft artifact tool that cannot externally write, bind approval to normalized request/content hash, and test every scenario first.  
**Outcome / files:** draft tool, approval state/policy, audit events, security tests, API route(s) if needed.  
**Acceptance:** Exactly one action tool exists; only authorized explicit approval for the unchanged proposal produces a draft; denial/replay/change/bypass fails and is audited.  
**Validation:** complete security scenario suite, full tests, and inspect audit event chain for controlled cases.  
**Evidence:** Approval state diagram, pass/fail table, and denied/bypass traces.  
**Non-goals:** GitHub/Jira/email write, generic workflow engine, cryptographic signing, or background jobs.  
**Next smallest step:** Attack untrusted documents and tool arguments systematically.

### Session 26 — Adversarial and failure tests

**Date / duration:** Sunday, 2026-10-18 — 90 minutes  
**Objective:** Test prompt injection, malicious corpus content, source poisoning, malformed arguments, repeated requests, and tool failures.  
**Concepts first:** data/instruction separation, indirect prompt injection, source provenance, output validation, graceful degradation, security invariant.  
**Diagnostic / skip:** For each threat, identify the protected asset, enforcement boundary, expected safe result, and observable event before writing a fixture.  
**Resources:** Microsoft Lesson 06 trustworthy agents and applicable Lesson 18 concepts; AI Engineer roadmap safety/prompt-injection nodes.  
**Sasha attempts:** Add controlled malicious fixtures and tests, mark retrieved content as untrusted in context construction, assert no authorization/approval bypass, and preserve useful failure responses.  
**Outcome / files:** adversarial fixture corpus, injection/source-poisoning/malformed/repeat/failure tests, updated controls.  
**Acceptance:** Untrusted text cannot grant capability or alter approval state; malformed and failed tools return typed safe outcomes; sources remain attributable.  
**Validation:** targeted adversarial suite and full deterministic evaluation; inspect telemetry for at least one case.  
**Evidence:** Threat-to-test matrix with results and one surviving limitation.  
**Non-goals:** Claiming injection is solved, content moderation platform, sandbox service, or new features.  
**Next smallest step:** Consolidate controls into a threat model and one failure analysis.

### Session 27 — Week 4 evidence gate

**Date / duration:** Monday, 2026-10-19 — 20 minutes  
**Objective:** Draft the threat model and verify that security/evaluation evidence is complete enough for final review.  
**Concepts first:** assets, actors, trust boundaries, abuse cases, mitigations, residual risk, evidence-linked claims.  
**Diagnostic / skip:** Explain why a prompt is not a security control and name the deterministic control for each high-risk path.  
**Resources:** Manifold `A Prompt Is Not a Security Control` after controls exist; Microsoft Lesson 06 recap.  
**Sasha attempts:** Update `docs/THREAT_MODEL.md`, link tests to threats, and outline one telemetry-backed failure analysis.  
**Outcome / files:** threat model v1 and failure-analysis draft.  
**Acceptance:** Each material boundary has a threat, control, verification link, and residual risk; claims do not exceed tests.  
**Validation:** documentation links resolve; targeted authorization/approval/injection tests pass.  
**Evidence:** Threat model and two-minute spoken/written security explanation.  
**Non-goals:** New controls unless a critical gap is found, formal compliance, or exhaustive STRIDE exercise.  
**Next smallest step:** Run the full Week 4 gate and repair only failures.

### Session 28 — Week 4 full gate and report

**Date / duration:** Tuesday, 2026-10-20 — 75 minutes  
**Objective:** Prove regression detection, observability, authorization, and approval behavior end to end.  
**Concepts first:** release gates, evidence integrity, diagnosing before fixing, residual-risk communication.  
**Diagnostic / skip:** From one injected failure, use telemetry to identify the stage and control; from one denied action, identify every enforcement/event step.  
**Resources:** Revisit only failing Lesson 10/16/18 or security sections; no new topic.  
**Sasha attempts:** Run all deterministic gates, repair failures, complete the failure analysis/evaluation report, and write weekly update #4.  
**Outcome / files:** evaluation report v0.2, completed threat model/failure analysis, updated status/evidence/README.  
**Acceptance:** Known regressions fail the gate; auth/approval bypass tests pass; at least one failure is diagnosed from telemetry; limitations are explicit.  
**Validation:** full pytest suite; deterministic evaluation; adversarial suite; documentation link check; clean secret scan.  
**Evidence:** Week 4 commit, reports, traces, test summary, and weekly update.  
**Non-goals:** CI/container reliability work, stakeholder pilot, new framework, or Week 5 implementation.  
**Next smallest step:** Define the clean-run, health, reset, and recovery experience for another developer.

## Week 5 — Reliability, packaging, and external review

### Session 29 — Operational requirements and failure modes

**Date / duration:** Wednesday, 2026-10-21 — 90 minutes  
**Objective:** Turn another developer's journey and known failures into concrete operational requirements.  
**Concepts first:** health/readiness, dependency failure, retries/backoff, idempotency, graceful degradation, configuration validation, recovery point.  
**Diagnostic / skip:** For provider timeout, corrupt index, missing config, duplicate request, and unavailable dependency, choose retry/fail/degrade and defend it.  
**Resources:** Microsoft Lesson 16 lifecycle, versioning, routing/caching and governance sections; Jam Week 1 health/service boundaries and Week 6 caching patterns.  
**Sasha attempts:** Map startup/run/reset/recovery flows, create an operational failure table, and identify only the retries/caching justified by measured failures.  
**Outcome / files:** `docs/RUNBOOK.md` outline, operational failure matrix, release/version plan.  
**Acceptance:** Each failure has detection, response, recovery, operator evidence, and retry/idempotency reasoning; no speculative cache/service is added.  
**Validation:** documentation link check and walkthrough of each command/path against the current repository.  
**Evidence:** Failure matrix and runbook outline.  
**Non-goals:** Implementing every resilience pattern, Redis, Kubernetes, autoscaling, or cloud deployment.  
**Next smallest step:** Make Docker startup and health deterministic from a clean state.

### Session 30 — Reproducible Docker and health/reset paths

**Date / duration:** Thursday, 2026-10-22 — 90 minutes  
**Objective:** Make containerized setup, readiness, corpus/index initialization, and reset repeatable.  
**Concepts first:** immutable image, persistent/generated data, startup ordering, health versus readiness, destructive reset scope.  
**Diagnostic / skip:** Identify which artifacts are source, cache, generated index, secret, and persistent evidence; explain safe reset boundaries.  
**Resources:** Jam Week 1 Docker Compose, health checks and service-boundary patterns; Microsoft Lesson 16 environment/version concepts.  
**Sasha attempts:** Refine Docker/Compose only as needed, add explicit init/reset commands, validate configuration at startup, and document safe data paths.  
**Outcome / files:** Docker/Compose configuration, scripts or CLI commands for ingest/reset, `.env.example`, runbook instructions.  
**Acceptance:** Clean build/start succeeds; readiness reflects required state; reset targets only documented generated data; secrets remain runtime-only.  
**Validation:** build from clean cache where practical; start; hit health/readiness; ingest fixture; query; reset; verify recovery; stop cleanly.  
**Evidence:** Clean-run transcript and recovery proof.  
**Non-goals:** Production cluster, registry release, persistent cloud database, or extra services without measured need.  
**Next smallest step:** Put stable tests/evaluations into CI with controlled live-call exclusion.

### Session 31 — Continuous integration gate

**Date / duration:** Friday, 2026-10-23 — 30 minutes  
**Objective:** Define and begin the minimal CI workflow for deterministic quality gates.  
**Concepts first:** hermetic CI, dependency lock enforcement, secrets in forks, deterministic versus live tiers, artifacts and exit codes.  
**Diagnostic / skip:** List which commands can safely run on every pull request and why live/provider evaluation must be separate.  
**Resources:** Full Stack roadmap CI/CD and automation nodes; GitHub Actions Python/uv documentation as syntax reference.  
**Sasha attempts:** Add or draft one CI job that syncs locked dependencies, runs tests and deterministic evaluation, and uploads/prints useful failure evidence.  
**Outcome / files:** CI workflow and documented gate table.  
**Acceptance:** No provider secret is required; failed tests/evaluations fail the job; Python/lock version is explicit.  
**Validation:** syntax inspection and local execution of the exact job commands; remote CI run when a remote exists.  
**Evidence:** Workflow link and first run result or clearly recorded remote blocker.  
**Non-goals:** Deployment pipeline, matrix explosion, coverage vanity target, or live paid evaluations on every commit.  
**Next smallest step:** Exercise a real operational failure and make the runbook sufficient.

### Session 32 — Reliability exercise and runbook

**Date / duration:** Saturday, 2026-10-24 — 3 hours  
**Objective:** Implement only evidence-justified retries/idempotency/degradation and prove recovery from one material failure.  
**Concepts first:** retryable versus permanent errors, exponential backoff/jitter, retry budget, idempotency key, circuit/degradation behavior, cache correctness.  
**Diagnostic / skip:** Classify current errors and demonstrate why retrying validation/auth failures is wrong; choose the highest-value observed operational gap.  
**Resources:** Microsoft Lesson 10 retries/fallbacks and Lesson 16 caching/model-routing/lifecycle sections; Jam Week 6 caching/optimization only if metrics justify caching.  
**Sasha attempts:** Write failure tests first, add bounded resilience to the selected path, exercise recovery, and complete runbook commands and troubleshooting.  
**Outcome / files:** resilience tests/code, completed runbook draft, recovery transcript, optional cache ADR only if measured.  
**Acceptance:** Behavior is bounded and observable; duplicate consequential drafts are prevented; runbook recovery works from another shell/clean state; unjustified cache is omitted.  
**Validation:** full tests/evaluation; inject selected failure; follow runbook recovery exactly; container smoke test.  
**Evidence:** Before/after failure result, runbook exercise, and decision note.  
**Non-goals:** Blanket retries, Redis by default, high availability, load testing at production scale, or feature work.  
**Next smallest step:** Prepare a reviewer task and operational summary that expose limitations.

### Session 33 — Operational report and reviewer protocol

**Date / duration:** Sunday, 2026-10-25 — 90 minutes  
**Objective:** Produce a compact quality/latency/cost/failure report and a safe external review script.  
**Concepts first:** task success versus demo appeal, reviewer bias, comparable metrics, feedback capture, non-sensitive pilot boundary.  
**Diagnostic / skip:** Explain what a reviewer can falsify and which observations would change the design.  
**Resources:** Microsoft Lesson 10 feedback/online evaluation concepts; Manifold portfolio/forward-deployed material is deferred until Week 6.  
**Sasha attempts:** Generate the operational report from current artifacts, write 3–5 review tasks plus observation questions, and schedule/request one or two reviews.  
**Outcome / files:** operational report, reviewer guide, feedback form/log, redacted demo data.  
**Acceptance:** Report names versions and limitations; tasks include success, abstention and denied action; no workplace/private data is requested.  
**Validation:** regenerate report; dry-run every reviewer task from documented setup; verify links and redaction.  
**Evidence:** Report and dry-run transcript.  
**Non-goals:** Marketing claims, hard-coding to a reviewer's department, feature promises, or broad user study.  
**Next smallest step:** Conduct or prepare the first review and capture observations verbatim.

### Session 34 — Reviewer session or preparation

**Date / duration:** Monday, 2026-10-26 — 20 minutes  
**Objective:** Conduct a short domain-neutral review if scheduled; otherwise ensure the package is ready and send the request.  
**Concepts first:** observation versus interpretation, leading questions, severity/impact, consent and public data boundary.  
**Diagnostic / skip:** State the target task and what evidence would show the workflow is not useful.  
**Resources:** `docs/RUNBOOK.md`, reviewer guide, current evidence only; no course study.  
**Sasha attempts:** Let the reviewer operate from instructions, capture friction/failures/quotes accurately, or complete the outreach and rehearsal.  
**Outcome / files:** dated reviewer notes or sent-review record; issue candidates.  
**Acceptance:** Notes separate observed behavior from requested features and contain no sensitive data; no code is changed mid-review.  
**Validation:** verify notes link to version/config and each issue has reproduction/impact evidence.  
**Evidence:** Reviewer record or preparation/outreach artifact.  
**Non-goals:** Defending the design, implementing live feedback immediately, or expanding scope.  
**Next smallest step:** Rank evidence and fix the single highest-value failure.

### Session 35 — Week 5 evidence gate

**Date / duration:** Tuesday, 2026-10-27 — 75 minutes  
**Objective:** Incorporate review evidence, fix one high-value failure, and prove another developer can run the project.  
**Concepts first:** severity versus frequency, opportunity cost, regression protection, feedback-to-decision traceability.  
**Diagnostic / skip:** Rank review/operational findings by user impact, safety, learning value and effort; justify why the chosen one outranks a new feature.  
**Resources:** Current test/evaluation/runbook evidence only; relevant source section only if the selected fix exposes a specific gap.  
**Sasha attempts:** Add a reproducing test, implement the smallest fix, rerun all gates, update runbook/report/status/evidence, and write weekly update #5.  
**Outcome / files:** one evidence-led fix and regression test, reviewer notes, CI/container/runbook proof, updated report.  
**Acceptance:** Another developer path is reproducible or remaining blocker is explicit; selected failure is fixed without weakening security/evaluation; one recovery path is proven.  
**Validation:** CI-equivalent commands; clean Docker run; deterministic evaluation; reviewer task rerun; documentation link/secret checks.  
**Evidence:** Week 5 commit, before/after case, reviewer artifact, CI result, weekly update.  
**Non-goals:** Multiple feedback features, UI polish, deployment breadth, or Week 6 storytelling before evidence is sound.  
**Next smallest step:** Freeze scope and rank remaining release-critical failures.

## Week 6 — Deployment, communication, and interview proof

### Session 36 — Release scope and architecture revision

**Date / duration:** Wednesday, 2026-10-28 — 90 minutes  
**Objective:** Freeze feature scope, choose reproducible local demo versus hosted deployment, and revise architecture/data-flow diagrams to match reality.  
**Concepts first:** release criteria, environment separation, rollback thinking, diagrams as behavior/ownership models, deployment signal versus cost.  
**Diagnostic / skip:** Defend whether hosting adds portfolio signal beyond a fully reproducible local demo; identify every diagram box's responsibility and failure boundary.  
**Resources:** Microsoft Lesson 16 deployment lifecycle/versioning sections; Manifold `AI Architecture Is Not a Diagram` after drafting the revision.  
**Sasha attempts:** Make the deployment/local-demo decision in an ADR, freeze noncritical features, update architecture/data-flow/deployment diagrams, and rank release blockers.  
**Outcome / files:** release ADR, diagrams, frozen blocker list, version/release checklist.  
**Acceptance:** Diagrams match implemented components and trust boundaries; decision considers cost, secrets, reproducibility and evaluator access; no new feature branch is opened.  
**Validation:** diagram links/rendering check; walk one success, abstention, denied action and failure path through the diagram.  
**Evidence:** Release decision and reviewed diagrams.  
**Non-goals:** Hosting for its own sake, new cloud platform study, architectural rewrite, or feature expansion.  
**Next smallest step:** Fix the highest release-critical evaluation or pilot failure.

### Session 37 — Highest-value hardening fix

**Date / duration:** Thursday, 2026-10-29 — 90 minutes  
**Objective:** Resolve the single highest-impact remaining failure with a regression test.  
**Concepts first:** root cause versus symptom, risk-based prioritization, narrow change, regression evidence.  
**Diagnostic / skip:** Reproduce the failure, identify the responsible stage from telemetry, and state the invariant before editing.  
**Resources:** Only the exact project/source section implicated by the root cause; Manifold `Forward Deployed AI Engineer Guide` after the fix for stakeholder framing.  
**Sasha attempts:** Add a failing test/eval case, implement the smallest correction, compare results, and update limitations/decision if behavior changes.  
**Outcome / files:** hardening fix, regression test/case, before/after result, updated limitation.  
**Acceptance:** Reproduction fails before and passes after; full gates do not regress; the change is explainable without framework magic.  
**Validation:** focused red/green test; full tests/evaluation/security suite; container smoke.  
**Evidence:** Root-cause note, diff/commit, and before/after metric or behavior.  
**Non-goals:** Fixing every low-severity issue, refactoring for aesthetics, or adding capabilities.  
**Next smallest step:** Assemble the final reproducibility and documentation package.

### Session 38 — Final documentation and report skeleton

**Date / duration:** Friday, 2026-10-30 — 30 minutes  
**Objective:** Identify and fill the most critical gap in setup, runbook, threat, decision, evaluation, or limitation documentation.  
**Concepts first:** audience-specific documentation, evidence-linked claims, known limitation, reproducible configuration.  
**Diagnostic / skip:** Use a checklist to locate the one missing item that would stop an external evaluator from reproducing or trusting the result.  
**Resources:** Final deliverables and definition of done in `SPEC.md`; Manifold architecture video only if not already used.  
**Sasha attempts:** Update the highest-priority document and create the final evaluation/case-study outline with evidence links.  
**Outcome / files:** improved README/runbook/report/threat/limitations document and final proof-package checklist.  
**Acceptance:** Claims link to artifacts; setup and versions are explicit; missing items have owners/dates rather than hidden placeholders.  
**Validation:** documentation link check, copy/paste command review, and definition-of-done checklist review.  
**Evidence:** Documentation diff and evaluator checklist.  
**Non-goals:** Recording the demo, writing generic AI prose, new technical work, or cosmetic overhaul.  
**Next smallest step:** Run a clean-room release rehearsal and capture final metrics.

### Session 39 — Clean-room release and final evaluation

**Date / duration:** Saturday, 2026-10-31 — 3 hours  
**Objective:** Exercise the project from a clean start and produce the final versioned technical report.  
**Concepts first:** release candidate, provenance, clean-room reproducibility, rollback/reset, statistically honest reporting, artifact retention.  
**Diagnostic / skip:** Before running, state exact expected commands, versions, gates and rollback; any ambiguity is a documentation defect.  
**Resources:** Current README/runbook; Microsoft Lesson 10 evaluation recap; Manifold `AI Interview Preparation Roadmap` after results exist.  
**Sasha attempts:** Build/start/ingest/evaluate from clean state, exercise success/abstention/denial/failure, capture versions/metrics, repair release-critical defects only, and tag/record a release candidate if Git exists.  
**Outcome / files:** final evaluation report, release manifest, command transcript, finalized runbook/known limitations, release candidate.  
**Acceptance:** All definition-of-done technical gates pass or each exception is explicit and noncritical; report includes quality, citations, abstention, latency, usage/cost, tools, security and failures with provenance.  
**Validation:** execute README from clean state; full tests/evaluation/security suite; Docker health/reset/recovery; secret scan; artifact/link checks.  
**Evidence:** Release candidate commit/tag, final report, clean-run transcript, and metrics artifacts.  
**Non-goals:** Hiding failures, changing evaluation data to improve scores, adding features, or claiming production readiness.  
**Next smallest step:** Turn verified evidence into concise demo and case-study narratives.

### Session 40 — Demo and case study

**Date / duration:** Sunday, 2026-11-01 — 90 minutes  
**Objective:** Record evidence-based demonstrations and draft the public case study/resume bullets.  
**Concepts first:** problem-action-result narrative, trade-off explanation, demo determinism, truthful attribution, measured claims.  
**Diagnostic / skip:** Deliver a two-minute explanation without notes covering problem, architecture, one metric, one failure, one security boundary and one limitation.  
**Resources:** Manifold `Five Portfolio Artifacts` and `Forward Deployed AI Engineer Guide`; `AI Interview Preparation Roadmap` for explanation prompts.  
**Sasha attempts:** Record a two-minute demo and five-minute walkthrough showing success, abstention, denied action and diagnosed failure; draft one-page case study and two factual resume bullets.  
**Outcome / files:** demo links/files, walkthrough, case study, resume bullets, updated evidence ledger.  
**Acceptance:** Every claim maps to final evidence; demo uses pinned public data and release candidate; limitations and Sasha's decisions are visible.  
**Validation:** replay media; verify all four required paths and links; peer/self-check claims against report.  
**Evidence:** Demo, walkthrough, case study and resume bullets.  
**Non-goals:** Promotional exaggeration, polished frontend, new benchmark, or reshooting for minor aesthetics.  
**Next smallest step:** Rehearse a skeptical architecture/security/operations review.

### Session 41 — Mock system-design review

**Date / duration:** Monday, 2026-11-02 — 20 minutes  
**Objective:** Rehearse defending the implemented system and record unanswered questions.  
**Concepts first:** requirements clarification, trade-offs, scaling boundary, identity/permissions, evaluation, cost, failure ownership, multi-tenancy concepts.  
**Diagnostic / skip:** Answer five prompts without notes: why agentic, why this retrieval, how approval works, how improvement is proven, and what changes for enterprise scale.  
**Resources:** Manifold `AI Interview Preparation Roadmap`; current ADRs, threat model, evaluation report and diagrams.  
**Sasha attempts:** Conduct a timed mock review, cite actual evidence, say `unknown` where appropriate, and record the top three weak answers.  
**Outcome / files:** mock-review notes and targeted final corrections list.  
**Acceptance:** Answers distinguish implemented facts from future design; Kubernetes/multi-agent/multi-tenancy are explained as scale considerations, not fake completed work.  
**Validation:** Verify each factual answer against an artifact and each unknown appears in limitations/next steps.  
**Evidence:** Mock questions, answers, and three improvement notes.  
**Non-goals:** Memorizing buzzwords, implementing corrections, or expanding the project overnight.  
**Next smallest step:** Run the final definition-of-done and six-week decision review.

### Session 42 — Final gate and November 3 decision review

**Date / duration:** Tuesday, 2026-11-03 — 75 minutes  
**Objective:** Close the sprint with a verified proof package, stakeholder notes, and an evidence-based next-step decision.  
**Concepts first:** completion versus perfection, evidence synthesis, honest residual risk, role-family fit, next-best investment.  
**Diagnostic / skip:** Walk every definition-of-done item and supply its artifact; any missing critical item is addressed before presentation material.  
**Resources:** `SPEC.md` definition of done; roadmap learning matrix; Manifold interview guide only for a final weak explanation—no new course.  
**Sasha attempts:** Run final gates, close/update status and evidence, finalize weekly/final notes tailored to the director, Igor and Prashant, and answer the six decision-review questions.  
**Outcome / files:** final status/evidence matrix, proof-package index, stakeholder notes, post-sprint decision record and prioritized next list.  
**Acceptance:** External run path works; reports/controls/demos are linked; remaining limitations are explicit; next learning/job step follows evidence rather than unfinished course lists.  
**Validation:** all README commands, tests, deterministic evaluation, adversarial suite, Docker/runbook checks, secret/link checks, and final definition-of-done audit.  
**Evidence:** Final release/commit, validation transcript, proof package, stakeholder messages, and November 3 review.  
**Non-goals:** Starting a second project, adding deferred technology, concealing incomplete items, or continuing without a retrospective.  
**Next smallest step:** Execute the chosen post-sprint action from the decision review.

## Weekly progress-note format

1. What I learned.
2. What I built, with one durable link.
3. What failed or changed because of evidence.
4. What I will prove next week.

For Igor, connect evidence to fundamentals. For the director, emphasize consistency and ownership. For Prashant, emphasize evaluation, identity/security, cost, and observability.

## Definition-of-done review questions

On November 3, answer with links:

1. Which skills moved from studied to built or operated?
2. What did evaluation reveal that a demo would have hidden?
3. Can an outsider run and assess the project?
4. Which role family now fits best: applied AI, AI platform, forward-deployed, solutions, or automation?
5. Is the next move deeper software fundamentals, cloud certification, deployment/platform work, applications, or a second project?
6. Which resource continues, and which is dropped?
