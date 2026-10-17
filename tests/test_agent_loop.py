import asyncio

from docs_action_agent.provider import ScriptedAgentProvider
from docs_action_agent.agent_loop import (
    run_agent,
    FinalAnswer,
    LoopLimits,
    ToolRequest,
    AgentLoopError,
    ToolError,
    AgentAction,
    ToolExecutionResult,
)
from docs_action_agent.tools import execute_tool_async


def test_run_agent_returns_immediate_final_answer() -> None:
    expected = FinalAnswer(
        kind="final_answer",
        answer="FastAPI validates request bodies using Pydantic.",
        citations=[],
    )
    agent_provider = ScriptedAgentProvider(outcomes=[expected])
    limits = LoopLimits()
    result = asyncio.run(
        run_agent(
            question="How does FastAPI validate request bodies?",
            provider=agent_provider,
            tool_executor=execute_tool_async,
            limits=limits,
        )
    )
    assert isinstance(result, FinalAnswer)
    assert result.answer == "FastAPI validates request bodies using Pydantic."


def test_run_agent_executes_tool_request_then_returns_final_answer() -> None:
    outcomes = []
    answer = FinalAnswer(
        kind="final_answer",
        answer="FastAPI validates request bodies using Pydantic.",
        citations=[],
    )
    tool_call = ToolRequest(
        kind="tool_request",
        tool_name="evidence_search",
        raw_arguments={"query": "FastAPI", "result_limit": 3},
    )

    outcomes.append(tool_call)
    outcomes.append(answer)

    agent_provider = ScriptedAgentProvider(outcomes=outcomes)
    limits = LoopLimits()
    result = asyncio.run(
        run_agent(
            question="How does FastAPI validate request bodies?",
            provider=agent_provider,
            tool_executor=execute_tool_async,
            limits=limits,
        )
    )
    assert isinstance(result, FinalAnswer)
    assert result.answer == "FastAPI validates request bodies using Pydantic."


def test_run_agent_handles_multiple_tool_requests_before_final_answer() -> None:
    outcomes = []
    answer = FinalAnswer(
        kind="final_answer",
        answer="FastAPI validates request bodies using Pydantic.",
        citations=[],
    )
    evidence_search_tool_call = ToolRequest(
        kind="tool_request",
        tool_name="evidence_search",
        raw_arguments={"query": "FastAPI", "result_limit": 3},
    )

    source_lookup_tool_call = ToolRequest(
        kind="tool_request",
        tool_name="source_lookup",
        raw_arguments={"chunk_id": "request-body-001"},
    )

    outcomes.append(evidence_search_tool_call)
    outcomes.append(source_lookup_tool_call)
    outcomes.append(answer)

    agent_provider = ScriptedAgentProvider(outcomes=outcomes)
    limits = LoopLimits()
    result = asyncio.run(
        run_agent(
            question="How does FastAPI validate request bodies?",
            provider=agent_provider,
            tool_executor=execute_tool_async,
            limits=limits,
        )
    )
    assert isinstance(result, FinalAnswer)
    assert result.answer == "FastAPI validates request bodies using Pydantic."


def test_run_agent_rejects_identical_repeated_tool_request() -> None:
    outcomes = []

    evidence_search_tool_call = ToolRequest(
        kind="tool_request",
        tool_name="evidence_search",
        raw_arguments={"query": "FastAPI", "result_limit": 3},
    )
    duplicate_evidence_search_tool_call = ToolRequest(
        kind="tool_request",
        tool_name="evidence_search",
        raw_arguments={"query": "FastAPI", "result_limit": 3},
    )
    answer = FinalAnswer(
        kind="final_answer",
        answer="FastAPI validates request bodies using Pydantic.",
        citations=[],
    )

    outcomes.append(evidence_search_tool_call)
    outcomes.append(duplicate_evidence_search_tool_call)
    outcomes.append(answer)

    agent_provider = ScriptedAgentProvider(outcomes=outcomes)
    limits = LoopLimits()
    result = asyncio.run(
        run_agent(
            question="How does FastAPI validate request bodies?",
            provider=agent_provider,
            tool_executor=execute_tool_async,
            limits=limits,
        )
    )

    assert isinstance(result, AgentLoopError)
    assert result.code == "repeated_tool_call"
    assert result.retryable is False


