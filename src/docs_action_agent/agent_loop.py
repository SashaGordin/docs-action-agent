import asyncio
from typing import Annotated, Literal, Protocol

from pydantic import BaseModel, Field, HttpUrl, StringConstraints

from docs_action_agent.tools import EvidenceSearchResult, SourceLookupResult, ToolError

type ToolExecutionResult = (EvidenceSearchResult | SourceLookupResult | ToolError)


class Citation(BaseModel):
    chunk_id: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=128)
    ]
    source_title: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)
    ]
    source_url: HttpUrl
    excerpt: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=1000)
    ]


class LoopLimits(BaseModel):
    max_tool_calls: int = Field(
        default=3,
        ge=1,
        strict=True,
    )
    max_iterations: int = Field(default=4, ge=1, strict=True)
    tool_timeout_seconds: float = Field(default=5.0, gt=0, strict=True)
    model_timeout_seconds: float = Field(default=45.0, gt=0, strict=True)
    overall_timeout_seconds: float = Field(default=120.0, gt=0, strict=True)


class FinalAnswer(BaseModel):
    kind: Literal["final_answer"]
    answer: str
    citations: list[Citation]


class ToolRequest(BaseModel):
    kind: Literal["tool_request"]
    tool_name: str
    raw_arguments: object


class AgentLoopError(BaseModel):
    kind: Literal["loop_error"]
    code: Literal[
        "repeated_tool_call",
        "tool_call_limit_exceeded",
        "iteration_limit_exceeded",
        "argument_correction_limit_exceeded",
        "tool_timeout",
        "model_timeout",
        "overall_timeout",
    ]
    message: str
    retryable: Literal[False]


type AgentAction = ToolRequest | FinalAnswer

type AgentOutcome = FinalAnswer | AgentLoopError | ToolError


class ToolExecutor(Protocol):
    async def __call__(
        self, tool_name: str, raw_arguments: object
    ) -> ToolExecutionResult: ...


class AgentProvider(Protocol):
    async def generate(
        self, question: str, tool_results: tuple[ToolExecutionResult, ...]
    ) -> AgentAction: ...


async def _run_agent_loop(
    question: str,
    provider: AgentProvider,
    tool_executor: ToolExecutor,
    limits: LoopLimits,
) -> AgentOutcome:
    argument_correction_count = 0
    tool_call_count = 0
    iteration_count = 0
    tool_results = ()
    seen_tool_requests: list[ToolRequest] = []
    while True:
        if iteration_count >= limits.max_iterations:
            return AgentLoopError(
                kind="loop_error",
                code="iteration_limit_exceeded",
                message="The model exceeded the iteration call limit.",
                retryable=False,
            )
        iteration_count += 1
        try:
            action = await asyncio.wait_for(
                provider.generate(
                    question=question,
                    tool_results=tool_results,
                ),
                timeout=limits.model_timeout_seconds,
            )
        except TimeoutError:
            return AgentLoopError(
                kind="loop_error",
                code="model_timeout",
                message="The model call timed out.",
                retryable=False,
            )
        if isinstance(action, FinalAnswer):
            return action
        else:
            if action in seen_tool_requests:
                return AgentLoopError(
                    kind="loop_error",
                    code="repeated_tool_call",
                    message="The model repeated an identical tool request.",
                    retryable=False,
                )
            if tool_call_count >= limits.max_tool_calls:
                return AgentLoopError(
                    kind="loop_error",
                    code="tool_call_limit_exceeded",
                    message="The model exceeded the tool call limit.",
                    retryable=False,
                )
            tool_call_count += 1
            try:
                tool_result = await asyncio.wait_for(
                    tool_executor(
                        tool_name=action.tool_name,
                        raw_arguments=action.raw_arguments,
                    ),
                    timeout=limits.tool_timeout_seconds,
                )
            except TimeoutError:
                return AgentLoopError(
                    kind="loop_error",
                    code="tool_timeout",
                    message="The tool execution timed out.",
                    retryable=False,
                )
            if (
                isinstance(tool_result, ToolError)
                and tool_result.code == "tool_not_allowed"
            ):
                return tool_result
            if (
                isinstance(tool_result, ToolError)
                and tool_result.code == "invalid_arguments"
            ):
                if argument_correction_count >= 1:
                    return AgentLoopError(
                        kind="loop_error",
                        code="argument_correction_limit_exceeded",
                        message="The model exceeded the argument correction limit.",
                        retryable=False,
                    )
                argument_correction_count += 1
            tool_results = tool_results + (tool_result,)
            seen_tool_requests.append(action)


async def run_agent(
    question: str,
    provider: AgentProvider,
    tool_executor: ToolExecutor,
    limits: LoopLimits,
) -> AgentOutcome:
    try:
        return await asyncio.wait_for(
            _run_agent_loop(
                question=question,
                provider=provider,
                tool_executor=tool_executor,
                limits=limits,
            ),
            timeout=limits.overall_timeout_seconds,
        )
    except TimeoutError:
        return AgentLoopError(
            kind="loop_error",
            code="overall_timeout",
            message="The overall agent request timed out.",
            retryable=False,
        )
