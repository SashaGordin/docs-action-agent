# October 26 Stephen Anthony Readiness Plan

**Plan window:** October 2–26, 2026  
**Implementation freeze:** End of October 21  
**Protected review window:** October 22–25  
**Call:** October 26  
**Planned capacity through October 25:** 36 hours 45 minutes

This is the capstone-local source of truth for pre-call sequencing. `SPRINT.md` still defines the full six-week curriculum and acceptance criteria; this file decides which call-critical work comes next and what may be deferred until after October 26.

## Priority allocation

| Workstream | Planned time | Priority and required evidence |
|---|---:|---|
| Agent architecture, vocabulary, implementation, and agentic engineering | **26 hr 45 min** | **Primary.** Explain the complete system top-down, implement its important boundaries, evaluate it, break it safely, diagnose it, and defend the design. Preserve one worked agentic-development loop with human review and correction. |
| FDE research and practice | **5 hr** | Self-directed supporting track. Understand the role, working style, discovery process, customer/product responsibilities, and personal fit; finish a brief and discovery role-play. |
| Riser exploration | **5 hr** | Self-directed supporting track. Configure and test an agent, iterate once, and reduce firsthand observations to three useful observations and three questions. |
| Next.js, TypeScript, and SQL | **No dedicated study block** | Treat as established background. Reference prior experience accurately and explain at a high level how the capstone's boundaries translate if asked. Reopen only if a real gap appears during the work or conversation. |

The capstone is the technical proof and owns the agent-architecture learning. FDE research and Riser use are separate readiness tracks. They remain visible here for deadline coordination but should not displace the capstone's architecture sessions.

## Agent architecture learning map

The capstone must teach the subject top-down rather than as disconnected features. For each layer, Sasha should be able to **explain it from memory, build or inspect a concrete example, predict a failure, and verify or diagnose that failure**.

1. **Purpose and system boundary:** What user problem is being solved; why an agent is or is not justified; where deterministic workflow and human judgment remain safer.
2. **Model interaction:** Inference, messages/instructions, tokens, context windows, structured output, nondeterminism, provider boundaries, latency, usage, and cost.
3. **Agent control loop:** State, planning/reasoning boundaries, tool selection, tool-call schemas, validation, allowlists, maximum steps, timeouts, retries, terminal states, and infinite-loop prevention.
4. **Knowledge and grounding:** Instructions versus knowledge, ingestion, normalization, chunking, metadata, keyword/vector/hybrid retrieval, reranking, citations, abstention, and retrieval failure versus generation failure.
5. **Actions and human control:** Read tools versus action tools, authorization, explicit approval, audit events, idempotency, replay/change protection, and why prompts are not security controls.
6. **Memory and state:** Request context, conversation history, durable application state, what should not be remembered, and how state changes testing, privacy, and failure recovery. Implement only what this capstone needs.
7. **Evaluation:** Fixed cases, retrieval and answer criteria, tool-choice checks, regression thresholds, version/configuration provenance, and the limits of a single score.
8. **Production operation:** Structured diagnostics/traces, identity and permissions, secrets, untrusted documents/prompt injection, errors, retries, cost/latency, tenancy/isolation, deployment, recovery, and residual risk.
9. **Agentic software development:** Planning, reusable repository instructions/context, bounded delegation, code review, tests, verification loops, human accountability, and the difference between a prototype and maintainable software.
10. **Architecture communication:** Draw and narrate the full path from user problem through data, retrieval, model, tools, approval, output, evaluation, and monitoring; state tradeoffs and known limitations without jargon-dumping.

### Coverage map

| Architecture layer | Capstone coverage |
|---|---|
| Purpose and system boundary | Agent-versus-workflow decision, bounded product scope, and October 21 architecture review |
| Model interaction | Existing provider seam and typed output plus the controlled live interaction and usage/cost evidence |
| Agent control loop | Tool-contract, allowlist, explicit-loop, timeout, step-limit, failure, and trace sessions |
| Knowledge and grounding | Corpus contract, deterministic ingestion/chunking, keyword baseline, retrieval comparator, citations, and abstention |
| Actions and human control | Read-only tools followed by authorization and the approval-gated draft boundary |
| Memory and state | Explicit closed-notes explanation during recall/review; implement no durable conversational memory unless the scoped workflow actually requires it |
| Evaluation | Versioned cases, metrics, retrieval/answer/tool checks, and regression gate |
| Production operation | Correlated diagnostics, failure analysis, threat model, identity/authorization, prompt-injection tests, cost/latency, and conceptual tenancy/recovery review |
| Agentic software development | Repository instructions, session plans, bounded implementation attempts, review, tests, corrections, and evidence ledger throughout the sprint |
| Architecture communication | October 21 freeze review, October 23 closed-notes explanation, and October 24 mock defense |

