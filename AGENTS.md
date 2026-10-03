# Repository Working Agreement

This repository is both a learning environment and a portfolio project. Optimize for Sasha's understanding, defensible engineering decisions, and durable evidence—not feature count or course completion.

## Source of truth

Before every session, read, in order:

1. `docs/STATUS.md`
2. the current session card in `docs/SPRINT.md`
3. applicable accepted and pending records in `docs/DECISIONS.md`
4. the relevant entries in `docs/SOURCES.md`
5. through October 26, 2026, the local [October 26 readiness plan](docs/OCTOBER_26_READINESS.md), which controls call-critical sequencing, timeboxes, catch-up rules, and the protected review window

`docs/SPEC.md` defines product scope and the final definition of done. If a request conflicts with it, surface the conflict and record an explicit decision before changing scope.

## Required learning loop

For each scheduled session:

1. State the session objective and prerequisite concepts.
2. Give Sasha a short diagnostic or ask for an explanation from memory.
3. Skip lessons Sasha can already explain and apply.
4. When a gap exists, point to the exact section listed in `docs/SOURCES.md`; do not assign an entire course by default.
5. Let Sasha attempt the important implementation before supplying replacement code.
6. Review the attempt, explain concrete issues, and help Sasha correct it.
7. Run every validation command on the current card. Do not advance while required validation fails.
8. Update `docs/STATUS.md`, `docs/EVIDENCE.md`, and any affected decision record before ending.

Do not silently implement later session cards. Work only on the current card unless Sasha explicitly asks to continue. Through October 26, `Start the next session` authorizes the next incomplete **agent-architecture capstone session** identified by the readiness plan; FDE research and Riser exploration start only when Sasha names that track or reaches its calendar block. State any departure from numeric card order before work begins and preserve all applicable acceptance criteria.

## Scope guardrails

- One agent or explicit workflow before any multi-agent design.
- One approved public documentation corpus and one vector store.
- At most two bounded read-only tools and one draft-producing action tool.
- The action tool must require explicit human approval; prompts are not authorization controls.
- Python 3.12+, FastAPI, Pydantic typed models, pytest, uv, Docker, and a small model-provider interface are defaults.
- The hosted provider path comes first; an OpenAI-compatible local endpoint is a later interchangeable adapter.
- No Kubernetes, fine-tuning, elaborate frontend, or more than one provider/vector-store implementation during the sprint.
- No LangChain, MCP, Pinecone, or additional agent framework unless a recorded ADR identifies a requirement the existing design cannot satisfy.
- Prefer direct, readable code over speculative abstractions.
- Reduce features before reducing tests, evaluation, security work, or documentation.

## Security and cost

- Never commit credentials, tokens, private data, `.env`, or captured sensitive payloads. Document variables in `.env.example`.
- Use mocks, fakes, deterministic fixtures, or recorded controlled responses when a paid model call is unnecessary.
- Treat ingested documents and model outputs as untrusted input.
- Validate all tool arguments, enforce tool allowlists and authorization in code, cap steps and time, and fail closed.
- No external write may occur in the capstone. The action tool produces a draft only, after approval, and records an audit event.

## Validation and evidence

- A behavior is not complete until its tests and the current card's acceptance criteria pass.
- Record exact commands and outcomes in `docs/STATUS.md`; link durable results in `docs/EVIDENCE.md`.
- Evaluation results must identify the corpus version, evaluation-set version, provider/model configuration, and code revision.
- Every session must produce at least one durable artifact: commit, test, evaluation result, diagram, decision, explanation, demo, or failure analysis.
- Never claim an improvement without a comparable before/after evaluation.
- Keep the repository runnable from documented commands. If a command changes, update the README and session references in the same change.

## Documentation maintenance

- `docs/STATUS.md`: current session only, completed work, blockers, next action, and validation state.
- `docs/DECISIONS.md`: append or supersede ADRs; never erase the rationale of an accepted decision.
- `docs/EVIDENCE.md`: append dated evidence links; distinguish planned placeholders from produced artifacts.
- `docs/SOURCES.md`: record exact assigned sections and why they are used; do not add resource breadth casually.
- `README.md`: keep setup, current status, and navigation accurate.

## Git practice

- Make focused commits whose messages describe the evidence produced.
- Do not include a `Co-Authored-By: Codex` line.
- This directory was not a Git repository at bootstrap time. Initialize Git only when Sasha approves or begins Session 1, then replace evidence placeholders with commit links or hashes.
