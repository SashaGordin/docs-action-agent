# Bounded Agent Loop

**Status:** Design accepted; implementation begins with the first read-only tool contract
**Date:** 2026-10-03

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
Model receives instructions and the two allowed tool schemas
        |
        +---- typed final answer with adequate evidence ----> grounded answer
        |
        +---- typed insufficient-evidence result ----------> safe abstention
        |
        `---- proposed tool call
                    |
                    v
          Check overall deadline and iteration budget
          Check the tool allowlist
          Validate typed arguments
          Check deterministic authorization/approval policy
                    |
                    v
          Execute with the per-tool timeout
                    |
                    v
          Validate the typed tool result
                    |
                    v
          Append the result to context and repeat
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
| Transient retries | At most 1; it consumes the applicable call and iteration budgets |

The tool-call limit counts executions, not unique tool names. A tool can be called
more than once with different arguments, and a retry counts as another call.

## Terminal and retry policy

Successful terminal states are a typed grounded answer with citations and a typed
safe abstention when the available evidence is insufficient.

Stop immediately for an unknown or unauthorized tool, an invalid result from trusted
tool code, an exhausted call/iteration budget, or an exhausted overall deadline.
A malformed model-proposed argument may receive one typed validation response so the
model can correct it, provided budgets remain. A genuinely transient tool or provider
failure may be retried once when time remains. Valid but unhelpful evidence is not a
retry failure; the model may choose another allowed call within the same budgets.

## Operation ownership

| Operation | Owner |
|---|---|
| Reject a blank question | Deterministic application validation |
| Choose evidence search or known-source lookup | Model-selected tool request |
| Rank chunks for a validated query | Deterministic retrieval code |
| Compose a cited response from evidence | Model generation |
| Decide whether an approval-gated operation may execute | Deterministic application policy |