No architecture layer is complete merely because its feature exists. Its session evidence must also include Sasha's explanation, a failure or limitation, and verification.

## Competency bar

The goal is not equal depth in every topic. For this exploratory FDE conversation, use three evidence levels:

| Area | Required level | Readiness test |
|---|---|---|
| Agent vocabulary and architecture | **Explain + Build** | Trace one agent from user problem through knowledge/retrieval, reasoning, tools, approval, output, evaluation, and monitoring; distinguish instructions from enforcement. |
| Bounded tool use and loops | **Build** | Demonstrate typed tool contracts, allowlist, validation, time/step limits, terminal states, and safe failures. |
| Retrieval and grounding | **Build** | Show versioned sources, a measured baseline, citations, abstention, and the difference between retrieval and generation failures. |
| Evaluation | **Build** | Explain the case set, metric, threshold/baseline, configuration, regression behavior, and at least one failure—not merely report a score. |
| Security and production architecture | **Build one boundary; explain the rest** | Demonstrate authorization or approval plus a correlated trace; explain secrets, identity versus permission, prompt injection, retries/idempotency, cost/latency, tenancy, and recovery tradeoffs. |
| Next.js/TypeScript/SQL | **Existing background; no new proof required** | Describe prior experience truthfully and give a high-level translation only if asked. Do not spend readiness time re-proving established skills absent an observed gap. |
| Agentic development | **Demonstrate a repeatable workflow** | Show plan, reusable instructions/context, bounded delegation, review, tests, a caught mistake, correction, and final verification; explain what remains human-owned. |
| FDE/customer discovery | **Apply in a role-play** | Ask before prescribing; uncover workflow, goals, data, constraints, stakeholders, risk, success measures, and adoption; translate evidence into hypotheses and product feedback. |
| Riser/product understanding | **Observe firsthand** | Configure one agent, run test cases, iterate once, and separate observed behavior from inference and feature suggestions. |

This is an FDE readiness bar, not a senior-software-architect bar. Sasha should show technical credibility and judgment without claiming production experience the evidence does not support.

## Session operating protocol

Sasha can begin work with:

> Start the next session.

The working agent must then:

1. Read `AGENTS.md`, `docs/STATUS.md`, this file, the applicable `SPRINT.md` card, relevant decisions, and relevant sources.
2. Select the next incomplete **agent-architecture capstone session**, not merely the next stale calendar date. FDE and Riser blocks are separate self-directed tracks unless Sasha explicitly starts one.
3. State the objective, prerequisite recall question, expected artifact, validation, and default timebox.
4. Follow the learning loop: Sasha attempts the important implementation before replacement code is supplied.
5. End by updating `STATUS.md` and `EVIDENCE.md` for code work, recording actual time and the daily score, and naming the next smallest step.

Sasha does not need to state available time when the default calendar/session timebox works. If it differs, use:

> Start the next session. I have 45 minutes.

Shrink the work to a safe, verified checkpoint. Do not mark the full session complete unless its acceptance criteria pass; unfinished work remains at the front of the queue.

## Daily completion rubric

A workday is complete at **4/5**. A score of **3/5 or below** is partial and the relevant gate remains open.

| Point | Completion test |
|---|---|
| Recall | Explain the scheduled concept before consulting notes. |
| Build/observe | Change a working artifact or capture a firsthand Riser observation. |
| Verify | Support the result with a test, evaluation, reproduction, or concrete comparison. |
| Explain | State why it matters and name one limitation. |
| Record | Write down the artifact, result, failure/confusion, actual time, and next step. |

Watching or reading material without recall, application, or evidence earns only the Recall point.

## Catch-up and progress rules

- As of October 2, Session 5 is complete. The original calendar expected Session 10, a five-session or 5-hour-5-minute backlog.
- The revised calendar below absorbs the backlog. Do not add five separate make-up sessions.
- Never skip a failed gate merely to match a date.
- Combine adjacent short cards only when both sets of acceptance criteria are checked explicitly.
- Remove a **Could**, then a **Should**, before reducing a **Must**.
- Never consume October 22–25 with new feature work.
- Reforecast each Sunday using actual hours, completed gates, and estimated remaining hours—not raw session count.

