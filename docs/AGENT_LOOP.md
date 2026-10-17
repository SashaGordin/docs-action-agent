# Bounded Agent Loop

**Status:** Implemented and verified with deterministic scripted scenarios
**Date:** Designed 2026-10-03; implementation verified 2026-10-16

## Why the model selects tools

The workflow answers questions over a bounded documentation corpus. Some questions
need a broad evidence search, while others refer to a source that is already known.
Always running a fixed `search -> lookup` sequence would make unnecessary calls.
The model may therefore choose between two narrow read-only tools.

This flexibility creates another error boundary. Tool selection is nondeterministic,
harder to test and diagnose than fixed routing, and increases the attack surface.
The application retains deterministic control of schemas, the allowlist,
authorization, budgets, execution, and terminal states.

## Allowed tools

| Tool | Purpose | Boundary |
|---|---|---|
| `evidence_search` | Discover ranked documentation chunks for a validated query | Read-only; bounded query and result count |
| `source_lookup` | Retrieve a known source or chunk with citation metadata | Read-only; validated source identifier |

Input validation, authorization, approval, and timeout enforcement are application
controls. They are not tools the model may select.

## Control loop

```text
Validated user question
        |
        v
Start overall deadline
        |
        v
Check iteration budget -> exhausted -----------------------> typed loop failure
        |
        v
Call provider with timeout -> timed out --------------------> typed loop failure
        |
        +---- typed final answer ---------------------------> grounded answer
        |
        +---- typed abstention -----------------------------> safe abstention
        |
        `---- typed tool request
                    |
                    v
          Reject identical repeat or exhausted tool budget
                    |
                    v
          Dispatch through the two-tool allowlist
          and execute with per-tool timeout
                    |
                    +---- unknown tool ---------------------> typed denial
                    +---- invalid trusted result ----------> typed loop failure
                    +---- second invalid-argument result ---> typed loop failure
                    |
                    v
          Append validated result to context and repeat

The overall deadline may terminate any nonterminal path above.
```

The model proposes a tool request. It never receives direct authority to execute
code or relax an application control.

## Initial budgets

| Control | Initial value |
|---|---:|
| Maximum tool calls | 3 |
| Maximum agent iterations | 4 |
| Per-tool timeout | 5 seconds |
| Per-model-call timeout | 45 seconds |
| Overall request deadline | 2 minutes |
| Invalid-argument corrections | 1; the corrected request consumes normal budgets |
| Transient retries | 0 in the current implementation; the accepted design permits at most 1 later |

The tool-call limit counts executions, not unique tool names. A tool can be called
more than once with different arguments, and a retry counts as another call.

## Terminal and retry policy

Successful terminal states are a typed grounded answer with citations and a typed
safe abstention when the available evidence is insufficient.

Stop immediately for an unknown or unauthorized tool, an invalid result from trusted
tool code, an exhausted call/iteration budget, or an exhausted overall deadline.
A malformed model-proposed argument may receive one typed validation response so the
model can correct it, provided budgets remain. A second malformed request fails. The
current implementation does not retry transient tool or provider failures; adding the
single retry allowed by ADR-007 is deferred until a real provider supplies a typed,
demonstrably transient failure. Valid but unhelpful evidence is not a retry failure;
the model may choose another allowed call within the same budgets.

## Verified scenarios

| Scenario | Expected terminal behavior | Result |
|---|---|---|
| Provider returns a final answer immediately | Return the typed answer | Pass |
| Provider returns an abstention immediately | Return the typed abstention | Pass |
| One tool request, then answer | Execute once and return the answer | Pass |
| Search followed by lookup, then answer | Execute both distinct requests | Pass |
| Identical tool request repeated | `repeated_tool_call` | Pass |
| Tool-call budget exhausted | `tool_call_limit_exceeded` | Pass |
| Iteration budget exhausted | `iteration_limit_exceeded` | Pass |
| Unknown tool requested | `tool_not_allowed` | Pass |
| One malformed argument request is corrected | Return validation result to provider and continue | Pass |
| Second malformed argument request | `argument_correction_limit_exceeded` | Pass |
| Tool exceeds its timeout | `tool_timeout` | Pass |
| Provider exceeds its timeout | `model_timeout` | Pass |
| Overall deadline expires | `overall_timeout` | Pass |
| Trusted executor returns an unknown result type | `invalid_tool_result` | Pass |
| Blank final answer or abstention reason | Pydantic validation rejects construction | Pass |

The focused command `uv run pytest -q tests/test_agent_loop.py` returned 16 passing
tests on 2026-10-16. The full suite returned 80 passing tests.

## Current limitations

- `ScriptedAgentProvider` proves loop control deterministically; no hosted provider
  adapter currently converts live model output into `AgentAction` values.
- The loop is not yet connected to the public `/questions` route.
- The tools still query three hand-authored fixtures, not the pinned corpus or a
  measured retrieval index.
- The presence and shape of citations are validated, but evidence support and citation
  adequacy are not yet evaluated.
- `execute_tool_async` uses `asyncio.to_thread`. A timeout stops waiting for the result,
  but Python cannot forcibly stop synchronous work already running in that thread.
- No transient retry is implemented. Retry classification must be evidence-driven and
  must consume the existing budgets when added.

## Operation ownership

| Operation | Owner |
|---|---|
| Reject a blank question | Deterministic application validation |
| Choose evidence search or known-source lookup | Model-selected tool request |
| Rank chunks for a validated query | Deterministic retrieval code |
| Compose a cited response from evidence | Model generation |
| Decide whether an approval-gated operation may execute | Deterministic application policy |
