# Learning Baseline Matrix

**Baseline date:** 2026-09-23  
**Session:** Session 1 — Baseline and corpus decision  
**Method:** Sasha explained each area from memory, revised the request path after feedback, and supplied experience/gap notes. States are self-assessment normalized against the Session 1 definitions and may be revised by later implementation evidence.

## State definitions

- **Explain:** Can explain the purpose and recognize examples; implementation practice is still needed.
- **Build:** Can implement a small version with ordinary references and troubleshoot it locally.
- **Operate:** Can configure, diagnose, maintain, and recover it in a running environment.
- **Defer:** Intentionally postponed until its scheduled session or excluded from the sprint.

## Application foundations

| Area | Baseline state | Evidence and current gap | Scheduled response |
|---|---|---|---|
| Python environments and dependency management | Explain | Understands isolation and dependency consistency at a basic level; initially conflated the virtual environment with `requirements.txt`. Needs practice with Python-version selection, `pyproject.toml`, lockfiles, and `uv`. | Session 2 hands-on work; use the Python foundations resource only if blocked. |
| Git | Build | Several years of practical collaborative use: branches, staging, commits, pushes, forks, and pull requests. Needs a clearer model of trunk-based versus long-lived development branches and release/deployment workflows. | Use Git directly throughout the sprint; no introductory lesson assigned. |
| HTTP and APIs | Build | Has substantial API implementation experience and identified malformed requests and rate limiting as failures. Initially described the response as another POST request; refine request/response semantics and backend/provider boundaries. | Recheck at the typed boundary in Sessions 3 and 5; consult the Full Stack API node only for the observed terminology gap. |
| JSON and schema validation | Build | Correctly distinguishes JSON syntax from typed/constraint validation and has applied schemas in TypeScript. Needs transfer practice with Pydantic and model-output validation. | Sessions 3–5 implementation. |
| Unit and integration testing | Explain | Correctly explained isolated unit behavior and multi-component integration behavior. Can write simple unit tests but lacks confidence with integration boundaries, fixtures, fakes, and mocking choices. | Session 2 test harness and Sessions 4–5 fake/provider/API tests; use the assigned maintainability section only if blocked. |
| Runtime configuration and secrets | Explain | Has used environment variables and knows secrets must not reach frontend code or logs. Needs to distinguish local `.env` loading from runtime injection, production secret management, validation, and non-secret configuration. | Sessions 4 and 6 implementation. |
| Persistence and databases | Build | Reports substantial schema design, data manipulation, and query experience. | Apply to the single-store design when scheduled; skip database fundamentals. |
| Authentication and authorization | Explain | Has used third-party authentication and recently studied JWT basics; has not independently built authorization enforcement. | Sessions 24–27; preserve the identity-versus-permission distinction. |
| Docker | Build (provisional) | Has used Docker and can explain containers and their purpose. Dockerfile construction, runtime configuration, and secret exclusion still need direct evidence. | Validate through the Session 6 container task. |
| CI/CD | Explain | Understands its purpose but has little implementation experience. | Sessions 29–31. |
| Monitoring and observability | Explain | Can explain the use cases but has little experience implementing telemetry or diagnostic workflows. | Sessions 22–23 and 29–33. |
| Application deployment | Build (managed platforms) | Has deployed applications using Vercel and other managed providers. Needs deeper evidence for release artifacts, runtime configuration, rollback, health, and operational recovery. | Sessions 29–34. |

## AI engineering

| Area | Baseline state | Evidence and current gap | Scheduled response |
|---|---|---|---|
| LLMs and inference | Explain | Understands pretraining at a high level and inference as generation from an already-trained model, commonly through next-token prediction. Deeper mechanics are not currently required. | Recheck during provider work in Session 4. |
| Model-provider APIs | Explain | Understands why an application calls a model API rather than a chat product. Has little direct implementation experience and initially lacked a clear provider-adapter boundary. | Microsoft Lessons 01–03 model/API portions and Session 4 implementation; use the assigned OpenAI API sections only if the attempt exposes a gap. |
| Tokens, context, and prompting | Explain | Correctly described tokenized text, context inputs, and prompting at a high level. Needed correction that tokens do not inherently measure speed and that conversation history is context only when supplied to a call. | Apply during Sessions 4 and 18; no broad prompt-engineering course. |
| Structured model outputs | Explain | Understands declaring an expected output shape but has little direct experience enforcing and validating it. | Sessions 3–4 typed schema and fake-provider work. |
| Agents and tool calling | Build (partial) | Classified deterministic validation/retrieval, model generation, and model-selected tool behavior; implemented one bounded read-only tool with strict arguments/results, deterministic execution, safe errors, and focused tests. The second tool, allowlist, and explicit model/tool loop remain pending. | Sessions 10–14 add the second tool, executable allowlist, and bounded loop using the assigned Tool Use material. |
| Embeddings, vector search, and RAG | Defer | Essentially new; only a very high-level recognition of RAG. | Sessions 15–21 after the keyword baseline and fixed evaluation set. |
| Local models | Defer | Can explain local execution and named Hugging Face/Ollama as examples, but has not established implementation or operational depth. | Optional bounded experiment in Session 13; hosted provider remains first. |
| AI evaluation | Defer | No current conceptual or implementation baseline. | Sessions 17–25, beginning with explicit cases and metrics rather than a broad course. |
| Prompt-injection defenses | Defer | No current conceptual or implementation baseline. | Sessions 24–27 after deterministic tool and authorization boundaries exist. |

## Request-path explanation evidence

Sasha's revised explanation identified a client request entering the backend API, deterministic forwarding logic toward a model provider, nondeterministic model generation, and a structured-output failure when the returned shape is unexpected. Sasha also identified malformed/oversized input, rate limiting, authentication or quota failure, and provider-output mismatch as boundary failures.

The review exposed two targeted gaps to test in code rather than cover through broad study:

1. The backend must validate and transform the client request into a provider-specific request rather than blindly forward the original payload.
2. Model generation may be nondeterministic, while schema validation and mapping the provider result into the declared HTTP response remain deterministic application behavior.

## Corpus decision

FastAPI English documentation is provisionally selected. Full approval and ingestion remain blocked until an immutable upstream tag or commit, bounded path allowlist, exclusions, MIT attribution, and durable source-URL rule are reviewed and recorded. Target resolution: no later than 2026-10-06, before Session 15 ingestion work begins.
