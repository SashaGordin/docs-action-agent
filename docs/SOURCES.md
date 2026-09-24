# Learning and Source Map

The capstone is the primary curriculum. Use these resources only where a session card assigns an exact section. If Sasha passes the diagnostic, skip the resource and build. URLs and syllabus fit were reviewed on 2026-09-22.

## Resource roles and assignments

### Roadmap.sh checklists

- [AI Engineer roadmap](https://roadmap.sh/ai-engineer) and [PDF](https://roadmap.sh/pdfs/roadmaps/ai-engineer.pdf): Session 1 gap matrix; revisit only the current week's nodes for model APIs, structured outputs, agents/tools, embeddings/vector search/RAG, local models, evaluation, and prompt-injection defenses.
- [Full Stack Developer roadmap](https://roadmap.sh/full-stack) and [PDF](https://roadmap.sh/pdfs/roadmaps/full-stack.pdf): Session 1 gap matrix; revisit API, testing, Git, persistence, authentication, Docker, CI/CD, monitoring, and deployment nodes when scheduled.
- The previously supplied `roadmap.sh/ai/full-stack-developer` URL returned 404 and is not a source.

### Microsoft AI Agents for Beginners

Repository: [microsoft/ai-agents-for-beginners](https://github.com/microsoft/ai-agents-for-beginners)

| Exact section | Scheduled use |
|---|---|
| `00-course-setup` README and Lessons 01–03 READMEs | Sessions 1–5: vocabulary, use cases, framework trade-offs, design patterns, model/API concepts; concepts only where Azure setup is unnecessary |
| Lesson 04, Tool Use Design Pattern | Sessions 8–11: tool schemas, calling loop, errors, bounded tools |
| Lesson 05, Agentic RAG | Sessions 15–20: retrieval/RAG concepts, citations, grounding |
| Lesson 06, Building Trustworthy AI Agents | Sessions 9, 22–27: trust boundaries, failures, untrusted content |
| Lesson 10, AI Agents in Production | Sessions 22–25: traces, latency, cost, errors, feedback, offline/online evaluation |
| Lesson 12, Context Engineering | Session 18 and optional retrieval debugging: evidence/context construction |
| Lesson 16, Deploying Scalable Agents — only lifecycle, versioning, routing/caching, evaluation gates, approval, safe tool-operation sections | Sessions 29–34: reliability and operations; no Azure deployment requirement |
| Lesson 17, Creating Local AI Agents — trade-off and requirements sections | Sessions 8 and 13: bounded local-model suitability; implementation optional |
| Lesson 18, Securing AI Agents — auditability/receipts concepts only | Sessions 24–27: audit trail concepts, not the full cryptographic implementation |

### DataCamp Associate AI Engineer for Developers

Track: [Associate AI Engineer for Developers](https://www.datacamp.com/tracks/associate-ai-engineer-for-developers). Use only if the diagnostic shows a gap and reapply it to the capstone within the same or next session.

| Exact course section | Scheduled use |
|---|---|
| `Working with the OpenAI API` — authenticated request, roles/parameters, response handling, tokens/cost, conversation context | Sessions 2–4 only if the API diagnostic fails; maximum three hours replacing, not adding to, other study |
| `Software Engineering Principles in Python`, Chapter 4 `Maintainability` | Sessions 2–6 only if package structure, docstrings, readability, or pytest is blocking |
| `Working with the OpenAI Responses API`, Chapter 2; Chapter 3 structured-output portion | Sessions 9–11 for function calling and structured JSON if guided practice is needed; skip streaming/multimodality |
| `Introduction to Embeddings with the OpenAI API` — semantic similarity/search, metadata/filtering, ChromaDB sections | Sessions 16–19 as a first embedding lab; does not replace keyword baseline or evaluation |
| `LLMOps Concepts` — Development and Operational chapters | Session 22, one hour maximum, as an evaluation/operations checklist |

Defer the full prompt-engineering course, Pinecone, LangChain, MCP, Hugging Face, bonus projects, and certification until a recorded requirement or the post-sprint review.

### Jam With AI — Production Agentic RAG Course

Repository: [jamwithai/production-agentic-rag-course](https://github.com/jamwithai/production-agentic-rag-course)

| Exact course area | Scheduled use |
|---|---|
| Week 1 — FastAPI/Docker health-check and service-boundary patterns only | Sessions 5–6 and 29–31 |
| Week 2 — ingestion retries, PDF/metadata patterns (adapt concepts to Markdown/HTML; no Airflow) | Sessions 15–16 |
| Week 3 — BM25, mappings/query concepts, filtering, relevance metrics | Sessions 16–18 |
| Week 4 — section-aware chunking, embeddings, hybrid retrieval/RRF | Sessions 18–20 |
| Week 5 — local generation/API patterns only | Optional Session 13; no Gradio requirement |
| Week 6 — tracing, caching, latency/cost monitoring | Sessions 23, 29–33 |

Defer Airflow, OpenSearch service sprawl unless justified, Redis unless measured, LangGraph, Gradio, Telegram, and the full seven-week topology.

### Manifold AI Learning

Channel: [Manifold AI Learning](https://www.youtube.com/@ManifoldAILearning). Watch after implementation and produce a two-minute explanation; passive viewing is not session evidence.

| Exact video | Scheduled use |
|---|---|
| [Python Programming Foundations](https://www.youtube.com/watch?v=HMrYZ1yHESQ) | Session 1–2 only if Python diagnostic fails |
| [LLM API: What to Learn](https://www.youtube.com/watch?v=LV9acAcHQFo) | Session 4 explanation check if API/model concepts are weak |
| [Building Blocks of Agentic AI](https://www.youtube.com/watch?v=K471DBTQ3Eg) | Session 14 retrospective explanation |
| [A Prompt Is Not a Security Control](https://www.youtube.com/watch?v=Q2coo-yOvEc) | Session 27 after security controls exist |
| [AI Architecture Is Not a Diagram](https://www.youtube.com/watch?v=5wbQdeTq6Fw) | Session 36 or 38 while revising the architecture narrative |
| [The Forward Deployed AI Engineer Guide](https://www.youtube.com/watch?v=pq3MvOB-u6A) | Session 37 or 40 for stakeholder/project framing |
| [Five Portfolio Artifacts](https://www.youtube.com/watch?v=IXCt89c-Zqs) | Session 40 for evidence-package review |
| [AI Interview Preparation Roadmap](https://www.youtube.com/watch?v=qEsJ9KEwPoY) | Sessions 39–41 for capstone-grounded rehearsal |

## Corpus candidate primary sources

- [FastAPI repository and MIT license](https://github.com/fastapi/fastapi), with source documentation under `docs/` and published docs at [fastapi.tiangolo.com](https://fastapi.tiangolo.com/).
- [pytest repository](https://github.com/pytest-dev/pytest), whose project metadata declares MIT licensing and whose authored documentation is under `doc/`.
- [uv repository](https://github.com/astral-sh/uv), with Markdown under `docs/` and dual [MIT](https://github.com/astral-sh/uv/blob/main/LICENSE-MIT) / [Apache-2.0](https://github.com/astral-sh/uv/blob/main/LICENSE-APACHE) licensing.

Selection remains pending in ADR-003. Pin a tag/commit, paths, and attribution before ingestion.