Track after every session:

1. Actual hours this week versus planned hours.
2. Call-critical gates complete versus remaining.
3. Estimated hours remaining through the October 21 freeze.
4. Schedule variance: estimated remaining hours minus remaining planned capacity.

Positive variance requires more time or a scope cut. Zero or negative variance is on track.

## Capacity forecast

| Calendar week | Planned time | Purpose |
|---|---:|---|
| Oct 2–4 | 5 hr 30 min | 3 hr 30 min capstone recovery; 2 hr Riser exploration |
| Oct 5–11 | 9 hr 45 min | 9 hr 15 min agent architecture; 30 min FDE orientation |
| Oct 12–18 | 10 hr 45 min | 7 hr 45 min agent architecture; 1 hr FDE research; 2 hr Riser testing |
| Oct 19–25 | 10 hr 45 min | Architecture freeze/review plus 3 hr 30 min FDE practice and 1 hr Riser synthesis |
| **Total** | **36 hr 45 min** | **26 hr 45 min agent architecture; 5 hr FDE; 5 hr Riser** |

The schedule returns to its revised track after the October 10 gate if the foundation, two tools, bounded loop, and agentic-development evidence are complete.

## Call-critical capstone scope

### Must be ready by October 21

1. Reproducible local start, tests, container baseline, and request-path explanation.
2. Two bounded read-only tools with allowlist, validation, timeout/step limits, and an explicit agent-versus-workflow decision.
3. Pinned corpus, deterministic ingestion/chunking, versioned evaluation cases, measured retrieval, citations, and abstention.
4. One repeatable evaluation result with a named metric and configuration.
5. One deterministic safety boundary. Prefer the approval-gated draft path; if it cannot be completed correctly, demonstrate authorization/denial and label approval unfinished.
6. One request-correlated diagnostic record showing the relevant retrieval, provider/model, tool, latency, result/error, and usage/cost fields without secrets or uncontrolled content.
7. One failure diagnosed from tests or telemetry and explained as a design lesson.
8. One controlled live model/tool interaction when credentials and bounded cost are available; otherwise document the limitation and use Riser to observe live model behavior.
9. One closed-notes top-down architecture explanation covering all ten layers in the learning map at the appropriate implemented-versus-conceptual depth.

### Defer after October 26 when necessary

- Local-model compatibility probe.
- Full CI and hosted deployment.
- Broad observability/dashboard work beyond the minimum correlated diagnostic record used for the showcased diagnosis.
- External reviewer sessions, caching, model routing, and multi-tenancy implementation.
- Portfolio polish, final case study, and the complete November 3 release package.

This changes sequencing, not the final definition of done in `SPEC.md`.

## Calendar and completion queue

These blocks are also on the connected Google Calendar. Exact dates guide capacity; the next incomplete gate controls the session.

