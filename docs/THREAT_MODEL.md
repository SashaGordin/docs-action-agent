# Threat Model

## Status and scope

This is the Session 6 baseline, not a complete production threat model. It covers
the current typed FastAPI boundary, deterministic fake provider, environment-based
settings, and local container image. Retrieval, live model calls, tools,
authorization, approval, and external writes do not exist yet and must extend this
model when introduced.

## Baseline assumptions

- HTTP input, future ingested documents, and future model output are untrusted.
- Text is data unless an application component explicitly interprets or executes it.
- A typed structure constrains shape; it does not establish truth, relevance, or safety.
- Credentials are supplied at runtime and must not enter source control or image layers.
- `GET /health` proves HTTP liveness only, not provider or workflow readiness.
- The current provider is deterministic and performs no network or external write.

## Initial threats and controls

| Boundary | Protected asset | Threat | Current control and evidence | Residual limitation |
|---|---|---|---|---|
| Untrusted user input | Service availability and application integrity | Missing, malformed, blank, oversized, or adversarial question content could trigger errors, consume resources, or later manipulate model/tool behavior. Text that resembles code becomes dangerous only if a later component interprets or executes it. | `QuestionRequest` requires a string, strips surrounding whitespace, rejects missing/empty values, and returns `422` before provider execution. Model and API tests cover those cases. | No maximum request/question length, rate limit, content policy, prompt-injection control, or tool boundary exists yet. A syntactically valid string remains untrusted. |
| Untrusted model output | Reliable response handling and future action/approval boundaries | Generated content may be false, irrelevant, adversarial, or unsuitable for downstream use even when its structure is valid. | `ProviderResult` and `QuestionResponse` constrain response shape and allowed status values. The current fake provider is deterministic, and no action tool or external write exists. | The answer itself is an unconstrained string. Typed output does not prove correctness or safety; grounding, citations, abstention, content checks, and approval enforcement remain future work. |
| Credentials | Confidentiality of provider credentials and related configuration | A credential could leak through Git history, image layers/build context, logs, error responses, or operator mistakes. | `.env` is excluded by both `.gitignore` and `.dockerignore`; the image copies only declared project files; `.env.example` contains empty placeholders; settings represent the key with `SecretStr`; unexpected HTTP failures return a generic response. | Runtime environment values may still be exposed through process/container inspection, unsafe logging, debugging, or host compromise. No production secret manager or credential rotation procedure exists yet. |

## Container boundary

The image contains the Python runtime, a pinned uv executable, locked runtime
dependencies, and application source. It excludes the host virtual environment,
credentials, Git history, tests, documentation, and local caches. The container
starts noninteractively with Uvicorn bound to `0.0.0.0:8000`; Docker checks liveness
inside the container through `http://127.0.0.1:8000/health`.

## Next review triggers

Update this file when a live provider, corpus ingestion, retrieval, a tool loop,
authorization, approval, telemetry, or deployment is added. Each material boundary
must eventually name its control, verification evidence, and remaining risk.