def test_run_agent_rejects_exceeding_loop_limits() -> None:
    outcomes = []

    evidence_search_tool_call = ToolRequest(
        kind="tool_request",
        tool_name="evidence_search",
        raw_arguments={"query": "FastAPI", "result_limit": 3},
    )
    second_evidence_search_tool_call = ToolRequest(
        kind="tool_request",
        tool_name="evidence_search",
        raw_arguments={"query": "Second Fast API", "result_limit": 3},
    )

    third_evidence_search_tool_call = ToolRequest(
        kind="tool_request",
        tool_name="evidence_search",
        raw_arguments={"query": "Third Fast API", "result_limit": 3},
    )

    fourth_evidence_search_tool_call = ToolRequest(
        kind="tool_request",
        tool_name="evidence_search",
        raw_arguments={"query": "Fourth Fast API", "result_limit": 3},
    )

    answer = FinalAnswer(
        kind="final_answer",
        answer="FastAPI validates request bodies using Pydantic.",
        citations=[],
    )
    outcomes.append(evidence_search_tool_call)
    outcomes.append(second_evidence_search_tool_call)
    outcomes.append(third_evidence_search_tool_call)
    outcomes.append(fourth_evidence_search_tool_call)
    outcomes.append(answer)

    agent_provider = ScriptedAgentProvider(outcomes=outcomes)
    limits = LoopLimits()
    result = asyncio.run(
        run_agent(
            question="How does FastAPI validate request bodies?",
            provider=agent_provider,
            tool_executor=execute_tool_async,
            limits=limits,
        )
    )

    assert isinstance(result, AgentLoopError)
    assert result.code == "tool_call_limit_exceeded"


def test_run_agent_rejects_exceeding_iteration_limit() -> None:
    outcomes = []

    evidence_search_tool_call = ToolRequest(
        kind="tool_request",
        tool_name="evidence_search",
        raw_arguments={"query": "FastAPI", "result_limit": 3},
    )
    second_evidence_search_tool_call = ToolRequest(
        kind="tool_request",
        tool_name="evidence_search",
        raw_arguments={"query": "Second Fast API", "result_limit": 3},
    )

    third_evidence_search_tool_call = ToolRequest(
        kind="tool_request",
        tool_name="evidence_search",
        raw_arguments={"query": "Third Fast API", "result_limit": 3},
    )

    fourth_evidence_search_tool_call = ToolRequest(
        kind="tool_request",
        tool_name="evidence_search",
        raw_arguments={"query": "Fourth Fast API", "result_limit": 3},
    )

    answer = FinalAnswer(
        kind="final_answer",
        answer="FastAPI validates request bodies using Pydantic.",
        citations=[],
    )
    outcomes.append(evidence_search_tool_call)
    outcomes.append(second_evidence_search_tool_call)
    outcomes.append(third_evidence_search_tool_call)
    outcomes.append(fourth_evidence_search_tool_call)
    outcomes.append(answer)

    agent_provider = ScriptedAgentProvider(outcomes=outcomes)
    limits = LoopLimits(max_tool_calls=4, max_iterations=4)
    result = asyncio.run(
        run_agent(
            question="How does FastAPI validate request bodies?",
            provider=agent_provider,
            tool_executor=execute_tool_async,
            limits=limits,
        )
    )

    assert isinstance(result, AgentLoopError)
    assert result.code == "iteration_limit_exceeded"


def test_run_agent_rejects_unknown_tools() -> None:
    outcomes = []

    unknown_tool_request = ToolRequest(
        kind="tool_request",
        tool_name="fake_tool",
        raw_arguments={},
    )

    answer = FinalAnswer(
        kind="final_answer",
        answer="FastAPI validates request bodies using Pydantic.",
        citations=[],
    )
    outcomes.append(unknown_tool_request)
    outcomes.append(answer)

    agent_provider = ScriptedAgentProvider(outcomes=outcomes)
    limits = LoopLimits(max_tool_calls=4, max_iterations=4)
    result = asyncio.run(
        run_agent(
            question="How does FastAPI validate request bodies?",
            provider=agent_provider,
            tool_executor=execute_tool_async,
            limits=limits,
        )
    )

    assert isinstance(result, ToolError)
    assert result.code == "tool_not_allowed"
    assert result.retryable is False