| Date | Time | Outcome | Completion condition |
|---|---:|---|---|
| Fri Oct 2 | 30 min | Rebaseline | Confirm status/backlog and explain the current request path. |
| Sat Oct 3 | 3 hr | Week 1 gate | Finish container/threat baseline; verify tests, startup, and architecture explanation. |
| Sun Oct 4 | 2 hr | Riser exploration 1 | Complete onboarding, configure a first bounded agent from public material, and record observations under worked, confused, customer need, and possible gap. |
| Mon Oct 5 | 30 min | FDE orientation | Define the role, distinguish it from software engineering, solutions engineering, account work, and product management, and start a role-and-fit research note. |
| Tue Oct 6 | 75 min | Agent/workflow design | Classify deterministic/model steps and define tools, limits, timeout, and terminal states. |
| Wed Oct 7 | 90 min | First read-only tool | Implement and test one bounded typed tool. |
| Thu Oct 8 | 90 min | Second tool and allowlist | Implement tool two and prove unknown/unauthorized calls fail closed. |
| Fri Oct 9 | 30 min | Recall checkpoint | Explain tools, tokens/context, loops, validation, and deterministic boundaries without notes. |
| Sat Oct 10 | 3 hr | Explicit tool loop | Complete the validated loop, preserve plan/reusable-context/review/correction evidence, and run one controlled live interaction if configured. |
| Sun Oct 11 | 90 min | Corpus contract | Pin the corpus and define paths, metadata, attribution, IDs, and reproducible inputs. |
| Mon Oct 12 | 1 hr | FDE research | Study representative responsibilities, working style, customer/engineering interface, success measures, common strengths, and likely personal fit/gaps. Record sources and conclusions rather than collecting job descriptions. |
| Tue Oct 13 | 75 min | Ingestion and eval set | Produce deterministic chunks and answerable, misleading, and unanswerable cases. |
| Wed Oct 14 | 90 min | Keyword baseline | Run a reproducible metric and record three categorized failures. |
| Thu Oct 15 | 90 min | Retrieval comparator | Compare one alternative retrieval configuration against the same cases and explain why measured retrieval choices matter to the complete agent architecture. |
| Fri Oct 16 | 30 min | Citation/abstention contract | Test evidence-linked answers and insufficient-evidence behavior. |
| Sat Oct 17 | 3 hr | Measured RAG slice | Integrate retrieval/citations/abstention and record metric, cost/latency if available, and a failure. |
| Sun Oct 18 | 2 hr | Riser exploration 2 | Test the Riser agent with planned successful, ambiguous, and unsupported cases; iterate once; classify findings as onboarding, configuration, or possible product-capability hypotheses. |
| Mon Oct 19 | 90 min | FDE workflow and discovery brief | Synthesize role research and fill user, workflow, pain, data, constraints, stakeholders, actions, risks, approval, success measures, adoption questions, and possible gaps. |
| Tue Oct 20 | 75 min | Evaluation, safety, and diagnosis | Add the regression check and authorization/approval boundary, prove one bypass fails, and capture the minimum correlated diagnostic trace. |
| Wed Oct 21 | 90 min | Implementation freeze | Run the call-critical gate, fix only a critical issue, record limitations, and freeze features. |
| Thu Oct 22 | 90 min | Riser synthesis + package proof | Spend 60 minutes reducing firsthand Riser work to three observations and three questions, then verify the capstone demo and FDE brief claims. |
| Fri Oct 23 | 30 min | Closed-notes architecture review | Explain the ten-layer agent architecture top-down, including production tradeoffs—identity, permissions, observability, cost, retries, and tenancy. Review only missed concepts. |
| Sat Oct 24 | 3 hr | Architecture mock + FDE discovery role-play | Spend about one hour defending the agent architecture and two hours rehearsing the call/FDE role, including a discovery scenario scored on workflow, data, constraints, risk, stakeholders, value, and next steps before proposing an agent. |
| Sun Oct 25 | 90 min max | Final readiness | Run demo once, verify logistics, select questions, review limitations, and stop. |

## October 21 go/no-go gate

### Must

- Documented capstone start path and relevant tests pass.
- Sasha can draw and explain request, retrieval, tool, and approval boundaries.
- A versioned evaluation produces at least one named metric.
- Demo includes one useful result and one honest failure, abstention, or denial.
- One request can be followed through a safe correlated diagnostic record and one failure can be localized from it.
- The agentic-development example includes reusable instructions/context, review, a caught issue, correction, and verification—not merely AI-generated code.
- The closed-notes top-down explanation covers all ten agent-architecture layers and clearly separates implemented behavior from conceptual production considerations.
- Riser was used firsthand; observations are separated from inferences.
- FDE discovery brief identifies a specific user/problem and open questions.
- A discovery role-play demonstrates question-first behavior and connects the proposed solution to measurable customer value.
- Three Riser observations and three call questions are selected.

### Should

- Approval-gated draft behavior is fully implemented and tested.
- Retrieval comparison includes keyword and vector/hybrid approaches.

### Could

- CI, hosted deployment, local-model probe, external review, and polished case study.

If a Must is false on October 21, narrow the demo to the strongest truthful slice and record the limitation. Do not add architecture during the review window.

## Final call package

1. Runnable capstone and three-to-five-minute walkthrough.
2. One-page pre-development/FDE discovery brief.
3. One-page Riser observation sheet: three observations and three questions.
4. Two-minute career/project story covering fit, measured evidence, failure, learning, and relevant prior web-stack experience.

This is evidence for a conversation, not five documents to present unprompted.

## Daily log template

```text
Date / planned time / actual time:
Today's workstream and agent-architecture layer:
Recall before notes:
Artifact or observation produced:
Verification and result:
What I can now explain:
Failure, uncertainty, or limitation:
Score (Recall / Build-observe / Verify / Explain / Record): __ / 5
Actual hours this week / planned hours:
Call-critical gates complete / remaining:
Estimated remaining hours / planned capacity remaining:
Next smallest step:
```