def test_run_agent_allows_one_malformed_argument_correction() -> None:
    answer = FinalAnswer(
        kind="final_answer",
        answer="FastAPI validates request bodies using Pydantic.",
        citations=[],
    )
    agent_provider = ScriptedAgentProvider(
        outcomes=[
            ToolRequest(
                kind="tool_request",
                tool_name="evidence_search",
                raw_arguments={"result_limit": 3},
            ),
            ToolRequest(
                kind="tool_request",
                tool_name="evidence_search",
                raw_arguments={"query": "FastAPI", "result_limit": 3},
            ),
            answer,
        ]
    )

    result = asyncio.run(
        run_agent(
            question="How does FastAPI validate request bodies?",
            provider=agent_provider,
            tool_executor=execute_tool_async,
            limits=LoopLimits(),
        )
    )

    assert result == answer


def test_run_agent_rejects_second_malformed_argument_request() -> None:
    answer = FinalAnswer(
        kind="final_answer",
        answer="This answer must not be reached.",
        citations=[],
    )
    agent_provider = ScriptedAgentProvider(
        outcomes=[
            ToolRequest(
                kind="tool_request",
                tool_name="evidence_search",
                raw_arguments={"result_limit": 3},
            ),
            ToolRequest(
                kind="tool_request",
                tool_name="evidence_search",
                raw_arguments={"query": 42, "result_limit": 3},
            ),
            answer,
        ]
    )

    result = asyncio.run(
        run_agent(
            question="How does FastAPI validate request bodies?",
            provider=agent_provider,
            tool_executor=execute_tool_async,
            limits=LoopLimits(),
        )
    )

    assert isinstance(result, AgentLoopError)
    assert result.code == "argument_correction_limit_exceeded"
    assert result.retryable is False


async def slow_tool_executor(tool_name: str, raw_arguments: object):
    await asyncio.sleep(0.05)
    return await execute_tool_async(tool_name=tool_name, raw_arguments=raw_arguments)


def test_run_agent_rejects_tool_timeout() -> None:
    answer = FinalAnswer(
        kind="final_answer",
        answer="This answer must not be reached.",
        citations=[],
    )
    agent_provider = ScriptedAgentProvider(
        outcomes=[
            ToolRequest(
                kind="tool_request",
                tool_name="evidence_search",
                raw_arguments={"query": "FastAPI", "result_limit": 3},
            ),
            answer,
        ]
    )

    result = asyncio.run(
        run_agent(
            question="How does FastAPI validate request bodies?",
            provider=agent_provider,
            tool_executor=slow_tool_executor,
            limits=LoopLimits(tool_timeout_seconds=0.001),
        )
    )

    assert isinstance(result, AgentLoopError)
    assert result.code == "tool_timeout"
    assert result.retryable is False


class SlowProvider:
    def __init__(self, outcomes: list[AgentAction]):
        self.outcomes = outcomes

    async def generate(
        self, question: str, tool_results: tuple[ToolExecutionResult, ...]
    ) -> FinalAnswer:
        await asyncio.sleep(0.05)
        return self.outcomes.pop(0)


def test_run_agent_rejects_model_timeout() -> None:
    answer = FinalAnswer(
        kind="final_answer",
        answer="This answer must not be reached.",
        citations=[],
    )
    agent_provider = SlowProvider(
        outcomes=[
            answer,
        ]
    )

    result = asyncio.run(
        run_agent(
            question="How does FastAPI validate request bodies?",
            provider=agent_provider,
            tool_executor=execute_tool_async,
            limits=LoopLimits(model_timeout_seconds=0.001),
        )
    )

    assert isinstance(result, AgentLoopError)
    assert result.code == "model_timeout"
    assert result.retryable is False


def test_run_agent_rejects_overall_timeout() -> None:
    answer = FinalAnswer(
        kind="final_answer",
        answer="This answer must not be reached.",
        citations=[],
    )
    agent_provider = SlowProvider(
        outcomes=[
            answer,
        ]
    )

    result = asyncio.run(
        run_agent(
            question="How does FastAPI validate request bodies?",
            provider=agent_provider,
            tool_executor=execute_tool_async,
            limits=LoopLimits(model_timeout_seconds=1.0, overall_timeout_seconds=0.001),
        )
    )

    assert isinstance(result, AgentLoopError)
    assert result.code == "overall_timeout"
    assert result.retryable is False
